/*
 * memwatchd.c — Memory file watcher daemon
 *
 * Watches workspace/memory/*.md and MEMORY.md for changes using Linux inotify.
 * On change, debounces 10 seconds then runs graph_refresh.py --quiet.
 *
 * Design:
 *   - Single-threaded, event-driven via inotify + select()
 *   - Zero heap allocation after init
 *   - No external dependencies (Linux inotify, POSIX only)
 *   - Graceful shutdown on SIGTERM/SIGINT
 *   - Writes PID file for process management
 *   - Logs to stderr (redirect to file if needed)
 *
 * Build:
 *   gcc -O2 -o memwatchd memwatchd.c
 *
 * Run:
 *   ./memwatchd &
 *   ./memwatchd /path/to/workspace   # explicit workspace path
 *
 * Stop:
 *   kill $(cat /tmp/memwatchd.pid)
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <errno.h>
#include <time.h>
#include <sys/inotify.h>
#include <sys/select.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <limits.h>

#define PID_FILE        "/tmp/memwatchd.pid"
#define DEBOUNCE_SECS   10
#define EVENT_BUF_LEN   (1024 * (sizeof(struct inotify_event) + NAME_MAX + 1))
#define MAX_WATCH_DIRS  4

static volatile sig_atomic_t g_running = 1;
static volatile sig_atomic_t g_pending = 0;  /* pending refresh */
static time_t g_last_trigger = 0;

static void handle_signal(int sig) {
    (void)sig;
    g_running = 0;
}

static void write_pid(void) {
    FILE *f = fopen(PID_FILE, "w");
    if (f) {
        fprintf(f, "%d\n", (int)getpid());
        fclose(f);
    }
}

static void remove_pid(void) {
    unlink(PID_FILE);
}

static int ends_with_md(const char *name) {
    size_t n = strlen(name);
    return n >= 3 && strcmp(name + n - 3, ".md") == 0;
}

static void run_refresh(const char *workspace) {
    char script[PATH_MAX];
    snprintf(script, sizeof(script),
             "%s/memory-upgrade/graph_refresh.py", workspace);

    /* Check script exists */
    struct stat st;
    if (stat(script, &st) != 0) {
        fprintf(stderr, "[memwatchd] refresh script not found: %s\n", script);
        return;
    }

    pid_t pid = fork();
    if (pid < 0) {
        fprintf(stderr, "[memwatchd] fork failed: %s\n", strerror(errno));
        return;
    }

    if (pid == 0) {
        /* Child: redirect stdout/stderr to /dev/null for quiet operation */
        int devnull = open("/dev/null", O_WRONLY);
        if (devnull >= 0) {
            dup2(devnull, STDOUT_FILENO);
            dup2(devnull, STDERR_FILENO);
            close(devnull);
        }

        /* Find python3 */
        char *python = "/home/node/.local/bin/python3";
        struct stat ps;
        if (stat(python, &ps) != 0) {
            python = "/usr/bin/python3";
        }

        execl(python, "python3", script, "--quiet", (char *)NULL);
        _exit(127);
    }

    /* Parent: reap child non-blocking (don't wait — fire and forget) */
    /* We'll reap zombies in the main loop via waitpid(-1, WNOHANG) */
    fprintf(stderr, "[memwatchd] refresh triggered (pid %d)\n", (int)pid);
}

int main(int argc, char *argv[]) {
    const char *workspace = "/home/node/.openclaw/workspace";
    if (argc >= 2) {
        workspace = argv[1];
    }

    fprintf(stderr, "[memwatchd] starting, workspace=%s\n", workspace);
    fprintf(stderr, "[memwatchd] pid=%d\n", (int)getpid());

    /* Signal handlers */
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_handler = handle_signal;
    sigaction(SIGTERM, &sa, NULL);
    sigaction(SIGINT,  &sa, NULL);

    /* Ignore SIGCHLD to auto-reap, or handle explicitly */
    signal(SIGCHLD, SIG_DFL);  /* we'll waitpid manually */

    write_pid();
    atexit(remove_pid);

    /* Set up inotify */
    int ifd = inotify_init1(IN_NONBLOCK | IN_CLOEXEC);
    if (ifd < 0) {
        fprintf(stderr, "[memwatchd] inotify_init1 failed: %s\n", strerror(errno));
        return 1;
    }

    uint32_t mask = IN_CLOSE_WRITE | IN_MOVED_TO | IN_CREATE;

    /* Watch workspace root (for MEMORY.md, USER.md, etc.) */
    char watch_dirs[MAX_WATCH_DIRS][PATH_MAX];
    int wd[MAX_WATCH_DIRS];
    int nwatch = 0;

    snprintf(watch_dirs[nwatch], PATH_MAX, "%s", workspace);
    wd[nwatch] = inotify_add_watch(ifd, watch_dirs[nwatch], mask);
    if (wd[nwatch] >= 0) {
        fprintf(stderr, "[memwatchd] watching %s\n", watch_dirs[nwatch]);
        nwatch++;
    }

    /* Watch memory/ subdirectory */
    snprintf(watch_dirs[nwatch], PATH_MAX, "%s/memory", workspace);
    wd[nwatch] = inotify_add_watch(ifd, watch_dirs[nwatch], mask);
    if (wd[nwatch] >= 0) {
        fprintf(stderr, "[memwatchd] watching %s\n", watch_dirs[nwatch]);
        nwatch++;
    } else {
        fprintf(stderr, "[memwatchd] warning: %s/memory not found (will retry)\n", workspace);
    }

    if (nwatch == 0) {
        fprintf(stderr, "[memwatchd] no watch dirs available, exiting\n");
        close(ifd);
        return 1;
    }

    char buf[EVENT_BUF_LEN] __attribute__((aligned(__alignof__(struct inotify_event))));

    fprintf(stderr, "[memwatchd] ready, debounce=%ds\n", DEBOUNCE_SECS);

    while (g_running) {
        /* Reap any finished children */
        while (waitpid(-1, NULL, WNOHANG) > 0) {}

        /* Fire pending refresh if debounce elapsed */
        if (g_pending) {
            time_t now = time(NULL);
            if (now - g_last_trigger >= DEBOUNCE_SECS) {
                g_pending = 0;
                run_refresh(workspace);
            }
        }

        /* select() with 1-second timeout to handle debounce + signals */
        fd_set rfds;
        FD_ZERO(&rfds);
        FD_SET(ifd, &rfds);
        struct timeval tv = { .tv_sec = 1, .tv_usec = 0 };

        int ret = select(ifd + 1, &rfds, NULL, NULL, &tv);
        if (ret < 0) {
            if (errno == EINTR) continue;
            fprintf(stderr, "[memwatchd] select error: %s\n", strerror(errno));
            break;
        }
        if (ret == 0) continue;  /* timeout — loop back to check debounce */

        /* Read inotify events */
        ssize_t len = read(ifd, buf, sizeof(buf));
        if (len < 0) {
            if (errno == EINTR || errno == EAGAIN) continue;
            fprintf(stderr, "[memwatchd] read error: %s\n", strerror(errno));
            break;
        }

        const struct inotify_event *event;
        for (char *ptr = buf; ptr < buf + len;
             ptr += sizeof(struct inotify_event) + event->len) {
            event = (const struct inotify_event *)ptr;

            if (event->len == 0) continue;
            if (!ends_with_md(event->name)) continue;
            if (event->mask & IN_ISDIR) continue;

            fprintf(stderr, "[memwatchd] change detected: %s\n", event->name);
            g_pending = 1;
            g_last_trigger = time(NULL);
        }
    }

    fprintf(stderr, "[memwatchd] shutting down\n");
    close(ifd);
    return 0;
}

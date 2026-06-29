/*
 * bench_small.c — hipool 小数据量基准 (无 eviction)
 * Compile: gcc -O2 -DTEST_MODE bench_small.c -o bench_small
 */
#define _POSIX_C_SOURCE 200809L
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include "memory.c"

#define N 1000

static uint64_t ns(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return (uint64_t)t.tv_sec * 1000000000UL + (uint64_t)t.tv_nsec;
}
static char rc(void) { return "abcdefghijklmnopqrstuvwxyz0123456789"[rand()%36]; }

static int cmp64(const void *a, const void *b) {
    uint64_t x=*(uint64_t*)a, y=*(uint64_t*)b; return (x>y)-(x<y);
}

static void bench(int vs, const char *label) {
    system("rm -rf /tmp/hb_small");
    MemoryCtx ctx;
    memory_init(&ctx, "/tmp/hb_small", 7);
    uint64_t *s_set = (uint64_t*)calloc(N, 8);
    uint64_t *s_get = (uint64_t*)calloc(N, 8);
    char k[64], v[16384];
    const char *tags[] = {"b"};
    uint64_t base = (uint64_t)time(NULL) - 86400*30;

    for (int i = 0; i < N; i++) {
        snprintf(k, 64, "%016d", i);
        for (int j = 0; j < vs-1; j++) v[j] = rc();
        v[vs-1] = 0;
        uint64_t t0 = ns();
        memory_set_with_ts(&ctx, k, v, tags, 1, base + (uint64_t)i*60);
        s_set[i] = ns() - t0;
    }
    for (int i = 0; i < N; i++) {
        snprintf(k, 64, "%016d", i);
        uint64_t t0 = ns();
        memory_get(&ctx, k);
        s_get[i] = ns() - t0;
    }

    qsort(s_set, N, 8, cmp64);
    qsort(s_get, N, 8, cmp64);
    double avg_set=0, avg_get=0;
    for (int i = 0; i < N; i++) { avg_set += s_set[i]; avg_get += s_get[i]; }
    avg_set /= N; avg_get /= N;

    printf("HIPOOL,SET,%s,%d,%.0f,%lu,%lu,%lu\n",
           label, vs, N, avg_set, s_set[(int)(N*0.5)], s_set[(int)(N*0.9)], s_set[(int)(N*0.99)]);
    printf("HIPOOL,GET,%s,%d,%.0f,%lu,%lu,%lu\n",
           label, vs, N, avg_get, s_get[(int)(N*0.5)], s_get[(int)(N*0.9)], s_get[(int)(N*0.99)]);

    free(s_set); free(s_get);
    memory_destroy(&ctx);
    system("rm -rf /tmp/hb_small");
}

int main(void) {
    srand((unsigned)time(NULL));
    bench(32,  "N=1000");
    bench(256, "N=1000");
    bench(1024,"N=1000");
    bench(4096,"N=1000");
    return 0;
}

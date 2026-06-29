/*
 * bench_compare.c — hipool vs LMDB vs SQLite 统一基准
 * 与 bench_lmdb.py 使用相同参数: N=50000, val_sizes=[32,256,1024,4096]
 * Compile: gcc -O2 -DTEST_MODE bench_compare.c -o bench_compare
 * 然后 python3 bench_lmdb.py 对比
 */

#define _POSIX_C_SOURCE 200809L
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h>

#include "memory.c"

#define N 50000
#define KEY_LEN 16

static inline uint64_t ns_now(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000UL + (uint64_t)ts.tv_nsec;
}

typedef struct { uint64_t *vals; int cap, n; } Samples;
static void s_init(Samples *s, int m) { s->vals = (uint64_t*)calloc(m,8); s->cap=m; s->n=0; }
static void s_add(Samples *s, uint64_t v) { if (s->n < s->cap) s->vals[s->n++] = v; }
static void s_free(Samples *s) { free(s->vals); }
static int cmp64(const void *a, const void *b) { uint64_t x=*(uint64_t*)a,y=*(uint64_t*)b; return (x>y)-(x<y); }

static void s_report(Samples *s, const char *label, int val_sz) {
    if (!s->n) { printf("  %s,val=%d,(no data)\n", label, val_sz); return; }
    qsort(s->vals, s->n, 8, cmp64);
    uint64_t p50=s->vals[(int)(s->n*0.50)], p90=s->vals[(int)(s->n*0.90)],
             p99=s->vals[(int)(s->n*0.99)], p999=s->vals[(int)(s->n*0.999)];
    uint64_t mn=s->vals[0], mx=s->vals[s->n-1];
    double avg=0; for(int i=0;i<s->n;i++)avg+=s->vals[i]; avg/=s->n;
    /* CSV-like output for easy parsing */
    printf("HIPOOL,%s,%d,%d,%.0f,%lu,%lu,%lu,%lu,%lu,%lu\n",
           label, val_sz, s->n, avg, p50, p90, p99, p999, mn, mx);
}

static char rc(void) { return "abcdefghijklmnopqrstuvwxyz0123456789"[rand()%36]; }
static void gen_key(char *b, int seq) {
    snprintf(b, KEY_LEN+1, "%016d", seq);
}
static void gen_val(char *b, int len) {
    for(int i=0;i<len-1;i++) b[i]=rc();
    b[len-1]=0;
}

static MemoryCtx *hipool_new(void) {
    system("rm -rf /tmp/bench_hipool");
    MemoryCtx *c = (MemoryCtx*)calloc(1, sizeof(MemoryCtx));
    memory_init(c, "/tmp/bench_hipool", 7);
    return c;
}
static void hipool_free(MemoryCtx *c) {
    memory_flush(c);
    memory_destroy(c);
    free(c);
    system("rm -rf /tmp/bench_hipool");
}

static void bench_hipool(int val_sz) {
    MemoryCtx *ctx = hipool_new();
    Samples s_set, s_get;
    s_init(&s_set, N); s_init(&s_get, N);
    char key[64], val[16384];
    const char *tags[]={"bench"};
    uint64_t base = (uint64_t)time(NULL) - 86400*60;

    /* SET */
    for (int i = 0; i < N; i++) {
        gen_key(key, i);
        if (val_sz <= (int)sizeof(val)) gen_val(val, val_sz);
        else gen_val(val, sizeof(val));
        uint64_t t0 = ns_now();
        memory_set_with_ts(ctx, key, val, tags, 1, base + (uint64_t)i);
        s_add(&s_set, ns_now() - t0);
    }

    /* GET */
    for (int i = 0; i < N; i++) {
        gen_key(key, i);
        uint64_t t0 = ns_now();
        memory_get(ctx, key);
        s_add(&s_get, ns_now() - t0);
    }

    s_report(&s_set, "SET", val_sz);
    s_report(&s_get, "GET", val_sz);
    s_free(&s_set); s_free(&s_get);
    hipool_free(ctx);
}

int main(void) {
    srand((unsigned)time(NULL));
    int val_sizes[] = {32, 256, 1024, 4096};
    int n_sizes = 4;

    for (int si = 0; si < n_sizes; si++) {
        bench_hipool(val_sizes[si]);
    }

    return 0;
}

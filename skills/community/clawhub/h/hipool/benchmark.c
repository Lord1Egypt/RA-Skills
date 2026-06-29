/*
 * benchmark.c — hipool 综合性能基准测试 v3
 * Fix: 交错的 timestamp + 更小 N 以适配 2MB 池
 * Compile: gcc -O2 -DTEST_MODE benchmark.c -o bench_micro
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

static void s_report(Samples *s, const char *label) {
    if (!s->n) { printf("  %-40s (no data)\n", label); return; }
    qsort(s->vals, s->n, 8, cmp64);
    uint64_t p50=s->vals[(int)(s->n*0.50)], p90=s->vals[(int)(s->n*0.90)],
             p99=s->vals[(int)(s->n*0.99)], p999=s->vals[(int)(s->n*0.999)];
    uint64_t mn=s->vals[0], mx=s->vals[s->n-1];
    double avg=0; for(int i=0;i<s->n;i++)avg+=s->vals[i]; avg/=s->n;
    printf("  %-40s n=%-5d avg=%-8.0fns p50=%-6lu p90=%-6lu p99=%-6lu p999=%-6lu min=%-6lu max=%-8lu\n",
           label, s->n, avg, p50, p90, p99, p999, mn, mx);
}

static char rc(void) { return "abcdefghijklmnopqrstuvwxyz0123456789"[rand()%36]; }
static void gk(char *b, int seq, int len) {
    snprintf(b, len, "b_%d_", seq); int base=(int)strlen(b);
    for(int i=base;i<len-1;i++) b[i]=rc(); b[len-1]=0;
}
static void gv(char *b, int len) { for(int i=0;i<len-1;i++) b[i]=rc(); b[len-1]=0; }

static MemoryCtx *mk(const char *n) {
    char d[256]; snprintf(d,256,"/tmp/bm_%s",n); system("rm -rf /tmp/bm_*");
    MemoryCtx *c=calloc(1,sizeof(MemoryCtx)); memory_init(c,d,7); return c;
}
static void fr(MemoryCtx *c) { memory_flush(c); memory_destroy(c); free(c); }

/* ============================================================
 * 微基准: 交错的 ts 确保 eviction 能工作
 * ============================================================ */
static void bench(int val_sz, const char *label, int n) {
    MemoryCtx *ctx = mk("b");
    Samples s_set, s_get;
    s_init(&s_set, n); s_init(&s_get, n);
    char key[64], val[16384];
    const char *tags[]={"bench"};
    uint64_t base = (uint64_t)time(NULL) - 86400*30; /* 30 天前开始 */

    for (int i = 0; i < n; i++) {
        gk(key, i, 32); gv(val, val_sz);
        uint64_t ts = base + (uint64_t)i * 60; /* 每分钟一条 => 跨天 */
        uint64_t t0 = ns_now();
        memory_set_with_ts(ctx, key, val, tags, 1, ts);
        s_add(&s_set, ns_now() - t0);
    }
    for (int i = 0; i < n; i++) {
        snprintf(key, 64, "b_%d_", i);
        uint64_t t0 = ns_now();
        memory_get(ctx, key);
        s_add(&s_get, ns_now() - t0);
    }
    printf("\n--- %s (val=%dB, n=%d) ---\n", label, val_sz, n);
    s_report(&s_set, "SET"); s_report(&s_get, "GET");
    s_free(&s_set); s_free(&s_get);
    fr(ctx);
}

/* ============================================================
 * 混合读写 70%R/30%W
 * ============================================================ */
static void bench_mixed(void) {
    MemoryCtx *ctx = mk("mix");
    int n = 5000;
    Samples s; s_init(&s, n);
    char key[64], val[256];
    const char *tags[]={"bench"};
    uint64_t base = (uint64_t)time(NULL) - 86400*30;

    for (int i = 0; i < n/2; i++) {
        gk(key, i, 32); gv(val, 128);
        memory_set_with_ts(ctx, key, val, tags, 1, base + (uint64_t)i*120);
    }
    for (int i = 0; i < n; i++) {
        int idx = rand() % (n/2);
        snprintf(key, 64, "b_%d_", idx);
        uint64_t t0 = ns_now();
        if (rand() % 10 < 7) memory_get(ctx, key);
        else { gv(val, 128); memory_set_with_ts(ctx, key, val, tags, 1, base + (uint64_t)(n/2+i)*120); }
        s_add(&s, ns_now() - t0);
    }
    printf("\n--- Mixed 70%%R/30%%W (256B, n=%d) ---\n", n);
    s_report(&s, "Combined");
    s_free(&s); fr(ctx);
}

/* ============================================================
 * 端到端
 * ============================================================ */
static void bench_e2e(void) {
    MemoryCtx *ctx = mk("e2e");
    int n = 3000;
    Samples s; s_init(&s, n);
    char key[64], val[4096];
    const char *tags[]={"e2e","test","demo"};
    uint64_t base = (uint64_t)time(NULL) - 86400*30;

    for (int i = 0; i < n; i++) {
        gk(key, 64, i); gv(val, 256);
        uint64_t t0 = ns_now();
        memory_set_with_ts(ctx, key, val, tags, 3, base + (uint64_t)i*60);
        s_add(&s, ns_now() - t0);
    }
    printf("\n--- End-to-End (3 tags, 256B val, n=%d) ---\n", n);
    s_report(&s, "E2E write");
    s_free(&s); fr(ctx);
}

/* ============================================================
 * 去重效率
 * ============================================================ */
static void bench_dedup(void) {
    MemoryCtx *ctx = mk("dedup");
    int n = 3000, skip = 0;
    Samples s; s_init(&s, n*2);
    char key[64], val[256];
    const char *tags[]={"dedup"};
    uint64_t base = (uint64_t)time(NULL) - 86400;

    for (int p = 0; p < 2; p++) {
        for (int i = 0; i < n; i++) {
            snprintf(key, 64, "2026-06-05-%d", i);
            gv(val, 200);
            uint64_t t0 = ns_now();
            int rc = memory_set_with_ts(ctx, key, val, tags, 1, base + (uint64_t)i*10);
            s_add(&s, ns_now() - t0);
            if (rc == -2) skip++;
        }
    }
    printf("\n--- Dedup Efficiency (n=%d*2, skipped=%d/%d) ---\n", n, skip, n*2);
    s_report(&s, "SET (with dedup)");
    s_free(&s); fr(ctx);
}

/* ============================================================
 * Eviction 压力测试
 * ============================================================ */
static void bench_evict(void) {
    MemoryCtx *ctx = mk("evict");
    Samples s1, s2; s_init(&s1, 500); s_init(&s2, 500);
    char key[64], val[64];
    const char *tags[]={"evict"};
    uint64_t base = (uint64_t)time(NULL) - 86400*60;

    for (int i = 0; i < 5000; i++) {
        gk(key, i, 32); gv(val, 48);
        uint64_t ts = base + (uint64_t)i * 300; /* 5分钟一条 => 跨 ~17天 */
        uint64_t t0 = ns_now();
        memory_set_with_ts(ctx, key, val, tags, 1, ts);
        uint64_t el = ns_now() - t0;
        if (i < 300) s_add(&s1, el);
        if (i >= 4500) s_add(&s2, el);
    }
    printf("\n--- Eviction (5000 entries, timestamp=300s gaps) ---\n");
    printf("  Watermark: %u%%  entries:%u\n", ctx->pool.wl, ctx->pool.ec);
    s_report(&s1, "SET first 300 (pre-evict)");
    s_report(&s2, "SET last 500 (post-evict)");
    s_free(&s1); s_free(&s2); fr(ctx);
}

/* ============================================================
 * Slab 时间分解
 * ============================================================ */
static void bench_slab(void) {
    printf("\n--- Slab Allocation Time Breakdown ---\n");
    int sz[]={32,64,128,256,512,1024,2048,4096,8192,12000};
    for(int si=0;si<10;si++){
        MemoryCtx *ctx = mk("slab");
        Samples s; s_init(&s, 2000);
        char k[64], v[16384];
        const char *tags[]={"slab"};
        uint64_t base = (uint64_t)time(NULL) - 86400*30;
        for(int i=0;i<2000;i++){
            snprintf(k,64,"s_%d_%d",si,i); gv(v,sz[si]);
            uint64_t t0=ns_now(); memory_set_with_ts(ctx,k,v,tags,1,base+(uint64_t)i*600);
            s_add(&s,ns_now()-t0);
        }
        char lb[64];
        snprintf(lb,64,"val=%dB (%s)",sz[si],sz[si]<=256?"256B slab":sz[si]<=1024?"1K slab":sz[si]<=4096?"4K slab":"16K slab");
        s_report(&s,lb);
        s_free(&s); fr(ctx);
    }
}

/* ============================================================
 * 入口
 * ============================================================ */
int main(void) {
    srand((unsigned)time(NULL));
    printf("═══════════════════════════════════════════════════════════\n");
    printf("  hipool Benchmark v3  |  Pool: %d KB\n", POOL_SIZE/1024);
    printf("═══════════════════════════════════════════════════════════\n");

    bench(32,    "Data size: 32B",    500);
    bench(256,   "Data size: 256B",   500);
    bench(1024,  "Data size: 1KB",    300);
    bench(4096,  "Data size: 4KB",    120);
    bench(16320, "Data size: 16KB",   40);

    bench_mixed();
    bench_e2e();
    bench_dedup();
    bench_evict();
    bench_slab();

    printf("\n═══════════════════════════════════════════════════════════\n");
    printf("  Done.\n");
    return 0;
}

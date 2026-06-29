/*
 * bench_v4.c — hipool benchmark, each test stays within single-slab capacity
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

static inline uint64_t ns(void) {
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts);
    return (uint64_t)ts.tv_sec*1000000000UL+(uint64_t)ts.tv_nsec;
}

typedef struct { uint64_t v[3000]; int n; } S;
static void sa(S *s, uint64_t v) { if(s->n<3000) s->v[s->n++]=v; }
static int cu(const void *a, const void *b) { uint64_t x=*(uint64_t*)a,y=*(uint64_t*)b; return (x>y)-(x<y); }
static void pr(S *s, const char *l) {
    if(!s->n)return;
    qsort(s->v,s->n,8,cu);
    double a=0; for(int i=0;i<s->n;i++)a+=s->v[i]; a/=s->n;
    uint64_t p50=s->v[(int)(s->n*0.5)],p99=s->v[(int)(s->n*0.99)];
    printf("  %-30s n=%-4d avg=%-8.0fns p50=%-6lu p99=%-8lu\n",l,s->n,a,p50,p99);
}

static char rc(void){return "abcdefghijklmnopqrstuvwxyz0123456789"[rand()%36];}
static void gk(char *b,int s){snprintf(b,64,"k_%d_",s);int n=strlen(b);for(int i=n;i<31;i++)b[i]=rc();b[31]=0;}
static void gv(char *b,int n){for(int i=0;i<n-1;i++)b[i]=rc();b[n-1]=0;}

int main(void) {
    srand(42);
    printf("═══ hipool Benchmark v4 ═══\n");
    printf("Pool: %d KB\n\n", POOL_SIZE/1024);

    /* Test each value size within slab capacity */
    struct {int size; int n; const char *label;} tests[] = {
        {32,    500, "32B (Slab_256)"},
        {256,   500, "256B (Slab_256)"},
        {512,   300, "512B (Slab_1K)"},
        {1024,  300, "1KB (Slab_1K)"},
        {2048,  100, "2KB (Slab_4K)"},
        {4096,  100, "4KB (Slab_4K)"},
        {8192,  40,  "8KB (Slab_16K)"},
        {12000, 40,  "12KB (Slab_16K)"},
    };
    int nt = sizeof(tests)/sizeof(tests[0]);

    for (int ti = 0; ti < nt; ti++) {
        int sz = tests[ti].size, n = tests[ti].n;
        S sset, sget; sset.n=sget.n=0;
        char dir[64]; snprintf(dir,64,"/tmp/bv4_%d",ti);
        system("rm -rf /tmp/bv4_*");
        MemoryCtx ctx; memory_init(&ctx,dir,7);
        char key[64], val[16384];
        const char *tags[]={"bt"};
        uint64_t base = (uint64_t)time(NULL) - 86400LL*60;

        for(int i=0;i<n;i++){
            gk(key,i); gv(val,sz);
            uint64_t ts = base + (uint64_t)i * 3600;
            uint64_t t0=ns(); memory_set_with_ts(&ctx,key,val,tags,1,ts);
            sa(&sset,ns()-t0);
        }
        for(int i=0;i<n;i++){
            snprintf(key,64,"k_%d_",i);
            uint64_t t0=ns(); memory_get(&ctx,key);
            sa(&sget,ns()-t0);
        }
        printf("%s (n=%d)\n", tests[ti].label, n);
        pr(&sset,"SET"); pr(&sget,"GET");
        memory_destroy(&ctx);
        printf("\n");
    }

    /* Mixed workload */
    {
        system("rm -rf /tmp/bv4_mix");
        MemoryCtx ctx; memory_init(&ctx,"/tmp/bv4_mix",7);
        S sm; sm.n=0; int n=5000;
        char key[64], val[256];
        const char *tags[]={"bt"};
        uint64_t base=(uint64_t)time(NULL)-86400LL*60;
        for(int i=0;i<n/2;i++){
            gk(key,i); gv(val,128);
            memory_set_with_ts(&ctx,key,val,tags,1,base+(uint64_t)i*60);
        }
        for(int i=0;i<n;i++){
            int idx=rand()%(n/2);
            snprintf(key,64,"k_%d_",idx);
            uint64_t t0=ns();
            if(rand()%10<7) memory_get(&ctx,key);
            else { gv(val,128); memory_set_with_ts(&ctx,key,val,tags,1,base+(uint64_t)(n/2+i)*60); }
            sa(&sm,ns()-t0);
        }
        printf("Mixed 70%%R/30%%W (256B, n=%d)\n", n);
        pr(&sm,"Combined");
        memory_destroy(&ctx);
        printf("\n");
    }

    /* Dedup */
    {
        system("rm -rf /tmp/bv4_dd");
        MemoryCtx ctx; memory_init(&ctx,"/tmp/bv4_dd",7);
        S sd; sd.n=0; int n=3000, skip=0;
        char key[64], val[256];
        const char *tags[]={"dd"};
        uint64_t base=(uint64_t)time(NULL)-86400LL;
        for(int p=0;p<2;p++){
            for(int i=0;i<n;i++){
                snprintf(key,64,"2026-06-05-%d",i);
                gv(val,200);
                uint64_t t0=ns();
                int rc=memory_set_with_ts(&ctx,key,val,tags,1,base+(uint64_t)i*10);
                sa(&sd,ns()-t0);
                if(rc==-2)skip++;
            }
        }
        printf("Dedup (n=%d*2, skipped=%d/%d)\n", n, skip, n*2);
        pr(&sd,"SET with dedup");
        memory_destroy(&ctx);
        printf("\n");
    }

    /* Eviction stress */
    {
        system("rm -rf /tmp/bv4_ev");
        MemoryCtx ctx; memory_init(&ctx,"/tmp/bv4_ev",7);
        S se1, se2; se1.n=se2.n=0;
        char key[64], val[64];
        const char *tags[]={"ev"};
        uint64_t base=(uint64_t)time(NULL)-86400LL*60;
        int n=8000;
        for(int i=0;i<n;i++){
            gk(key,i); gv(val,32);
            uint64_t ts=base+(uint64_t)i*120;
            uint64_t t0=ns();
            memory_set_with_ts(&ctx,key,val,tags,1,ts);
            uint64_t el=ns()-t0;
            if(i<300) sa(&se1,el);
            if(i>=n-300) sa(&se2,el);
        }
        printf("Eviction (n=%d, ts=120s gaps)\n", n);
        printf("  wl=%u%% ec=%u\n", ctx.pool.wl, ctx.pool.ec);
        pr(&se1,"SET first 300");
        pr(&se2,"SET last 300");
        memory_destroy(&ctx);
        printf("\n");
    }

    printf("═══ Done ═══\n");
    return 0;
}

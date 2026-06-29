/*
 * memory.c — 嵌入式 AI Agent 记忆系统
 *
 * 架构: 海马体-皮层双存储模型
 *   - 热内存池 (2MB, slab 分配器) → 短期记忆
 *   - 日文件溢出 (7天 TTL)         → 长期巩固
 *
 * 零外部依赖 (libc only). 编译:
 *   gcc -O2 memory.c -o memory
 *
 * 用法:
 *   memory set <key> <value> [--tags a,b,c]
 *   memory get <key>
 *   memory search <query|--tag <tag>|--date YYYY-MM-DD>
 *   memory del <key>
 *   memory flush / load / clean / stats
 */

#define _POSIX_C_SOURCE 200809L
#include <stdint.h>
#include <stddef.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <errno.h>
#include <unistd.h>

/* ============================================================
 * 可选多线程支持 (编译时开关)
 * 默认: 单线程零开销. 编译加 -DHIPOOL_USE_MUTEX -lpthread 启用.
 * ============================================================ */
#ifdef HIPOOL_USE_MUTEX
#include <pthread.h>
#define LOCK(c)   pthread_mutex_lock(&(c)->lock)
#define UNLOCK(c) pthread_mutex_unlock(&(c)->lock)
#else
#define LOCK(c)   ((void)0)
#define UNLOCK(c) ((void)0)
#endif

/* ============================================================
 * 常量 & 类型定义
 * ============================================================ */

#define POOL_SIZE        (2 * 1024 * 1024)
#define MAX_KEY_LEN      256
#define MAX_VAL_LEN      16320
#define MAX_TAGS         16
#define MAX_TAG_LEN      64
#define MAX_ENTRIES      4096
#define HASHTABLE_SIZE   4096
#define TAG_HASHTABLE_SIZE 512
#define EVICT_WATER      80
#define OVERFLOW_DIR     "memory_data"
#define FILE_TTL_DAYS    7
#define CANARY_MAGIC     0xDEADBEEF

/* ============================================================
 * Skip List (排序索引) 常量
 * ============================================================ */
#define SL_MAX_LEVEL     16
#define SL_PROB          4   /* 1/4 = 0.25 概率提升层级（更少指针开销） */

/* ============================================================
 * WAL (预写日志) 常量
 * ============================================================ */
#define WAL_MAGIC        0x57414C31UL  /* "WAL1" */
#define WAL_OP_SET       0x01
#define WAL_OP_DEL       0x02

typedef enum { SLAB_256=0, SLAB_1K=1, SLAB_4K=2, SLAB_16K=3, SLAB_LEVELS=4 } SlabLevel;
#define SLAB_SIZES { 256, 1024, 4096, 16384 }

#define FLAG_ACTIVE     0x01
#define FLAG_OVERFLOWED 0x02

typedef struct __attribute__((packed)) {
    uint32_t magic_start;
    uint32_t key_hash;
    uint16_t key_len;
    uint16_t val_len;
    uint8_t  tag_count;
    uint8_t  flags;
    uint8_t  _pad[2];
    uint64_t created_at;
    uint64_t accessed_at;
} MemEntry;

#define ENTRY_HEADER_SIZE  (sizeof(MemEntry) - sizeof(uint32_t))
#define ENTRY_DATA_OFFSET  sizeof(MemEntry)

static inline size_t entry_total_size(uint16_t kl, uint16_t vl, uint8_t tc) {
    return sizeof(MemEntry) + (size_t)(kl+1) + (size_t)(vl+1) + (size_t)tc * MAX_TAG_LEN;
}

typedef struct HashNode { uint32_t kh; MemEntry *e; struct HashNode *next; } HashNode;
typedef struct TagEntry { char tag[MAX_TAG_LEN]; MemEntry **es; uint32_t n, cap; struct TagEntry *next; } TagEntry;

typedef struct {
    uint8_t *base; size_t total, used; uint32_t ec;
    uint32_t so[4], ss[4], sc[4]; uint8_t *bm[4];
    uint64_t ta, tf; uint32_t wl;
} Pool;

typedef struct { HashNode *b[HASHTABLE_SIZE]; uint32_t cnt; } HashTable;
typedef struct { TagEntry *b[TAG_HASHTABLE_SIZE]; uint32_t cnt; } TagIndex;

/* ============================================================
 * Skip List (排序索引) 数据结构—定义在 MemoryCtx 之前
 * ============================================================ */
typedef struct SLNode {
    MemEntry *entry;
    uint64_t sort_key;          /* (created_at << 32) | (key_hash >> 32) 复合排序 */
    uint8_t level;
    struct SLNode *next[];      /* 柔性数组: level+1 个 forward 指针 */
} SLNode;

typedef struct {
    SLNode *head;                /* 哨兵节点 (含 SL_MAX_LEVEL 个 forward 指针) */
    int top_level;               /* 当前最高非空层 */
    uint32_t count;
} SkipList;

#define MAX_SHARDS 8
#define SHARD_POOL_SIZE (256 * 1024)

typedef struct MemoryCtx MemoryCtx;

typedef struct { char name[64]; MemoryCtx *ctx; } ShardEntry;

struct MemoryCtx {
    Pool pool; HashTable table; TagIndex tag_index; SkipList sorted;
    char data_dir[512]; int file_ttl, initialized, wal_disabled;
    ShardEntry shards[MAX_SHARDS]; int shard_count;
#ifdef HIPOOL_USE_MUTEX
    pthread_mutex_t lock;
#endif
};

typedef struct { char *k, *v, *ts; time_t ca; } SearchResult;

/* ============================================================
 * 工具函数
 * ============================================================ */

static uint32_t djb2(const char *s) {
    uint32_t h = 5381; int c;
    while ((c = (unsigned char)*s++)) h = ((h<<5)+h) + (uint32_t)c;
    return h;
}
static uint32_t djb2_n(const char *s, size_t n) {
    uint32_t h = 5381;
    for (size_t i=0; i<n && s[i]; i++) h = ((h<<5)+h) + (uint32_t)(unsigned char)s[i];
    return h;
}

/* ============================================================
 * 内存池 (pool)
 * ============================================================ */

static inline size_t bm_bytes(uint32_t n) { return (n+7)/8; }
static inline int bm_test(const uint8_t *bm, uint32_t i) { return (bm[i/8]>>(i%8))&1; }
static inline void bm_set(uint8_t *bm, uint32_t i) { bm[i/8] |= (1<<(i%8)); }
static inline void bm_clear(uint8_t *bm, uint32_t i) { bm[i/8] &= ~(1<<(i%8)); }

static int bm_find0(const uint8_t *bm, uint32_t n) {
    for (uint32_t i=0; i<n; i++) if (!bm_test(bm,i)) return (int)i;
    return -1;
}

static int pool_init(Pool *p, size_t sz) {
    p->base = (uint8_t*)calloc(1,sz);
    if (!p->base) return -1;
    p->total = sz; p->used = 0; p->ec = 0; p->ta = p->tf = 0; p->wl = 0;
    double ratios[4] = {0.10, 0.20, 0.30, 0.40};
    size_t off = 0;
    uint32_t sizes[] = SLAB_SIZES;
    for (int lv=0; lv<4; lv++) {
        uint32_t ss = sizes[lv], rs = ss+8;
        size_t budget = (size_t)(sz * ratios[lv]);
        uint32_t max = (uint32_t)((budget*8)/(rs*8+1));
        if (max<16) max=16;
        size_t bm_sz = bm_bytes(max); bm_sz = (bm_sz+7)&~7UL;
        size_t need = bm_sz + (size_t)max*rs;
        while (need>budget && max>16) { max--; bm_sz=bm_bytes(max); bm_sz=(bm_sz+7)&~7UL; need=bm_sz+(size_t)max*rs; }
        p->so[lv]=(uint32_t)off; p->ss[lv]=ss; p->sc[lv]=max;
        p->bm[lv]=p->base+off; memset(p->bm[lv],0,bm_sz);
        off+=need;
    }
    return 0;
}

static void *pool_alloc(Pool *p, size_t sz) {
    int lv;
    uint32_t sizes[] = SLAB_SIZES;
    if      (sz<=sizes[0]) lv=0;
    else if (sz<=sizes[1]) lv=1;
    else if (sz<=sizes[2]) lv=2;
    else if (sz<=sizes[3]) lv=3;
    else { fprintf(stderr,"pool_alloc: %zu > max\n",sz); return NULL; }
    int sl=lv, idx=-1;
    for (; lv<4; lv++) { idx=bm_find0(p->bm[lv],p->sc[lv]); if (idx>=0) break; }
    if (idx<0) { fprintf(stderr,"pool_alloc: slabs full (lv%d+)\n",sl); return NULL; }
    uint32_t rs = sizes[lv]+8;
    size_t b_sz = bm_bytes(p->sc[lv]); b_sz = (b_sz+7)&~7UL;
    uint8_t *sb = p->base + p->so[lv] + (uint32_t)b_sz + (uint32_t)(idx*rs);
    *(uint32_t*)sb = CANARY_MAGIC;
    *(uint32_t*)(sb+4+sizes[lv]) = CANARY_MAGIC;
    bm_set(p->bm[lv],idx);
    void *up = sb+4;
    p->used += rs; p->ta++; p->wl = (uint32_t)(p->used*100/p->total);
    return up;
}

static void pool_free(Pool *p, void *ptr) {
    if (!ptr) return;
    uint8_t *up = (uint8_t*)ptr, *sb = up-4;
    if (*(uint32_t*)sb != CANARY_MAGIC) { fprintf(stderr,"pool_free: bad canary\n"); return; }
    size_t rel = sb - p->base; int found=0;
    uint32_t sizes[] = SLAB_SIZES;
    for (int lv=0; lv<4; lv++) {
        size_t b_sz = bm_bytes(p->sc[lv]); b_sz = (b_sz+7)&~7UL;
        uint32_t ds = p->so[lv]+(uint32_t)b_sz, rs = sizes[lv]+8;
        if (rel>=p->so[lv] && rel<p->so[lv]+b_sz+(size_t)p->sc[lv]*rs && rel>=ds) {
            uint32_t sr = (uint32_t)(rel-ds), idx = sr/rs;
            if (idx<p->sc[lv] && sr%rs==0) {
                /* 校验尾部 canary 检测写溢出 */
                if (*(uint32_t*)(sb+4+sizes[lv]) != CANARY_MAGIC) {
                    fprintf(stderr,"pool_free: tail canary corrupted at idx %u\n",idx);
                    return;
                }
                bm_clear(p->bm[lv],idx);
                *(uint32_t*)sb=0; *(uint32_t*)(sb+4+sizes[lv])=0;
                p->used -= rs; p->tf++; p->wl = (uint32_t)(p->used*100/p->total);
                found=1; break;
            }
        }
    }
    if (!found) fprintf(stderr,"pool_free: ptr %p not in pool\n",ptr);
}

/* ============================================================
 * 哈希表 (hash)
 * ============================================================ */

static int hash_init(HashTable *t) { memset(t->b,0,sizeof(t->b)); t->cnt=0; return 0; }

static int hash_insert(HashTable *t, uint32_t kh, MemEntry *e) {
    uint32_t bk = kh % HASHTABLE_SIZE;
    HashNode *n = t->b[bk];
    while (n) { if (n->kh==kh) { n->e=e; return 0; } n=n->next; }
    HashNode *nn = (HashNode*)malloc(sizeof(HashNode));
    if (!nn) return -1;
    nn->kh=kh; nn->e=e; nn->next=t->b[bk]; t->b[bk]=nn; t->cnt++;
    return 0;
}

static MemEntry *hash_lookup(HashTable *t, uint32_t kh, const char *key) {
    HashNode *n = t->b[kh % HASHTABLE_SIZE];
    while (n) {
        if (n->kh==kh) {
            char *ek = (char*)n->e + sizeof(MemEntry);
            size_t kl = n->e->key_len;
            if (strncmp(key,ek,kl)==0) { n->e->accessed_at=(uint64_t)time(NULL); return n->e; }
        }
        n=n->next;
    }
    return NULL;
}

static int hash_remove(HashTable *t, uint32_t kh, const char *key) {
    uint32_t bk = kh % HASHTABLE_SIZE;
    HashNode *n=t->b[bk], *pr=NULL;
    while (n) {
        if (n->kh==kh) {
            char *ek=(char*)n->e+sizeof(MemEntry); size_t kl=n->e->key_len;
            if (strncmp(key,ek,kl)==0) {
                if (pr) pr->next=n->next; else t->b[bk]=n->next;
                free(n); t->cnt--; return 0;
            }
        }
        pr=n; n=n->next;
    }
    return -1;
}

/* ============================================================
 * 标签索引 (tag_index)
 * ============================================================ */

static uint32_t tag_hash(const char *t) { return djb2(t) % TAG_HASHTABLE_SIZE; }

static int tag_init(TagIndex *ti) { memset(ti->b,0,sizeof(ti->b)); ti->cnt=0; return 0; }

static TagEntry *tag_ensure(TagIndex *ti, const char *tag) {
    uint32_t bk = tag_hash(tag);
    TagEntry *te = ti->b[bk];
    while (te) { if (strncmp(te->tag,tag,MAX_TAG_LEN)==0) return te; te=te->next; }
    te=(TagEntry*)calloc(1,sizeof(TagEntry));
    if (!te) return NULL;
    strncpy(te->tag,tag,MAX_TAG_LEN-1); te->n=0; te->cap=0; te->es=NULL;
    te->next=ti->b[bk]; ti->b[bk]=te; ti->cnt++;
    return te;
}

static int tag_add(TagIndex *ti, const char *tag, MemEntry *e) {
    TagEntry *te = tag_ensure(ti,tag);
    if (!te) return -1;
    for (uint32_t i=0; i<te->n; i++) if (te->es[i]==e) return 0;
    if (te->n >= te->cap) {
        uint32_t nc = te->cap ? te->cap*2 : 8;
        MemEntry **na = (MemEntry**)realloc(te->es, nc*sizeof(MemEntry*));
        if (!na) return -1;
        te->es=na; te->cap=nc;
    }
    te->es[te->n++] = e;
    return 0;
}

static MemEntry **tag_search(TagIndex *ti, const char *tag, uint32_t *cnt) {
    TagEntry *te = ti->b[tag_hash(tag)];
    while (te) {
        if (strncmp(te->tag,tag,MAX_TAG_LEN)==0) {
            *cnt=te->n;
            if (te->n==0) return NULL;
            MemEntry **r = (MemEntry**)malloc(te->n*sizeof(MemEntry*));
            if (!r) { *cnt=0; return NULL; }
            memcpy(r,te->es,te->n*sizeof(MemEntry*));
            return r;
        }
        te=te->next;
    }
    *cnt=0; return NULL;
}

static void tag_remove_all(TagIndex *ti, MemEntry *e) {
    for (int b=0; b<TAG_HASHTABLE_SIZE; b++) {
        TagEntry *te=ti->b[b];
        while (te) {
            uint32_t nc=0;
            for (uint32_t i=0; i<te->n; i++) if (te->es[i]!=e) te->es[nc++]=te->es[i];
            te->n=nc; te=te->next;
        }
    }
}

/* ============================================================
 * 序列化 / 加载 / TTL (overflow)
 * ============================================================ */

static void json_esc(const char *s, char *d, size_t dm) {
    size_t di=0;
    for (size_t i=0; s[i] && di<dm-2; i++) {
        unsigned char c=(unsigned char)s[i];
        if (c=='"')      { d[di++]='\\'; d[di++]='"'; }
        else if (c=='\\'){ d[di++]='\\'; d[di++]='\\'; }
        else if (c=='\n'){ d[di++]='\\'; d[di++]='n'; }
        else if (c=='\r'){ d[di++]='\\'; d[di++]='r'; }
        else if (c=='\t'){ d[di++]='\\'; d[di++]='t'; }
        /* 注意：这里没有处理 Unicode 字符 
         * (如 \uXXXX 转义序列)。如果输入为
         * 合法 UTF-8 序列，它们会被原封不动
         * 地传输，这对大多数用户而言已经
         * 足够。若需要完整的 \uXXXX 转义，
         * 应对 UTF-8 序列进行 3/4 字节解码后
         * 转为 \uXXXX 形式。 */
        else d[di++]=c;
    }
    d[di]='\0';
}

static int json_get_str(const char *s, const char *key, char *out, size_t om) {
    char search[256]; snprintf(search,sizeof(search),"\"%s\":\"",key);
    const char *p = strstr(s,search); if (!p) return -1; p+=strlen(search);
    size_t i=0;
    while (*p && *p!='"' && i<om-1) {
        if (*p=='\\' && *(p+1)) { p++; if (*p=='n') out[i++]='\n'; else if (*p=='r') out[i++]='\r'; else if (*p=='t') out[i++]='\t'; else out[i++]=*p; }
        else out[i++]=*p;
        p++;
    }
    out[i]='\0'; return 0;
}

static int json_get_u64(const char *s, const char *key, uint64_t *v) {
    char search[256]; snprintf(search,sizeof(search),"\"%s\":",key);
    const char *p = strstr(s,search); if (!p) return -1;
    *v = strtoull(p+strlen(search),NULL,10); return 0;
}

static int json_get_tags(const char *s, char tags[][MAX_TAG_LEN], int max) {
    const char *p = strstr(s,"\"tags\":["); if (!p) return 0;
    p+=8; int cnt=0;
    while (*p && *p!=']' && cnt<max) {
        while (*p==',' || *p==' ') p++;
        if (*p=='"') { p++; size_t i=0; while (*p && *p!='"' && i<MAX_TAG_LEN-1) tags[cnt][i++]=*p++; tags[cnt][i]='\0'; if (*p=='"') p++; cnt++; }
    }
    return cnt;
}

/* ============================================================
 * 前置声明 (overflow 之前调用)
 * ============================================================ */

int memory_set(MemoryCtx*, const char*, const char*, const char**, int);
int memory_set_with_ts(MemoryCtx*, const char*, const char*, const char**, int, uint64_t);
static int memory_del_unlocked(MemoryCtx*, const char*);
int memory_del(MemoryCtx*, const char*);
int memory_flush(MemoryCtx*);
int memory_flush_shards(MemoryCtx*);
int memory_fork_snapshot(MemoryCtx*);
MemoryCtx* memory_shard_get(MemoryCtx*, const char *name);
MemoryCtx* memory_shard_ensure(MemoryCtx*, const char *name);

/* ============================================================
 * Skip List — 排序索引 (O(log n) 插入/删除/范围查询)
 * ============================================================ */

static inline uint64_t make_sort_key(uint64_t ts, uint32_t kh) {
    return (ts << 32) | (uint64_t)kh;
}

static int sl_rand_level(void) {
    int lv = 0;
    while (lv < SL_MAX_LEVEL - 1 && (rand() & (SL_PROB - 1)) == 0) lv++;
    return lv;
}

static int sl_init(SkipList *sl) {
    memset(sl, 0, sizeof(*sl));
    sl->top_level = 0; sl->count = 0;
    /* 单个哨兵节点，含 SL_MAX_LEVEL 个 forward 指针 */
    sl->head = (SLNode*)calloc(1, sizeof(SLNode) + SL_MAX_LEVEL * sizeof(SLNode*));
    if (!sl->head) return -1;
    sl->head->level = 0; sl->head->entry = NULL; sl->head->sort_key = 0;
    memset(sl->head->next, 0, SL_MAX_LEVEL * sizeof(SLNode*));
    return 0;
}

static int sl_insert(SkipList *sl, MemEntry *entry) {
    uint64_t sk = make_sort_key(entry->created_at, entry->key_hash);
    SLNode *update[SL_MAX_LEVEL];
    SLNode *cur = sl->head;

    for (int i = sl->top_level; i >= 0; i--) {
        while (cur->next[i] && cur->next[i]->sort_key < sk)
            cur = cur->next[i];
        update[i] = cur;
    }

    /* 检查重复 */
    SLNode *nxt = cur->next[0];
    if (nxt && nxt->sort_key == sk && nxt->entry == entry) return 0;

    int nlv = sl_rand_level();
    if (nlv > sl->top_level) {
        for (int i = sl->top_level + 1; i <= nlv; i++)
            update[i] = sl->head;
        sl->top_level = nlv;
    }

    SLNode *nn = (SLNode*)calloc(1, sizeof(SLNode) + (nlv+1)*sizeof(SLNode*));
    if (!nn) return -1;
    nn->entry = entry; nn->sort_key = sk; nn->level = (uint8_t)nlv;

    for (int i = 0; i <= nlv; i++) {
        nn->next[i] = update[i]->next[i];
        update[i]->next[i] = nn;
    }
    sl->count++;
    return 0;
}

static void sl_remove(SkipList *sl, MemEntry *entry) {
    uint64_t sk = make_sort_key(entry->created_at, entry->key_hash);
    SLNode *update[SL_MAX_LEVEL];
    SLNode *cur = sl->head;

    for (int i = sl->top_level; i >= 0; i--) {
        while (cur->next[i] && cur->next[i]->sort_key < sk)
            cur = cur->next[i];
        update[i] = cur;
    }

    SLNode *target = cur->next[0];
    if (!target || target->sort_key != sk || target->entry != entry) return;

    int tlv = (int)target->level;
    for (int i = 0; i <= tlv && i <= sl->top_level; i++)
        update[i]->next[i] = target->next[i];

    free(target);
    sl->count--;

    while (sl->top_level > 0 && !sl->head->next[sl->top_level])
        sl->top_level--;
}

/* 按时间范围查询: [t_start, t_end) */
static int sl_range(SkipList *sl, uint64_t t_start, uint64_t t_end,
                    MemEntry ***out, uint32_t *cnt) {
    *out = NULL; *cnt = 0;
    if (sl->count == 0) return 0;

    /* 跳到 >= t_start 的第一个节点 */
    uint64_t sk_start = make_sort_key(t_start, 0);
    SLNode *cur = sl->head->next[0];
    while (cur && cur->sort_key < sk_start) cur = cur->next[0];

    /* 收集范围内节点 */
    uint32_t cap = 64, found = 0;
    MemEntry **res = (MemEntry**)malloc(cap * sizeof(MemEntry*));
    if (!res) return -1;

    while (cur && cur->entry && (cur->sort_key >> 32) < t_end) {
        if (found >= cap) {
            cap *= 2;
            MemEntry **nr = (MemEntry**)realloc(res, cap * sizeof(MemEntry*));
            if (!nr) { free(res); return -1; }
            res = nr;
        }
        res[found++] = cur->entry;
        cur = cur->next[0];
    }

    *out = res; *cnt = found;
    return 0;
}

static void sl_destroy(SkipList *sl) {
    SLNode *cur = sl->head ? sl->head->next[0] : NULL;
    while (cur) { SLNode *nx = cur->next[0]; free(cur); cur = nx; }
    free(sl->head);
    memset(sl, 0, sizeof(*sl));
}

/* ============================================================
 * WAL — 预写日志 (Crash-safe 持久化)
 * ============================================================ */

static int wal_path(char *buf, size_t bs, const char *dd) {
    return snprintf(buf, bs, "%s/wal.log", dd);
}

/* 写入一条 WAL 记录 (二进制) */
static int wal_append(const char *wal_file, uint8_t op,
                      const char *key, const char *val,
                      const char **tags, int tc, uint64_t ts) {
    size_t kl = strlen(key), vl = val ? strlen(val) : 0;
    if (kl > MAX_KEY_LEN) kl = MAX_KEY_LEN;
    if (vl > MAX_VAL_LEN) vl = MAX_VAL_LEN;
    if (tc > MAX_TAGS) tc = MAX_TAGS;

    FILE *fp = fopen(wal_file, "ab");
    if (!fp) return -1;

    uint32_t magic = WAL_MAGIC;
    uint16_t nkl = (uint16_t)kl, nvl = (uint16_t)vl;
    uint8_t ntc = (uint8_t)tc;

    fwrite(&magic, 4, 1, fp);
    fwrite(&op, 1, 1, fp);
    fwrite(&nkl, 2, 1, fp);
    fwrite(&nvl, 2, 1, fp);
    fwrite(&ntc, 1, 1, fp);
    fwrite(&ts, 8, 1, fp);
    fwrite(key, 1, kl, fp);
    if (val) fwrite(val, 1, vl, fp);
    /* 写入标签: 每个 MAX_TAG_LEN 字节, 不足用 \0 填充 */
    for (int i = 0; i < tc; i++) {
        if (tags[i]) {
            size_t tl = strlen(tags[i]);
            if (tl > MAX_TAG_LEN - 1) tl = MAX_TAG_LEN - 1;
            fwrite(tags[i], 1, tl, fp);
            if (tl < MAX_TAG_LEN) {
                char pad = 0;
                for (size_t p = tl; p < MAX_TAG_LEN; p++) fwrite(&pad, 1, 1, fp);
            }
        } else {
            char pad[MAX_TAG_LEN] = {0};
            fwrite(pad, 1, MAX_TAG_LEN, fp);
        }
    }

    fclose(fp);
    return 0;
}

/* 重播 WAL: 预读整个文件到内存，从内存解析。
 * 避免 memory_set_with_ts 写入 WAL 导致的自己写自己读死循环。 */
static int wal_replay(MemoryCtx *ctx, const char *wal_file) {
    FILE *fp = fopen(wal_file, "rb");
    if (!fp) return 0;

    fseeko(fp, 0, SEEK_END);
    long sz = ftello(fp);
    if (sz <= 0) { fclose(fp); return 0; }
    fseeko(fp, 0, SEEK_SET);

    char *buf = (char*)malloc((size_t)sz);
    if (!buf) { fclose(fp); return 0; }
    size_t nread = fread(buf, 1, (size_t)sz, fp);
    fclose(fp);
    if (nread == 0) { free(buf); return 0; }

    int restored = 0;
    size_t pos = 0;
    while (pos + 18 <= nread) {
        uint32_t magic = *(uint32_t*)(buf + pos); pos += 4;
        if (magic != WAL_MAGIC) continue;

        uint8_t op   = *(uint8_t*)(buf + pos); pos += 1;
        uint16_t nkl = *(uint16_t*)(buf + pos); pos += 2;
        uint16_t nvl = *(uint16_t*)(buf + pos); pos += 2;
        uint8_t  ntc = *(uint8_t*)(buf + pos); pos += 1;
        uint64_t ts  = *(uint64_t*)(buf + pos); pos += 8;

        if (nkl > MAX_KEY_LEN || pos + nkl > nread) break;

        char key_buf[MAX_KEY_LEN+1];
        memcpy(key_buf, buf + pos, nkl); pos += nkl;
        key_buf[nkl] = '\0';

        char val_buf[MAX_VAL_LEN+1]; val_buf[0] = '\0';
        if (op == WAL_OP_SET) {
            if (nvl > MAX_VAL_LEN || pos + nvl > nread) break;
            memcpy(val_buf, buf + pos, nvl); pos += nvl;
            val_buf[nvl] = '\0';
        }

        int tci = ntc > MAX_TAGS ? MAX_TAGS : ntc;
        const char *tag_ptrs[MAX_TAGS];
        char tag_buf[MAX_TAGS * MAX_TAG_LEN];
        for (int i = 0; i < tci; i++) {
            if (pos + MAX_TAG_LEN > nread) { tci = i; goto replay_done; }
            memcpy(tag_buf + i * MAX_TAG_LEN, buf + pos, MAX_TAG_LEN); pos += MAX_TAG_LEN;
            if (tag_buf[i * MAX_TAG_LEN] == '\0') {
                tag_ptrs[i] = NULL;
            } else {
                tag_buf[i * MAX_TAG_LEN + MAX_TAG_LEN - 1] = '\0';
                tag_ptrs[i] = tag_buf + i * MAX_TAG_LEN;
            }
        }

        if (op == WAL_OP_SET) {
            if (memory_set_with_ts(ctx, key_buf, val_buf, tag_ptrs, tci, ts) >= 0)
                restored++;
        } else if (op == WAL_OP_DEL) {
            if (memory_del_unlocked(ctx, key_buf) == 0)
                restored++;
        }
    }

replay_done:
    free(buf);
    return restored;
}

/* 压缩 WAL: flush 后将 WAL 变短（仅保留未写入快照的最旧操作）
 * 简单策略: 刷完后直接 truncate WAL（所有操作已被快照保存） */
static int wal_compact(const char *wal_file) {
    FILE *fp = fopen(wal_file, "wb");
    if (!fp) return -1;
    fclose(fp);
    return 0;
}

/* ============================================================
 * 序列化 / 加载 / TTL (overflow 函数体)
 * ============================================================ */

static int ovf_flush(MemoryCtx *ctx) {
    char fn[1024]; snprintf(fn,sizeof(fn),"%s/memory_snapshot.json",ctx->data_dir);
    int mkr = mkdir(ctx->data_dir,0755);
    if (mkr!=0 && errno!=EEXIST) { if (errno==ENOTDIR) { unlink(ctx->data_dir); mkdir(ctx->data_dir,0755); } }

    /* 收集活跃条目 */
    MemEntry *to_evict[MAX_ENTRIES];
    int n_evict = 0;
    for (int b=0; b<HASHTABLE_SIZE; b++) {
        HashNode *n = ctx->table.b[b];
        while (n) {
            MemEntry *e=n->e;
            if ((e->flags & FLAG_ACTIVE) && n_evict < MAX_ENTRIES)
                to_evict[n_evict++] = e;
            n=n->next;
        }
    }
    if (n_evict == 0) return 0;

    /* Pass 1: 写入磁盘 */
    FILE *fp = fopen(fn,"w"); if (!fp) return -1;
    int w=0;
    for (int i=0; i<n_evict; i++) {
        MemEntry *e=to_evict[i];
        char *key=(char*)e+sizeof(MemEntry), *val=key+e->key_len+1, *tb=val+e->val_len+1;
        char ke[MAX_KEY_LEN*2], ve[MAX_VAL_LEN*2];
        json_esc(key,ke,sizeof(ke)); json_esc(val,ve,sizeof(ve));
        fprintf(fp,"{\"k\":\""); fwrite(ke,1,strlen(ke),fp);
        fprintf(fp,"\",\"v\":\""); fwrite(ve,1,strlen(ve),fp);
        fprintf(fp,"\",\"ts\":%lu,\"tags\":[",(unsigned long)e->created_at);
        for (int j=0; j<e->tag_count; j++) { if (j>0) fputc(',',fp); char *t=tb+j*MAX_TAG_LEN; fputc('"',fp); fwrite(t,1,strlen(t),fp); fputc('"',fp); }
        fprintf(fp,"]}\n"); w++;
    }
    fclose(fp);

    /* Pass 2: 释放内存 */
    for (int i=0; i<n_evict; i++) {
        MemEntry *e=to_evict[i];
        tag_remove_all(&ctx->tag_index, e);
        hash_remove(&ctx->table, e->key_hash, (char*)e+sizeof(MemEntry));
        e->flags = 0;
        pool_free(&ctx->pool, e);
        if (ctx->pool.ec > 0) ctx->pool.ec--;
    }
    return w;
}


/* 取时间戳所在日期的午夜 (UTC) */
static uint64_t day_of_ts(uint64_t ts) {
    struct tm tm; time_t t = (time_t)ts;
    localtime_r(&t, &tm);
    tm.tm_hour = 0; tm.tm_min = 0; tm.tm_sec = 0;
    return (uint64_t)mktime(&tm);
}

/* 释放指定日期的全部条目 (写入磁盘后释放内存) */
static int ovf_flush_day(MemoryCtx *ctx, uint64_t day_start) {
    uint64_t day_end = day_start + 86400;

    /* 收集该日期的条目 */
    MemEntry *to_evict[MAX_ENTRIES];
    int n_evict = 0;
    for (int b = 0; b < HASHTABLE_SIZE; b++) {
        HashNode *n = ctx->table.b[b];
        while (n) {
            MemEntry *e = n->e;
            if ((e->flags & FLAG_ACTIVE)
                && e->created_at >= day_start && e->created_at < day_end
                && n_evict < MAX_ENTRIES)
                to_evict[n_evict++] = e;
            n = n->next;
        }
    }
    if (n_evict == 0) return 0;

    /* 打开该日期的文件 (先写临时文件, 再原子 rename) */
    time_t dt = (time_t)day_start;
    struct tm tm; localtime_r(&dt, &tm);
    char fn[1024], tmp_fn[1024];
    snprintf(fn, sizeof(fn), "%s/memory-%04d-%02d-%02d.json",
        ctx->data_dir, tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday);
    snprintf(tmp_fn, sizeof(tmp_fn), "%s/.tmp_memory-%04d-%02d-%02d.json",
        ctx->data_dir, tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday);
    int mkr = mkdir(ctx->data_dir, 0755);
    if (mkr != 0 && errno != EEXIST) {
        if (errno == ENOTDIR) { unlink(ctx->data_dir); mkdir(ctx->data_dir, 0755); }
    }

    FILE *fp = fopen(tmp_fn, "w");
    if (!fp) return -1;
    int w = 0;
    for (int i = 0; i < n_evict; i++) {
        MemEntry *e = to_evict[i];
        char *key = (char*)e + sizeof(MemEntry);
        char *val = key + e->key_len + 1;
        char *tb = val + e->val_len + 1;
        char ke[MAX_KEY_LEN * 2], ve[MAX_VAL_LEN * 2];
        json_esc(key, ke, sizeof(ke)); json_esc(val, ve, sizeof(ve));
        fprintf(fp, "{\"k\":\""); fwrite(ke, 1, strlen(ke), fp);
        fprintf(fp, "\",\"v\":\""); fwrite(ve, 1, strlen(ve), fp);
        fprintf(fp, "\",\"ts\":%lu,\"tags\":[", (unsigned long)e->created_at);
        for (int j = 0; j < e->tag_count; j++) {
            if (j > 0) fputc(',', fp);
            char *t = tb + j * MAX_TAG_LEN;
            fputc('"', fp); fwrite(t, 1, strlen(t), fp); fputc('"', fp);
        }
        fprintf(fp, "]}\n"); w++;
    }
    fclose(fp);

    /* 原子替换: rename 保证要么旧文件完整, 要么新文件完整 */
    if (rename(tmp_fn, fn) != 0) {
        unlink(tmp_fn);
        return -1;
    }

    /* 释放内存 */
    for (int i = 0; i < n_evict; i++) {
        MemEntry *e = to_evict[i];
        tag_remove_all(&ctx->tag_index, e);
        hash_remove(&ctx->table, e->key_hash, (char*)e + sizeof(MemEntry));
        sl_remove(&ctx->sorted, e);
        e->flags = 0;
        pool_free(&ctx->pool, e);
        if (ctx->pool.ec > 0) ctx->pool.ec--;
    }
    return w;
}

/* 逐出最早的日期，循环直到水位低于 EVICT_WATER */
static int ovf_evict_oldest(MemoryCtx *ctx) {
    int total = 0;
    while (ctx->pool.wl >= EVICT_WATER) {
        /* 找到最早的日期 */
        uint64_t oldest_day = UINT64_MAX;
        for (int b = 0; b < HASHTABLE_SIZE; b++) {
            HashNode *n = ctx->table.b[b];
            while (n) {
                MemEntry *e = n->e;
                if (e->flags & FLAG_ACTIVE) {
                    uint64_t d = day_of_ts(e->created_at);
                    if (d < oldest_day) oldest_day = d;
                }
                n = n->next;
            }
        }
        if (oldest_day == UINT64_MAX) break; /* 没有可逐出的 */

        int n = ovf_flush_day(ctx, oldest_day);
        if (n <= 0) break;
        total += n;
    }
    return total;
}


/* 盘上扫描匹配 key 的条目，找到后回填内存，返回 value。
 * 返回 NULL 表示未找到。遍历日文件（跳过今天的文件，已内存在热池中）。 */
static const char *scan_day_files(MemoryCtx *ctx, const char *key) {
    DIR *d = opendir(ctx->data_dir);
    if (!d) return NULL;

    time_t now = time(NULL);
    struct tm today_tm; localtime_r(&now, &today_tm);
    char today_file[64];
    snprintf(today_file, sizeof(today_file), "memory-%04d-%02d-%02d.json",
             today_tm.tm_year + 1900, today_tm.tm_mon + 1, today_tm.tm_mday);

    /* 收集文件名，按日期倒序（最新的先查） */
    char fnames[32][256];
    int nf = 0;
    struct dirent *de;
    while ((de = readdir(d)) != NULL && nf < 32) {
        const char *nm = de->d_name;
        if (strncmp(nm, "memory-", 7) != 0) continue;
        size_t nl = strlen(nm);
        if (nl < 18 || strcmp(nm + nl - 5, ".json") != 0) continue;
        if (strcmp(nm, today_file) == 0) continue; /* 跳过今天，已热加载 */
        int y, m, dd;
        if (sscanf(nm, "memory-%04d-%02d-%02d.json", &y, &m, &dd) == 3) {
            snprintf(fnames[nf], 256, "%s", nm);
            nf++;
        }
    }
    closedir(d);

    /* 按文件名倒序（YYYY-MM-DD 能直接字符串比对） */
    for (int i = 0; i < nf - 1; i++)
        for (int j = i + 1; j < nf; j++)
            if (strcmp(fnames[i], fnames[j]) < 0) {
                char tmp[256];
                strcpy(tmp, fnames[i]);
                strcpy(fnames[i], fnames[j]);
                strcpy(fnames[j], tmp);
            }

    for (int fi = 0; fi < nf; fi++) {
        char fp[4096];
        snprintf(fp, sizeof(fp), "%s/%s", ctx->data_dir, fnames[fi]);
        FILE *f = fopen(fp, "r");
        if (!f) continue;

        char line[65536];
        while (fgets(line, sizeof(line), f)) {
            if (line[0] == '\n' || line[0] == '\0') continue;
            char kb[MAX_KEY_LEN];
            if (json_get_str(line, "k", kb, sizeof(kb)) < 0) continue;
            if (strcmp(kb, key) != 0) continue;

            /* 命中：解析完整条目，加载回内存 */
            char vb[MAX_VAL_LEN];
            uint64_t ts = 0;
            json_get_str(line, "v", vb, sizeof(vb));
            json_get_u64(line, "ts", &ts);
            char tags[MAX_TAGS][MAX_TAG_LEN];
            int tc = json_get_tags(line, tags, MAX_TAGS);
            const char *tp[MAX_TAGS];
            for (int ti = 0; ti < tc; ti++) tp[ti] = tags[ti];

            memory_set_with_ts(ctx, kb, vb, tp, tc, ts);
            MemEntry *e = hash_lookup(&ctx->table, djb2(kb), kb);
            if (e) e->accessed_at = (uint64_t)time(NULL);
            fclose(f);

            /* 从内存中返回 value */
            e = hash_lookup(&ctx->table, djb2(kb), kb);
            if (e) return (char*)e + sizeof(MemEntry) + e->key_len + 1;
            return NULL;
        }
        fclose(f);
    }
    return NULL;
}

static int ovf_load(MemoryCtx *ctx) {
    /* 1. 加载快照 (如果存在) */
    char snap[1024]; snprintf(snap,sizeof(snap),"%s/memory_snapshot.json",ctx->data_dir);
    FILE *sf = fopen(snap,"r");
    if (sf) {
        char line[65536];
        while (fgets(line,sizeof(line),sf)) {
            if (line[0]=='\n'||line[0]=='\0') continue;
            char kb[MAX_KEY_LEN], vb[MAX_VAL_LEN]; uint64_t ts=0;
            if (json_get_str(line,"k",kb,sizeof(kb))<0) continue;
            if (json_get_str(line,"v",vb,sizeof(vb))<0) continue;
            json_get_u64(line,"ts",&ts);
            char tags[MAX_TAGS][MAX_TAG_LEN]; int tc=json_get_tags(line,tags,MAX_TAGS);
            const char *tp[MAX_TAGS]; for (int i=0;i<tc;i++) tp[i]=tags[i];
            memory_set_with_ts(ctx,kb,vb,tp,tc,ts);
        }
        fclose(sf);
    }
    /* 2. 只加载今天的日文件 (惰性皮层: 旧数据留在磁盘, 检索时才激活) */
    time_t now = time(NULL);
    struct tm ttm; localtime_r(&now,&ttm);
    char today[64]; snprintf(today,sizeof(today),"memory-%04d-%02d-%02d.json",
        ttm.tm_year+1900,ttm.tm_mon+1,ttm.tm_mday);
    char fp[4096]; snprintf(fp,sizeof(fp),"%s/%s",ctx->data_dir,today);
    FILE *df = fopen(fp,"r");
    if (df) {
        char line[65536];
        while (fgets(line,sizeof(line),df)) {
            if (line[0]=='\n'||line[0]=='\0') continue;
            char kb[MAX_KEY_LEN], vb[MAX_VAL_LEN]; uint64_t ts=0;
            if (json_get_str(line,"k",kb,sizeof(kb))<0) continue;
            if (json_get_str(line,"v",vb,sizeof(vb))<0) continue;
            json_get_u64(line,"ts",&ts);
            char tags[MAX_TAGS][MAX_TAG_LEN]; int tc=json_get_tags(line,tags,MAX_TAGS);
            const char *tp[MAX_TAGS]; for (int i=0;i<tc;i++) tp[i]=tags[i];
            memory_set_with_ts(ctx,kb,vb,tp,tc,ts);
        }
        fclose(df);
    }
    return 0;
}

static int ovf_clean(const MemoryCtx *ctx) {
    DIR *d = opendir(ctx->data_dir); if (!d) return 0;
    struct dirent *de; time_t now=time(NULL); int r=0;
    while ((de=readdir(d))!=NULL) {
        const char *nm=de->d_name; size_t nl=strlen(nm);
        if (nl<18 || strncmp(nm,"memory-",7)!=0) continue;
        int y,m,dd; if (sscanf(nm,"memory-%04d-%02d-%02d.json",&y,&m,&dd)!=3) continue;
        struct tm ft={0}; ft.tm_year=y-1900; ft.tm_mon=m-1; ft.tm_mday=dd;
        if (difftime(now,mktime(&ft))/86400.0 > ctx->file_ttl) {
            char fp[4096]; snprintf(fp,sizeof(fp),"%s/%s",ctx->data_dir,nm);
            if (unlink(fp)==0) r++;
        }
    }
    closedir(d); return r;
}

/* ============================================================
 * Shard (命名分片) — 每个分片独立 Pool/Hash/Tag/Sorted
 * 所有内部函数不改，通过不同的 MemoryCtx* 路由
 * ============================================================ */

/* 通过名称查找已存在的 shard */
MemoryCtx* memory_shard_get(MemoryCtx *ctx, const char *name) {
    if (!name || name[0] == '\0' || strcmp(name, "default") == 0)
        return ctx;
    for (int i = 0; i < ctx->shard_count; i++)
        if (strcmp(ctx->shards[i].name, name) == 0)
            return ctx->shards[i].ctx;
    return NULL;
}

/* 确保 shard 存在，不存在则创建并初始化（惰性创建） */
MemoryCtx* memory_shard_ensure(MemoryCtx *ctx, const char *name) {
    if (!name || name[0] == '\0' || strcmp(name, "default") == 0)
        return ctx;
    /* 已有？直接返回 */
    MemoryCtx *existing = memory_shard_get(ctx, name);
    if (existing) return existing;
    if (ctx->shard_count >= MAX_SHARDS) { fprintf(stderr,"max shards (%d) reached\n",MAX_SHARDS); return NULL; }

    int idx = ctx->shard_count;
    strncpy(ctx->shards[idx].name, name, 63);
    ctx->shards[idx].name[63] = '\0';

    /* 子数据目录: data_dir/shard_<name>/ */
    char sd[1024];
    snprintf(sd, sizeof(sd), "%s/shard_%s", ctx->data_dir, name);

    MemoryCtx *sc = (MemoryCtx*)calloc(1, sizeof(MemoryCtx));
    if (!sc) return NULL;
    ctx->shards[idx].ctx = sc;
    ctx->shard_count++;

    /* 小池: 256KB 每个 shard */
    sc->wal_disabled = 1;
    if (pool_init(&sc->pool, SHARD_POOL_SIZE) < 0) { free(sc); ctx->shard_count--; return NULL; }
    hash_init(&sc->table); tag_init(&sc->tag_index);
    sl_init(&sc->sorted);
    strncpy(sc->data_dir, sd, sizeof(sc->data_dir)-1);
    sc->file_ttl = ctx->file_ttl;
    sc->initialized = 1;

    /* 加载 shard 的持久化数据 */
    ovf_load(sc); ovf_clean(sc);
    char wf[1024]; wal_path(wf, sizeof(wf), sd);
    int restored = wal_replay(sc, wf);
    wal_compact(wf);
    sc->wal_disabled = 0;
    if (restored > 0) fprintf(stderr,"shard '%s': restored %d entries\n", name, restored);

    return sc;
}

/* ============================================================
 * Fork 快照 (类似 Redis BGSAVE)
 * fork 子进程写快照, 父进程继续服务
 * 子进程利用 COW 看到一致的内存快照
 * ============================================================ */

int memory_fork_snapshot(MemoryCtx *ctx) {
#ifdef HIPOOL_USE_MUTEX
    /* 多线程下 fork 不安全: 只有调用线程被复制 */
    fprintf(stderr, "fork_snapshot: unsafe with threads, skipping\n");
    return -1;
#endif
    pid_t pid = fork();
    if (pid < 0) { perror("fork"); return -1; }
    if (pid > 0) {
        /* 父进程: 返回子 PID, 调用者可 waitpid */
        return (int)pid;
    }
    /* 子进程: 继承 COW 内存, 写入快照后退出 */
    ctx->wal_disabled = 1;
    int r = ovf_flush(ctx);
    /* 同时 flush 所有命名 shard */
    for (int i = 0; i < ctx->shard_count; i++) {
        if (ctx->shards[i].ctx)
            r += ovf_flush(ctx->shards[i].ctx);
    }
    /* 关闭所有继承的 fd (除了 stdio) */
    for (int fd = 3; fd < 256; fd++) close(fd);
    _exit(r >= 0 ? 0 : 1);
}

/* flush 所有 shard */
int memory_flush_shards(MemoryCtx *ctx) {
    int total = memory_flush(ctx);  /* 默认 shard */
    for (int i = 0; i < ctx->shard_count; i++) {
        if (ctx->shards[i].ctx) {
            LOCK(ctx->shards[i].ctx);
            total += ovf_flush(ctx->shards[i].ctx);
            UNLOCK(ctx->shards[i].ctx);
        }
    }
    return total;
}

/* ============================================================
 * 公开 API
 * ============================================================ */

int memory_init(MemoryCtx *ctx, const char *dd, int ttl) {
    memset(ctx,0,sizeof(MemoryCtx));
    if (pool_init(&ctx->pool,POOL_SIZE)<0) return -1;
    hash_init(&ctx->table); tag_init(&ctx->tag_index);
    if (sl_init(&ctx->sorted) < 0) return -1;
    strncpy(ctx->data_dir,dd,sizeof(ctx->data_dir)-1);
    ctx->file_ttl = ttl>0 ? ttl : FILE_TTL_DAYS;
    ctx->initialized=1;
#ifdef HIPOOL_USE_MUTEX
    pthread_mutex_init(&ctx->lock, NULL);
#endif
    /* 加载期间禁用 WAL，避免 ovf_load + wal_replay 自己写自己 */
    ctx->wal_disabled = 1;
    ovf_load(ctx); ovf_clean(ctx);
    /* WAL 重播: 从崩溃中恢复未落盘的条目 */
    char wf[1024]; wal_path(wf,sizeof(wf),ctx->data_dir);
    int restored = wal_replay(ctx, wf);
    /* 重播完成后截断 WAL（所有操作已恢复），下次启动从头写 */
    wal_compact(wf);
    ctx->wal_disabled = 0;
    if (restored > 0) fprintf(stderr,"wal_replay: restored %d entries\n",restored);

    /* 自动发现已有的 shard 目录并加载 */
    {
        DIR *d = opendir(ctx->data_dir);
        if (d) {
            struct dirent *de;
            while ((de = readdir(d)) != NULL) {
                if (strncmp(de->d_name, "shard_", 6) != 0) continue;
                /* 检查是否是目录 */
                char sp[1024]; struct stat st;
                snprintf(sp,sizeof(sp),"%s/%s",ctx->data_dir,de->d_name);
                if (stat(sp,&st) != 0 || !S_ISDIR(st.st_mode)) continue;
                char sname[64];
                snprintf(sname, sizeof(sname), "%s", de->d_name + 6);
                if (!memory_shard_get(ctx, sname))
                    memory_shard_ensure(ctx, sname);
            }
            closedir(d);
        }
    }

    return 0;
}

void memory_destroy(MemoryCtx *ctx) {
    /* 先 flush 所有 shard */
    memory_flush_shards(ctx);

    /* 销毁命名 shard */
    for (int i = 0; i < ctx->shard_count; i++) {
        MemoryCtx *sc = ctx->shards[i].ctx;
        if (!sc) continue;
        for (int b=0; b<HASHTABLE_SIZE; b++) { HashNode *n=sc->table.b[b]; while (n) { HashNode *nx=n->next; free(n); n=nx; } }
        for (int b=0; b<TAG_HASHTABLE_SIZE; b++) { TagEntry *te=sc->tag_index.b[b]; while (te) { TagEntry *nx=te->next; free(te->es); free(te); te=nx; } }
        sl_destroy(&sc->sorted);
        free(sc->pool.base);
        free(sc);
        ctx->shards[i].ctx = NULL;
    }
    ctx->shard_count = 0;

    /* 销毁默认 shard */
    for (int b=0; b<HASHTABLE_SIZE; b++) { HashNode *n=ctx->table.b[b]; while (n) { HashNode *nx=n->next; free(n); n=nx; } }
    for (int b=0; b<TAG_HASHTABLE_SIZE; b++) { TagEntry *te=ctx->tag_index.b[b]; while (te) { TagEntry *nx=te->next; free(te->es); free(te); te=nx; } }
    sl_destroy(&ctx->sorted);
    free(ctx->pool.base);
#ifdef HIPOOL_USE_MUTEX
    pthread_mutex_destroy(&ctx->lock);
#endif
    memset(ctx,0,sizeof(MemoryCtx));
}

/* 同日期去重: 检查同一天是否已有相似内容的条目 */
static int dedup_same_day(MemoryCtx *ctx, const char *key, const char *val) {
    /* 提取日期前缀 (YYYY-MM-DD) */
    const char *last_dash = strrchr(key, '-');
    if (!last_dash) return 0; /* 没序号 → 不检查 */
    int dash_pos = (int)(last_dash - key);
    if (dash_pos < 10) return 0; /* 不匹配 YYYY-MM-DD-N */

    size_t vl = strlen(val);
    if (vl < 20) return 0; /* 太短不比较 */

    int checked = 0;
    for (int b = 0; b < HASHTABLE_SIZE && checked < 10; b++) {
        HashNode *n = ctx->table.b[b];
        while (n && checked < 10) {
            MemEntry *e = n->e;
            if (!(e->flags & FLAG_ACTIVE)) { n = n->next; continue; }
            char *ek = (char*)e + sizeof(MemEntry);
            size_t ekl = e->key_len;
            /* 同一天 (key 前缀相同) */
            if (ekl >= (size_t)dash_pos
                && strncmp(ek, key, dash_pos) == 0
                && ek[dash_pos] == '-') {
                checked++;
                char *ev = ek + ekl + 1;
                size_t evl = e->val_len;
                /* 内容相似度 > 60% → 重复 */
                if ((vl >= evl && (double)evl / vl > 0.60) ||
                    (evl >= vl && (double)vl / evl > 0.60)) {
                    /* 进一步: 检查较短的 value 是否有 70% 字符出现在较长的中 */
                    const char *shorter = vl < evl ? val : ev;
                    size_t sl = vl < evl ? vl : evl;
                    const char *longer = vl < evl ? ev : val;
                    size_t match_chars = 0;
                    for (size_t i = 0; i < sl; i++) {
                        if (memchr(longer, shorter[i], strlen(longer)))
                            match_chars++;
                    }
                    if ((double)match_chars / sl > 0.80) return 1; /* 重复 */
                }
            }
            n = n->next;
        }
    }
    return 0;
}

/* 内部: 带时间戳的 memory_set (磁盘回填用) */
int memory_set_with_ts(MemoryCtx *ctx, const char *key, const char *val,
                               const char **tags, int tc, uint64_t ts) {
    if (!ctx->initialized || !key || !val) return -1;
    if (tc>MAX_TAGS) tc=MAX_TAGS;
    size_t kl=strlen(key), vl=strlen(val);
    if (kl>MAX_KEY_LEN) kl=MAX_KEY_LEN;
    if (vl>MAX_VAL_LEN) vl=MAX_VAL_LEN;

    char tk[MAX_KEY_LEN+1]; memcpy(tk,key,kl); tk[kl]='\0';
    uint32_t kh = djb2(tk);

    if (ctx->pool.wl >= EVICT_WATER) ovf_evict_oldest(ctx);
    if (dedup_same_day(ctx, key, val)) return -2;
    memory_del_unlocked(ctx,key);

    size_t tot = entry_total_size((uint16_t)kl,(uint16_t)vl,(uint8_t)tc);
    void *ptr = pool_alloc(&ctx->pool,tot);
    if (!ptr) return -1;

    MemEntry *e = (MemEntry*)ptr;
    e->magic_start=CANARY_MAGIC; e->key_hash=kh;
    e->key_len=(uint16_t)kl; e->val_len=(uint16_t)vl; e->tag_count=(uint8_t)tc;
    e->flags=FLAG_ACTIVE; e->_pad[0]=e->_pad[1]=0;
    e->created_at = ts ? ts : (uint64_t)time(NULL);
    e->accessed_at = (uint64_t)time(NULL);

    char *kp=(char*)e+sizeof(MemEntry), *vp=kp+kl+1, *tp=vp+vl+1;
    memcpy(kp,key,kl); kp[kl]='\0';
    memcpy(vp,val,vl); vp[vl]='\0';
    memset(tp,0,(size_t)tc*MAX_TAG_LEN);
    for (int i=0; i<tc; i++) if (tags[i]) strncpy(tp+i*MAX_TAG_LEN,tags[i],MAX_TAG_LEN-1);
    hash_insert(&ctx->table,kh,e);
    sl_insert(&ctx->sorted, e);
    for (int i=0; i<tc; i++) if (tags[i]&&tags[i][0]) tag_add(&ctx->tag_index,tags[i],e);
    ctx->pool.ec++;

    /* WAL: 先写日志再落内存，保证可恢复 */
    if (!ctx->wal_disabled) {
        char wf[1024]; wal_path(wf,sizeof(wf),ctx->data_dir);
        wal_append(wf, WAL_OP_SET, key, val, tags, tc,
                   ts ? ts : (uint64_t)time(NULL));
    }
    return 0;
}

int memory_set(MemoryCtx *ctx, const char *key, const char *val, const char **tags, int tc) {
    LOCK(ctx);
    int rc = memory_set_with_ts(ctx, key, val, tags, tc, 0);
    UNLOCK(ctx);
    return rc;
}

const char *memory_get(MemoryCtx *ctx, const char *key) {
    if (!ctx->initialized || !key) return NULL;
    LOCK(ctx);
    size_t kl=strlen(key); if (kl>MAX_KEY_LEN) kl=MAX_KEY_LEN;
    MemEntry *e = hash_lookup(&ctx->table,djb2_n(key,kl),key);
    if (e) { UNLOCK(ctx); return (char*)e + sizeof(MemEntry) + e->key_len + 1; }
    const char *result = scan_day_files(ctx, key);
    UNLOCK(ctx); return result;
}

/* 内部: 无锁版本的 memory_del（供 memory_set_with_ts 调用，避免重入死锁） */
static int memory_del_unlocked(MemoryCtx *ctx, const char *key) {
    if (!ctx->initialized || !key) return -1;
    size_t kl=strlen(key); if (kl>MAX_KEY_LEN) kl=MAX_KEY_LEN;
    uint32_t kh = djb2_n(key,kl);
    MemEntry *e = hash_lookup(&ctx->table,kh,key);
    if (!e) return -1;
    sl_remove(&ctx->sorted, e);
    tag_remove_all(&ctx->tag_index,e);
    hash_remove(&ctx->table,kh,key);
    e->flags=0; pool_free(&ctx->pool,e);
    if (ctx->pool.ec>0) ctx->pool.ec--;
    
    /* WAL: 先写日志再落内存 */
    if (!ctx->wal_disabled) {
        char wf[1024]; wal_path(wf,sizeof(wf),ctx->data_dir);
        wal_append(wf, WAL_OP_DEL, key, NULL, NULL, 0, (uint64_t)time(NULL));
    }
    return 0;

}

int memory_del(MemoryCtx *ctx, const char *key) {
    LOCK(ctx);
    int rc = memory_del_unlocked(ctx, key);
    UNLOCK(ctx);
    return rc;
}

int memory_search_by_tag(MemoryCtx *ctx, const char *tag, SearchResult **r, int *cnt) {
    *r=NULL; *cnt=0;
    LOCK(ctx);
    uint32_t ec; MemEntry **es = tag_search(&ctx->tag_index,tag,&ec);
    if (!es||ec==0) { free(es); UNLOCK(ctx); return 0; }
    SearchResult *sr=(SearchResult*)calloc(ec,sizeof(SearchResult));
    if (!sr) { free(es); UNLOCK(ctx); return -1; }
    for (uint32_t i=0; i<ec; i++) {
        MemEntry *e=es[i]; char *kd=(char*)e+sizeof(MemEntry), *vd=kd+e->key_len+1, *tb=vd+e->val_len+1;
        sr[i].k=strndup(kd,e->key_len); sr[i].v=strndup(vd,e->val_len);
        sr[i].ca=(time_t)e->created_at;
        size_t tl=(size_t)e->tag_count*MAX_TAG_LEN+e->tag_count;
        sr[i].ts=(char*)malloc(tl); sr[i].ts[0]='\0';
        for (int t=0; t<e->tag_count; t++) { if (t>0) strcat(sr[i].ts,","); strcat(sr[i].ts,tb+t*MAX_TAG_LEN); }
    }
    free(es); *r=sr; *cnt=(int)ec;
    UNLOCK(ctx); return 0;
}

int memory_search_text(MemoryCtx *ctx, const char *q, SearchResult **r, int *cnt) {
    *r=NULL; *cnt=0; if (!q||!q[0]) return 0;
    LOCK(ctx);
    /* 上限: 内存 + 磁盘汇总 */
    int cap = ctx->table.cnt + 256;
    SearchResult *sr=(SearchResult*)calloc(cap,sizeof(SearchResult));
    if (!sr) { UNLOCK(ctx); return -1; }
    int f=0;
    /* 1. 内存 (热路径) */
    for (int b=0; b<HASHTABLE_SIZE; b++) {
        HashNode *n=ctx->table.b[b];
        while (n) {
            MemEntry *e=n->e; if (!(e->flags & FLAG_ACTIVE)) { n=n->next; continue; }
            char *kd=(char*)e+sizeof(MemEntry), *vd=kd+e->key_len+1;
            if (strstr(kd,q)||strstr(vd,q)) {
                sr[f].k=strndup(kd,e->key_len); sr[f].v=strndup(vd,e->val_len);
                sr[f].ca=(time_t)e->created_at;
                char *tb=vd+e->val_len+1; size_t tl=(size_t)e->tag_count*MAX_TAG_LEN+e->tag_count;
                sr[f].ts=(char*)malloc(tl); sr[f].ts[0]='\0';
                for (int t=0; t<e->tag_count; t++) { if (t>0) strcat(sr[f].ts,","); strcat(sr[f].ts,tb+t*MAX_TAG_LEN); }
                f++;
            }
            n=n->next;
        }
    }
    /* 2. 磁盘日文件扫描 (惰性皮层) */
    time_t now = time(NULL);
    struct tm ttm; localtime_r(&now,&ttm);
    char today_fn[64]; snprintf(today_fn,sizeof(today_fn),"memory-%04d-%02d-%02d.json",
        ttm.tm_year+1900,ttm.tm_mon+1,ttm.tm_mday);
    DIR *d = opendir(ctx->data_dir);
    if (d) {
        struct dirent *de;
        while ((de = readdir(d)) != NULL && f < cap) {
            const char *nm = de->d_name;
            if (strncmp(nm,"memory-",7)!=0 || strcmp(nm+strlen(nm)-5,".json")!=0) continue;
            if (strcmp(nm, today_fn) == 0) continue;
            char fp[4096]; snprintf(fp,sizeof(fp),"%s/%s",ctx->data_dir,nm);
            FILE *ff = fopen(fp,"r"); if (!ff) continue;
            char line[65536];
            while (fgets(line,sizeof(line),ff) && f < cap) {
                if (line[0]=='\n') continue;
                if (!strstr(line, q)) continue;
                char kb[MAX_KEY_LEN], vb[MAX_VAL_LEN]; uint64_t ts=0;
                if (json_get_str(line,"k",kb,sizeof(kb))<0) continue;
                /* 去重: 如果已被惰性激活加载回内存，跳过 */
                uint32_t kbh = djb2(kb);
                if (hash_lookup(&ctx->table, kbh, kb)) continue;
                if (json_get_str(line,"v",vb,sizeof(vb))<0) continue;
                json_get_u64(line,"ts",&ts);
                sr[f].k = strndup(kb, strlen(kb));
                sr[f].v = strndup(vb, strlen(vb));
                sr[f].ca = (time_t)ts;
                char tag_str[512] = "";
                char tags[MAX_TAGS][MAX_TAG_LEN]; int tc = json_get_tags(line, tags, MAX_TAGS);
                for (int ti=0; ti<tc; ti++) { if (ti>0) strcat(tag_str,","); strcat(tag_str,tags[ti]); }
                sr[f].ts = strdup(tag_str);
                f++;
            }
            fclose(ff);
        }
        closedir(d);
    }
    *r=sr; *cnt=f; UNLOCK(ctx); return 0;
}

int memory_search_date(MemoryCtx *ctx, const char *ds, SearchResult **r, int *cnt) {
    LOCK(ctx);
    *r=NULL; *cnt=0; int y,m,d; if (sscanf(ds,"%d-%d-%d",&y,&m,&d)!=3) { UNLOCK(ctx); return -1; }
    struct tm tt={0}; tt.tm_year=y-1900; tt.tm_mon=m-1; tt.tm_mday=d;
    time_t ds0=mktime(&tt), de=ds0+86400;

    /* 优先：使用 Skip List 范围查询 */
    MemEntry **entries = NULL;
    uint32_t ec = 0;
    if (sl_range(&ctx->sorted, (uint64_t)ds0, (uint64_t)de, &entries, &ec) >= 0 && ec > 0) {
        SearchResult *sr = (SearchResult*)calloc(ec, sizeof(SearchResult));
        if (!sr) { free(entries); UNLOCK(ctx); return -1; }
        int f = 0;
        for (uint32_t i = 0; i < ec; i++) {
            MemEntry *e = entries[i];
            if (!(e->flags & FLAG_ACTIVE)) continue;
            char *kd=(char*)e+sizeof(MemEntry), *vd=kd+e->key_len+1;
            sr[f].k=strndup(kd,e->key_len); sr[f].v=strndup(vd,e->val_len);
            sr[f].ca=(time_t)e->created_at;
            char *tb=vd+e->val_len+1; size_t tl=(size_t)e->tag_count*MAX_TAG_LEN+e->tag_count;
            sr[f].ts=(char*)malloc(tl); sr[f].ts[0]='\0';
            for (int t=0; t<e->tag_count; t++) { if (t>0) strcat(sr[f].ts,","); strcat(sr[f].ts,tb+t*MAX_TAG_LEN); }
            f++;
        }
        free(entries);
        *r=sr; *cnt=f; UNLOCK(ctx); return 0;
    }
    free(entries);

    /* 回退：磁盘日文件扫描 */
    SearchResult *sr=(SearchResult*)calloc(256,sizeof(SearchResult));
    if (!sr) { UNLOCK(ctx); return -1; }
    int f=0;
    char dfn[64]; snprintf(dfn,sizeof(dfn),"memory-%04d-%02d-%02d.json",y,m,d);
    char fp[4096]; snprintf(fp,sizeof(fp),"%s/%s",ctx->data_dir,dfn);
    FILE *ff = fopen(fp,"r");
    if (ff) {
        char line[65536];
        while (fgets(line,sizeof(line),ff) && f < 256) {
            if (line[0]=='\n') continue;
            char kb[MAX_KEY_LEN], vb[MAX_VAL_LEN]; uint64_t ts=0;
            if (json_get_str(line,"k",kb,sizeof(kb))<0) continue;
            if (json_get_str(line,"v",vb,sizeof(vb))<0) continue;
            json_get_u64(line,"ts",&ts);
            sr[f].k = strndup(kb, strlen(kb));
            sr[f].v = strndup(vb, strlen(vb));
            sr[f].ca = (time_t)ts;
            char tag_str[512] = "";
            char tags[MAX_TAGS][MAX_TAG_LEN]; int tc = json_get_tags(line, tags, MAX_TAGS);
            for (int ti=0; ti<tc; ti++) { if (ti>0) strcat(tag_str,","); strcat(tag_str,tags[ti]); }
            sr[f].ts = strdup(tag_str);
            f++;
        }
        fclose(ff);
    }
    *r=sr; *cnt=f; UNLOCK(ctx); return 0;
}

/* 按时间范围搜索: 使用 Skip List O(log n + k) */
int memory_search_range(MemoryCtx *ctx, uint64_t t_start, uint64_t t_end,
                         SearchResult **r, int *cnt) {
    *r = NULL; *cnt = 0;
    LOCK(ctx);
    MemEntry **entries = NULL;
    uint32_t ec = 0;
    if (sl_range(&ctx->sorted, t_start, t_end, &entries, &ec) < 0) { UNLOCK(ctx); return -1; }
    if (ec == 0) { free(entries); UNLOCK(ctx); return 0; }

    SearchResult *sr = (SearchResult*)calloc(ec, sizeof(SearchResult));
    if (!sr) { free(entries); UNLOCK(ctx); return -1; }
    int f = 0;
    for (uint32_t i = 0; i < ec; i++) {
        MemEntry *e = entries[i];
        if (!(e->flags & FLAG_ACTIVE)) continue;
        char *kd = (char*)e + sizeof(MemEntry);
        char *vd = kd + e->key_len + 1;
        sr[f].k = strndup(kd, e->key_len);
        sr[f].v = strndup(vd, e->val_len);
        sr[f].ca = (time_t)e->created_at;
        char *tb = vd + e->val_len + 1;
        size_t tl = (size_t)e->tag_count * MAX_TAG_LEN + e->tag_count;
        sr[f].ts = (char*)malloc(tl); sr[f].ts[0] = '\0';
        for (int t = 0; t < e->tag_count; t++) {
            if (t > 0) strcat(sr[f].ts, ",");
            strcat(sr[f].ts, tb + t * MAX_TAG_LEN);
        }
        f++;
    }
    free(entries);
    *r = sr; *cnt = f;
    UNLOCK(ctx);
    return 0;
}

void memory_search_free(SearchResult *r, int cnt) {
    if (!r) return;
    for (int i=0; i<cnt; i++) { free(r[i].k); free(r[i].v); free(r[i].ts); }
    free(r);
}

int memory_flush(MemoryCtx *ctx) {
    LOCK(ctx);
    int r = ovf_flush(ctx);
    /* flush 只写快照，不截断 WAL（WAL 在下次 init 后截断） */
    UNLOCK(ctx);
    return r;
}
int memory_load(MemoryCtx *ctx) { LOCK(ctx); int r=ovf_load(ctx); UNLOCK(ctx); return r; }
int memory_cleanup_ttl(MemoryCtx *ctx) { LOCK(ctx); int r=ovf_clean(ctx); UNLOCK(ctx); return r; }

void memory_stats(const MemoryCtx *ctx, char *buf, size_t bl) {
    /* 只读操作, 不加锁 */
    /* 统计所有 shard 总条目 */
    uint32_t total_entries = ctx->pool.ec;
    for (int i = 0; i < ctx->shard_count; i++)
        if (ctx->shards[i].ctx) total_entries += ctx->shards[i].ctx->pool.ec;

    char sb[2048];
    int pos = snprintf(sb, sizeof(sb),
        "=== Memory System Stats ===\n"
        "Pool: %zu/%zu (%.1f%%), %u entries, %lu allocs, %lu frees\n"
        "  Slab256: 0/%u   Slab1K: 0/%u   Slab4K: 0/%u   Slab16K: 0/%u\n"
        "  Hash table: %u entries / %u buckets\n"
        "  Tag index:  %u tags indexed\n"
        "  Sorted idx: %u entries / max lv %d\n"
        "  Data dir:   %s (TTL: %d days)\n"
        "  Shards:     %d total, %u entries\n",
        ctx->pool.used,ctx->pool.total,ctx->pool.total>0?(double)ctx->pool.used*100/ctx->pool.total:0,
        ctx->pool.ec,(unsigned long)ctx->pool.ta,(unsigned long)ctx->pool.tf,
        ctx->pool.sc[0],ctx->pool.sc[1],ctx->pool.sc[2],ctx->pool.sc[3],
        ctx->table.cnt,(uint32_t)HASHTABLE_SIZE,ctx->tag_index.cnt,
        ctx->sorted.count, ctx->sorted.top_level,
        ctx->data_dir,ctx->file_ttl,
        ctx->shard_count, total_entries);

    /* 列出所有 shard */
    for (int i = 0; i < ctx->shard_count; i++) {
        MemoryCtx *sc = ctx->shards[i].ctx;
        if (!sc) continue;
        pos += snprintf(sb + pos, sizeof(sb) - (size_t)pos > 0 ? sizeof(sb) - (size_t)pos : 0,
            "    [%s] %u entries, %zu/%zu bytes\n",
            ctx->shards[i].name, sc->pool.ec, sc->pool.used, sc->pool.total);
    }

    snprintf(buf, bl, "%s", sb);
}

/* ============================================================
 * CLI 入口
 * ============================================================ */

static void usage(void) {
    printf("usage: memory <command> [args...] [--shard <name>]\n\n"
        "commands:\n"
        "  set   <key> <value> [--tags a,b,c] [--ts <unix_sec>]    存储\n"
        "  get   <key>                            读取\n"
        "  search <query|--tag <tag>|--date YYYY-MM-DD|--range <start_ts> <end_ts>>  搜索\n"
        "  del   <key>                            删除\n"
        "  shard list                             列出所有 shard\n"
        "  flush / load / clean / stats / snapshot  管理\n"
        "  --shard <name>  指定操作目标 shard (默认: default)\n");
}

static void print_r(SearchResult *r, int cnt) {
    if (cnt==0) { printf("(no results)\n"); return; }
    for (int i=0; i<cnt; i++) {
        char tb[32]; struct tm tm; localtime_r(&r[i].ca,&tm);
        strftime(tb,sizeof(tb),"%Y-%m-%d %H:%M",&tm);
        printf("—— %s ————————————————\n  key: %s\n  tags: [%s]\n  %s\n\n",tb,r[i].k,r[i].ts?r[i].ts:"",r[i].v);
    }
    printf("(%d results)\n",cnt);
}

#ifndef TEST_MODE

/* 从 argv 中提取 --shard <name> (如果存在) */
static const char* extract_shard(int argc, char **argv) {
    for (int i = 2; i < argc - 1; i++)
        if (strcmp(argv[i], "--shard") == 0)
            return argv[i + 1];
    return NULL;
}

int main(int argc, char **argv) {
    if (argc<2) { usage(); return 1; }
    const char *cmd=argv[1];
    if (strcmp(cmd,"load")==0) {
        const char *dd=OVERFLOW_DIR; int ttl=FILE_TTL_DAYS;
        for (int i=2; i<argc; i++) {
            if (strcmp(argv[i],"--dir")==0 && i+1<argc) dd=argv[++i];
            else if (strcmp(argv[i],"--ttl")==0 && i+1<argc) ttl=atoi(argv[++i]);
        }
        MemoryCtx ctx; memory_init(&ctx,dd,ttl);
        char buf[4096]; memory_stats(&ctx,buf,sizeof(buf)); printf("%s\n",buf);
        memory_destroy(&ctx); return 0;
    }
    MemoryCtx ctx; if (memory_init(&ctx,OVERFLOW_DIR,FILE_TTL_DAYS)<0) { fprintf(stderr,"init failed\n"); return 1; }

    /* shard 子命令 */
    if (strcmp(cmd,"shard")==0) {
        if (argc<3) { fprintf(stderr,"usage: memory shard (list|create <name>)\n"); memory_destroy(&ctx); return 1; }
        if (strcmp(argv[2],"list")==0) {
            printf("Shards:\n");
            printf("  default\n");
            for (int i = 0; i < ctx.shard_count; i++)
                printf("  %s\n", ctx.shards[i].name);
            memory_destroy(&ctx); return 0;
        }
        if (strcmp(argv[2],"create")==0 && argc>3) {
            MemoryCtx *sc = memory_shard_ensure(&ctx, argv[3]);
            printf("%s\n", sc ? "ok" : "failed");
            if (sc) memory_flush(sc);
            memory_destroy(&ctx); return 0;
        }
        fprintf(stderr,"unknown: shard %s\n", argv[2]);
        memory_destroy(&ctx); return 1;
    }

    /* 提取 --shard 参数，路由到对应的 shard ctx */
    const char *shard_name = extract_shard(argc, argv);
    MemoryCtx *target = &ctx;
    if (shard_name) {
        target = memory_shard_ensure(&ctx, shard_name);
        if (!target) { memory_destroy(&ctx); return 1; }
    }

    if (strcmp(cmd,"set")==0) {
        if (argc<4) { fprintf(stderr,"usage: memory set <key> <value> [--tags a,b,c] [--ts <unix_sec>] [--shard <name>]\n"); memory_destroy(&ctx); return 1; }
        const char *tp[MAX_TAGS]; int tc=0;
        uint64_t explicit_ts = 0;
        for (int i=4; i<argc; i++) {
            if ((strcmp(argv[i],"--tags")==0||strcmp(argv[i],"--tag")==0) && i+1<argc) {
                char *ts=argv[++i], *sp;
                char *t = strtok_r(ts,",",&sp);
                while (t && tc<MAX_TAGS) { while (*t==' ') t++; size_t l=strlen(t); while (l>0&&t[l-1]==' ') t[--l]='\0'; tp[tc++]=t; t=strtok_r(NULL,",",&sp); }
            } else if (strcmp(argv[i],"--ts")==0 && i+1<argc) {
                explicit_ts = (uint64_t)atoll(argv[++i]);
            }
        }
        int rc = memory_set_with_ts(target,argv[2],argv[3],tp,tc,explicit_ts);
        if (rc == -2) printf("skipped (duplicate)\n");
        else if (rc < 0) { fprintf(stderr,"set failed\n"); memory_destroy(&ctx); return 1; }
        else printf("ok\n");
    } else if (strcmp(cmd,"get")==0) {
        if (argc<3) { memory_destroy(&ctx); return 1; }
        const char *v=memory_get(target,argv[2]);
        printf("%s\n",v?v:"(not found)");
    } else if (strcmp(cmd,"del")==0) {
        if (argc<3) { memory_destroy(&ctx); return 1; }
        printf("%s\n",memory_del(target,argv[2])<0?"(not found)":"ok");
    } else if (strcmp(cmd,"search")==0) {
        if (argc<3) { memory_destroy(&ctx); return 1; }
        SearchResult *r=NULL; int cnt=0;
        if (strcmp(argv[2],"--tag")==0&&argc>3) memory_search_by_tag(target,argv[3],&r,&cnt);
        else if (strcmp(argv[2],"--date")==0&&argc>3) memory_search_date(target,argv[3],&r,&cnt);
        else if (strcmp(argv[2],"--range")==0&&argc>4) {
            uint64_t ts_start=(uint64_t)atoll(argv[3]), ts_end=(uint64_t)atoll(argv[4]);
            memory_search_range(target,ts_start,ts_end,&r,&cnt);
        } else memory_search_text(target,argv[2],&r,&cnt);
        print_r(r,cnt); memory_search_free(r,cnt);
    } else if (strcmp(cmd,"flush")==0) printf("flushed %d\n",memory_flush_shards(&ctx));
    else if (strcmp(cmd,"snapshot")==0) {
        pid_t child_pid = (pid_t)memory_fork_snapshot(&ctx);
        if (child_pid < 0) { fprintf(stderr,"snapshot fork failed\n"); memory_destroy(&ctx); return 1; }
        int status;
        waitpid(child_pid, &status, 0);
        printf("%s\n", (WIFEXITED(status) && WEXITSTATUS(status) == 0) ? "snapshot ok" : "snapshot failed");
    } else if (strcmp(cmd,"clean")==0) printf("cleaned %d\n",memory_cleanup_ttl(target));
    else if (strcmp(cmd,"stats")==0) { char b[4096]; memory_stats(&ctx,b,sizeof(b)); printf("%s\n",b); }
    else { fprintf(stderr,"unknown: %s\n",cmd); usage(); memory_destroy(&ctx); return 1; }
    memory_destroy(&ctx); return 0;
}
#endif

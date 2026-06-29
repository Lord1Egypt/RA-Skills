/*
 * hash_bench.c — djb2 vs MurmurHash3 vs xxHash: 冲突率 & 性能对比
 * Compile: gcc -O2 hash_bench.c -o hash_bench
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* ============================================================
 * djb2
 * ============================================================ */
static uint32_t djb2(const char *s) {
    uint32_t h = 5381;
    int c;
    while ((c = (unsigned char)*s++))
        h = ((h<<5)+h) + (uint32_t)c;
    return h;
}

/* ============================================================
 * MurmurHash3 32-bit (x86)
 * ============================================================ */
static uint32_t mmh3_32(const char *key, int len, uint32_t seed) {
    const uint8_t *data = (const uint8_t*)key;
    int nblocks = len / 4;
    uint32_t h1 = seed;
    uint32_t c1 = 0xcc9e2d51;
    uint32_t c2 = 0x1b873593;
    const uint32_t *blocks = (const uint32_t*)(data);
    for (int i = 0; i < nblocks; i++) {
        uint32_t k1 = blocks[i];
        k1 *= c1; k1 = (k1 << 15) | (k1 >> 17); k1 *= c2;
        h1 ^= k1; h1 = (h1 << 13) | (h1 >> 19); h1 = h1*5 + 0xe6546b64;
    }
    const uint8_t *tail = data + nblocks*4;
    uint32_t k1 = 0;
    switch (len & 3) {
        case 3: k1 ^= tail[2] << 16;
        case 2: k1 ^= tail[1] << 8;
        case 1: k1 ^= tail[0]; k1 *= c1; k1 = (k1<<15)|(k1>>17); k1 *= c2; h1 ^= k1;
    }
    h1 ^= len;
    h1 ^= h1>>16; h1 *= 0x85ebca6b;
    h1 ^= h1>>13; h1 *= 0xc2b2ae35;
    h1 ^= h1>>16;
    return h1;
}

static uint32_t mmh3_wrap(const char *s) { return mmh3_32(s, (int)strlen(s), 42); }

/* ============================================================
 * xxHash 32-bit
 * ============================================================ */
static uint32_t xxh32(const char *input, int len, uint32_t seed) {
    const uint8_t *p = (const uint8_t*)input;
    uint32_t h32;
    enum { PRIME32_1=2654435761U, PRIME32_2=2246822519U, PRIME32_3=3266489917U,
           PRIME32_4=668265263U, PRIME32_5=374761393U };
    if (len >= 16) {
        uint32_t v1 = seed + PRIME32_1 + PRIME32_2;
        uint32_t v2 = seed + PRIME32_2;
        uint32_t v3 = seed;
        uint32_t v4 = seed - PRIME32_1;
        const uint8_t *limit = p + len - 16;
        do {
            uint32_t l1 = *(uint32_t*)p; p += 4;
            uint32_t l2 = *(uint32_t*)p; p += 4;
            uint32_t l3 = *(uint32_t*)p; p += 4;
            uint32_t l4 = *(uint32_t*)p; p += 4;
            l1 *= PRIME32_2; l1 = (l1<<13)|(l1>>19); l1 *= PRIME32_1; v1 = (v1<<1)|(v1>>31); v1 += l1;
            l2 *= PRIME32_2; l2 = (l2<<13)|(l2>>19); l2 *= PRIME32_1; v2 = (v2<<7)|(v2>>25); v2 += l2;
            l3 *= PRIME32_2; l3 = (l3<<13)|(l3>>19); l3 *= PRIME32_1; v3 = (v3<<12)|(v3>>20); v3 += l3;
            l4 *= PRIME32_2; l4 = (l4<<13)|(l4>>19); l4 *= PRIME32_1; v4 = (v4<<18)|(v4>>14); v4 += l4;
        } while (p <= limit);
        h32 = (v1<<1)|(v1>>31); h32 += (v2<<7)|(v2>>25);
        h32 += (v3<<12)|(v3>>20); h32 += (v4<<18)|(v4>>14);
    } else {
        h32 = seed + PRIME32_5;
    }
    h32 += len;
    while (p + 4 <= input + len) {
        uint32_t l1 = *(uint32_t*)p; p += 4;
        h32 += l1*PRIME32_3; h32 = (h32<<17)|(h32>>15); h32 *= PRIME32_4;
    }
    while (p < input + len) {
        h32 += (*p)*PRIME32_5; h32 = (h32<<11)|(h32>>21); h32 *= PRIME32_1;
        p++;
    }
    h32 ^= h32>>15; h32 *= PRIME32_2;
    h32 ^= h32>>13; h32 *= PRIME32_3;
    h32 ^= h32>>16;
    return h32;
}

static uint32_t xxh_wrap(const char *s) { return xxh32(s, (int)strlen(s), 42); }

/* ============================================================
 * 测试
 * ============================================================ */
#define BUCKETS 4096
#define N_KEYS  100000

static char rand_char(void) {
    static const char chars[] = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    return chars[rand() % (sizeof(chars)-1)];
}

static void gen_key(char *buf, int len) {
    for (int i = 0; i < len-1; i++) buf[i] = rand_char();
    buf[len-1] = '\0';
}

static void collision_test(const char *label, uint32_t (*hash_fn)(const char*),
                           int key_len) {
    int bc[BUCKETS] = {0};
    char key[65];
    for (int i = 0; i < N_KEYS; i++) {
        gen_key(key, key_len);
        bc[hash_fn(key) % BUCKETS]++;
    }
    int used = 0, max_c = 0, collided = 0;
    double sum_chain = 0;
    for (int i = 0; i < BUCKETS; i++) {
        if (bc[i]) { used++; sum_chain += bc[i]; if (bc[i] > max_c) max_c = bc[i]; }
        if (bc[i] > 1) collided += bc[i] - 1;
    }
    printf("  %-18s key=%dB  used=%d/%d  max_chain=%d  avg_chain=%.1f  collisions=%d (%.3f%%)\n",
           label, key_len, used, BUCKETS, max_c, sum_chain/used, collided,
           100.0*collided/N_KEYS);
}

static void throughput_test(const char *label, uint32_t (*hash_fn)(const char*),
                            char keys[][65], int n) {
    struct timespec ts;
    uint64_t _sink = 0;
    /* warmup */
    for (int i = 0; i < 10000; i++) _sink ^= hash_fn(keys[i % n]);
    clock_gettime(CLOCK_MONOTONIC, &ts);
    uint64_t t0 = (uint64_t)ts.tv_sec * 1000000000UL + (uint64_t)ts.tv_nsec;
    int total_ops = 100 * n;
    for (int iter = 0; iter < 100; iter++)
        for (int i = 0; i < n; i++)
            _sink ^= hash_fn(keys[i]);
    clock_gettime(CLOCK_MONOTONIC, &ts);
    uint64_t t1 = (uint64_t)ts.tv_sec * 1000000000UL + (uint64_t)ts.tv_nsec;
    printf("  %-18s %.1f ns/hash\n", label, (double)(t1-t0)/total_ops);
    (void)_sink;
}

int main(void) {
    srand(42);
    printf("═══════════════════════════════════════════════════════\n");
    printf("  Hash Analysis: djb2 vs MurmurHash3 vs xxHash\n");
    printf("  buckets=%d  keys=%d\n", BUCKETS, N_KEYS);
    printf("═══════════════════════════════════════════════════════\n");

    printf("\n--- Collision Rate ---\n");
    int key_lens[] = {8, 16, 32, 64};
    for (int ki = 0; ki < 4; ki++) {
        printf("\n");
        collision_test("djb2", djb2, key_lens[ki]);
        collision_test("murmur3-32", mmh3_wrap, key_lens[ki]);
        collision_test("xxh32", xxh_wrap, key_lens[ki]);
    }

    printf("\n--- Throughput ---\n");
    char key_samples[N_KEYS][65];
    for (int i = 0; i < N_KEYS; i++) gen_key(key_samples[i], 16 + (i%32));
    throughput_test("djb2", djb2, key_samples, N_KEYS);
    throughput_test("murmur3-32", mmh3_wrap, key_samples, N_KEYS);
    throughput_test("xxh32", xxh_wrap, key_samples, N_KEYS);

    printf("\n--- Real-world: sequential date keys (hipool format) ---\n");
    {
        int bc[BUCKETS] = {0};
        char k[32];
        for (int i = 0; i < 10000; i++) {
            snprintf(k, 32, "2026-06-%02d-%d", (i/100)+1, i%100);
            bc[djb2(k) % BUCKETS]++;
        }
        int used = 0, max_c = 0, collided = 0;
        for (int i = 0; i < BUCKETS; i++) {
            if (bc[i]) used++;
            if (bc[i] > 1) collided += bc[i]-1;
            if (bc[i] > max_c) max_c = bc[i];
        }
        printf("  djb2 (date keys):  used=%d/%d  collided=%d  max_chain=%d\n",
               used, BUCKETS, collided, max_c);
    }

    printf("\n═══════════════════════════════════════════════════════\n");
    printf("  Done.\n");
    return 0;
}

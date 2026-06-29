#!/bin/bash
# hipool v4.5 消融实验 — 逐个剥新功能找 bug
# 不使用 set -e — 预期失败也是测试的一部分
set +e
cd "$(dirname "$0")"

PASS=0; FAIL=0; TOTAL=0
RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; NC='\033[0m'
OK() { TOTAL=$((TOTAL+1)); PASS=$((PASS+1)); echo -e "  ${GREEN}✓${NC} $1"; }
FAIL() { TOTAL=$((TOTAL+1)); FAIL=$((FAIL+1)); echo -e "  ${RED}✗${NC} $1"; }

cleanup() { rm -rf memory_data; }

echo -e "${CYAN}══════════════════════════════════════════════${NC}"
echo -e "${CYAN}  hipool v4.5 消融实验 — 边界条件压力测试${NC}"
echo -e "${CYAN}══════════════════════════════════════════════${NC}"
echo ""

# =============================================================
# 1. Skip List 排序索引 — 边界
# =============================================================
echo -e "${CYAN}[1/6] SkipList 排序索引${NC}"
cleanup; mkdir -p memory_data

# 1a. 时间戳完全相同的条目（复合排序键 key_hash 分胜负）
for i in $(seq 1 20); do ./memory set "ts_collide_$i" "val_$i" --ts 1000000000 >/dev/null 2>&1; done
NOW=1000000000
r=$(./memory search --range 999999999 1000000001 2>/dev/null)
c=$(echo "$r" | grep -c "^  key:")
[ "$c" -eq 20 ] && OK "1a 同时间戳20条->$c" || FAIL "1a 同时间戳: 期望20->$c"

# 1b. 空范围查询
r=$(./memory search --range 1 2 2>/dev/null)
echo "$r" | grep -q "no results" && OK "1b 空范围->no results" || FAIL "1b 空范围"

# 1c. 超大范围（uint64 边界）
r=$(./memory search --range 0 999999999999999 2>/dev/null)
c=$(echo "$r" | grep -c "^  key:")
[ "$c" -ge 20 ] && OK "1c 超大范围->$c" || FAIL "1c 超大范围: $c"

# 1d. 范围开始 == 结束
r=$(./memory search --range $NOW $NOW 2>/dev/null)
echo "$r" | grep -q "no results" && OK "1d start==end" || FAIL "1d start==end"

# 1e. 插入后删除全部再范围查询
for i in $(seq 1 20); do ./memory del "ts_collide_$i" >/dev/null 2>&1; done
r=$(./memory search --range 0 999999999999999 2>/dev/null)
echo "$r" | grep -q "no results" && OK "1e 删光后范围空" || FAIL "1e 删光后范围"

echo ""

# =============================================================
# 2. SkipList 大量数据穿透测试
# =============================================================
echo -e "${CYAN}[2/6] SkipList 大量数据${NC}"
cleanup; mkdir -p memory_data

# 2a. 密集插入 500 条（接近上限）
for i in $(seq 1 500); do
  ./memory set "bulk_$(printf '%04d' $i)" "data_$i" --ts $((1000000 + i)) >/dev/null 2>&1
done
r=$(./memory stats 2>/dev/null)
echo "$r" | grep -q "500 entries" && OK "2a 500条批量插入" || FAIL "2a: $(echo "$r" | grep entries)"

# 2b. 范围查询全部 (半开区间 [start, end), 所以 end 要 +1)
r=$(./memory search --range 1000000 1000501 2>/dev/null)
c=$(echo "$r" | grep -c "^  key:")
[ "$c" -eq 500 ] && OK "2b 范围查询500条->$c" || FAIL "2b 范围查询: $c/500"

# 2c. 删除一半（ID 奇偶删除）
for i in $(seq 1 2 500); do
  ./memory del "bulk_$(printf '%04d' $i)" >/dev/null 2>&1
done
r=$(./memory stats 2>/dev/null)
echo "$r" | grep -q "250 entries" && OK "2c 删除250条后->250" || FAIL "2c 删一半"

# 2d. 范围查询删除后剩余
r=$(./memory search --range 1000000 1000501 2>/dev/null)
c=$(echo "$r" | grep -c "^  key:")
[ "$c" -eq 250 ] && OK "2d 范围查询250条->$c" || FAIL "2d 范围查询: $c/250"

# 2e. 交错时间戳插入（验证排序顺序）
cleanup; mkdir -p memory_data
for i in 10 20 5 15 1 25; do
  ./memory set "order_$i" "v_$i" --ts $i >/dev/null 2>&1
done
r=$(./memory search --range 0 100 2>/dev/null)
# 按时间顺序应该是: 1,5,10,15,20,25
order=$(echo "$r" | grep "^  key:" | sed 's/.*order_//' | paste -sd ' ')
[ "$order" = "1 5 10 15 20 25" ] && OK "2e 排序顺序: $order" || FAIL "2e 排序: '$order' expect '1 5 10 15 20 25'"

echo ""

# =============================================================
# 3. WAL 崩溃恢复 — 边界
# =============================================================
echo -e "${CYAN}[3/6] WAL 预写日志${NC}"
cleanup; mkdir -p memory_data

# 3a. 正常 WAL 写 + 恢复
./memory set wal_a "survive" --tags w >/dev/null 2>&1
rm -f memory_data/memory_snapshot.json
r=$(./memory get wal_a 2>/dev/null)
[ "$r" = "survive" ] && OK "3a WAL 基本恢复" || FAIL "3a WAL 恢复: '$r'"

# 3b. WAL 是进程内崩溃恢复机制, 跨进程不生效。测试单进程内写 100 条后崩溃恢复
cat > /tmp/wal_bulk_test.c << 'WEOF'
#define _POSIX_C_SOURCE 200809L
#define TEST_MODE 1
#include "/root/.openclaw/workspace/skills/memory-c/memory.c"
#undef main
int main(void) {
    MemoryCtx ctx;
    mkdir("memory_data", 0755);
    memory_init(&ctx, "memory_data", 7);
    for (int i = 0; i < 100; i++) {
        char k[64], v[64];
        snprintf(k,64,"wal_bulk_%d",i); snprintf(v,64,"val_%d",i);
        const char *t[]={"w"};
        memory_set(&ctx, k, v, t, 1);
    }
    /* crash: 不调 memory_destroy */
    _exit(0);
}
WEOF
gcc -I/root/.openclaw/workspace/skills/memory-c -O0 /tmp/wal_bulk_test.c -o /tmp/wal_bulk_test 2>&1 | grep -v warning | grep -v note | head -1
cleanup; mkdir -p memory_data
/tmp/wal_bulk_test 2>/dev/null
rm -f memory_data/memory_snapshot.json
r=$(./memory search --tag w 2>/dev/null)
c=$(echo "$r" | grep -c "^  key:")
[ "$c" -eq 100 ] && OK "3b 进程内WAL恢复100条->$c" || FAIL "3b 进程内WAL恢复: $c"

# 3c. WAL + DEL 混合恢复
cleanup; mkdir -p memory_data
./memory set w_del "will_be_deleted" >/dev/null 2>&1
./memory del w_del >/dev/null 2>&1
./memory set w_keep "should_exist" >/dev/null 2>&1
rm -f memory_data/memory_snapshot.json
r=$(./memory get w_del 2>/dev/null)
[ "$r" = "(not found)" ] && OK "3c DEL 记录恢复后消失" || FAIL "3c DEL 恢复: '$r'"
r=$(./memory get w_keep 2>/dev/null)
[ "$r" = "should_exist" ] && OK "3c SET 记录恢复后存在" || FAIL "3c SET 恢复: '$r'"

# 3d. 空 WAL 文件（0 字节）
cleanup; mkdir -p memory_data
touch memory_data/wal.log
./memory stats >/dev/null 2>&1 && OK "3d 空 WAL 不崩溃" || FAIL "3d 空 WAL 崩溃"

# 3e. 损坏的 WAL（随机字节）
cleanup; mkdir -p memory_data
dd if=/dev/urandom of=memory_data/wal.log bs=1024 count=1 2>/dev/null
./memory stats >/dev/null 2>&1 && OK "3e 损坏 WAL 不崩溃" || FAIL "3e 损坏 WAL 崩溃"

# 3f. flush 后数据在 snapshot 中, WAL 被截断。删 snapshot 后不应恢复（correct behavior）
cleanup; mkdir -p memory_data
./memory set w_final "final" >/dev/null 2>&1
./memory flush >/dev/null 2>&1
rm -f memory_data/memory_snapshot.json
r=$(./memory get w_final 2>/dev/null)
[ "$r" = "(not found)" ] && OK "3f flush后删snapshot=丢(正确): $r" || FAIL "3f flush后数据应该丢失: '$r'"
# flush 前保留 snapshot，数据应在
./memory set w_keep "keep" >/dev/null 2>&1
r=$(./memory get w_keep 2>/dev/null)
[ "$r" = "keep" ] && OK "3f flush不删snapshot: $r" || FAIL "3f flush: '$r'"

echo ""

# =============================================================
# 4. Shard 分区 — 隔离 + 边界
# =============================================================
echo -e "${CYAN}[4/6] Shard 分区${NC}"
cleanup; mkdir -p memory_data

# 4a. 多 shard 隔离
for s in a b c d e; do
  ./memory set "k_$s" "val_$s" --shard "shard_$s" >/dev/null 2>&1
done
for s in a b c d e; do
  r=$(./memory get "k_$s" --shard "shard_$s" 2>/dev/null)
  [ "$r" = "val_$s" ] || FAIL "4a shard_$s: '$r'"
done
OK "4a 5个shard隔离"

# 4b. 默认 shard 不应有 shard 数据
r=$(./memory get k_a 2>/dev/null)
[ "$r" = "(not found)" ] && OK "4b 默认shard无泄漏" || FAIL "4b 泄漏: '$r'"

# 4c. shard 数量上限（MAX_SHARDS=8，已有5个占5个名额，只能再建3个）
for s in 1 2 3; do
  ./memory set x "y" --shard "sc_$s" >/dev/null 2>&1
done
# 第9个应失败
r=$(./memory set x "y" --shard overflow 2>&1)
echo "$r" | grep -q "max shards" && OK "4c 超限拒绝" || FAIL "4c 超限: '$r'"

# 4d. shard 内范围查询
cleanup; mkdir -p memory_data
for i in $(seq 1 30); do
  ./memory set "s_item_$i" "sv_$i" --ts $((2000000 + i)) --shard srange >/dev/null 2>&1
done
r=$(./memory search --range 2000005 2000015 --shard srange 2>/dev/null)
c=$(echo "$r" | grep -c "^  key:")
[ "$c" -eq 10 ] && OK "4d shard 范围查询->$c" || FAIL "4d shard 范围: $c"

# 4e. shard 删除后数据隔离
./memory del s_item_5 --shard srange >/dev/null 2>&1
r=$(./memory get s_item_5 --shard srange 2>/dev/null)
[ "$r" = "(not found)" ] && OK "4e shard 删除" || FAIL "4e shard 删除: '$r'"

# 4f. shard flush 后重载
cleanup; mkdir -p memory_data
./memory set persist_k "persist_v" --shard persist >/dev/null 2>&1
./memory flush >/dev/null 2>&1
r=$(./memory get persist_k --shard persist 2>/dev/null)
[ "$r" = "persist_v" ] && OK "4f shard flush+reload" || FAIL "4f shard flush: '$r'"

echo ""

# =============================================================
# 5. Fork Snapshot
# =============================================================
echo -e "${CYAN}[5/6] Fork Snapshot${NC}"
cleanup; mkdir -p memory_data

# 5a. 基本 snapshot
./memory set fs1 "data1" >/dev/null 2>&1
r=$(./memory snapshot 2>&1)
echo "$r" | grep -q "snapshot ok" && OK "5a snapshot 基本" || FAIL "5a snapshot: '$r'"

# 5b. snapshot 后数据完整
r=$(./memory get fs1 2>/dev/null)
[ "$r" = "data1" ] && OK "5b snapshot 后数据" || FAIL "5b snapshot 后: '$r'"

# 5c. snapshot 期间修改不影响子进程
cleanup; mkdir -p memory_data
./memory set before "before_val" >/dev/null 2>&1
# fork 后父进程立即修改
(./memory snapshot >/dev/null 2>&1) &
sleep 0.1
./memory set after "after_val" >/dev/null 2>&1
wait
r=$(./memory get before 2>/dev/null)
[ "$r" = "before_val" ] && OK "5c snapshot+并发写入" || FAIL "5c 并发: '$r'"

# 5d. 空数据 snapshot
cleanup; mkdir -p memory_data
r=$(./memory snapshot 2>&1)
echo "$r" | grep -q "snapshot ok" && OK "5d 空 snapshot" || FAIL "5d 空 snapshot: '$r'"

# 5e. shard + snapshot
cleanup; mkdir -p memory_data
./memory set fk "fv" --shard fs >/dev/null 2>&1
./memory snapshot >/dev/null 2>&1
r=$(./memory get fk --shard fs 2>/dev/null)
[ "$r" = "fv" ] && OK "5e shard+snapshot" || FAIL "5e shard+snapshot: '$r'"

echo ""

# =============================================================
# 6. 综合边界 — 并发 + 混合操作
# =============================================================
echo -e "${CYAN}[6/6] 综合边界${NC}"
cleanup; mkdir -p memory_data

# 6a. 中文 key/value
./memory set "你好世界" "这是一段测试文本" --tags 中文 >/dev/null 2>&1
r=$(./memory get "你好世界" 2>/dev/null)
[ "$r" = "这是一段测试文本" ] && OK "6a 中文 key" || FAIL "6a 中文: '$r'"

# 6b. emoji 值
./memory set emoji_key "🔥测试🔥" >/dev/null 2>&1
r=$(./memory get emoji_key 2>/dev/null)
[ "$r" = "🔥测试🔥" ] && OK "6b emoji" || FAIL "6b emoji: '$r'"

# 6c. 255 字节 key
k256=$(python3 -c "print('k'*255)")
./memory set "$k256" "long_key_test" >/dev/null 2>&1
r=$(./memory search "long_key_test" 2>/dev/null)
echo "$r" | grep -q "long_key_test" && OK "6c 255B key" || FAIL "6c 255B key"

# 6d. 空 value
./memory set empty_val "" >/dev/null 2>&1
r=$(./memory get empty_val 2>/dev/null)
[ "$r" = "" ] && OK "6d 空 value" || FAIL "6d 空 value: '$r'"

# 6e. 超大 value（接近 16320 上限）
big=$(python3 -c "print('B'*16000)")
./memory set big_val "$big" >/dev/null 2>&1
r=$(./memory get big_val 2>/dev/null)
[ "${#r}" -eq 16000 ] && OK "6e 16KB value" || FAIL "6e 16KB: len=${#r}"

# 6f. 无 tags
./memory set notag "value" >/dev/null 2>&1
r=$(./memory search --tag nonexistent 2>/dev/null)
echo "$r" | grep -q "no results" && OK "6f 无tag搜索" || FAIL "6f 无tag搜索"

# 6g. 重复 key 覆盖
./memory set dupkey "first" >/dev/null 2>&1
./memory set dupkey "second" >/dev/null 2>&1
r=$(./memory get dupkey 2>/dev/null)
[ "$r" = "second" ] && OK "6g key 覆盖" || FAIL "6g 覆盖: '$r'"

# 6h. 16 个标签
tags=$(python3 -c "print(','.join([f't{i}' for i in range(16)]))")
./memory set manytags "v" --tags "$tags" >/dev/null 2>&1
r=$(./memory search --tag t15 2>/dev/null)
echo "$r" | grep -q "manytags" && OK "6h 16标签" || FAIL "6h 16标签"

# 6i. --date 查询旧数据（日期跨边界）
cleanup; mkdir -p memory_data
# 写入带特定日期的数据
./memory set old_entry "old" --ts 1700000000 >/dev/null 2>&1
./memory set new_entry "new" --ts 1800000000 >/dev/null 2>&1
r=$(./memory search --range 1700000000 1700000001 2>/dev/null)
echo "$r" | grep -q "old_entry" && ! echo "$r" | grep -q "new_entry" && OK "6i 时间范围精确" || FAIL "6i 时间范围"

# 6j. Mutex 版编译 + 基本功能
gcc -O2 -DHIPOOL_USE_MUTEX memory.c -o /tmp/hipool_mt -lpthread 2>&1 | grep -v warning | grep -v note | head -3
/tmp/hipool_mt set mt "mt_val" >/dev/null 2>&1
r=$(/tmp/hipool_mt get mt 2>/dev/null)
[ "$r" = "mt_val" ] && OK "6j Mutex 版" || FAIL "6j Mutex: '$r'"
rm -f /tmp/hipool_mt

# 6k. snapshot 拒绝（mutex 模式）
gcc -O2 -DHIPOOL_USE_MUTEX memory.c -o /tmp/hipool_mt -lpthread 2>&1
r=$(/tmp/hipool_mt snapshot 2>&1)
echo "$r" | grep -q "failed" && OK "6k Mutex snapshot拒绝" || FAIL "6k Mutex snapshot: '$r'"
rm -f /tmp/hipool_mt

echo ""
echo -e "${CYAN}══════════════════════════════════════════════${NC}"
echo -e "  ${GREEN}通过: $PASS/$TOTAL  |  失败: $FAIL${NC}"
echo -e "${CYAN}══════════════════════════════════════════════${NC}"
exit $FAIL

#!/bin/bash
# hipool 一键测试脚本
set -e

HIPOOL_DIR="$(cd "$(dirname "$0")" && pwd)"
MEMORY="$HIPOOL_DIR/memory"
PASS=0; FAIL=0; TOTAL=0
RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; NC='\033[0m'

cleanup() { rm -rf "$1/memory_data"; }

run_test() {
    local name="$1" srcdir="$2" verify_cmd="$3"
    TOTAL=$((TOTAL+1))
    local testdir="$HIPOOL_DIR/$srcdir"

    mkdir -p "$testdir/memory_data"
    for f in "$testdir"/*.json; do [ -f "$f" ] && cp "$f" "$testdir/memory_data/"; done

    cd "$testdir"
    $MEMORY load 2>/dev/null

    if eval "$verify_cmd" 2>/dev/null; then
        echo -e "  ${GREEN}✓ PASS${NC}  $name"
        PASS=$((PASS+1))
    else
        echo -e "  ${RED}✗ FAIL${NC}  $name"
        FAIL=$((FAIL+1))
    fi

    cleanup "$testdir"
    cd "$HIPOOL_DIR"
}

echo -e "${CYAN}══════════════════════════════════════${NC}"
echo -e "${CYAN}  hipool 测试套件${NC}"
echo -e "${CYAN}══════════════════════════════════════${NC}"
echo ""

# 1. 基础功能
echo -e "${CYAN}[1/8] 基础功能${NC}"
run_test "单条读写(含中文/emoji)" "test_uni" \
    'r=$($MEMORY search "中文键" 2>/dev/null); echo "$r" | grep -q "这是一段中文记忆内容"'
run_test "按标签搜索(中文标签)" "test_uni" \
    'r=$($MEMORY search --tag "中文标签" 2>/dev/null); echo "$r" | grep -q "中文键"'

# 2. 数据搜索
echo -e "\n${CYAN}[2/8] 数据搜索${NC}"
run_test "全局搜索" "test_data" \
    'r=$($MEMORY search "cherry" 2>/dev/null); echo "$r" | grep -q "A small red fruit"'
run_test "按标签搜索" "test_data" \
    'r=$($MEMORY search --tag "fruit" 2>/dev/null); echo "$r" | grep -q "cherry"'
run_test "按日期搜索" "test_data" \
    'r=$($MEMORY search --date 2026-05-28 2>/dev/null); [ "$(echo "$r" | grep -c "^  key:")" -ge 10 ]'

# 3. Hash碰撞
echo -e "\n${CYAN}[3/8] Hash碰撞${NC}"
run_test "50条同前缀键" "test_coll" \
    'r=$($MEMORY search "same_prefix" 2>/dev/null); [ "$(echo "$r" | grep -c "^  key:")" -eq 50 ]'

# 4. 随机数据
echo -e "\n${CYAN}[4/8] 随机数据${NC}"
run_test "101条随机键值" "test_rand" \
    'r=$($MEMORY search "rand_" 2>/dev/null); [ "$(echo "$r" | grep -c "^  key:")" -eq 101 ]'
run_test "随机单条检索" "test_rand" \
    'r=$($MEMORY search "rand_100" 2>/dev/null); echo "$r" | grep -q "random_val"'

# 5. 批量压力
echo -e "\n${CYAN}[5/8] 批量压力${NC}"
run_test "354条批量内存加载" "test_fill" \
    '$MEMORY stats 2>/dev/null | grep -q "354 entries"'
run_test "批量数据逐条验证" "test_fill" \
    'r=$($MEMORY search "fill_00350" 2>/dev/null); echo "$r" | grep -q "Filler entry number 00350"'

# 6. 边界条件
echo -e "\n${CYAN}[6/8] 边界条件${NC}"
run_test "255字节超长key" "test_edge" \
    'r=$($MEMORY search --date 2026-05-28 2>/dev/null); long=$(python3 -c "print(\"k\"*255)"); echo "$r" | grep -qF "$long"'
run_test "空value条目" "test_edge" \
    'r=$($MEMORY search "empty" 2>/dev/null); echo "$r" | grep -q "empty"'
run_test "空标签条目" "test_edge" \
    'r=$($MEMORY search "notags" 2>/dev/null); echo "$r" | grep -q "value"'

# 7. 循环覆盖
echo -e "\n${CYAN}[7/8] 循环覆盖${NC}"
run_test "循环写入3条" "test_cycle" \
    'r=$($MEMORY search "cycle_" 2>/dev/null); [ "$(echo "$r" | grep -c "^  key:")" -eq 3 ]'

# 8. 持久化
echo -e "\n${CYAN}[8/8] 持久化${NC}"
run_test "flush刷盘" "test_data" \
    '$MEMORY flush 2>/dev/null && [ -f "$HIPOOL_DIR/test_data/memory_data/memory_snapshot.json" ]'
run_test "load重载后数据可恢复" "test_data" \
    '$MEMORY load 2>/dev/null && r=$($MEMORY search --date 2026-05-28 2>/dev/null); echo "$r" | grep -q "cherry"'

# 汇总
echo ""
echo -e "${CYAN}══════════════════════════════════════${NC}"
if [ $FAIL -eq 0 ]; then
    echo -e "  ${GREEN}全部通过: $PASS/$TOTAL${NC} ✨"
else
    echo -e "  ${RED}通过: $PASS/$TOTAL  |  失败: $FAIL${NC}"
fi
echo -e "${CYAN}══════════════════════════════════════${NC}"
exit $FAIL

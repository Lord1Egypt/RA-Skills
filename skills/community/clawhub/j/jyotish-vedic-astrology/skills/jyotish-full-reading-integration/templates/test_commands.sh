#!/bin/bash
# jyotish_engine.py v4.4.0 测试脚本

set -e  # 遇到错误立即退出

echo "========================================="
echo "jyotish_engine.py v4.4.0 集成测试"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试计数器
PASSED=0
FAILED=0

# 测试函数
test_module() {
    local module_name=$1
    local test_command=$2
    
    echo -e "${YELLOW}测试 ${module_name}...${NC}"
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ ${module_name} 测试通过${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ ${module_name} 测试失败${NC}"
        ((FAILED++))
    fi
    echo ""
}

# 1. 检查依赖
echo "1. 检查依赖..."
test_module "swisseph" "python3 -c 'import swisseph'"
test_module "numpy" "python3 -c 'import numpy'"

# 2. 检查模块文件存在
echo "2. 检查模块文件..."
test_module "karaka_calculator.py" "test -f scripts/karaka_calculator.py"
test_module "special_lagnas.py" "test -f scripts/special_lagnas.py"
test_module "vimsopaka_calculator.py" "test -f scripts/vimsopaka_calculator.py"
test_module "avastha_calculator.py" "test -f scripts/avastha_calculator.py"
test_module "divisional_charts_extended.py" "test -f scripts/divisional_charts_extended.py"

# 3. 单元测试（如果模块支持 --test 参数）
echo "3. 单元测试..."
test_module "special_lagnas 单元测试" "python3 scripts/special_lagnas.py --asc 45.5 --sun 120.3 --moon 200.1"
test_module "karaka_calculator 单元测试" "python3 scripts/karaka_calculator.py --mode jh --planets 'Sun:45.5,Moon:120.3,Mars:200.1,Mercury:50.8,Jupiter:180.5,Venus:90.2,Saturn:250.7,Rahu:150.4'"

# 4. 集成测试（完整调用链）
echo "4. 集成测试（完整调用链）..."

# 测试数据
BIRTH_DATE="1990-01-01"
BIRTH_TIME="12:00:00"
LATITUDE="28.6139"
LONGITUDE="77.2090"
TIMEZONE="Asia/Kolkata"

# 运行 full-reading
echo -e "${YELLOW}运行 full-reading...${NC}"
OUTPUT=$(python3 scripts/jyotish_engine.py \
    --mode full-reading \
    --birth-date "$BIRTH_DATE" \
    --birth-time "$BIRTH_TIME" \
    --latitude "$LATITUDE" \
    --longitude "$LONGITUDE" \
    --timezone "$TIMEZONE" 2>&1)

# 检查输出是否包含关键字段
echo "5. 验证输出结构..."
test_module "version 字段" "echo '$OUTPUT' | grep -q '4.4.0-full-reading'"
test_module "special_lagnas 模块" "echo '$OUTPUT' | grep -q 'special_lagnas'"
test_module "vimsopaka 模块" "echo '$OUTPUT' | grep -q 'vimsopaka'"
test_module "varga_extended 模块" "echo '$OUTPUT' | grep -q 'varga_extended'"
test_module "chara_karaka_jh 模块" "echo '$OUTPUT' | grep -q 'chara_karaka_jh'"
test_module "avasthas 模块" "echo '$OUTPUT' | grep -q 'avasthas'"

# 6. JH 兼容模式验证
echo "6. JH 兼容模式验证..."
test_module "Rahu 在 MK 位置" "echo '$OUTPUT' | grep -q 'MK.*Rahu'"

# 7. 性能测试
echo "7. 性能测试..."
echo -e "${YELLOW}测量执行时间...${NC}"
START_TIME=$(date +%s)
python3 scripts/jyotish_engine.py \
    --mode full-reading \
    --birth-date "$BIRTH_DATE" \
    --birth-time "$BIRTH_TIME" \
    --latitude "$LATITUDE" \
    --longitude "$LONGITUDE" \
    --timezone "$TIMEZONE" > /dev/null 2>&1
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo -e "${GREEN}执行时间: ${DURATION} 秒${NC}"
if [ $DURATION -lt 10 ]; then
    echo -e "${GREEN}✓ 性能测试通过（< 10秒）${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ 性能测试警告（>= 10秒）${NC}"
fi
echo ""

# 8. 输出测试结果
echo "========================================="
echo "测试结果汇总"
echo "========================================="
echo -e "${GREEN}通过: $PASSED${NC}"
echo -e "${RED}失败: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ 所有测试通过！${NC}"
    exit 0
else
    echo -e "${RED}✗ 有 $FAILED 个测试失败${NC}"
    exit 1
fi

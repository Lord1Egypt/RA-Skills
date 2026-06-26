#!/bin/bash
# CodeQL + LLM 扫描器 - 一键测试脚本
# 自动检查配置、运行扫描、显示结果

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色
GREEN='\e[0;32m'
YELLOW='\e[1;33m'
RED='\e[0;31m'
BLUE='\e[0;34m'
NC='\e[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  CodeQL 扫描器 - 一键测试${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# 1. 检查 .env 配置
echo -e "${YELLOW}[1/5] 检查 .env 配置...${NC}"
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ .env 文件存在${NC}"
    
    # 显示关键配置
    echo "\n📋 当前配置:"
    grep -E "^JENKINS_URL=|^JENKINS_USER=|^JENKINS_SCAN_TARGET=|^CODEQL_LANGUAGE=" .env | sed 's/^/   /'
else
    echo -e "${RED}✗ .env 文件不存在${NC}"
    echo "💡 提示：cp .env.example .env"
    exit 1
fi
echo

# 2. 检查 CodeQL
echo -e "${YELLOW}[2/5] 检查 CodeQL...${NC}"

# 加载 .env 中的 CODEQL_PATH
source .env 2>/dev/null || true
if [ -n "$CODEQL_PATH" ] && [ -d "$CODEQL_PATH" ]; then
    export PATH="$CODEQL_PATH:$PATH"
fi

if command -v codeql &> /dev/null; then
    CODEQL_VERSION=$(codeql --version | head -1)
    echo -e "${GREEN}✓ CodeQL 已安装：${CODEQL_VERSION}${NC}"
else
    echo -e "${RED}✗ CodeQL 未安装${NC}"
    echo "💡 提示：设置 CODEQL_PATH 或添加到 PATH"
    exit 1
fi
echo

# 3. 安全检查
echo -e "${YELLOW}[3/5] 安全检查...${NC}"
if [ -f "security_check.py" ]; then
    python3 security_check.py /root/devsecops-python-web > /dev/null 2>&1 && \
        echo -e "${GREEN}✓ 未发现敏感信息${NC}" || \
        echo -e "${YELLOW}⚠ 发现敏感信息，继续扫描...${NC}"
else
    echo -e "${YELLOW}⚠ 安全检查脚本不存在${NC}"
fi
echo

# 4. 运行 CodeQL 扫描
echo -e "${YELLOW}[4/5] 运行 CodeQL 扫描...${NC}"
TEST_OUTPUT="./test-$(date +%Y%m%d-%H%M%S)"

python3 scanner.py \
    /root/devsecops-python-web \
    --output "$TEST_OUTPUT" \
    --language python \
    --suite python-security-extended.qls

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 扫描完成${NC}"
else
    echo -e "${RED}✗ 扫描失败${NC}"
    exit 1
fi
echo

# 5. 显示结果
echo -e "${YELLOW}[5/5] 显示结果...${NC}"
echo -e "${BLUE}========================================${NC}"

if [ -f "${TEST_OUTPUT}/codeql-results.sarif" ]; then
    echo -e "${GREEN}✓ SARIF: ${TEST_OUTPUT}/codeql-results.sarif${NC}"
fi

if [ -f "${TEST_OUTPUT}/CODEQL_SECURITY_REPORT.md" ]; then
    echo -e "${GREEN}✓ 报告：${TEST_OUTPUT}/CODEQL_SECURITY_REPORT.md${NC}"
fi

if [ -f "${TEST_OUTPUT}/漏洞验证_Checklist.md" ]; then
    echo -e "${GREEN}✓ 清单：${TEST_OUTPUT}/漏洞验证_Checklist.md${NC}"
fi

echo -e "${BLUE}========================================${NC}"
echo

# 显示统计
if [ -f "${TEST_OUTPUT}/codeql-results.sarif" ]; then
    echo -e "${YELLOW}📊 漏洞统计:${NC}"
    python3 << EOF
import json
with open('${TEST_OUTPUT}/codeql-results.sarif') as f:
    data = json.load(f)
results = data.get('runs', [{}])[0].get('results', [])
print(f"  总发现数：{len(results)}")

by_level = {}
for r in results:
    level = r.get('level', 'none')
    by_level[level] = by_level.get(level, 0) + 1

for level, count in sorted(by_level.items()):
    emoji = {'error': '🔴 严重', 'warning': '🟠 高危', 'note': '🟡 中危', 'none': '⚪ 提示'}.get(level, '')
    print(f"  {emoji} {level}: {count}")
EOF
    echo
fi

# 显示报告摘要
if [ -f "${TEST_OUTPUT}/CODEQL_SECURITY_REPORT.md" ]; then
    echo -e "${YELLOW}📄 报告摘要:${NC}"
    head -30 "${TEST_OUTPUT}/CODEQL_SECURITY_REPORT.md"
    echo "... (查看更多：cat ${TEST_OUTPUT}/CODEQL_SECURITY_REPORT.md)"
    echo
fi

echo -e "${GREEN}✅ 测试完成！${NC}"
echo
echo -e "${YELLOW}下一步:${NC}"
echo "  1. 查看完整报告：cat ${TEST_OUTPUT}/CODEQL_SECURITY_REPORT.md"
echo "  2. 打印验证清单：cat ${TEST_OUTPUT}/漏洞验证_Checklist.md"
echo "  3. 配置 Jenkins: 查看 JENKINS_MANUAL_SETUP.md"
echo

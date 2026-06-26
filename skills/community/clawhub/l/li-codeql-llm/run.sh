#!/bin/bash
# CodeQL + LLM 扫描器 - 快速启动脚本
# CodeQL + LLM Scanner - Quick Launch Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色 / Colors
RED='\e[0;31m'
GREEN='\e[0;32m'
YELLOW='\e[1;33m'
BLUE='\e[0;34m'
NC='\e[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  CodeQL + LLM 融合扫描器${NC}"
echo -e "${BLUE}  CodeQL + LLM Fusion Scanner${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# 加载 .env 配置 / Load .env configuration
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ 加载配置文件 / Loading .env configuration${NC}"
    set -a
    source .env
    set +a
else
    echo -e "${YELLOW}⚠ 未找到 .env 文件，使用默认配置${NC}"
    echo -e "${YELLOW}⚠ .env file not found, using defaults${NC}"
    echo -e "${BLUE}💡 提示 / Tip: cp .env.example .env${NC}"
    echo
    
    # 设置默认值 / Set defaults
    export CODEQL_PATH="${CODEQL_PATH:-/opt/codeql/codeql}"
    export CODEQL_LANGUAGE="${CODEQL_LANGUAGE:-python}"
    export CODEQL_SUITE="${CODEQL_SUITE:-python-security-extended.qls}"
    export OUTPUT_DIR="${OUTPUT_DIR:-./codeql-scan-output}"
    export SECURITY_CHECK_BEFORE_SCAN="${SECURITY_CHECK_BEFORE_SCAN:-true}"
fi

# 添加 CodeQL 到 PATH
if [ -n "$CODEQL_PATH" ] && [ -d "$CODEQL_PATH" ]; then
    export PATH="$CODEQL_PATH:$PATH"
fi

# 检查 CodeQL
echo -e "${YELLOW}[1/6] 检查 CodeQL 安装 / Checking CodeQL...${NC}"
if command -v codeql &> /dev/null; then
    CODEQL_VERSION=$(codeql --version | head -1)
    echo -e "${GREEN}✓ CodeQL 已安装 / Installed: ${CODEQL_VERSION}${NC}"
else
    echo -e "${RED}✗ CodeQL 未安装 / Not installed${NC}"
    echo
    echo "请安装 CodeQL / Please install CodeQL:"
    echo "1. 访问 / Visit: https://github.com/github/codeql-cli-binaries/releases"
    echo "2. 下载对应系统的版本 / Download for your system"
    echo "3. 解压并添加到 PATH / Extract and add to PATH"
    exit 1
fi
echo

# 检查 Python
echo -e "${YELLOW}[2/6] 检查 Python 环境 / Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ ${PYTHON_VERSION}${NC}"
else
    echo -e "${RED}✗ Python3 未安装 / Not installed${NC}"
    exit 1
fi
echo

# 安全检查（可选）
if [ "$SECURITY_CHECK_BEFORE_SCAN" = "true" ]; then
    echo -e "${YELLOW}[3/6] 安全检查 / Security check...${NC}"
    if [ -f "security_check.py" ]; then
        python3 security_check.py "${1:-.}" > /dev/null 2>&1 && \
            echo -e "${GREEN}✓ 未发现敏感信息 / No sensitive information found${NC}" || \
            echo -e "${YELLOW}⚠ 发现敏感信息，请谨慎处理 / Sensitive info found, handle with care${NC}"
    fi
    echo
else
    echo -e "${YELLOW}[3/6] 跳过安全检查 / Skipping security check${NC}"
    echo
fi

# 解析参数
SOURCE_DIR="${1:-.}"
OUTPUT_DIR="${2:-$OUTPUT_DIR}"

echo -e "${YELLOW}[4/6] 准备扫描目录 / Preparing scan directory: ${SOURCE_DIR}${NC}"
if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "${RED}✗ 目录不存在 / Directory does not exist: ${SOURCE_DIR}${NC}"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
echo -e "${GREEN}✓ 输出目录 / Output directory: ${OUTPUT_DIR}${NC}"
echo

# 运行扫描器
echo -e "${YELLOW}[5/6] 运行 CodeQL 扫描 / Running CodeQL scan...${NC}"
python3 scanner.py \
    "$SOURCE_DIR" \
    --output "$OUTPUT_DIR" \
    --language "$CODEQL_LANGUAGE" \
    --suite "$CODEQL_SUITE"

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${RED}✗ 扫描失败 / Scan failed${NC}"
    exit $EXIT_CODE
fi

echo

# 显示结果
echo -e "${YELLOW}[6/6] 扫描结果 / Scan results${NC}"
echo -e "${BLUE}========================================${NC}"

if [ -f "${OUTPUT_DIR}/codeql-results.sarif" ] && [ "$GENERATE_SARIF" = "true" ]; then
    echo -e "${GREEN}✓ SARIF 结果 / SARIF: ${OUTPUT_DIR}/codeql-results.sarif${NC}"
fi

if [ -f "${OUTPUT_DIR}/CODEQL_SECURITY_REPORT.md" ] && [ "$GENERATE_MARKDOWN" = "true" ]; then
    echo -e "${GREEN}✓ 安全报告 / Report: ${OUTPUT_DIR}/CODEQL_SECURITY_REPORT.md${NC}"
fi

if [ -f "${OUTPUT_DIR}/漏洞验证_Checklist.md" ] && [ "$GENERATE_CHECKLIST" = "true" ]; then
    echo -e "${GREEN}✓ 验证清单 / Checklist: ${OUTPUT_DIR}/漏洞验证_Checklist.md${NC}"
fi

echo -e "${BLUE}========================================${NC}"
echo

# 显示统计
if [ -f "${OUTPUT_DIR}/codeql-results.sarif" ]; then
    echo -e "${YELLOW}📊 漏洞统计 / Vulnerability Statistics:${NC}"
    python3 << EOF
import json
with open('${OUTPUT_DIR}/codeql-results.sarif') as f:
    data = json.load(f)
results = data.get('runs', [{}])[0].get('results', [])
print(f"  总发现数 / Total: {len(results)}")

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

# Jenkins 集成
if [ "$JENKINS_UPLOAD_SARIF" = "true" ] && [ -n "$JENKINS_URL" ]; then
    echo -e "${YELLOW}🏢 上传到 Jenkins / Uploading to Jenkins...${NC}"
    if [ -f "jenkins_integration.py" ]; then
        python3 -c "
import sys
sys.path.insert(0, '.')
from jenkins_integration import create_jenkins_client_from_config
from config_loader import get_config

config = get_config()
client = create_jenkins_client_from_config(config)

if client:
    job_name = config.get('JENKINS_JOB_NAME', 'codeql-security-scan')
    sarif_file = '${OUTPUT_DIR}/codeql-results.sarif'
    
    if client.upload_sarif(job_name, sarif_file):
        print('✅ SARIF 已上传到 Jenkins / SARIF uploaded to Jenkins')
    else:
        print('⚠️  上传失败 / Upload failed')
"
    fi
    echo
fi

echo -e "${GREEN}✅ 扫描完成！/ Scan complete!${NC}"
echo
echo -e "${YELLOW}下一步 / Next steps:${NC}"
echo "  1. 查看报告 / View report: cat ${OUTPUT_DIR}/CODEQL_SECURITY_REPORT.md"
echo "  2. 打印清单 / Print checklist: cat ${OUTPUT_DIR}/漏洞验证_Checklist.md"
echo "  3. 发送给 LLM 分析 / Send to LLM: 将结果发送到对话中"
echo "  4. Jenkins 查看 / View in Jenkins: ${JENKINS_URL:-http://localhost:8080}"
echo

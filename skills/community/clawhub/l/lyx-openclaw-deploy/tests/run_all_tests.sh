#!/bin/bash
# OpenClaw Deploy 测试套件
# 运行所有测试

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "╔════════════════════════════════════════╗"
echo "║   OpenClaw Deploy 自动化测试套件      ║"
echo "╚════════════════════════════════════════╝"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 检查依赖
check_deps() {
  local missing=0

  for dep in bash grep; do
    if ! command -v "$dep" >/dev/null 2>&1; then
      echo -e "${RED}缺少依赖: $dep${NC}"
      missing=1
    fi
  done

  if [ $missing -eq 1 ]; then
    exit 1
  fi
}

# 运行单个测试文件
run_test_file() {
  local test_file="$1"
  local test_name=$(basename "$(dirname "$test_file")")

  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BLUE}模块: $test_name${NC}"
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

  if bash "$test_file"; then
    echo -e "${GREEN}✓ $test_name 测试通过${NC}"
    return 0
  else
    echo -e "${RED}✗ $test_name 测试失败${NC}"
    return 1
  fi
}

# 主函数
main() {
  check_deps

  local total_tests=0
  local passed_tests=0
  local failed_tests=0
  local failed_modules=""

  # 查找所有测试文件
  for test_file in "$SCRIPT_DIR"/**/test_*.sh; do
    if [ -f "$test_file" ]; then
      total_tests=$((total_tests + 1))

      if run_test_file "$test_file"; then
        passed_tests=$((passed_tests + 1))
      else
        failed_tests=$((failed_tests + 1))
        failed_modules="$failed_modules\n  - $(basename "$(dirname "$test_file")")"
      fi
      echo ""
    fi
  done

  # 打印汇总
  echo "╔════════════════════════════════════════╗"
  echo "║            测试汇总                     ║"
  echo "╚════════════════════════════════════════╝"
  echo ""
  echo -e "模块总数: ${BLUE}$total_tests${NC}"
  echo -e "通过:     ${GREEN}$passed_tests${NC}"
  echo -e "失败:     ${RED}$failed_tests${NC}"
  echo ""

  if [ $failed_tests -gt 0 ]; then
    echo -e "${RED}失败的模块:${NC}"
    echo -e "$failed_modules"
    echo ""
    exit 1
  else
    echo -e "${GREEN}✅ 全部测试通过!${NC}"
    exit 0
  fi
}

main "$@"

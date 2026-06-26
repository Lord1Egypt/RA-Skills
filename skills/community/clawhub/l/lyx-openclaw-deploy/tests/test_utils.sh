#!/bin/bash
# 测试工具函数库

set -euo pipefail

# 测试框架配置
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/.." && pwd)"
SCRIPT_DIR="$PROJECT_ROOT/scripts/deploy"

# 测试输出\033[0颜色
RED=';31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 测试统计
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0
CURRENT_TEST=""

# 测试目录（每个测试用例独立）
TEST_TMP_DIR=""

setup_test() {
  TEST_TMP_DIR=$(mktemp -d)
  CURRENT_TEST="$1"
  ((TESTS_RUN++))
  echo -e "${BLUE}[SETUP]${NC} $CURRENT_TEST"
}

teardown_test() {
  if [ -n "$TEST_TMP_DIR" ] && [ -d "$TEST_TMP_DIR" ]; then
    rm -rf "$TEST_TMP_DIR"
  fi
}

assert_pass() {
  local msg="$1"
  ((TESTS_PASSED++))
  echo -e "  ${GREEN}✓${NC} $msg"
}

assert_fail() {
  local msg="$1"
  ((TESTS_FAILED++))
  echo -e "  ${RED}✗${NC} $msg"
}

assert_eq() {
  local expected="$1"
  local actual="$2"
  local msg="${3:-value mismatch}"

  if [ "$expected" = "$actual" ]; then
    assert_pass "$msg"
    return 0
  else
    assert_fail "$msg (expected: '$expected', got: '$actual')"
    return 1
  fi
}

assert_file_exists() {
  local path="$1"
  local msg="${2:-file should exist}"

  if [ -e "$path" ]; then
    assert_pass "$msg"
    return 0
  else
    assert_fail "$msg (file not found: $path)"
    return 1
  fi
}

assert_file_not_exists() {
  local path="$1"
  local msg="${2:-file should not exist}"

  if [ ! -e "$path" ]; then
    assert_pass "$msg"
    return 0
  else
    assert_fail "$msg (file should not exist: $path)"
    return 1
  fi
}

assert_dir_exists() {
  local path="$1"
  local msg="${2:-directory should exist}"

  if [ -d "$path" ]; then
    assert_pass "$msg"
    return 0
  else
    assert_fail "$msg (dir not found: $path)"
    return 1
  fi
}

assert_contains() {
  local haystack="$1"
  local needle="$2"
  local msg="${3:-should contain substring}"

  if echo "$haystack" | grep -q "$needle"; then
    assert_pass "$msg"
    return 0
  else
    assert_fail "$msg (expected to find: '$needle')"
    return 1
  fi
}

assert_cmd_success() {
  local cmd="$1"
  local msg="${2:-command should succeed}"

  if eval "$cmd" >/dev/null 2>&1; then
    assert_pass "$msg"
    return 0
  else
    assert_fail "$msg (command failed: $cmd)"
    return 1
  fi
}

assert_cmd_failure() {
  local cmd="$1"
  local msg="${2:-command should fail}"

  if ! eval "$cmd" >/dev/null 2>&1; then
    assert_pass "$msg"
    return 0
  else
    assert_fail "$msg (command should have failed: $cmd)"
    return 1
  fi
}

print_summary() {
  echo ""
  echo "========================================"
  echo -e "${BLUE}测试汇总${NC}"
  echo "========================================"
  echo -e "运行: ${BLUE}$TESTS_RUN${NC}"
  echo -e "通过: ${GREEN}$TESTS_PASSED${NC}"
  echo -e "失败: ${RED}$TESTS_FAILED${NC}"
  echo "========================================"

  if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}❌ 部分测试失败${NC}"
    return 1
  else
    echo -e "${GREEN}✅ 全部测试通过${NC}"
    return 0
  fi
}

# 创建测试目录结构
create_test_fixtures() {
  local base="$1"

  mkdir -p "$base/source/config"
  mkdir -p "$base/source/skills"
  mkdir -p "$base/source/docker"
  mkdir -p "$base/target/config"
  mkdir -p "$base/target/skills"

  # 创建测试文件
  echo "test-config" > "$base/source/config/test.conf"
  echo "test-skill" > "$base/source/skills/test.md"
  echo "test-docker" > "$base/source/docker/Dockerfile"
}

# 模拟 SSH 命令（用于远程测试）
mock_ssh() {
  local mock_script="$TEST_TMP_DIR/mock_ssh"
  cat > "$mock_script" <<'MOCK'
#!/bin/bash
# 模拟 SSH 执行远程命令
# 忽略实际连接，只返回预设的输出
echo "🖥️  系统: ubuntu"
echo "✅ Docker 已安装"
echo "✅ docker-compose 可用"
echo "✅ tar 已安装"
echo "✅ curl 已安装"
echo "✅ 环境检测完成"
MOCK
  chmod +x "$mock_script"
}

export -f setup_test teardown_test
export -f assert_pass assert_fail
export -f assert_eq assert_file_exists assert_file_not_exists
export -f assert_dir_exists assert_contains
export -f assert_cmd_success assert_cmd_failure
export -f create_test_fixtures mock_ssh

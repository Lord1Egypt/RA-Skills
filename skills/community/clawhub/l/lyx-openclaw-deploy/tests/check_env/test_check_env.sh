#!/bin/bash
# 环境检测模块测试用例
# 测试目标: scripts/deploy/check_env.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../test_utils.sh"

CHECK_ENV="$PROJECT_ROOT/scripts/deploy/check_env.sh"

echo "========================================"
echo "环境检测模块测试"
echo "========================================"
echo ""

# ============================================
# 测试用例 1: 本地环境检测 - 正常执行
# ============================================
test_local_check_basic() {
  setup_test "本地环境检测 - 正常执行"

  output=$("$CHECK_ENV" 2>&1)

  if echo "$output" | grep -q "系统:"; then
    assert_pass "输出包含系统信息"
  else
    assert_fail "未输出系统信息"
  fi

  if echo "$output" | grep -q "环境检测完成"; then
    assert_pass "检测完成"
  else
    assert_fail "检测未正常完成"
  fi

  teardown_test
}

# ============================================
# 测试用例 2: 本地环境检测 - Docker 检测
# ============================================
test_local_check_docker() {
  setup_test "本地环境检测 - Docker 检测"

  output=$("$CHECK_ENV" 2>&1)

  # 检查是否有 Docker 相关输出
  if echo "$output" | grep -qE "(Docker|docker)"; then
    assert_pass "Docker 检测正常"
  else
    assert_fail "Docker 检测缺失"
  fi

  teardown_test
}

# ============================================
# 测试用例 3: 本地环境检测 - 依赖检测
# ============================================
test_local_check_deps() {
  setup_test "本地环境检测 - 依赖工具检测"

  output=$("$CHECK_ENV" 2>&1)

  # 至少应该检测 tar 或 curl
  if echo "$output" | grep -qE "(tar|curl)"; then
    assert_pass "依赖工具检测正常"
  else
    assert_fail "依赖工具检测缺失"
  fi

  teardown_test
}

# ============================================
# 测试用例 4: 帮助信息
# ============================================
test_help_flag() {
  setup_test "-h/--help 参数"

  if "$CHECK_ENV" -h 2>&1 | grep -q "Usage"; then
    assert_pass "-h 显示帮助信息"
  else
    assert_fail "-h 未显示帮助"
  fi

  if "$CHECK_ENV" --help 2>&1 | grep -q "Usage"; then
    assert_pass "--help 显示帮助信息"
  else
    assert_fail "--help 未显示帮助"
  fi

  teardown_test
}

# ============================================
# 测试用例 5: 缺少远程主机参数
# ============================================
test_remote_missing_params() {
  setup_test "远程检测 - 缺少参数检测"

  # 只有 --host 没有 --user
  output=$("$CHECK_ENV" --host "192.168.1.1" 2>&1 || true)
  if echo "$output" | grep -qE "(缺少|host|user)"; then
    assert_pass "缺少 --user 时报错"
  else
    assert_fail "未检测到缺少 --user"
  fi

  teardown_test
}

# ============================================
# 测试用例 6: 远程检测 - 使用密钥
# ============================================
test_remote_with_key() {
  setup_test "远程检测 - 密钥认证"

  local key_file="$TEST_TMP_DIR/test_key"
  touch "$key_file"

  # 由于真实的SSH会挂起，我们使用 timeout
  output=$(timeout 2 bash "$CHECK_ENV" --host "192.168.1.1" --user "test" --key "$key_file" --port 22 2>&1 || true)
  
  if ! echo "$output" | grep -q "未知参数"; then
    assert_pass "密钥参数被正确解析"
  else
    assert_fail "密钥参数解析错误"
  fi

  teardown_test
}

# ============================================
# 测试用例 7: 远程检测 - 端口参数
# ============================================
test_remote_custom_port() {
  setup_test "远程检测 - 自定义端口"

  local key_file="$TEST_TMP_DIR/test_key"
  touch "$key_file"

  # 由于真实的SSH会挂起，我们使用 timeout
  output=$(timeout 2 bash "$CHECK_ENV" --host "192.168.1.1" --user "test" --key "$key_file" --port 2222 2>&1 || true)

  if ! echo "$output" | grep -q "未知参数"; then
    assert_pass "端口参数被正确解析"
  else
    assert_fail "端口参数解析错误"
  fi

  teardown_test
}

# ============================================
# 测试用例 8: 远程检测 - sshpass 需求
# ============================================
test_remote_password_requires_sshpass() {
  setup_test "远程检测 - 密码模式需要 sshpass"

  # 临时移除 sshpass 以测试
  local had_sshpass=0
  if command -v sshpass >/dev/null 2>&1; then
    had_sshpass=1
    # 临时移动 sshpass
    command -v sshpass | xargs -I{} mv {} {}.bak
  fi

  output=$("$CHECK_ENV" --host "192.168.1.1" --user "test" --password "test123" 2>&1 || true)

  if echo "$output" | grep -q "sshpass"; then
    assert_pass "缺少 sshpass 时报错"
  else
    assert_fail "未检测到 sshpass 缺失"
  fi

  # 恢复 sshpass
  if [ $had_sshpass -eq 1 ]; then
    command -v sshpass.bak | xargs -I{} mv {} {}
  fi

  teardown_test
}

# ============================================
# 测试用例 9: 输出格式检查
# ============================================
test_output_format() {
  setup_test "输出格式检查"

  output=$("$CHECK_ENV" 2>&1)

  # 检查是否有 emoji 或特殊字符（ANSI 颜色码）
  if echo "$output" | grep -q $'\033'; then
    assert_pass "输出包含 ANSI 颜色码"
  else
    assert_fail "输出缺少格式化"
  fi

  teardown_test
}

# ============================================
# 测试用例 10: 异常参数处理
# ============================================
test_unknown_args() {
  setup_test "未知参数处理"

  output=$("$CHECK_ENV" --unknown-arg 2>&1 || true)
  if echo "$output" | grep -qE "(未知|Unknown)"; then
    assert_pass "未知参数时报错"
  else
    assert_fail "未知参数未报错"
  fi

  teardown_test
}

# ============================================
# 测试用例 11: 无参数执行
# ============================================
test_no_args() {
  setup_test "无参数执行"

  output=$("$CHECK_ENV" 2>&1)

  if echo "$output" | grep -q "系统:"; then
    assert_pass "无参数时执行本地检测"
  else
    assert_fail "无参数时行为异常"
  fi

  teardown_test
}

# ============================================
# 运行所有测试
# ============================================
main() {
  test_local_check_basic
  test_local_check_docker
  test_local_check_deps
  test_help_flag
  test_remote_missing_params
  test_remote_with_key
  test_remote_custom_port
  test_remote_password_requires_sshpass
  test_output_format
  test_unknown_args
  test_no_args

  print_summary
}

main "$@"

#!/bin/bash
# 打包模块测试

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TEST_TMP_DIR=""
TEST_OPENCLAW_DIR=""

cleanup() {
  if [ -n "$TEST_TMP_DIR" ] && [ -d "$TEST_TMP_DIR" ]; then
    rm -rf "$TEST_TMP_DIR"
  fi
  if [ -n "$TEST_OPENCLAW_DIR" ] && [ -d "$TEST_OPENCLAW_DIR" ]; then
    rm -rf "$TEST_OPENCLAW_DIR"
  fi
}
trap cleanup EXIT

# 模拟 OpenClaw 配置目录
setup_mock_openclaw() {
  TEST_OPENCLAW_DIR=$(mktemp -d)
  mkdir -p "$TEST_OPENCLAW_DIR/workspace/memory"
  mkdir -p "$TEST_OPENCLAW_DIR/workspace/skills"

  # 创建模拟配置
  cat > "$TEST_OPENCLAW_DIR/openclaw.json" << 'EOF'
{
  "channels": [
    {
      "id": "test-channel",
      "name": "Test Channel",
      "api_key": "sk-secret-key-12345",
      "model": "claude-3-opus"
    }
  ],
  "settings": {
    "token": "user-token-abc",
    "password": "secret123"
  }
}
EOF

  # 创建工作区文件
  echo "# SOUL" > "$TEST_OPENCLAW_DIR/workspace/SOUL.md"
  echo "# IDENTITY" > "$TEST_OPENCLAW_DIR/workspace/IDENTITY.md"
  echo "# USER" > "$TEST_OPENCLAW_DIR/workspace/USER.md"

  # 创建 skills
  echo "# Custom Skill" > "$TEST_OPENCLAW_DIR/workspace/skills/custom.sh"
}

# 测试参数解析
test_args() {
  echo -e "${BLUE}[SETUP]${NC} 参数解析 - 输出文件"

  local output
  output=$(HOME="$TEST_OPENCLAW_DIR" "$PROJECT_ROOT/build/base/base_builder.sh" --output /tmp/test-output.tar.gz 2>&1 || true)

  if echo "$output" | grep -q "打包 OpenClaw"; then
    echo -e "  ${GREEN}✓${NC} --output 参数被正确解析"
  else
    echo -e "  ${RED}✗${NC} --output 参数解析失败"
    return 1
  fi

  # 检查自动生成的文件名
  if [ -f "/tmp/test-output.tar.gz" ]; then
    echo -e "  ${GREEN}✓${NC} 输出文件已生成"
    rm -f /tmp/test-output.tar.gz /tmp/test-output.tar.gz.sha256
  else
    echo -e "  ${RED}✗${NC} 输出文件未生成"
    return 1
  fi
}

# 测试帮助信息
test_help() {
  echo -e "${BLUE}[SETUP]${NC} 帮助信息 - -h/--help"

  local output
  output=$("$PROJECT_ROOT/build/base/base_builder.sh" -h 2>&1 || true)

  if echo "$output" | grep -q "用法"; then
    echo -e "  ${GREEN}✓${NC} -h 显示帮助信息"
  else
    echo -e "  ${RED}✗${NC} -h 帮助信息显示失败"
    return 1
  fi

  output=$("$PROJECT_ROOT/build/base/base_builder.sh" --help 2>&1 || true)
  if echo "$output" | grep -q "用法"; then
    echo -e "  ${GREEN}✓${NC} --help 显示帮助信息"
  else
    echo -e "  ${RED}✗${NC} --help 帮助信息显示失败"
    return 1
  fi
}

# 测试敏感信息移除
test_sensitive_removal() {
  echo -e "${BLUE}[SETUP]${NC} 敏感信息移除"

  # 创建带 .openclaw 子目录的配置
  local test_home=$(mktemp -d)
  mkdir -p "$test_home/.openclaw/workspace/memory"
  mkdir -p "$test_home/.openclaw/workspace/skills"

  # 创建模拟配置
  cat > "$test_home/.openclaw/openclaw.json" << 'EOF'
{
  "channels": [
    {
      "id": "test-channel",
      "name": "Test Channel",
      "api_key": "sk-secret-key-12345",
      "model": "claude-3-opus"
    }
  ],
  "settings": {
    "token": "user-token-abc",
    "password": "secret123"
  }
}
EOF

  # 创建工作区文件
  echo "# SOUL" > "$test_home/.openclaw/workspace/SOUL.md"
  echo "# IDENTITY" > "$test_home/.openclaw/workspace/IDENTITY.md"
  echo "# USER" > "$test_home/.openclaw/workspace/USER.md"

  # 创建 skills
  echo "# Custom Skill" > "$test_home/.openclaw/workspace/skills/custom.sh"

  local output_file="/tmp/test-sensitive.tar.gz"
  HOME="$test_home" "$PROJECT_ROOT/build/base/base_builder.sh" --output "$output_file" 2>&1 || true

  rm -rf "$test_home"

  if [ ! -f "$output_file" ]; then
    echo -e "  ${RED}✗${NC} 打包文件未生成"
    return 1
  fi

  # 解压检查
  local tmp_extract="/tmp/test-extract-$$"
  mkdir -p "$tmp_extract"
  tar -xzf "$output_file" -C "$tmp_extract"

  # 检查敏感信息是否被移除
  local config_content
  config_content=$(cat "$tmp_extract/config/openclaw.json")

  if echo "$config_content" | grep -q '\$REMOVED'; then
    echo -e "  ${GREEN}✓${NC} 敏感信息已被移除"
  else
    echo -e "  ${RED}✗${NC} 敏感信息未被移除"
    rm -rf "$tmp_extract" "$output_file" /tmp/test-extract-*.tar.gz.sha256
    return 1
  fi

  # 确认原始敏感信息不存在
  if echo "$config_content" | grep -q "sk-secret-key"; then
    echo -e "  ${RED}✗${NC} 原始 api_key 仍然存在"
    rm -rf "$tmp_extract" "$output_file" /tmp/test-extract-*.tar.gz.sha256
    return 1
  fi

  echo -e "  ${GREEN}✓${NC} 原始敏感信息已清除"

  rm -rf "$tmp_extract" "$output_file" /tmp/test-extract-*.tar.gz.sha256
}

# 测试元数据生成
test_metadata() {
  echo -e "${BLUE}[SETUP]${NC} 元数据生成"

  setup_mock_openclaw

  local output_file="/tmp/test-metadata.tar.gz"
  HOME="$TEST_OPENCLAW_DIR" "$PROJECT_ROOT/build/base/base_builder.sh" --output "$output_file" 2>&1 || true

  local tmp_extract="/tmp/test-meta-extract-$$"
  mkdir -p "$tmp_extract"
  tar -xzf "$output_file" -C "$tmp_extract"

  # 检查元数据文件
  if [ -f "$tmp_extract/metadata.json" ]; then
    echo -e "  ${GREEN}✓${NC} metadata.json 已生成"

    # 检查必需字段
    if grep -q '"name"' "$tmp_extract/metadata.json" && \
       grep -q '"version"' "$tmp_extract/metadata.json" && \
       grep -q '"created_at"' "$tmp_extract/metadata.json"; then
      echo -e "  ${GREEN}✓${NC} 元数据包含必需字段"
    else
      echo -e "  ${RED}✗${NC} 元数据缺少必需字段"
      rm -rf "$tmp_extract" "$output_file" /tmp/test-meta-*.tar.gz.sha256
      return 1
    fi
  else
    echo -e "  ${RED}✗${NC} metadata.json 未生成"
    rm -rf "$tmp_extract" "$output_file" /tmp/test-meta-*.tar.gz.sha256
    return 1
  fi

  rm -rf "$tmp_extract" "$output_file" /tmp/test-meta-*.tar.gz.sha256
}

# 测试 SHA256 校验
test_sha256() {
  echo -e "${BLUE}[SETUP]${NC} SHA256 校验生成"

  setup_mock_openclaw

  local output_file="/tmp/test-sha256.tar.gz"
  HOME="$TEST_OPENCLAW_DIR" "$PROJECT_ROOT/build/base/base_builder.sh" --output "$output_file" 2>&1 || true

  # 检查 SHA256 文件
  if [ -f "${output_file}.sha256" ]; then
    echo -e "  ${GREEN}✓${NC} SHA256 文件已生成"

    # 验证 SHA256 正确性
    local expected
    expected=$(awk '{print $1}' "${output_file}.sha256")
    local actual
    actual=$(sha256sum "$output_file" | awk '{print $1}' || shasum -a 256 "$output_file" | awk '{print $1}')

    if [ "$expected" = "$actual" ]; then
      echo -e "  ${GREEN}✓${NC} SHA256 校验正确"
    else
      echo -e "  ${RED}✗${NC} SHA256 校验失败"
      rm -f "$output_file" "${output_file}.sha256"
      return 1
    fi
  else
    echo -e "  ${RED}✗${NC} SHA256 文件未生成"
    rm -f "$output_file" "${output_file}.sha256"
    return 1
  fi

  rm -f "$output_file" "${output_file}.sha256"
}

# 测试必需参数
test_required_args() {
  echo -e "${BLUE}[SETUP]${NC} 必需参数检测"

  # 不带参数应该报错或显示用法
  local output
  output=$("$PROJECT_ROOT/build/base/base_builder.sh" 2>&1 || true)

  if echo "$output" | grep -q "用法\|output"; then
    echo -e "  ${GREEN}✓${NC} 缺少参数时报错"
  else
    echo -e "  ${RED}✗${NC} 缺少参数时未报错"
    return 1
  fi
}

# 主函数
main() {
  echo "========================================"
  echo "打包模块测试"
  echo "========================================"
  echo ""

  setup_mock_openclaw
  TEST_TMP_DIR=$(mktemp -d)

  local passed=0
  local failed=0

  # 运行测试
  for test_func in test_args test_help test_sensitive_removal test_metadata test_sha256 test_required_args; do
    if $test_func; then
      passed=$((passed + 1))
    else
      failed=$((failed + 1))
    fi
    echo ""
  done

  echo "========================================"
  echo "测试汇总"
  echo "========================================"
  echo "运行: ${BLUE}$((passed + failed))${NC}"
  echo "通过: ${GREEN}$passed${NC}"
  echo "失败: ${RED}$failed${NC}"
  echo ""

  if [ $failed -gt 0 ]; then
    echo -e "${RED}✗ 测试失败${NC}"
    exit 1
  else
    echo -e "${GREEN}✅ 全部测试通过${NC}"
    exit 0
  fi
}

main "$@"

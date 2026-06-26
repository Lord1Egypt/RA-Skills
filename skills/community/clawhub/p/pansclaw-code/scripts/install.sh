#!/bin/bash
# 一键构建并测试 Claw

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAW_ROOT="/Users/dashi/.openclaw-pansclaw/claw-code-main"
RUST_DIR="$CLAW_ROOT/rust"

echo "====================================="
echo "  Claw CLI 一键构建脚本"
echo "====================================="
echo ""

# 步骤 1: 构建
echo "📦 步骤 1/2: 构建二进制..."
cd "$RUST_DIR"
cargo build -p rusty-claude-cli --release

# 步骤 2: 创建符号链接
echo "🔗 步骤 2/2: 更新符号链接..."
mkdir -p "$HOME/.local/bin"
rm -f "$HOME/.local/bin/claw"
ln -sf "$RUST_DIR/target/release/claw" "$HOME/.local/bin/claw"

# 验证
echo ""
echo "✅ 构建成功！"
echo ""
echo "验证安装:"
ls -la "$HOME/.local/bin/claw"
echo ""
echo "运行以下命令开始使用:"
echo "  ~/.local/bin/claw /doctor"

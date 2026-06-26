#!/bin/bash
# 构建 Claw CLI 二进制文件

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAW_ROOT="/Users/dashi/.openclaw-pansclaw/claw-code-main"
RUST_DIR="$CLAW_ROOT/rust"
BIN_DIR="$HOME/.local/bin"

echo "🔨 开始构建 Claw CLI..."

cd "$RUST_DIR"

# 检查 Rust 工具链
if ! command -v cargo &> /dev/null; then
    echo "❌ Rust 工具链未安装"
    echo "   安装: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi

# 构建
echo "📦 编译中..."
cargo build -p rusty-claude-cli --release

# 创建 bin 目录
mkdir -p "$BIN_DIR"

# 链接或复制二进制
if [ -L "$BIN_DIR/claw" ]; then
    rm "$BIN_DIR/claw"
fi

ln -sf "$RUST_DIR/target/release/claw" "$BIN_DIR/claw"

echo "✅ 构建完成！"
echo "   二进制: $BIN_DIR/claw"
echo ""
echo "运行 'claw /doctor' 进行健康检查"

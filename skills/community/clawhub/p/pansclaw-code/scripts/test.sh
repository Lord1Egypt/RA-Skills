#!/bin/bash
# 运行测试

set -e

CLAW_ROOT="/Users/dashi/.openclaw-pansclaw/claw-code-main"
RUST_DIR="$CLAW_ROOT/rust"

echo "🧪 运行 Claw 测试套件..."

cd "$RUST_DIR"

# 格式检查
echo "📝 检查代码格式..."
cargo fmt --check

# Lint 检查
echo "🔎 运行 clippy..."
cargo clippy --workspace --all-targets -- -D warnings

# 运行测试
echo "✅ 执行单元测试..."
cargo test --workspace

echo ""
echo "🎉 所有检查通过！"

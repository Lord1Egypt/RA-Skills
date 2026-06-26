#!/bin/bash
# 示例食谱 1：从零到一做品牌 KV
# 配合 RECIPES.md 食谱 1。运行前确保已配置 ANTHROPIC_API_KEY + OPENAI_API_KEY。
#
# 这个脚本演示完整工作流：
#   导入 brand_kit → polish → variants 出 4 个候选 → image_review 排名 → 闭环迭代到 7.5 分

set -e

SCRIPTS_DIR="$(dirname "$0")/../scripts"
EXAMPLES_DIR="$(dirname "$0")"

echo "━━━ Step 1: 导入示例 brand_kit ━━━"
cat "$EXAMPLES_DIR/brand_kit-song_tea.json" | python3 "$SCRIPTS_DIR/brand_kit.py" --import

echo
echo "━━━ Step 2: Claude 智能润色（建议预设） ━━━"
python3 "$SCRIPTS_DIR/claude_polish.py" "宋韵茶饮品牌主视觉，一杯热茶，远山轮廓" --suggest

echo
echo "━━━ Step 3: 出 4 个 A/B 变体（同 seed 不同 mood/composition） ━━━"
python3 "$SCRIPTS_DIR/enhance_prompt.py" \
    "宋韵茶饮品牌主视觉，一杯热茶，远山轮廓" \
    -p "汉服写真+水墨" \
    --brand-kit song_tea \
    --variants 4 \
    -j > /tmp/variants.json
echo "已写入 /tmp/variants.json，含 4 个变体的完整 prompt"

echo
echo "━━━ Step 4（需要 ANTHROPIC + 后端）: 闭环自动迭代到 7.5 分 ━━━"
echo "下一步真正出图（需要 OPENAI_API_KEY）："
cat <<EOF
python3 $SCRIPTS_DIR/auto_iterate.py \\
    "宋韵茶饮品牌主视觉，一杯热茶，远山轮廓" \\
    -p "汉服写真+水墨" \\
    --backend dalle \\
    --target 7.5 \\
    --max-rounds 3
EOF

echo
echo "━━━ Step 5: 把最终 recipe 写入 Obsidian vault ━━━"
echo "如果有 OBSIDIAN_VAULT 或 ~/knowledge/huo15:"
cat <<EOF
python3 $SCRIPTS_DIR/enhance_prompt.py \\
    "宋韵茶饮品牌主视觉，一杯热茶，远山轮廓" \\
    -p "汉服写真+水墨" \\
    --brand-kit song_tea \\
    --obsidian
EOF

echo
echo "✅ 食谱 1 演示完成。详见 RECIPES.md。"

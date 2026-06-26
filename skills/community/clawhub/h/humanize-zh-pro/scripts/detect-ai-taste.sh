#!/usr/bin/env bash
# detect-ai-taste.sh — AI味深度检测器
# 用法: ./detect-ai-taste.sh input.txt

set -euo pipefail

INPUT="${1:-}"
if [[ -z "$INPUT" ]]; then
  echo "用法: ./detect-ai-taste.sh <文件路径>"
  exit 1
fi

if [[ ! -f "$INPUT" ]]; then
  echo "❌ 文件不存在: $INPUT"
  exit 1
fi

TEXT=$(cat "$INPUT")
TOTAL_CHARS=$(echo "$TEXT" | wc -m | tr -d ' ')
PARA_COUNT=$(echo "$TEXT" | awk 'NF{print}' | wc -l | tr -d ' ')

echo "========================================="
echo "  🔍 AI味深度检测报告"
echo "========================================="
echo "  文件: $INPUT"
echo "  字数: $TOTAL_CHARS"
echo "  段落: $PARA_COUNT"
echo "========================================="
echo ""

# === 维度1: 结构模式 ===
echo "📐 维度1: 结构模式"
SCORE1=0

echo "$TEXT" | grep -qE '(首先.*其次|第一.*第二.*第三|一方面.*另一方面)' && { echo "  ⚠️ 使用了序列化结构（首先/其次、第一/第二）"; ((SCORE1+=20)); } || echo "  ✅ 未使用明显的序列化结构"
echo "$TEXT" | grep -qE '综上所述|总而言之|总的来看' && { echo "  ⚠️ 使用了'综上所述'等AI总结语"; ((SCORE1+=15)); } || echo "  ✅ 未使用AI总结语"
echo "$TEXT" | grep -qE '在当今|随着.*的发展|众所周知' && { echo "  ⚠️ 使用了'在当今/随着发展/众所周知'等AI开头"; ((SCORE1+=15)); } || echo "  ✅ 未使用AI万能开头"

echo "  结构得分: $SCORE1/50 (越高越AI味)"
echo ""

# === 维度2: 语句多样性 ===
echo "📝 维度2: 语句多样性"
SCORE2=0

# 句子长度标准差
SENTENCES=$(echo "$TEXT" | sed 's/[^。！？；]/ /g' | wc -w | tr -d ' ')
if [[ $SENTENCES -gt 0 ]]; then
  AVG_SENT_LEN=$((TOTAL_CHARS / SENTENCES))
  if [[ $AVG_SENT_LEN -gt 20 ]] && [[ $AVG_SENT_LEN -lt 50 ]]; then
    echo "  ⚠️ 句子长度偏均匀（${AVG_SENT_LEN}字/句），缺乏长短变化"
    ((SCORE2+=20))
  else
    echo "  ✅ 句子长度有变化"
  fi
fi

# 标点多样性
PUNCT_TYPES=$(echo "$TEXT" | grep -oE '[。！？…～、：；""（）]' | sort -u | wc -l | tr -d ' ')
if [[ $PUNCT_TYPES -lt 5 ]]; then
  echo "  ⚠️ 标点类型偏少（${PUNCT_TYPES}种），缺少情感标点"
  ((SCORE2+=15))
else
  echo "  ✅ 标点使用多样"
fi

# 段落长度均匀性
echo "  语句得分: $SCORE2/35"
echo ""

# === 维度3: 人性化指标 ===
echo "💬 维度3: 人性化指标"
SCORE3=0

echo "$TEXT" | grep -qE '(吧|嘛|啦|哈|呀|呢|咯|哎|嗯|啊|哦)' || { echo "  ⚠️ 缺少语气词"; ((SCORE3+=15)); }
echo "$TEXT" | grep -qE '(我觉得|我个人|说实话|老实说|讲道理)' || { echo "  ⚠️ 缺少个人观点表达"; ((SCORE3+=15)); }
echo "$TEXT" | grep -qE '(真的|特别|太.*了|挺|满|好.*啊)' || { echo "  ⚠️ 缺少情感强化词"; ((SCORE3+=10)); }
echo "$TEXT" | grep -qE '(我之前|我上次|我遇到|有一次|记得)' || { echo "  ⚠️ 缺少个人经历引用"; ((SCORE3+=10)); }
echo "$TEXT" | grep -qE '(😀|😂|🔥|💡|✅|❤️|👆|👇|💕|🎉|📝|🔍|⚡|💰|🎯|📊|🎬|🏆|🤔|👀|💪|🙏|✨|🌟|💯|📌|📍|🎵|🍀|🆕|👋)' || { echo "  ⚠️ 未使用emoji"; ((SCORE3+=5)); }

echo "  人性得分: $SCORE3/55"
echo ""

# === 维度4: 连接词模式 ===
echo "🔗 维度4: 连接词"
SCORE4=0

echo "$TEXT" | grep -qE '此外|然而|因此|从而|进而' && { echo "  ⚠️ 使用了AI偏好连接词（此外/然而/因此）"; ((SCORE4+=15)); } || echo "  ✅ 连接词自然"
echo "$TEXT" | grep -qE '希望本文|期待您的|通过以上|通过本文' && { echo "  ⚠️ 使用了AI客套结尾"; ((SCORE4+=15)); } || echo "  ✅ 结尾自然"

echo "  连接词得分: $SCORE4/30"
echo ""

# === 总分 ===
TOTAL=$((SCORE1 + SCORE2 + SCORE3 + SCORE4))
MAX=170
PCT=$((TOTAL * 100 / MAX))

echo "========================================="
echo "  📊 综合评分"
echo "========================================="
echo "  总分: $TOTAL / $MAX"
echo "  AI味: ${PCT}%"
echo ""

if [[ $PCT -ge 60 ]]; then
  echo "  🔴 重度AI味 — 建议全面去味处理"
elif [[ $PCT -ge 30 ]]; then
  echo "  🟡 中度AI味 — 建议针对性去味"
else
  echo "  🟢 轻度AI味 — 接近人类写作"
fi

echo ""
echo "  建议操作:"
echo "    ./humanize.sh -i $INPUT -s casual -o humanized.txt"
echo "========================================="

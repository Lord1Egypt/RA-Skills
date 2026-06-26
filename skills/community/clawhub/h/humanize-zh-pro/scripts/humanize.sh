#!/usr/bin/env bash
# humanize.sh — AI文本去味工具
# 用法: ./humanize.sh --input text.txt --style zhihu [--output result.txt]
#        echo "AI文本" | ./humanize.sh --style xiaohongshu

set -euo pipefail

STYLE="casual"
INPUT_FILE=""
OUTPUT_FILE=""
TEXT=""
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

usage() {
  cat <<EOF
📝 AI文本去味工具 (Humanize)

用法:
  ./humanize.sh --input <file> --style <style> [--output <file>]
  echo "文本" | ./humanize.sh --style <style>

可用风格:
  zhihu        — 知乎理性风（专业但不装）
  xiaohongshu  — 小红书活泼风（闺蜜聊天感）
  gongzhonghao — 公众号叙事风（娓娓道来）
  pengyouquan  — 朋友圈随性风（真实日常）
  casual       — 通用口语风（朋友聊天）[默认]

选项:
  --input, -i   输入文件路径
  --output, -o  输出文件路径（默认输出到stdout）
  --style, -s   目标风格
  --score        仅检测AI味，输出评分（0-100，越高越AI味）
  --help, -h    显示帮助

示例:
  ./humanize.sh -i draft.md -s zhihu -o ready.md
  cat ai_text.txt | ./humanize.sh -s xiaohongshu
  ./humanize.sh -i essay.txt --score
EOF
  exit 0
}

# 解析参数
SCORE_ONLY=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --input|-i) INPUT_FILE="$2"; shift 2 ;;
    --output|-o) OUTPUT_FILE="$2"; shift 2 ;;
    --style|-s) STYLE="$2"; shift 2 ;;
    --score) SCORE_ONLY=true; shift ;;
    --help|-h) usage ;;
    *) echo "未知参数: $1"; usage ;;
  esac
done

# 验证风格
TEMPLATE="$BASE_DIR/templates/${STYLE}.md"
if [[ ! -f "$TEMPLATE" ]]; then
  echo "❌ 未知风格: $STYLE"
  echo "可用: zhihu, xiaohongshu, gongzhonghao, pengyouquan, casual"
  exit 1
fi

# 读取输入
if [[ -n "$INPUT_FILE" ]]; then
  if [[ ! -f "$INPUT_FILE" ]]; then
    echo "❌ 文件不存在: $INPUT_FILE"
    exit 1
  fi
  TEXT=$(cat "$INPUT_FILE")
else
  # 从stdin读取
  if [[ -t 0 ]]; then
    echo "❌ 请提供输入文本（--input 或 管道）"
    usage
  fi
  TEXT=$(cat)
fi

if [[ -z "${TEXT// }" ]]; then
  echo "❌ 输入文本为空"
  exit 1
fi

# AI味检测
if $SCORE_ONLY; then
  AI_INDICATORS=0
  TOTAL_CHECKS=10
  
  # 检测AI特征
  echo "$TEXT" | grep -qE '(首先.*其次.*最后|第一.*第二.*第三|综上所述|此外|然而|因此|众所周知|在当今)' && ((AI_INDICATORS++)) || true
  echo "$TEXT" | grep -qE '(希望本文|期待您的|谢谢阅读|通过以上)' && ((AI_INDICATORS++)) || true
  echo "$TEXT" | grep -qE '([，。！？；：]){1}' && true  # always check
  
  # 段落长度检测（AI倾向于均匀段落）
  PARAGRAPHS=$(echo "$TEXT" | awk 'NF{print length}' | sort -n)
  if [[ -n "$PARAGRAPHS" ]]; then
    MAX_LEN=$(echo "$PARAGRAPHS" | tail -1)
    MIN_LEN=$(echo "$PARAGRAPHS" | head -1)
    if [[ $((MAX_LEN - MIN_LEN)) -lt 20 ]]; then
      ((AI_INDICATORS++))
    fi
  fi
  
  # 句子长度均匀性
  SENTENCE_LENGTHS=$(echo "$TEXT" | tr '。！？；' '\n' | awk 'NF{print length}' | sort -n)
  if [[ -n "$SENTENCE_LENGTHS" ]]; then
    S_MAX=$(echo "$SENTENCE_LENGTHS" | tail -1)
    S_MIN=$(echo "$SENTENCE_LENGTHS" | head -1)
    if [[ $((S_MAX - S_MIN)) -lt 10 ]]; then
      ((AI_INDICATORS++))
    fi
  fi
  
  # 语气词检测（人类多用语气词）
  if ! echo "$TEXT" | grep -qE '(吧|嘛|啦|哈|呀|呢|咯|哎|嗯)' ; then
    ((AI_INDICATORS++))
  fi
  
  # 个人经历/观点词检测
  if ! echo "$TEXT" | grep -qE '(我觉得|我个人|说实话|老实说|讲道理|我之前|我上次|我遇到)' ; then
    ((AI_INDICATORS++))
  fi
  
  # 情感表达检测
  if ! echo "$TEXT" | grep -qE '(真的|特别|太|挺|满|好)' ; then
    ((AI_INDICATORS++))
  fi
  
  # 标点多样性（AI倾向句号逗号）
  PUNCT_VAR=$(echo "$TEXT" | grep -oE '[。！？…～]' | sort -u | wc -l)
  if [[ $PUNCT_VAR -lt 3 ]]; then
    ((AI_INDICATORS++))
  fi
  
  # emoji使用
  if ! echo "$TEXT" | grep -qE '(😀|😂|🔥|💡|✅|❤️|👆|👇|💕|🎉|📝|🔍|⚡|💰|🎯|📊|🎬|🏆|🤔|👀|💪|🙏|✨|🌟|💯|📌|📍|🎵|🍀|🆕|👋)' ; then
    ((AI_INDICATORS++))
  fi
  
  SCORE=$((AI_INDICATORS * 100 / TOTAL_CHECKS))
  
  cat <<EOF
📊 AI味检测报告
━━━━━━━━━━━━━━━━━━━━
文本长度: $(echo "$TEXT" | wc -m | tr -d ' ') 字符
AI味评分: ${SCORE}/100
$(if [[ $SCORE -ge 70 ]]; then echo "🔴 高AI味 — 建议深度去味"; elif [[ $SCORE -ge 40 ]]; then echo "🟡 中AI味 — 建议轻度去味"; else echo "🟢 低AI味 — 接近人类写作"; fi)

检测到的AI特征:
$(echo "$TEXT" | grep -oE '(首先.*其次.*最后|第一.*第二.*第三|综上所述|此外|然而|因此|众所周知|在当今|希望本文|期待您的|谢谢阅读)' | while read -r m; do echo "  • $m"; done)
EOF
  exit 0
fi

# 构建去味提示词
PROMPT=$(cat <<PROMPT_END
你是一个中文文本润色专家。请将以下AI生成的机械化文本转换为自然的人类写作风格。

目标风格: $(head -1 "$TEMPLATE" | sed 's/^# *//')

风格参考:
$(cat "$TEMPLATE")

核心要求:
1. 打破完美结构 — 不要"第一第二第三"，用更自然的过渡
2. 长短句混搭 — 短句有力，长句娓娓
3. 加入口语化表达 — 语气词、口头禅
4. 用具体代替抽象 — 加入场景和例子
5. 加入个人色彩 — 情感、主观判断、思考过程
6. 替换AI味连接词 — "此外"→"还有"、"然而"→"但问题是"
7. 保持内容核心信息不变，只改变表达方式

原文:
$TEXT

请直接输出去味后的文本，不要加任何说明。
PROMPT_END
)

# 输出去味提示词（供AI处理）
if [[ -n "$OUTPUT_FILE" ]]; then
  echo "$PROMPT" > "$OUTPUT_FILE"
  echo "✅ 去味提示词已生成: $OUTPUT_FILE"
  echo "   风格: $STYLE"
  echo "   原始长度: $(echo "$TEXT" | wc -m | tr -d ' ') 字符"
  echo "   请将输出文件内容发送给AI进行去味处理"
else
  echo "$PROMPT"
fi

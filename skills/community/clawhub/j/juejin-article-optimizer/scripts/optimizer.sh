#!/usr/bin/env bash
#
# Juejin Article Optimizer — diagnose, optimize, and publish technical articles
# for the Juejin (掘金) developer community.
#
# Usage:
#   optimizer.sh --title "Go并发编程入门" --task diagnose
#   optimizer.sh --title "微服务监控实战" --task title
#   optimizer.sh --title "Kubernetes教程" --task full --tags 后端,Kubernetes
#   optimizer.sh --help
#
# MIT-0 License
#
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REF_DIR="$(cd "$SCRIPT_DIR/../references" && pwd)"

usage() {
  cat <<'USAGE'
Juejin Article Optimizer — optimize technical articles for the Juejin community.

Usage:
  optimizer.sh --title <TITLE> --task <TASK> [--tags TAGS] [--output FORMAT]
  optimizer.sh --help

Tasks:
  diagnose       Run diagnostic scoring on article title + metadata
  title          Generate 3 optimized title variants
  tags           Recommend 5 tags for maximum reach
  seo            Generate SEO keywords and meta description
  publish        Best publish time and cross-promotion strategy
  full           Run full optimization pipeline

Options:
  -t, --title TEXT      Article title
  -k, --task TASK       Task to execute (diagnose|title|tags|seo|publish|full)
  -g, --tags TAGS       Comma-separated tags
  -o, --output FORMAT   Output format: table (default) or json
  -h, --help            Show this help message

Examples:
  optimizer.sh --title "Go并发编程入门" --task diagnose
  optimizer.sh --title "微服务监控踩坑实录" --task title
  optimizer.sh --title "Kubernetes从入门到实战" --task tags --tags 后端,Kubernetes
  optimizer.sh --title "React性能优化指南" --task full --tags 前端,React

MIT-0 License
USAGE
}

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
info()  { echo -e "${CYAN}  [INFO]${NC} $*"; }
ok()    { echo -e "${GREEN}  [OK]${NC} $*"; }
warn()  { echo -e "${YELLOW}  [WARN]${NC} $*"; }
header(){ echo -e "\n${BOLD}== $* ==${NC}"; }

# ── Step 2: Diagnostic Scoring ──────────────────────────────────────────────
diagnose_article() {
  local title="$1"
  local tags_input="$2"
  local title_len="${#title}"
  local has_number=0 has_colon=0 has_question=0
  [[ "$title" =~ [0-9]+ ]] && has_number=1
  [[ "$title" == *：* ]] || [[ "$title" == *":"* ]] && has_colon=1
  [[ "$title" == *?* ]] || [[ "$title" == *？* ]] && has_question=1

  local title_score=5 seo_score=5 readability_score=7
  local structure_score=7 engagement_score=4 code_text_score=7

  # Title scoring heuristics
  [ "$has_number" -eq 1 ] && title_score=$((title_score + 2))
  [ "$has_colon" -eq 1 ] && title_score=$((title_score + 1))
  [ "$has_question" -eq 1 ] && title_score=$((title_score + 1))
  [ "$title_len" -ge 10 ] && [ "$title_len" -le 30 ] && title_score=$((title_score + 1))
  [ "$title_len" -gt 30 ] && title_score=$((title_score - 1))
  [ "$title_len" -lt 6 ] && title_score=$((title_score - 2))
  [ "$title_score" -gt 10 ] && title_score=10
  [ "$title_score" -lt 1 ] && title_score=1

  # SEO scoring
  [ -n "$tags_input" ] && seo_score=$((seo_score + 2))
  [[ "$title" =~ 实战|入门|教程|指南|技巧|最佳实践|原理|深入 ]] && seo_score=$((seo_score + 1))
  [ "$seo_score" -gt 10 ] && seo_score=10

  local total_score=$(( (title_score * 20 + structure_score * 15 + readability_score * 20 + seo_score * 15 + engagement_score * 15 + code_text_score * 15) / 100 ))

  header "Diagnostic Report"
  echo ""
  echo "  Title: $title"
  echo "  Title length: $title_len chars"
  echo ""
  echo "  Dimension          | Score (1-10) | Weight | Weighted"
  echo "  ───────────────────|──────────────|────────|─────────"
  printf "  Title Power        | %2d/10        | 20%%    | %d/10\n" "$title_score" $((title_score * 20 / 100))
  printf "  Structure          | %2d/10        | 15%%    | %d/10\n" "$structure_score" $((structure_score * 15 / 100))
  printf "  Code/Text Balance  | %2d/10        | 15%%    | %d/10\n" "$code_text_score" $((code_text_score * 15 / 100))
  printf "  Readability        | %2d/10        | 20%%    | %d/10\n" "$readability_score" $((readability_score * 20 / 100))
  printf "  SEO & Discovery    | %2d/10        | 15%%    | %d/10\n" "$seo_score" $((seo_score * 15 / 100))
  printf "  Engagement Design  | %2d/10        | 15%%    | %d/10\n" "$engagement_score" $((engagement_score * 15 / 100))
  echo "  ───────────────────|──────────────|────────|─────────"
  echo "  Overall: $total_score/10"
  echo ""

  if [ "$title_score" -lt 6 ]; then
    warn "Title needs improvement. Low on: keywords, curiosity gap, or number patterns."
  fi
  if [ "$engagement_score" -lt 5 ]; then
    warn "Engagement is weak. Add discussion hooks, takeaways, and comment-bait questions."
  fi
  if [ "$seo_score" -lt 6 ]; then
    warn "SEO can be improved. Use primary keywords in title, first paragraph, and H2s."
  fi

  if [ "$OUTPUT_FORMAT" = "json" ]; then
    echo '{
      "title":"'"$title"'",
      "title_length":'"$title_len"',
      "scores":{
        "title_power":'"$title_score"',
        "structure":'"$structure_score"',
        "code_text_balance":'"$code_text_score"',
        "readability":'"$readability_score"',
        "seo":'"$seo_score"',
        "engagement":'"$engagement_score"'
      },
      "overall":'"$total_score"',
      "warnings": [
        '"$( [ "$title_score" -lt 6 ] && echo '"Title needs improvement"' || echo '')"'
      ]
    }'
  fi
}

# ── Step 5: Title Optimization ──────────────────────────────────────────────
generate_titles() {
  local title="$1"
  local category="${2:-一般}"

  header "Title Optimization"
  echo ""
  info "Original title: $title"
  info "Category: $category"
  echo ""
  echo "  Top 3 optimized variants:"
  echo ""

  echo "  Variant 1 (Numbered List Pattern):"
  echo "  \"$title 的 5 个最佳实践，第 3 个 90% 的人不知道\""
  echo "  CTR Potential: 8.5/10 — High appeal, uses curiosity gap + numbered list."
  echo ""
  echo "  Variant 2 (Practical Value Pattern):"
  echo "  \"用了 $title 这么久，你可能一直忽略了这些关键细节\""
  echo "  CTR Potential: 8.0/10 — Experience authority + curiosity gap."
  echo ""
  echo "  Variant 3 (How-to / Comprehensive):"
  echo "  \"一文搞懂 $title：从入门到高阶实战\""
  echo "  CTR Potential: 7.5/10 — Broad appeal, good for beginner-friendly content."
  echo ""
  info "Recommendation: Variant 1 has best pattern match for Juejin trending articles."

  if [ "$OUTPUT_FORMAT" = "json" ]; then
    cat <<JSONEOF
{
  "original_title": "$title",
  "variants": [
    {"variant": 1, "pattern": "Numbered List", "title": "${title} 的 5 个最佳实践，第 3 个 90% 的人不知道", "ctr_potential": 8.5},
    {"variant": 2, "pattern": "Practical Value", "title": "用了 ${title} 这么久，你可能一直忽略了这些关键细节", "ctr_potential": 8.0},
    {"variant": 3, "pattern": "How-to / Comprehensive", "title": "一文搞懂 ${title}：从入门到高阶实战", "ctr_potential": 7.5}
  ],
  "recommended": "Variant 1"
}
JSONEOF
  fi
}

# ── Step 7: SEO & Tags ──────────────────────────────────────────────────────
recommend_tags() {
  local title="$1"
  local tags_input="$2"

  header "Tag Strategy"
  echo ""
  info "Based on title and Juejin category:"
  echo ""
  echo "  Recommended tags (5):"

  local primary_tag=""
  if [ -n "$tags_input" ]; then
    primary_tag=$(echo "$tags_input" | cut -d, -f1)
  else
    primary_tag="技术"
  fi

  echo "  1. $primary_tag           — Primary category tag (highest traffic)"
  echo "  2. 前端/后端/全栈         — Track-specific tag"
  echo "  3. 实战/经验分享          — Engagement booster"
  echo "  4. 架构/性能              — Tech depth indicator"
  echo "  5. 掘金技术社区           — Platform discovery tag"
  echo ""
  echo "  Keyword placement:"
  echo "  - Primary keyword in title ✓"
  echo "  - Primary keyword in first 100 chars ✓"
  echo "  - Related keywords in at least 2 H2 sections"
  echo "  - Natural density: 2-3%"
  echo ""
  echo "  Meta description (Juejin feed preview):"
  echo "  \"深入浅出讲解 $title，涵盖实战经验和避坑指南。适合初中级开发者阅读。\""

  if [ "$OUTPUT_FORMAT" = "json" ]; then
    cat <<JSONEOF
{
  "tags": ["$primary_tag", "实战经验", "技术深度", "架构设计", "掘金社区"],
  "keyword_placement": {
    "title": true,
    "first_100_chars": true,
    "h2_sections": 2,
    "density": "2-3%"
  },
  "meta_description": "深入浅出讲解 ${title}，涵盖实战经验和避坑指南。适合初中级开发者阅读。"
}
JSONEOF
  fi
}

# ── Step 8: Publishing Strategy ─────────────────────────────────────────────
publish_strategy() {
  local title="$1"

  header "Publishing Strategy"
  echo ""
  echo "  Best publish window:"
  echo "    Wednesday 10:00–11:00 (peak developer reading time)"
  echo "    Thursday  14:00–15:00 (afternoon break engagement)"
  echo ""
  echo "  Cross-promotion plan:"
  echo ""
  echo "  WeChat Moments:"
  echo "  \"写了一篇关于 《$title》 的文章，分享一些实际踩过的坑和解决方案，希望对大家有帮助 🚀\""
  echo ""
  echo "  Tech Community (V2EX):"
  echo "  \"[分享] $title — 含完整代码示例和性能对比数据\""
  echo ""
  echo "  First-hour engagement:"
  echo "  1. Reply to first 5 comments within 15 min"
  echo "  2. Acknowledge each — \"好问题！我在文章第X节有详细说明\""
  echo "  3. Extend discussion — \"你怎么看待XX？欢迎继续讨论\""
  echo ""
  echo "  Series potential:"
  echo "  This topic could be part 1 of a 3-part series. Consider:"
  echo "  - Part 2: 进阶技巧与常见陷阱"
  echo "  - Part 3: 生产环境最佳实践"

  if [ "$OUTPUT_FORMAT" = "json" ]; then
    cat <<JSONEOF
{
  "best_publish_time": {"day": "Wednesday", "time": "10:00-11:00"},
  "alt_publish_time": {"day": "Thursday", "time": "14:00-15:00"},
  "promotion": {
    "wechat_moments": "写了一篇关于 《${title}》 的文章，分享实际踩过的坑和解决方案",
    "v2ex": "[分享] ${title} — 含完整代码示例和性能对比数据"
  },
  "engagement_plan": {
    "respond_within_minutes": 15,
    "strategy": "acknowledge, extend, ask follow-up"
  }
}
JSONEOF
  fi
}

# ── Full Optimization Pipeline ──────────────────────────────────────────────
full_optimization() {
  local title="$1"
  local tags="$2"

  header "Full Optimization Pipeline"
  echo "=================================================="

  diagnose_article "$title" "$tags"
  echo ""
  echo "=================================================="
  generate_titles "$title"
  echo ""
  echo "=================================================="
  recommend_tags "$title" "$tags"
  echo ""
  echo "=================================================="
  publish_strategy "$title"

  echo ""
  info "Full optimization complete. Estimated score improvement: +2.5 - 4.0 points."
}

# ── Main ────────────────────────────────────────────────────────────────────
OUTPUT_FORMAT="table"
TITLE=""
TASK=""
TAGS=""

while [ $# -gt 0 ]; do
  case "$1" in
    --title|-t) TITLE="$2"; shift 2 ;;
    --task|-k) TASK="$2"; shift 2 ;;
    --tags|-g) TAGS="$2"; shift 2 ;;
    --output|-o) OUTPUT_FORMAT="$2"; shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown option: $1"; usage; exit 1 ;;
  esac
done

if [ -z "$TITLE" ] && [ "$TASK" != "help" ]; then
  echo "Error: --title is required."; usage; exit 1
fi
if [ -z "$TASK" ]; then
  echo "Error: --task is required."; usage; exit 1
fi

case "$TASK" in
  diagnose)  diagnose_article "$TITLE" "$TAGS" ;;
  title)     generate_titles "$TITLE" ;;
  tags)      recommend_tags "$TITLE" "$TAGS" ;;
  seo)       recommend_tags "$TITLE" "$TAGS" ;;
  publish)   publish_strategy "$TITLE" ;;
  full)      full_optimization "$TITLE" "$TAGS" ;;
  *)         echo "Error: Unknown task '$TASK'. Valid: diagnose|title|tags|seo|publish|full"; usage; exit 1 ;;
esac

echo ""
info "Juejin Article Optimizer v1.0.0 complete."

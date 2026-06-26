#!/bin/bash

# 今日人格运势（娱乐性质）
# 用法: bash daily_horoscope.sh [你的MBTI类型]

TYPE=${1:-"INTJ"}
TYPE=$(echo "$TYPE" | tr '[:lower:]' '[:upper:]')

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 基于日期生成伪随机数（保证同一天结果一致）
day_of_year=$(date +%j)
seed=$((day_of_year + $(echo "$TYPE" | sum | cut -d' ' -f1)))

# 随机选择函数
function random_select() {
    local arr=("$@")
    local idx=$((seed % ${#arr[@]}))
    echo "${arr[$idx]}"
}

# 各领域运势文本
declare -a work_advice
declare -a love_advice
declare -a social_advice
declare -a luck_items
declare -a lucky_colors

work_advice=(
    "今天适合处理需要深度思考的任务"
    "团队合作会带来意想不到的收获"
    "避免陷入完美主义，先完成再优化"
    "尝试用新的方法解决老问题"
    "注意劳逸结合，效率比时长更重要"
)

love_advice=(
    "坦诚表达你的感受，不要让对方猜测"
    "给对方一些空间，过度的关心可能变成压力"
    "今天适合进行深入的交流"
    "用行动而非言语表达你的关心"
    "保持耐心，好的关系需要时间培养"
)

social_advice=(
    "主动发起对话，今天你的社交能量很强"
    "选择小范围的深度交流而非大型聚会"
    "倾听比表达更重要"
    "今天适合修复之前的误会"
    "保持真诚，做真实的自己"
)

luck_items=("笔记本" "耳机" "咖啡" "书签" "便签纸")
lucky_colors=("深蓝" "墨绿" "暖黄" "浅灰" "酒红")

# 运势指数计算（1-5星）
work_stars=$(( (seed % 3) + 3 ))
love_stars=$(( (seed * 7 % 3) + 3 ))
social_stars=$(( (seed * 13 % 3) + 3 ))

function print_stars() {
    local count=$1
    local stars=""
    for ((i=0; i<count; i++)); do
        stars="${stars}★"
    done
    for ((i=count; i<5; i++)); do
        stars="${stars}☆"
    done
    echo "$stars"
}

echo "═══════════════════════════════════════════════════════════════════"
echo -e "              ${TYPE} 今日运势 - $(date '+%Y年%m月%d日')"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

echo -e "${BLUE}【工作/学习】${NC} $(print_stars $work_stars)"
echo "$(random_select "${work_advice[@]}")"
echo ""

echo -e "${GREEN}【感情/人际】${NC} $(print_stars $love_stars)"
echo "$(random_select "${love_advice[@]}")"
echo ""

echo -e "${CYAN}【社交/沟通】${NC} $(print_stars $social_stars)"
echo "$(random_select "${social_advice[@]}")"
echo ""

echo "─────────────────────────────────────────────────────────────────"
echo -e "${YELLOW}今日幸运色:${NC} $(random_select "${lucky_colors[@]}")"
echo -e "${YELLOW}幸运物品:${NC} $(random_select "${luck_items[@]}")"
echo "─────────────────────────────────────────────────────────────────"
echo ""

echo "═══════════════════════════════════════════════════════════════════"
echo "⚠️  免责声明：此运势仅供娱乐，不应作为决策依据"
echo "═══════════════════════════════════════════════════════════════════"
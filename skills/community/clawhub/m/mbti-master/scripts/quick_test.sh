#!/bin/bash

# MBTI快速测试 - 4维度8题版
# 用法: bash quick_test.sh

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "═══════════════════════════════════════"
echo "        MBTI 快速人格测试"
echo "            Created by 申哥"
echo "═══════════════════════════════════════"
echo ""
echo "回答以下8个问题，选择最符合你倾向的选项（A或B）"
echo ""

# 初始化分数
declare -A scores
declare -A descriptions

scores[E]=0
scores[I]=0
scores[S]=0
scores[N]=0
scores[T]=0
scores[F]=0
scores[J]=0
scores[P]=0

descriptions[E]="外向 - 从外部世界获取能量"
descriptions[I]="内向 - 从内心世界获取能量"
descriptions[S]="实感 - 关注具体事实和细节"
descriptions[N]="直觉 - 关注模式和可能性"
descriptions[T]="思考 - 基于逻辑做决策"
descriptions[F]="情感 - 基于价值观做决策"
descriptions[J]="判断 - 喜欢计划和结构"
descriptions[P]="感知 - 喜欢灵活和开放"

# 问题1: E/I
echo "【问题1】在社交场合后，你通常感到："
echo "  A) 充满活力，还想继续社交"
echo "  B) 需要独处恢复精力"
echo ""
read -p "你的选择 (A/B): " q1
if [[ $q1 == "A" || $q1 == "a" ]]; then
    scores[E]=$((scores[E] + 1))
else
    scores[I]=$((scores[I] + 1))
fi
echo ""

# 问题2: E/I
echo "【问题2】你更倾向于："
echo "  A) 边想边说，在交流中理清思路"
echo "  B) 先想清楚，再表达观点"
echo ""
read -p "你的选择 (A/B): " q2
if [[ $q2 == "A" || $q2 == "a" ]]; then
    scores[E]=$((scores[E] + 1))
else
    scores[I]=$((scores[I] + 1))
fi
echo ""

# 问题3: S/N
echo "【问题3】你更关注："
echo "  A) 当下的具体细节和实际情况"
echo "  B) 未来的可能性和整体模式"
echo ""
read -p "你的选择 (A/B): " q3
if [[ $q3 == "A" || $q3 == "a" ]]; then
    scores[S]=$((scores[S] + 1))
else
    scores[N]=$((scores[N] + 1))
fi
echo ""

# 问题4: S/N
echo "【问题4】学习新事物时，你更喜欢："
echo "  A) 循序渐进，从基础开始"
echo "  B) 先了解整体框架，再深入细节"
echo ""
read -p "你的选择 (A/B): " q4
if [[ $q4 == "A" || $q4 == "a" ]]; then
    scores[S]=$((scores[S] + 1))
else
    scores[N]=$((scores[N] + 1))
fi
echo ""

# 问题5: T/F
echo "【问题5】做决定时，你更重视："
echo "  A) 客观逻辑和因果分析"
echo "  B) 个人价值和对他人的影响"
echo ""
read -p "你的选择 (A/B): " q5
if [[ $q5 == "A" || $q5 == "a" ]]; then
    scores[T]=$((scores[T] + 1))
else
    scores[F]=$((scores[F] + 1))
fi
echo ""

# 问题6: T/F
echo "【问题6】面对冲突，你更倾向于："
echo "  A) 直接指出问题，寻求最佳解决方案"
echo "  B) 考虑各方感受，寻求和谐共识"
echo ""
read -p "你的选择 (A/B): " q6
if [[ $q6 == "A" || $q6 == "a" ]]; then
    scores[T]=$((scores[T] + 1))
else
    scores[F]=$((scores[F] + 1))
fi
echo ""

# 问题7: J/P
echo "【问题7】你的工作/生活方式更像："
echo "  A) 有计划、有条理，按部就班"
echo "  B) 灵活应变，随性而为"
echo ""
read -p "你的选择 (A/B): " q7
if [[ $q7 == "A" || $q7 == "a" ]]; then
    scores[J]=$((scores[J] + 1))
else
    scores[P]=$((scores[P] + 1))
fi
echo ""

# 问题8: J/P
echo "【问题8】面对截止日期，你通常："
echo "  A) 提前完成，避免最后时刻的压力"
echo "  B) 在压力下效率更高，喜欢最后冲刺"
echo ""
read -p "你的选择 (A/B): " q8
if [[ $q8 == "A" || $q8 == "a" ]]; then
    scores[J]=$((scores[J] + 1))
else
    scores[P]=$((scores[P] + 1))
fi
echo ""

# 计算结果
echo "═══════════════════════════════════════"
echo "            测试结果"
echo "═══════════════════════════════════════"
echo ""

# 确定四字母类型
type=""
if [ ${scores[E]} -gt ${scores[I]} ]; then
    type="${type}E"
    echo -e "${GREEN}E (外向)${NC}: ${descriptions[E]}"
else
    type="${type}I"
    echo -e "${GREEN}I (内向)${NC}: ${descriptions[I]}"
fi

if [ ${scores[S]} -gt ${scores[N]} ]; then
    type="${type}S"
    echo -e "${GREEN}S (实感)${NC}: ${descriptions[S]}"
else
    type="${type}N"
    echo -e "${GREEN}N (直觉)${NC}: ${descriptions[N]}"
fi

if [ ${scores[T]} -gt ${scores[F]} ]; then
    type="${type}T"
    echo -e "${GREEN}T (思考)${NC}: ${descriptions[T]}"
else
    type="${type}F"
    echo -e "${GREEN}F (情感)${NC}: ${descriptions[F]}"
fi

if [ ${scores[J]} -gt ${scores[P]} ]; then
    type="${type}J"
    echo -e "${GREEN}J (判断)${NC}: ${descriptions[J]}"
else
    type="${type}P"
    echo -e "${GREEN}P (感知)${NC}: ${descriptions[P]}"
fi

echo ""
echo "═══════════════════════════════════════"
echo -e "    你的MBTI类型是: ${YELLOW}${type}${NC}"
echo "═══════════════════════════════════════"
echo ""

# 保存结果
RESULTS_DIR="$HOME/.mbti-results"
mkdir -p "$RESULTS_DIR"
echo "$(date '+%Y-%m-%d %H:%M'),$type,快速测试" >> "$RESULTS_DIR/test_history.csv"

echo "查看详细分析:"
echo "  bash scripts/type_analysis.sh $type"
echo ""
echo "查看兼容性:"
echo "  bash scripts/compatibility.sh $type [对方类型]"
echo ""
echo "💾 测试结果已保存至: $RESULTS_DIR/test_history.csv"
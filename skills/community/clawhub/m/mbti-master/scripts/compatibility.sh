#!/bin/bash

# 人格兼容性匹配
# 用法: bash compatibility.sh [你的类型] [对方类型]
# 示例: bash compatibility.sh INTJ ENFP

TYPE1=${1:-"INTJ"}
TYPE2=${2:-"ENFP"}
TYPE1=$(echo "$TYPE1" | tr '[:lower:]' '[:upper:]')
TYPE2=$(echo "$TYPE2" | tr '[:lower:]' '[:upper:]')

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 兼容性评分和描述
declare -A compatibility_scores
declare -A compatibility_desc

# 黄金配对（主导功能互补）
compatibility_scores["INTJ_ENFP"]="95"
compatibility_scores["ENFP_INTJ"]="95"
compatibility_scores["INTJ_ENTP"]="90"
compatibility_scores["ENTP_INTJ"]="90"
compatibility_scores["INFJ_ENTP"]="95"
compatibility_scores["ENTP_INFJ"]="95"
compatibility_scores["INFJ_ENFP"]="90"
compatibility_scores["ENFP_INFJ"]="90"

# 镜像类型（吸引但冲突）
compatibility_scores["INTJ_ESFP"]="70"
compatibility_scores["ESFP_INTJ"]="70"
compatibility_scores["INTP_ESFJ"]="70"
compatibility_scores["ESFJ_INTP"]="70"
compatibility_scores["ENTJ_ISFP"]="70"
compatibility_scores["ISFP_ENTJ"]="70"

# 相似类型（理解但可能 stagnation）
compatibility_scores["INTJ_INTJ"]="85"
compatibility_scores["ENFP_ENFP"]="80"
compatibility_scores["INTP_INTP"]="85"

# 默认中等兼容性
default_score="75"

key="${TYPE1}_${TYPE2}"
score=${compatibility_scores[$key]:-$default_score}

echo "═══════════════════════════════════════════════════"
echo -e "    ${TYPE1} × ${TYPE2} 兼容性分析"
echo "═══════════════════════════════════════════════════"
echo ""

# 评分展示
if [ $score -ge 90 ]; then
    echo -e "匹配度: ${GREEN}★★★★★ ${score}/100${NC} (极佳)"
    echo -e "${GREEN}黄金配对！你们的功能栈互补，能够互相激发成长。${NC}"
elif [ $score -ge 80 ]; then
    echo -e "匹配度: ${GREEN}★★★★☆ ${score}/100${NC} (优秀)"
    echo -e "${GREEN}高度兼容，有共同语言且能互相补充。${NC}"
elif [ $score -ge 70 ]; then
    echo -e "匹配度: ${YELLOW}★★★☆☆ ${score}/100${NC} (良好)"
    echo -e "${YELLOW}有吸引力但需要理解和妥协。${NC}"
else
    echo -e "匹配度: ${YELLOW}★★☆☆☆ ${score}/100${NC} (一般)"
    echo -e "${YELLOW}差异较大，需要更多努力经营关系。${NC}"
fi

echo ""

# 分析维度
echo -e "${CYAN}【沟通模式】${NC}"

# 第一个字母相同
if [ "${TYPE1:0:1}" == "${TYPE2:0:1}" ]; then
    echo "✓ 能量获取方式相同，相处节奏一致"
else
    echo "⚡ 内外向差异：一方需要独处充电，一方需要社交充电"
    echo "  建议：尊重彼此的能量恢复方式，给对方空间"
fi

# 第二个字母相同
if [ "${TYPE1:1:1}" == "${TYPE2:1:1}" ]; then
    echo "✓ 信息处理方式相同，容易理解对方的思维方式"
else
    echo "⚡ 感知差异：一方关注细节事实，一方关注模式未来"
    echo "  建议：欣赏彼此的不同视角，互补而非对立"
fi

# 第三个字母相同
if [ "${TYPE1:2:1}" == "${TYPE2:2:1}" ]; then
    echo "✓ 决策方式一致，价值观容易达成共识"
else
    echo "⚡ 决策差异：一方重逻辑，一方重情感"
    echo "  建议：理解对方决策背后的逻辑/价值依据"
fi

# 第四个字母相同
if [ "${TYPE1:3:1}" == "${TYPE2:3:1}" ]; then
    echo "✓ 生活方式相似，减少日常摩擦"
else
    echo "⚡ 生活方式差异：一方喜欢计划，一方喜欢随性"
    echo "  建议：在计划与灵活之间找到平衡点"
fi

echo ""
echo -e "${CYAN}【相处建议】${NC}"

if [ $score -ge 90 ]; then
    echo "• 你们是天然的学习伙伴，能够激发彼此最好的一面"
    echo "• 注意：不要因为太过舒适而忽视经营关系"
    echo "• 共同成长是你们关系的主题"
elif [ $score -ge 80 ]; then
    echo "• 有相似的世界观，容易建立深层连接"
    echo "• 注意：避免陷入舒适区，保持新鲜感"
    echo "• 共同的兴趣和价值观是你们的优势"
elif [ $score -ge 70 ]; then
    echo "• 差异带来吸引力，但也可能产生摩擦"
    echo "• 关键是理解和接纳彼此的不同"
    echo "• 沟通时多考虑对方的认知功能偏好"
else
    echo "• 差异较大，需要更多的耐心和包容"
    echo "• 明确彼此的底线和需求"
    echo "• 差异可以互补，也可能冲突，取决于经营方式"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "注：MBTI兼容性仅供参考，真实关系取决于双方的成熟度和努力。"
echo "═══════════════════════════════════════════════════"
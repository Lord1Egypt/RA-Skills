#!/bin/bash

# 人格猜猜看游戏
# 用法: bash guess_game.sh

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# 问题和答案数组
declare -a descriptions
declare -a answers
declare -a hints

descriptions[0]="他们是天生的战略家，善于制定长期计划并坚决执行。
喜欢独立工作，追求知识和能力的提升，对效率有极高要求。
往往显得有些神秘和难以接近，但对认定的目标会全力以赴。"
answers[0]="INTJ"
hints[0]="被称为'建筑师'，约占人口的2%"

descriptions[1]="他们是充满热情的创意者，总能看到事物的多种可能性。
善于激励他人，追求自由和意义，讨厌被束缚。
社交中充满魅力，但内心深处需要authenticity。"
answers[1]="ENFP"
hints[1]="被称为'竞选者'，是理想的创业伙伴"

descriptions[2]="他们是温暖体贴的保护者，总是默默关心他人的需求。
重视和谐与传统，有强烈的责任感。
往往不善于表达自己的想法，但会无私地为他人付出。"
answers[2]="ISFJ"
hints[2]="被称为'守卫者'，约占人口的13-14%"

descriptions[3]="他们是精力充沛的行动派，善于把握机会并立即行动。
喜欢刺激和冒险，活在当下，不拘小节。
在危机中往往表现最佳，善于解决实际问题。"
answers[3]="ESTP"
hints[3]="被称为'企业家'，是天生的销售人才"

descriptions[4]="他们是追求真理的理论家，热爱分析复杂系统和抽象概念。
思维独立，好奇心强，常常沉浸在自己的思考世界中。
对社交活动兴趣不大，但讨论感兴趣的话题时会滔滔不绝。"
answers[4]="INTP"
hints[4]="被称为'逻辑学家'，爱因斯坦就是这一类型"

descriptions[5]="他们是魅力四射的激励者，善于理解他人需求并帮助他们成长。
天生的教育者和领导者，重视和谐与人际关系。
有时会过度关注他人而忽略自己的需求。"
answers[5]="ENFJ"
hints[5]="被称为'主人公'，奥巴马、奥普拉都是这一类型"

score=0
total=${#descriptions[@]}

echo "═══════════════════════════════════════════════════════════════════"
echo "                    MBTI 人格猜猜看"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "根据描述猜出是哪种MBTI人格类型（4个字母）"
echo "输入你的答案，或输入'hint'获取提示"
echo ""

for i in "${!descriptions[@]}"; do
    echo -e "${BLUE}问题 $((i+1))/${total}:${NC}"
    echo "─────────────────────────────────────────────────────────────────"
    echo "${descriptions[$i]}"
    echo ""
    
    while true; do
        read -p "你的答案 (4个字母): " guess
        guess=$(echo "$guess" | tr '[:lower:]' '[:upper:]')
        
        if [ "$guess" == "HINT" ]; then
            echo -e "${YELLOW}提示: ${hints[$i]}${NC}"
        elif [ "$guess" == "${answers[$i]}" ]; then
            echo -e "${GREEN}✓ 正确！是 ${answers[$i]}${NC}"
            score=$((score + 1))
            break
        else
            echo -e "${RED}✗ 不对，再想想 (输入'hint'获取提示)${NC}"
        fi
    done
    
    echo ""
done

echo "═══════════════════════════════════════════════════════════════════"
echo -e "                  游戏结束！你的得分: ${GREEN}${score}/${total}${NC}"
echo "═══════════════════════════════════════════════════════════════════"

if [ $score -eq $total ]; then
    echo -e "${GREEN}🏆 完美！你是MBTI大师！${NC}"
elif [ $score -ge $((total * 2 / 3)) ]; then
    echo -e "${GREEN}👏 不错！你对MBTI有很好的理解${NC}"
else
    echo -e "${YELLOW}💪 继续学习！建议查看详细分析:${NC}"
    echo "  bash scripts/type_cheatsheet.sh"
fi
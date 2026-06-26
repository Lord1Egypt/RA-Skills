#!/bin/bash

# 人格类型详细分析
# 用法: bash type_analysis.sh [MBTI类型]
# 示例: bash type_analysis.sh INTJ

TYPE=${1:-"INTJ"}
TYPE=$(echo "$TYPE" | tr '[:lower:]' '[:upper:]')

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 定义16种人格的详细信息
declare -A types
declare -A nicknames
declare -A functions
declare -A careers
declare -A relationships

# INTJ - 建筑师
types[INTJ]="独立思考的战略家，善于制定长期计划并执行。追求知识和能力，重视效率和逻辑。"
nicknames[INTJ]="建筑师 (Architect)"
functions[INTJ]="主导: Ni (内倾直觉) - 洞察未来趋势\n辅助: Te (外倾思考) - 高效执行计划\n第三: Fi (内倾情感) - 内心价值坚守\n劣势: Se (外倾感觉) - 当下体验较弱"
careers[INTJ]="战略顾问、系统架构师、投资分析师、科研工作者、企业高管"
relationships[INTJ]="重视 intellectual connection，需要独立空间，表达情感较内敛，但忠诚度极高"

# INTP - 逻辑学家
types[INTP]="追求真理的理论家，热爱分析复杂系统和抽象概念。思维独立，好奇心强。"
nicknames[INTP]="逻辑学家 (Logician)"
functions[INTP]="主导: Ti (内倾思考) - 构建逻辑体系\n辅助: Ne (外倾直觉) - 探索多种可能\n第三: Si (内倾感觉) - 细节记忆\n劣势: Fe (外倾情感) - 社交共情较弱"
careers[INTP]="软件工程师、理论物理学家、数学家、哲学家、数据科学家"
relationships[INTP]="重视思想交流，可能忽略情感表达，需要理解型伴侣"

# ENTJ - 指挥官
types[ENTJ]="天生的领导者，果断高效，善于组织资源达成目标。战略思维强，执行力突出。"
nicknames[ENTJ]="指挥官 (Commander)"
functions[ENTJ]="主导: Te (外倾思考) - 目标导向执行\n辅助: Ni (内倾直觉) - 战略规划\n第三: Se (外倾感觉) - 把握当下\n劣势: Fi (内倾情感) - 个人情感处理"
careers[ENTJ]="企业CEO、管理顾问、创业者、律师、政治领袖"
relationships[ENTJ]="直接坦率，期望伴侣有独立性和进取心，可能显得强势"

# ENTP - 辩论家
types[ENTP]="充满创意的辩论家，热爱智力挑战和新颖想法。机智幽默，善于发现可能性。"
nicknames[ENTP]="辩论家 (Debater)"
functions[ENTP]="主导: Ne (外倾直觉) - 探索创新\n辅助: Ti (内倾思考) - 逻辑分析\n第三: Fe (外倾情感) - 社交魅力\n劣势: Si (内倾感觉) - 细节执行力"
careers[ENTP]="创业者、律师、咨询顾问、创意总监、政治家"
relationships[ENTP]="需要智力刺激，厌恶单调，喜欢有趣且独立的伴侣"

# INFJ - 提倡者
types[INFJ]="理想主义的倡导者，具有深刻洞察力和强烈使命感。追求意义，关心人类福祉。"
nicknames[INFJ]="提倡者 (Advocate)"
functions[INFJ]="主导: Ni (内倾直觉) - 深刻洞察\n辅助: Fe (外倾情感) - 共情他人\n第三: Ti (内倾思考) - 内在逻辑\n劣势: Se (外倾感觉) - 当下体验"
careers[INFJ]="心理咨询师、作家、人权工作者、教育工作者、非营利组织领导者"
relationships[INFJ]="寻求深层连接，理想主义，需要被理解，忠诚且投入"

# INFP - 调停者
types[INFP]="理想主义的梦想家，忠于内心价值，富有创造力。追求authenticity和意义。"
nicknames[INFP]="调停者 (Mediator)"
functions[INFP]="主导: Fi (内倾情感) - 价值坚守\n辅助: Ne (外倾直觉) - 创意探索\n第三: Si (内倾感觉) - 经验内化\n劣势: Te (外倾思考) - 外部执行"
careers[INFP]="作家、艺术家、心理咨询师、音乐家、人力资源"
relationships[INFP]="浪漫理想主义，需要情感深度，重视被接纳和理解"

# ENFJ - 主人公
types[ENFJ]="魅力四射的激励者，善于理解他人需求并帮助他们成长。天生的教育者和领导者。"
nicknames[ENFJ]="主人公 (Protagonist)"
functions[ENFJ]="主导: Fe (外倾情感) - 共情领导\n辅助: Ni (内倾直觉) - 洞察潜力\n第三: Se (外倾感觉) - 当下互动\n劣势: Ti (内倾思考) - 内在逻辑"
careers[ENFJ]="教师、培训师、HR总监、销售总监、政治家、非营利组织领导"
relationships[ENFJ]="付出型，关注伴侣成长，可能过度照顾他人而忽略自己"

# ENFP - 竞选者
types[ENFP]="热情洋溢的创意者，充满好奇心和可能性。善于激励他人，追求自由和意义。"
nicknames[ENFP]="竞选者 (Campaigner)"
functions[ENFP]="主导: Ne (外倾直觉) - 探索可能\n辅助: Fi (内倾情感) - 价值驱动\n第三: Te (外倾思考) - 目标执行\n劣势: Si (内倾感觉) - 细节稳定"
careers[ENFP]="创意总监、记者、演员、创业者、咨询顾问、教师"
relationships[ENFP]="热情浪漫，需要精神共鸣，厌恶束缚，喜欢探索和成长"

# ISTJ - 检查员
types[ISTJ]="可靠负责的实干家，重视传统和秩序。细节导向，执行力强，值得信赖。"
nicknames[ISTJ]="检查员 (Logistician)"
functions[ISTJ]="主导: Si (内倾感觉) - 经验细节\n辅助: Te (外倾思考) - 高效执行\n第三: Fi (内倾情感) - 内在价值\n劣势: Ne (外倾直觉) - 可能性探索"
careers[ISTJ]="会计、审计师、系统管理员、法官、军官、项目经理"
relationships[ISTJ]="忠诚稳定，通过行动表达爱，需要明确的承诺和稳定"

# ISFJ - 守卫者
types[ISFJ]="温暖体贴的保护者，默默付出，关心他人需求。重视和谐，有强烈的责任感。"
nicknames[ISFJ]="守卫者 (Defender)"
functions[ISFJ]="主导: Si (内倾感觉) - 细节关怀\n辅助: Fe (外倾情感) - 他人需求\n第三: Ti (内倾思考) - 内在逻辑\n劣势: Ne (外倾直觉) - 可能性探索"
careers[ISFJ]="护士、社工、行政助理、教师、客户服务、人力资源"
relationships[ISFJ]="无私奉献型，需要被认可和感谢，可能压抑自身需求"

# ESTJ - 总经理
types[ESTJ]="务实高效的管理者，善于组织资源和人员。重视传统，执行力强，结果导向。"
nicknames[ESTJ]="总经理 (Executive)"
functions[ESTJ]="主导: Te (外倾思考) - 目标执行\n辅助: Si (内倾感觉) - 经验细节\n第三: Ne (外倾直觉) - 可能性\n劣势: Fi (内倾情感) - 个人价值"
careers[ESTJ]="企业管理者、军官、法官、项目经理、政府官员、银行家"
relationships[ESTJ]="传统且负责，通过提供稳定表达爱，可能显得不够浪漫"

# ESFJ - 执政官
types[ESFJ]="热心肠的协调者，善于维护和谐的人际关系。关心他人，重视社会规范。"
nicknames[ESFJ]="执政官 (Consul)"
functions[ESFJ]="主导: Fe (外倾情感) - 和谐共情\n辅助: Si (内倾感觉) - 传统细节\n第三: Ne (外倾直觉) - 可能性\n劣势: Ti (内倾思考) - 内在逻辑"
careers[ESFJ]="教师、护士、社工、HR、销售、活动策划、客户服务"
relationships[ESFJ]="关心照顾型，需要被需要，重视家庭和社会认可"

# ISTP - 鉴赏家
types[ISTP]="冷静理性的手艺人，善于分析问题并找到实际解决方案。独立，喜欢动手操作。"
nicknames[ISTP]="鉴赏家 (Virtuoso)"
functions[ISTP]="主导: Ti (内倾思考) - 逻辑分析\n辅助: Se (外倾感觉) - 当下体验\n第三: Ni (内倾直觉) - 洞察\n劣势: Fe (外倾情感) - 共情表达"
careers[ISTP]="工程师、飞行员、外科医生、法医、技术专家、运动员"
relationships[ISTP]="独立自由，通过行动而非言语表达，需要个人空间"

# ISFP - 探险家
types[ISFP]="敏感艺术的创作者，追求authenticity和美好体验。温和，活在当下，富有审美力。"
nicknames[ISFP]="探险家 (Adventurer)"
functions[ISFP]="主导: Fi (内倾情感) - 价值authenticity\n辅助: Se (外倾感觉) - 当下体验\n第三: Ni (内倾直觉) - 内在洞察\n劣势: Te (外倾思考) - 外部执行"
careers[ISFP]="艺术家、设计师、音乐家、厨师、护士、兽医、摄影师"
relationships[ISFP]="温柔浪漫，需要被接纳真实自我，厌恶冲突和压力"

# ESTP - 企业家
types[ESTP]="精力充沛的行动派，善于把握机会并立即行动。务实，喜欢刺激和冒险。"
nicknames[ESTP]="企业家 (Entrepreneur)"
functions[ESTP]="主导: Se (外倾感觉) - 当下行动\n辅助: Ti (内倾思考) - 逻辑分析\n第三: Fe (外倾情感) - 社交影响\n劣势: Ni (内倾直觉) - 长远洞察"
careers[ESTP]="创业者、销售、营销人员、急救人员、运动员、金融交易员"
relationships[ESTP]="激情四溢，喜欢刺激，可能缺乏长期规划，需要有趣伴侣"

# ESFP - 表演者
types[ESFP]="活力四射的表演者，热爱生活和社交。乐观，善于带动气氛，享受当下。"
nicknames[ESFP]="表演者 (Entertainer)"
functions[ESFP]="主导: Se (外倾感觉) - 当下体验\n辅助: Fi (内倾情感) - 价值authenticity\n第三: Te (外倾思考) - 目标执行\n劣势: Ni (内倾直觉) - 长远规划"
careers[ESFP]="演员、销售、公关、活动策划、主持人、旅游顾问、儿科医生"
relationships[ESFP]="热情浪漫，喜欢被关注，需要乐趣和刺激，社交能力强"

# 输出分析
echo "═══════════════════════════════════════════════════"
echo -e "              ${YELLOW}${TYPE} - ${nicknames[$TYPE]}${NC}"
echo "═══════════════════════════════════════════════════"
echo ""

if [ -z "${types[$TYPE]}" ]; then
    echo -e "${RED}错误: 未知的MBTI类型 '${TYPE}'${NC}"
    echo "有效的类型: INTJ, INTP, ENTJ, ENTP, INFJ, INFP, ENFJ, ENFP"
    echo "            ISTJ, ISFJ, ESTJ, ESFJ, ISTP, ISFP, ESTP, ESFP"
    exit 1
fi

echo -e "${CYAN}【核心特征】${NC}"
echo "${types[$TYPE]}"
echo ""

echo -e "${CYAN}【认知功能栈】${NC}"
echo -e "${functions[$TYPE]}"
echo ""

echo -e "${CYAN}【适合职业】${NC}"
echo "${careers[$TYPE]}"
echo ""

echo -e "${CYAN}【人际关系】${NC}"
echo "${relationships[$TYPE]}"
echo ""

echo -e "${CYAN}【成长建议】${NC}"
case $TYPE in
    INTJ|INTP|ENTJ|ENTP)
        echo "• 关注情感因素，不只用逻辑做决策"
        echo "• 适当放松对完美的追求"
        echo "• 学会表达内心感受"
        ;;
    INFJ|INFP|ENFJ|ENFP)
        echo "• 建立健康的边界，不过度付出"
        echo "• 将理想转化为可执行的计划"
        echo "• 接受不完美的现实"
        ;;
    ISTJ|ISFJ|ESTJ|ESFJ)
        echo "• 保持开放心态，接受变化"
        echo "• 关注自身需求，不过度压抑"
        echo "• 尝试新的可能性"
        ;;
    ISTP|ISFP|ESTP|ESFP)
        echo "• 考虑长期后果，不只看当下"
        echo "• 建立稳定的生活节奏"
        echo "• 适当规划未来"
        ;;
esac

echo ""
echo "═══════════════════════════════════════════════════"
echo "查看兼容性: bash scripts/compatibility.sh ${TYPE} [对方类型]"
echo "═══════════════════════════════════════════════════"
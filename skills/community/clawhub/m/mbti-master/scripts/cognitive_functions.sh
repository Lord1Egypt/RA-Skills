#!/bin/bash

# 8种认知功能详解
# 用法: bash cognitive_functions.sh

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "═══════════════════════════════════════════════════════════════════"
echo "                    荣格认知功能详解"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

echo -e "${BLUE}【感知功能 (Perceiving Functions)】${NC}"
echo "如何收集信息、认识世界"
echo ""

echo -e "${CYAN}Ni (内倾直觉) - Introverted Intuition${NC}"
echo "─────────────────────────────────────────────────────────────────"
echo "• 洞察事物本质和发展趋势"
echo "• 善于预见未来、规划长远"
echo "• 关注抽象模式和象征意义"
echo "• 代表类型: INTJ, INFJ, ENTJ, ENFJ"
echo ""

echo -e "${CYAN}Ne (外倾直觉) - Extraverted Intuition${NC}"
echo "─────────────────────────────────────────────────────────────────"
echo "• 探索多种可能性和创新思路"
echo "• 善于联想、头脑风暴"
echo "• 关注外部机会和潜在联系"
echo "• 代表类型: ENTP, ENFP, INTP, INFP"
echo ""

echo -e "${GREEN}Si (内倾感觉) - Introverted Sensing${NC}"
echo "─────────────────────────────────────────────────────────────────"
echo "• 精确记忆细节和经验"
echo "• 重视传统和已验证的方法"
echo "• 关注内部的身体感受和记忆"
echo "• 代表类型: ISTJ, ISFJ, ESTJ, ESFJ"
echo ""

echo -e "${GREEN}Se (外倾感觉) - Extraverted Sensing${NC}"
echo "─────────────────────────────────────────────────────────────────"
echo "• 敏锐感知当下的外部环境"
echo "• 善于把握当下机会和实际行动"
echo "• 享受感官体验和物质世界"
echo "• 代表类型: ESTP, ESFP, ISTP, ISFP"
echo ""

echo -e "${RED}【判断功能 (Judging Functions)】${NC}"
echo "如何做决策、组织生活"
echo ""

echo -e "${YELLOW}Ti (内倾思考) - Introverted Thinking${NC}"
echo "─────────────────────────────────────────────────────────────────"
echo "• 构建精确的逻辑体系"
echo "• 追求内在一致性和准确性"
echo "• 独立分析，不轻易受外界影响"
echo "• 代表类型: INTP, ISTP, ENTP, ESTP"
echo ""

echo -e "${YELLOW}Te (外倾思考) - Extraverted Thinking${NC}"
echo "─────────────────────────────────────────────────────────────────"
echo "• 追求效率和实际结果"
echo "• 善于组织资源和制定计划"
echo "• 关注可量化的成果和系统优化"
echo "• 代表类型: ENTJ, ESTJ, INTJ, ISTJ"
echo ""

echo -e "${RED}Fi (内倾情感) - Introverted Feeling${NC}"
echo "─────────────────────────────────────────────────────────────────"
echo "• 坚守个人核心价值观"
echo "• 追求authenticity和自我认同"
echo "• 深度的情感体验但不易外显"
echo "• 代表类型: INFP, ISFP, ENFP, ESFP"
echo ""

echo -e "${RED}Fe (外倾情感) - Extraverted Feeling${NC}"
echo "─────────────────────────────────────────────────────────────────"
echo "• 关注他人的情感需求和群体和谐"
echo "• 善于共情和维护社会关系"
echo "• 重视社会规范和他人的认可"
echo "• 代表类型: ENFJ, ESFJ, INFJ, ISFJ"
echo ""

echo "═══════════════════════════════════════════════════════════════════"
echo "认知功能顺序决定人格类型的独特表现："
echo "主导功能(1st) > 辅助功能(2nd) > 第三功能(3rd) > 劣势功能(4th)"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "查看你的人格类型的功能栈:"
echo "  bash scripts/type_analysis.sh [你的类型]"
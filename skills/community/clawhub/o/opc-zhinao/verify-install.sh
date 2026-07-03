#!/bin/bash

# OPC智脑安装验证脚本
# 用法：bash verify-install.sh

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  OPC智脑安装验证${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

ERRORS=0
WARNINGS=0

# 检查AGENTS.md
echo -e "${BLUE}[1/5] 检查AGENTS.md...${NC}"
if [ -f "AGENTS.md" ]; then
    LINES=$(wc -l < "AGENTS.md")
    SIZE=$(ls -lh "AGENTS.md" | awk '{print $5}')
    echo -e "${GREEN}  ✓ AGENTS.md存在 ($LINES 行, $SIZE)${NC}"
    
    # 检查关键内容
    if grep -q "OPC智脑" "AGENTS.md"; then
        echo -e "${GREEN}    ✓ 包含'OPC智脑'${NC}"
    else
        echo -e "${RED}    ✗ 缺少'OPC智脑'${NC}"
        ((ERRORS++))
    fi
    
    if grep -q "五阶段Skills" "AGENTS.md"; then
        echo -e "${GREEN}    ✓ 包含'五阶段Skills'${NC}"
    else
        echo -e "${RED}    ✗ 缺少'五阶段Skills'${NC}"
        ((ERRORS++))
    fi
    
    if grep -q "报告导出流程" "AGENTS.md"; then
        echo -e "${GREEN}    ✓ 包含'报告导出流程'${NC}"
    else
        echo -e "${RED}    ✗ 缺少'报告导出流程'${NC}"
        ((ERRORS++))
    fi
else
    echo -e "${RED}  ✗ AGENTS.md不存在${NC}"
    ((ERRORS++))
fi

echo ""

# 检查opc-zhinao.json
echo -e "${BLUE}[2/5] 检查opc-zhinao.json...${NC}"
if [ -f ".codeartsdoer/agents/opc-zhinao.json" ]; then
    echo -e "${GREEN}  ✓ opc-zhinao.json存在${NC}"
    
    if grep -q '"instructions": "AGENTS.md"' ".codeartsdoer/agents/opc-zhinao.json"; then
        echo -e "${GREEN}    ✓ instructions指向AGENTS.md${NC}"
    else
        echo -e "${RED}    ✗ instructions未指向AGENTS.md${NC}"
        ((ERRORS++))
    fi
    
    if grep -q '"name": "OPC智脑"' ".codeartsdoer/agents/opc-zhinao.json"; then
        echo -e "${GREEN}    ✓ name为'OPC智脑'${NC}"
    else
        echo -e "${RED}    ✗ name不正确${NC}"
        ((ERRORS++))
    fi
else
    echo -e "${RED}  ✗ opc-zhinao.json不存在${NC}"
    ((ERRORS++))
fi

echo ""

# 检查ProjectSkillStatus.txt
echo -e "${BLUE}[3/5] 检查ProjectSkillStatus.txt...${NC}"
if [ -f ".codeartsdoer/skills/ProjectSkillStatus.txt" ]; then
    REGISTERED=$(wc -l < ".codeartsdoer/skills/ProjectSkillStatus.txt")
    echo -e "${GREEN}  ✓ ProjectSkillStatus.txt存在${NC}"
    echo -e "${GREEN}    ✓ 已注册 $REGISTERED 个skills${NC}"
    
    # 检查关键skills
    for skill in skill1-idea-feasibility skill2-mvp-design report-export; do
        if grep -q "^$skill=true$" ".codeartsdoer/skills/ProjectSkillStatus.txt"; then
            echo -e "${GREEN}    ✓ $skill 已注册${NC}"
        else
            echo -e "${RED}    ✗ $skill 未注册${NC}"
            ((ERRORS++))
        fi
    done
else
    echo -e "${RED}  ✗ ProjectSkillStatus.txt不存在${NC}"
    ((ERRORS++))
fi

echo ""

# 检查skills目录
echo -e "${BLUE}[4/5] 检查skills目录...${NC}"
if [ -d ".codeartsdoer/skills" ]; then
    SKILL_DIRS=$(find .codeartsdoer/skills -mindepth 1 -maxdepth 1 -type d | wc -l)
    echo -e "${GREEN}  ✓ skills目录存在${NC}"
    echo -e "${GREEN}    ✓ 发现 $SKILL_DIRS 个skill目录${NC}"
    
    # 检查关键skills的SKILL.md
    for skill in skill1-idea-feasibility skill2-mvp-design report-export; do
        if [ -f ".codeartsdoer/skills/$skill/SKILL.md" ]; then
            echo -e "${GREEN}    ✓ $skill/SKILL.md 存在${NC}"
        else
            echo -e "${RED}    ✗ $skill/SKILL.md 不存在${NC}"
            ((ERRORS++))
        fi
    done
else
    echo -e "${RED}  ✗ skills目录不存在${NC}"
    ((ERRORS++))
fi

echo ""

# 完成
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  验证结果${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ 安装验证通过！${NC}"
    echo ""
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠ 有 $WARNINGS 个警告，但不影响使用${NC}"
    fi
    echo ""
    echo -e "${BLUE}项目结构：${NC}"
    echo "  your-project/"
    echo "  ├── AGENTS.md"
    echo "  └── .codeartsdoer/"
    echo "      ├── agents/"
    echo "      │   └── opc-zhinao.json"
    echo "      └── skills/"
    echo "          ├── ProjectSkillStatus.txt"
    echo "          └── ... (8个skills)"
    echo ""
    echo -e "${BLUE}下一步：${NC}"
    echo "  1. 在码道IDE中打开此项目"
    echo "  2. 输入创业Idea开始诊断"
    echo "  例如：'我想做一个XX产品'"
    exit 0
else
    echo -e "${RED}✗ 发现 $ERRORS 个错误${NC}"
    echo ""
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠ 有 $WARNINGS 个警告${NC}"
    fi
    echo ""
    echo -e "${BLUE}建议：${NC}"
    echo "  重新运行安装脚本："
    echo "  bash install-codearts.sh ."
    exit 1
fi
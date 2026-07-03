#!/bin/bash

# OPC智脑 - 通用安装脚本
# 作者：李屹镒（公众号：科技新潮。视频号：小李君与AI）
# 用法：bash install-prompt.sh [目标项目路径]
# 说明：智能检测项目环境，自动选择最佳安装方式
#
# ⚠️ 重要说明：
# 本脚本会自动检测目标项目的IDE环境，并选择对应的安装方式：
#   - 码道IDE项目：安装AGENTS.md + opc-zhinao.json + skills
#   - Cursor项目：安装.cursorrules + skills
#   - VSCode项目：安装.github/copilot-instructions.md + skills
#   - 国内主流IDE：安装AGENTS.md + skills（通义灵码、百度Comate、腾讯云AI代码助手、豆包MarsCode、CodeGeeX、讯飞iFlyCode）
#   - 其他项目：生成opc-zhinao-prompt.md（通用Prompt）
#
# 支持的IDE列表：
#   国内主流IDE：
#     - 码道IDE（CodeArts）
#     - 通义灵码（阿里云）
#     - 百度Comate
#     - 腾讯云AI代码助手
#     - 豆包MarsCode（字节跳动）
#     - CodeGeeX（智谱）
#     - 讯飞iFlyCode
#   国际主流IDE：
#     - Cursor
#     - VSCode + Copilot
#     - Windsurf
#     - CodeBuddy/WorkBuddy
#
# 如需强制使用特定IDE的安装方式，请使用对应的专用脚本：
#   - 码道IDE：install-codearts.sh
#   - CodeBuddy：install-codebuddy.sh
#   - 其他IDE：本脚本会自动适配

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 目标项目路径
TARGET_DIR="${1:-.}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  OPC智脑 - 通用安装${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查目标目录
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${YELLOW}目标目录不存在，正在创建：$TARGET_DIR${NC}"
    mkdir -p "$TARGET_DIR"
fi

cd "$TARGET_DIR"
TARGET_DIR="$(pwd)"

echo -e "${GREEN}✓ 源目录：$SOURCE_DIR${NC}"
echo -e "${GREEN}✓ 目标目录：$TARGET_DIR${NC}"
echo ""

# 检测项目环境
echo -e "${BLUE}[检测] 分析项目环境...${NC}"

PROJECT_TYPE="unknown"
PROJECT_TYPE_DESC="未知"

# 检测码道IDE项目
if [ -d ".codeartsdoer" ] || [ -f ".codeartsdoer/agents" ]; then
    PROJECT_TYPE="codearts"
    PROJECT_TYPE_DESC="码道IDE"
    echo -e "${GREEN}  ✓ 检测到码道IDE项目${NC}"
# 检测Cursor项目
elif [ -f ".cursorrules" ] || [ -d ".cursor" ]; then
    PROJECT_TYPE="cursor"
    PROJECT_TYPE_DESC="Cursor IDE"
    echo -e "${GREEN}  ✓ 检测到Cursor项目${NC}"
# 检测VSCode项目
elif [ -d ".vscode" ] || [ -f ".github/copilot-instructions.md" ]; then
    PROJECT_TYPE="vscode"
    PROJECT_TYPE_DESC="VSCode + Copilot"
    echo -e "${GREEN}  ✓ 检测到VSCode项目${NC}"
# 检测CodeBuddy/WorkBuddy项目
elif [ -d ".codebuddy" ] || [ -f ".codebuddy/skills-registry.json" ]; then
    PROJECT_TYPE="codebuddy"
    PROJECT_TYPE_DESC="CodeBuddy/WorkBuddy"
    echo -e "${GREEN}  ✓ 检测到CodeBuddy/WorkBuddy项目${NC}"
# 检测Windsurf项目
elif [ -d ".windsurf" ] || [ -f ".windsurfrules" ]; then
    PROJECT_TYPE="windsurf"
    PROJECT_TYPE_DESC="Windsurf"
    echo -e "${GREEN}  ✓ 检测到Windsurf项目${NC}"
# 检测Trae项目
elif [ -d ".trae" ] || [ -f ".trae/config.json" ]; then
    PROJECT_TYPE="trae"
    PROJECT_TYPE_DESC="Trae"
    echo -e "${GREEN}  ✓ 检测到Trae项目${NC}"
# 检测通义灵码项目
elif [ -d ".tongyi" ] || [ -f ".tongyi/config.json" ]; then
    PROJECT_TYPE="tongyi"
    PROJECT_TYPE_DESC="通义灵码"
    echo -e "${GREEN}  ✓ 检测到通义灵码项目${NC}"
# 检测百度Comate项目
elif [ -d ".comate" ] || [ -f ".comate/config.json" ]; then
    PROJECT_TYPE="comate"
    PROJECT_TYPE_DESC="百度Comate"
    echo -e "${GREEN}  ✓ 检测到百度Comate项目${NC}"
# 检测腾讯云AI代码助手项目
elif [ -d ".tencent-ai-code" ] || [ -f ".tencent-ai-code/config.json" ]; then
    PROJECT_TYPE="tencent"
    PROJECT_TYPE_DESC="腾讯云AI代码助手"
    echo -e "${GREEN}  ✓ 检测到腾讯云AI代码助手项目${NC}"
# 检测豆包MarsCode项目
elif [ -d ".marscode" ] || [ -f ".marscode/config.json" ]; then
    PROJECT_TYPE="marscode"
    PROJECT_TYPE_DESC="豆包MarsCode"
    echo -e "${GREEN}  ✓ 检测到豆包MarsCode项目${NC}"
# 检测CodeGeeX项目
elif [ -d ".codegeex" ] || [ -f ".codegeex/config.json" ]; then
    PROJECT_TYPE="codegeex"
    PROJECT_TYPE_DESC="CodeGeeX"
    echo -e "${GREEN}  ✓ 检测到CodeGeeX项目${NC}"
# 检测iFlyCode项目
elif [ -d ".iflycode" ] || [ -f ".iflycode/config.json" ]; then
    PROJECT_TYPE="iflycode"
    PROJECT_TYPE_DESC="讯飞iFlyCode"
    echo -e "${GREEN}  ✓ 检测到讯飞iFlyCode项目${NC}"
# 检测Node.js项目（无法确定IDE）
elif [ -f "package.json" ]; then
    echo -e "${YELLOW}  ⚠ 检测到Node.js项目，但未确定IDE类型${NC}"
    PROJECT_TYPE="nodejs"
    PROJECT_TYPE_DESC="Node.js项目"
else
    echo -e "${YELLOW}  ⚠ 未检测到已知IDE环境${NC}"
fi

echo ""

# 如果检测到已知IDE，询问是否使用对应的安装方式
if [ "$PROJECT_TYPE" != "unknown" ] && [ "$PROJECT_TYPE" != "nodejs" ]; then
    echo -e "${YELLOW}检测到${PROJECT_TYPE_DESC}项目，建议使用专用安装方式${NC}"
    echo -e "${YELLOW}是否使用${PROJECT_TYPE_DESC}安装方式？[Y/n]: ${NC}"
    read -p "" use_specific
    
    if [ "$use_specific" = "n" ] || [ "$use_specific" = "N" ]; then
        PROJECT_TYPE="prompt"
        PROJECT_TYPE_DESC="通用Prompt"
    fi
else
    # 未检测到已知IDE，询问用户使用的IDE
    echo -e "${BLUE}请选择或输入你使用的IDE：${NC}"
    echo ""
    echo "国内主流IDE："
    echo "  1) 码道IDE（CodeArts）"
    echo "  2) 通义灵码（阿里云）"
    echo "  3) 百度Comate"
    echo "  4) 腾讯云AI代码助手"
    echo "  5) 豆包MarsCode（字节跳动）"
    echo "  6) CodeGeeX（智谱）"
    echo "  7) 讯飞iFlyCode"
    echo ""
    echo "国际主流IDE："
    echo "  8) Cursor"
    echo "  9) VSCode + Copilot"
    echo "  10) Windsurf"
    echo "  11) CodeBuddy/WorkBuddy"
    echo ""
    echo "  12) 通用Prompt（适用任何AI平台）"
    echo "  13) 其他（手动输入IDE名称）"
    echo ""
    echo -e "${YELLOW}请输入选项 [1-13，默认12]: ${NC}"
    read -p "" choice
    
    case "$choice" in
        1) PROJECT_TYPE="codearts"; PROJECT_TYPE_DESC="码道IDE" ;;
        2) PROJECT_TYPE="tongyi"; PROJECT_TYPE_DESC="通义灵码" ;;
        3) PROJECT_TYPE="comate"; PROJECT_TYPE_DESC="百度Comate" ;;
        4) PROJECT_TYPE="tencent"; PROJECT_TYPE_DESC="腾讯云AI代码助手" ;;
        5) PROJECT_TYPE="marscode"; PROJECT_TYPE_DESC="豆包MarsCode" ;;
        6) PROJECT_TYPE="codegeex"; PROJECT_TYPE_DESC="CodeGeeX" ;;
        7) PROJECT_TYPE="iflycode"; PROJECT_TYPE_DESC="讯飞iFlyCode" ;;
        8) PROJECT_TYPE="cursor"; PROJECT_TYPE_DESC="Cursor IDE" ;;
        9) PROJECT_TYPE="vscode"; PROJECT_TYPE_DESC="VSCode + Copilot" ;;
        10) PROJECT_TYPE="windsurf"; PROJECT_TYPE_DESC="Windsurf" ;;
        11) PROJECT_TYPE="codebuddy"; PROJECT_TYPE_DESC="CodeBuddy/WorkBuddy" ;;
        13)
            read -p "请输入IDE名称: " custom_ide
            PROJECT_TYPE="custom"
            PROJECT_TYPE_DESC="$custom_ide"
            ;;
        *) PROJECT_TYPE="prompt"; PROJECT_TYPE_DESC="通用Prompt" ;;
    esac
fi

echo ""
echo -e "${GREEN}✓ 选择安装方式：${PROJECT_TYPE_DESC}${NC}"
echo ""

# 根据项目类型执行安装
case "$PROJECT_TYPE" in
    codearts)
        # 码道IDE安装（参考install-codearts.sh）
        echo -e "${BLUE}[安装] 码道IDE模式${NC}"
        echo ""
        
        # 创建目录结构
        echo -e "${BLUE}[1/4] 创建.codeartsdoer目录结构...${NC}"
        mkdir -p "$TARGET_DIR/.codeartsdoer/agents"
        mkdir -p "$TARGET_DIR/.codeartsdoer/skills"
        echo -e "${GREEN}  ✓ 目录结构已创建${NC}"
        
        # 复制AGENTS.md
        echo -e "${BLUE}[2/4] 复制AGENTS.md...${NC}"
        if [ -f "$SOURCE_DIR/AGENTS.md" ]; then
            cp "$SOURCE_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
            echo -e "${GREEN}  ✓ AGENTS.md 已复制${NC}"
        else
            echo -e "${RED}  ✗ AGENTS.md不存在${NC}"
            exit 1
        fi
        
        # 生成opc-zhinao.json
        echo -e "${BLUE}[3/4] 生成opc-zhinao.json...${NC}"
        cat > "$TARGET_DIR/.codeartsdoer/agents/opc-zhinao.json" << 'EOF'
{
  "name": "OPC智脑",
  "description": "一人公司全生命周期创业诊断专家，基于五阶段模型提供精准诊断与可执行规划",
  "instructions": "AGENTS.md",
  "model": "glm-5.1",
  "skills": [
    "skill1-idea-feasibility",
    "skill2-mvp-design",
    "skill3-opc-compliance",
    "skill4-seed-coldstart",
    "skill5-scale-growth",
    "feasibility-scoring",
    "report-export",
    "user-feedback"
  ]
}
EOF
        echo -e "${GREEN}  ✓ opc-zhinao.json 已生成${NC}"
        
        # 复制skills
        echo -e "${BLUE}[4/4] 复制所有skills...${NC}"
        SKILLS_SOURCE="$SOURCE_DIR/skills"
        
        if [ ! -d "$SKILLS_SOURCE" ]; then
            echo -e "${RED}  ✗ 未找到skills目录${NC}"
            exit 1
        fi
        
        SKILLS_TARGET="$TARGET_DIR/.codeartsdoer/skills"
        SKILL_COUNT=0
        
        for skill_dir in "$SKILLS_SOURCE"/*/; do
            if [ -d "$skill_dir" ]; then
                skill_name=$(basename "$skill_dir")
                
                if [ -f "$skill_dir/SKILL.md" ]; then
                    mkdir -p "$SKILLS_TARGET/$skill_name"
                    cp "$skill_dir/SKILL.md" "$SKILLS_TARGET/$skill_name/"
                    echo -e "${GREEN}  ✓ $skill_name/SKILL.md${NC}"
                    ((SKILL_COUNT++))
                fi
            fi
        done
        
        echo -e "${GREEN}  ✓ 共复制 $SKILL_COUNT 个skills${NC}"
        
        # 显示安装结果
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}  ✓ 码道IDE安装完成！${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo -e "${BLUE}已安装文件：${NC}"
        echo "  ├── AGENTS.md"
        echo "  └── .codeartsdoer/"
        echo "      ├── agents/"
        echo "      │   └── opc-zhinao.json"
        echo "      └── skills/ ($SKILL_COUNT个)"
        ;;
    
    cursor)
        # Cursor IDE安装
        echo -e "${BLUE}[安装] Cursor IDE模式${NC}"
        echo ""
        
        # 创建目录结构
        echo -e "${BLUE}[1/4] 创建目录结构...${NC}"
        mkdir -p "$TARGET_DIR/skills"
        echo -e "${GREEN}  ✓ 目录结构已创建${NC}"
        
        # 复制AGENTS.md
        echo -e "${BLUE}[2/4] 复制AGENTS.md...${NC}"
        if [ -f "$SOURCE_DIR/AGENTS.md" ]; then
            cp "$SOURCE_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
            echo -e "${GREEN}  ✓ AGENTS.md 已复制${NC}"
        else
            echo -e "${RED}  ✗ AGENTS.md不存在${NC}"
            exit 1
        fi
        
        # 生成.cursorrules
        echo -e "${BLUE}[3/4] 生成.cursorrules...${NC}"
        # Cursor使用.cursorrules文件，内容基于AGENTS.md
        echo "# OPC智脑 - Cursor IDE配置" > "$TARGET_DIR/.cursorrules"
        echo "" >> "$TARGET_DIR/.cursorrules"
        cat "$TARGET_DIR/AGENTS.md" >> "$TARGET_DIR/.cursorrules"
        echo -e "${GREEN}  ✓ .cursorrules 已生成${NC}"
        
        # 复制skills
        echo -e "${BLUE}[4/4] 复制所有skills...${NC}"
        SKILLS_SOURCE="$SOURCE_DIR/skills"
        
        if [ ! -d "$SKILLS_SOURCE" ]; then
            echo -e "${RED}  ✗ 未找到skills目录${NC}"
            exit 1
        fi
        
        SKILLS_TARGET="$TARGET_DIR/skills"
        SKILL_COUNT=0
        
        for skill_dir in "$SKILLS_SOURCE"/*/; do
            if [ -d "$skill_dir" ]; then
                skill_name=$(basename "$skill_dir")
                
                if [ -f "$skill_dir/SKILL.md" ]; then
                    mkdir -p "$SKILLS_TARGET/$skill_name"
                    cp "$skill_dir/SKILL.md" "$SKILLS_TARGET/$skill_name/"
                    echo -e "${GREEN}  ✓ $skill_name/SKILL.md${NC}"
                    ((SKILL_COUNT++))
                fi
            fi
        done
        
        echo -e "${GREEN}  ✓ 共复制 $SKILL_COUNT 个skills${NC}"
        
        # 显示安装结果
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}  ✓ Cursor IDE安装完成！${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo -e "${BLUE}已安装文件：${NC}"
        echo "  ├── AGENTS.md"
        echo "  ├── .cursorrules"
        echo "  └── skills/ ($SKILL_COUNT个)"
        echo ""
        echo -e "${YELLOW}⚠️ 提示：${NC}"
        echo -e "${YELLOW}   skills目录位于项目根目录${NC}"
        echo -e "${YELLOW}   如Cursor有特定的skills路径，请手动移动${NC}"
        ;;
    
    vscode)
        # VSCode + Copilot安装
        echo -e "${BLUE}[安装] VSCode + Copilot模式${NC}"
        echo ""
        
        # 创建目录结构
        echo -e "${BLUE}[1/4] 创建目录结构...${NC}"
        mkdir -p "$TARGET_DIR/.github"
        mkdir -p "$TARGET_DIR/skills"
        echo -e "${GREEN}  ✓ 目录结构已创建${NC}"
        
        # 复制AGENTS.md
        echo -e "${BLUE}[2/4] 复制AGENTS.md...${NC}"
        if [ -f "$SOURCE_DIR/AGENTS.md" ]; then
            cp "$SOURCE_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
            echo -e "${GREEN}  ✓ AGENTS.md 已复制${NC}"
        else
            echo -e "${RED}  ✗ AGENTS.md不存在${NC}"
            exit 1
        fi
        
        # 生成copilot-instructions.md
        echo -e "${BLUE}[3/4] 生成copilot-instructions.md...${NC}"
        cp "$TARGET_DIR/AGENTS.md" "$TARGET_DIR/.github/copilot-instructions.md"
        echo -e "${GREEN}  ✓ copilot-instructions.md 已生成${NC}"
        
        # 复制skills
        echo -e "${BLUE}[4/4] 复制所有skills...${NC}"
        SKILLS_SOURCE="$SOURCE_DIR/skills"
        
        if [ ! -d "$SKILLS_SOURCE" ]; then
            echo -e "${RED}  ✗ 未找到skills目录${NC}"
            exit 1
        fi
        
        SKILLS_TARGET="$TARGET_DIR/skills"
        SKILL_COUNT=0
        
        for skill_dir in "$SKILLS_SOURCE"/*/; do
            if [ -d "$skill_dir" ]; then
                skill_name=$(basename "$skill_dir")
                
                if [ -f "$skill_dir/SKILL.md" ]; then
                    mkdir -p "$SKILLS_TARGET/$skill_name"
                    cp "$skill_dir/SKILL.md" "$SKILLS_TARGET/$skill_name/"
                    echo -e "${GREEN}  ✓ $skill_name/SKILL.md${NC}"
                    ((SKILL_COUNT++))
                fi
            fi
        done
        
        echo -e "${GREEN}  ✓ 共复制 $SKILL_COUNT 个skills${NC}"
        
        # 显示安装结果
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}  ✓ VSCode + Copilot安装完成！${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo -e "${BLUE}已安装文件：${NC}"
        echo "  ├── AGENTS.md"
        echo "  ├── .github/"
        echo "  │   └── copilot-instructions.md"
        echo "  └── skills/ ($SKILL_COUNT个)"
        echo ""
        echo -e "${YELLOW}⚠️ 提示：${NC}"
        echo -e "${YELLOW}   skills目录位于项目根目录${NC}"
        echo -e "${YELLOW}   如VSCode有特定的skills路径，请手动移动${NC}"
        ;;
    
    prompt)
        # 通用Prompt安装
        echo -e "${BLUE}[安装] 通用Prompt模式${NC}"
        echo ""
        
        # 创建目录结构
        echo -e "${BLUE}[1/4] 创建目录结构...${NC}"
        mkdir -p "$TARGET_DIR/skills"
        echo -e "${GREEN}  ✓ 目录结构已创建${NC}"
        
        # 复制AGENTS.md
        echo -e "${BLUE}[2/4] 复制AGENTS.md...${NC}"
        if [ -f "$SOURCE_DIR/AGENTS.md" ]; then
            cp "$SOURCE_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
            echo -e "${GREEN}  ✓ AGENTS.md 已复制${NC}"
        else
            echo -e "${RED}  ✗ AGENTS.md不存在${NC}"
            exit 1
        fi
        
        # 生成opc-zhinao-prompt.md
        echo -e "${BLUE}[3/4] 生成opc-zhinao-prompt.md...${NC}"
        
        if [ -f "$SOURCE_DIR/src/prompts/system-persona.md" ]; then
            cat "$SOURCE_DIR/src/prompts/system-persona.md" > "$TARGET_DIR/opc-zhinao-prompt.md"
            echo "" >> "$TARGET_DIR/opc-zhinao-prompt.md"
            echo "---" >> "$TARGET_DIR/opc-zhinao-prompt.md"
            echo "" >> "$TARGET_DIR/opc-zhinao-prompt.md"
            
            if [ -f "$SOURCE_DIR/src/prompts/core-hub.md" ]; then
                cat "$SOURCE_DIR/src/prompts/core-hub.md" >> "$TARGET_DIR/opc-zhinao-prompt.md"
            fi
            
            echo -e "${GREEN}  ✓ opc-zhinao-prompt.md 已生成${NC}"
        else
            # 如果prompts文件不存在，使用AGENTS.md
            if [ -f "$SOURCE_DIR/AGENTS.md" ]; then
                cp "$SOURCE_DIR/AGENTS.md" "$TARGET_DIR/opc-zhinao-prompt.md"
                echo -e "${GREEN}  ✓ opc-zhinao-prompt.md 已生成（基于AGENTS.md）${NC}"
            else
                echo -e "${RED}  ✗ 找不到Prompt源文件${NC}"
                exit 1
            fi
        fi
        
        # 复制skills（通用模式也需要skills）
        echo -e "${BLUE}[4/4] 复制所有skills...${NC}"
        SKILLS_SOURCE="$SOURCE_DIR/skills"
        
        if [ ! -d "$SKILLS_SOURCE" ]; then
            echo -e "${RED}  ✗ 未找到skills目录${NC}"
            exit 1
        fi
        
        SKILLS_TARGET="$TARGET_DIR/skills"
        SKILL_COUNT=0
        
        for skill_dir in "$SKILLS_SOURCE"/*/; do
            if [ -d "$skill_dir" ]; then
                skill_name=$(basename "$skill_dir")
                
                if [ -f "$skill_dir/SKILL.md" ]; then
                    mkdir -p "$SKILLS_TARGET/$skill_name"
                    cp "$skill_dir/SKILL.md" "$SKILLS_TARGET/$skill_name/"
                    echo -e "${GREEN}  ✓ $skill_name/SKILL.md${NC}"
                    ((SKILL_COUNT++))
                fi
            fi
        done
        
        echo -e "${GREEN}  ✓ 共复制 $SKILL_COUNT 个skills${NC}"
        
        # 显示安装结果
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}  ✓ 通用Prompt安装完成！${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo -e "${BLUE}已安装文件：${NC}"
        echo "  ├── AGENTS.md"
        echo "  ├── opc-zhinao-prompt.md"
        echo "  └── skills/ ($SKILL_COUNT个)"
        echo ""
        echo -e "${BLUE}使用方式：${NC}"
        echo ""
        echo "  **OpenAI / Claude / 文心一言 / 通义千问等：**"
        echo "  1. 打开opc-zhinao-prompt.md"
        echo "  2. 复制全部内容"
        echo "  3. 粘贴到AI对话的System Prompt或开头"
        echo ""
        echo "  **Coze / Dify / FastGPT等：**"
        echo "  1. 创建新的Bot/应用"
        echo "  2. 将opc-zhinao-prompt.md内容作为System Prompt"
        echo "  3. 配置触发关键词"
        echo ""
        echo -e "${YELLOW}⚠️ 提示：${NC}"
        echo -e "${YELLOW}   skills目录位于项目根目录${NC}"
        echo -e "${YELLOW}   可根据实际IDE环境调整位置${NC}"
        ;;
    
    codebuddy)
        # CodeBuddy/WorkBuddy安装
        echo -e "${BLUE}[安装] CodeBuddy/WorkBuddy模式${NC}"
        echo ""
        
        echo -e "${BLUE}[1/4] 创建.codebuddy目录结构...${NC}"
        mkdir -p "$TARGET_DIR/.codebuddy"
        mkdir -p "$TARGET_DIR/.codebuddy/skills"
        echo -e "${GREEN}  ✓ 目录结构已创建${NC}"
        
        echo -e "${BLUE}[2/4] 复制AGENTS.md...${NC}"
        if [ -f "$SOURCE_DIR/AGENTS.md" ]; then
            cp "$SOURCE_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
            echo -e "${GREEN}  ✓ AGENTS.md 已复制${NC}"
        else
            echo -e "${RED}  ✗ AGENTS.md不存在${NC}"
            exit 1
        fi
        
        echo -e "${BLUE}[3/4] 生成skills-registry.json...${NC}"
        SKILLS_JSON="["
        first=true
        for skill_dir in "$SOURCE_DIR/skills"/*/; do
            if [ -d "$skill_dir" ] && [ -f "$skill_dir/SKILL.md" ]; then
                skill_name=$(basename "$skill_dir")
                if [ "$first" = true ]; then
                    first=false
                else
                    SKILLS_JSON="$SKILLS_JSON,"
                fi
                SKILLS_JSON="$SKILLS_JSON\"$skill_name\""
            fi
        done
        SKILLS_JSON="$SKILLS_JSON]"
        
        cat > "$TARGET_DIR/.codebuddy/skills-registry.json" << EOF
{
  "name": "opc-skills",
  "version": "1.2.0",
  "ide": "codebuddy",
  "skills": $SKILLS_JSON
}
EOF
        echo -e "${GREEN}  ✓ skills-registry.json 已生成${NC}"
        
        echo -e "${BLUE}[4/4] 复制所有skills...${NC}"
        SKILLS_SOURCE="$SOURCE_DIR/skills"
        SKILLS_TARGET="$TARGET_DIR/.codebuddy/skills"
        SKILL_COUNT=0
        
        for skill_dir in "$SKILLS_SOURCE"/*/; do
            if [ -d "$skill_dir" ]; then
                skill_name=$(basename "$skill_dir")
                if [ -f "$skill_dir/SKILL.md" ]; then
                    mkdir -p "$SKILLS_TARGET/$skill_name"
                    cp "$skill_dir/SKILL.md" "$SKILLS_TARGET/$skill_name/"
                    echo -e "${GREEN}  ✓ $skill_name/SKILL.md${NC}"
                    ((SKILL_COUNT++))
                fi
            fi
        done
        
        echo -e "${GREEN}  ✓ 共复制 $SKILL_COUNT 个skills${NC}"
        
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}  ✓ CodeBuddy/WorkBuddy安装完成！${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo -e "${BLUE}已安装文件：${NC}"
        echo "  ├── AGENTS.md"
        echo "  └── .codebuddy/"
        echo "      ├── skills-registry.json"
        echo "      └── skills/ ($SKILL_COUNT个)"
        ;;
    
    tongyi|comate|tencent|marscode|codegeex|iflycode)
        # 国内主流IDE安装（通义灵码、百度Comate、腾讯云AI代码助手、豆包MarsCode、CodeGeeX、讯飞iFlyCode）
        echo -e "${BLUE}[安装] $PROJECT_TYPE_DESC模式${NC}"
        echo ""
        
        echo -e "${BLUE}[1/3] 创建目录结构...${NC}"
        mkdir -p "$TARGET_DIR/skills"
        echo -e "${GREEN}  ✓ 目录结构已创建${NC}"
        
        echo -e "${BLUE}[2/3] 复制AGENTS.md...${NC}"
        if [ -f "$SOURCE_DIR/AGENTS.md" ]; then
            cp "$SOURCE_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
            echo -e "${GREEN}  ✓ AGENTS.md 已复制${NC}"
        else
            echo -e "${RED}  ✗ AGENTS.md不存在${NC}"
            exit 1
        fi
        
        echo -e "${BLUE}[3/3] 复制所有skills...${NC}"
        SKILLS_SOURCE="$SOURCE_DIR/skills"
        SKILLS_TARGET="$TARGET_DIR/skills"
        SKILL_COUNT=0
        
        for skill_dir in "$SKILLS_SOURCE"/*/; do
            if [ -d "$skill_dir" ]; then
                skill_name=$(basename "$skill_dir")
                if [ -f "$skill_dir/SKILL.md" ]; then
                    mkdir -p "$SKILLS_TARGET/$skill_name"
                    cp "$skill_dir/SKILL.md" "$SKILLS_TARGET/$skill_name/"
                    echo -e "${GREEN}  ✓ $skill_name/SKILL.md${NC}"
                    ((SKILL_COUNT++))
                fi
            fi
        done
        
        echo -e "${GREEN}  ✓ 共复制 $SKILL_COUNT 个skills${NC}"
        
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}  ✓ $PROJECT_TYPE_DESC安装完成！${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo -e "${BLUE}已安装文件：${NC}"
        echo "  ├── AGENTS.md"
        echo "  └── skills/ ($SKILL_COUNT个)"
        echo ""
        echo -e "${YELLOW}⚠️ 提示：${NC}"
        echo -e "${YELLOW}   1. skills目录位于项目根目录${NC}"
        echo -e "${YELLOW}   2. 请查阅 $PROJECT_TYPE_DESC 文档确认Skills配置路径${NC}"
        echo -e "${YELLOW}   3. 如需调整路径，请手动移动skills目录${NC}"
        ;;
    
    windsurf|trae|custom)
        # Windsurf/Trae/自定义IDE安装（通用方式）
        echo -e "${BLUE}[安装] $PROJECT_TYPE_DESC模式${NC}"
        echo ""
        
        echo -e "${BLUE}[1/3] 创建目录结构...${NC}"
        mkdir -p "$TARGET_DIR/skills"
        echo -e "${GREEN}  ✓ 目录结构已创建${NC}"
        
        echo -e "${BLUE}[2/3] 复制AGENTS.md...${NC}"
        if [ -f "$SOURCE_DIR/AGENTS.md" ]; then
            cp "$SOURCE_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
            echo -e "${GREEN}  ✓ AGENTS.md 已复制${NC}"
        else
            echo -e "${RED}  ✗ AGENTS.md不存在${NC}"
            exit 1
        fi
        
        echo -e "${BLUE}[3/3] 复制所有skills...${NC}"
        SKILLS_SOURCE="$SOURCE_DIR/skills"
        SKILLS_TARGET="$TARGET_DIR/skills"
        SKILL_COUNT=0
        
        for skill_dir in "$SKILLS_SOURCE"/*/; do
            if [ -d "$skill_dir" ]; then
                skill_name=$(basename "$skill_dir")
                if [ -f "$skill_dir/SKILL.md" ]; then
                    mkdir -p "$SKILLS_TARGET/$skill_name"
                    cp "$skill_dir/SKILL.md" "$SKILLS_TARGET/$skill_name/"
                    echo -e "${GREEN}  ✓ $skill_name/SKILL.md${NC}"
                    ((SKILL_COUNT++))
                fi
            fi
        done
        
        echo -e "${GREEN}  ✓ 共复制 $SKILL_COUNT 个skills${NC}"
        
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}  ✓ $PROJECT_TYPE_DESC安装完成！${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo -e "${BLUE}已安装文件：${NC}"
        echo "  ├── AGENTS.md"
        echo "  └── skills/ ($SKILL_COUNT个)"
        echo ""
        echo -e "${YELLOW}⚠️ 提示：${NC}"
        echo -e "${YELLOW}   1. skills目录位于项目根目录${NC}"
        echo -e "${YELLOW}   2. 请查阅 $PROJECT_TYPE_DESC 文档确认Skills配置路径${NC}"
        echo -e "${YELLOW}   3. 如需调整路径，请手动移动skills目录${NC}"
        ;;
esac

echo ""
echo -e "${BLUE}下一步：${NC}"
echo "  1. 打开项目：$TARGET_DIR"
echo "  2. 开始使用OPC智脑进行创业诊断"
echo ""

# 清理opc-skills目录
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  清理安装源文件${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

CURRENT_DIR="$(pwd)"

if [ -f "$SOURCE_DIR/install-prompt.sh" ]; then
    echo -e "${YELLOW}检测到opc-skills目录：$SOURCE_DIR${NC}"
    echo -e "${YELLOW}是否删除opc-skills目录以保持项目清爽？[y/N]: ${NC}"
    read -p "" confirm_delete
    
    if [ "$confirm_delete" = "y" ] || [ "$confirm_delete" = "Y" ]; then
        if [ "$SOURCE_DIR" != "$CURRENT_DIR" ]; then
            rm -rf "$SOURCE_DIR"
            echo -e "${GREEN}✓ opc-skills目录已删除${NC}"
        else
            echo -e "${YELLOW}⚠ 当前在opc-skills目录内，请手动删除${NC}"
        fi
    fi
fi

#!/bin/bash

# OPC智脑 - 码道IDE一键安装脚本
# 作者：李屹镒（公众号：科技新潮。视频号：小李君与AI）
# 用法：bash install-codearts.sh [目标项目路径]
# 说明：自动生成AGENTS.md和opc-zhinao.json，复制skills到目标项目
#
# ⚠️ 重要约束：
# 本脚本仅适用于【码道CodeArts IDE】
# 其他IDE请优先使用对应的安装脚本：
#   - Cursor IDE：install-cursor.sh（如不存在，可参考本脚本适配）
#   - VSCode + Copilot：install-vscode.sh（如不存在，可参考本脚本适配）
#   - 通用Prompt：install-prompt.sh（适用于任何AI平台）
# 如其他IDE的脚本不存在，可参考本脚本进行适配

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取脚本所在目录（opc-skills源目录）
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 目标项目路径（默认为当前目录）
TARGET_DIR="${1:-.}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  OPC智脑 - 码道IDE一键安装${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}⚠️ 本脚本仅适用于【码道CodeArts IDE】${NC}"
echo -e "${YELLOW}   其他IDE请使用对应的安装脚本或参考本脚本适配${NC}"
echo ""

# 检查目标目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${YELLOW}目标目录不存在，正在创建：$TARGET_DIR${NC}"
    mkdir -p "$TARGET_DIR"
fi

cd "$TARGET_DIR"
TARGET_DIR="$(pwd)"

echo -e "${GREEN}✓ 源目录：$SOURCE_DIR${NC}"
echo -e "${GREEN}✓ 目标目录：$TARGET_DIR${NC}"
echo ""

# 步骤1：创建.codeartsdoer目录结构
echo -e "${BLUE}[1/5] 创建.codeartsdoer目录结构...${NC}"
mkdir -p "$TARGET_DIR/.codeartsdoer/agents"
mkdir -p "$TARGET_DIR/.codeartsdoer/skills"
echo -e "${GREEN}  ✓ 目录结构已创建${NC}"

# 步骤2：复制AGENTS.md
echo -e "${BLUE}[2/4] 复制AGENTS.md...${NC}"
if [ -f "$SOURCE_DIR/AGENTS.md" ]; then
    cp "$SOURCE_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
    echo -e "${GREEN}  ✓ AGENTS.md 已复制${NC}"
else
    echo -e "${YELLOW}  ⚠ AGENTS.md不存在，跳过${NC}"
fi

# 步骤3：生成opc-zhinao.json
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

# 步骤4：复制所有skills（只复制SKILL.md）
echo -e "${BLUE}[4/4] 复制所有skills...${NC}"

# 使用opc-skills/skills/目录
SKILLS_SOURCE="$SOURCE_DIR/skills"

if [ ! -d "$SKILLS_SOURCE" ]; then
    echo -e "${RED}  ✗ 未找到skills目录：$SKILLS_SOURCE${NC}"
    echo -e "${RED}  请确保skills目录存在于opc-skills下${NC}"
    exit 1
fi

SKILL_NAMES=()
SKILLS_TARGET="$TARGET_DIR/.codeartsdoer/skills"
SKILL_COUNT=0

for skill_dir in "$SKILLS_SOURCE"/*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        
        # 检查SKILL.md是否存在
        if [ -f "$skill_dir/SKILL.md" ]; then
            mkdir -p "$SKILLS_TARGET/$skill_name"
            cp "$skill_dir/SKILL.md" "$SKILLS_TARGET/$skill_name/"
            SKILL_NAMES+=("$skill_name")
            echo -e "${GREEN}  ✓ $skill_name/SKILL.md 已复制${NC}"
            ((SKILL_COUNT++))
        else
            echo -e "${YELLOW}  ⚠ $skill_name/SKILL.md 不存在，跳过${NC}"
        fi
    fi
done

if [ $SKILL_COUNT -gt 0 ]; then
    echo -e "${GREEN}  ✓ 共复制 $SKILL_COUNT 个skills${NC}"
else
    echo -e "${RED}  ✗ 没有找到任何SKILL.md文件${NC}"
    exit 1
fi

# 完成
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✓ OPC智脑安装完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}已安装文件：${NC}"
echo "  ├── AGENTS.md"
echo "  └── .codeartsdoer/"
echo "      ├── agents/"
echo "      │   └── opc-zhinao.json"
echo "      └── skills/"
echo "          ├── skill1-idea-feasibility/SKILL.md"
echo "          ├── skill2-mvp-design/SKILL.md"
echo "          ├── skill3-opc-compliance/SKILL.md"
echo "          ├── skill4-seed-coldstart/SKILL.md"
echo "          ├── skill5-scale-growth/SKILL.md"
echo "          ├── feasibility-scoring/SKILL.md"
echo "          ├── report-export/SKILL.md"
echo "          └── user-feedback/SKILL.md"
echo ""
echo -e "${BLUE}下一步：${NC}"
echo "  1. 在码道IDE中打开项目：$TARGET_DIR"
echo "  2. IDE会自动识别opc-zhinao.json和AGENTS.md"
echo "  3. 输入创业Idea开始诊断"
echo ""
echo -e "${BLUE}验证安装：${NC}"
echo "  运行以下命令检查文件是否完整："
echo "  cat $TARGET_DIR/.codeartsdoer/skills/ProjectSkillStatus.txt"

# 清理opc-skills目录（保持用户目录清爽）
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  清理安装源文件${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查是否在opc-skills目录内
CURRENT_DIR="$(pwd)"
OPC_SKILLS_DIR=""

# 查找opc-skills目录
if [ -f "$SOURCE_DIR/install-codearts.sh" ]; then
    OPC_SKILLS_DIR="$SOURCE_DIR"
fi

if [ -n "$OPC_SKILLS_DIR" ] && [ -d "$OPC_SKILLS_DIR" ]; then
    echo -e "${YELLOW}检测到opc-skills目录：$OPC_SKILLS_DIR${NC}"
    echo -e "${YELLOW}为了保持项目目录清爽，是否删除opc-skills目录？${NC}"
    echo ""
    echo "  删除后只保留已安装的文件，opc-skills源文件将被移除。"
    echo "  如需重新安装，请重新下载opc-skills。"
    echo ""
    read -p "是否删除？[y/N]: " confirm_delete
    
    if [ "$confirm_delete" = "y" ] || [ "$confirm_delete" = "Y" ]; then
        # 确保不删除当前工作目录
        if [ "$OPC_SKILLS_DIR" != "$CURRENT_DIR" ]; then
            rm -rf "$OPC_SKILLS_DIR"
            echo ""
            echo -e "${GREEN}✓ opc-skills目录已删除${NC}"
            echo -e "${GREEN}✓ 项目目录保持清爽${NC}"
        else
            echo ""
            echo -e "${YELLOW}⚠ 当前在opc-skills目录内，跳过删除${NC}"
            echo -e "${YELLOW}  请手动删除：rm -rf $OPC_SKILLS_DIR${NC}"
        fi
    else
        echo ""
        echo -e "${BLUE}保留opc-skills目录${NC}"
        echo -e "${BLUE}如需手动删除：rm -rf $OPC_SKILLS_DIR${NC}"
    fi
fi

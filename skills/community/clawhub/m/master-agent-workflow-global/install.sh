#!/bin/bash
# master-agent-workflow-global 安装脚本
# 版本: 2.0.0
# 作者: 小龙

set -e

echo "========================================="
echo "  安装 master-agent-workflow-global 技能"
echo "========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查操作系统
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS="windows"
else
    OS="unknown"
fi

echo -e "${GREEN}✓ 检测到操作系统: $OS${NC}"

# 检查OpenClaw安装
if ! command -v openclaw &> /dev/null; then
    echo -e "${RED}✗ 未找到OpenClaw，请先安装OpenClaw${NC}"
    exit 1
fi

OPENCLAW_VERSION=$(openclaw --version 2>/dev/null || echo "未知")
echo -e "${GREEN}✓ 检测到OpenClaw版本: $OPENCLAW_VERSION${NC}"

# 确定安装目录
if [ "$OS" = "windows" ]; then
    # Windows路径
    if [ -n "$USERPROFILE" ]; then
        INSTALL_DIR="$USERPROFILE/.openclaw/global-skills/master-agent-workflow"
    else
        INSTALL_DIR="$HOME/.openclaw/global-skills/master-agent-workflow"
    fi
else
    # Linux/Mac路径
    INSTALL_DIR="$HOME/.openclaw/global-skills/master-agent-workflow"
fi

echo -e "${YELLOW}安装目录: $INSTALL_DIR${NC}"

# 创建安装目录
mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/templates"
mkdir -p "$INSTALL_DIR/examples"
mkdir -p "$INSTALL_DIR/scripts"

# 复制文件
echo -e "${GREEN}正在复制技能文件...${NC}"

# 复制核心文件
cp skill.json "$INSTALL_DIR/"
cp SKILL.md "$INSTALL_DIR/" 2>/dev/null || echo "SKILL.md 不存在，跳过"

# 复制配置文件
if [ -f "config-template.json" ]; then
    cp config-template.json "$INSTALL_DIR/"
fi

# 复制模板
if [ -d "templates" ]; then
    cp -r templates/* "$INSTALL_DIR/templates/"
fi

# 复制示例
if [ -d "examples" ]; then
    cp -r examples/* "$INSTALL_DIR/examples/"
fi

# 复制脚本
if [ -d "scripts" ]; then
    cp -r scripts/* "$INSTALL_DIR/scripts/"
fi

# 创建配置文件
CONFIG_FILE="$INSTALL_DIR/maw-config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    cat > "$CONFIG_FILE" << EOF
{
  "version": "2.0.0",
  "installed_at": "$(date -Iseconds)",
  "defaults": {
    "max_workers": 5,
    "timeout_hours": 3,
    "worker_timeout_minutes": 30,
    "stuck_threshold_minutes": 15,
    "fail_threshold": 10,
    "auto_cleanup": true,
    "report_channel": "feishu"
  },
  "templates": {
    "file_processing": {
      "name": "文件处理",
      "description": "批量文件处理模板"
    },
    "api_calling": {
      "name": "API调用", 
      "description": "批量API调用模板"
    },
    "data_processing": {
      "name": "数据处理",
      "description": "批量数据处理模板"
    }
  }
}
EOF
    echo -e "${GREEN}✓ 创建默认配置文件${NC}"
fi

# 更新OpenClaw配置
echo -e "${YELLOW}正在更新OpenClaw配置...${NC}"

if [ "$OS" = "windows" ]; then
    # Windows配置更新
    OPENCLAW_CONFIG="$USERPROFILE/.openclaw/config.json"
    if [ -f "$OPENCLAW_CONFIG" ]; then
        # 使用PowerShell更新配置
        powershell -Command "
            \$config = Get-Content '$OPENCLAW_CONFIG' | ConvertFrom-Json
            if (-not \$config.skills) { \$config | Add-Member -NotePropertyName 'skills' -NotePropertyValue @() }
            if ('master-agent-workflow-global' -notin \$config.skills) {
                \$config.skills += 'master-agent-workflow-global'
                \$config | ConvertTo-Json -Depth 10 | Set-Content '$OPENCLAW_CONFIG'
                Write-Host '✓ 更新OpenClaw配置' -ForegroundColor Green
            } else {
                Write-Host '✓ 技能已在配置中' -ForegroundColor Yellow
            }
        "
    else
        echo -e "${YELLOW}⚠ 未找到OpenClaw配置文件，跳过配置更新${NC}"
    fi
else
    # Linux/Mac配置更新
    OPENCLAW_CONFIG="$HOME/.openclaw/config.json"
    if [ -f "$OPENCLAW_CONFIG" ]; then
        if command -v jq &> /dev/null; then
            # 使用jq更新配置
            if ! jq -e '.skills' "$OPENCLAW_CONFIG" > /dev/null 2>&1; then
                jq '. + {skills: []}' "$OPENCLAW_CONFIG" > "$OPENCLAW_CONFIG.tmp"
                mv "$OPENCLAW_CONFIG.tmp" "$OPENCLAW_CONFIG"
            fi
            
            if ! jq -e '.skills | index("master-agent-workflow-global")' "$OPENCLAW_CONFIG" > /dev/null 2>&1; then
                jq '.skills += ["master-agent-workflow-global"]' "$OPENCLAW_CONFIG" > "$OPENCLAW_CONFIG.tmp"
                mv "$OPENCLAW_CONFIG.tmp" "$OPENCLAW_CONFIG"
                echo -e "${GREEN}✓ 更新OpenClaw配置${NC}"
            else
                echo -e "${YELLOW}✓ 技能已在配置中${NC}"
            fi
        else
            echo -e "${YELLOW}⚠ 未找到jq命令，跳过JSON配置更新${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ 未找到OpenClaw配置文件，跳过配置更新${NC}"
    fi
fi

# 创建快捷命令
echo -e "${YELLOW}创建快捷命令...${NC}"

if [ "$OS" = "windows" ]; then
    # Windows创建批处理文件
    BATCH_FILE="$USERPROFILE/.openclaw/scripts/maw.bat"
    mkdir -p "$(dirname "$BATCH_FILE")"
    
    cat > "$BATCH_FILE" << 'EOF'
@echo off
REM master-agent-workflow-global 快捷命令
echo 使用 master-agent-workflow-global %*
EOF
    chmod +x "$BATCH_FILE"
    
    # 添加到PATH（可选）
    echo -e "${YELLOW}如需添加到PATH，请手动添加: $(dirname "$BATCH_FILE")${NC}"
    
else
    # Linux/Mac创建shell脚本
    SHELL_FILE="$HOME/.openclaw/scripts/maw.sh"
    mkdir -p "$(dirname "$SHELL_FILE")"
    
    cat > "$SHELL_FILE" << 'EOF'
#!/bin/bash
# master-agent-workflow-global 快捷命令
echo "使用 master-agent-workflow-global $*"
EOF
    chmod +x "$SHELL_FILE"
    
    # 创建符号链接
    if [ -d "$HOME/bin" ]; then
        ln -sf "$SHELL_FILE" "$HOME/bin/maw"
        echo -e "${GREEN}✓ 创建符号链接到 ~/bin/maw${NC}"
    fi
    
    # 更新bashrc/zshrc
    SHELL_RC="$HOME/.bashrc"
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi
    
    if ! grep -q "master-agent-workflow" "$SHELL_RC" 2>/dev/null; then
        echo "" >> "$SHELL_RC"
        echo "# master-agent-workflow-global 快捷命令" >> "$SHELL_RC"
        echo "alias maw='使用 master-agent-workflow-global'" >> "$SHELL_RC"
        echo "alias maw-list='查看 master-agent-workflow-global 模板'" >> "$SHELL_RC"
        echo "export MAW_HOME='$INSTALL_DIR'" >> "$SHELL_RC"
        echo -e "${GREEN}✓ 更新shell配置文件${NC}"
    fi
fi

# 创建迁移工具
MIGRATION_SCRIPT="$INSTALL_DIR/scripts/migrate.sh"
cat > "$MIGRATION_SCRIPT" << 'EOF'
#!/bin/bash
# master-agent-workflow 迁移工具

set -e

ACTION="$1"
SOURCE="$2"
TARGET="$3"

case "$ACTION" in
    export)
        echo "导出配置..."
        # 导出逻辑
        ;;
    import)
        echo "导入配置..."
        # 导入逻辑
        ;;
    *)
        echo "用法: migrate.sh [export|import] [source] [target]"
        exit 1
        ;;
esac
EOF
chmod +x "$MIGRATION_SCRIPT"

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  安装完成！${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo -e "${YELLOW}技能信息:${NC}"
echo -e "  名称: master-agent-workflow-global"
echo -e "  版本: 2.0.0"
echo -e "  位置: $INSTALL_DIR"
echo ""
echo -e "${YELLOW}使用方法:${NC}"
echo -e "  1. 直接使用: '使用 master-agent-workflow-global 执行任务'"
echo -e "  2. 快捷命令: 'maw 执行任务' (需要重新打开终端)"
echo -e "  3. 查看模板: 'maw-list'"
echo ""
echo -e "${YELLOW}迁移功能:${NC}"
echo -e "  导出配置: $INSTALL_DIR/scripts/migrate.sh export"
echo -e "  导入配置: $INSTALL_DIR/scripts/migrate.sh import"
echo ""
echo -e "${GREEN}✅ 安装成功！${NC}"
echo ""
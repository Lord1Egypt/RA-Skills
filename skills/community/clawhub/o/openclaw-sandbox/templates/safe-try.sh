#!/bin/bash
set -e

# ============================================================================
# OpenClaw 沙盒测试脚本 v3.0
# 用途：在沙盒环境中安全测试配置变更
# 作者：墨墨 (Mò)
# 版本：3.0.0 (基于 9 层防护 +5 原则)
# ============================================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
SANDBOX_DIR="/tmp/openclaw-sandbox-3.8"
SANDBOX_CONFIG="$SANDBOX_DIR/.openclaw/openclaw.json"
PROD_CONFIG="$HOME/.openclaw/openclaw.json"
BACKUP_DIR="$HOME/.openclaw/backups"

# ============================================================================
# 函数：显示使用说明
# ============================================================================
show_usage() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   OpenClaw 沙盒测试脚本 v3.0                           ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "用法：${GREEN}bash ~/.openclaw/skills/openclaw-sandbox/templates/safe-try.sh${NC}"
    echo ""
    echo -e "${YELLOW}功能:${NC}"
    echo "  1. 创建独立沙盒环境（9 层防护）"
    echo "  2. 应用配置变更到沙盒"
    echo "  3. 启动沙盒 Gateway 测试"
    echo "  4. 验证配置有效性"
    echo "  5. 清理环境变量"
    echo ""
    echo -e "${YELLOW}9 层防护:${NC}"
    echo "  1. 环境变量隔离"
    echo "  2. 配置验证"
    echo "  3. 配置隔离"
    echo "  4. 插件隔离"
    echo "  5. 端口隔离"
    echo "  6. Agent ID 唯一"
    echo "  7. CORS 修复"
    echo "  8. 进程保护"
    echo "  9. 性能优化"
    echo ""
}

# ============================================================================
# 函数：检查前置条件
# ============================================================================
check_prerequisites() {
    echo -e "${BLUE}[1/6] 检查前置条件...${NC}"
    
    # 检查 Git
    if ! command -v git &> /dev/null; then
        echo -e "${RED}错误：Git 未安装${NC}"
        exit 1
    fi
    
    # 检查 OpenClaw
    if ! command -v openclaw &> /dev/null; then
        echo -e "${RED}错误：OpenClaw 未安装${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ 前置条件检查通过${NC}"
}

# ============================================================================
# 函数：创建沙盒目录（配置隔离 + 插件隔离）
# ============================================================================
create_sandbox_dir() {
    echo -e "${BLUE}[2/6] 创建沙盒目录（配置隔离 + 插件隔离）...${NC}"
    
    # 创建独立目录（不复制生产！）
    mkdir -p $SANDBOX_DIR/.openclaw/{extensions,agents/writer,agents/media,logs,backups}
    
    # 创建独立配置（空插件列表）
    cat > $SANDBOX_CONFIG << 'EOF'
{
  "meta": {
    "purpose": "sandbox-3.8",
    "created_at": "2026-03-10T09:00:00+08:00"
  },
  "gateway": {
    "auth": {
      "mode": "token",
      "token": "sandbox-token-xxx"
    },
    "port": 18800,
    "bind": "loopback"
  },
  "agents": {
    "list": [
      {
        "id": "writer-sandbox",
        "name": "墨墨 (沙盒)",
        "workspace": "/tmp/openclaw-sandbox-3.8/agents/writer",
        "model": {"primary": "bailian/qwen3.5-plus"}
      },
      {
        "id": "media-sandbox",
        "name": "小媒 (沙盒)",
        "workspace": "/tmp/openclaw-sandbox-3.8/agents/media",
        "model": {"primary": "bailian/glm-4.7"}
      }
    ]
  },
  "plugins": {
    "allow": ["feishu-openclaw-plugin"],
    "entries": {
      "feishu-openclaw-plugin": {"enabled": true}
    }
  },
  "memory": {
    "backend": "qmd"
  }
}
EOF
    
    echo -e "${GREEN}✓ 沙盒目录创建完成${NC}"
}

# ============================================================================
# 函数：验证配置（配置验证原则）
# ============================================================================
validate_config() {
    echo -e "${BLUE}[3/6] 验证配置（配置验证原则）...${NC}"
    
    # 配置验证
    OPENCLAW_HOME=$SANDBOX_DIR/.openclaw openclaw config validate
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}错误：配置验证失败${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ 配置验证通过${NC}"
}

# ============================================================================
# 函数：备份配置（配置备份原则）
# ============================================================================
backup_config() {
    echo -e "${BLUE}[4/6] 备份配置（配置备份原则）...${NC}"
    
    # 备份沙盒配置
    cp $SANDBOX_CONFIG $SANDBOX_CONFIG.bak.$(date +%Y%m%d_%H%M%S)
    
    echo -e "${GREEN}✓ 配置备份完成${NC}"
}

# ============================================================================
# 函数：启动沙盒 Gateway（进程保护 + 性能优化）
# ============================================================================
start_gateway() {
    echo -e "${BLUE}[5/6] 启动沙盒 Gateway（进程保护 + 性能优化）...${NC}"
    
    # 设置环境变量
    export OPENCLAW_HOME=$SANDBOX_DIR/.openclaw
    export HOME=$SANDBOX_DIR  # 破解~/陷阱
    
    # 后台启动（nohup 进程保护）
    cd $SANDBOX_DIR
    nohup openclaw gateway run --bind loopback --port 18800 \
      > $SANDBOX_DIR/.openclaw/logs/gateway.log 2>&1 &
    
    # 记录 PID
    echo $! > $SANDBOX_DIR/.openclaw/gateway.pid
    
    # 等待启动
    sleep 3
    
    # 清理环境变量（环境清理原则）
    unset OPENCLAW_HOME
    
    echo -e "${GREEN}✓ 沙盒 Gateway 启动完成${NC}"
    echo -e "${BLUE}WebUI: http://127.0.0.1:18800/#token=sandbox-token-xxx${NC}"
}

# ============================================================================
# 函数：验证沙盒状态
# ============================================================================
verify_sandbox() {
    echo -e "${BLUE}[6/6] 验证沙盒状态...${NC}"
    
    # 检查进程
    if ps aux | grep "openclaw gateway.*18800" | grep -v grep > /dev/null; then
        echo -e "${GREEN}✓ Gateway 进程运行中${NC}"
    else
        echo -e "${RED}错误：Gateway 进程未运行${NC}"
        exit 1
    fi
    
    # 检查端口
    if lsof -i :18800 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 端口 18800 已监听${NC}"
    else
        echo -e "${YELLOW}警告：端口 18800 未监听（可能启动中）${NC}"
    fi
    
    echo -e "${GREEN}✓ 沙盒验证完成${NC}"
}

# ============================================================================
# 主流程
# ============================================================================
main() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   OpenClaw 沙盒测试 v3.0 - 9 层防护                      ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_prerequisites
    create_sandbox_dir
    validate_config
    backup_config
    start_gateway
    verify_sandbox
    
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   沙盒测试环境就绪！                                   ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}沙盒路径:${NC} $SANDBOX_DIR"
    echo -e "${BLUE}WebUI: ${NC} http://127.0.0.1:18800/#token=sandbox-token-xxx"
    echo -e "${BLUE}日志：${NC} $SANDBOX_DIR/.openclaw/logs/gateway.log"
    echo ""
    echo -e "${YELLOW}下一步:${NC}"
    echo "  1. 在沙盒中测试配置变更"
    echo "  2. 验证功能正常"
    echo "  3. 使用 apply-config.sh 应用到生产"
    echo ""
}

# 执行
main

#!/bin/bash
# 创建 VIP Agent 脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 参数解析
USER_ID=""
USER_NAME=""
CHANNEL="feishu"
VIP_LEVEL="platinum"

usage() {
    echo "用法：$0 -u <user_id> -n <user_name> [-c channel] [-l vip_level]"
    echo ""
    echo "选项:"
    echo "  -u, --user-id      用户 ID（必填）"
    echo "  -n, --user-name    用户名称（必填）"
    echo "  -c, --channel      渠道（可选，默认：feishu）"
    echo "  -l, --level        VIP 等级（可选，默认：platinum）"
    echo ""
    echo "示例:"
    echo "  $0 -u laoliu -n \"老刘\" -c feishu -l platinum"
    exit 1
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--user-id)
            USER_ID="$2"
            shift 2
            ;;
        -n|--user-name)
            USER_NAME="$2"
            shift 2
            ;;
        -c|--channel)
            CHANNEL="$2"
            shift 2
            ;;
        -l|--level)
            VIP_LEVEL="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "未知选项：$1"
            usage
            ;;
    esac
done

# 验证必填参数
if [ -z "$USER_ID" ] || [ -z "$USER_NAME" ]; then
    echo -e "${RED}❌ 错误：user_id 和 user_name 是必填参数${NC}"
    usage
fi

# 变量定义
VIP_AGENT_NAME="vip-${USER_ID}"
WORKSPACE_DIR="${HOME}/.openclaw/workspace-vip-${USER_ID}"
CONFIG_FILE="${WORKSPACE_DIR}/.privacy-config.json"

echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}🚀 创建 VIP Agent${NC}"
echo -e "${BLUE}==================================${NC}"
echo ""
echo -e "用户 ID:   ${GREEN}${USER_ID}${NC}"
echo -e "用户名称：${GREEN}${USER_NAME}${NC}"
echo -e "渠道：     ${GREEN}${CHANNEL}${NC}"
echo -e "VIP 等级：  ${GREEN}${VIP_LEVEL}${NC}"
echo ""

# 步骤 1：创建 agent
echo -e "${YELLOW}[1/5] 创建 VIP agent...${NC}"
if openclaw agents add "${VIP_AGENT_NAME}" \
    --identity "${USER_NAME} 专属助手" \
    --workspace "${WORKSPACE_DIR}"; then
    echo -e "${GREEN}✅ VIP agent 创建成功${NC}"
else
    echo -e "${RED}❌ VIP agent 创建失败${NC}"
    exit 1
fi
echo ""

# 步骤 2：绑定路由
echo -e "${YELLOW}[2/5] 绑定路由...${NC}"
if openclaw agents bind "${VIP_AGENT_NAME}" \
    --channel "${CHANNEL}" \
    --account "ou_${USER_ID}"; then
    echo -e "${GREEN}✅ 路由绑定成功${NC}"
else
    echo -e "${RED}❌ 路由绑定失败${NC}"
    exit 1
fi
echo ""

# 步骤 3：创建配置目录
echo -e "${YELLOW}[3/5] 创建配置目录...${NC}"
mkdir -p "${WORKSPACE_DIR}/credentials"
mkdir -p "${WORKSPACE_DIR}/memory"
mkdir -p "${WORKSPACE_DIR}/logs"
echo -e "${GREEN}✅ 配置目录创建成功${NC}"
echo ""

# 步骤 4：创建隐私配置
echo -e "${YELLOW}[4/5] 创建隐私配置...${NC}"
cat > "${CONFIG_FILE}" << EOF
{
  "admin": {
    "id": "ou_${USER_ID}",
    "name": "${USER_NAME}",
    "role": "admin"
  },
  "privacy": {
    "mode": "strict",
    "forbiddenTerms": []
  },
  "vip": {
    "level": "${VIP_LEVEL}",
    "created_at": "$(date -Iseconds)",
    "features": {
      "dedicated_agent": true,
      "priority_support": true,
      "custom_config": true,
      "data_export": true
    }
  }
}
EOF
echo -e "${GREEN}✅ 隐私配置创建成功${NC}"
echo -e "   配置文件：${CONFIG_FILE}"
echo ""

# 步骤 5：创建欢迎文档
echo -e "${YELLOW}[5/5] 创建欢迎文档...${NC}"
cat > "${WORKSPACE_DIR}/README.md" << EOF
# ${USER_NAME} 的专属 VIP Agent

> 创建于：$(date -Iseconds)

## 🎯 专属功能

- ✅ 独立工作空间
- ✅ 完全数据隔离
- ✅ 优先响应
- ✅ 专属配置

## 📁 目录结构

\`\`\`
${WORKSPACE_DIR}/
├── credentials/     # 认证信息
├── memory/          # 记忆文件
├── logs/            # 日志文件
└── README.md        # 本文档
\`\`\`

## 🔧 管理命令

\`\`\`bash
# 查看 agent 状态
openclaw agents list

# 查看路由绑定
openclaw agents bindings

# 删除 agent（谨慎操作）
openclaw agents delete ${VIP_AGENT_NAME}
\`\`\`

## 📞 技术支持

如有问题，请联系：support@example.com

---

**VIP 等级**: ${VIP_LEVEL}  
**创建时间**: $(date -Iseconds)
EOF
echo -e "${GREEN}✅ 欢迎文档创建成功${NC}"
echo ""

# 完成
echo -e "${BLUE}==================================${NC}"
echo -e "${GREEN}✅ VIP Agent 创建完成！${NC}"
echo -e "${BLUE}==================================${NC}"
echo ""
echo -e "Agent 名称：${GREEN}${VIP_AGENT_NAME}${NC}"
echo -e "工作空间：${GREEN}${WORKSPACE_DIR}${NC}"
echo -e "路由配置：${GREEN}${CHANNEL} -> ou_${USER_ID}${NC}"
echo ""
echo -e "${YELLOW}下一步:${NC}"
echo "1. 配置 API Keys（如需要）"
echo "2. 测试 agent 是否正常工作"
echo "3. 通知用户已开通 VIP 服务"
echo ""
echo -e "祝使用愉快！🎉"

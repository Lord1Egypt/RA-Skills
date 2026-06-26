# VIP Agent 配置模板

> 用于快速创建 VIP 用户专属 agent

---

## 📋 创建 VIP Agent 流程

### 步骤 1：创建 agent

```bash
openclaw agents add vip-{user_id} \
  --identity "VIP 用户 {user_name} 的专属助手" \
  --workspace ~/.openclaw/workspace-vip-{user_id}
```

### 步骤 2：配置路由

```bash
openclaw agents bind vip-{user_id} \
  --channel feishu \
  --account ou_{user_id}
```

### 步骤 3：配置身份

```yaml
# ~/.openclaw/agents/vip-{user_id}/identity.yaml
name: "{user_name} 专属助手"
emoji: "💎"
avatar: "./avatars/vip.png"
theme: "professional"
```

### 步骤 4：配置认证

```bash
mkdir -p ~/.openclaw/workspace-vip-{user_id}/credentials

cat > ~/.openclaw/workspace-vip-{user_id}/credentials/api-keys.json << 'EOF'
{
  "api_keys": {
    "llm": "vip-api-key-xxx",
    "oss": "vip-oss-key-xxx"
  }
}
EOF
```

---

## 🎯 VIP 用户迁移流程

### 从普通用户升级到 VIP

**1. 备份技能层数据**

```bash
# 备份记忆文件
cp ~/.openclaw/workspace/memory/users/{user_id}.md \
   ~/.openclaw/workspace-vip-{user_id}/memory-backup.md

# 备份会话历史
cp ~/.openclaw/agents/main/sessions/{session_id}.jsonl \
   ~/.openclaw/workspace-vip-{user_id}/sessions-backup.jsonl
```

**2. 创建 VIP agent**

```bash
openclaw agents add vip-{user_id} \
  --identity "{user_name} 专属助手" \
  --workspace ~/.openclaw/workspace-vip-{user_id}
```

**3. 切换路由**

```bash
openclaw agents bind vip-{user_id} \
  --channel feishu \
  --account ou_{user_id}
```

**4. 验证**

```bash
openclaw agents list
# 确认 vip-{user_id} 已创建

openclaw agents bindings
# 确认路由已切换
```

---

## 📊 VIP Agent 配置示例

### 示例 1：企业客户

```bash
# 创建
openclaw agents add vip-company1 \
  --identity "XX 公司专属助手" \
  --workspace ~/.openclaw/workspace-vip-company1

# 绑定
openclaw agents bind vip-company1 \
  --channel feishu \
  --account ou_company1_admin_id

# 配置
cat > ~/.openclaw/workspace-vip-company1/.privacy-config.json << 'EOF'
{
  "admin": {
    "id": "ou_company1_admin_id",
    "name": "公司管理员",
    "role": "admin"
  },
  "privacy": {
    "mode": "strict"
  },
  "company": {
    "name": "XX 公司",
    "industry": "物流",
    "custom_rules": [
      "禁止泄露公司数据",
      "优先使用公司知识库"
    ]
  }
}
EOF
```

---

### 示例 2：个人 VIP

```bash
# 创建
openclaw agents add vip-laoliu \
  --identity "老刘的专属助手" \
  --workspace ~/.openclaw/workspace-vip-laoliu

# 绑定
openclaw agents bind vip-laoliu \
  --channel feishu \
  --account ou_b96f5424607baf3a0455b55e0f4a2213
```

---

## 🔧 自动化脚本

### 创建 VIP agent 脚本

```bash
#!/bin/bash
# scripts/create-vip-agent.sh

USER_ID=$1
USER_NAME=$2
CHANNEL=${3:-feishu}

if [ -z "$USER_ID" ] || [ -z "$USER_NAME" ]; then
    echo "用法：$0 <user_id> <user_name> [channel]"
    exit 1
fi

echo "🚀 创建 VIP agent: vip-${USER_ID}"

# 1. 创建 agent
openclaw agents add vip-${USER_ID} \
  --identity "${USER_NAME} 专属助手" \
  --workspace ~/.openclaw/workspace-vip-${USER_ID}

# 2. 绑定路由
openclaw agents bind vip-${USER_ID} \
  --channel ${CHANNEL} \
  --account ou_${USER_ID}

# 3. 创建配置目录
mkdir -p ~/.openclaw/workspace-vip-${USER_ID}/credentials
mkdir -p ~/.openclaw/workspace-vip-${USER_ID}/memory

# 4. 创建隐私配置
cat > ~/.openclaw/workspace-vip-${USER_ID}/.privacy-config.json << EOF
{
  "admin": {
    "id": "ou_${USER_ID}",
    "name": "${USER_NAME}",
    "role": "admin"
  },
  "privacy": {
    "mode": "strict"
  },
  "vip": {
    "level": "platinum",
    "created_at": "$(date -Iseconds)"
  }
}
EOF

echo "✅ VIP agent 创建完成：vip-${USER_ID}"
echo "📁 工作空间：~/.openclaw/workspace-vip-${USER_ID}"
echo "🔗 路由：${CHANNEL} -> ou_${USER_ID}"
```

---

### 删除 VIP agent 脚本

```bash
#!/bin/bash
# scripts/delete-vip-agent.sh

USER_ID=$1

if [ -z "$USER_ID" ]; then
    echo "用法：$0 <user_id>"
    exit 1
fi

echo "⚠️  警告：即将删除 VIP agent: vip-${USER_ID}"
read -p "确认删除？(y/N): " confirm

if [ "$confirm" != "y" ]; then
    echo "已取消"
    exit 0
fi

# 1. 删除 agent
openclaw agents delete vip-${USER_ID}

# 2. 清理工作空间
rm -rf ~/.openclaw/workspace-vip-${USER_ID}

echo "✅ VIP agent 已删除：vip-${USER_ID}"
```

---

### 列出所有 VIP agent

```bash
#!/bin/bash
# scripts/list-vip-agents.sh

echo "💎 VIP Agent 列表"
echo "================"
echo ""

openclaw agents list | grep "vip-"

echo ""
echo "📊 统计信息"
echo "=========="
VIP_COUNT=$(openclaw agents list | grep "vip-" | wc -l)
echo "VIP 用户数：${VIP_COUNT}"
```

---

## 📈 监控 VIP agent

### 健康检查脚本

```bash
#!/bin/bash
# scripts/check-vip-health.sh

echo "🏥 VIP Agent 健康检查"
echo "===================="
echo ""

for agent in $(openclaw agents list | grep "vip-" | awk '{print $1}'); do
    echo "检查：${agent}"
    
    # 检查工作空间
    if [ -d "~/.openclaw/workspace-${agent}" ]; then
        echo "  ✅ 工作空间：正常"
    else
        echo "  ❌ 工作空间：缺失"
    fi
    
    # 检查路由
    if openclaw agents bindings | grep -q "${agent}"; then
        echo "  ✅ 路由配置：正常"
    else
        echo "  ❌ 路由配置：缺失"
    fi
    
    echo ""
done
```

---

## 🎯 下一步

1. ✅ 创建自动化脚本
2. ⏸️ 测试 VIP agent 创建流程
3. ⏸️ 设计收费套餐
4. ⏸️ 实现计费系统

---

**文档版本**: v1.0  
**创建时间**: 2026-03-11  
**维护者**: 狗子 🐶

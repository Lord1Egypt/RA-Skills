# AgentGuard + Feishu 集成

## 快速开始

### 1. 启用 Feishu 通知

```javascript
const AgentGuard = require('agentguard');

const guard = new AgentGuard({
  masterPassword: 'your-password'
});

await guard.init();

// 启用 Feishu 通知
guard.enableFeishu({
  openId: 'ou_xxx',  // 你的 Feishu Open ID
  useOpenClaw: true  // 使用 OpenClaw 发送
});
```

### 2. 创建审批请求（自动发送通知）

```javascript
// 发送邮件前检查权限
const check = await guard.checkOrApprove('my-agent', 'send_email', {
  to: 'user@example.com',
  subject: 'Hello'
});
```

**Feishu 收到的消息**:

```
🔐 AgentGuard 审批请求

智能体: my-agent
操作: send_email
创建时间: 2026/3/1 18:49:59
过期时间: 2026/3/1 18:54:59

详情:
{
  "to": "user@example.com",
  "subject": "Hello"
}

请求ID: 1e2d3841...

[✅ 批准] [❌ 拒绝]
```

### 3. 批准/拒绝请求

#### 方式 1: CLI
```bash
agentguard approve 1e2d384179bb05d94134f681741a7dea
agentguard deny 1e2d384179bb05d94134f681741a7dea
```

#### 方式 2: API
```javascript
// 批准
await guard.approveRequest(requestId, 'Master');

// 拒绝
await guard.denyRequest(requestId, 'Master', '原因');
```

### 4. 发送结果通知

```javascript
// 批准后发送通知
await guard.notifyApprovalResult(request, true, 'Master');
```

**Feishu 收到的消息**:

```
✅ 审批已批准 - AgentGuard

智能体: my-agent
操作: send_email
处理人: Master
时间: 2026/3/1 18:50:21

操作已授权执行
```

## OpenClaw 集成

AgentGuard 与 OpenClaw 完美集成：

```javascript
const guard = new AgentGuard({
  masterPassword: process.env.AGENTGUARD_PASSWORD,
  feishu: true,
  feishuOpenId: process.env.FEISHU_OPEN_ID
});

await guard.init();

// 在智能体执行操作前
const check = await guard.checkOrApprove('nano', 'send_email', {
  to: 'user@example.com',
  subject: 'Daily report'
});

if (check.allowed) {
  // 人类已批准，可以执行
  await sendEmail(...);
}
```

## Feishu 卡片格式

AgentGuard 使用 Feishu 交互式卡片，包含：

- **标题**: 橙色高亮 "🔐 AgentGuard 审批请求"
- **字段**: 智能体、操作、创建时间、过期时间
- **详情**: JSON 格式的操作详情
- **按钮**: "✅ 批准" 和 "❌ 拒绝"

## 环境变量

```bash
# AgentGuard
export AGENTGUARD_PASSWORD="your-master-password"

# Feishu
export AGENTGUARD_FEISHU="true"
export FEISHU_OPEN_ID="ou_xxx"

# 1Password (可选)
export AGENTGUARD_USE_1PASSWORD="true"
```

## 完整示例

```javascript
const AgentGuard = require('agentguard');

async function main() {
  // 1. 初始化
  const guard = new AgentGuard({
    masterPassword: process.env.AGENTGUARD_PASSWORD
  });
  await guard.init();

  // 2. 启用 Feishu
  guard.enableFeishu({
    openId: process.env.FEISHU_OPEN_ID
  });

  // 3. 检查权限 + 自动请求审批
  try {
    const check = await guard.checkOrApprove('my-agent', 'send_email', {
      to: 'boss@company.com',
      subject: '月度报告',
      body: '请查收附件中的月度报告'
    });

    if (check.allowed) {
      console.log('✅ 已批准，开始发送邮件');
      // 执行发送
    }
  } catch (e) {
    console.log('❌ 操作被拒绝:', e.message);
  }
}

main();
```

## 下一步

- [ ] 支持 Feishu 卡片按钮回调（直接在 Feishu 中批准）
- [ ] 支持群聊通知
- [ ] 支持多审批人

---

*AgentGuard + Feishu = 安全 + 便捷*

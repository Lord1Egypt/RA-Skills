---
name: loudy-ai-auto-task
description: |
  Loudy.ai 任务自动化工具 - 查询奖池、提交任务链接、追踪审核和支付状态。
  重要说明：此工具仅与 loudy.ai API 交互，不包含 Twitter/X 自动发布功能。
  使用条件：
  (1) 用户需要先配置 LOUDY_API_KEY 环境变量
  (2) 启动后会定时查询奖池、提交任务链接、查询审核和支付状态
  (3) 适用于需要自动管理 loudy.ai 任务的场景
metadata:
  openclaw:
    requires:
      env:
        - name: LOUDY_API_KEY
          description: "Loudy.ai API Key"
          required: true
---

# Loudy.ai 自动任务 Skill

## ⚠️ 安全警告

- 🔐 **API Key 安全**：建议使用环境变量 `export LOUDY_API_KEY=你的密钥`，**不要**写入 TOOLS.md 或其他共享文件
- 📝 **文件系统访问**：本工具会读写工作区目录下的文件（默认：`/root/.openclaw/workspace/`，可通过 `OPENCLAW_WORKSPACE` 环境变量自定义）
- ⏰ **可选的 Cron 任务**：如需自动检查，需手动配置 cron 任务

## 快速开始

### 1. 配置 API Key (推荐环境变量方式)

```bash
export LOUDY_API_KEY="你的API密钥"
```

⚠️ **注意**：不建议将密钥写入 TOOLS.md，避免意外泄露

### 2. 启动任务

告诉 AI：
> "查看 loudy 可用奖池"

### 3. 自动执行流程

1. AI 展示可用奖池详情（包括要求、奖金、截止时间、详情页面链接）
2. 你根据要求发布推文到 X/Twitter
3. 将推文链接发送给 AI
4. AI 自动提交到 loudy.ai

## 工作流程

```
1. fetch_earning_pools() → 获取进行中的奖池列表
2. 展示奖池详情给用户 → 包括要求、奖金、截止时间、详情页面链接
3. 提示用户根据要求发推文 → 用户手动发布到 X/Twitter
4. 等待用户提供推文链接 → 用户把推文链接发给 AI
5. submit_task() → 自动提交作品链接到 loudy.ai
6. 定时 check_task_status() → 查询任务是否被接受
   ├─ 超时未接受 → 报告失败
   └─ 已接受 → 定时查询 payment/支付信息
```

## 用户交互流程示例

### 步骤 1: 查看可用奖池
```
用户: "查看 loudy 可用奖池"
AI: 调用 fetch_pools.py，展示奖池列表（包含详情页面链接）
```

### 步骤 2: 选择奖池并发推文
```
AI: 展示奖池详情和要求
用户: 选择奖池，根据要求发布推文
```

### 步骤 3: 提交推文链接
```
用户: "提交推文链接 https://x.com/xxx/status/123 到奖池 3"
AI: 调用 submit_task.py(3, "https://x.com/xxx/status/123")
```

### 步骤 4: 查询任务状态
```
用户: "查询任务状态"
AI: 调用 check_task.py 查询审核和支付状态
```

## API 接口

### 1. 获取奖池列表
- **URL**: `GET https://api.loudy.ai/app-api/open-api/v1/earning-pools`
- **Header**: `X-API-Key: <LOUDY_API_KEY>`

### 2. 获取奖池详情
- **URL**: `GET https://api.loudy.ai/app-api/open-api/v1/earning-pools/{id}`
- **Header**: `X-API-Key: <LOUDY_API_KEY>`

### 3. 提交任务
- **URL**: `POST https://api.loudy.ai/app-api/open-api/v1/earning-pool-tasks/submit`
- **Header**: `X-API-Key: <LOUDY_API_KEY>`
- **Body**:
```json
{
  "earningPoolId": 123,
  "taskLink": ["https://x.com/xxx/status/123"],
  "languageType": "zh_CN"
}
```

### 4. 查询我的任务列表（分页）
- **URL**: `GET https://api.loudy.ai/app-api/open-api/v1/earning-pool-tasks`
- **Header**: `X-API-Key: <LOUDY_API_KEY>`
- **Query**:
  - `pageNo` - 页码（必填）
  - `pageSize` - 每页条数，最大100（必填）
  - `earningPoolId` - 奖池ID（可选）
  - `taskStatus` - 任务状态（可选）

### 5. 查询任务状态
- **URL**: `GET https://api.loudy.ai/app-api/open-api/v1/earning-pool-tasks/{id}`
- **Header**: `X-API-Key: <LOUDY_API_KEY>`
- **返回字段**:
  - `taskStatus` - 任务状态
  - `auditStatus` - 审核状态 (0=未审核, 1=通过, 2=拒绝)
  - `taskLinks` - 作品链接

## 脚本说明

### scripts/fetch_pools.py
获取进行中的奖池列表，过滤 Ongoing 状态

### scripts/list_my_tasks.py
查询当前用户的任务列表（分页）

### scripts/submit_task.py
提交作品链接到奖池

### scripts/check_task.py
查询单个任务状态和支付信息

### scripts/auto_task_flow.py
优化的任务流程脚本：
1. 获取可用奖池列表
2. 展示奖池详情（包括要求、奖金、截止时间）
3. 显示 Loudy.ai 详情页面链接
4. 等待用户提供推文链接
5. 自动提交到 loudy.ai

### scripts/check_tasks.py
定时检查脚本，获取当前奖池并格式化输出

### scripts/cron_check.sh
Cron 定时任务脚本，每5分钟检查一次新任务。使用 `OPENCLAW_WORKSPACE` 环境变量自定义工作目录。

## 配置定时检查（可选）

### 1. 设置环境变量
```bash
export LOUDY_API_KEY="你的API Key"
export OPENCLAW_WORKSPACE="/root/.openclaw/workspace"  # 可选，默认值
```

### 2. 配置 Cron 定时检查（可选）
```bash
# 方法1: 使用工作区安装路径（推荐）
SKILL_DIR="/root/.openclaw/workspace/skills/claw-loudyai-skill"
(crontab -l 2>/dev/null; echo "*/5 * * * * $SKILL_DIR/scripts/cron_check.sh") | crontab -

# 方法2: 如果安装到系统路径
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/lib/node_modules/openclaw/skills/loudy-ai-auto-task/scripts/cron_check.sh") | crontab -
```

### 3. 配置 Heartbeat 通知（可选）
在 HEARTBEAT.md 中添加：
```
## Loudy.ai 任务检查
检查工作区目录下的 loudy_has_new.txt 是否存在：
- 如果存在 → 读取 loudy_tasks.json 内容
- 发送消息通知用户
- 删除 loudy_has_new.txt
```

## 注意事项

- ⚠️ **API Key 安全**：建议使用环境变量 `export LOUDY_API_KEY=你的密钥`，**不要**写入 TOOLS.md 或其他共享文件
- 📝 **文件系统访问**：本工具会读写工作区目录下的文件（默认：`/root/.openclaw/workspace/`，可通过 `OPENCLAW_WORKSPACE` 环境变量自定义），包括 `loudy_tasks.json`, `loudy_has_new.txt`
- ⏰ **可选的 Cron 任务**：如需自动检查，需手动配置 cron 任务（可选功能）
- 🐦 **Twitter 功能说明**：本工具**不包含** Twitter/X 自动发布功能，用户需手动发布推文后提供链接
- ⏳ **任务截止时间**：任务有截止时间 (activityEnd)，需在截止前提交
- ✅ **审核流程**：提交后需等待审核 (auditStatus)，建议设置定时检查间隔为 5-10 分钟

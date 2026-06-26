---
name: keplerjai-dingtalk-attendance
description: 从钉钉开放平台获取员工考勤数据，并保存到本地或推送到指定渠道。
---

# 钉钉考勤数据获取技能

## 功能描述
定时从钉钉开放平台获取员工考勤数据，并保存到本地或推送到指定渠道。

## 配置步骤

### 1. 钉钉开放平台配置
1. 访问 https://open.dingtalk.com
2. 创建企业内部应用
3. 获取 AppKey 和 AppSecret
4. 添加应用权限：
   - 考勤管理权限
   - 通讯录权限（获取员工信息）
5. 企业管理员审批授权

### 2. 本地配置
复制 `.env.example` 为 `.env` 并填写：
```env
DINGTALK_APP_KEY=你的 AppKey
DINGTALK_APP_SECRET=你的 AppSecret
DINGTALK_AGENT_ID=应用的 agentId
OUTPUT_DIR=./data/attendance
OUTPUT_FORMAT=json
```

执行规则：
- 仅使用技能目录下的 `.env` 读取凭证与输出配置。
- 不依赖 `config.json`。
- 若 `.env` 已存在且字段完整，直接执行，不要重复要求用户在对话中提供凭证。

建议先做本地自检：
- 确认 `.env` 文件在本技能根目录，与 `index.js` 同级。
- 确认包含 `DINGTALK_APP_KEY` 和 `DINGTALK_APP_SECRET`。
- 确认从本技能目录执行 `node index.js`（避免在其他目录启动导致找错文件）。

Windows PowerShell 示例：
```powershell
Copy-Item .env.example .env
node index.js
```

macOS/Linux 示例：
```bash
cp .env.example .env
node index.js
```

### 3. 安装依赖
```bash
npm install axios moment
```

## 使用方法

### 手动运行
```bash
cd keplerjai-dingtalk-attendance
node index.js
```

### 定时任务（推荐）
在 OpenClaw 中配置 cron 任务，每天自动获取前一天的考勤数据。

## 输出数据
- 打卡记录（JSON/CSV）
- 考勤日报/月报
- 异常考勤提醒

## 注意事项
- API 调用有频率限制，建议定时获取而非实时
- 需要企业管理员授权
- 敏感数据请妥善保管

## Agent 执行约定
- 先读取本技能目录下的 `.env` 再执行任务。
- 若缺少必要字段，仅提示“本地 `.env` 缺少必填项”，不要要求用户在聊天中粘贴密钥。
- 默认返回考勤结果与输出文件位置，不回显任何密钥值。

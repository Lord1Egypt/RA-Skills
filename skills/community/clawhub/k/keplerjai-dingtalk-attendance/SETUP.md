# 设置指南

## 完成以下配置后即可使用

### ✅ 步骤 1: 配置钉钉应用

1. 访问 https://open.dingtalk.com
2. 创建企业内部应用
3. 获取 AppKey 和 AppSecret
4. 添加考勤管理权限并等待管理员审批

### ✅ 步骤 2: 创建本地环境变量文件

```bash
cd keplerjai-dingtalk-attendance
cp .env.example .env
```

### ✅ 步骤 3: 编辑配置

编辑 `.env`，填入你的钉钉应用信息：

```env
DINGTALK_APP_KEY=你的 AppKey
DINGTALK_APP_SECRET=你的 AppSecret
DINGTALK_AGENT_ID=你的 agentId
OUTPUT_DIR=./data/attendance
OUTPUT_FORMAT=json
```

### ✅ 步骤 4: 测试运行

```bash
node index.js
```

### ✅ 步骤 5: 配置定时任务（可选）

如需每天自动获取考勤数据，可以使用 OpenClaw 的 cron 功能：

```bash
openclaw cron add --file cron-example.json
```

或手动配置每天早上 9 点运行。

---

## 配置完成后

配置完成后，你可以：
- 手动运行 `node index.js` 获取考勤数据
- 配置 cron 定时任务自动获取
- 扩展功能：异常提醒、报表推送等

**数据输出位置**: `./data/attendance/`

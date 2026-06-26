# 全球新闻晚报 - 安装指南

## ✅ 已完成的步骤

1. ✅ 创建技能目录和文件
2. ✅ 编写推送脚本
3. ✅ 配置 SKILL.md

## ⚙️ 需要配置的步骤

### 1. 配置飞书 Webhook

```bash
# 编辑 .env 文件
notepad "$env:USERPROFILE\.openclaw\.env"

# 添加以下内容（替换为你的飞书机器人 Webhook）
FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx"
QQ_ENABLED="true"
```

### 2. 设置定时任务

**方法 A：使用 OpenClaw cron（推荐）**

```bash
# 查看 cron 帮助
openclaw cron --help

# 添加定时任务（每天晚上 8 点）
openclaw cron add "全球新闻晚报" "0 20 * * *" "python $env:USERPROFILE\.openclaw\workspace\skills\news-evening-digest\scripts\fetch_and_digest.py"
```

**方法 B：使用 Windows 任务计划程序**

1. 打开"任务计划程序"
2. 创建基本任务
3. 名称：全球新闻晚报
4. 触发器：每天 20:00
5. 操作：启动程序
   - 程序：`python`
   - 参数：`C:\Users\shenz\.openclaw\workspace\skills\news-evening-digest\scripts\fetch_and_digest.py`
   - 起始于：`C:\Users\shenz\.openclaw\workspace`

**方法 C：手动执行（测试用）**

```bash
# 手动运行一次测试
python "$env:USERPROFILE\.openclaw\workspace\skills\news-evening-digest\scripts\fetch_and_digest.py"
```

### 3. 测试推送

```bash
# 运行测试
cd "$env:USERPROFILE\.openclaw\workspace\skills\news-evening-digest\scripts"
python fetch_and_digest.py
```

## 📋 验证清单

- [ ] 飞书 Webhook URL 已配置
- [ ] 定时任务已设置
- [ ] 手动测试推送成功
- [ ] 确认推送时间：每天 20:00 (Asia/Shanghai)

## 🔧 故障排查

### 问题：飞书推送失败

**检查：**
1. Webhook URL 是否正确
2. 网络连接是否正常
3. 飞书机器人是否已启用

### 问题：新闻抓取失败

**检查：**
1. Tavily Search 技能是否已安装
2. 网络连接是否正常
3. 查看脚本输出日志

### 问题：定时任务未执行

**检查：**
1. cron 任务是否已添加：`openclaw cron list`
2. 时间设置是否正确（注意时区）
3. 查看 OpenClaw 日志

## 📊 推送内容示例

```
📰 全球新闻晚报 | 03 月 13 日 20:00

━━━━━━━━━━━━━━━━━━━━

🌍 全球热点 (7 天焦点)

• 伊朗局势：第 13 天军事冲突持续
  - 伊朗导弹袭击以色列北部，30+ 人受伤
  - 美军加油机伊拉克坠毁，4 人丧生
  - 油价突破$100/桶，全球股市下跌

• 俄乌冲突：最新军事与外交进展
• 全球经济：制裁与能源市场波动

💻 科技动态

• Kimi：长文本处理能力持续优化
• DeepSeek：开源模型性能再突破
• OpenClaw：AI Agent 自动化工具新进展

📈 财经要闻

• 全球股市：主要指数今日走势
• 加密货币：比特币及主流币种动态
• 央行政策：各国货币政策最新动向

━━━━━━━━━━━━━━━━━━━━

🗺️ 数据来源：World Monitor、Tavily Search
🤖 由 OpenClaw AI 自动整理
📊 查看实时情报：worldmonitor.app
```

## 🎯 自定义选项

### 修改推送时间

编辑 cron 任务，修改为其他时间：
- 早上 8 点：`0 8 * * *`
- 中午 12 点：`0 12 * * *`
- 晚上 10 点：`0 22 * * *`

### 添加更多数据源

编辑 `fetch_and_digest.py`，添加新的搜索关键词或 API。

### 修改推送格式

编辑 `format_news_digest()` 函数，自定义消息格式。

---

**安装完成后，请运行一次手动测试确认一切正常！**

如有问题，请查看日志或联系管理员。

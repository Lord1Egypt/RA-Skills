# Platform Monitor v2.0

全平台状态监控 + 产品监控 + 竞品监控 一体化工具

## ✨ 功能特性

### 🔍 三大监控板块

1. **平台动向监控** - 监测AI平台官方公告（待实现）
2. **产品+竞品监控** - 跟踪自己产品状态 & 竞品动态
3. **每日巡检** - 定时检测产品正常运行

### 📊 核心功能

- ✅ HTTP/HTTPS 可达性检测
- ✅ 关键词变化监控
- ✅ 响应时间追踪 & 趋势异常检测
- ✅ 产品上架状态监控
- ✅ 竞品增长数量统计（待实现）
- ✅ 飞书/企业微信/钉钉 多渠通知
- ✅ 通知冷却机制（避免刷屏）
- ✅ 健康度评分（0~100）
- ✅ 历史记录（JSONL格式）

## 🚀 快速开始

### 1️⃣ 安装

#### Windows
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

#### macOS / Linux
```bash
bash install.sh
```

#### 手动安装
```bash
# 1. 安装依赖
npm install axios cheerio playwright

# 2. 生成配置文件
node monitor.js --init

# 3. 编辑配置文件
# 打开 platform_monitor_config.json 填入你的配置

# 4. 测试运行
node monitor.js
```

### 2️⃣ 配置

编辑 `platform_monitor_config.json`，填入：

- **通知配置** - 飞书/企业微信/钉钉 Webhook URL
- **平台列表** - 要监控的AI平台（已预设10个）
- **产品列表** - 你自己上架的产品URL
- **监控频率** - 每天1次或2次

详细配置说明见 `config.example.json`（带注释）

### 3️⃣ 运行

```bash
# 执行一次完整检测
node monitor.js

# 生成并推送报告（无论有无异常）
node monitor.js --report

# 查看最近7天历史
node monitor.js --history
```

### 4️⃣ 定时任务

#### Windows（推荐）
已通过 `install.ps1` 自动创建，可在"任务计划程序"中查看：
- **PlatformMonitor-Morning** - 每天 09:00
- **PlatformMonitor-Evening** - 每天 21:00

手动创建：
```powershell
$action = New-ScheduledTaskAction -Execute "node" -Argument "monitor.js" -WorkingDirectory (Get-Location)
$trigger1 = New-ScheduledTaskTrigger -Daily -At "09:00"
$trigger2 = New-ScheduledTaskTrigger -Daily -At "21:00"
Register-ScheduledTask -TaskName "PlatformMonitor-Morning" -Action $action -Trigger $trigger1 -Force
Register-ScheduledTask -TaskName "PlatformMonitor-Evening" -Action $action -Trigger $trigger2 -Force
```

#### macOS / Linux
已通过 `install.sh` 自动创建 cron 任务

手动创建：
```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天9:00和21:00运行）
0 9,21 * * * cd /path/to/platform-monitor && node monitor.js >> monitor.log 2>&1
```

## 📋 配置说明

### 通知渠道

支持三种通知渠道（可同时使用）：

1. **飞书** - `webhookUrl` 填入飞书机器人 Webhook
2. **企业微信** - `wechatWebhookUrl` 填入企业微信 Webhook
3. **钉钉** - `dingtalkWebhookUrl` 填入钉钉机器人 Webhook

### 监控目标

#### 平台监控（`platforms`）
预设10个AI平台：
- 支付宝A2A / AI付
- 扣子Bot商店
- 百度文心智能体
- 闲鱼 / 豆包 / Kimi / 通义千问 / 天工AI / 智谱AI

可自定义添加/删除。

#### 产品监控（`products`）
填写你自己上架的产品URL，例如：
```json
{
  "name": "我的Bot-扣子",
  "url": "https://www.coze.cn/store/agent/你的BotID",
  "expectKeyword": "",
  "note": "扣子上架的产品"
}
```

### 通知策略

- `alwaysReport: true` - 每次运行都推送报告（推荐）
- `alwaysReport: false` - 仅异常时推送
- `cooldownMinutes: 30` - 同一告警最少间隔30分钟

## 📊 输出示例

### 控制台输出
```
[2026-05-30 18:00:00] ===== 开始本轮监控 (v1.1) =====
[2026-05-30 18:00:00] 检测目标: 12 个 (平台:10, 产品:2)
[2026-05-30 18:00:01] 检查 [平台]: 扣子Bot商店 (https://www.coze.cn/store)
[2026-05-30 18:00:01]   ✅ 扣子Bot商店: UP (245ms)
[2026-05-30 18:00:02] 检查 [产品]: 活动策划专家-扣子Bot (https://www.coze.cn/store/agent/...)
[2026-05-30 18:00:02]   ✅ 活动策划专家-扣子Bot: UP (312ms)
...
[2026-05-30 18:00:05] ===== 监控完成 =====
[2026-05-30 18:00:05] 状态变化: 0 个 | 健康度: 100/100 (✅12 ⚠️0 ❌0/12)
```

### 飞书通知（富文本卡片）
```
📊 平台巡检报告
时间: 2026-05-30 18:00:00
概览: 健康度 100/100 | ✅12 ⚠️0 ❌0/12 | 变化0个

全平台状态:
🟢 支付宝A2A首页: UP (189ms)
🟢 扣子Bot商店: UP (245ms)
...
```

## 🛠️ 高级用法

### 查看历史记录
```bash
node monitor.js --history
```

输出最近7天监控记录：
```
最近监控记录:
  2026-05-30 18:00:00  变化:0 健康:100  ...
  2026-05-29 21:00:00  变化:1 健康:92  ...
```

### 强制推送报告
```bash
node monitor.js --report
```

无论有无异常，都生成并推送报告。

### 自定义配置路径
```bash
node monitor.js --config /path/to/custom_config.json
```

（待实现）

## 🐛 故障排查

### 通知未收到
1. 检查 `webhookUrl` 是否正确
2. 运行 `node monitor.js --report` 强制推送测试
3. 查看控制台输出，确认通知是否发送成功

### 误报（平台实际正常但报DOWN）
1. 增加 `timeoutMs`（默认15000ms）
2. 检查 `expectKeyword` 是否正确
3. 查看 `platform_monitor_log.txt` 详细日志

### 配置文件不生效
1. 确认文件名是 `platform_monitor_config.json`
2. 确认文件在**当前工作目录**
3. 运行 `node monitor.js --init` 重新生成

## 📦 上架计划

- ✅ QClaw Skill - 上架 ClawHub
- 🔲 Coze Bot/插件 - 上架 Coze 商店
- 🔲 独立 SaaS - 按次/按月收费
- 🔲 闲鱼服务 - 帮人部署配置

## 📝 更新日志

### v2.0（进行中）
- ✅ 清理硬编码，改为配置化
- ✅ 交互式 `--init` 向导
- ✅ Windows/macOS/Linux 一键安装脚本
- ✅ 产品化改造（别人装了就能用）
- 🔲 平台公告监控（板块一）
- 🔲 竞品监控（板块二）
- 🔲 竞品增长数量统计

### v1.1（当前版本）
- ✅ 飞书富文本卡片通知
- ✅ 每日巡检健康度报告
- ✅ 响应时间趋势异常检测
- ✅ 产品上架状态监控
- ✅ 通知冷却持久化

### v1.0
- ✅ HTTP/HTTPS 可达性检测
- ✅ 关键词变化监控
- ✅ 基础通知功能

## 📄 许可证

MIT License

## 🙏 致谢

- Axios - HTTP 客户端
- Cheerio - HTML 解析
- Playwright - 无头浏览器（待使用）

---

**作者**: 大侠  
**用户**: 老张  
**最后更新**: 2026-05-30

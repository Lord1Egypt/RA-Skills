# Oil Price Monitor

监控国家发改委官网成品油价格调整公告的自动化技能。

## 功能

- 📅 基于官方工作日计算调价窗口（每10个工作日）
- 🕐 每日17:30自动运行检查
- 🔍 抓取发改委新闻发布页面
- 📢 检测到价格调整立即推送
- 🎯 起始日期：2026年4月7日

## 安装

```bash
clawhub install oil-price-monitor
```

或从源码安装：

```bash
cd skills/oil-price-monitor
clawhub publish .
```

## 使用方法

### 命令行

```bash
# 正常运行（仅窗口期执行）
python oil_price_monitor.py

# 强制运行（测试用）
python oil_price_monitor.py --test

# 查看下一个窗口期
python oil_price_monitor.py --next-window

# 查看最新新闻
python oil_price_monitor.py --recent
```

### OpenClaw 定时任务

发布后，在 OpenClaw 中添加定时任务：

```json
{
  "schedule": "30 17 * * *",
  "tz": "Asia/Shanghai",
  "payload": {
    "kind": "agentTurn",
    "message": "python3 /path/to/oil_price_monitor.py"
  },
  "delivery": {
    "mode": "announce"
  }
}
```

这将配置每天17:30运行（窗口期逻辑在脚本内处理）。

## 输出示例

正常输出（窗口期且检测到调整）：

```
🛢️  **成品油价格调整公告**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 窗口期: 2026-04-07 (第1个窗口)
📢 发布机构: 国家发改委
🕐 发布时间: 2026-04-07 10:00

💵 调整内容:
  汽油每吨上调 300 元
  柴油每吨上调 290 元

📄 公告标题: 关于成品油价格调整的通知
🔗 原文链接: https://www.ndrc.gov.cn/...

⚠️ 请以官方公报为准，本通知仅供参考。
```

非窗口期输出：

```
⏸️  今天不是成品油调价窗口期
   下一个调价窗口: 2026-04-07 (还有14天)
   本次任务跳过，等待下次执行
```

## 配置

修改 `oil_price_monitor.py` 顶部常量：

- `START_DATE`: 第一个窗口日期
- `WINDOW_INTERVAL`: 工作日间隔（默认10）
- `CHECK_TIME`: 每日检查时间
- `NDRC_URL`: 发改委新闻 URL
- `KEYWORDS`: 搜索关键词列表

## 依赖

- Python 3.8+
- requests
- beautifulsoup4
- lxml
- chinese-workdays 技能

## 数据源

- 国家发改委官网新闻发布: https://www.ndrc.gov.cn/xwdt/xwfb/
- 中国法定节假日: chinese-workdays 技能

## License

MIT
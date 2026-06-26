---
name: ndrc-oil-price
description: Monitor NDRC (National Development and Reform Commission) website for oil price adjustment announcements. Searches news releases every 10 working days at 17:30 starting from 2026-04-07 and pushes notifications via Feishu.
license: MIT
---

# 成品油价格监控器

监控国家发改委官网新闻发布，自动检测成品油价格调整信息并推送通知。

## 功能特性

- 📅 基于中国工作日计算调价窗口（每10个工作日）
- 🕐 每日17:30自动检查
- 🔍 搜索发改委官网新闻发布页面
- 📢 发现调整信息后立即推送到 Feishu
- 🎯 起始日期：2026-04-07
- ⚙️ 可配置窗口间隔和通知时间

## 工作原理

1. 计算下一个10工作日窗口期（基于 chinese-workdays 技能）
2. 每日17:30检查当前日期是否在窗口期内
3. 如果是窗口期，搜索发改委网站最新新闻
4. 筛选包含"成品油"、"油价"等关键词的公告
5. 提取价格调整信息（上调/下调幅度）
6. 通过 OpenClaw stdout 捕获推送到 Feishu

## 数据源

- **官网**: https://www.ndrc.gov.cn/xwdt/xwfb/
- **公告类型**: 新闻发布、政策通知
- **关键词**: 成品油、油价调整、汽油、柴油

## 配置

默认配置：
- 起始窗口: 2026-04-07
- 窗口间隔: 10 个工作日
- 检查时间: 每日 17:30
- 时区: Asia/Shanghai

## Quick Start

### 命令行使用

```bash
# 测试运行（强制检查）
python oil_price_monitor.py --test

# 查看下一个窗口期
python oil_price_monitor.py --next-window

# 查看最近公告
python oil_price_monitor.py --recent
```

## 输出示例

当检测到价格调整时，输出类似：

```
🛢️  成品油价格调整公告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 窗口期: 2026-04-07 (第1个窗口)
📢 发布机构: 国家发改委
🕐 发布时间: 2026-04-07 10:00

💵 调整内容:
  汽油每吨上调 300 元
  柴油每吨上调 290 元

🔗 原文链接: https://www.ndrc.gov.cn/...
```

## 技术实现

- 使用 `requests` 抓取发改委网站新闻列表
- 使用 `BeautifulSoup` 解析HTML
- 集成 `chinese-workdays` 计算工作日
- 输出 Markdown 格式，由 OpenClaw 捕获并推送到 Feishu

## Files

```
oil-price-monitor/
├── SKILL.md              # 技能说明
├── __init__.py           # 包入口
├── oil_price_monitor.py  # 主程序
├── config.yaml          # 配置文件（可选）
├── requirements.txt     # 依赖
└── README.md            # 详细文档
```

## License

MIT
# Oil Price Monitor - 发布前检查

## ✅ 文件清单

- SKILL.md ✅
- __init__.py ✅
- oil_price_monitor.py ✅
- requirements.txt ✅
- README.md ✅

## ⚠️ 注意事项

1. **依赖**: 需要 `requests`, `beautifulsoup4`, `lxml`，以及 `chinese-workdays` 技能
2. **运行时**: 需要在 OpenClaw 环境中运行，利用 stdout 捕获推送到 Feishu
3. **调度**: 应配置为 cron 任务每天 17:30 运行（逻辑内会判断窗口期）
4. **反爬**: 发改委网站可能有反爬措施，需合理设置 User-Agent 和请求频率
5. **数据准确性**: 价格调整信息提取需要持续优化

## 定价建议

考虑到这是一个监控通知类技能，建议：
- **免费**: 核心监控功能免费
- 或 **$0.01/月** 象征性收费

## 发布命令

```bash
cd /root/.openclaw/workspace/skills/oil-price-monitor
clawhub publish . --version "1.0.0" --changelog "Initial release: monitor NDRC oil price announcements and push notifications. Runs every 10 working days at 17:30 starting 2026-04-07." --tags "monitor,oil,price,ndrc,china,energy"
```
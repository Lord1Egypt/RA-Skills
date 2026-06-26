---
name: price-monitor-skill
description: 监控产品价格变化，自动对比历史价格并生成报告。支持价格搜索、历史追踪、变动提醒，适合竞品价格监控、商品降价提醒、价格趋势分析等场景。
author: MoltbookAgent
version: 1.0.0
tags: [price, monitor, product, competition, automation]
---

# Price Monitor Skill

## 一句话说明

监控产品价格变化，自动对比历史价格并生成报告。

## 适用场景

- 🏷️ 竞品价格监控（跟踪竞争对手产品定价）
- 🛍️ 商品降价提醒（心仪商品降价时及时知道）
- 📊 价格趋势分析（了解产品价格波动规律）
- 💰 采购时机判断（选择最佳购买时机）

## 快速开始

### 添加监控产品

```bash
python3 scripts/monitor_price.py --add "Cursor Pro" --url "https://cursor.com/pricing"
```

### 搜索并记录价格

```bash
# 1. 获取搜索建议
python3 scripts/monitor_price.py --search --product "Cursor Pro"

# 2. AI Agent 执行搜索
kimi_search(query="Cursor Pro 价格", limit=3)

# 3. 记录价格（根据搜索结果）
python3 scripts/monitor_price.py --record --product "Cursor Pro" --price "$20/月" --source "cursor.com"
```

### 生成报告

```bash
python3 scripts/monitor_price.py --report
```

## 功能详解

### 1. 产品管理

- 添加监控产品（支持自定义搜索关键词）
- 删除不再监控的产品
- 列出所有监控中的产品

### 2. 价格追踪

- 自动对比历史价格
- 检测价格上涨/下降
- 记录价格变更历史

### 3. 报告生成

- 生成完整价格监控报告
- 统计监控产品数量和检查次数
- 显示每个产品的最新价格和最后检查时间

## 使用示例

### 场景1: 监控编程工具价格

```bash
# 添加竞品
python3 scripts/monitor_price.py --add "Cursor Pro" --url "https://cursor.com/pricing"
python3 scripts/monitor_price.py --add "Windsurf Pro" --url "https://windsurf.com/pricing"
python3 scripts/monitor_price.py --add "GitHub Copilot" --url "https://github.com/features/copilot"

# 定期生成报告
python3 scripts/monitor_price.py --report
```

### 场景2: 设置定时监控

```bash
# 添加到 crontab，每天早上9点检查
0 9 * * * cd /root/.openclaw/workspace/skills/price-monitor-skill && python3 scripts/monitor_price.py --report
```

## 数据说明

### 存储位置

- **价格数据库**: `/tmp/price_monitor_db.json`
- **截图存档**: `/tmp/price_screenshots/`

### 数据库结构

```json
{
  "products": {
    "产品名称": {
      "url": "官网链接",
      "search_query": "搜索关键词",
      "added_at": "添加时间",
      "last_price": "最后记录价格",
      "last_check": "最后检查时间"
    }
  },
  "history": [
    {
      "product": "产品名称",
      "price": "价格",
      "source": "来源",
      "date": "记录时间",
      "change": "变动信息（可选）"
    }
  ]
}
```

## 高级用法

### 自定义数据路径

```bash
export PRICE_DB_FILE="/custom/path/price_db.json"
export PRICE_SCREENSHOT_DIR="/custom/path/screenshots"
python3 scripts/monitor_price.py --report
```

### 批量导入产品

```bash
# 创建一个产品列表文件 products.txt
# 格式: 产品名称|官网URL|搜索关键词

# 然后批量导入
while IFS='|' read -r name url query; do
  python3 scripts/monitor_price.py --add "$name" --url "$url"
done < products.txt
```

## 注意事项

1. **数据持久化**: 默认数据存储在 `/tmp` 目录，系统重启可能丢失。建议设置自定义路径到持久化存储。

2. **价格解析**: 当前版本需要手动解析 kimi_search 结果并记录价格。未来版本可能支持自动解析。

3. **并发安全**: 单文件 JSON 存储不适合高并发写入。

## 与其他 Skill 配合

| Skill | 配合方式 |
|-------|---------|
| kimi_search | 搜索产品价格信息 |
| browser | 官网价格截图存档 |
| weekly-report-skill | 价格变动周报 |
| auto-weekly-system | 定时价格监控报告 |

## 更新日志

### v1.0.0 (2025-03-26)
- ✅ 基础价格监控功能
- ✅ 历史价格对比
- ✅ 价格变动提醒
- ✅ 报告生成
- ✅ 错误处理完善

## 反馈与贡献

如有问题或建议，欢迎反馈。

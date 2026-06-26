# 价格监控技能 (Price Monitor Skill)

监控产品价格变化，自动对比历史价格并生成报告。

## 功能特点

- 🔍 **价格搜索**: 快速搜索产品最新价格信息
- 📊 **历史对比**: 自动对比历史价格，检测变化
- 🖼️ **截图存档**: 支持官网价格截图（需结合 browser 工具）
- 📈 **趋势报告**: 生成价格监控报告
- 🔔 **变动提醒**: 价格涨跌自动提示

## 安装

### 方式1: 使用技能包

```bash
clawhub install price-monitor-skill
```

### 方式2: 手动安装

```bash
cd /root/.openclaw/workspace/skills/price-monitor-skill
# 确保 scripts 目录可执行
chmod +x scripts/*.py
```

## 使用方法

### 添加监控产品

```bash
python3 scripts/monitor_price.py --add "Cursor Pro" --url "https://cursor.com/pricing"
```

### 搜索产品价格

```bash
python3 scripts/monitor_price.py --search --product "Cursor Pro"
```

> 注: 此命令会输出搜索建议，实际搜索需要 AI Agent 调用 kimi_search 工具

### 生成价格报告

```bash
python3 scripts/monitor_price.py --report
```

示例输出：
```
============================================================
📊 价格监控报告
============================================================
生成时间: 2025-03-26 10:30:00
------------------------------------------------------------

📦 监控产品列表:

   Cursor Pro
   ├─ 当前价格: $20/月
   ├─ 最后检查: 2025-03-26 10:15
   └─ 官网: https://cursor.com/pricing

   Windsurf Pro
   ├─ 当前价格: $15/月
   ├─ 最后检查: 2025-03-26 09:45
   └─ 官网: https://windsurf.com/pricing

📈 统计:
   监控产品数: 2
   已记录价格: 2
   历史记录数: 5
============================================================
```

### 列出所有产品

```bash
python3 scripts/monitor_price.py --list
```

### 删除产品

```bash
python3 scripts/monitor_price.py --remove "Cursor Pro"
```

## 完整工作流程

### 场景: 监控竞品价格

```bash
# 1. 添加要监控的产品
python3 scripts/monitor_price.py --add "Cursor Pro" --url "https://cursor.com/pricing"
python3 scripts/monitor_price.py --add "GitHub Copilot" --url "https://github.com/features/copilot"

# 2. 定期搜索价格（可设为定时任务）
# 由 AI Agent 执行: kimi_search 获取最新价格

# 3. 记录价格变化
# 由 AI Agent 调用: python3 scripts/monitor_price.py --record

# 4. 生成周报
python3 scripts/monitor_price.py --report
```

## 数据存储

- **数据库**: `/tmp/price_monitor_db.json`
- **截图目录**: `/tmp/price_screenshots/`

可通过环境变量自定义：

```bash
export PRICE_DB_FILE="/custom/path/price_db.json"
export PRICE_SCREENSHOT_DIR="/custom/path/screenshots"
```

## 结合 OpenClaw 使用

```python
# 在 Agent 中调用示例
# 1. 添加产品
exec(command="python3 skills/price-monitor-skill/scripts/monitor_price.py --add 'Cursor Pro' --url 'https://cursor.com/pricing'")

# 2. 搜索价格
kimi_search(query="Cursor Pro 价格", limit=3)
# 解析结果，提取价格

# 3. 记录价格
exec(command="python3 skills/price-monitor-skill/scripts/monitor_price.py --record --product 'Cursor Pro' --price '$20/月'")

# 4. 生成报告
exec(command="python3 skills/price-monitor-skill/scripts/monitor_price.py --report")
```

## 配置项

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `PRICE_DB_FILE` | `/tmp/price_monitor_db.json` | 价格数据库路径 |
| `PRICE_SCREENSHOT_DIR` | `/tmp/price_screenshots` | 截图保存目录 |

## 技术栈

- **数据采集**: kimi_search (网络搜索)
- **网页截图**: browser (OpenClaw browser 工具)
- **数据存储**: JSON 文件
- **报告生成**: Python CLI

## 作者

MoltbookAgent

## 许可证

MIT License

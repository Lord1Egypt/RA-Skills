---
name: 同花顺问财数据提取器
description: 从同花顺问财(iwencai.com) AI选股页面批量抓取涨停股票数据，使用 agent-browser 通过 Chrome CDP 连接操作浏览器，将数据存入 SQLite 数据库，并可导出为 Excel 汇总报告。适用场景：用户要求爬取/抓取/提取问财涨停数据、查询特定日期涨停股票、批量获取历史涨停记录、生成涨停数据报告。关键词触发：问财、iwencai、涨停数据、爬取涨停、抓取涨停、AI选股数据。
version: 1.0.0
tags:
  - 数据爬取
  - 涨停
  - A股
  - 同花顺
  - agent-browser
  - SQLite
  - Excel
---

# 同花顺问财数据提取器

## 环境配置

使用前确认以下路径（可从用户记忆或直接询问）：

| 配置项 | 默认值 |
|--------|--------|
| Python | `C:\Users\JacobWu\AppData\Local\Programs\Python\Python312\python.exe` |
| agent-browser | `C:\Users\JacobWu\AppData\Roaming\npm\agent-browser.cmd` |
| Chrome CDP端口 | `9222` |
| 数据库路径 | `D:\workbuddyclaw\iwencai_zt.db` |
| 数据目录 | `D:\workbuddyclaw\iwencai_data\` |

**启动 Chrome 调试模式（用户须手动执行一次）：**
```
chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\ChromeDebug
```
然后在 Chrome 中手动导航到 `https://www.iwencai.com/unifiedwh/stockpicker/`（AI选股页面）。

## 核心工作流

### 单日 / 批量爬取

使用 `scripts/crawl.py`，修改顶部配置后运行：

```bash
# Windows PowerShell/cmd，用 cmd /c 规避编码问题
cmd /c python D:\workbuddyclaw\iwencai_data\crawl.py
```

脚本关键参数（脚本顶部修改）：
- `TRADE_DAYS`：要爬取的日期列表（ISO格式 `YYYY-MM-DD`）
- `AGENT`：agent-browser 路径
- `DB_PATH`：SQLite 数据库路径

### 导出 Excel 报告

使用 `scripts/export_excel.py`，生成包含5个Sheet的汇总报告：

```bash
cmd /c python D:\workbuddyclaw\iwencai_data\export_excel.py
```

## 关键技术细节（必读）

### agent-browser 调用规范

```python
# 正确：不要加 --timeout 参数（子命令不支持，会报 Unknown command）
cmd = [AGENT, "--cdp", "9222"] + list(args)

# eval 输出是双层 JSON 包裹，需双层解析
raw = ab("eval", js)
step1 = json.loads(raw)
result = json.loads(step1) if isinstance(step1, str) else step1
```

### 搜索框定位

snapshot 中搜索框类型为 `textbox`，带 "筛选条件" 提示文字：
```python
for line in snap.split('\n'):
    if 'textbox' in line.lower() and 'ref=' in line:
        if '筛选条件' in line or '请输入您的' in line:
            m = re.search(r'ref=(e\d+)', line)
            if m:
                search_ref = m.group(1)
                break
```

### 分页翻页（Vue.js 兼容）

普通 `click()` 无效，必须用 `dispatchEvent` 触发 Vue 响应式事件：

```javascript
// 分页 class 是 .page-item（不是 .iw-asidetable-page-item）
var items = document.querySelectorAll('.page-item');
// 找到目标页码元素后：
var evt = new MouseEvent('click', {bubbles: true, cancelable: true, view: window});
a.dispatchEvent(evt);
```

### Windows 编码

所有 Python 脚本顶部加：
```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
```
运行脚本用 `cmd /c python script.py`（不用 PowerShell 直接调用）。

## 数据库结构

表名：`zt_stocks`

| 字段 | 类型 | 说明 |
|------|------|------|
| trade_date | TEXT | 交易日期 YYYY-MM-DD |
| stock_code | TEXT | 股票代码（6位） |
| stock_name | TEXT | 股票名称 |
| price | REAL | 收盘价 |
| change_pct | REAL | 涨跌幅(%) |
| zt_time | TEXT | 涨停时间 |
| zt_status | TEXT | 涨停状态 |
| volume | TEXT | 成交量 |
| amount | TEXT | 成交额 |
| first_zt_time | TEXT | 首次涨停时间 |
| lb_count | INTEGER | 连板数 |
| zt_type | TEXT | 涨停类型（首板/二连板等） |
| float_mv | TEXT | 流通市值 |
| vol_ratio | TEXT | 量比 |
| themes | TEXT | 所属题材（+分隔） |
| zt_tags | TEXT | 涨停标签 |
| total_mv | TEXT | 总市值 |

## 参考文档

- **爬取脚本完整实现**：见 `references/crawl_reference.md`
- **常见问题排查**：见 `references/troubleshooting.md`

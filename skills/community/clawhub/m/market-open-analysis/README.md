# 🌅 每日开盘分析 (market-open-analysis)

自动推送 WTI 原油和黄金的开盘预测报告。

## ⚡ 快速开始

### 1. 安装依赖

```bash
pip3 install -r ~/.openclaw/skills/market-open-analysis/requirements.txt
```

### 2. 安装定时任务

```bash
python3 ~/.openclaw/skills/market-open-analysis/install_cron.py install
```

### 3. 测试运行

```bash
# 手动测试收集
python3 ~/.openclaw/skills/market-open-analysis/main.py --stage collect

# 手动测试推送
python3 ~/.openclaw/skills/market-open-analysis/main.py --stage analyze
```

## 📋 推送示例

```
# 🌅 交易日早间行情播报
_生成时间：2026-03-17 05:30:00_

---

| 品种 | 收盘价 | 开盘预测 | 置信度 |
|------|--------|----------|--------|
| ⛽ 美油 | `94.92` | 🔴 高开 | 🟡 中 |
| 🥇 黄金 | `5002.59` | ⚪ 平开 | ⚪ 低 |

---

## 💡 预测原因

**⛽ 美油**：高开
  - 利好消息占优 (+3 条)
  - 信号强烈，置信度高
  - 隔夜消息：25 条（利好 3/利空 0）

**🥇 黄金**：平开
  - 消息面中性
  - 隔夜消息：16 条（利好 0/利空 0）

---
> ⚠️ _市场有风险，投资需谨慎_
```

## 🔧 配置

编辑 `config.py` 自定义设置：

```python
# 修改推送用户
DEFAULT_TARGET = "ou_xxxxxxxxxxxx"

# 修改 API Key
MX_API_KEY = "your_api_key"
```

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `main.py` | 主程序 |
| `config.py` | 配置文件 |
| `install_cron.py` | 定时任务安装脚本 |
| `requirements.txt` | Python 依赖 |

## 📊 数据源

- **价格数据**：CommodityPriceAPI（需自行配置 API Key）
- **新闻资讯**：东方财富妙想 API（需自行配置 API Key）

**包含的 API：**
- `commodity_price.py` - 国际商品价格查询（黄金、WTI 原油等）
- `mx_search` - 新闻资讯查询（通过 main.py 内置调用）

### 🔑 获取 API Key

| API | 官网 | 说明 |
|-----|------|------|
| **CommodityPriceAPI** | https://commoditypriceapi.com | 国际商品价格数据 |
| **东方财富妙想** | 联系官方 | 财经新闻资讯 |

## ⚠️ 注意事项

- 数据可能有 15 分钟延迟
- 非交易时间价格不变
- 预测仅供参考，不构成投资建议

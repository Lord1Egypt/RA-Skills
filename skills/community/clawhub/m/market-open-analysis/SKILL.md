---
name: market-open-analysis
description: |
  每日开盘分析 Skill - 每个交易日自动推送 WTI 原油和黄金的开盘预测报告
  
  **功能特性：**
  - 5:00 自动收集实时价格数据
  - 5:30 分析信息面并推送到飞书
  - 表格格式展示：品种、收盘价、开盘预测、置信度
  - 基于隔夜新闻的利好/利空分析
  
  **数据源：**
  - 价格数据：CommodityPriceAPI（黄金、WTI 原油）- **需自行配置 API Key**
  - 新闻资讯：东方财富妙想 API - **需自行配置 API Key**
  
  **推送格式：**
  | 品种 | 收盘价 | 开盘预测 | 置信度 |
  |------|--------|----------|--------|
  | ⛽ 美油 | `94.92` | 🔴 高开 | 🟡 中 |
  | 🥇 黄金 | `5002.59` | ⚪ 平开 | ⚪ 低 |
  
homepage: https://github.com/openclaw/skills
metadata:
  {
    "openclaw":
      {
        "emoji": "🌅",
        "requires": { "bins": ["python3", "curl"], "pip": ["requests"] },
        "install":
          [
            {
              "id": "requests",
              "kind": "pip",
              "package": "requests",
              "label": "安装依赖：pip3 install requests",
            },
          ],
      },
  }
---

# 每日开盘分析 Skill (market-open-analysis)

自动推送 WTI 原油和黄金的开盘预测报告。

---

## 📦 安装步骤

### 1. 安装 Skill

```bash
# 方式 1：使用 clawhub（推荐）
clawhub install market-open-analysis

# 方式 2：手动克隆
git clone <repo-url> ~/.openclaw/skills/market-open-analysis
```

### 2. 安装依赖

```bash
pip3 install requests
```

### 3. 配置 API Key（必填！）

#### 商品价格 API

1. 访问 https://commoditypriceapi.com 获取 API Key
2. 编辑文件：
```bash
vim ~/.openclaw/skills/market-open-analysis/commodity_price.py
```
3. 修改：
```python
API_KEY = "YOUR_COMMODITY_PRICE_API_KEY_HERE"  # ← 改为你的 Key
```

#### 新闻资讯 API

1. 联系东方财富妙想官方获取 API Key
2. 编辑文件：
```bash
vim ~/.openclaw/skills/market-open-analysis/config.py
```
3. 修改：
```python
MX_API_KEY = "YOUR_MX_API_KEY_HERE"  # ← 改为你的 Key
```

#### 推送配置

编辑 `config.py` 配置推送渠道和用户：
```bash
vim ~/.openclaw/skills/market-open-analysis/config.py
```

```python
# 推送用户 ID（必填）
# 飞书：ou_xxxxxxxxxxxx
# Telegram: username 或 user_id
# Discord: user_id 或 channel_id
DEFAULT_TARGET = "your_user_id"

# 推送渠道（可选，留空使用默认）
# 支持：feishu, telegram, discord, slack, whatsapp 等
DEFAULT_CHANNEL = ""  # 留空使用 OpenClaw 默认渠道
```

### 4. 设置定时任务

```bash
# 运行安装脚本
python3 ~/.openclaw/skills/market-open-analysis/install_cron.py
```

或手动添加：
```bash
crontab -e

# 添加以下两行（交易日 5:00 收集，5:30 推送）
0 5 * * 1-5 /usr/bin/python3 ~/.openclaw/skills/market-open-analysis/main.py --stage collect
30 5 * * 1-5 /usr/bin/python3 ~/.openclaw/skills/market-open-analysis/main.py --stage analyze
```

### 5. 测试运行

```bash
# 手动测试收集
python3 ~/.openclaw/skills/market-open-analysis/main.py --stage collect

# 手动测试推送
python3 ~/.openclaw/skills/market-open-analysis/main.py --stage analyze
```

---

## 📊 使用方式

### 命令行调用

```bash
# 收集价格数据（5:00）
python3 main.py --stage collect

# 分析并推送（5:30）
python3 main.py --stage analyze

# 指定日期
python3 main.py --stage analyze --date 2026-03-17

# 指定推送用户
python3 main.py --stage analyze --target ou_xxxxxxxxxxxx
```

### Python 调用

```python
import sys
sys.path.insert(0, '~/.openclaw/skills/market-open-analysis')
from main import collect_price_data, analyze_and_push

# 收集数据
data = collect_price_data()

# 分析推送
analyze_and_push(data, target_user="ou_xxxxxxxxxxxx")
```

---

## 📁 文件结构

```
~/.openclaw/skills/market-open-analysis/
├── SKILL.md                    # 技能说明文档
├── README.md                   # 快速开始
├── INSTALL.md                  # 安装指南
├── API_KEY.example.md          # API Key 配置指南
├── main.py                     # 主程序
├── commodity_price.py          # 价格查询 API（需配置 Key）
├── config.py                   # 配置文件（需配置 Key）
├── install_cron.py             # 定时任务安装脚本
└── requirements.txt            # Python 依赖
```

---

## 🔧 配置说明

### config.py

```python
# API 配置
MX_API_KEY = "mkt_xxxxxxxxxxxx"  # 东方财富妙想 API Key
MX_API_URL = "https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search"

# 推送配置
DEFAULT_TARGET = "ou_xxxxxxxxxxxx"  # 默认推送用户
DEFAULT_CHANNEL = "feishu"  # 推送渠道

# 时间配置
COLLECT_TIME = "05:00"  # 数据收集时间
PUSH_TIME = "05:30"     # 推送时间
```

### 定时任务

```bash
# 查看当前定时任务
crontab -l

# 编辑定时任务
crontab -e

# 删除定时任务
crontab -r
```

---

## 📈 数据源说明

### 价格数据 - CommodityPriceAPI

| 商品 | 代码 | 单位 |
|------|------|------|
| 黄金 | XAU | 美元/盎司 |
| WTI 原油 | WTIOIL-FUT | 美元/桶 |

API 端点：
- 最新价格：`/v2/rates/latest`
- 历史价格：`/v2/rates/{date}`

### 新闻资讯 - 东方财富妙想

查询关键词：
- **美油**：OPEC 产量、库存数据、地缘政治、供应中断
- **黄金**：美联储利率、非农数据、地缘政治、通胀预期

---

## 📋 推送格式

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

---

## 🔍 日志查看

```bash
# 查看最新日志
tail -f ~/openclaw/workspace/logs/market_open.log

# 查看历史报告
ls -la ~/openclaw/workspace/reports/
```

---

## ❓ 常见问题

### Q: 推送失败？
**A:** 检查：
1. OpenClaw 是否正常运行
2. 飞书授权是否有效
3. 目标用户 ID 是否正确

### Q: 价格为空？
**A:** 检查：
1. 网络连接是否正常
2. API Key 是否有效
3. 是否为交易日（周末休市）

### Q: 定时任务不执行？
**A:** 检查：
```bash
# 确认 cron 服务状态
systemctl status cron

# 确认定时任务
crontab -l

# 查看 cron 日志
grep CRON /var/log/syslog | tail
```

---

## 📝 更新日志

- **v1.0.0** - 初始版本
  - 支持 WTI 原油和黄金价格查询
  - 基于信息面的开盘预测
  - 飞书推送支持
  - 定时任务自动配置

---

## ⚠️ 注意事项

- 数据可能有 15 分钟延迟
- 非交易时间价格不变
- 预测仅供参考，不构成投资建议
- 需要访问国际 API 服务器

---

## 📞 支持

- 问题反馈：GitHub Issues
- 文档：~/.openclaw/skills/market-open-analysis/SKILL.md

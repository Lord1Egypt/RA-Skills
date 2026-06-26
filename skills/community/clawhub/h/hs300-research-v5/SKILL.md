---
name: hs300-research-v5
version: 5.2.0
description: >
  沪深300多因子投研系统。每当用户要求分析A股、沪深300、多因子选股、投研日报、
  股票评分、个股基本面分析、技术面分析时，必须使用此技能。
  支持8大类因子体系、多数据源自动降级（东方财富/Tushare Pro/AKShare/pywencai同花顺问财）、动态权重调整、信号共振检测、风险评级、自然语言问财查询。
metadata:
  author: Paudy
  category: finance
---

# 沪深300多因子投研系统 v5.2

AI Agent 个人投研技能 — 自动采集多源数据，计算 8 大类因子，生成结构化投研日报。

## v5.2 新增
- ✅ **pywencai(同花顺问财)** 集成 — 自然语言查询补充数据
- ✅ 投研日报新增「问财补充数据」板块（双金叉/资金流/北向/高股息）
- ⚠️ **JQData 已禁用** — 免费版数据截止2026-02-10，已从数据源剔除

## 什么时候使用

- 用户要求分析 A 股 / 沪深300
- 用户要求多因子选股 / 股票评分
- 用户要求生成投研日报
- 用户要求分析个股基本面或技术面
- 用户要求集合竞价量比分析
- 用户要求查看分红送配 / 资金流向 / 龙虎榜

## 核心工作流

### 1. 环境检查
```bash
cd hs300_research_system
python -c "import akshare; print('AKShare:', akshare.__version__)"
python data_fetcher.py  # 检查所有数据源状态
```

### 2. 运行完整分析
```bash
python full_analysis_v5.py
# 或新版：
python run_analysis_v3.py
```

运行结果包含：
- 沪深300成分股获取（AKShare）
- 日K线数据（东方财富 → Tushare Pro → AKShare）
- 基本面数据（Tushare Pro → 东方财富 → AKShare）
- 技术面分析（MACD/KDJ/均线）
- 多因子评分（8大类因子）
- **pywencai问财补充**（双金叉/资金流/北向资金/高股息）
- AKShare附加数据（分红送配/资金流/龙虎榜）

⚠️ JQData(聚宽) 已禁用：免费版数据仅到2026-02-10，不再使用。

### 3. 输出投研日报

报告结构：
```
📊 沪深300多因子投研日报
├── 🌍 市场环境（牛市/熊市/震荡市 + 建议仓位）
├── 📈 技术信号（MACD金叉/KDJ金叉/均线排列统计）
├── 💰 基本面概况（PE/PB/ROE均值）
├── ⭐ 潜力个股 TOP 10（代码/名称/价格/PE/ROE/得分/风险/涨幅）
├── ⚠️ 高风险个股
└── 💡 核心结论
```

### 4. 可选：集合竞价分析
```bash
python call_auction_analysis.py
```

## 数据源架构

| 数据源 | 覆盖内容 | 降级优先级 |
|--------|---------|-----------|
| pywencai(问财) | 自然语言查询/信号/资金流/北向/高股息 | 补充查询 |
| 东方财富HTTP | 日K线/实时行情/估值 | 1（主力） |
| AKShare | 成分股/分红/资金流/龙虎榜 | 2（补充） |
| Tushare Pro | 日线/财务/估值 | 3（需2000+积分） |
| SZSE/SSE | 交易所官方数据（辅助） | 4 |

### 自动降级链
```
获取日线: 东方财富HTTP → Tushare Pro → AKShare
获取估值: 东方财富 → Tushare Pro → AKShare
获取财务: Tushare Pro → AKShare
问财补充: pywencai（自然语言查询）
```

## pywencai(同花顺问财) 查询能力

集成 pywencai 后，支持以下自然语言查询：

| 查询类型 | 问财语句示例 |
|---------|------------|
| 信号检测 | `MACD金叉` / `KDJ金叉` / `MACD金叉并且KDJ金叉` |
| 资金流向 | `今日主力资金净流入排行` |
| 行业资金流 | `今日行业板块资金流向` |
| 北向资金 | `北向资金增持` |
| 涨停/跌停 | `今日涨停` |
| 高股息 | `股息率大于4%` |
| 高ROE | `ROE大于20%` |
| 自定义 | 任意自然语言问句 |

## 8 大类因子体系

| 因子类别 | 权重 | 指标 |
|---------|------|------|
| 估值 | 25% | PE/PB/PS |
| 质量 | 20% | ROE/ROA/毛利率/净利率 |
| 成长 | 15% | 营收增长/利润增长 |
| 动量 | 15% | 1月涨幅/3月涨幅 |
| 趋势 | 15% | MACD金叉/KDJ金叉/均线排列 |
| 波动率 | 5% | 年化波动率/ATR |
| 技术 | 5% | 突破信号 |
| 量能 | 5% | 量比/换手率 |

## 配置说明

### JQData（已禁用）
编辑 `jq_config.py`：
```python
JQ_USER = '手机号'
JQ_PASSWORD = '密码'
JQ_AUTH = False  # 免费版数据截止2026-02-10，已禁用
```

### Tushare Pro（可选）
编辑 `tushare_config.py`：
```python
TUSHARE_TOKEN = 'your_token'
TUSHARE_AUTH = True
```

### 依赖安装
```bash
pip install akshare tushare pywencai pandas numpy scipy
```

## pywencai 使用示例
```python
import pywencai
# 双金叉共振
res = pywencai.get(query='MACD金叉并且KDJ金叉')
# 今日资金流
res = pywencai.get(query='今日主力资金净流入排行', sort_key='主力资金净流入(元)')
```

## 注意事项

- JQData 免费版数据有日期范围限制（通常到最近几个月）
- 获取最新实时数据需要升级 JQData 会员（约298元/年）
- 公司网络可能拦截东方财富 push2 API
- 建议配置 OpenClaw Heartbeat 每日 08:30 自动运行

## 文件结构

```
hs300_research_system/
├── full_analysis_v5.py      # 主分析程序 v5.1
├── run_analysis_v3.py       # 主分析程序 v5.2（含pywencai补充数据）
├── data_fetcher.py          # 多数据源采集模块 v5.2
├── factor_calculator_v3.py  # 8大类因子计算器
├── pywencai_fetcher.py      # 同花顺问财数据获取器 ⭐新增
├── market_regime.py         # 市场环境判断
├── risk_management.py       # 风险管理和仓位建议
├── data_quality.py          # 数据质量检查
├── jq_config.py             # JQData 配置（已禁用）
├── tushare_config.py        # Tushare 配置
├── config.py                # 全局配置
├── call_auction_analysis.py # 集合竞价分析
├── requirements.txt         # 依赖清单
└── DATA_SOURCES.md          # 数据源详细说明 v5.2
```

## 输出格式

```
===================================================================
  沪深300多因子投研日报 v5.1
  生成时间: 2026-05-14 14:34:00
===================================================================

技术信号: MACD金叉:1 | KDJ金叉:3 | 均线多头:6 | 均线空头:6
基本面: PE均值=21.9 | ROE均值=2.9%

潜力个股 TOP 10:
  1. 000157 中联重科   价:9.68  PE:19.5  ROE:2.0%  营收:+24.9%  利润:+26.8%  得分:67.0  风险:低  1月:+9.9%
  2. 000338 潍柴动力   价:25.89 PE:19.0  ROE:3.5%  营收:+16.1%  利润:+44.5%  得分:62.0  风险:中  1月:+36.3%
  ...

高风险:
  ⚠ 601318 中国平安  得分:-0.18  PE:8.5  均线:空头
```

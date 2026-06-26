# 投资大师 Skill (Investment Gurus)

基于**中国顶级投资大师** + **国际投资大师**的价值投资分析Skill。

## 整合了20+位投资大师

### 🇨🇳 中国大师（7位）
段永平、张磊、李录、邱国鹭、王国斌、林园、但斌

### 🌍 国际大师（13位）
巴菲特、彼得林奇、木头姐、格雷厄姆、芒格、费雪、伯里、阿克曼、索罗斯、达里奥、达摩达兰、米勒、邓普顿

> 基于 ai-hedge-fund 项目研究 (55,797 Stars)

**四大功能**：
1. **数据抓取** - 腾讯财经API实时行情、均线、走势、板块
2. **智能分析** - 自动匹配大师方法，生成投资建议
3. **多维度评估** - 估值、基本面、技术面、情绪面
4. **Agent集成** - 对话式股票分析

### 数据源
- **腾讯财经API** (`web.ifzq.gtimg.cn`) - 实时/收盘行情
- 支持港股、美股、A股

## 快速开始

### 安装

```bash
pip install -e .
```

### 对话式分析（推荐）

```python
from investment_gurus import handle_user_message

# 用户问股票时自动触发
response = handle_user_message("茅台现在能买吗？")
print(response)
```

### 直接调用

```python
from investment_gurus import smart_analyze

# 分析股票
report = smart_analyze("贵州茅台")

# 对比大师方法
report = smart_analyze("宁德时代", guru="linyuan")

# 多大师对比
from investment_gurus import compare_all_methods
report = compare_all_methods("比亚迪")
```

### 命令行

```bash
# 分析股票
invest-guru analyze -s 贵州茅台

# 对比分析
invest-guru compare -s 比亚迪
```

## 功能详解

### 1. 数据抓取 (data_fetcher.py)

| 功能 | 说明 |
|------|------|
| 实时行情 | 价格、涨跌幅、成交量、PE、市值 |
| K线数据 | 历史走势 |
| 均线 | MA5/10/20/60 |
| 走势分析 | 1日/5日/1月/3月涨跌幅 |
| 板块信息 | 行业、细分 |
| 市场情绪 | VIX等 |

### 2. 智能分析 (smart_analyzer.py)

- 自动抓取实时数据
- 根据行业自动匹配最合适的大师方法
- 生成完整分析报告

**分析报告结构**：
1. 实时行情
2. 近期走势
3. 均线位置
4. 板块信息
5. 大师方法分析
6. 综合建议

### 3. Agent集成 (agent_handler.py)

当用户问股票相关问题时自动触发：

| 用户输入 | 触发 |
|----------|------|
| "茅台怎么样" | ✅ |
| "宁德时代能买吗" | ✅ |
| "用林园的方法看比亚迪" | ✅ |
| "今天天气" | ❌ |

## 大师方法对比

| 大师 | 核心理念 | 擅长行业 | 关键指标 |
|------|----------|----------|----------|
| 段永平 | 能力圈+商业模式 | 消费、科技 | 商业模式、竞争壁垒 |
| 张磊 | 超长期+动态护城河 | 科技、新能源 | 长期增长、企业家精神 |
| 林园 | 嘴巴经济+垄断 | 白酒、医药 | 成瘾性、定价权 |
| 但斌 | 伟大企业+时间玫瑰 | 消费、互联网 | 伟大企业、长期持有 |
| 邱国鹭 | 三好原则+逆向 | 金融、周期 | 好行业、好公司、好价格 |
| 李录 | 安全边际+文明视角 | 消费、科技 | 安全边际、跨市场 |
| 王国斌 | 幸运行业+企业 | 消费、制造 | 行业+企业+价格 |

## 使用示例

```python
# 1. 简单分析
from investment_gurus import smart_analyze
print(smart_analyze("贵州茅台"))

# 2. 指定大师方法
print(smart_analyze("片仔癀", guru="linyuan"))

# 3. 对比分析
from investment_gurus import compare_all_methods
print(compare_all_methods("宁德时代"))

# 4. 快速获取行情
from investment_gurus import quick_quote
print(quick_quote("腾讯"))
```

## 项目结构

```
investment_gurus/
├── investment_gurus/
│   ├── __init__.py           # 入口
│   ├── base.py               # 基类定义
│   ├── data_fetcher.py       # 数据抓取
│   ├── smart_analyzer.py     # 智能分析
│   ├── agent_handler.py      # Agent集成
│   ├── analyzer.py           # 综合分析器
│   ├── duan.py               # 段永平
│   ├── zhanglei.py           # 张磊
│   ├── liu_lu.py             # 李录
│   ├── qiuguoluo.py          # 邱国鹭
│   ├── wangguobin.py         # 王国斌
│   ├── linyuan.py            # 林园
│   └── danbing.py            # 但斌
├── SKILL.md
├── README.md
├── setup.py
├── requirements.txt
└── manifest.json
```

## 依赖

- Python 3.8+
- yfinance (Yahoo Finance数据)
- pandas
- numpy
- click (CLI)

## License

MIT License
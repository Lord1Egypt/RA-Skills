# 投资大师 Skill

基于**中国顶级投资大师** + **国际投资大师**的价值投资分析Skill。

## 整合了20+位投资大师

### 🇨🇳 中国大师（7位）
段永平、张磊、李录、邱国鹭、王国斌、林园、但斌

### 🌍 国际大师（13位）
巴菲特、彼得林奇、木头姐、格雷厄姆、芒格、费雪、伯里、阿克曼、索罗斯、达里奥、达摩达兰、米勒、邓普顿

## 功能

### 1. 股票数据自动抓取
- 实时行情（价格、涨跌幅、成交量、PE、市值）
- K线历史数据
- 均线系统（MA5/10/20/60）
- 近期走势（1日/5日/1月/3月）
- 板块/行业信息
- 市场情绪指标

### 2. 智能投资分析
- 自动识别股票
- 根据行业自动匹配最合适的大师方法
- 生成完整分析报告（7个部分）
- 多大师对比分析

### 3. Agent对话式集成
- 当用户问股票时自动触发
- 支持指定大师方法（"用林园的方法看XXX"）
- 支持对比分析（"XXX和YYY哪个好"）

## 安装

```bash
pip install -e .
```

## 使用方法

### Python API

```python
from investment_gurus import smart_analyze, handle_user_message

# 方法1: 对话式触发（Agent用）
response = handle_user_message("茅台现在能买吗？")

# 方法2: 直接分析
report = smart_analyze("贵州茅台")

# 方法3: 指定大师
report = smart_analyze("片仔癀", guru="linyuan")

# 方法4: 多大师对比
from investment_gurus import compare_all_methods
report = compare_all_methods("宁德时代")
```

### 命令行

```bash
invest-guru analyze -s 贵州茅台
invest-guru compare -s 比亚迪
```

## 支持的股票

- A股：茅台、五粮液、片仔癀、宁德时代、比亚迪、平安、招商银行等
- 港股：腾讯、阿里、美团、京东等
- 美股：苹果、微软、谷歌、亚马逊、特斯拉等

## 投资大师

### 🇨🇳 中国大师（7位）

| 大师 | 方法 | 擅长行业 |
|------|------|----------|
| 段永平 | 能力圈+商业模式 | 消费、科技 |
| 张磊 | 超长期+动态护城河 | 科技、新能源 |
| 林园 | 嘴巴经济+垄断 | 白酒、医药 |
| 但斌 | 伟大企业+时间玫瑰 | 消费、互联网 |
| 邱国鹭 | 三好原则+逆向 | 金融、周期 |
| 李录 | 安全边际+文明 | 消费、科技 |
| 王国斌 | 幸运行业+企业 | 消费、制造 |

### 🌍 国际大师（13位）

| 大师 | 方法 | 核心指标 |
|------|------|----------|
| 巴菲特 | 合理价格买伟大公司 | ROE>15%, PE<25, 自由现金流 |
| 彼得林奇 | 寻找10倍股(GARP) | PEG<1, 营收增长>15% |
| 木头姐 | 创新颠覆 | 创新指数, TAM, 研发>10% |
| 格雷厄姆 | 安全边际 | PE<15, PB<1.5, NCAV |
| 芒格 | Wonderful Business | 商业模式, 护城河, 定价权 |
| 费雪 | 成长股调研 | 研发投入, 毛利率, 市场份额 |
| 伯里 | 深度价值+逆向 | 隐蔽资产, PB, 清算价值 |
| 阿克曼 | 激进投资 | 催化剂, 估值修复空间 |
| 索罗斯 | 宏观对冲 | 宏观周期, 流动性, 政策 |
| 达里奥 | 全天候 | 经济周期, 利率, 通胀 |
| 达摩达兰 | DCF估值 | DCF, EV/EBITDA, 相对估值 |
| 米勒 | 价值成长合一 | ROIC>15%, 成长性 |
| 邓普顿 | 逆向投资 | PE历史低位, VIX高位 |

### 📊 分析维度（4个）

| 维度 | 指标 |
|------|------|
| 估值 | PE, PB, PS, EV/EBITDA, DCF, 股息率 |
| 基本面 | ROE, 毛利率, 净利率, 营收增长 |
| 技术面 | MA5/20/60, RSI, MACD, 成交量 |
| 情绪 | 新闻情绪, 机构评级, 资金流向, VIX |

## 触发条件

当用户输入包含以下内容时自动触发：
- 股票名称（茅台、宁德时代等）
- 6位股票代码
- 关键词：股票、买、卖、投资、分析、走势、行情、估值

## 文件结构

```
investment_gurus/
├── investment_gurus/
│   ├── __init__.py           # 入口
│   ├── base.py               # 基类
│   ├── data_fetcher.py       # 数据抓取
│   ├── smart_analyzer.py     # 智能分析
│   ├── agent_handler.py      # Agent集成 (核心)
│   ├── tencent_api.py        # 腾讯财经API (实时行情)
│   ├── international_gurus.py # 国际大师分析
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

## 数据源

- **腾讯财经API** (`web.ifzq.gtimg.cn`) - 实时/收盘行情
- **Yahoo Finance** (yfinance) - 备用数据源
- 支持：港股、美股、A股
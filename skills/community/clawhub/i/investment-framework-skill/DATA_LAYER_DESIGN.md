# 投资框架技能包 - 数据获取层设计方案

> **版本**：v1.0.0  
> **创建时间**：2026-03-20  
> **设计原则**：免费优先、用户可选、透明配置

---

## 一、设计目标

### 核心原则

1. **免费优先**：默认使用无需 API Key 的免费数据源
2. **用户触发**：数据获取在用户使用时实时进行，不内置静态数据
3. **付费可选**：无免费数据时提供付费方案，用户自行配置密钥
4. **透明配置**：所有数据源、限制、费用清晰告知用户
5. **降级可用**：API 不可用时提供手动输入方案

---

## 二、技能数据需求分析

### 2.1 数据需求矩阵

| 技能 | 股价行情 | 财报数据 | 行业数据 | 宏观数据 | 新闻事件 | 数据依赖度 |
|------|---------|---------|---------|---------|---------|-----------|
| **value-analyzer** | 🔴 必需 | 🔴 必需 | 🟡 可选 | ⚪ 不需要 | ⚪ 不需要 | 高 |
| **moat-evaluator** | 🟡 可选 | 🔴 必需 | 🟡 可选 | ⚪ 不需要 | 🟡 可选 | 高 |
| **stock-picker** | 🔴 必需 | 🔴 必需 | 🟡 可选 | ⚪ 不需要 | ⚪ 不需要 | 高 |
| **industry-analyst** | 🟡 可选 | 🟡 可选 | 🔴 必需 | 🟡 可选 | 🟡 可选 | 中 |
| **cycle-locator** | 🟡 可选 | ⚪ 不需要 | ⚪ 不需要 | 🔴 必需 | 🟡 可选 | 中 |
| **portfolio-designer** | 🟡 可选 | ⚪ 不需要 | ⚪ 不需要 | 🟡 可选 | ⚪ 不需要 | 低 |
| **global-allocator** | 🟡 可选 | ⚪ 不需要 | ⚪ 不需要 | 🟡 可选 | ⚪ 不需要 | 低 |
| **simple-investor** | 🔴 必需 | 🔴 必需 | 🟡 可选 | ⚪ 不需要 | ⚪ 不需要 | 高 |
| **intrinsic-value-calculator** | 🔴 必需 | 🔴 必需 | ⚪ 不需要 | ⚪ 不需要 | ⚪ 不需要 | 高 |
| **asset-allocator** | ⚪ 不需要 | ⚪ 不需要 | ⚪ 不需要 | 🟡 可选 | ⚪ 不需要 | 低 |
| **decision-checklist** | ⚪ 不需要 | ⚪ 不需要 | ⚪ 不需要 | ⚪ 不需要 | ⚪ 不需要 | 无 |
| **future-forecaster** | ⚪ 不需要 | ⚪ 不需要 | ⚪ 不需要 | 🟡 可选 | 🔴 必需 | 中 |
| **bias-detector** | ⚪ 不需要 | ⚪ 不需要 | ⚪ 不需要 | ⚪ 不需要 | ⚪ 不需要 | 无 |
| **second-level-thinker** | ⚪ 不需要 | ⚪ 不需要 | ⚪ 不需要 | ⚪ 不需要 | 🟡 可选 | 低 |

**图例**：
- 🔴 必需：核心功能依赖，无数据无法工作
- 🟡 可选：增强功能，有数据更好，无数据可降级
- ⚪ 不需要：不依赖外部数据

---

### 2.2 技能分组

#### **高数据依赖组（需优先实现数据层）**

| 技能 | 核心数据需求 | 免费方案 | 付费方案 |
|------|------------|---------|---------|
| value-analyzer | 股价、PE、PB、财报 | 腾讯/新浪 API | Tushare Pro |
| stock-picker | 股价、PEG、增长率 | 腾讯/新浪 API | Tushare Pro |
| simple-investor | 股价、PE、PB、ROE | 腾讯/新浪 API | Tushare Pro |
| intrinsic-value-calculator | 股价、财报、现金流 | 东方财富 API | Tushare Pro |
| moat-evaluator | 财报、市场份额 | 手动输入 | 理杏仁/Choice |

#### **中数据依赖组（可降级运行）**

| 技能 | 核心数据需求 | 免费方案 | 付费方案 |
|------|------------|---------|---------|
| industry-analyst | 行业规模、增速 | 搜索 + 手动 | 券商研报 |
| cycle-locator | GDP、利率、债务 | 统计局/央行 | Wind/CEIC |
| future-forecaster | 趋势新闻、技术动态 | 搜索 | 付费资讯 |

#### **低数据依赖组（无需数据层）**

| 技能 | 说明 |
|------|------|
| portfolio-designer | 配置比例计算，无需实时数据 |
| global-allocator | 配置建议，无需实时数据 |
| asset-allocator | 生命周期配置，无需实时数据 |
| decision-checklist | 决策清单检查，无需数据 |
| bias-detector | 认知偏差检查，无需数据 |
| second-level-thinker | 思维模型，无需数据 |

---

## 三、数据源架构

### 3.1 数据源分层

```
┌─────────────────────────────────────────┐
│          用户配置层 (config.yaml)         │
│  - API Key 管理                          │
│  - 数据源优先级                          │
│  - 降级策略                              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          数据获取层 (data_fetcher)        │
│  - 统一接口                              │
│  - 自动降级                              │
│  - 缓存管理                              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          数据源层 (providers)             │
│  ┌─────────┬─────────┬─────────┐        │
│  │ 免费层  │ 注册层  │ 付费层  │        │
│  │腾讯/新浪│ Tushare │ 理杏仁  │        │
│  │东方财富│ 聚宽    │ Choice  │        │
│  └─────────┴─────────┴─────────┘        │
└─────────────────────────────────────────┘
```

---

### 3.2 免费数据源（无需 API Key）

#### **A. 腾讯财经 API**

**用途**：实时股价、大盘指数

**接口**：
```python
# 大盘指数
http://qt.gtimg.cn/q=s_sh000001,s_sz399001,s_sz399006

# 个股行情
http://qt.gtimg.cn/q=sh600519,sz000001
```

**数据**：
- 当前价、涨跌幅、涨跌额
- 成交量、成交额
- 总市值、市盈率

**优点**：
- ✅ 无需 API Key
- ✅ 实时数据
- ✅ 稳定可靠

**缺点**：
- ⚠️ 非 JSON 格式，需解析
- ⚠️ 有频率限制（~100 次/分钟）

---

#### **B. 新浪财经 API**

**用途**：实时股价、大盘指数

**接口**：
```python
http://hq.sinajs.cn/list=s_sh000001,s_sz399001
```

**数据**：同腾讯

**优点**：
- ✅ 无需 API Key
- ✅ 实时数据

**缺点**：
- ⚠️ 有时返回 Forbidden
- ⚠️ 有频率限制

---

#### **C. 东方财富 API**

**用途**：个股行情、财报数据

**接口**：
```python
# 实时行情
https://push2.eastmoney.com/api/qt/stock/get?secid=1.600519&fields=f43,f44,f45,f46,f47,f48,f49

# 财报数据
https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_F10_FINANCE_MAINFINADATA&secucode=600519.SH
```

**数据**：
- 股价、市值、市盈率
- 营收、净利润、ROE
- 资产负债率

**优点**：
- ✅ 数据全面
- ✅ 支持财报

**缺点**：
- ⚠️ 字段代码复杂
- ⚠️ 需解析回调函数

---

### 3.3 注册免费数据源（需 API Key）

#### **A. Tushare Pro**

**网址**：https://tushare.pro/

**免费额度**：
- 注册送 100 积分
- 可获取：日线行情、基本面数据、财报

**限制**：
- 基础数据：100 积分够用
- 高频数据：需更多积分（付费或签到）

**配置方式**：
```yaml
data_sources:
  tushare:
    enabled: true
    token: "YOUR_TOKEN_HERE"  # 用户自行填写
```

---

#### **B. 聚宽 JoinQuant**

**网址**：https://www.joinquant.com/

**免费额度**：
- 注册送免费额度
- 可获取：历史行情、财务数据

**限制**：
- 实时数据需付费

---

### 3.4 付费数据源（可选）

#### **A. 理杏仁**

**网址**：https://www.lixinger.com/

**价格**：基础版免费，高级版 ¥299/年

**数据**：
- 估值数据（PE/PB 历史分位）
- 财务数据
- 行业数据

---

#### **B. 财联社 VIP**

**价格**：¥380/年

**数据**：
- 实时新闻
- 政策解读
- 行业动态

---

## 四、配置文件设计

### 4.1 用户配置文件模板

**文件位置**：`~/.investment_framework/config.yaml`

```yaml
# 投资框架数据源配置

# 数据源优先级（从高到低）
data_sources:
  priority:
    - tencent      # 腾讯财经（免费，优先）
    - sina         # 新浪财经（免费，备用）
    - eastmoney    # 东方财富（免费，财报）
    - tushare      # Tushare Pro（需 API Key）
    - lixinger     # 理杏仁（付费，可选）

# API Key 配置
api_keys:
  tushare:
    token: ""  # 用户填写：https://tushare.pro/user/token
    enabled: false  # 默认关闭，用户开启后填写 token
  
  lixinger:
    token: ""  # 用户填写
    enabled: false

# 降级策略
fallback:
  # API 失败时是否使用缓存
  use_cache: true
  cache_ttl: 3600  # 缓存有效期（秒）
  
  # API 全部失败时是否允许手动输入
  allow_manual_input: true
  
  # 超时设置（秒）
  timeout: 5

# 数据偏好
preferences:
  # A 股市场代码前缀
  a_share_prefix:
    sh: "sh"  # 沪市
    sz: "sz"  # 深市
  
  # 默认显示字段
  default_fields:
    - price
    - change_percent
    - pe
    - pb
    - market_cap
```

---

### 4.2 配置初始化流程

```python
def init_config():
    """初始化配置文件"""
    config_path = os.path.expanduser("~/.investment_framework/config.yaml")
    
    if not os.path.exists(config_path):
        # 创建默认配置
        create_default_config(config_path)
        print("✅ 配置文件已创建：~/.investment_framework/config.yaml")
        print("📝 请编辑配置文件填写 API Key（可选）")
        print("🔗 Tushare 注册：https://tushare.pro/user/register")
    else:
        print("✅ 配置文件已存在")
```

---

## 五、数据获取模块设计

### 5.1 统一数据接口

```python
class DataFetcher:
    """统一数据获取接口"""
    
    def __init__(self, config_path=None):
        self.config = load_config(config_path)
        self.cache = CacheManager(ttl=self.config['fallback']['cache_ttl'])
    
    def get_quote(self, symbol: str) -> Quote:
        """获取股价行情"""
        # 1. 检查缓存
        if cached := self.cache.get(f"quote:{symbol}"):
            return cached
        
        # 2. 按优先级尝试数据源
        for source in self.config['data_sources']['priority']:
            try:
                if source == 'tencent' and self.config['data_sources']['tencent']:
                    quote = fetch_tencent(symbol)
                    self.cache.set(f"quote:{symbol}", quote)
                    return quote
                elif source == 'tushare' and self.config['api_keys']['tushare']['enabled']:
                    quote = fetch_tushare(symbol)
                    self.cache.set(f"quote:{symbol}", quote)
                    return quote
            except Exception as e:
                log_error(f"{source} failed: {e}")
                continue
        
        # 3. 全部失败，返回降级方案
        if self.config['fallback']['allow_manual_input']:
            return prompt_manual_input(symbol)
        
        raise DataFetchError("All data sources failed")
    
    def get_financials(self, symbol: str) -> Financials:
        """获取财报数据"""
        # 类似逻辑...
```

---

### 5.2 数据源实现

```python
# 腾讯财经
def fetch_tencent(symbol: str) -> Quote:
    """腾讯财经 API"""
    code = convert_to_tencent_code(symbol)
    url = f"http://qt.gtimg.cn/q={code}"
    
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    
    # 解析非 JSON 格式
    data = parse_tencent_quote(response.text)
    return Quote(**data)

# 东方财富
def fetch_eastmoney_financials(symbol: str) -> Financials:
    """东方财富财报 API"""
    secucode = convert_to_eastmoney_code(symbol)
    url = f"https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_F10_FINANCE_MAINFINADATA&secucode={secucode}"
    
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    
    data = response.json()
    return Financials(**data)

# Tushare（需 API Key）
def fetch_tushare(symbol: str) -> Quote:
    """Tushare Pro API"""
    ts.set_token(config['api_keys']['tushare']['token'])
    pro = ts.pro_api()
    
    df = pro.daily(ts_code=symbol, start_date='20260320')
    return Quote.from_tushare(df)
```

---

### 5.3 降级方案

```python
def prompt_manual_input(symbol: str) -> Quote:
    """手动输入降级方案"""
    print(f"⚠️  无法自动获取 {symbol} 数据")
    print("📝 请手动输入以下数据（或按回车跳过）：")
    
    price = input("当前价格：")
    pe = input("市盈率 (PE)：")
    pb = input("市净率 (PB)：")
    
    return Quote(
        symbol=symbol,
        price=float(price) if price else None,
        pe=float(pe) if pe else None,
        pb=float(pb) if pb else None,
        source="manual"
    )
```

---

## 六、技能集成方案

### 6.1 技能调用数据层

```python
# value-analyzer 示例
def analyze_stock(symbol: str):
    """价值分析"""
    # 1. 获取数据
    fetcher = DataFetcher()
    quote = fetcher.get_quote(symbol)
    financials = fetcher.get_financials(symbol)
    
    # 2. 执行分析
    result = {
        'symbol': symbol,
        'price': quote.price,
        'pe': quote.pe,
        'pb': quote.pb,
        'roe': financials.roe,
        'debt_ratio': financials.debt_ratio,
    }
    
    # 3. 格雷厄姆标准检查
    graham_check = check_graham_standards(result)
    
    # 4. 安全边际计算
    margin_of_safety = calculate_margin_of_safety(result)
    
    return {
        **result,
        'graham_check': graham_check,
        'margin_of_safety': margin_of_safety,
        'recommendation': generate_recommendation(result)
    }
```

---

### 6.2 工作流集成

**文件**：`workflows/scripts/market-scan-realtime.py`

```python
#!/usr/bin/env python3
"""
实时市场扫描脚本
使用免费 API 获取大盘数据
"""

from data_fetcher import DataFetcher

def main():
    fetcher = DataFetcher()
    
    # 获取大盘数据
    indices = fetcher.get_indices(['000001.SH', '399001.SZ', '399006.SZ'])
    
    # 生成报告
    report = generate_market_report(indices)
    
    # 输出到飞书文档
    publish_to_feishu(report)

if __name__ == '__main__':
    main()
```

---

## 七、用户体验流程

### 7.1 首次使用

```
用户：分析贵州茅台

AI: 📊 正在获取贵州茅台数据...

    ✅ 股价：¥1,392.00 (+8.10%)  [来源：腾讯财经]
    ✅ 市盈率：28.5  [来源：东方财富]
    ✅ 市净率：7.2  [来源：东方财富]
    ⚠️  ROE: 未获取到（免费数据源限制）
    
    💡 提示：如需 ROE 等财务数据，可配置 Tushare Pro（免费）
       注册：https://tushare.pro/user/register
       配置：编辑 ~/.investment_framework/config.yaml
    
    是否继续分析？（基于已有数据）
    [是/否/配置 API]
```

---

### 7.2 API 配置引导

```
用户：配置 API

AI: 🔧 数据源配置向导
    
    1️⃣  Tushare Pro（推荐，免费）
        - 数据：股价、财报、ROE、增长率
        - 限制：注册送 100 积分，够用
        - 注册：https://tushare.pro/user/register
        
        是否现在注册？[是/跳过]
    
    2️⃣  理杏仁（付费，¥299/年）
        - 数据：估值历史分位、行业数据
        - 适合：深度研究用户
        
        是否需要？[是/跳过]
    
    ✅ 配置完成！
    配置文件：~/.investment_framework/config.yaml
```

---

### 7.3 降级方案

```
用户：分析某小公司股票

AI: ⚠️  数据获取失败
    
    ❌ 腾讯财经：超时
    ❌ 新浪财经：Forbidden
    ❌ 东方财富：无数据
    
    💡 降级方案：
    1. 手动输入数据（推荐）
    2. 使用缓存数据（2 小时前）
    3. 跳过数据，仅做框架分析
    
    请选择：[1/2/3]
```

---

## 八、实施计划

### 阶段 1：核心数据层（P0）

**时间**：2026-03-20 ~ 2026-03-22

**任务**：
- [ ] 创建 `data_fetcher/` 模块
- [ ] 实现腾讯/新浪/东方财富 API
- [ ] 实现配置文件管理
- [ ] 实现缓存管理
- [ ] 集成到 value-analyzer、stock-picker

**交付**：
- `data_fetcher/__init__.py`
- `data_fetcher/providers/tencent.py`
- `data_fetcher/providers/sina.py`
- `data_fetcher/providers/eastmoney.py`
- `config/default.yaml`

---

### 阶段 2：注册数据源（P1）

**时间**：2026-03-23 ~ 2026-03-25

**任务**：
- [ ] 实现 Tushare Pro 集成
- [ ] 实现 API Key 安全存储
- [ ] 添加配置向导
- [ ] 集成到 intrinsic-value-calculator

**交付**：
- `data_fetcher/providers/tushare.py`
- `data_fetcher/config_wizard.py`

---

### 阶段 3：高级数据源（P2）

**时间**：2026-03-26 ~ 2026-03-28

**任务**：
- [ ] 实现理杏仁集成（可选付费）
- [ ] 实现行业数据获取
- [ ] 实现宏观数据获取
- [ ] 集成到 industry-analyst、cycle-locator

**交付**：
- `data_fetcher/providers/lixinger.py`
- `data_fetcher/providers/macro.py`

---

### 阶段 4：优化与文档（P3）

**时间**：2026-03-29 ~ 2026-03-31

**任务**：
- [ ] 编写用户文档
- [ ] 编写 API 文档
- [ ] 添加单元测试
- [ ] 性能优化（并发、缓存）

**交付**：
- `docs/DATA_LAYER_GUIDE.md`
- `tests/test_data_fetcher.py`

---

## 九、文件结构

```
investment-framework-skill/
├── data_fetcher/
│   ├── __init__.py
│   ├── core.py              # 核心 DataFetcher 类
│   ├── config.py            # 配置管理
│   ├── cache.py             # 缓存管理
│   ├── exceptions.py        # 异常定义
│   └── providers/
│       ├── __init__.py
│       ├── tencent.py       # 腾讯财经
│       ├── sina.py          # 新浪财经
│       ├── eastmoney.py     # 东方财富
│       ├── tushare.py       # Tushare Pro（需 API Key）
│       ├── lixinger.py      # 理杏仁（付费）
│       └── macro.py         # 宏观数据
├── config/
│   ├── default.yaml         # 默认配置模板
│   └── schema.yaml          # 配置 Schema
├── workflows/
│   └── scripts/
│       ├── market-scan-realtime.py  # 实时市场扫描
│       └── data-fetch-test.py       # 数据获取测试
├── docs/
│   └── DATA_LAYER_GUIDE.md  # 数据层使用指南
└── tests/
    ├── test_data_fetcher.py
    └── test_providers.py
```

---

## 十、风险与应对

### 风险 1：免费 API 不稳定

**应对**：
- 多数据源冗余（腾讯→新浪→东方财富）
- 缓存机制（5 分钟 TTL）
- 手动输入降级

---

### 风险 2：API Key 泄露

**应对**：
- 配置文件权限 600（仅用户可读）
- 不提交到 Git（.gitignore）
- 提示用户妥善保管

---

### 风险 3：数据准确性

**应对**：
- 多源交叉验证
- 异常值检测
- 用户确认机制

---

## 十一、总结

### 设计亮点

1. ✅ **免费优先**：默认使用无需 API Key 的免费数据
2. ✅ **用户触发**：数据在使用时实时获取，不内置静态数据
3. ✅ **付费可选**：提供付费方案，用户自行决定
4. ✅ **降级可用**：API 失败时可手动输入
5. ✅ **透明配置**：所有数据源清晰告知

### 下一步

1. 确认设计方案
2. 开始阶段 1 实施（P0 核心数据层）
3. 逐步推进 P1/P2/P3

---

*创建时间：2026-03-20*  
*版本：v1.0.0*

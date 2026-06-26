# 数据获取层集成指南

> **版本**：v1.1.0  
> **更新**：2026-03-20  
> **状态**：✅ Tushare 已启用（120 积分）

---

## 📊 数据源状态

| 数据源 | 状态 | 数据类型 | 积分需求 |
|--------|------|---------|---------|
| 腾讯财经 | ✅ 启用 | 股价、大盘 | 免费 |
| 新浪财经 | ✅ 启用 | 股价、大盘 | 免费 |
| 东方财富 | ✅ 启用 | 股价、财报 | 免费 |
| Tushare Pro | ✅ 启用 | 日线行情 | 120 积分 |

---

## 🎯 已集成技能

### 1. value-analyzer（价值分析师）

**脚本**：`value-analyzer/scripts/analyze-value.py`

**功能**：
- 获取实时股价（Tushare/腾讯/新浪/东方财富）
- 获取财报数据（东方财富）
- 格雷厄姆标准分析
- 安全边际计算

**用法**：
```bash
cd investment-framework-skill
python3 value-analyzer/scripts/analyze-value.py 600519.SH
```

**输出示例**：
```
📊 价值分析：600519.SH
==================================================
📈 获取股价数据...
✅ 600519.SH: ¥1452.87 (PE: 28.5, PB: 7.2)
   数据来源：tushare

📋 获取财报数据...
✅ ROE: 30.5%, 负债率：15.2%
   数据来源：eastmoney

🔍 格雷厄姆标准分析...
建议：部分符合，需进一步分析
置信度：中
```

---

### 2. stock-picker（选股专家）

**待集成**：PEG 计算、林奇 13 条原则检查

---

### 3. simple-investor（简单投资者）

**待集成**：邱国鹭选股三要素分析

---

## 🔧 数据获取层使用

### 基础用法

```python
from data_fetcher import DataFetcher

# 初始化
fetcher = DataFetcher()

# 获取股价
quote = fetcher.get_quote('600519.SH')
print(f"贵州茅台：¥{quote.price}")
print(f"数据来源：{quote.source}")

# 获取财报
financials = fetcher.get_financials('600519.SH')
print(f"ROE: {financials.roe}%")

# 获取大盘指数
indices = fetcher.get_indices()
for idx in indices:
    print(f"{idx.symbol}: {idx.price} ({idx.change_percent}%)")
```

### 数据源优先级

```
1. Tushare Pro（如果 token 有效）
2. 腾讯财经（免费）
3. 新浪财经（免费）
4. 东方财富（免费）
```

### 自动降级

```python
try:
    # 优先使用 Tushare
    quote = fetcher.get_quote('600519.SH')
    print(f"数据来源：{quote.source}")
except DataFetchError as e:
    # 自动降级到免费数据源
    print(f"使用备用数据源：{e}")
```

---

## 📝 配置文件

**位置**：`~/.investment_framework/config.yaml`

```yaml
api_keys:
  tushare:
    token: 'b2c8dcae10cf07e7d2e6e60088cef1b9404a7cf759d55bd7260ac8d9'
    enabled: true  # ✅ 已启用

data_sources:
  priority:
    - tushare   # Tushare 优先
    - tencent   # 腾讯备用
    - sina      # 新浪备用
    - eastmoney # 东方财富备用
```

---

## 🧪 测试脚本

### 测试 Tushare

```bash
python3 workflows/scripts/test-tushare.py
```

### 测试数据获取层

```bash
python3 workflows/scripts/test-data-fetcher.py
```

### 测试价值分析

```bash
python3 value-analyzer/scripts/analyze-value.py 600519.SH
```

---

## ⚠️ 注意事项

### Tushare 积分限制

| 接口 | 需求积分 | 当前状态 |
|------|---------|---------|
| 日线行情 | 100 | ✅ 可用（120 积分） |
| 股票列表 | 100 | ✅ 可用 |
| 大盘指数 | 100 | ✅ 可用 |
| 财务指标 | 300 | ❌ 需要更多积分 |
| PE/PB 数据 | 300 | ❌ 需要更多积分 |
| 财务报表 | 500 | ❌ 需要更多积分 |

### 解决方案

1. **每日签到**：https://tushare.pro/user/profile
2. **邀请好友**：每人 20 积分
3. **多源融合**：Tushare（股价）+ 东方财富（财报）

---

## 🚀 下一步

### 待集成技能

- [ ] stock-picker（选股专家）
- [ ] simple-investor（简单投资者）
- [ ] intrinsic-value-calculator（内在价值计算器）
- [ ] industry-analyst（行业分析师）

### 优化计划

- [ ] 多源数据融合（Tushare + 东方财富）
- [ ] 缓存优化（减少 API 调用）
- [ ] 错误处理优化
- [ ] 添加更多测试用例

---

*最后更新：2026-03-20*

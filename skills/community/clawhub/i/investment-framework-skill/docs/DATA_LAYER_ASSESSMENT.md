# 数据接入层评估报告 📊

**评估时间**：2026-04-07  
**评估标准**：OUTPUT_SCHEMA.md v1.0.0 信源分级验证要求

---

## 🎯 评估目标

根据 `OUTPUT_SCHEMA.md` 要求，所有投资分析技能的输出必须包含：

```json
{
  "sources": [
    {
      "name": "数据源名称",
      "type": "官方 | 媒体 | 第三方",
      "reliability": "S | A | B | C",
      "url": "原始链接"
    }
  ]
}
```

**信源分级标准**：
| 等级 | 标识 | 来源类型 | 使用方式 |
|------|------|---------|---------|
| S | 🟢 | 官方文档、监管机构、财报 | 直接引用 |
| A | 🟡 | 权威媒体、知名分析师 | 交叉验证后使用 |
| B | 🟠 | 技术社区、行业分析 | 多源印证或标注不确定性 |
| C | 🔴 | 匿名论坛、单一来源 | 仅作线索，标注「待核实」 |

---

## 📁 现有数据层架构

### 1. data_fetcher（investment-framework-skill）

**位置**：`investment-framework-skill/data_fetcher/`

**核心功能**：
- ✅ 统一数据接口（DataFetcher 类）
- ✅ 多数据源冗余（腾讯/新浪/东方财富）
- ✅ 自动降级链
- ✅ 缓存管理（内存 + 文件）
- ✅ 配置管理

**支持数据源**：
| 数据源 | 类型 | 可靠性 | 状态 |
|--------|------|--------|------|
| 腾讯财经 | 第三方 | A | ✅ |
| 新浪财经 | 第三方 | A | ✅ |
| 东方财富 | 第三方 | A | ✅ |
| Tushare Pro | 第三方 | A | ⏳ 需 API Key |

**数据类型**：
- ✅ 个股行情（股价、PE、PB、市值）
- ✅ 大盘指数
- ✅ 财报数据（营收、利润、ROE）
- ✅ 基金数据

### 2. data_layer（独立模块）

**位置**：`/home/admin/.openclaw/workspace/data_layer/`

**核心功能**：
- ✅ 统一数据 API（DataAPI 类）
- ✅ Provider 抽象层
- ✅ 缓存管理
- ✅ 配置管理
- ✅ 异常处理

**支持数据源**：
| 数据源 | 类型 | 可靠性 | 状态 |
|--------|------|--------|------|
| 腾讯财经 | 第三方 | A | ✅ |
| 新浪财经 | 第三方 | A | ✅ |
| 东方财富 | 第三方 | A | ✅ |
| Tushare | 第三方 | A | ⏳ |
| SearXNG | 搜索引擎 | B | ✅ |
| QVeris | 付费 API | A | ✅ |

---

## ✅ 符合性分析

### 1. 信源分级支持

**要求**：每个数据源必须有明确的可靠性等级（S/A/B/C）

**现状**：
- ✅ data_fetcher 有数据源标识（source 字段）
- ✅ data_layer 有 Provider 抽象
- ❌ **缺少**：信源分级元数据（S/A/B/C）
- ❌ **缺少**：数据源类型分类（官方/媒体/第三方）

**改进建议**：
```python
# 在 Provider 配置中添加信源分级
PROVIDERS = {
    "tencent": {
        "name": "腾讯财经",
        "type": "第三方",
        "reliability": "A",
        "url": "https://stockapp.finance.qq.com/"
    },
    "eastmoney": {
        "name": "东方财富",
        "type": "第三方",
        "reliability": "A",
        "url": "https://www.eastmoney.com/"
    },
    "sse": {
        "name": "上海证券交易所",
        "type": "官方",
        "reliability": "S",
        "url": "http://www.sse.com.cn/"
    }
}
```

### 2. 数据来源追溯

**要求**：每个数据点都能追溯到原始来源

**现状**：
- ✅ Quote 对象包含 source 字段
- ✅ Financials 对象包含 source 字段
- ✅ 缓存管理保留来源信息
- ❌ **缺少**：原始 URL 链接

**改进建议**：
```python
@dataclass
class Quote:
    symbol: str
    price: float
    # ... 其他字段
    source: str  # 数据源名称
    source_url: str  # 原始数据链接 ⭐ 新增
    reliability: str  # S/A/B/C ⭐ 新增
```

### 3. 数据质量验证

**要求**：数据质量说明和局限性

**现状**：
- ✅ 缓存 TTL 管理
- ✅ 超时控制
- ✅ 异常处理
- ❌ **缺少**：数据质量评分
- ❌ **缺少**：数据 freshness 标识

**改进建议**：
```python
@dataclass
class DataQuality:
    freshness: str  # "realtime" | "delayed" | "stale"
    completeness: float  # 0-1 完整度
    accuracy: str  # "verified" | "unverified"
    limitations: List[str]  # 局限性说明
```

### 4. 多源交叉验证

**要求**：关键数据需要多源验证

**现状**：
- ✅ 自动降级链（腾讯→新浪→东财）
- ✅ 故障转移
- ❌ **缺少**：多源对比验证
- ❌ **缺少**：数据一致性检查

**改进建议**：
```python
def get_quote_verified(self, symbol: str) -> Quote:
    """获取多源验证的报价"""
    quotes = []
    for provider in [tencent, sina, eastmoney]:
        try:
            quotes.append(provider.get_quote(symbol))
        except:
            continue
    
    # 检查数据一致性
    if len(quotes) >= 2:
        max_diff = max(q.price for q in quotes) - min(q.price for q in quotes)
        if max_diff > threshold:
            # 数据不一致，发出警告
            log_warning(f"多源数据不一致：{quotes}")
    
    return quotes[0]  # 返回第一个成功的数据
```

---

## 📊 功能对比

### data_fetcher vs data_layer

| 功能 | data_fetcher | data_layer | 需求满足 |
|------|-------------|-----------|---------|
| 统一接口 | ✅ | ✅ | ✅ |
| 多数据源 | ✅ 3 个 | ✅ 6 个 | ✅ |
| 自动降级 | ✅ | ✅ | ✅ |
| 缓存管理 | ✅ | ✅ | ✅ |
| 信源分级 | ❌ | ❌ | ⚠️ 需改进 |
| 原始 URL | ❌ | ❌ | ⚠️ 需改进 |
| 数据质量 | ❌ | ❌ | ⚠️ 需改进 |
| 多源验证 | ❌ | ❌ | ⚠️ 需改进 |
| 基金数据 | ✅ | ❌ | ✅ |
| 个股数据 | ✅ | ✅ | ✅ |

---

## 🎯 改进方案

### Phase 1：信源分级（1 天）

**目标**：为所有 Provider 添加信源分级元数据

**步骤**：
1. 在 `config.py` 中添加 PROVIDERS 配置
2. 在 `Quote`和`Financials` 中添加 reliability 字段
3. 更新所有 Provider 返回数据
4. 在技能输出中传递信源信息

**代码示例**：
```python
# data_fetcher/config.py
PROVIDERS = {
    "tencent": {
        "name": "腾讯财经",
        "type": "第三方",
        "reliability": "A",
        "url": "https://stockapp.finance.qq.com/"
    },
    # ... 其他 Provider
}

# data_fetcher/core.py
@dataclass
class Quote:
    # ... 现有字段
    source_reliability: str = "A"  # S/A/B/C
    source_type: str = "第三方"  # 官方/媒体/第三方
```

### Phase 2：数据质量（2 天）

**目标**：添加数据质量评估和 freshness 标识

**步骤**：
1. 创建 DataQuality 数据类
2. 在缓存层添加 freshness 检查
3. 实现数据完整性验证
4. 添加数据质量评分

### Phase 3：多源验证（2 天）

**目标**：实现关键数据的多源交叉验证

**步骤**：
1. 实现多源数据获取
2. 添加数据一致性检查
3. 实现冲突解决策略
4. 添加验证日志

### Phase 4：技能集成（1 天）

**目标**：在技能输出中传递完整信源信息

**步骤**：
1. 更新所有技能的数据获取调用
2. 在输出 Schema 中包含完整 sources
3. 添加数据质量说明
4. 测试验证

---

## ✅ 结论

### 当前状态

**整体评分**：70/100

| 维度 | 得分 | 说明 |
|------|------|------|
| **基础功能** | 90/100 | ✅ 统一接口、多数据源、降级链完善 |
| **信源分级** | 40/100 | ❌ 缺少 S/A/B/C 分级元数据 |
| **数据追溯** | 60/100 | ⚠️ 有 source 字段，缺少 URL |
| **数据质量** | 50/100 | ⚠️ 有缓存 TTL，缺少质量评分 |
| **多源验证** | 30/100 | ❌ 仅有降级，无交叉验证 |

### 是否满足要求？

**短期**（立即使用）：✅ **基本满足**
- 可以开始使用现有数据层
- 技能输出包含基础 source 信息
- 信源分级可以手动标注

**长期**（完整合规）：⚠️ **需要改进**
- 需要 5-6 天完成 Phase 1-4 改进
- 重点是信源分级和多源验证
- 数据质量评估需要完善

---

## 📝 建议

### 立即行动（今天）

1. **手动标注信源分级**
   - 在技能输出中手动添加 reliability 字段
   - 示例：`"sources": [{"name": "东方财富", "reliability": "A"}]`

2. **更新技能示例**
   - 在 risk-assessor 和 sentiment-analyzer 中完善 sources
   - 确保每个示例都有完整的信源信息

### 本周完成（Phase 1）

1. **data_fetcher 信源分级**
   - 添加 PROVIDERS 配置
   - 更新 Quote/Financials 数据类
   - 测试验证

2. **技能集成**
   - 更新所有技能调用数据层
   - 确保输出包含完整信源信息

### 下周完成（Phase 2-3）

1. **数据质量评估**
2. **多源交叉验证**

---

**总结**：现有数据层基础扎实，70% 满足要求。完成 Phase 1 后可达 90% 合规。

*数据质量决定分析质量，信源分级是信任的基石。* 📊

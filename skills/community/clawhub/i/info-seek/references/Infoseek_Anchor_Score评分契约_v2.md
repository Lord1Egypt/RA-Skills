# Infoseek Anchor Score 评分契约（四维 base + 加权层 + 兜底）

> **历史命名勘误（v1.8.2 P1）**：本契约 v1.5.0 曾称「五维」，v2.0.0 将信任源合并为独立
> 加权层后，核心评分为**四维 base**（interaction / topic_match / credibility / llm_readability）；
> 信任源 / 领域 / 跨平台 / 语义为 base 之上的可选加权层，非并列维度。文件名「五维契约_v1.5」
> 已更名「评分契约_v2」，消除与 SKILL §5.1「唯一口径 = v2 四维」的矛盾。

> 版本：v2.0.2（mod-v）｜ 状态：✅ 现行唯一口径（四维 base）｜ 对齐全：`scripts/infoseek_core_v2.py` / `core/anchor_score_v2.py` / `scripts/anchor_adapter.py`
>
> **唯一聚合真源（v1.8.3 · skill 版本）= `core/anchor_score_v2.aggregate_score_v2`**：
> 复活 → 衰减 → 跨平台 → 语义 → 信任 → 领域 → 分类七环节单点实现，两个评分入口
> （链A `compute_final_score_v2` / 链B `infoseek_core_v2.score_source`）**同源委托**，
> 任何消费方禁止自算聚合公式。详见 §6。

## 1. 评分公式（四维 base；v2.0.0 起信任源/领域/跨平台/语义为独立加权层）

```
Anchor_Score = 互动深度×20% + 主题一致性×30% + 来源可信度×40% + LLM 上下文可读性×10%
```

完整链路（**聚合段由 `aggregate_score_v2` 单点实现**，v1.8.3）：

```
base_score（四维 0-100，compute_base_score_v2）
  ↓ 以下七环节 = aggregate_score_v2（唯一聚合真源）
  → 复活门控（base ≥90 时保底 70 + whitelist_triggered 标志）
  → 时间衰减（days_since_published 因子：1.0/0.9/0.7/0.5/0.3）
  → 跨平台第 6 维（可选，占 5%）
  → Jaccard 语义第 8 维（可选，占 5%）
  → Trust 信任源加权（tier1-4 白名单，0-30 分）
  → Domain 领域加权（可选，0-`domain_bonus_cap()`，默认 20，env 可配）
  → clamp 到 0-100 → 分类（阈值常量 CLASSIFY_CORE=70 / CLASSIFY_POTENTIAL=40）
```

> **口径事实（v1.8.3 实测 40004 组样本）**：复活门控 `base≥90 → max(base,70)` 对数值
> **恒为 no-op**（base≥90 必然 ≥70，差值全为 +0.00），仅 `whitelist_triggered` 标志位有效。
> 保留该环节是为返回 schema 兼容 + 未来门控扩展挂点，**不产生评分实效**。
> v1.2 的「白名单 + TOP3 + 峰值门控」双层复活已于 v1.8.2 显式废弃（`top3_triggered` 恒 False）。

## 2. 门控规则

| 分数 | 分类 | 处理 |
|------|------|------|
| ≥70 | 🟢 核心 | 自动进入采集队列 |
| 40-69 | 🟡 潜力 | 需人工确认 |
| <40 | ❌ 噪声 | 过滤 |

## 3. v1.0.1 语义兜底（P0-1 修复）

真实搜索源（`search_web` 返回 `url/title`，无 `interaction/topic_match/credibility` 三字段）时：

```
base_score = max(
    compute_semantic_similarity(title+snippet, subject),   # Jaccard 三跑关键词
    int(string_containment(title+snippet, subject) × 0.8)  # 主题词包含比例
)
```

- 三字段齐全 → 走四维 base 原路径（不触发兜底）
- source 自带 `score` 字段 → 尊重该值（`base_score <= 0` 才兜底）

## 4. 信任源加权（core/trust_sources.py）

| Tier | 权重 | 来源 |
|------|------|------|
| 1 官方权威 | 25-30 | gov / arxiv / iso / astm / 知网 / ieee 等 |
| 2 行业头部 | 15-25 | 头部企业 / 官方媒体 / zhihu / github 等 |
| 3 一般可信 | 5-15 | 虎嗅 / 钛媒体 / 财新 等 |
| 4 低优先 | 0-5 | 未命中白名单（默认） |

领域：`tech-research` / `market-research` / `finance-research` / `policy-research` / `competitor-intel` / `general`。

## 5. 兼容性

- **表述纠错（v1.8.3）**：原文称「v2 API `score_source()` 与 v1 `calculate_score()` 行为一致」
  并不准确 —— 二者是**两条不同的链**：`calculate_score()` 是链A 的兼容 shim（转调
  `compute_final_score_v2`，逐字段恒等，见 `test_score_consistency_v178`）；
  `score_source()` 是链B（MCP 工具 `score_source` 入口，base 三态入口 + 领域探测 +
  KB 交集加权）。v1.8.3 前两者**聚合公式各不相同**（链B 自算且缺衰减环节）；
  现两链共用 `aggregate_score_v2` → 同一 base 必得同一 final（见 §6）
- 链A 为纯函数：不修改 source dict；返回体 `version` 为 algo-v（`2.0.2`），
  链B 返回体 `version` 为 algo-v（`1.2.0`）—— 均为下游契约，**不随 skill 版本变动**
- `method='tfidf'` 已废弃 → 内部重定向到 Jaccard（DeprecationWarning）

## 6. 三链路口径一致性（v1.8.3 · §8.4 验收总闸闭合）

「三链路」= **base / 复活 / 信任加权**。v1.7.8 的 `test_score_consistency_v178` 仅覆盖 base，
复活与信任加权零覆盖 → v1.8.3 实测坐实 **8 处分叉**（D1-D8）并全部收敛。

### 6.1 两链职责边界

| | 链A `compute_final_score_v2` | 链B `infoseek_core_v2.score_source` |
|---|---|---|
| 定位 | 唯一完整评分口径（四维 base） | 兼容入口 / 编排层（MCP 工具 `score_source`）|
| base 来源 | `compute_base_score_v2`（四维加权） | 三态入口，由 **`base_origin`** 标注：`four_dim`（含四维字段 → 转调链A）/ `v1_score`（仅 `score`）/ `semantic_fallback`（§3 兜底）/ `empty` |
| 聚合 | **委托 `aggregate_score_v2`** | **委托 `aggregate_score_v2`**（同源）|
| trust_bonus | 纯信任源 0-30 | = `trust_bonus_base`(0-30) + `kb_bonus`(0-12)，合计 0-42 |
| domain_bonus | 计入 final | **计入 final**（v2.3.2 收口：经聚合真源 `aggregate_score_v2` 环节化计入；仅承载纯领域特定信任段 0-20，KB 交集段已在 `trust_bonus`，故不双重计分）|
| tier | `resolve_tier_v2` → `get_tier_level`（1-4）| `get_tier_level`（1-4，同源）|

> base 差异是**有意的入口差异**（链B 须兼容 v1 输入与真实搜索源），非口径分叉。
> 分叉的定义是：**同一 base 经不同聚合公式得不同 final** —— 该分叉已消除
> （`test_three_chain_v183` T2 以 90 组 base×days×trust 网格断言 final + classification 全恒等）。

### 6.2 信任加权三个单源

| 单源 | 职责 | 消费方 |
|------|------|--------|
| `trust_sources.compute_trust_bonus` | 白名单 pattern 加权 0-30 | 链A / 链B |
| `trust_sources.get_tier_level` | tier 1-4（v1.8.3 起走 `query_pattern_index` 缓存，20.4x）| 链A `resolve_tier_v2` / 链B |
| `domain_router.trust_source_bonus` | profile 信任源词加权（url +5 / platform +3）| `apply_profile_to_score` / `compute_domain_bonus_v2` / `_compute_domain_bonus` |
| `domain_router.kb_intersect_bonus` | KB 交集加分（单 KB +8 / 多 KB 额外 +4，**合计 +12**；profile `intersect_boost` 可覆盖基准）| 链A（双参）/ 链B（默认单参，可传 `domain_profile` 走双参）/ `trusted_kb` |
| `domain_router.domain_bonus_cap()` | 领域加权上限（env `INFOSEEK_DOMAIN_BONUS_CAP`，默认 20，**动态读取**）| 上述三处消费点统一委托 |

### 6.3 守护

`tests/test_three_chain_v183.py` **63 check**：T1 聚合单点性（含「链B 自算公式仅存于降级分支」
结构断言）/ T2 90 组网格恒等 / T3 复活（标志位同源 + no-op 事实 + `top3_triggered` 恒 False）/
T4 衰减（含 D1 分类翻转级回归）/ T5 信任加权（cap env 三方同值 + tier ∈1-4 + KB 双参）/
T6 分类阈值单源 / T7 `base_origin` 四态 / T8 文档口径 / T9 零回归契约（空源=0、prefer_kb +12、algo-v 1.2.0）。

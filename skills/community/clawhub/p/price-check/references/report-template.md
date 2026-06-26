# price-check v0.3 输出格式与 verdict 阈值

> agent 拿到 `bin/price_check.py` 的 JSON 后照本文件渲染最终回复。本文件是规范，调整 verdict 规则要 **同时改本文件 + `bin/price_check.py:compute_verdict`** 保持两边一致。

## 数据流（v0.2 三层过滤）

```
原始 items (≈22-60)
   ↓ [1] 价格层：_filter_outliers   剔除 price < raw_median × 0.3
clean_items                          → removed_outliers
   ↓ [2] 信任层 + [3] 相关性层 一次完成（_select_best_deal）
   ↓   condition ∈ SUSPICIOUS         → flagged_items
   ↓   relevance.score < 0.75 或 ambiguous=True  → low_relevance_items
   ↓   剩下进 candidates，按 trusted_shop × condition 三档优先级
best_deal (or None)
```

`stats` 基于 clean_items；`stats_raw` 保留原始统计；`all_platforms` 仍是原始全量 items（每条已含 `condition` / `condition_hits` / `is_trusted_shop` / `relevance` 字段）。

## condition 关键词词典（v0.2 = 7 档）

排查顺序（**第一个命中的是最终 condition**；前面已命中就不再往下查）：

| condition | 关键词 |
|-----------|------|
| `bundle` | 套装 / 组合装 / 礼盒装 / +iPhone / +iPad / +AirPods / +MacBook / +Apple / +保护壳 / +钢化膜 / +保护套 |
| `accessory` | 配件 / 支架 / 充电支架 / 充电底座 / 底座 / 保护套 / 保护壳 / 保护膜 / 屏幕膜 / 钢化膜 / 贴膜 / 皮套 / 替换头 / 替换 / 除螨仪 / 除螨头 / 电池组件 / Dok / Dok免打孔 / 适用于 / 兼容 |
| `refurbished` | 翻新 / 认证翻新 / 官翻 / renewed / 二手 / 9成新 / 样机 / 展示机 / 演示机 / 展品 / 模型机 |
| `activation_questionable` | 需签收激活 / 需现场激活 / 已激活 / 已拆封 / 拆封 |
| `parallel_import` | 港版 / 美版 / 日版 / 韩版 / 欧版 / 海外版 / 海外 / 全球版 / 国际版 |
| `trusted_domestic` | 国行 / 大陆版 / 国行正品 / 国行原封 |
| `unknown` | 默认（命不中以上任何一档）|

`SUSPICIOUS_CONDITIONS = {refurbished, bundle, activation_questionable, accessory}` —— 永不进 best_deal。

## trusted_shop 识别

- **字面量**：`Apple产品京东自营` / `苹果京东自营` / `Apple官方旗舰店` / `苹果官方旗舰店`
- **正则**：`京东自营` / `^.*官方旗舰店$` / `^Apple.*旗舰店$` / `^.*天猫官方旗舰店$`

任一命中即 `is_trusted_shop = true`。

## 标题相关性（v0.2 新增）

### Tokenization
`_tokenize(query)` 用 whitespace 分隔。中英文混合用户自己加空格，例：

- `"iPhone 16 Pro 256G"` → `["iPhone", "16", "Pro", "256G"]`
- `"戴森 V12"` → `["戴森", "V12"]`
- `"Switch 2 港版"` → `["Switch", "2", "港版"]`

### Score 计算
对每个 token 在 title 里做大小写不敏感的 substring 匹配，特殊处理 `G ↔ GB` 等价（"256G" 命中 "256GB"，反之亦然）。

```
score = matched / total_tokens
threshold = 0.75 (4 token query 至少命中 3 个；2-3 token query 必须全命中)
```

### Ambiguous detection
`MODEL_PATTERNS` 扫描 title 里的型号 token（V\d+ / iPhone\d+ / Switch\d+ / OLED / Lite / Galaxy S\d+ / Pixel\d+），不同型号 ≥ 3 个 → `ambiguous = True`。

例："戴森dysonV8 V10 V12 V15V16 G5..." → V8/V10/V12 三个不同 → ambiguous=True。

`relevance.score < 0.75` 或 `ambiguous=True` 的条目都进 `low_relevance_items`，不进 best_deal candidates。

## best_deal 选择优先级

按下表从上到下，第一个有候选的层级出 best_deal：

| 优先级 | 条件 | 含义 |
|-------|------|-----|
| 1 | `is_trusted_shop` AND `condition in {trusted_domestic, unknown}` | 自营/旗舰店 + 全新国行 → 最优 |
| 2 | `is_trusted_shop` AND `condition == parallel_import` | 自营/旗舰店 + 水货 → 次优 |
| 3 | `condition == trusted_domestic` AND NOT `is_trusted_shop` | 第三方店但明说国行 → 备选 |
| ❌ | `condition in SUSPICIOUS_CONDITIONS` | **永不**进 best_deal，转 `flagged_items` |
| ❌ | `relevance.score < 0.75` 或 `relevance.ambiguous` | **永不**进 best_deal，转 `low_relevance_items` |
| ❌ | 都不满足 | best_deal = null，verdict = "数据质量不足，无法可信推荐" |

## verdict 阈值（v0.2）

设 `price = best_deal.price`，`med = stats.median`，`n = stats.count`：

| 条件 | verdict | verdict_reason 模板 |
|------|---------|--------------------|
| 原始 items 为空 | 无数据 | shopmind 未返回任何商品记录 |
| `removed > 0` 且 `n < 5` | 数据噪音过多，无法判断 | 原始 R 条中 K 条疑似噪音（< ¥T），剔除后仅 n 条，低于 5 条最低样本 |
| `n == 0` | 无数据 | 剔除后无可用价格记录 |
| `med <= 0` | 无数据 | 中位数为 0（n=N），无法判断 |
| `best_deal == null`（信任层 × 相关性层全过滤）| 数据质量不足，无法可信推荐 | 剔除噪音后 n 条中无满足相关性 + 信任层条件的候选 |
| `history.trap` 命中（v0.3）| 别买 | 历史数据命中先涨后降：{trap} |
| `price / med ≤ 0.85` | 强烈推荐 | 可信最低价 ¥X（locator）比 N 平台中位数 ¥Y 低 K%；匹配度 M% (a/b token)，缺 [...] |
| `price / med ≤ 0.95` | 可以买 | 同上格式 |
| `price ≤ med` | 再等等 | 可信最低价 ¥X（locator）接近 N 平台中位数 ¥Y（仅低 K%）；匹配度 ... |
| `price > med` | 再等等 | 可信最低价 ¥X（locator）高于 N 平台中位数 ¥Y K%；匹配度 ... |

> v0.3 历史价接入后会扩"别买"档（`history.trap` 已预留接入点；`price > history.avg_30d` 也降档）。

## trap_warning 文案规则（v0.2）

文案分四段拼接，按命中情况追加；末尾固定追加 v0.3 提醒。

| 触发 | 文案片段 |
|------|---------|
| `removed` 非空 且 `clean_count < 5` | `⚠️ 剔除前 N 条价格远低于中位数（< ¥T，最低 ¥X），疑似配件/同关键词噪音；剔除后仅剩 M 条，不足 5 条最低样本，verdict 不可信。建议加更精确关键词重跑。` |
| `removed` 非空 且 `clean_count ≥ 5` | `⚠️ 已自动剔除 N 条疑似配件/噪音商品（价格区间 ¥X–¥Y，阈值 ¥T）` |
| `flagged_count > 0` | `⚠️ 已过滤 N 条配件/翻新/套装/激活可疑商品（详见 flagged_items 字段）` |
| `low_relevance_count > 0` | `⚠️ 已过滤 N 条标题不匹配的商品（详见 low_relevance_items），其中 K 条是多型号关键词堆砌` |
| best_deal 存在 + 安全候选里有比 best_deal 更便宜的非可信店铺商品 | `💡 还有 N 条更低价候选未进 best_deal：最低 ¥X（店铺名），因不是可信店铺被设计跳过；如愿冒店铺风险可参考 Top 5。` |
| 任一以上命中 | 末尾追加：`v0.3 接入历史价后会再加一道'先涨后降'识别。` |

如果以上都没命中（既没剔除也没过滤）→ `trap_warning = null`。

## 输出 schema 字段约定

| 字段 | 类型 | 何时为 null | 备注 |
|------|------|------------|------|
| `product` | str | 永不 | 用户原始查询 |
| `verdict` | str | 永不 | 七档枚举值之一 |
| `verdict_reason` | str | 永不 | 一句话说明依据，必含具体数值 + 匹配度 |
| `best_deal` | obj | verdict 是"无数据 / 数据噪音过多 / 数据质量不足"时 | 含 platform / shopName / price / title / condition / is_trusted_shop / **relevance** / goodsId / source / url |
| `best_deal.url` | str | **v0.2 永远 null** | v0.3 按需并发调 shopmind detail 拉链接 |
| `history_summary` | obj | **v0.2 永远 null** | v0.3 由 HistoryProvider 填 |
| `all_platforms` | list | 原始为空时 `[]` | **原始全量**，每条含 condition / condition_hits / is_trusted_shop / relevance |
| `removed_outliers` | list | 没剔除时 `[]` | 价格层剔除（配件/噪音）|
| `flagged_items` | list | 没过滤时 `[]` | 信任层过滤（refurbished / bundle / accessory / activation_questionable）|
| `low_relevance_items` | list | 没过滤时 `[]` | **v0.2 新增**：相关性层过滤（score<0.75 或 ambiguous）|
| `stats` | obj | 永不 | **剔除后** clean_items 的 min/max/median/stdev/count |
| `stats_raw` | obj | 永不 | **原始** 全部条目的统计 |
| `trap_warning` | str | 既没剔除也没过滤也没低价非可信候选时 null | 见上节 |
| `_meta` | obj | 永不 | skill / version / history_provider / data_source / outlier_filter / min_clean_samples / **relevance_threshold** / **ambiguous_model_count** / condition_classifier / trusted_shop_classifier / suspicious_conditions |

## 人类报告模板 — v0.4.1 "C 模式"（混合：导购数据 + 综合判断 + 完整透明）

> **v0.4.1 关键升级（C 模式）**：导购数据优先展示 + Molty 综合判断单独成段 + 完整数据透明，**三段都不能省**。
> - 即使 Molty 判断"不建议买"，**也必须**完整展示 best_deal / Top 3 / 历史价段（信息透明 — 用户有权看原始数据）
> - 当 SKU 不完全匹配 / 无可信候选时，**必须**在顶部用 ⚠️ 警告区前置（防误推）
> - "🤖 我的建议"是 Molty 的综合判断，与 verdict 字段不同 —— 可以叠加"工具说强烈推荐但 SKU 不对实际不建议"

> 渲染 Top 候选时**必须三层过滤**：去 `removed_outliers` + 去 `flagged_items` + 去 `low_relevance_items`。

```
🛒 比价 · {{product}}

{# === 顶部警告区：SKU 不匹配 / 无可信候选 时必须显示，防误推 === #}
{% if best_deal and best_deal.relevance.missing %}
⚠️ **重要提醒：SKU 不完全匹配**
   你查的是「{{product}}」，最划算可信价对应的实际 SKU 是「{{best_deal.title|truncate(50)}}」，
   缺关键词 [{{best_deal.relevance.missing | join('/')}}]。
   下方数据**仅供参考**，不能直接作为「{{product}}」的购买推荐。
   想要精准 SKU，请加更严格关键词（如 "国行"/"全新"/容量）重查。
{% elif not best_deal %}
⚠️ **重要提醒：本次召回不足以可信推荐**
   {{verdict_reason}}
   下方虽有原始召回数据，但建议加更精确关键词重查。
{% endif %}

🏆 最划算可信价（已过滤翻新/套装/配件/激活可疑/标题不匹配）
{% if best_deal %}
   ¥{{best_deal.price}} | {{best_deal.platform}} / {{best_deal.shopName}}{% if best_deal.is_trusted_shop %} ✓ 可信店铺{% endif %}
   {{best_deal.title}}
   匹配度 {{best_deal.relevance.score * 100}}% ({{best_deal.relevance.matched | join('+')}}{% if best_deal.relevance.missing %} 缺 {{best_deal.relevance.missing | join('/')}}{% endif %})
   🔗 转链: {{best_deal.buy_url}}
   {% if best_deal.copy_cmd and best_deal.copy_cmd != best_deal.buy_url %}📋 淘口令: {{best_deal.copy_cmd}}{% endif %}
   {% if best_deal.search_url %}🔍 原生搜索（兜底，登录后也能用）: {{best_deal.search_url}}{% endif %}
{% else %}
   （信任层 + 相关性层全过滤后无可信候选）
{% endif %}

> ⚠️ **重要使用说明**：上面的 🔗 转链是**联盟推广短链**（淘宝/天猫/京东/拼多多 通用规则）：
> - **必须在未登录浏览器（或隐身窗口）打开**，能正常进商品页
> - **登录账号后再点击会报"链接失效/参数错误"** —— 这是各电商联盟的反作弊机制（防自购返佣）
> - 用户实际购买流程：先在未登录浏览器打开转链 → 看到商品页确认是要买的 → 再用购物 App 直接搜索同款下单
> - 如果嫌麻烦，直接用 🔍 原生搜索 链接：无推广追踪、登录后照样能用、可以直接下单

📊 全网前 3 名候选 + 直链
{% set excluded_ids = (removed_outliers + flagged_items + low_relevance_items) | map(attribute='goodsId') | list %}
{% set safe = all_platforms | rejectattr('goodsId', 'in', excluded_ids) | sort(attribute='price') %}
| # | 价格 | 平台 | 店铺 | SKU | 链接 |
|---|------|------|------|-----|------|
{% for item in safe[:3] %}| {{loop.index}} | ¥{{item.price}} | {{item.platform}} | {{item.shopName or '-'}}{% if item.is_trusted_shop %} ✓{% endif %} | {{item.title|truncate(40)}} | [打开]({{item.buy_url or '#'}}) |
{% endfor %}

📈 历史价（{{history_summary.provider if history_summary else 'noop'}}）
{% if history_summary and history_summary.best_deal_history %}
   该商品 {{history_summary.best_deal_history.snapshots_count}} 次快照（按 shop+title 指纹匹配）
   历史最低 ¥{{history_summary.best_deal_history.low.price}} | 最高 ¥{{history_summary.best_deal_history.high.price}} | 均 ¥{{history_summary.best_deal_history.avg}}
   **当前处于 {{history_summary.best_deal_history.current_rank}}**（low/mid/high）
{% endif %}
{% if history_summary and history_summary.market %}
   该 query 已查询 {{history_summary.market.queries_count}} 次
   市场 30 日中位 ¥{{history_summary.market.stats_median_30d}} · 当前/中位 {{history_summary.market.current_vs_30d_median}}
{% endif %}
{% if history_summary and history_summary.trap %}
   ⚠️ {{history_summary.trap}}
{% endif %}
{% if not history_summary %}
   本地数据不足（同 query 查 ≥3 次或同商品出现 ≥2 次后会有）
{% endif %}

🤖 我的建议
   工具 verdict：「{{verdict}}」 — {{verdict_reason}}
   {% if best_deal and best_deal.relevance.missing %}
   **但**因为 SKU 不匹配（缺 {{best_deal.relevance.missing | join('/')}}），对你这个具体问题（「{{product}}」），**不建议**直接采信工具的 verdict。
   想要这个 SKU，建议加更精确关键词重查；
   或者你接受换 SKU（{{best_deal.title|truncate(30)}}），那 ¥{{best_deal.price}} 是当前可看的候选。
   {% elif not best_deal %}
   **建议**加更精确关键词重查（如 "全新"/"国行"/SKU 容量），让信任层有更可靠的候选。
   {% else %}
   {% if verdict == "强烈推荐" %}**建议入手** — 价格 + SKU + 店铺信任度三层都过关。{% endif %}
   {% if verdict == "可以买" %}**可以考虑** — 价格还行但不算明显低位。{% endif %}
   {% if verdict == "再等等" %}**先观望** — 当前价没明显优势。{% endif %}
   {% if verdict == "别买" %}**不建议买** — 历史命中先涨后降。{% endif %}
   {% endif %}

⚠️ 透明度
{% if trap_warning %}{{trap_warning}}{% else %}本次无剔除/过滤/低价候选提示。{% endif %}

—— 数据来源：{{stats_raw.count}} 平台原始召回；剔除 {{removed_outliers|length}} 条噪音 / 过滤 {{flagged_items|length}} 条状态可疑 / 过滤 {{low_relevance_items|length}} 条标题不匹配
```

### 关键渲染规则（v0.4.1 强化）

1. **C 模式六段都不能省** —— 顶部警告区（条件） / best_deal / Top 3 / 历史价 / 我的建议 / 透明度。即使你要给"不建议买"的结论，**也必须完整展示**。用户有权看原始数据 + 链接。
2. **顶部警告区**：当 `best_deal.relevance.missing` 非空 OR `best_deal == null`，**必须**在标题正下方用 ⚠️ 块前置警告。这是防误推的硬要求。
3. **best_deal 段必须显示 `best_deal.buy_url`** + 淘口令（如有）—— 即使你建议不买，链接也要给（用户可能换 SKU 后想点）
4. **Top 3 表格**用 markdown table，每行带 `[打开](url)` 可点击文字
5. **"我的建议"是综合判断**，跟 verdict 字段是两回事 —— 可以叠加"工具说强烈推荐但 SKU 不对实际不建议"，但 verdict 原始值仍要在该段开头明示
6. **历史价段**有数据就完整展示（含 current_rank / market / trap），没有也明确说"本地数据不足"，不要省略
7. 信息密度顺序固定：⚠️ 警告 → 🏆 best_deal + 链接 → 📊 Top 3 → 📈 历史价 → 🤖 我的建议 → ⚠️ 透明度。**不能改**。

## agent 使用提示（v0.4.1 — C 模式硬约束）

**最重要的一条**：你**不能**因为判断"不建议买"就省略数据展示。C 模式硬要求**完整六段**都给。如果你想给用户"产品级建议"，单独写在 `🤖 我的建议` 段里，**不要**砍掉前面的 best_deal / Top 3 / 历史价段。

1. 用户问"X 多少钱值得买" / "X 哪里买" / 触发词命中 → 调 `uv run bin/price_check.py "<query>"`，把 stdout JSON 直接喂回来
2. 拿到 JSON 后**必须按 6 段顺序完整渲染**（顶部警告 / best_deal / Top 3 / 历史价 / 我的建议 / 透明度）—— 哪怕用户问的 SKU 没匹配上，所有段都要给
3. **best_deal.buy_url 永远要显示**（v0.3 已自动 enrich）。淘宝/天猫额外显示 `copy_cmd` 淘口令；**v0.5.2 起** 当 `best_deal.search_url` 非 null（即 source ∈ {1,2,3,10}）必须额外显示原生搜索链接。**v0.5.3 起** 必须在 best_deal 链接段下方显示一段使用说明："转链需在未登录浏览器打开（登录后会被联盟反作弊判失效）；登录用户直接用原生搜索链接更稳"。即使你判断"不建议买"，链接也要给，用户可能换 SKU 后想点
4. **Top 3 候选必须三层过滤 + 带链接**：去 `removed_outliers` + 去 `flagged_items` + 去 `low_relevance_items`。每条带 `[打开](buy_url)` 可点击文字
5. **当 best_deal.relevance.missing 非空时**，必须在最顶部用 ⚠️ 警告区前置（不是隐藏在底部，是顶部！），告诉用户"SKU 不完全匹配"
6. **`🤖 我的建议` 段**：先明示 verdict 原始值，再叠加你的综合判断。两者可以不同 —— 例如 "工具 verdict：强烈推荐 — 但因 SKU 不匹配，不建议直接采信"
7. **历史价段**有数据完整展示（snapshots_count / low / high / avg / current_rank / market / trap），没有就明示"本地数据不足"
8. 渲染时必须**保留 verdict_reason 里的具体数值**（"低 38.1%" / "¥9689 中位数" / "匹配度 75% 缺 16"），不要换成"明显便宜"模糊话术
9. `verdict in {"数据噪音过多，无法判断", "数据质量不足，无法可信推荐"}` 时，best_deal 可能是 null。这种情况下 best_deal 段写"（信任层 + 相关性层全过滤后无可信候选）"，但 Top 3 / 历史价段仍按数据展示
10. `flagged_items` 和 `low_relevance_items` 的存在有透明性价值。如果用户追问"翻新机/水货也行"，可以从 flagged_items 里取，但明确标注"被标记为状态可疑"
11. 当 trap_warning 有 "💡 还有 N 条更低价候选" 提示，必须**主动告诉用户**"如果你愿意接受第三方店风险，Top 3 里有更低价"
12. `_meta.from_cache = true` 表示来自 30min 缓存，告诉用户"这是 N 分钟前的缓存数据" 或加 `--no-cache` 重跑
13. **可以主动重跑严控关键词**：当首次结果 SKU 严重不匹配，你可以再调一次脚本加更严格关键词（如加 "国行"/"全新"），但**两次结果都要展示给用户**（不要藏起来），让用户看到 SKU 严控前后的对比

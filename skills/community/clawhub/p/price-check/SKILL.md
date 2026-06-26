---
name: price-check
description: "搜索国内主流电商平台（淘宝/天猫、京东、拼多多、苏宁、唯品会、考拉、抖音、快手、1688）的实时价格，自动找到最合适的可信购买点并给出'值不值得买'建议 + 直接可点击的购买链接；本地积累历史价数据，能识别当前价是历史低位还是高位。Keywords: 比价, 值不值得买, 哪里买最便宜, 历史价, 价格监控, X 现在合适入手吗, X 多少钱合适, 哪个平台最便宜, 套路价, 购买链接, 淘口令, price compare"
homepage: https://github.com/yuxiaoyang2007-prog/price-check
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins: ["python3", "uv"]
---

# price-check v0.6.4

## ⚠️ Agent 渲染硬规则（拿到 stdout JSON 时必读）

**第一步永远是把 `human_report` 字段原样发给用户**。

- ❌ 不要省略 human_report
- ❌ 不要重新组织 / 翻译 / 简化 human_report 内容
- ❌ 不要把 human_report 拆开重组成你自己的格式
- ✅ 你**只能**在 human_report 完整发完之后追加一段「我的建议」（≤ 200 字，基于 verdict + SKU 不匹配警告 + 你的产品判断）
- 违反这些规则 = skill 输出无效

JSON 里 `_meta.agent_must_render` 字段也重复了同一条规则。

CLI 用法（绕过 LLM 直出 markdown）：`uv run bin/price_check.py "X" --report`

## 安装即用，飞书同步完全可选

- **零配置即可用**：装上 skill 直接 `uv run bin/price_check.py "X"` 就能跑，所有功能（横向比价 / verdict / 购买链接 / 本地 SQLite 历史价积累）开箱即得
- **`~/.openclaw/data/price-check/`** 是 skill 自己的数据目录，零依赖（仅用 Python stdlib `sqlite3`），跨平台无障碍
- **飞书多维表格同步是 OPT-IN**：不需要它的人**什么都不用做**，主流程不会触碰飞书 / 不会调 `lark-cli` / 不会因此报错。详见后面"飞书多维表格同步"章节
- **lark-cli 也是 OPT-IN 依赖**：仅启用飞书同步的人才需要装；`metadata.openclaw.requires.bins` 没声明它
- 完整可配置项参考 `config.example.json`（位于 skill 根目录）

## 这个 skill 能为你做什么

**三件事**，对应你日常买东西的三个真实需求：

1. **搜全网最低价** — 一次查询，22+ 个国内电商平台横向对比（淘宝/天猫、京东、拼多多、苏宁、唯品会、考拉、抖音、快手、1688）。同关键词的配件、翻新机、套装、激活可疑、SKU 不匹配的混淆商品自动过滤掉，只留**真正可信的购买候选**
2. **告诉你"该不该买"** — 不只是给价格列表，而是给"强烈推荐 / 可以买 / 再等等 / 数据质量不足"的明确建议，附**具体依据**（"可信最低价 ¥X 比 N 平台中位数 ¥Y 低 K%"），并自动拉取**直接可点击的购买链接**（淘宝淘口令、京东短链）
3. **监控历史价** — 每次查询自动写入本地 SQLite，**多查几次同商品后**自动激活"该商品历史最低 ¥X / 最高 ¥Y / 当前处于低位/中位/高位"识别。能捕捉"先涨后降"假促销陷阱

可选叠加：把每次查询自动同步到飞书多维表格，方便手机/电脑跨设备刷历史 + 标记"已购"。

## 触发词

比价、值不值得买、哪里买最便宜、历史价、X 现在合适入手吗、X 多少钱合适、哪个平台最便宜、套路价、是不是先涨后降、当前价合理吗、给我购买链接、价格监控、price compare

## v0.4.1 升级亮点（vs v0.4）

| 升级 | 用户感知 |
|------|---------|
| **C 模式** | 报告固定 6 段：⚠️ 警告 → 🏆 best_deal+链接 → 📊 Top 3 表 → 📈 历史价 → 🤖 我的建议 → ⚠️ 透明度。即使建议不买也完整展示，防止 agent 为简洁砍数据 |
| **顶部警告区** | SKU 不匹配 / 无可信候选时，必须在标题正下方用 ⚠️ 块前置。防止用户被 best_deal 假象误推 |
| **"我的建议"段独立** | Molty 综合判断单独成段（"工具 verdict X，但因 SKU 不匹配实际不建议"），跟 verdict 字段语义分离 |

## v0.4 升级亮点（vs v0.3）

| 升级 | 用户感知 |
|------|---------|
| **F. LocalDBHistoryProvider** | 用本地 SQLite price_snapshots 当历史价数据源（不依赖外部慢慢买）。同 query 跑 ≥3 次后，verdict 会引用"该商品历史 X-Y 元，当前处于历史低位/中位/高位"|
| **G. verdict 升降档** | 当前价处于历史低位 + 比市场中位低 5-15% → 升档为"强烈推荐"（原本是"可以买"）；trap 命中（先涨后降）→ "别买" |
| **H. 商品稳定指纹** | shopmind goodsId 含 session token（每次返回都不同），改用 (shop + title 前 30 字符) 作为商品稳定指纹，跨次匹配同一商品的历史价 |
| **I. 飞书表加历史字段** | （首次跑 setup_feishu.py 一次性建 31 个字段，含历史段：历史样本数 / 历史最低 / 历史最高 / 历史均价 / 当前位置 / 市场30日中位 / 当前/市场比）|

## v0.3 升级亮点（vs v0.2）

| 升级 | 用户感知 |
|------|---------|
| **A. best_deal 自动拉购买链接** | 不再追问"哪里买"，淘宝/天猫给淘口令、京东给短链 URL |
| **B. Top 3 候选也自动拉链接** | 飞书消息里就能多平台对比 + 直接点击下单 |
| **C. 导购优先排版** | 报告顶部不再是 verdict，而是"最划算 ¥X + 链接"和"Top 3 价格速览表"；verdict 退居中部作为决策建议 |
| **D. SQLite 本地持久化** | 每次查询写库，30min 缓存复用；本地积累历史价快照 |
| **E. 飞书多维表格同步（opt-in）** | 启用后查询历史进飞书表，手机/PC 飞书 App 直接刷历史 + 点击购买链接 |

## v0.2 范围 vs v0.3 计划

| 功能 | v0.2 已实现 | v0.3 计划 |
|------|------------|----------|
| 全网横向比价（≈ 22-60 平台） | ✅ | ✅ |
| 价格分布底部 outlier 剔除（去配件/噪音）| ✅（`price < raw_median × 0.3` 自动剔除）| ✅（叠加历史价交叉验证）|
| condition 识别 7 档（accessory / bundle / refurbished / activation_questionable / parallel_import / trusted_domestic / unknown）| ✅（title 关键词词典）| ✅（叠加店铺评分）|
| trusted_shop 识别（自营/旗舰店）| ✅（shopName 字面量 + 正则）| ✅（叠加京东开放平台 vender_type 字段，运营商京东自营单独一档）|
| **标题相关性 / SKU 精确匹配**（"16 Pro 256G" vs "17 Pro 256G"）| ✅（token 命中率 ≥ 0.75 + 多型号堆砌检测）| ✅（叠加 fuzzy match + 同义词 / 大小写 / 容量等价）|
| best_deal 选择按可信度 × 相关性 优先级 | ✅（先过 condition + relevance，再三档优先级）| ✅（叠加历史价档"别买"）|
| 当前价 verdict（强烈推荐/可以买/再等等/数据质量不足/数据噪音过多/无数据）| ✅（基于 best_deal 价 vs 中位数 + relevance 标注）| ✅（叠加历史价精度更高 + "别买"档）|
| trap_warning 透明化（剔除 + flagged + low_relevance + 低价非可信候选提示）| ✅ | ✅（叠加"先涨后降"识别）|
| 历史价 history_summary | ❌（输出为 null）| ✅（HistoryProvider plugin 接入慢慢买自爬）|
| 详情页 URL（购买链接）| ❌（best_deal.url=null）| ✅（按需调 shopmind detail）|

> **注意**：`history_summary` 与"先涨后降"两类信号在 v0.2 仍为 `null`，下游不要假设它们存在。`bin/price_check.py` 已留 `HistoryProvider` 抽象接口，v0.3 接入慢慢买/什么值得买/京东价保后只换 provider 即可，不动主流程。

## 工作流（v0.2 三层过滤）

```
用户问"X 多少钱值得买" / 触发词命中
    ↓
price-check 调 fetch_items(query)
    ↓
shopmind._fetch_search_items()  ← 直接 import 上游 helper，拿 to-string 之前的原始 items
    ↓
_normalize_item(item, query)  ← 字段标准化 + 注入 condition / condition_hits /
                                  is_trusted_shop / relevance(score, matched, missing, ambiguous)
    ↓
原始 items[]（≈ 22-60 条，全字段已含 condition + relevance）
    ↓
[1] 价格层 _filter_outliers()  剔除 price < raw_median × 0.3 → removed_outliers
    ↓
若 clean_items < 5 → verdict = "数据噪音过多，无法判断"
    ↓
[2] 信任层 + [3] 相关性层（在 _select_best_deal 内一次完成）
    - condition ∈ {refurbished/bundle/accessory/activation_questionable} → flagged_items
    - relevance.score < 0.75 或 relevance.ambiguous=True              → low_relevance_items
    - 剩下进 candidates，按三档优先级选 best_deal:
        1. trusted_shop AND condition ∈ {trusted_domestic, unknown}
        2. trusted_shop AND condition == parallel_import
        3. NOT trusted_shop AND condition == trusted_domestic
    ↓
若所有档都没候选 → best_deal=null → verdict = "数据质量不足，无法可信推荐"
    ↓
compute_verdict()  ← 用 best_deal.price vs stats.median 跑阈值（含 ratio>1 时"高于中位数"路径）
compute_trap_warning()  ← 4 段拼接：剔除 / flagged / low_relevance / 低价非可信透明化
HistoryProvider.get_history()  ← v0.2 = NoOp，永远 null（v0.3 swap-in 点）
    ↓
JSON 输出（agent 用）+ references/report-template.md（agent 拿去做最终回复）
```

## 调用方式

```bash
uv run bin/price_check.py "iPhone 16 Pro 256G"
uv run bin/price_check.py "戴森 V12" --source 2     # 限制单平台（2=京东）
uv run bin/price_check.py "Switch 2" --page 2
uv run bin/price_check.py "AirPods Pro 3" --no-cache  # 忽略 30min 缓存，强制重打
```

stdout 是单个 JSON 对象（含 best_deal.buy_url + Top 候选 buy_url）。agent 拿到 JSON 后照 `references/report-template.md` 渲染**导购优先**人类回复。

## 飞书多维表格同步（opt-in，完全可选）

> **不想用飞书的人请直接跳过这一节**。skill 默认 `feishu_sync.enabled = false`，不会触碰飞书 / 不会调 lark-cli / 不会因此报错。完全 0 痕迹。

启用后，每次查询的 best_deal + Top 3 + verdict + 历史价 自动同步到飞书多维表格，方便在手机/PC 飞书 App 直接刷历史 + 点击购买链接。

启用步骤：

1. **装好 lark-cli**（OPT-IN 依赖，未启用飞书的人不用装）
2. **创建飞书多维表格** —— 在飞书云空间里新建一个空多维表格（推荐命名 "价格监控"），位置随意
3. **授权要用的 bot 应用** —— 表格右上"协作" → 添加飞书 Bot 为可编辑（哪个应用看你 lark-cli 的默认 profile，OpenClaw 默认 Molty）
4. **跑配置脚本**（一次性）：
   ```bash
   uv run bin/setup_feishu.py 'https://your-tenant.feishu.cn/base/&lt;BASE_TOKEN&gt;...?...'
   ```
   脚本会一次性自动建 31 个字段：查询词 / Verdict / Verdict依据 / best_deal 价格/平台/店铺/标题/链接/口令 / Top2链接 / Top3链接 / 匹配度 / Condition / 中位数 / 最低价 / 最高价 / 原始条数 / 剔除数 / 过滤数 / 不匹配数 / Trap提示 / 历史样本数 / 历史最低 / 历史最高 / 历史均价 / 当前位置 / 市场30日中位 / 当前/市场比 / 标记已购。

   字段建好后把 `base_token` / `table_id` / `enabled=true` 写到 `~/.openclaw/data/price-check/config.json`。
5. **后续每次跑 price-check 自动同步**，无需手动操作

如需关闭：编辑 `~/.openclaw/data/price-check/config.json` 把 `feishu_sync.enabled` 改成 `false`。

如需切换 lark-cli profile（多飞书账号场景）：在 config.json 加 `feishu_sync.lark_cli_profile = "<profile-name>"`。

## 输出 schema

```jsonc
{
  "product": "<原始查询>",
  "verdict": "强烈推荐 | 可以买 | 再等等 | 别买 | 数据噪音过多，无法判断 | 数据质量不足，无法可信推荐 | 无数据",
  "verdict_reason": "可信最低价 ¥X（平台/店铺）比 N 平台中位数 ¥Y 低 K%；匹配度 100% (M/N token)，缺 [token]",
  "best_deal": {
    "platform": "京东",
    "shopName": "Apple产品京东自营旗舰店",
    "price": 5999.0,
    "title": "...",
    "condition": "unknown",
    "is_trusted_shop": true,
    "relevance": {                    // v0.2 新增
      "score": 0.75,
      "matched": ["iPhone", "Pro", "256G"],
      "missing": ["16"],
      "ambiguous": false
    },
    "goodsId": "...",
    "source": "2",
    "url": null
  },
  "history_summary": null,
  "all_platforms": [ /* 原始 items，每条含 condition / condition_hits / is_trusted_shop / relevance */ ],
  "removed_outliers":     [ /* [1] 价格层剔除：底部噪音 */ ],
  "flagged_items":        [ /* [2] 信任层过滤：refurbished/bundle/accessory/activation_questionable */ ],
  "low_relevance_items":  [ /* [3] 相关性层过滤：score < 0.75 或 ambiguous=true (v0.2 新增) */ ],
  "stats":     { "count": 17, "min": 5998, "max": 13998, "median": 8999, "stdev": ... },
  "stats_raw": { "count": 22, "min": 4.9,  "max": 13998, "median": 8999, "stdev": ... },
  "trap_warning": "⚠️ 已自动剔除 N 条… ⚠️ 已过滤 M 条… ⚠️ 已过滤 K 条标题不匹配… 💡 还有 P 条更低价候选未进 best_deal…" | null,
  "_meta": {
    "skill": "price-check",
    "version": "0.2.0",
    "history_provider": "noop",
    "data_source": "shopmind-price-compare._fetch_search_items()",
    "outlier_filter": "price < raw_median × 0.3",
    "min_clean_samples": 5,
    "relevance_threshold": 0.75,
    "ambiguous_model_count": 3,
    "condition_classifier": "title-keyword (v0.2)",
    "trusted_shop_classifier": "shopName-pattern (v0.2)",
    "suspicious_conditions": ["refurbished", "bundle", "activation_questionable", "accessory"]
  }
}
```

## verdict 阈值（v0.2）

完整规则详见 `references/report-template.md`。摘要：

- 原始 items 为空 → **无数据**
- `removed > 0` 且 `clean_count < 5` → **数据噪音过多，无法判断**
- `best_deal == null`（信任层 × 相关性层全部过滤完没有候选）→ **数据质量不足，无法可信推荐**
- `best_deal.price ≤ clean_median × 0.85` → **强烈推荐**
- `best_deal.price ≤ clean_median × 0.95` → **可以买**
- `best_deal.price ≤ clean_median` → **再等等**（仅低 K%）
- `best_deal.price > clean_median` → **再等等**（高 K%，常见于"全网真品 best_deal 比含个人店/翻新的中位数贵"场景）
- 历史价 v0.3 接入后会增加"别买"档（`history.trap` 命中 / 当前价高于历史均价两档）

> **设计要点**：verdict 用 `best_deal.price`（已过 condition + relevance + trust 三层筛选）而不是 `stats.min`。stats.min 可能是配件、翻新机、不相关 SKU；best_deal 才是"真正能买的可信全新国行/水货的最便宜款"。verdict_reason 末尾必带 `匹配度 X%`，提醒 SKU 接近度。

## 数据层

v0.5 起数据层**自包含**在 `bin/_data_layer.py`，不再依赖外部 skill。该文件是 `maishou88.com` 公共 API 的薄客户端，HTTP endpoints / OPENID 种子 / items 构造逻辑**衍生自** [shopmind-price-compare v2.2.0](https://clawhub.ai/skills/shopmind-price-compare)（作者 [xiaohaook](https://clawhub.ai/users/xiaohaook)）—— 完整归属信息见 `_data_layer.py` 顶部 + `README.md → Acknowledgements`。

## 已知限制

1. **历史价完全缺位**（v0.3 接入慢慢买自爬 / 京东价保 API）：v0.2 verdict 仅基于"当下 N 平台分布"，碰到全网同步涨价的场景会判错。HistoryProvider 已留 swap-in 点。
2. **best_deal.url** 已自动 enrich（v0.3 起）；如果有日并发限流问题 v0.6 会改回按需拉取。
3. **剔除阈值 0.3 是定值**：对 3C/家电正常工作，但极端价格分散（如收藏品/手办 ¥10–¥50000）可能误剔。v0.3 接入历史价后这个阈值可以放松或动态化。
4. **condition 词典是启发式**：会有偶发误判 —— "全新激活试用"误命中 `activation_questionable`；"宠物除螨仪"可能误命中 `accessory`（实际可能是带除螨头的吸尘器主机）。词典在 `bin/price_check.py:CONDITION_RULES` 可调。
5. **运营商京东自营当 trusted**：中国联通 / 移动 / 电信京东自营旗舰店合约机风险偏高但当前算 trusted_shop。v0.3 计划单独给运营商专卖店一档。
6. **标题相关性是 substring 字符匹配 + token 命中率**：query 必须用空格分词；只做 G/GB 等价，没有同义词 / 中英文别名映射。"V12s" 含 "V12" 子串会命中，但"V12 plus"和 query "V12 Pro" 不会互相识别。复杂场景待 v0.3 fuzzy match。
7. **AMBIGUOUS_MODEL_COUNT = 3 是定值**：title 出现 3+ 个不同型号 token 才算模糊堆砌。某些 title 写"V8/V10/V12 通用配件"恰好踩边界，但 condition=accessory 那道大概率会拦下。
8. **shopmind keyword 召回有上限**：单次最多 ~20-60 条结果，可能根本没召回到精确 SKU。verdict_reason 末尾的"匹配度"提醒会让用户/agent 警觉。

---
name: ok-search
description: |
  OK.com 复合搜索技能。处理"在某地找某类内容"的完整流程：解析意图、查询城市、执行搜索、展示结果。支持价格区间筛选。
  当用户请求包含 地点+内容 两个要素时触发（如"找夏威夷房源"、"搜索东京的工作"、"温哥华二手车"、"夏威夷50万以下的房子"）。
---

# ok-search — 复合搜索工作流

处理"在某地找某类内容"的完整流程。当用户请求同时包含**地点**和**内容**两个要素时使用此技能。

> **WARNING**: `--country` / `--city` / `--category` / `--keyword` 只接受英文值。传入中文（如"华盛顿"、"房地产"）会导致超时失败。必须先翻译为英文再传参。

## 执行约束（强制）

- 所有操作只能通过 `uv run --project <SKILL_DIR> ok-cli` 执行，**禁止自行编写代码或直接调用 API**
- `<SKILL_DIR>` 是本 SKILL.md 的**上两级目录**（即包含 `pyproject.toml` 的项目根目录）

---

## 步骤 1 — 解析用户意图

从用户自然语言中提取要素，**全部翻译为英文**：

| 要素 | 说明 | 示例 |
|------|------|------|
| 国家 | **必须从下方 10 个值中选** | usa, japan, canada |
| 城市关键词 | 地点英文名（下一步用 list-cities 确认） | washington, tokyo, vancouver |
| 内容类型 | 分类 code 或搜索关键词 | property, jobs, "laptop" |
| 价格区间 | 可选 | 50万以下→500000, $500以内→500 |

**`--country` 只接受以下 10 个值（不可自造）：**
`singapore` `canada` `usa` `uae` `australia` `hong_kong` `japan` `uk` `malaysia` `new_zealand`

**分类映射（固定 6 个值）：**

| 用户意图 | --category |
|---------|-----------|
| 房子/房源/租房/公寓/房地产 | property |
| 工作/招聘/求职 | jobs |
| 二手/买卖/市场 | marketplace |
| 车/汽车/买车 | cars |
| 服务/维修 | services |
| 社区/活动 | community |
| 具体物品（如"笔记本电脑"） | 不传 category，用 `--keyword "laptop"` |

**价格区间映射：**

| 用户说的 | --min-price | --max-price |
|---------|-------------|-------------|
| 50万以下 | 不传 | 500000 |
| 100万以上 | 1000000 | 不传 |
| 100-200万 | 1000000 | 2000000 |
| $500以内 | 不传 | 500 |
| 5000刀以上 | 5000 | 不传 |

注意：ok.com 价格为当地货币（美国=USD、新加坡=SGD 等），"万"需乘以 10000。

如果用户**未指定地点**，先询问"您想在哪个国家/城市搜索？"，不要猜测。

---

## 步骤 2 — 查询城市名称

用 `list-cities` 确认城市的英文名称：

```bash
uv run --project <SKILL_DIR> ok-cli list-cities --country <国家> --mode search --keyword <城市英文名>
```

从返回结果中选取最匹配的城市 **name**（不是 code），传给下一步的 `--city` 参数。`full-search` 内部通过 UI 搜索城市，需要人类可读的名称。

> 如果 `list-cities` 返回空（`total: 0`），直接用城市英文名作为 `--city` 参数即可——`full-search` 内部会通过 UI 搜索城市，不依赖此步结果。**禁止在搜索流程中使用 `set-locale` 或 `get-locale`**，`full-search` 已内置城市切换。

---

## 步骤 3 — 执行 full-search

```bash
uv run --project <SKILL_DIR> ok-cli full-search \
  --country <国家> --city <城市name> \
  [--category <分类code>] [--keyword <搜索关键词>] \
  [--min-price <数值>] [--max-price <数值>] \
  [--max-results 20]
```

- `--country` 和 `--city` 必填
- `--category` 和 `--keyword` 至少提供一个；同时提供时先进入分类页再搜索
- 内部自动完成：打开网站 → UI 搜索城市并点选切换 → 点击分类 → 输入关键词搜索 → 价格筛选 → 提取结果

---

## 完整示例推导

**用户："找华盛顿100万以下的房子"**

步骤1 解析：country=usa, category=property, max-price=1000000, 城市关键词=washington

步骤2 查城市：
```bash
uv run --project <SKILL_DIR> ok-cli list-cities --country usa --mode search --keyword washington
# 返回 → name: "Washington", code: "washington"
# 用 name 字段传给 --city
```

步骤3 执行搜索：
```bash
uv run --project <SKILL_DIR> ok-cli full-search --country usa --city Washington --category property --max-price 1000000
```

**用户："在新加坡搜索笔记本电脑"**

步骤1 解析：country=singapore, keyword="laptop", 城市关键词=singapore

步骤2 查城市：
```bash
uv run --project <SKILL_DIR> ok-cli list-cities --country singapore --mode search --keyword singapore
```

步骤3 执行搜索：
```bash
uv run --project <SKILL_DIR> ok-cli full-search --country singapore --city singapore --keyword "laptop"
```

**用户："东京的工作"**

步骤1 解析：country=japan, category=jobs, 城市关键词=tokyo

步骤2 查城市：
```bash
uv run --project <SKILL_DIR> ok-cli list-cities --country japan --mode search --keyword tokyo
```

步骤3 执行搜索：
```bash
uv run --project <SKILL_DIR> ok-cli full-search --country japan --city tokyo --category jobs
```

---

## 步骤 4 — 展示结果

将 JSON 输出结构化展示给用户：

```
1. **标题** — 价格
   地点 | [查看详情](url)
```

如果用户想看某条帖子的详情：
```bash
uv run --project <SKILL_DIR> ok-cli get-listing --url "<帖子URL>"
```

## 结果为空时的处理

- 搜索无结果 → 告知用户"该地区暂无相关帖子"，建议更换关键词或分类
- 如果不确定分类 → 建议用 `--keyword` 代替 `--category`

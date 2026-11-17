---
name: kb-dashboard
description: This skill generates a read-only visual dashboard of the user's ima knowledge base (via ima-mcp). Trigger ONLY when the user explicitly asks for an ima knowledge base dashboard, structure overview, or folder-level map — e.g. "知识库看板", "ima 知识库结构图", "生成 ima 知识库图谱", "ima 看板", "看看我的 ima 库长啥样". It pulls the current structure from ima (read-only) and renders a self-contained HTML dashboard (collapsible folder tree, KPI gauges, bar/pie charts, folder-level graph). Does NOT trigger on generic "看板"/"dashboard"/"知识图谱" requests unrelated to an ima knowledge base.
version: 1.1.3
author: dzz-777
display_name: "IMA 知识库可视化看板"
display_name_en: "IMA Knowledge Base Dashboard"
description_zh: "你的 ima 知识库长什么样？一句话生成自包含 HTML 看板：结构树+KPI+图表+图谱，还能统计蒸馏进度——空壳夹、未消化原料一目了然。"
description_en: "Generate a read-only visual dashboard of your ima knowledge base as a self-contained HTML file, with optional tag-based distillation stats."
examples_zh:
- "生成我的 ima 知识库看板，看看结构和空壳夹"
- "三库并排对比，个人主库和公司库哪边更厚"
- "统计一下资料收集库的蒸馏状态，还有多少没消化"
examples_en:
- "Generate my ima knowledge base dashboard: structure and empty folders"
- "Compare all three libraries side by side — which one is richer?"
- "Show the distillation status of my collection library — how much is unprocessed?"
allowed-tools:
  - mcp__ima-mcp__get_knowledge_base_list
  - mcp__ima-mcp__get_knowledge_list
  - mcp__ima-mcp__fetch_media_content
  - Bash(python3 *)
  - present_files
triggers:
  - 知识库看板
  - ima 知识库结构图
  - 生成 ima 知识库图谱
  - ima 看板
  - 知识库可视化
  - 知识库标签统计
  - 看看我的库长啥样
tags:
  - ima
  - 知识库
  - 可视化
  - 看板
agent_created: true
---

# ima 知识库看板生成器（kb-dashboard）

## Overview

为你的 ima 知识库生成一份**全局快照看板**——双击即看的 HTML，包含结构树（根→子目录，可折叠）、KPI 仪表、分层柱状图、方法卡四环节饼图、folder 级知识图谱。解决「ima 个人版无原生结构/图谱可视化看板」的缺口，让**用户**随时用「上帝视角」看见整个库的状态、哪里空、哪里堵。

**特性**：
- 纯只读拉取 ima 数据，绝不动库。
- 自包含单文件 HTML（内嵌 ECharts，亮/暗双主题，右上角切换）。
- 支持单库（个人主库 / 公司库 / 资料收集）或三库全局（tab 切换）。

## 环境自检（无 ima-mcp 环境第一眼看这里）

本 skill 的正式流程需要 ima-mcp 工具；**工具不可用时不要报错中断**，按以下顺序执行：

```bash
# 1) 零依赖自检：校验包完整性 + 数据校验器 + demo 端到端
python3 scripts/build_dashboard.py --selftest

# 2) 零依赖体验：内置演示数据端到端生成示例看板
python3 scripts/build_dashboard.py --demo --out ./demo.html
```

两条命令均不依赖 ima-mcp、不联网。`--selftest` 全部通过 = 本 skill 在当前环境可正常运行；`--demo` 产出约 1MB 自包含 HTML（内嵌 ECharts）。拿到真实结构 JSON 后用 `--data` 正式生成。

## 触发条件（When to use）

- 用户说「知识库看板」「生成 ima 知识库图谱」「ima 知识库结构图」「ima 看板」「知识库可视化」「看看我的库现在长啥样」。
- 用户想定期巡检知识库结构、空壳夹、Express 缺口。
- **严格范围**：本 skill 只服务于 **ima 知识库**的结构可视化。用户如果只是说「给我做个看板」「画个 dashboard」「生成知识图谱」（未指明 ima 知识库），**不应触发**——那可能是 BI/前端/其它需求，需先确认是否针对 ima 库。
- **不做**：实时自动刷新（个人版无开放 API，见诚实边界）、写库、改结构、非 ima 库的图表。

## 提示词模板（可直接复制）

> 把下面的指令直接发给 WorkBuddy 即可触发本 skill；scope 可替换。

- 个人主库看板：`请生成我的 ima 知识库看板（个人主库），让我用上帝视角看看结构、空壳夹和 Express 缺口。`
- 全局三库看板：`生成 ima 全局看板，把个人主库 / 公司库 / 资料收集库并排对比。`
- 公司库看板：`生成你的品牌知识库（公司库）的看板。`

## 输出格式

- **产物**：一份**自包含单文件 HTML 看板**（内嵌 ECharts，亮/暗双主题可切换），输出到当前工作目录或 `--out` 指定路径（如 `ima看板_<库名>_<日期>.html`）。
- **展示**：通过 `present_files` 自动在浏览器预览；并告知用户「这是快照，想看最新状态随时重跑」。
- **内容页**：结构树（可折叠）+ KPI 仪表 + 顶层夹柱状图 + 方法卡四环节饼图 + folder 级知识图谱；`all` 模式额外生成三库并排 tab。
- **边界**：本 skill 只读拉取与渲染，不建夹、不改标签、不写任何内容。

## 范围解析（先确认，再拉取）

| 用户表述 | scope | 目标库 |
|---|---|---|
| 「知识库看板」「我的库看板」（默认） | `main` | 个人主库 |
| 「全局看板」「整体看板」「所有库」 | `all` | 三库并排 tab |
| 「公司库看板」「品牌库看板」 | `company` | 你的品牌知识库（公司库）|
| 「资料库看板」「收集库看板」 | `material` | 资料收集库 |

> 若用户未指定，默认 `main`（个人主库，图谱效果最好）。涉及 `all` 时，先简短确认是否要三库全量（数据量较大），再执行。

scope 只是语义标签；**真正的库 ID 由 Step 1 自动探测、或从上方「目标库 ID」表取（示例）**。使用者切勿套用示例 ID，应先 `get_knowledge_base_list` 拿自己的库再填。

## 目标库 ID（使用者须替换为自己库）

> ⚠️ **去个人化提醒（上架必读）**：下表是**作者个人的 ima 库 ID 示例**，仅作占位。公开上架后，**使用者首次运行必须先获取自己的库 ID**，不要直接套用下表。
>
> **自动探测（推荐）**：先调 `mcp__ima-mcp__get_knowledge_base_list` 列出你账号下全部库（含 `knowledge_base_id` 与库名）；再用 `mcp__ima-mcp__get_knowledge_list`（不带 folder_id）拉该库顶层 folder 列表。把返回的真实 ID 填进 DATA JSON 即可，无需硬编码。
>
> 下表作为**默认示例**保留，仅作占位说明；使用者请按上面自动探测流程替换为自己的库 ID。

| 库（示例占位，请替换） | knowledge_base_id | 关键 folder_id |
|---|---|---|
| 你的个人主库 | `<你的主库ID>` | `<顶层夹1 folder_id>`；`<顶层夹2 folder_id>`；（按你的库结构填关键 folder）|
| 你的品牌知识库（公司库）| `<你的公司库ID>` | `<核心方法论 folder_id>`；`<治理层 folder_id>` |
| 资料收集库 | `<你的资料收集库ID>` | （按文件夹分组，无需逐子夹枚举）|
| 书籍萃取库 | `<你的书籍萃取库ID>` | （独立质检，一般不在看板主视图）|

> folder ID 可能随 ima 结构微调而漂移。若拉取返回空或异常，用 `mcp__ima-mcp__get_knowledge_list`（无 folder_id）重新拉顶层确认当前 ID。

## 拉取与渲染流程（Step-by-Step）

### Step 1 · 拉取 folder 树（只读）

> **先定库 ID（去个人化关键）**：若 DATA 里还没有 `knowledge_base_id`，先调 `mcp__ima-mcp__get_knowledge_base_list` 列出账号下全部库，让用户选 / 按库名匹配 scope；再把真实 ID 填入。不要写死示例 ID。

对每个目标库，调用 `mcp__ima-mcp__get_knowledge_list`：
1. 先拉**顶层**（参数 `{knowledge_base_id, limit:50}`，不带 folder_id）→ 得到 root 的子节点列表（folder + 散文件）。
2. 对每个 folder 节点，再拉其子层（`{knowledge_base_id, folder_id, limit:50}`）统计 count 与 children。
3. **翻页**：单次 limit 上限 50，返回 `cursor` 非空时继续拉下一页，直到取完。
4. 散文件（无 folder_id 的直接子项）计入父 folder 的 `count`，文件名进 `items`。

> 只统计「结构」即可：folder 名、每层 count、空壳夹（count=0 的 Areas）、方法卡四环节分布（仅主库：4 个子夹计数）、案例库子夹数（subfolders）。

### Step 2 · 整理成 DATA JSON

将数据整理为下方 schema（与 `scripts/build_dashboard.py` 的 docstring 一致）。**graph 节点 cat: 0=根·库, 1=顶层夹, 2=子夹；links 为父子索引对**。

```json
{
  "generated_at": "2026-01-01 12:00",
  "scope": "main",
  "libraries": [{
    "id": "<你的主库ID>",
    "name": "你的知识库",
    "note": "可选·诚实边界说明（覆盖默认文案）",
    "kpis": {"topFolders":8,"totalDocs":120,"methodCards":60,"metaLayer":12,"emptyAreas":2,"express":"薄"},
    "tree": [
      {"name":"知识领域A","count":12,"items":["示例文档1","..."]},
      {"name":"知识领域B","count":60,"children":[{"name":"子领域B1","count":15},{"name":"子领域B2","count":30},{"name":"子领域B3","count":15}]},
      {"name":"暂空领域","count":0,"empty":true}
    ],
    "topCounts": [["知识领域A",12],["知识领域B",60],["项目实战",4],["案例库",40],["待建领域",0]],
    "methodStage": [["阶段1",15],["阶段2",30],["阶段3",10],["阶段4",5]],
    "graph": {"nodes":[{"name":"你的知识库","count":120,"cat":0},{"name":"知识领域A","count":12,"cat":1},{"name":"知识领域B","count":60,"cat":1},{"name":"子领域B1","count":15,"cat":2}],"links":[{"source":0,"target":1},{"source":0,"target":2},{"source":2,"target":3}]}
  }]
}
```

- **kpis.express**：根据项目实战夹内容判读，如「薄」「丰富」「—」。主库常「薄」（仅模板）。
- **methodStage**：仅主库填 4 项；公司库/资料收集库传空数组 `[]`（饼图自动显示占位）。
- **note**：默认文案已写在模板；如需强调某库边界，可覆盖。

### Step 3 · 渲染 HTML

将 DATA 写成临时 JSON（如 `/tmp/kb_main.json`），调用脚本（`<skill目录>` = 本 skill 包所在目录，其下有 `scripts/` 与 `assets/`）：

```bash
python3 <skill目录>/scripts/build_dashboard.py \
  --data /tmp/kb_main.json \
  --out ./ima看板_个人主库_$(date +%Y-%m-%d).html
```

- `--out` 可省略：默认输出到**当前工作目录** `kb_dashboard_YYYY-MM-DD.html`。使用者可传任意绝对 / 相对路径（如自己的桌面）。
- `--template` 可覆盖模板路径（一般不需）。
- **离线自包含**：脚本会将包内 `assets/echarts.min.js` 内嵌进产物 HTML，无需联网即可完整渲染全部图表。
- **快速体验（无需 ima-mcp）**：`python3 <skill目录>/scripts/build_dashboard.py --demo --out ./demo.html` 用内置演示数据端到端生成，可用于安装后自检。

脚本读取 `assets/template.html`，把数据注入 `/*DATA_PLACEHOLDER*/`、把 ECharts 注入 `/*ECHARTS_INLINE*/`，输出自含 HTML。

### Step 4 · 交付与刷新

用 `present_files` 展示生成的 HTML（自动打开浏览器预览）。告知用户：**这是快照，想看最新状态随时让我重跑**。

## 进阶模式：标签维度统计 + 卡片级关系链图谱（可选）

默认图谱是 **folder 级从属**（100% 真实，但只到文件夹）。进阶有两条路，仅在用户明确要求时启用（成本高，需逐卡读内容），不要默认跑：

### A. 标签维度统计（v1.1.0 新增，与入库助手的自动打标配套）
1. 拉目标夹的卡片/文章列表。
2. 对每项调 `mcp__ima-mcp__fetch_media_content` 或读 front-matter，提取标签：原料层 `来源/置信度/蒸馏状态` 三段式；资产层 `学科域/方法/阶段/类型/行业` 五维。
3. 聚合出三类统计并渲染进看板新增图表位：
   - **蒸馏漏斗饼图**：`蒸馏状态` 分布（待评估 / 已蒸馏→X卡 / 暂缓 / 归案例库）——直接回答「这堆原料消化了多少」；
   - **置信度分布柱状图**：二手/待校准占比，暴露语料质量风险；
   - **五维热力条**：学科域×类型 交叉计数，看知识主干哪里厚哪里薄。
4. 无标签的项计入「未打标」单独一档——**未打标占比本身就是看板的重要发现**，如实展示，不要隐藏。

### B. 卡片级关系链图谱
1. 拉主库方法卡列表，读 front-matter 的「挂接卡」字段。
2. 卡片作节点、挂接关系作 links，生成卡片级网络，可并入「关系链」tab 或单独输出。

## 注意事项（诚实边界，必须向用户说明）

1. **ima 个人版无原生图谱数据**：看板「知识图谱」= folder 层级从属关系还原（真实）；卡片级「挂接卡」需进阶模式读卡。
2. **快照非实时**：数据固定为生成时刻。真·实时需本地服务代理 ima API（配 `~/.config/ima/` 凭证 + 常驻），当前未做。
3. **离线可用·零远程加载**：产物 HTML 已内嵌 ECharts（Apache-2.0），断网双击也能完整渲染；v1.1.1 起不再回退在线 CDN——包内 `assets/echarts.min.js` 缺失时构建报错提示恢复，产物不含任何远程脚本引用。
4. **只读**：本 skill 只拉取与生成，绝不写库、建夹、改标签。
5. **比例真相**：看板如实暴露空壳 Areas、Express 薄、资产 vs 订阅失衡——这是看板的价值，不是缺陷。
6. **标签统计依赖打标质量**：标签维度统计（v1.1.0）只统计实际写在卡片 front-matter/文末标签区里的标签；未打标的项只能计入「未打标」档，无法凭空补齐。
7. **不绑定个人库**：本 skill 不写死任何个人 ima 库。示例 folder ID 仅为占位说明；使用者须按 Step 1 自动探测替换为自己的库 ID 后才能正确拉取。

## Resources

- `scripts/build_dashboard.py` — JSON → HTML 渲染器（含数据校验、ECharts 内嵌、`--demo` 演示模式、默认输出命名）。
- `assets/template.html` — 自含看板模板（ECharts 注入点、亮/暗双主题、结构树+KPI+柱状+饼图+folder 图谱、单库/三库 tab）。
- `assets/echarts.min.js` — Apache ECharts 5.5.0（Apache-2.0），构建时内嵌进产物，保证离线渲染。

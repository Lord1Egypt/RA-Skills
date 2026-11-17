# 四条路由（作业闭环）

主技能只锁定路由。本文件展开：**新建（含材料→稿）/ 填壳 / 美化保结构 / 增强**。字段以 `schema write pptx` / `schema edit` 为准。

一次作业只走一条路由到交稿。中途要换路由，先跟用户说，再重锁。

## 0. 一条判别题（歧义时）

禁止列出四条让用户点。只问：

> 新做一份，还是改你这份文件？  
> 改的话：填新内容 / 保结构美化 / 只加动画备注？

| 用户补充 | 锁定 |
|----------|------|
| 「从零做」「把这份材料做成 PPT」 | **新建** |
| 「用我的模板 / 母版 / 这个壳」 | **填壳** |
| 「页还是这些，好看一点」 | **美化** |
| 「加个切换 / 备注 / 动画就行」 | **增强** |
| 「第 3 页改两个字」 | **美化**（定点 `set_text`） |
| 「拆一页 / 合两页 / 加一页」 | 先确认叙事还是否原结构；变叙事 → **新建** 或 **填壳** 加页 |

课件仍转 `office-kejian`。洗表 / 8D 仍转 `office-xlsx-data` 或 Hub fill。

---

## 1. 新建（Generate）

无现成 `.pptx`，或材料要变成**新文件**。

### 1.1 精修 vs 速出

| | 精修（默认对外） | 速出 |
|--|------------------|------|
| 信号 | 正式 / 高级感 / 官网 / ≥8 页 / 单页很重 | ≤6 页内部提纲，用户没要好看 |
| 落盘 | 骨架 `write` + 逐页 `upsert_slide` | 整份 `write pptx` |
| 门 | 确认大纲 + 三档验收 | 可跳过门 1；仍建议 `preflight`；对外仍要档 C |

「精修 / 高级感 / 对外」即使 5～6 页也走精修。

### 1.2 材料→稿（新建的前缀，不是第五条路由）

「把这份 PDF / Word / 提纲做成 PPT」= 先抽论点，再走新建精修。**勿跳过确认直接出。**

| 源 | 怎么进 | 不要 |
|----|--------|------|
| `.docx` / `.doc` | `read docx --mode outline`（不够再 `text`） | 把整篇粘进 bullets |
| `.pptx` / `.ppt`（当素材，不是壳） | `read pptx --mode outline` | `write` 覆盖源文件 |
| `.xlsx` 数字证据 | `read xlsx --mode table`，抽出 3–5 个可上屏的数 | 整表倒进 PPT |
| 用户粘贴 / `.md` | 当原文 | — |
| **`.pdf`** | 引擎**无** `read pdf` | 假装读了 PDF；改请用户粘贴要点或另存 DOCX |
| 扫描件 / 仅图 | 宿主能看图再摘要；否则请用户列页纲 | 盲写 |

步骤：

1. 读源（或声明读不了）→ 列缺口（受众、要不要对外、页数上限）。
2. 交大纲：受众 / 页数 / `theme` / 逐页一句话论点 + 布局标签。等人改。
3. 确认后骨架 `write` → 逐页 `upsert_slide` → `preflight` + `view svg`（线框核 bbox，看 `data-source-path`）→ **打开文件**（档 C；CLI 无 screenshot）。
4. 源里的原话可作证据，标题必须是**结论句**，不要「第一章 / 概述」。

大纲最小形态：

```markdown
# 华东零售增长 路演 · 咨询风 · 10 页
受众：客户合伙人  对外：是  theme: consulting
P1 封面 · cover
P2 判断：增长来自复购不是拉新 · 左论点+右 KPI
P3 证据：三城复购差 12pt · 图+三数
…
```

---

## 2. 填壳（Fill Native）

用户给了 `.pptx` / `.potx`，要**新内容进旧壳**。

1. `read pptx --mode outline`（必要时 `stats`）对页：标题、页数、哪页是壳。
2. 把用户材料映射到现有页。缺页用 `add_slide` / `upsert_slide`；多出来的壳页问是否留空还是删（`delete_slide`）。
3. 逐页 `set_text` / `set_props` / 换图（本地 `path`）。**保母版、主题、未改页。**
4. **禁止**对原 path `write pptx`（会丢母版与未建模形状）。要新文件：先复制再改副本。
5. 改完 `preflight` + `view svg`。未改页也扫一眼。正式稿再打开文件看图。

对不上的占位（「单击此处」）必须清掉或换成真文案。

---

## 3. 美化保结构（Restyle）

页数和每页论点不变，只改气质 / 对齐 / 密度。

1. `read pptx --mode outline` 列出「页 → 论点」。论点写进回复，让用户确认「结构不动」。
2. 能点改就 `set_text` / `set_props` / `align` / `distribute` / `fit_text`。整页重画仅当旧页是「标题+两条 bullet」——`upsert_slide` **沿用同一 thesis**。
3. 色板：优先沿用文件里已有色；没有再用 preset。勿手填默认蓝 / 奶油底（见 `pptx-design.md` §3.3）。
4. **禁止**整份 `write` 覆盖；**禁止**借美化改叙事、删论证页、加新章节（那是新建或填壳）。
5. `preflight` + `view svg`。`layout_overlap` 先对线框，勿盲目 `avoid_overlap`。对外再打开文件。

---

## 4. 增强（Enhance）

画面不动，只加演示附件。

- 切换：`set_transition`（含 `morph` 时带 fade fallback）。
- 动画：`add_animation`；勿为「显得高级」给每段字加飞入。
- 备注：改 `notes`（给讲者，不当第三页正文）。

`transition` / `anim` 写在 `write` JSON 里**无效**（`write_field_ignored`）。`role` / `thesis` 在 write 里静默忽略；只在 `upsert_slide` 进备注。本路由不要 `upsert_slide` 改版式。做完可用 `view` 抽一页确认备注还在。

---

## 5. 与引擎能力的诚实边界

| 想做 | 现状 |
|------|------|
| 抽客户 VI 成可复用 theme/master | 技能暂无品牌工作区；每稿重选 preset 或手写六色 |
| 缩略图挑版式再填 | 未做；填壳靠 `read outline` 对页 |
| 旁白 / 配音 / 出视频 | 不做（演示附件，不是本技能主路径） |
| PDF 直接抽文 | 无 `read pdf`；请用户给 DOCX/粘贴 |

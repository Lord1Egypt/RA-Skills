# 片段库索引(复制 → 替换 {{参数}} → validate)

> v1 不建模板引擎:直接复制片段内容进页面,替换 `{{参数}}` 即可。
> 每个片段文件头部注释都自带参数表与 z 序约定。
> **选片段前先看页面形态:`reference/page-archetypes.md`(43 个原型)与设计纪律 `reference/design-principles.md`。**
> 带 ⚠️ 的片段有使用限制(去 AI 味纪律),超限场景禁用。
> **2026-08-05 起**:图示构件片段是**结构形状**(承载信息),不计装饰预算、不占卡片矩阵限额;图标从 `assets/icons.md` 复制(stroke 用 `style="stroke:var(--变量)"`,禁 currentColor)。

## 分析论证片段(2026-08-09 新增,咨询页型主力 · 原型 31-43)

> 只给**最难手搓的 8 个**(涉及坐标计算或形状语法);剩下那几个原型(40/41/42/43 与 36 散点)
> 骨架直接可抄,查 `page-archetypes.md` 对应小节即可 —— 避免片段库膨胀成第二份原型库。
> **本组共同硬要求**:每页必须带来源/口径注(时间范围 + 样本 + 测算方式),见
> `design-principles.md`"数据页的口径纪律";拿不到数按各原型"降级"行退回,**别编基准**。

| 片段 | 用途 | 布局方式 | 主要参数 |
|---|---|---|---|
| `exec-summary.html` | 统领结论面板+3 支柱裸排+来源行(原型 31) | A 定位 + C 支柱 grid | VERDICT / KPI / P1-3_KICKER·TITLE·BODY / SOURCE |
| `issue-tree.html` | 议题树 MECE:根+3 分支+叶子+正交线(原型 32) | A 绝对定位 | ROOT / B1-3_TITLE·META·L1·L2 / MECE_NOTE / SOURCE |
| `harvey-row.html` | Harvey ball 评分行:表格行+4 圆饼叠放(原型 33) | 表格行 + A 定位圆饼 | ROW_BG / NAME / VERDICT / ROW_Y / C1-4_SHAPE·BG·BORDER |
| `waterfall-bar.html` | 瀑布单柱:浮空增减柱+柱顶值+连接虚线(原型 34) | A 绝对定位 | X / TOP / H / BG / VALUE / LINK_X / LABEL |
| `swimlane-row.html` | 甘特单道:底纹带+泳道名+任务条+里程碑(原型 35) | A 绝对定位 | LANE_Y / LANE_BG / OWNER / BAR_X·W / TASK / MS_X·LABEL |
| `driver-node.html` | 驱动树单因子:运算符徽章+三层信息盒(原型 37) | A 绝对定位 | OP / X / ACCENT / NAME / VALUE / HEADROOM |
| `heatmap-table.html` | 热力矩阵:表格+逐格三档底纹+图例(原型 38) | A 绝对定位 | DIM1-5 / R*C*_BG·FG / LEGEND_NOTE / SOURCE |
| `scenario-col.html` | 情景分析单栏:档名+数字+副指标+说明(原型 39) | 置于 grid 列内 | TIER / BG / VALUE / SUB / BODY(+各色令牌) |

**三个最容易搞错的点**(片段头注释里也写了,这里汇总):
1. `harvey-row` 的圆饼是**独立叠放对象,不随表格流** —— 改行高/列宽后必须重算 left/top。
2. `waterfall-bar` 搭完必须**验算闭合**(起始 + 各增减 = 结束);不闭合的瀑布是错图。
3. `heatmap-table` 的中档色用 `var(--brand-primary-soft)`(主色 17% 混白);**换预设自动跟随**,不必重算。

## 图示构件片段(2026-08-05 新增,形式丰富主力)

| 片段 | 用途 | 布局方式 | 主要参数 |
|---|---|---|---|
| `icon-grid-cell.html` | 图标网格单元卡(原型 23 单元;并列要点首选图示) | A 定位 / C 删定位挂 data-layout-h | X/Y/W/H / ICON / TITLE / BODY / EXAMPLE |
| `chevron-band.html` | 4 步 chevron 流程带+说明列(原型 24) | A 绝对定位 | S1-4_BG / S1-4_TITLE / S1-4_DESC |
| `funnel-stack.html` | 4 层转化漏斗+左右侧注(原型 25) | A 绝对定位 | L1-4_BG / TEXT / STAGE / VALUE |
| `pyramid-tiers.html` | 三层金字塔(原型 26) | A 绝对定位 | T1-3_BG / NAME / SUB |
| `cycle-loop.html` | SVG 环+中心圆+4 卫星卡(原型 27) | A 绝对定位 | RING_COLOR / HUB_BG / HUB_TEXT / N·E·S·W_TITLE·BODY |
| `hub-spoke.html` | 中心圆+正交连接线+4 卫星卡(原型 28) | A 绝对定位 | HUB_BG / HUB_TEXT / N·S·W·E_ICON·TITLE·BODY |
| `vs-cards.html` | 双卡对决+中央 VS 徽章+图标特征行(原型 29) | A 绝对定位 | L/R_KICKER·NAME·ITEMS / VS_BG |
| `color-band.html` | 色带行单元(原型 30;3-4 条 stack) | A 定位 + 对象内 flex | Y/H / BG / ICON / TITLE / SUB / NUM |

## 原型直出片段(2026-08-02 新增,去 AI 味主力)

| 片段 | 用途 | 填充 | 主要参数 |
|---|---|---|---|
| `agenda-list.html` | 议程条目:大数字编号裸排(原型 3) | 满填 | NUM / TITLE / SUB / H / BORDER |
| `section-divider.html` | 章节分隔:超大编号+章节名(原型 4) | airy | NUM / TITLE / SUB |
| `big-statement.html` | 大字观点页(原型 5) | airy | STATEMENT / PROOF |
| `quote-hero.html` | 引用页:巨引号+正体(原型 6) | airy | QUOTE / ATTRIBUTION / MARK_COLOR |
| `editorial-columns.html` | 编辑式双栏文字(原型 7 内容区) | 满填 | COL1 / COL2 |
| `image-bleed.html` | 全出血大图页(原型 11) | 出血 | IMG / HEADLINE / SUB / VEIL |

## 基础构件片段

| 片段 | 用途 | 布局方式 | 主要参数 |
|---|---|---|---|
| `page-header.html` | ⚠️ 页头三件套(**仅章节首页/封面**) | A 绝对定位 | KICKER / TITLE / SUBTITLE / PAGE_NUM |
| `card-accent-top.html` | ⚠️ 顶部强调条卡片(**纯文字卡片矩阵每 deck ≤2 页;图标网格用 icon-grid-cell 不受此限**) | A 绝对定位 | X/Y/W/H / ACCENT / KICKER / TITLE / BODY / FOOTNOTE |
| `badge-center.html` | 单行垂直居中徽章(仅状态标注) | A 绝对定位 | X/Y/W/H / BG / FG / TEXT / RADIUS |
| `gradient-bar.html` | ⚠️ 渐变横条+叠字(**仅封面/分隔/收尾**) | A 绝对定位 | X/Y/W/H / FROM→TO / TEXT |
| `stat-number.html` | 混合字号大数字格(原型 17 单元) | 置于 grid/columns 列内 | VALUE / UNIT / COLOR / LABEL |
| `layer-row.html` | ⚠️ 序号圆横条目(**仅流程/步骤类**) | A 定位 + 对象内 flex | X/Y/W/H / NUM / ACCENT / TITLE / SUB |
| `data-table.html` | 数据表格(交替底纹+深色表头+右对齐数字) | A 绝对定位 | X/Y/W / HEAD_COLOR / ZEBRA |
| `code-block.html` | 代码展示(深色渐变+虚线边框+pre/code) | A 绝对定位 | X/Y/W/H / BG_FROM→TO / TITLE / CODE |
| `flow-step.html` | chevron 单元(**整带用 chevron-band 更省**) | A 绝对定位 | X/Y/W/H / BG / NUM / TITLE |
| `compare-card.html` | ⚠️ 对比卡(**双卡对决用 vs-cards 更齐**) | A 绝对定位 | X/Y/W/H / ACCENT / BADGE / TITLE / ITEMS |

## 限用/弃用片段

| 片段 | 状态 | 说明 |
|---|---|---|
| `hero-gradient.html` | ⚠️ 仅封面/分隔/收尾 | 渐变英雄区(内容页禁用) |
| `kpi-card.html` | ⚠️ 仅仪表盘(阅读/混合档) | 演讲档 KPI 用 stat-number 裸排 |
| `timeline-node.html` | ⚠️ 默认用原型 14 替代 | 仅用户明确要求"活泼风"时 |
| `quote-block.html` | ⛔ 已弃用 | 渐变左边框+斜体 = AI 指纹;用 `quote-hero.html` |

## z 序与叠放约定

1. **PPTX 叠放 = DOM 顺序**(先画在下);片段内部的 z-index 仅为浏览器合成服务
2. 层次惯例:底卡 `z-index:1` < 强调条/徽章底 `z-index:5` < 文字 `z-index:10` < 截图区叠字 `z-index:11`
3. 组合多个片段时,按"底→顶"的阅读顺序写 DOM;同容器内元素重叠时尤其如此(勿靠 z-index 补救)

## 组合建议

- **满填纪律**:内容带必须铺满内容区(320-940,利用率 ≥85%);条目/卡片少就放大字号与间距(scale-to-fill),不许留白在底部
- `agenda-list` 多条堆叠:方式 B 用 `flex-direction:column` 容器免算 top;方式 C 用 `data-layout="stack"`
- `stat-number` 必须放在某个已标记格子/列内部(它是内容片段,不是独立 data-object)
- 成组内容优先方式 B/C(见 layout-recipes);页面骨架(标题/页码)用方式 A
- **装饰预算**:每页装饰元素 ≤3 件(装饰线/徽章/渐变条/图形点缀各计 1 件);每页高亮 ≤1 处
- **结构色面下限**(2026-08-06):每个内容页至少一块结构色面(色带/深色面板/卡片底/表头底纹,
  ≥1.5 万 px²)—— 结构色面**不占装饰预算**,它是内容页应该有的层次,不是点缀

## 占位符规范

`{{X}} {{Y}} {{W}} {{H}}` 含单位(如 `100px`);`calc()` 已预写在需要偏移的位置(如卡内边距 30px)。
替换时**整页内唯一**:先全局替换 `{{X}}` 再复制下一张卡,避免串值。

---
name: html-slides-to-pptx
description: >-
  编写可无损还原为 PPTX 的 HTML 幻灯片。先经引导式访谈确认样式/形式/结构并落盘
  deck-brief,再生成完整目录结构(assets/theme.css、slides/*.html、playlist.json),
  每页严格遵循 html-spec.md 规范,经 validate.js 预检零 ERROR 后用 convert.js 转成
  PowerPoint。TRIGGER when: 用户要求"做PPT/幻灯片/slides/演示文稿"、"把内容做成
  HTML幻灯片"、"生成可转PPTX的slides",或调用 /html-slides-to-pptx。DO NOT TRIGGER when:
  只需单页HTML网页、或要做的是 reveal.js/Marp 等其他幻灯片格式。
version: 2.1.0
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
---

# html-slides · 可无损转 PPTX 的 HTML 幻灯片生成器(引导式访谈版)

## 核心原则

转换器(`scripts/convert.js` + 浏览器端提取管线)只**无损支持 HTML/CSS 的一个子集**。
每页 HTML 必须严格遵循 `reference/html-spec.md` —— 这是契约,不是建议。
写页面之前必须先完成 Step 1 访谈并让用户确认 `slides/deck-brief.md`。

## 首次使用:检查工具依赖

> 以下命令中的 `SKILL_DIR` 指本技能的根目录(即 SKILL.md 所在目录)。
> 技能加载时系统会显示 "Base directory for this skill: <路径>",用该路径替换 `SKILL_DIR`。

```bash
SKILL_DIR="<技能根目录,即 Base directory>"
ls "$SKILL_DIR/scripts/node_modules/playwright" >/dev/null 2>&1 \
  && echo OK || (cd "$SKILL_DIR/scripts" && npm install && npx playwright install chromium)
```
若输出 OK 则跳过安装;否则等待安装完成再继续。

## 工作流程(按顺序执行)

### Step 1 · 引导式访谈 → 需求确认卡

**读 `reference/interview-guide.md` 并严格执行**:5 阶段(定位→结构→视觉→版式→输出)+ 收尾确认卡,
共 **16 问 + 1 个大纲确认环节**,每问有默认值与智能跳过规则。配套查询:
- 叙事骨架:`reference/narrative-skeletons.md`(脚手架非模具;用户可选"自由结构")
- 色板预设:`reference/theme-presets.md`(5 套预设 + 自定义 hex 推导)
- 信息密度:`reference/density-tiers.md`(演讲/混合/阅读 三档参数)
- **内容深化:`reference/content-deepening.md`**(**素材形态 × 深度档**二维矩阵定做什么:
  四步追问审素材 → 多角色 → 委员会审大纲;裸主题改出**假设清单**不做追问;
  所有档位都跑**大纲级形式门禁**;大纲 v2 才进 Q5 确认)

**Step 1 执行顺序**:①读 interview-guide 的**推断总表**,从用户首句匹配 deck 族 → 一次定全轴推荐值
②按**依赖图**决定哪些问可跳 ③选路径(快通道 2-3 轮 / 标准 4-6 轮 / 深度 + 深化层)
④逐阶段抛问,置首项说明理由 ⑤深化层按矩阵执行 ⑥Q5 确认大纲 v2。
**任何路径都不跳 Q6 色板 与 Q5 大纲确认**(返工最贵的两个决定)。

访谈收尾:按 `assets/deck-brief.template.md` 生成确认卡展示给用户,
**用户确认后落盘 `slides/deck-brief.md`** —— 此后它是唯一执行事实源;
后续"改第 N 页/换色板"类迭代直接读它,不重访谈。

### Step 2 · 搭目录结构
在当前工作目录生成:
```
assets/theme.css          # 按 brief 色板:复制 assets/presets/<选定预设>.css(自定义色则按推导值生成)
slides/NN-slug.html       # 每页一个文件,两位数字前缀排序
slides/playlist.json      # 从 assets/playlist.template.json 实例化,playlist 按顺序列全页面
slides/deck-brief.md      # Step 1 落盘的需求确认卡
slides/deck-insights.md   # 深化层详档(非快速档才有;模板 assets/deck-insights.template.md)
slides/deck-pages.md      # 页级内容卡(所有档位都有;模板 assets/deck-pages.template.md)
slides/slides.config.json # 从 assets/slides.config.template.json 实例化(键见 scripts/config/default.config.js)
```
目录已存在时,保留用户已有文件,只补缺失项。

**slides.config.json 按 brief 填**(实例化 `assets/slides.config.template.json`):
```json
{
  "design": {
    "tier": "presentation | mixed | reading",
    "minBodyPx": 14,
    "fillThreshold": 0.85,
    "airyPages": ["01-cover.html", "05-statement.html"],
    "formProfile": "balanced",
    "hedgePages": ["07-forecast.html"]
  }
}
```
- 设计检查**默认就是开着的**(缺省 `presentation` + `balanced`);本文件的作用是按 brief
  **校准**档位与豁免页,不是"开启开关"。整份文件缺失时按默认档跑,不会静默放行。
- `design.tier` 由 brief 使用场景映射(演讲→presentation/混合→mixed/阅读→reading);
  决定字号下限与单页信息量上限(见 `reference/density-tiers.md`)
- `design.formProfile` 由 brief 视觉形式偏好映射(克制型→text/平衡型→balanced/丰富型→rich);
  决定 deck 级形式检查口径(纯文字页占比/同形式连排,见 design-principles 第五章)
- `airyPages` 填 brief 中的 airy 页文件名(封面/分隔/大字观点/引用/收尾)——
  **这是唯一豁免填充检查的途径**,漏填会让这些页因"底部留白"被报 WARN
- `hedgePages`(2026-08-06 第六轮)填 `deck-insights.md` 里**降级论断**所在页 →
  validate 会检查这些页确实出现限定词(我们认为/有待验证/预估…),缺失报 WARN。
  作用是把"降级为观点"从措辞变成可审计约束;**不判断内容真伪**(真伪归 Q5 用户判断)
- 其余常用键:`applyFontMap`(brief 演示机字体决定)、`nativeGradient`(原生渐变)、`master`(页码页脚)

### Step 3.0 · 逐页内容卡(写这一页 HTML 之前)

**一页一卡,填完即写这一页**(不要先填完全部卡再统一写页)。载体 `slides/deck-pages.md`
(实例化 `assets/deck-pages.template.md`);工序定义与判据出处见 `reference/content-deepening.md` **第四章**。

七项:①Action title(结论句)②支撑 2-4 条,**每条必须挂一个可验证事实**(数字+单位/专有名词/
时间范围/具体例子)**+ 一个已分类的出处**③口径行(有数字则时间范围+样本+测算方式,估算标注假设)
④逻辑三问(支撑能否推出标题/最强反驳本页答不答/观众下一问下一页答不答)⑤限定词判定 ⑥数据不足退路 ⑦容量核算。

- **② 的出处必须落到六类之一**:素材 §N / insights #N / 用户口述 / 公开可核验(机构+报告名+年份)
  / **模型知识** / 待补。**本技能不联网、无检索** —— 内容只有用户素材、由素材推出的洞察、
  模型自身知识三个来源。出处 = 模型知识时**必须带限定词 + 本页入 `hedgePages`**,或改标"待补"。
  危险的不是用模型知识,是不标注的模型知识(纪律见 content-deepening 第四章"出处纪律")
- **时效自查**(③ 内):本页有市场规模/竞品/政策/价格/排名这类时间敏感项吗?
  有 → 出处不得为"模型知识"(模型知识有截止日),只能是素材/用户口述/公开可核验/待补

- **填卡前先读 `slides/deck-insights.md` 里本页那一行**(行动方案表:核心断言/证据需求/风险旗标/
  待补素材)+ 相关洞察编号 → 填进 ② 的"出处"列与 ⑤。这是深化层产物被真正消费的地方;
  快速档没有 insights,② 出处填素材位置或"待补",⑤ 按本页断言自判
- **② 填不出可验证事实 → 这页现在不该写**:回去补料、换页,或按 ⑥ 退回原型 8 + 待补数据清单
- **⑦ 超标当场处置**(演讲/混合档拆页、阅读档精简措辞)——写完再截图发现就是改一屏
- **⑤ 有降级论断** → 限定词写进页面 + 本页文件名入 `slides.config.json` 的 `hedgePages`
- 快速档降级:只填 ①②③ + 三问第 1 问(⑦ 仍必填),并在 `deck-pages.md` 顶部标"快速档:降级填卡"。
  本工序**不花 agent 调用**,与大纲级形式门禁同例——所有档位都跑

### Step 3 · 逐页写 HTML
1. **按 brief 的骨架页序与密度参数写**(要点数/行数/字号/填充率是硬约束;超标:演讲/混合档拆页,阅读档精简措辞)
2. **写页前只需读两份契约**:`reference/design-principles.md`(设计)+ `reference/html-spec.md`(转换)。
   其余文档**用到才查**,不要通读(读取分层见文末"文件清单")。
   逐页流程:**先定形式**(brief 大纲表"形式"列:文字/图示/图表/图片/混合)
   → **再选原型**(查 `reference/page-archetypes.md` 的索引跳到目标原型,别通读 1800+ 行;咨询分析页型见组 7(31-43))
   → **起手必须用现成件,不从空白页手写**(2026-08-17 第九轮改为默认而非建议):
     先复制 `assets/snippets/INDEX.md` 的片段,或 `assets/slide-template{,-flex,-layout}.html`
     三套样板页(方式 A/B/C),**再改参数**。实测:同一份输入,逐页手搓内联样式的 deck
     (1377/3225 处 `style=`、class 去重 1-2 个)在字号值域与用色纪律上都明显更散
   → **参数一律填变量名,不填 hex**:片段的 `{{BG}}`/`{{ACCENT}}`/`{{GRAD_FROM}}` 等色参数
     填 `var(--brand-dark)` 这种形态。色板外硬编码会被 validate R1/R2 报 WARN(判据见
     `design-principles.md`"用色纪律");需要浅一档/深一档的色**先查梯级令牌**
     (`--brand-primary-soft/-pale`、`--brand-dark-pale/-tint/-mid`、`--ink-soft/-faint`、
     `--surface-sunken`、`--signal-*-soft`),别自己调一个近似值 —— 那正是色值逐页漂的来源
   → 容器内部写法查 `reference/layout-recipes.md`;要图标查 `assets/icons.md`
     (用 `style="stroke:var(--变量)"`,**禁 currentColor**)
2.5 **P2 高级特性**(按需使用,详见 html-spec.md §5;**用法克制,以 design-principles 为准**):
   - `data-shape="chevron|star5|rightArrow|..."` → 80+ 预设几何(流程图/箭头/星形)
   - `data-chart='{"type":"bar",...}'` → 原生可编辑图表(bar/line/area/pie)
   - `<img data-object="true">` → 原生可编辑图片(object-fit 映射;图片政策见 brief)
   - `<video poster src>` / `<audio src>` → 原生音视频嵌入
   - 转场/母版:由 playlist.json / slides.config.json 配置,非页面内属性
3. **布局选择**:骨架(页标题/页码)用方式 A;成组内容(条目/分栏/数字带)优先方式 C 或 B(brief 另有指定时从其指定)
4. **不改结构规则**:
   - 画布 `1920x1080`,`.slide-container` relative + overflow hidden
   - 每个可见元素可归结到 `data-object="true"`;嵌套标记 = ERROR
   - 多行文字显式 `line-height`;字重只用 400/600/700/800/900
   - 文字纯色(半透明先预算混合色);装饰预算每页 ≤3 件;默认左对齐
   - **每个内容页至少一块结构色面**(色带/深色面板/卡片底/表头底纹,≥1.5 万 px²)——
     纯白底+黑字+细线是"素雅单调"的根源,validate 在 balanced/rich 档会报 WARN
   - **颜色只来自 theme.css 色板**(2026-08-17 第九轮):`background`/`color`/`border-color`
     写 `var(--…)`,不写 hex。要浅一档/深一档先查**梯级令牌**(见上 2 的清单),
     没有合适令牌才加进 theme.css + 16 套预设(`node scripts/tools/gen-ladder.js`),
     **不要就地调一个近似值** —— validate R1/R2/R3 会报(判据见 design-principles"用色纪律")。
     `<svg>` 图标豁免此条,但也应写 `style="stroke:var(--变量)"`
   - **正文默认 24-28px**(演讲档),22px 是破档红线而非默认值;深色底上的文字**必须**用
     `--on-navy-text`/`--on-navy-sub`,否则回退近黑压深底、PPTX 里不可见(H13)
   - 纯 `transform:rotate()` 已支持(scale/skew/translate 仍禁);方式 C 子级禁写 position/left/top/width/height
5. 备注按 brief 的备注策略写 `<template data-slide-notes>`

### Step 3.5 · 视觉自查(写完页先过自己这关)
```bash
node "$SKILL_DIR/scripts/preview.js" slides/
```
把每页截成 PNG(slides/.preview/),**逐张看图**,按八条自查。
第 7-8 条自 2026-08-10 第八轮起是**复核**(判断已在 Step 3.0 的内容卡里做过),
查的是"卡上承诺的东西有没有真的落到页面上",不是重新判一遍:
1. **填充率**:内容带是否撑满 320-940?判据不是"底边够低"而是**墨迹铺开** ——
   有没有 ≥200px 的连续空白断层?内容是否一头沉?底部一根细线 + 脚注**不算**撑满。
   不达标 → 回 Step 3 按 scale-to-fill 放大字号/行距/间距
2. **字号**:正文是否明显偏小?演讲档正文默认 **24-28px**(22px 是破档红线,不是默认值);
   页标题/正文比值 <1.6 或全页字号只有两档 → 层级不足,按字号阶拉开
3. **对齐**:卡片/条目边缘是否齐;间距是否一致 → 修正坐标或改方式 B/C
4. **去 AI 味**:对照 brief 的约束清单(kicker/结论条/渐变条是否超编;装饰 ≤3 件;高亮 ≤1 处)
5. **视觉形式**(2026-08-05 起):这页除了文字还有什么?答案为"只有细线"→ 记入纯文字页;全 deck 纯文字内容页占比/同形式连排是否超 brief 的形式偏好档 → 超则换图示原型(23-30),不换内容
6. **结构色面**(2026-08-06 起):这页是不是纯白底 + 黑字 + 细线?内容页至少要有**一块结构色面**
   (色带/深色面板/卡片底/表头底纹)。深色底上的文字有没有用 `--on-navy-*`?
   用错会在 PPTX 里近黑压深底、整块消失(H13)
7. **内容卡兑付 · 支撑与限定词**(2026-08-06 第六轮起限定词;2026-08-10 第八轮改为复核):
   对照本页内容卡 —— ② 每条支撑的**可验证事实**在页面上看得见吗(还是只剩空泛的一句)?
   ⑤ 判定要带限定词的地方带了吗(我们认为/有待验证/预估…),该页在 `hedgePages` 里吗?
   ① 的标题换个 deck 还能用吗(空标题)?**把假设写成结论是 AI PPT 最典型的病**
8. **内容卡兑付 · 数据口径**(2026-08-09 起,数据页与分析论证页):这页有具体数字/百分比/排名吗?
   有则页面上必须真的有那一行来源注(≥16px):**时间范围 + 样本/范围 + 测算方式**,估算标"估算"并给假设
   —— 内容卡 ③ 填的三要素与页面逐项对上没有?适用原型 17-20、31-43。
   卡上 ⑥ 已判"数据不足"的页,页面必须真的退回原型 8,不许中途又编回一个基准。
   判据见 `design-principles.md`"数据页的口径纪律"
发现问题**就地修复并重截**,直到八关全过,再进 Step 4。
**卡与页不一致时改哪个**:页面为准就改卡(排版中发现更好的说法,合法),
但 ②③ 的事实与口径**只能改页面去兑付卡**——不许为了过关把卡上的事实要求划掉。

### Step 4 · 预检(必须零 ERROR)
```bash
node "$SKILL_DIR/scripts/validate.js" slides/
```
- ❌ ERROR → 必须修复后重跑,直到 0 ERROR
- ⚠️ WARN → 逐条判断是否可接受(见 html-spec.md 速查表),可接受就在汇报中说明
- 设计 WARN(文字适配/字号下限/画布填充/对齐,由 slides.config.json 的 design 键启用)→ 优先按 scale-to-fill 修复,这正是视觉质量的自动守门员

### Step 5 · 转换
```bash
node "$SKILL_DIR/scripts/convert.js" ./slides ./slides/playlist.json output.pptx
```

### Step 6 · 汇报
告知用户:PPTX 路径、页数、validate 结果(残留 WARN 及理由)、备注写入情况、deck-brief.md 位置。
如用户装了 PowerPoint,可提示可直接打开 output.pptx 检查。

## 转换机制简述(排查问题时读)

- 管线:加载页面 → 等字体就绪+稳定 → 注入提取脚本 → data-layout 解析 → 提取基元 → 截图 pass → pptxgenjs 渲染
- **原生可编辑**(PPT 中可修改):文字/纯色形状/图片/表格/图表/列表/上下标/字距/渐变(opt-in)/预设几何/旋转/虚线边框
- **截图贴回**(不可编辑):渐变(默认)/background-image/SVG/视觉特效/mix-blend-mode/clip-path(2x DPI,截图前隐藏文字避免重影)
- 文字 run 级样式:斜体/下划线/删除线/超链接/text-transform 原生还原;`<sup>`/`<sub>` 原生上下标
- 配置:`config/default.config.js` 是唯一事实源;项目级 `slides/slides.config.json` 覆盖(如 `{"nativeGradient":true}` 开启原生渐变;`{"master":{"pageNumbers":true}}` 开启页码;`{"incrementalCache":false}` 关闭增量缓存)
- 转场:playlist 项 `{"file":"01.html","transition":"fade"}` → p:transition(fade/push/wipe/cover/split)
- 音视频:`<video poster src>` / `<audio src>` → addMedia 原生嵌入
- 增量缓存:HTML 未变时跳过提取/截图(11x 提速);缓存目录 slides/.cache/
- 叠放 = DOM 深度优先顺序;z-index 只影响浏览器合成
- `<template data-slide-notes>` → 写入该页备注
- 特性速查:`reference/creative-layouts.md` 查渐变/几何/图表等写法(含使用限制);页面形态以 page-archetypes.md 为准
- 回归:`node "$SKILL_DIR/scripts/test/golden.js" verify` 三层等价(L1 提取+L2 XML+L3 截图);行为契约见 `reference/behavior-baseline.md`

## 文件清单

> **2026-08-06 第五轮 P4 重组**:此前 12 份 reference 平铺,"必读"散在各处措辞里,
> 写第一页前要读 13 份文档 + 8 类资产(合计 3700+ 行)—— 实测后果是规范写了不被执行
> (`--text-*` 令牌零引用、正文长期钉在破档线 22px,四轮无人发现)。
> 现按**读取时机**分三层:主干必读只有 3 份,其余按需查。

### 第一层 · 主干必读(只有这三份,合计约 720 行)

| 文件 | 何时读 | 作用 |
|---|---|---|
| `reference/interview-guide.md` | **Step 1 之前** | 5 阶段 16 问 + 1 确认的访谈脚本(含推断总表与依赖图) |
| `reference/design-principles.md` | **写第一页之前** | 设计契约:版面分区/字号阶/满填四判据/12 反模式/结构色面下限/**版面达标≠内容达标** |
| `reference/html-spec.md` | **写第一页之前** | 转换契约:什么写法能无损还原 |

这三份决定输出质量的下限。**其余任何一份都不该在写页前通读。**

### 第二层 · 按需查阅(用到才读,查完即走)

| 文件 | 什么时候需要 |
|---|---|
| `reference/page-archetypes.md` | 选页面形态时 —— **查索引直接跳到目标原型,别通读**(1800+ 行;组 7 为咨询分析页型) |
| `reference/density-tiers.md` | 定档位参数、算填充率与要点数上限 |
| `reference/layout-recipes.md` | 写方式 B/C 的容器骨架 |
| `reference/creative-layouts.md` | 用渐变/几何/图表/旋转等特性,查写法与限制 |
| `reference/content-deepening.md` | 需要四步追问/多角色/委员会(素材×深度矩阵定做什么);**第四章页级内容卡在 Step 3.0 前查**(所有档位) |
| `reference/narrative-skeletons.md` | 定全篇叙事结构 |
| `reference/theme-presets.md` / `brand-styles.md` | 选色板或蒸馏品牌风 |
| `assets/icons.md` | 要图标时复制(`style="stroke:var(--变量)"`,**禁 currentColor**) |
| `assets/snippets/INDEX.md` | 找现成片段(36 个,含参数表与使用限制) |

### 第三层 · 改代码才读

| 文件 | 场景 |
|---|---|
| `reference/behavior-baseline.md` | **改转换管线前必读**(怪癖 H1-H14) |
| `scripts/test/FEATURE-COVERAGE.md` | 增删转换特性或夹具页(硬约束) |
| `CLAUDE.md` | 管线架构、回归纪律、单一事实源规则 |

### 资产与脚本

- `assets/theme.css` — 默认色板(含 12 个梯级令牌)+版面变量;`assets/presets/` — 16 套色板预设
- `scripts/tools/gen-ladder.js` — 按各文件基色重算梯级令牌(改主色/加令牌后跑一次;幂等)
- `assets/deck-brief.template.md` — 需求确认卡模板;`assets/slides.config.template.json` — 项目配置模板
- `assets/deck-insights.template.md` — 深化层详档模板(洞察/假设/委员会意见与裁决/形式门禁/行动方案)
- `assets/deck-pages.template.md` — 页级内容卡模板(Step 3.0 逐页填;**写物不是读物**,不计入写页前阅读量)
- `assets/slide-template{,-flex,-layout}.html` — 三套样板页(方式 A/B/C)
- `assets/playlist.template.json` — playlist 模板
- `scripts/validate.js` — 预检器(ERROR/WARN 分级;设计检查缺省开启)
- `scripts/preview.js` — 视觉自查截图(Step 3.5)
- `scripts/convert.js` — 转换 CLI
- `scripts/test/` — golden 回归 + 样张门禁 + 阈值守卫 + 生成侧回归

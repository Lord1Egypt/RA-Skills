# 特性覆盖矩阵(FEATURE-COVERAGE)

> golden fixtures 的"特性 → 锚定页"台账(2026-08-02 Phase G 建立)。
> **登记规则(硬约束)**:
> 1. 新增转换器特性(基元/样式/元素/配置)时,必须指定锚定页并更新本表;无锚定页的特性不得合并。
> 2. 删除夹具页前,先查本表确认它不是某特性的唯一锚点。
> 3. 样张页(96-107、110-117、118-130)同时受 `test/exemplar-checks.js` 设计门禁(0 ERROR/0 WARN)。
> 4. **2026-08-06 第五轮 P5**:本表的锚点关系已由 `test/anchor-integrity.js` 变成**可执行断言**
>    —— 改样张设计时若换掉了承载特性的元素,守卫会失败(唯一锚点失效 = 致命)。
>    新增/换锚时**同步改该守卫的 ANCHORS 表**,否则台账与守卫脱节(守卫自身会警告)。

### 样张双角色的已知张力(2026-08-06 定型)

样张页身兼"设计范本 + 转换锚点"两职。曾考虑让样张退出 L2/L3 基线以解耦,**经查证不可行**:
`99-archetype-chart` 是 `data-chart:line` 的唯一锚点,`107-dashboard` 是 pie/doughnut/area 的唯一锚点,
`112-funnel` 是 `data-shape="trapezoid"` 的唯一锚点 —— 退出即等于删除这些特性的转换覆盖。

实测澄清了成本结构:这 9 页**本来就不在 L3**(2026-08-05 瘦身:L3 只截含 capture 基元的页),
所以改设计的成本只有 L1+L2 重建,而那是"输出确实变了"的证据,不是冗余开销。
真正的风险不是重建成本,而是**改设计会静默摧毁转换覆盖**:实测把 99 页的 `data-chart` 换成纯文本后,
样张门禁 ✅、生成侧回归 ✅,只有 golden 报 diff —— 而"我重排了这页"的 diff 复核里重建基线是自然动作。
故结论:**保留双角色,用 `anchor-integrity.js` 守住锚点**,而不是拆分角色。
> 页面角色:fidelity 锚(01-21 精简页/游离页/特性页)= 转换保真;exemplar 样张(96-107、110-117、118-130)= 保真+设计纪律双锚。
> 2026-08-05 第三轮重构(布局丰富度):零管线改动;新增样张 110-117 锚定组 6 图示原型(23-30)与内联 SVG 图标。
> 2026-08-09 第七轮重构(咨询分析布局):零管线改动;新增样张 118-130 锚定组 7 分析论证原型(31-43)。
> 新增四个唯一锚点:`data-chart:scatter`→123、`data-shape="pie"`→120、`data-shape="diamond"`→122、td 级底纹→125。

## 一、文字类

| 特性 | 锚定页 | 备注 |
|---|---|---|
| 斜体 `<i>/<em>` | 90-p0-features、49-four-layer、chip-market-share | 49-four/chip 是历史缺陷修复锚 |
| 下划线 / 删除线 / 超链接 | 90-p0-features | run 级 |
| run 级字体 fontFace | 90-p0-features、96-107(`.num`) | `.num` Inter 混排是真实场景锚 |
| text-transform | 90-p0-features | uppercase/lowercase |
| 上下标 `<sup>/<sub>` | 93-p2-sup-sub-geo | baseline 30000/-40000 |
| run 级字距 charSpacing | 93-p2-sup-sub-geo | 与 box 级独立 |
| 原生列表 `<ul>/<ol>` bullet | 91-p1-forms、01-cockpit 压测(临时) | LI 直接含文字挂 bullet;**2026-08-05 H11 修复**:旧写法 type+characterCode 永不产 buChar;现 UL 无 type、OL 用 style |
| pre/code 空白保留 | 91-p1-forms | white-space:pre |
| 竖排 writing-mode | 49-four-layer | 实验性 eaVert(基线 WARN) |
| 混合字号行 | 98-statband、107-dashboard | 大数字+单位,行高按最大 run |
| 500 字重退化 WARN | advice-for-newcomers、ai-trends-2026、four-revolutions | validate 基线锚 |

## 二、形状/装饰类

| 特性 | 锚定页 | 备注 |
|---|---|---|
| 纯色形状 / 圆角 / 正圆 | 全体 | 基础 |
| 统一边框 | 02 等 | px→pt(0.5 倍) |
| 非统一边框逐边细条 | 02、12 | 圆角共存 WARN 锚 |
| 虚线/点线 dashType | 90-p0-features | dashed→dash,dotted→sysDot |
| box-shadow 真实参数 | 07-journey-map、data-limit-boundary、90 | 历史缺陷修复锚(行为红线) |
| 纯旋转 rotate | 90-p0-features、93-p2-sup-sub-geo | origin 居中约束 |
| data-shape 预设几何 | 93-p2-sup-sub-geo、111(chevron/homePlate)、112(trapezoid+rotate)、116(triangle/trapezoid) | 15 种(白名单 80+) |
| 不透明度 opacity 折算 | 全体(基础路径) | 形状填充折算 |
| 内联 SVG 图标(截图) | 110/114/115/117(卡内嵌套)、113(环形箭头) | 2026-08-05;stroke 显式 hex;currentColor→空白(H7 怪癖) |
| 组 6 图示原型 | 110 图标网格(23)/111 chevron 带(24)/112 漏斗(25)/113 循环(27)/114 辐射(28)/115 色带(30)/116 金字塔(26)/117 对比卡阵(29) | 2026-08-05 第三轮;exemplar 门禁 0/0 |
| `data-shape="pie"` 扇形(Harvey ball) | **120-harvey-matrix**(唯一锚点) | 2026-08-09;圆饼打分格,与 ellipse 描边配套表达五档 |
| `data-shape="diamond"` 菱形(里程碑) | **122-swimlane-gantt**(唯一锚点) | 2026-08-09;压网格线的里程碑标记 |
| 组 7 分析论证原型 | 118 执行摘要(31)/119 议题树(32)/120 评估矩阵(33)/121 瀑布(34)/122 泳道甘特(35)/123 散点(36)/124 驱动树(37)/125 热力(38)/126 情景(39)/127 规模拆解(40)/128 成熟度(41)/129 价值链(42)/130 对标(43) | 2026-08-09 第七轮;零管线改动;exemplar 门禁 0/0 |
| preview data-shape clip-path 近似 | 111/112/116(仅 preview 截图层) | H8;页面文件不动 |

## 三、背景/媒体类

| 特性 | 锚定页 | 备注 |
|---|---|---|
| 渐变(截图路径,默认) | 01、94-p2-gradient | 2x DPI |
| 原生线性渐变 a:gradFill | **已知缺口(有意)** | `nativeGradient` 默认关;开启路径由 convert 冒烟覆盖,未入 golden(见"五") |
| `<img>` 原生图片 | 91-p1-forms | object-fit 映射;file:// 路径(注意环境漂移) |
| `<table>` 原生表格 | 91-p1-forms、106-table-focus | colspan/底纹/边框/右对齐;**2026-08-05 H12 修复**:tr 级底纹(background 不继承到 td)原丢失,现沿 td→tr→table 回溯 |
| `<canvas>` 截图 | 92-p1-chart-visual | 可见化保底 |
| data-chart:bar | 92-p1-chart-visual | 原生图表 |
| data-chart:line | 99-archetype-chart | |
| data-chart:pie / doughnut / area | 107-dashboard | 2026-08-02 Phase G 补锚 |
| data-chart:scatter | **123-scatter-map**(唯一锚点) | 2026-08-09;`series[0]`=X 轴值,`lineSize:0` 去连线。**bubble 当前渲染器不支持**(数据装配不符,见"已知缺口") |
| `<svg>` 截图 | data-limit-boundary | 整体截图含文字 |
| `<video>` / `<audio>` | 95-p2-master-media | addMedia;poster 封面 |
| 图标字体自动截图 | 92-p1-chart-visual | iconFonts 命中 |
| mix-blend-mode / clip-path 转截图 | 92-p1-chart-visual | 视觉特效 |

## 四、布局/页面级

| 特性 | 锚定页 | 备注 |
|---|---|---|
| 方式 A 绝对定位 | 全体 | |
| 方式 B flex/grid 流式 | 02、96-editorial、104-comparison | |
| 方式 C data-layout(columns/grid) | 98-statband、103-split-7-5、107-dashboard | 解析器改写 |
| 母版 pageNumbers + footer | **全体 L2 页**(fixtures/slides.config.json) | 2026-08-02 Phase G 开启 |
| 转场 fade/push/wipe/cover/split | 96/97/98/99/100(playlist 项) | 2026-08-02 Phase G 开启,五档齐 |
| 深底容器背景导出 | 97-archetype-divider、01 | |
| 演讲者备注 template | 全体 | notesSlide XML |
| 增量缓存 | L2 全 deck | hash 命中/失效 |
| design.formProfile deck 级形式检查 | 开发期构造用例(5 页纯文字单调 deck → 2 WARN) | 2026-08-05;缺省/text 休眠,fixtures 无 profile 零影响 |

## 五、行为锚点(回归红线活证据,删页红线)

| 页 | 锚定的历史行为 |
|---|---|
| 49-four-layer-overview | 斜体提取修复(4 处)+ 竖排 eaVert |
| chip-market-share | 斜体提取修复(1 处) |
| 07-journey-map | box-shadow 真实值化(4 处) |
| data-limit-boundary | box-shadow 真实值化(7 处)+ SVG 截图 |
| advice-for-newcomers | 字体时序加固(L1 height 抖动 37→39px) |
| ai-trends-2026 / four-revolutions | 500 字重 WARN 基线 |

## 六、设计质量检查的锚定页(2026-08-06 第四轮 P3 建立)

> 这些是 **validate 设计检查**(非转换器特性)的锚定页,由 `test/exemplar-checks.js` 断言 0 ERROR/0 WARN。
> 与转换器特性同规则:新增设计规则必须在此登记锚定页;改这些页前先查本表。
> 判据阈值与设计契约同源 —— 改阈值须同步 `reference/design-principles.md` 第一/二章。

| 检查(规则号) | 正向锚定页(应通过) | 反向自证方式 | 标定实测值 |
|---|---|---|---|
| 文字对比度(layout-checks 5) | 97/103/117(深底页,用 `--on-navy-*`) | 把 `--on-navy-text` 改成 `#1F1F1F` → 97 页立即 2×ERROR(1.22:1) | 全 44 页命中 0;豁免 ≥120px 水印数字、≤2 字符纯符号 |
| 墨迹行覆盖率(dom-checks 14a) | 96/104/105/106/107/111(P5 重排后 58-97%) | 105 重排前实测 29% | 阈值 55%;airy 页(97/101/102)整条豁免 |
| 连续空白断层(dom-checks 14b) | 同上(重排后 20-110px) | 96 重排前 330px | 阈值 200px |
| 上下分布偏斜(dom-checks 14c) | 全样张 | — | 阈值任一半 ≤88% |
| 字号层级(dom-checks 15) | 全样张(比值 2.1-4.7) | 构造同字号页 → WARN | 页标题/正文 ≥1.6;字号档数 ≥3;正文样本限 top≥320 |
| 结构色面下限(dom-checks 16) | 96/98/99/100/104/105/106/107/111(色面 13.9-45%) | 96-107 段重排前 10 页色面 **恰好 0%** | ≥1 块(≥1.5 万 px²)或 ≥8%;仅 balanced/rich 档 |
| 企业黑话密度(dom-checks 17) | 全语料(一档命中最高 1 次 / 11.5‰) | 构造空话页 → WARN(5 次 / 32 字 = 156‰) | ≥40‰ 且 ≥3 次;二档词(对齐/协同/沉淀/闭环)不计 |
| **限定词落地(layout-checks 6)** | 无常设锚定页(按设计:`hedgePages` 缺省 `[]`,旧夹具零命中) | 注入式自证:构造两页(同内容,一页含"我们认为/有待验证")→ 登记进 `hedgePages` → 未含限定词页 WARN、含限定词页静默;未登记页零命中 | 限定词表 7 词;只查内容区(top < footerZoneTop 980),`<template>` 备注不计 |
| **色板外用色 R1 / R1b(palette-checks)** | 全 33 张样张(迁移后裸色仅剩 `<svg>` 内与 rgba 阴影,两者均豁免) | `generation-checks.js` C4a 构造式自证:整页写死另一套预设色值 → 逐色 WARN | 容差 ΔRGB ≤6 判"近似重打";同页色板外色 ≥3 种升级为"整页脱离色板" |
| **var() 占比 R2(palette-checks)** | 全 33 张样张(迁移后色声明 var() 占比 100%) | C4b:零 var() 页 → WARN | 色声明 ≥4 处才判;占比下限 70%(实测样张中位 95%、坏 deck 0%) |
| **整套色板未生效 R3(index.js deck 级)** | 全 33 张样张(交集充足) | C4c:4 页全用另一套预设色 → deck 级 WARN | 裸色种类 ≥5 种才判;前 8 高频色与色板交集 <3。**与 R2 互补**:用对色板但写死 hex 时 R3 沉默、R2 抓 |

**exemplar-checks 的 DESIGN 档**:`presentation` + `balanced` + airyPages(97/101/102)。
`formProfile` 是 2026-08-06 补的 —— 缺该键时规则 16 在样张上从不触发(样张自己得先过 balanced 档)。

## 七、已知缺口(有意/待办)

| 缺口 | 状态 | 说明 |
|---|---|---|
| 原生渐变(nativeGradient:true)渲染路径 | 有意未入 golden | D2 拍板默认关;建议后续建第二 playlist(独立 config)锚定 |
| validate ERROR 触发路径 | 未系统锚定 | 目前以 0 ERROR 通过反向验证;ERROR 构造用例散见于开发期,低优先。例外:对比度 ERROR 已有注入式自证(见上表) |
| 全出血大图页(原型 11)/ 图文页(原型 10) | 样张未含 | 图片型页面已有 91 img 锚定;后续按需要补样张 |
| `95-p2-master-media.html` 引用的 `demo.mp4` | 仓库中从未存在 | 转换时报"媒体文件不存在"警告并跳过;媒体嵌入路径因此未被真正锚定(2026-08-06 发现,先登记不修) |
| 深化层产物本身的质量 | **有意未测**(2026-08-06 第六轮 P6 决策) | D 组能断言深化层的**结构**(计数一致、总表取值合法、依赖图完备、字段对齐、角色覆盖、阈值同源),但无法断言"这条洞察是否真的深刻""这次委员会是否真的改进了大纲"。丢弃率是委员会的自体检指标,不是质量判据。内容质量的最终闸仍是 Q5 用户确认 —— 机器不越位 |
| `--text-*` 字号令牌零引用 | **已知未修**(2026-08-06 P4 决策) | 语料/片段/原型库共 59 处硬编码 font-size,`--text-*` 引用数为 **0** —— 字号阶仍只存在于文档。未迁移的原因:`--text-body: 24px` 与页面现用 26px 不等值,迁移会**实际改变字号**而非纯重构,且要重建一轮基线。替代保护:`generation-checks.js` 的 A1/A2/A3 已能拦住"令牌缺失/下限当默认值/正文破档"三类漂移,故迁移收益有限、可延后 |
| `data-chart:bubble` 气泡图 | **不支持,有意未修**(2026-08-09) | 实测 `renderChart` 喂 bubble 的数据形状不符 pptxgenjs 预期,抛 `Cannot read properties of undefined`。原型 36 因此声明"需要第三维时写进点标注",不给气泡骨架。要支持需改 `render/chart-renderer.js` 的 bubble 数据装配(约 10 行)+ 补锚点页 + 重建 L2 基线 —— 本轮不做,以免把纯文档改动扩成管线改动 |
| 数据页口径纪律的机器约束 | **有意不做 validate 规则**(2026-08-09) | 机器只能查"页底有没有一行 ≥16px 小字",查不了那行字是否诚实;做成外观检查会催生"贴一行假来源过检"(与 design-principles 记录的"1px 细线+脚注凑底边"同一类失败)。故落为写作纪律 + SKILL Step 3.5 第 8 条自查。若要机器化,正确形态是 `slides.config.json` 显式登记数据页与口径(声明式,像 `airyPages`/`hedgePages`) |

## 八、corpus 账本(2026-08-02 Phase G 定稿;2026-08-05 第三轮更新 + 瘦身)

- L1/L3:36 页 + 8 样张(110-117)+ 13 样张(118-130)+ 模板 3(extraPages)= **60**
- L2 playlist:32 页 + 8 样张 + 13 样张 = **53**(10 精简 deck + 4 游离 + 6 特性 + 33 样张)
- 退役:06/16/18(重复)+ 04/07/10/13/14/17/19/20(精简)= 11 页
- **2026-08-05 瘦身(golden.js)**:L2 notesSlide 合并为单项锚定(53 文件 → 1 项,差异时明细列文件);L3 仅含 capture 基元页截图(19 页;41 纯原生页由 L1 完全锚定免截图);孤儿 PNG(退役 11 页)已清。比对项 174 → **107**(2026-08-05),磁盘 6.4MB → 2.7MB,保护范围不减
- **2026-08-09 第七轮**:新增 13 页组 7 样张(118-130),比对项 107 → **133**(L1 60 + L2 54 + L3 19)。这 13 页**全为纯原生**(无 capture 基元),故 L3 截图数不变、免截图数 28 → 41 —— 新增成本只落在 L1/L2

# 页面原型库(page-archetypes · 43 个原型)

> **口径(2026-08-06 第六轮 P1 归一)**:全库 **43 个编号原型**(`### 原型 1` … `### 原型 43`)。
> 此前标题写"28 个原型 30 款"、而 narrative-skeletons/creative-layouts 写"20 原型"——
> 三处三个数,且"20 原型"的说法让**图示组(23-30)在引用方的自我描述里不存在**。
> 现统一由 `test/generation-checks.js` D1 实测编号数并断言各文档措辞一致。

> **组 7 · 分析论证(2026-08-09 新增,原型 31-43)**:此前全库按"视觉形态"完备、按"分析论证"残缺 ——
> 有把数字**陈列**出来的页(17-20),没有把数字**推成一个可被质疑的结论**的页。
> 咨询页型的共同特征不是更花,而是**页面本身携带推理结构**:一页里同时有主张、支撑、口径,
> 以及"我知道你会怎么反驳"。执行摘要/议题树/评估矩阵/瀑布/甘特/散点/驱动树/热力图此前全为零。
> 本组零管线改动(与第三轮新增 23-30 同构),但**必须配口径纪律**(见 design-principles"数据页的口径纪律")——
> 分析页型没有出处与口径就会退化成"看起来很咨询的空页"。

> ⚠️ **别通读本文件(1500+ 行)。** 用法是**查索引 → 跳到那一个原型小节 → 读完即走**。
> 全文只有下面的「索引」表需要扫一遍;43 个原型小节按需单点查阅。
> (2026-08-06 第五轮 P4:此前它被列为"写页首选起点",导致每次写页都通读,
> 挤占了真正该读的两份契约的注意力。)

> **人类专业 PPT 的页面类型学。** 写页先选原型,再填内容——原型决定"这一页怎么摆",配方(`layout-recipes.md`)只管容器内部写法。
> 每个原型:用途 / 何时别用 / 填充行为(满填|airy) / HTML 骨架 / 参数表 / 反 AI 味要点。
> 骨架全部遵循 `design-principles.md`(分区/字号阶/scale-to-fill/**视觉形式**)与 `html-spec.md`(转换契约);字号以**演讲档**标注,其他档位按 design-principles 字号阶等比换算。
> **选原型流程(二级,2026-08-05 起)**:访谈 Q5 大纲确认时**先定视觉形式**(文字/图示/图表/图片/混合,写入 brief 形式列,按 Q8c 档位与信息结构)→ **再从该形式组选原型** → 写页时只查 brief 指定的原型小节。

## 索引

| 组 | 原型 | 形式 | 填充 | 一句话 |
|---|---|---|---|---|
| 开场导航 | 1 封面·深底大字 | 文字(airy) | airy | 深底+超大标题+细强调条 |
| | 2 封面·浅底编辑 | 文字(airy) | airy | 浅底+左对齐巨标+底部信息行 |
| | 3 议程 | 文字 | 满填 | 大数字编号裸列表 |
| | 4 章节分隔 | 文字(airy) | airy | 超大编号+章节名 |
| | 5 大字观点 | 文字(airy) | airy | 一句话占满页 |
| | 6 引用页 | 文字(airy) | airy | 巨引号+引文+署名 |
| 论述 | 7 编辑文字页 | 文字 | 满填 | action title+双栏文字,零卡片 |
| | 8 要点列表 | 文字 | 满填 | 粗体引导裸排要点+细分隔线 |
| | 9 不对称分栏 7:5 | 混合 | 满填 | 主栏论述+辅栏深面/数据 |
| | 10 图文页 | 图片 | 满填 | 左图右文(可镜像) |
| | 11 全出血大图页 | 图片 | 出血满填 | 图满画布+左下文字块 |
| 对比流程 | 12 双栏对照 | 文字 | 满填 | 旧vs新/AvsB+中缝 |
| | 13 流程步骤 | 文字/图示(chevron 款) | 满填 | 横向步骤带(大数字或 chevron) |
| | 14 时间线 | 图示 | 满填 | 横轴实线+圆点+交替标签 |
| | 15 2×2 象限 | 图示 | 满填 | 坐标轴+四象限+点位 |
| | 16 层级 | 图示 | 满填 | 3-4 层横条,上窄下宽 |
| 数据 | 17 大数字带 | 文字 | 满填 | 3-4 个巨数字+标签,细线分隔 |
| | 18 图表主角 | 图表 | 满填 | 大图表(1100px)+右侧解读栏 |
| | 19 表格主角 | 图表 | 满填 | 大表格居中,表头深色 |
| | 20 仪表盘 | 图表 | 满填 | KPI 行+图表+表格(阅读/混合档) |
| 收尾 | 21 行动号召 | 文字(airy) | airy | 深底+大字行动句+联系方式 |
| | 22 附录指引 | 文字 | 满填 | 资料清单编辑式排版 |
| **图示(2026-08-05 新增)** | 23 图标要点网格 | 图示 | 满填 | 2×2/2×3 图标卡:图标+标题+说明 |
| | 24 chevron 流程带 | 图示 | 满填 | 3-5 步箭头链+下方说明列 |
| | 25 转化漏斗 | 图示 | 满填 | trapezoid 叠层收窄+左右侧注 |
| | 26 金字塔 | 图示 | 满填 | 三角+梯形真分层(3-4 层) |
| | 27 循环图 | 图示 | 满填 | SVG 环形箭头+中心命题+4 节点 |
| | 28 中心辐射 | 图示 | 满填 | 中心圆+4 卫星卡+细连接线 |
| | 29 对比卡阵 | 图示 | 满填 | 双卡对决+中央 VS 徽章+图标行 |
| | 30 色带分节页 | 图示 | 满填 | 横向纯色带 stack,每带一主张 |
| **分析论证(2026-08-09 新增)** | 31 执行摘要 | 混合 | 满填 | 统领结论面板+3 支柱+来源行 |
| | 32 议题树 MECE | 图示 | 满填 | 根问题→分支树,同层互斥完全穷尽 |
| | 33 评估矩阵 | 图表 | 满填 | 方案×准则打分表,Harvey ball 填充度 |
| | 34 瀑布桥图 | 图示 | 满填 | 起止柱+浮空增减柱,变动分解 |
| | 35 泳道甘特 | 图示 | 满填 | 责任方×阶段横条+里程碑菱形 |
| | 36 散点定位图 | 图表 | 满填 | 原生 scatter+象限参考线+点标注 |
| | 37 驱动因素树 | 图示 | 满填 | KPI 根+运算符徽章+因子分解 |
| | 38 热力评估矩阵 | 图表 | 满填 | 维度×对象逐格三档底纹+图例 |
| | 39 情景分析 | 图示 | 满填 | 悲观/基准/乐观三栏+关键假设行 |
| | 40 规模拆解 | 图示 | 满填 | TAM/SAM/SOM 嵌套+右侧算式链 |
| | 41 成熟度阶梯 | 图示 | 满填 | 5 级递升条+当前位标记 |
| | 42 价值链 | 图示 | 满填 | 主活动 chevron 带+支撑活动带 |
| | 43 标杆对标 | 图表 | 满填 | 对标表+基准参考线+自身行高亮 |

---

## 组 1 · 开场导航

### 原型 1 · 封面 · 深底大字(airy)

**用途**:deck 第一页;产品发布/路演/汇报通用。**何时别用**:全浅基调 deck(用原型 2)。
**填充**:airy —— 文字块垂直居中偏上,底部信息行贴页脚区。

```html
<div class="slide-container" style="background:var(--deep-navy);">
  <!-- 细强调条(装饰 1 件) -->
  <div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:420px;width:120px;height:6px;background:var(--accent-orange);"></div>
  <!-- 主标 88-120px,最多两行 -->
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:460px;width:1600px;">
    <div style="font-size:104px;font-weight:800;line-height:1.15;color:var(--on-navy-text);letter-spacing:-1px;">
      标题一句话,<br>最多两行
    </div>
  </div>
  <!-- 副标:一句话承诺 28-32px -->
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:720px;width:1400px;">
    <div style="font-size:30px;font-weight:400;line-height:1.4;color:var(--on-navy-sub);">一句话承诺或定位</div>
  </div>
  <!-- 底部信息行:汇报人/日期,18px -->
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:980px;width:1720px;">
    <div style="font-size:22px;line-height:1.4;color:var(--on-navy-dim);">汇报人 · 机构 · 2026-08</div>
  </div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 主标字号 | 88-120px,一行能放下就取大值 |
| 强调条位置 | 主标上方 40px;是唯一装饰 |
| 深底 | `var(--deep-navy)` 或品牌深底色 |

**反 AI 味要点**:❌ 不加 kicker/徽章/渐变英雄区/装饰图形;✓ 克制 = 一根强调条 + 三级文字。标题即定位,不写"XX 汇报 PPT"。

---

### 原型 2 · 封面 · 浅底编辑(airy)

**用途**:全浅基调 deck(阅读档/学术/编辑杂志风)。**何时别用**:需要开场冲击力(用原型 1)。
**填充**:airy —— 巨标靠上 1/3,信息行贴底。

```html
<div class="slide-container" style="background:var(--off-white);">
  <!-- 眉题:机构/性质,20px 字距 4px -->
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1200px;">
    <div style="font-size:20px;font-weight:600;letter-spacing:4px;color:var(--text-tertiary);">机构名 · 报告性质</div>
  </div>
  <!-- 巨标 96-120px 左对齐 -->
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:200px;width:1700px;">
    <div style="font-size:110px;font-weight:800;line-height:1.12;color:var(--charcoal);letter-spacing:-1.5px;">
      编辑式大标题,<br>像杂志封面
    </div>
  </div>
  <!-- 细分隔线 -->
  <div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:920px;width:1720px;height:1px;background:var(--border-medium);"></div>
  <!-- 信息行 -->
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:950px;width:1720px;">
    <div style="font-size:22px;line-height:1.4;color:var(--text-secondary);">作者 · 日期 · 版本</div>
  </div>
</div>
```

**反 AI 味要点**:巨标是唯一主角;❌ 不要色块/渐变/卡片。编辑感靠**字号反差 + 留白**。

---

### 原型 3 · 议程(满填)

**用途**:第 2 页,给全 deck 导航。**何时别用**:≤5 页的短 deck(直接进内容)。
**填充**:满填 —— 条目在内容区 320-940 **均匀分布**(条目少就拉大间距与字号)。
**丰富档(2026-08-02 测试反馈)**:副题写"这章会怎么讲"(例子/问题/承诺),不要只写章节名——"从 X 说起""每个都问:它改变了谁的工作"这类带钩子的副题,让议程页有信息量而非占位。

```html
<!-- 页标题(action title 可省,议程页允许"议程/今天讲三件事"式) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.15;color:var(--charcoal);">今天讲三件事</div>
</div>
<!-- 编号裸列表:方式 B,条目纵向分布 -->
<div style="position:absolute;left:100px;top:320px;width:1720px;display:flex;flex-direction:column;gap:0;">
  <!-- 条目 1:大数字 + 标题 + 一句话,底部细线 -->
  <div data-object="true" data-object-type="shape" style="height:200px;border-bottom:1px solid var(--border-light);display:flex;align-items:center;gap:40px;">
    <div class="num" style="font-size:64px;font-weight:800;color:var(--lenovo-red);line-height:1;">01</div>
    <div>
      <div style="font-size:30px;font-weight:700;line-height:1.3;color:var(--charcoal);">章节标题</div>
      <div style="font-size:24px;line-height:1.4;color:var(--text-secondary);margin-top:6px;">一句话说明这章回答什么问题</div>
    </div>
  </div>
  <!-- 条目 2、3 同构;height 按 620/条目数 均分 -->
</div>
```

| 参数 | 调什么 |
|---|---|
| 条目数 | 3-5 条;条目高 = 620÷N(3 条 ≈ 200px,5 条 ≈ 124px) |
| 数字字号 | 条目高 ≥180px 时 64px;否则 48px |
| 末条细线 | 最后一条去 border-bottom |

**反 AI 味要点**:❌ 不装卡片、不套圆圈;✓ 大数字+细线就是最专业的议程。章节名必须与后续分隔页/kicker 一致。
**图示化升级**:章节 3-4 个且形式偏好为丰富型 → 改原型 30 色带分节页(每带一章)。

---

### 原型 4 · 章节分隔(airy)

**用途**:章与章之间换节奏。**何时别用**:≤6 页短 deck 或单章 deck。
**填充**:airy —— 超大编号+章节名居中偏左;可深可浅(与封面同底最稳)。

```html
<div class="slide-container" style="background:var(--deep-navy);">
  <!-- 超大编号 240px,半透明感用预算混合深色(非 rgba 文字) -->
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:80px;top:180px;width:800px;">
    <div class="num" style="font-size:240px;font-weight:800;line-height:1;color:var(--deep-navy-light);">02</div>
  </div>
  <!-- 章节名 64px -->
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:560px;width:1500px;">
    <div style="font-size:64px;font-weight:800;line-height:1.2;color:var(--on-navy-text);">章节标题</div>
  </div>
  <!-- 一句话 24px -->
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:680px;width:1400px;">
    <div style="font-size:24px;line-height:1.5;color:var(--on-navy-sub);">这一章回答的一个问题</div>
  </div>
</div>
```

**反 AI 味要点**:编号用"比深底浅一号"的混合色做水印感;❌ 不加渐变条/徽章/装饰图形。浅底变体:编号 `--border-light`、标题 `--charcoal`。

---

### 原型 5 · 大字观点(airy)

**用途**:全 deck 最重要的一句话(主张/转折/结论前置);呼吸页。**何时别用**:没有值得独占一页的话。
**填充**:airy —— 文字垂直居中。

```html
<div class="slide-container" style="background:var(--off-white);">
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:200px;top:400px;width:1520px;">
    <div style="font-size:72px;font-weight:800;line-height:1.25;color:var(--charcoal);text-align:center;">
      全 deck 最重要的那句话,<br>独占一页
    </div>
  </div>
  <!-- 可选:一行佐证 22px -->
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:200px;top:640px;width:1520px;">
    <div style="font-size:26px;line-height:1.5;color:var(--text-secondary);text-align:center;">—— 一个数字或来源作佐证</div>
  </div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 字号 | ≤20 字 → 80px;20-35 字 → 72px;>35 字 → 删字,不降 64px 以下 |
| 强调 | ≤1 处 span 变色(主色),全页唯一高亮 |

**反 AI 味要点**:这是"居中崇拜"的合法场景之一;❌ 不加 kicker/页码/装饰。深底变体同原型 4 配色。

---

### 原型 6 · 引用页(airy)

**用途**:金句/客户证言/专家观点;呼吸页。**何时别用**:没有真引用(不要编造)。
**填充**:airy。

```html
<div class="slide-container" style="background:var(--off-white);">
  <!-- 巨引号 200px,主色 -->
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:140px;top:200px;width:300px;">
    <div style="font-size:200px;font-weight:800;line-height:1;color:var(--lenovo-red);">"</div>
  </div>
  <!-- 引文 40-48px -->
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:180px;top:440px;width:1400px;">
    <div style="font-size:44px;font-weight:600;line-height:1.4;color:var(--charcoal);">引文一到两句,保持原话</div>
  </div>
  <!-- 署名 20px -->
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:180px;top:700px;width:1400px;">
    <div style="font-size:22px;line-height:1.5;color:var(--text-tertiary);">—— 姓名 · 头衔 · 出处</div>
  </div>
</div>
```

**反 AI 味要点**:❌ 不用渐变左边框+斜体的"AI 引用块"(那是旧模式 6);✓ 巨引号+正体。引文 >3 行就删减,不降字号。

---

## 组 2 · 论述

### 原型 7 · 编辑文字页(满填)—— 去 AI 味主力

**用途**:讲清一个道理(背景/分析/论证);替代"三卡片"的首选。**何时别用**:真并列实体(用原型 9/12)。
**填充**:满填 —— 双栏文字从 320 排到 940。

```html
<!-- action title 两行 60px -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">
    结论式标题:这一页只讲一个道理,<br>标题把它说完
  </div>
</div>
<!-- 双栏文字:方式 B,栏宽 840/840 gap 80 -->
<div style="position:absolute;left:100px;top:340px;width:1720px;display:flex;gap:80px;">
  <div data-object="true" data-object-type="textbox" style="flex:1;">
    <div style="font-size:24px;line-height:1.7;color:var(--text-primary);">
      <span style="font-weight:700;color:var(--charcoal);">粗体引导句。</span>正文段落,每段 3-4 行,讲清一个论据。行距 1.7 是编辑感的来源。
      <br><br>
      第二段,段间用空行而不是缩进。全栏 4-8 行,自然排到底。
    </div>
  </div>
  <div data-object="true" data-object-type="textbox" style="flex:1;">
    <div style="font-size:24px;line-height:1.7;color:var(--text-primary);">第二栏继续论证或给例证、数据引用。</div>
  </div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 栏数 | 2 栏为主;阅读档可 3 栏(gap 60) |
| 正文字号 | 演讲档 24px/行高 1.7;每栏 4-8 行 |
| 引导句 | 每段 1 句粗体,是唯一"强调"(反模式 9) |

**反 AI 味要点**:❌ 零卡片、零 kicker、零图标;✓ 像《经济学人》内页。这页是"内容密度"与"专业感"兼得的原型,演讲档每 deck 至少 2 页。
**图示化升级**:论据为 2-4 个并列点 → 改原型 23 图标网格;分节主张 → 改原型 30 色带。

---

### 原型 8 · 要点列表(满填)

**用途**:3-6 个要点(结论清单/建议/原则)。**何时别用**:要点是并列实体(产品/方案)→ 原型 12 或卡片矩阵(限额内)。
**填充**:满填 —— 条目均分内容区。
**丰富档(2026-08-02 测试反馈)**:每页 2 条"例子/证据"——要点页只写判断会显得"素"。写法:要点区收窄(每条 150px),下方加一行 26px 例子(如"效果(真实试点):检索耗时 11→6.4 分钟")+ 一行 16px 来源注。克制是纪律,内容单薄是失误。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">三个判断,结论先行</div>
</div>
<div style="position:absolute;left:100px;top:320px;width:1720px;display:flex;flex-direction:column;">
  <!-- 条目:粗体引导词 + 说明,底部细线 -->
  <div data-object="true" data-object-type="shape" style="height:150px;border-bottom:1px solid var(--border-light);display:flex;align-items:center;">
    <div style="font-size:26px;line-height:1.5;color:var(--text-primary);">
      <span style="font-weight:700;color:var(--charcoal);">判断一:</span>一句话说清这个判断,不超过两行
    </div>
  </div>
  <!-- 条目 2、3 同构;4 条 → 每条高 155px,3 条 → 每条 200px 且字号 28px -->
</div>
```

| 参数 | 调什么 |
|---|---|
| 条目数/高度 | 3 条 ×200px(字号 28)｜4 条 ×155px(26)｜5-6 条 ×125/105px(24) |
| 引导词 | 2-6 字粗体(判断一/建议 2/原则③),后接冒号 |
| 细线 | 相邻条目间 1px `--border-light`;末条无 |

**反 AI 味要点**:❌ 序号圆圈、卡片、图标全免;✓ 粗体引导词+细线。需要编号就用 40px 大数字裸排(放引导词前,gap 32px)。
**图示化升级**:要点 ≥4 且各项有图标语义 → 升级原型 23 图标网格;有严格先后 → 原型 24 chevron 带。

---

### 原型 9 · 不对称分栏 7:5(满填)

**用途**:主辅双栏——左论述+右证据(数据/引文/图)。**何时别用**:两栏同等重要(用原型 12)。
**填充**:满填。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">主栏观点的 action title</div>
</div>
<!-- 方式 C:7:5 分栏 -->
<div data-layout="columns" data-layout-gap="60" style="position:absolute;left:100px;top:340px;width:1720px;height:560px;">
  <!-- 主栏:裸排版论述(无边框无底色) -->
  <div data-object="true" data-layout-w="7fr">
    <div style="font-size:26px;font-weight:700;line-height:1.35;color:var(--charcoal);">核心论述一段,粗体开场</div>
    <div style="font-size:26px;line-height:1.65;color:var(--text-primary);margin-top:24px;">论证正文 4-6 行,自然往下排。主栏不装盒子,保持编辑感。</div>
  </div>
  <!-- 辅栏:深色面(证据区) -->
  <div data-object="true" data-layout-w="5fr" style="background:var(--deep-navy);border-radius:10px;padding:40px;">
    <div style="font-size:20px;font-weight:600;letter-spacing:2px;color:var(--accent-orange);">关键证据</div>
    <div class="num" style="font-size:72px;font-weight:800;line-height:1.1;color:var(--on-navy-text);margin-top:16px;">87<span style="font-size:36px;">%</span></div>
    <div style="font-size:24px;line-height:1.55;color:var(--on-navy-sub);margin-top:16px;">证据说明 1-2 行</div>
  </div>
</div>
```

**反 AI 味要点**:辅栏深色面是"对比"不是"卡片";主栏留白不装盒。7:5 之外可 3:2、2:1;**主辅必须分明**,等宽即失败。

---

### 原型 10 · 图文页(满填)

**用途**:产品图/截图/照片 + 解读。**何时别用**:没有图——不要用图库凑数(降级为原型 7/8)。
**填充**:满填。图片契约:`<img>` 显式 `object-fit`(html-spec 5.2.1)。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">图为证,标题说图的结论</div>
</div>
<!-- 左图 5 份 -->
<img data-object="true" src="../assets/img/example.png" alt=""
     style="position:absolute;left:100px;top:320px;width:700px;height:580px;object-fit:cover;border-radius:10px;">
<!-- 右文 7 份 -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:860px;top:320px;width:960px;">
  <div style="font-size:26px;font-weight:700;line-height:1.4;color:var(--charcoal);">看图先看这一句</div>
  <div style="font-size:26px;line-height:1.65;color:var(--text-primary);margin-top:20px;">解读 3-5 行。图与文同高,底部对齐页脚区。</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 图:文 | 5:7(图小文大)或 7:5(图为主);图高 580-620px 撑满内容区 |
| object-fit | 照片 `cover`;截图 `contain`+底色 `--card-bg` |
| 镜像 | 图右文左亦可,同 deck 内统一一边 |

**反 AI 味要点**:❌ 不给图加圆角卡片底+阴影+边框三件套;✓ 单圆角或直角。截图务必 `contain`,裁切失真比留白更难看。

---

### 原型 11 · 全出血大图页(出血满填)

**用途**:一张图说一件事(场景/产品/数据可视化大图)。**何时别用**:图质量低/与论点无关。
**填充**:图满画布(出血),文字区 airy。装饰图用 `background-image`(截图路径);内容图用 `<img>`。

```html
<div class="slide-container" style="background:var(--charcoal);">
  <!-- 全画布图(装饰/背景走 background-image;内容照片换 <img object-fit:cover>) -->
  <div data-object="true" data-object-type="shape" style="position:absolute;left:0;top:0;width:1920px;height:1080px;background-image:url('../assets/img/hero.png');background-size:cover;background-position:center;"></div>
  <!-- 左下文字块:深底图上用白字,可垫预算混合深色条 -->
  <div data-object="true" data-object-type="shape" style="position:absolute;left:0;top:820px;width:1920px;height:260px;background:var(--code-bg);"></div>
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:870px;width:1500px;">
    <div style="font-size:40px;font-weight:700;line-height:1.3;color:var(--white);">图说的一句话结论</div>
  </div>
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:950px;width:1500px;">
    <div style="font-size:22px;line-height:1.4;color:var(--brand-dark-tint);">补充说明一行 · 来源</div>
  </div>
</div>
```

**反 AI 味要点**:文字垫条用**预算混合纯色**(非 rgba);❌ 不用渐变蒙版+居中巨标的"AI 英雄区"。图上文字 ≤2 行。

---

## 组 3 · 对比流程

### 原型 12 · 双栏对照(满填)

**用途**:旧 vs 新 / A vs B / 前后对比。**何时别用**:三方以上对比(用表格原型 19)。
**填充**:满填。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">对比结论先行的标题</div>
</div>
<!-- 左栏:旧/痛点 -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:340px;width:800px;">
  <div style="font-size:22px;font-weight:600;letter-spacing:2px;color:var(--text-tertiary);">过去</div>
  <div style="font-size:30px;font-weight:700;line-height:1.3;color:var(--charcoal);margin-top:12px;">旧方式</div>
  <div style="font-size:26px;line-height:1.7;color:var(--text-primary);margin-top:24px;">
    · 痛点一,一行说清<br>· 痛点二<br>· 痛点三
  </div>
</div>
<!-- 中缝细线 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:940px;top:360px;width:1px;height:520px;background:var(--border-medium);"></div>
<!-- 右栏:新/方案(主色强调) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1020px;top:340px;width:800px;">
  <div style="font-size:22px;font-weight:600;letter-spacing:2px;color:var(--lenovo-red);">现在</div>
  <div style="font-size:30px;font-weight:700;line-height:1.3;color:var(--charcoal);margin-top:12px;">新方式</div>
  <div style="font-size:26px;line-height:1.7;color:var(--text-primary);margin-top:24px;">
    · 解法一<br>· 解法二<br>· 解法三
  </div>
</div>
```

**反 AI 味要点**:❌ 双卡片+顶边色条+图标(旧模式 7);✓ 裸双栏+中缝线。"新"侧可用一处主色,全页唯一高亮。
**图示化升级**:双方各有 ≥3 条特征清单 → 升级原型 29 对比卡阵(VS 徽章+图标行)。

---

### 原型 13 · 流程步骤(满填)

**用途**:3-5 步流程/方法论/实施路径。**何时别用**:纯时间顺序(用原型 14)。
**填充**:满填。两款:**大数字裸排款**(首选)与 **chevron 款**(步骤有严格先后箭头语义时)。
**丰富档(2026-08-02 测试反馈)**:步骤卡下方留 1-2 行"例子(个人)/例子(团队)"真实场景,把抽象步骤落地成"我也能抄"的模板——只放步骤名+说明的流程页,是"内容单薄"的高发区。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">三步落地,标题说路径</div>
</div>
<!-- 大数字裸排款:方式 C 三列 -->
<div data-layout="columns" data-layout-gap="60" style="position:absolute;left:100px;top:360px;width:1720px;height:480px;">
  <div data-object="true" data-layout-w="1fr" style="border-top:3px solid var(--charcoal);padding-top:24px;">
    <div class="num" style="font-size:56px;font-weight:800;line-height:1;color:var(--charcoal);">1</div>
    <div style="font-size:28px;font-weight:700;line-height:1.3;color:var(--charcoal);margin-top:16px;">步骤名</div>
    <div style="font-size:24px;line-height:1.6;color:var(--text-secondary);margin-top:12px;">这一步做什么、产出什么,2-3 行。</div>
  </div>
  <!-- 步骤 2、3 同构;当前步/关键步 border-top 换主色 -->
</div>
```

| 参数 | 调什么 |
|---|---|
| 步骤数 | 3 步高 480px / 4-5 步高 400px;说明字号 20px |
| 强调步 | 仅 1 步:border-top 主色 + 数字主色 |
| chevron 款 | `data-shape="chevron"` 横排+文字叠加(见 creative-layouts 模式 2),每 deck ≤1 页 |

**反 AI 味要点**:❌ 序号圆圈+卡片(旧配方 4);✓ 顶线+大数字。步骤间不需要箭头图形——数字本身就是顺序。
**图示化升级**:步骤有强箭头语义或形式偏好为丰富型 → 升级原型 24 chevron 带(chevron 属结构形状,原"每 deck ≤1 页"装饰限额已解除,仅守"同原型不连续 >2 页")。

---

### 原型 14 · 时间线(满填)

**用途**:历程/路线图/里程碑(有真实日期)。**何时别用**:无时间属性的"步骤"(用原型 13)。
**填充**:满填。横向款(4-6 节点)为主;纵向款(>6 节点)用议程式排版。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">路线图的 action title</div>
</div>
<!-- 横轴实线(非虚线) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:560px;width:1720px;height:2px;background:var(--border-medium);"></div>
<!-- 节点 1:圆点+上方日期+下方事件 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:140px;top:548px;width:24px;height:24px;border-radius:50%;background:var(--lenovo-red);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:460px;width:200px;">
  <div class="num" style="font-size:28px;font-weight:800;color:var(--charcoal);">Q1</div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:600px;width:260px;">
  <div style="font-size:24px;line-height:1.5;color:var(--text-primary);">里程碑事件,两行内</div>
</div>
<!-- 节点 2-4 同构,x 均匀分布(间隔 1720/N);已完成节点主色,未来节点边框白心 -->
```

**反 AI 味要点**:❌ 旋转标签/渐变圆/虚线(旧模式 4 的炫技三件套);✓ 实线+圆点+正立文字。当前位置用主色,是唯一点缀。
**图示化升级**:里程碑需带详情 → 节点说明改小卡片变体;闭环流程 → 原型 27 循环图。

---

### 原型 15 · 2×2 象限(满填)

**用途**:双维度定位(优先级/风险评估/竞争地图)。**何时别用**:维度不成立(为显得专业硬凑 XY 轴是最大的外行特征)。
**填充**:满填。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">标题说象限结论(如:先打右上)</div>
</div>
<!-- 象限区:方式 C 2x2 grid -->
<div data-layout="grid" data-layout-cols="2" data-layout-gap="2" style="position:absolute;left:260px;top:340px;width:1300px;height:560px;">
  <div data-object="true" data-layout-h="280" style="background:var(--card-bg);padding:32px;">
    <div style="font-size:24px;font-weight:700;color:var(--charcoal);">象限名(高X低Y)</div>
    <div style="font-size:24px;line-height:1.55;color:var(--text-secondary);margin-top:10px;">点位/说明</div>
  </div>
  <!-- 其余三象限;目标象限底换 --deep-navy、文字换 on-navy 组 -->
</div>
<!-- 轴标签 -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:260px;top:920px;width:1300px;text-align:center;">
  <div style="font-size:22px;color:var(--text-tertiary);">X 轴名 →</div>
</div>
```

**反 AI 味要点**:象限底色用 `--card-bg`/白,目标象限唯一深色;❌ 四色渐变象限。轴标签 18px 灰色,别画箭头森林。

---

### 原型 16 · 层级(满填)

**用途**:金字塔/分层模型(战略→战术→执行;需求层次)。**何时别用**:层级关系不成立(并列项别堆成塔)。
**填充**:满填。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">层级模型的 action title</div>
</div>
<!-- 3 层横条,上窄下宽:方式 B -->
<div style="position:absolute;left:100px;top:340px;width:1720px;display:flex;flex-direction:column;gap:16px;align-items:center;">
  <div data-object="true" data-object-type="shape" style="width:700px;height:180px;background:var(--deep-navy);border-radius:8px;display:flex;align-items:center;justify-content:center;">
    <div style="text-align:center;">
      <div style="font-size:28px;font-weight:700;color:var(--on-navy-text);">顶层:一句话</div>
      <div style="font-size:24px;color:var(--on-navy-sub);margin-top:8px;line-height:1.4;">支撑说明</div>
    </div>
  </div>
  <div data-object="true" data-object-type="shape" style="width:1100px;height:180px;background:var(--deep-navy-light);border-radius:8px;display:flex;align-items:center;justify-content:center;">…中层…</div>
  <div data-object="true" data-object-type="shape" style="width:1500px;height:180px;background:var(--off-white);border:1px solid var(--border-medium);border-radius:8px;display:flex;align-items:center;justify-content:center;">…底层…</div>
</div>
```

**反 AI 味要点**:层宽递进(700/1100/1500)就是金字塔,❌ 不需要画三角 SVG。层数 3-4;色彩由深到浅单向,❌ 彩虹分层。

---

## 组 4 · 数据

### 原型 17 · 大数字带(满填)

**用途**:3-4 个关键数字(业绩/效果/规模)。**何时别用**:数字 >4(拆页或改仪表盘)、数字无说服力。
**填充**:满填。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">标题说数字的结论(如:效率提升四成)</div>
</div>
<!-- 方式 C 3-4 列,细线分隔无卡片 -->
<div data-layout="columns" data-layout-gap="40" style="position:absolute;left:100px;top:380px;width:1720px;height:420px;">
  <div data-object="true" data-layout-w="1fr" style="border-left:1px solid var(--border-light);padding-left:40px;">
    <div class="num" style="font-size:88px;font-weight:800;line-height:1;color:var(--charcoal);">87<span style="font-size:40px;">%</span></div>
    <div style="font-size:26px;line-height:1.4;color:var(--text-secondary);margin-top:20px;">指标说明,一两行</div>
    <div style="font-size:22px;line-height:1.4;color:var(--signal-green);margin-top:12px;">↑ 同比 +12pp</div>
  </div>
  <!-- 列 2-4 同构;首列去 border-left -->
</div>
```

| 参数 | 调什么 |
|---|---|
| 数字字号 | 3 列 88px / 4 列 72px;单位 40-45% 主数字 |
| 增减行 | 18px;增 `--signal-green` 减 `--signal-red`,全页仅此处用信号色 |
| 强调列 | 至多 1 列数字用主色,其余 `--charcoal` |

**反 AI 味要点**:❌ KPI 卡片+渐变底+上标(旧模式 3);✓ 细线分隔裸排。大数字 = 自信,盒子 = 心虚。
**图示化升级**:指标有图标语义(成本/用户/时效)→ 数字上方加同色系小图标;KPI >4 且需图表 → 原型 20(阅读/混合档)。
**填充提示(2026-08-05 试点反馈)**:3 列数字+两行说明只占内容区上半截时,数字上调 96-104px(scale-to-fill),并在底部加一条浅底"怎么读/口径"补充条(顶 780-800,高 90,22px 单行)——别让数字带悬空。

---

### 原型 18 · 图表主角(满填)

**用途**:一页一图,图是论据主角。**何时别用**:图说不清楚(先改图,不是加字)。
**填充**:满填。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">标题=图表的结论(不是"销售趋势图")</div>
</div>
<!-- 大图表 1080px:原生 data-chart -->
<div data-object="true" data-chart='{"type":"bar","labels":["Q1","Q2","Q3","Q4"],"series":[{"name":"营收","values":[120,180,240,310]}]}'
     style="position:absolute;left:100px;top:320px;width:1080px;height:580px;"></div>
<!-- 右侧解读栏 560px -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1260px;top:320px;width:560px;">
  <div style="font-size:24px;font-weight:700;line-height:1.4;color:var(--charcoal);">怎么读这张图</div>
  <div style="font-size:24px;line-height:1.65;color:var(--text-primary);margin-top:20px;">
    · 解读一:拐点在哪<br><br>· 解读二:说明什么<br><br>· 解读三:下一步
  </div>
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);margin-top:32px;">来源:数据口径与时间</div>
</div>
```

**反 AI 味要点**:图无卡片底、无边框;解读栏裸排。图表系列数受密度档上限(演讲 ≤3)。

---

### 原型 19 · 表格主角(满填)

**用途**:结构化数据必须全列出(对比矩阵/清单/参数表)。**何时别用**:行数超档(拆页/附录)。
**填充**:满填。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">标题说表格结论</div>
</div>
<div data-object="true" data-object-type="table" style="position:absolute;left:100px;top:320px;width:1720px;">
  <table style="width:100%;border-collapse:collapse;font-size:22px;">
    <tr style="background:var(--deep-navy);color:var(--white);">
      <th style="padding:20px 24px;text-align:left;font-weight:700;">列一</th>
      <th style="padding:20px 24px;text-align:left;font-weight:700;">列二</th>
      <th style="padding:20px 24px;text-align:right;font-weight:700;">数字列</th>
    </tr>
    <tr style="border-bottom:1px solid var(--border-light);">
      <td style="padding:18px 24px;line-height:1.4;">行内容</td>
      <td style="padding:18px 24px;line-height:1.4;">行内容</td>
      <td class="num" style="padding:18px 24px;text-align:right;line-height:1.4;">1,024</td>
    </tr>
    <!-- 行数 ≤ 档内上限(演讲 ≤6 含表头);偶数行可 zebra --card-bg -->
  </table>
</div>
```

**反 AI 味要点**:表头深色、行线细分、数字右对齐;❌ 全框线网格+居中所有列。字号 22px(演讲)/18px(阅读)。

---

### 原型 20 · 仪表盘(满填 · 阅读/混合档向)

**用途**:KPI 全景(复盘/月报)。**何时别用**:演讲档(信息过载;拆成原型 17+18 两页)。
**填充**:满填。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:100px;width:1720px;">
  <div style="font-size:52px;font-weight:700;line-height:1.2;color:var(--charcoal);">月度复盘的 action title</div>
</div>
<!-- KPI 行:3 大数字(原型 17 压缩款,无卡) -->
<div data-layout="columns" data-layout-gap="40" style="position:absolute;left:100px;top:260px;width:1720px;height:200px;">
  <div data-object="true" data-layout-w="1fr" style="border-left:1px solid var(--border-light);padding-left:32px;">
    <div class="num" style="font-size:64px;font-weight:800;line-height:1;color:var(--charcoal);">87<span style="font-size:32px;">%</span></div>
    <div style="font-size:24px;color:var(--text-secondary);margin-top:12px;">指标</div>
  </div>
</div>
<!-- 下区:图表 + 表格 双拼 -->
<div data-object="true" data-chart='{"type":"line","labels":["1月","2月","3月"],"series":[{"name":"趋势","values":[10,14,19]}]}'
     style="position:absolute;left:100px;top:520px;width:840px;height:380px;"></div>
<div data-object="true" data-object-type="table" style="position:absolute;left:980px;top:520px;width:840px;">
  <table style="width:100%;border-collapse:collapse;font-size:18px;">…4 行内…</table>
</div>
```

**反 AI 味要点**:三区分明(KPI/图/表),区间 40px 留白分隔;❌ 渐变 KPI 卡堆叠。仅混合/阅读档使用。

---

## 组 5 · 收尾

### 原型 21 · 行动号召(airy)

**用途**:最后一页:明确的下一步。**何时别用**:没有行动(用原型 5 大字观点收尾)。
**填充**:airy。

```html
<div class="slide-container" style="background:var(--deep-navy);">
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:200px;top:400px;width:1520px;">
    <div style="font-size:64px;font-weight:800;line-height:1.25;color:var(--on-navy-text);text-align:center;">
      希望您做的一件事
    </div>
  </div>
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:200px;top:600px;width:1520px;">
    <div style="font-size:24px;line-height:1.5;color:var(--on-navy-sub);text-align:center;">
      联系方式 / 链接 / 时间承诺
    </div>
  </div>
</div>
```

**反 AI 味要点**:❌ 徽章按钮/渐变 CTA 条;✓ 一句话+一行联系。"谢谢聆听"是废话,行动句才是收尾。

---

### 原型 22 · 附录指引(满填)

**用途**:附录封面或资料清单(数据来源/参考/详细参数入口)。**何时别用**:无附录。
**填充**:满填(它是内容页)。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">附录:数据与资料</div>
</div>
<div style="position:absolute;left:100px;top:320px;width:1720px;display:flex;flex-direction:column;">
  <div data-object="true" data-object-type="shape" style="height:120px;border-bottom:1px solid var(--border-light);display:flex;align-items:center;">
    <div style="font-size:26px;line-height:1.5;color:var(--text-primary);">
      <span style="font-weight:700;color:var(--charcoal);">数据来源:</span>口径、时间范围、样本说明
    </div>
  </div>
  <!-- 参考资料/术语表/详细参数入口 同构 -->
</div>
```

**反 AI 味要点**:与议程页同构(首尾呼应);条目含真实出处,❌ 不写"详见相关资料"。

---

## 组 6 · 图示(2026-08-05 新增;结构形状,非装饰——反模式豁免见 design-principles 第四章总则)

> 本组 8 款是"形式丰富"的主力。共性纪律:**先有信息结构,后选图示**(并列→23/29,先后→24,递减→25,分层→26,循环→27,辐射→28,分节→30);图标从 `assets/icons.md` 复制(**stroke 必须显式 hex,禁 currentColor**——截图时 currentColor 会变透明);全页图标同一色系。

### 原型 23 · 图标要点网格(满填)—— 并列信息的首选图示

**用途**:3、4 或 6 个并列要点(特性/能力/原则/优势)——"万物皆卡片"的合法出口(反模式 2/7 结构豁免:不计入卡片矩阵限额)。**何时别用**:要点有先后/层级(用 24/26);纯结论清单无图标语义(原型 8 更省);5 个要点(网格不齐,改 9 或 8)。
**填充**:满填 —— 2×2:卡高 290(320+290+40+290=940 铺满);2×3:列数改 3;1×3:单行三列纵向卡(卡高 460)。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">四个能力,标题把结论说完</div>
</div>
<!-- 2×2 网格:方式 C grid -->
<div data-layout="grid" data-layout-cols="2" data-layout-gap="40" style="position:absolute;left:100px;top:320px;width:1720px;">
  <div data-object="true" data-layout-h="290" style="background:var(--white);border:1px solid var(--border-light);border-radius:12px;padding:40px;">
    <div style="display:flex;align-items:center;gap:20px;">
      <!-- 图标:assets/icons.md 复制,stroke 显式 hex,全页同色 -->
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" style="stroke:var(--brand-primary)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2" style="fill:var(--brand-primary)" stroke="none"/></svg>
      <div style="font-size:30px;font-weight:700;line-height:1.3;color:var(--charcoal);">要点标题</div>
    </div>
    <div style="font-size:26px;line-height:1.6;color:var(--text-primary);margin-top:20px;">说明 2 行以内:这个要点是什么、为什么重要。</div>
    <div style="font-size:22px;line-height:1.5;color:var(--text-tertiary);margin-top:14px;">例子/证据一行(丰富档必备,可选)</div>
  </div>
  <!-- 卡 2-4 同构,换图标/标题/说明 -->
</div>
```

| 参数 | 调什么 |
|---|---|
| 布局 | 4 点 → 2×2(cols 2,h 290);6 点 → 2×3(cols 3,h 290,卡内 padding 32);3 点 → 1×3(cols 3,h 460,纵向卡:图标在上,标题 margin-top:18px,说明 21px) |
| 图标 | 48px;全页同一 hex(主色或炭灰);深底卡上换亮色系 |
| 标题行 | 横向(图标左+标题右)为主;窄卡(2×3/1×3)改纵向(图标在上) |
| 说明 | 22px ≤2 行;例子行 18px 灰色 |

**反 AI 味要点**:❌ 每卡一色的彩虹图标(全页同色);❌ 阴影+边框+圆角三件套(只取"细边框+圆角"或"浅底+圆角"其一);❌ 无语义凑数图标。✓ 这是结构卡片:卡上有图标+信息,合法且不计装饰件。

---

### 原型 24 · chevron 流程带(满填)

**用途**:3-5 步严格先后的流程(实施路径/方法论/转化步骤),箭头语义强。**何时别用**:并列要点(23);时间属性强(14);闭环(27)。
**填充**:满填。chevron 属结构形状——旧"每 deck ≤1 页"装饰限额**已解除**(2026-08-05),仅守"同原型不连续 >2 页"。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">四步落地,标题说路径</div>
</div>
<!-- chevron 带(4 步,w424 gap8;首步 homePlate 平头;带高 120,顶 380) -->
<div data-object="true" data-object-type="shape" data-shape="homePlate" style="position:absolute;left:100px;top:380px;width:424px;height:120px;background:var(--deep-navy);"></div>
<div data-object="true" data-object-type="shape" data-shape="chevron" style="position:absolute;left:532px;top:380px;width:424px;height:120px;background:var(--deep-navy-light);"></div>
<div data-object="true" data-object-type="shape" data-shape="chevron" style="position:absolute;left:964px;top:380px;width:424px;height:120px;background:var(--deep-navy-light);"></div>
<div data-object="true" data-object-type="shape" data-shape="chevron" style="position:absolute;left:1396px;top:380px;width:424px;height:120px;background:var(--lenovo-red);"></div>
<!-- 叠字(DOM 在形状后;左右各让 48px 避开箭头缺口;line-height=带高做单行居中) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:148px;top:380px;width:328px;height:120px;text-align:center;">
  <div style="font-size:26px;font-weight:700;color:var(--white);line-height:120px;">1 诊断</div>
</div>
<!-- 步骤 2-4 叠字同构(x 同 chevron,左右各让 48px) -->
<!-- 说明列:与 chevron 同 x 同宽,顶 540 -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:540px;width:424px;">
  <div style="font-size:26px;line-height:1.6;color:var(--text-primary);">这一步做什么、产出什么,2-3 行说透。</div>
  <div style="font-size:22px;line-height:1.5;color:var(--text-tertiary);margin-top:12px;">例子:真实场景一句话(≤20 字)。</div>
</div>
<!-- 说明列 2-4 同构 -->
<!-- 口径条(贯穿补充:口径/周期/负责,浅底单行) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:780px;width:1720px;height:90px;background:var(--card-bg);border:1px solid var(--border-light);border-radius:10px;"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:140px;top:780px;width:1640px;height:90px;">
  <div style="font-size:22px;line-height:90px;color:var(--text-secondary);">口径:收益以季度复盘为准 · 周期:每步 6 周 · 负责:数字化转型办</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 3 步 | w 568 gap 8,x = 100/676/1252 |
| 4 步 | w 424 gap 8,x = 100/532/964/1396(带高 120,顶 380) |
| 5 步 | w 336 gap 10,x = 100/446/792/1138/1484;带高可降 96,说明列/口径条不动 |
| 配色 | 同色系递进(深→浅);**仅关键步用主色**(上图第 4 步);禁每步一色彩虹 |
| 口径条 | 顶 780,高 90(底 870);单行 22px,放口径/周期/负责等贯穿信息 |

**反 AI 味要点**:✓ 首步 `homePlate`(平头)、后续 `chevron`(咬合感);❌ 每步叠图标+徽章的堆砌;说明列与 chevron 严格同 x 同宽(对齐即专业)。

---

### 原型 25 · 转化漏斗(满填)

**用途**:逐级递减模型(转化/筛选/审核漏斗)。**何时别用**:无递减语义的层级(用 26/16);仅 2 级(用 12 双栏)。
**填充**:满填。结构:`trapezoid` + `transform:rotate(180deg)`(窄边朝下)+ 居中层叠 + 左右侧注。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">漏斗标题:从 X 到 Y 的转化</div>
</div>
<!-- 漏斗层(4 层,w 1200/950/700/450,h120 gap16,顶 360;rotate(180) 窄边朝下) -->
<div data-object="true" data-object-type="shape" data-shape="trapezoid" style="position:absolute;left:360px;top:360px;width:1200px;height:120px;background:var(--deep-navy);transform:rotate(180deg);"></div>
<div data-object="true" data-object-type="shape" data-shape="trapezoid" style="position:absolute;left:485px;top:496px;width:950px;height:120px;background:var(--deep-navy-light);transform:rotate(180deg);"></div>
<div data-object="true" data-object-type="shape" data-shape="trapezoid" style="position:absolute;left:610px;top:632px;width:700px;height:120px;background:var(--brand-dark-mid);transform:rotate(180deg);"></div>
<div data-object="true" data-object-type="shape" data-shape="trapezoid" style="position:absolute;left:735px;top:768px;width:450px;height:120px;background:var(--lenovo-red);transform:rotate(180deg);"></div>
<!-- 层内叠字(单行居中,line-height=层高) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:360px;top:360px;width:1200px;height:120px;text-align:center;">
  <div style="font-size:24px;font-weight:700;color:var(--white);line-height:120px;">线索(全部触达)</div>
</div>
<!-- 层 2-4 叠字同构 -->
<!-- 左侧阶段标签(右对齐) + 右侧数值(主色) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:404px;width:220px;text-align:right;">
  <div style="font-size:22px;font-weight:600;color:var(--text-secondary);line-height:44px;">阶段一</div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1600px;top:404px;width:220px;">
  <div class="num" style="font-size:28px;font-weight:800;color:var(--lenovo-red);line-height:44px;">10,000</div>
</div>
<!-- 层 2-4 侧注同构,y 各 +136(404/540/676/812) -->
```

| 参数 | 调什么 |
|---|---|
| 3 层 | w 1200/850/500,h 140,y = 360/516/672(底 812,下方可补一行结论) |
| 4 层 | 如骨架:1200/950/700/450,h 120,y 360/496/632/768(底 888) |
| 配色 | 同色系由深到浅单向;末层可用主色(转化终点) |
| 侧注 | 左=阶段名(右对齐灰),右=数值/转化率(主色 num) |

**反 AI 味要点**:✓ 递减语义才画漏斗;❌ 层间加渐变/阴影;`transform-origin` 保持默认居中(契约要求),叠字不随转。

---

### 原型 26 · 金字塔(满填)

**用途**:分层模型(战略→战术→执行/需求层次/能力栈),图示感强于原型 16(横条收窄)。**何时别用**:并列关系(23);递减语义(25)。
**填充**:满填。顶层 `triangle` + 下层 `trapezoid`(预设顶边约为底边一半,天然成塔)。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">三层模型,标题说结构</div>
</div>
<!-- 3 层(h180 gap16,顶 340;顶层三角 w500,中梯 w1000,底梯 w1500) -->
<div data-object="true" data-object-type="shape" data-shape="triangle" style="position:absolute;left:710px;top:340px;width:500px;height:180px;background:var(--deep-navy);"></div>
<div data-object="true" data-object-type="shape" data-shape="trapezoid" style="position:absolute;left:460px;top:536px;width:1000px;height:180px;background:var(--deep-navy-light);"></div>
<div data-object="true" data-object-type="shape" data-shape="trapezoid" style="position:absolute;left:210px;top:732px;width:1500px;height:180px;background:var(--brand-dark-pale);border:1px solid var(--border-medium);"></div>
<!-- 层内叠字(上层白字,底层深字;两行:层名 26 粗 + 一句 18) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:710px;top:360px;width:500px;text-align:center;">
  <div style="font-size:26px;font-weight:700;color:var(--white);line-height:1.3;">战略层</div>
  <div style="font-size:22px;color:var(--brand-dark-tint);margin-top:8px;line-height:1.4;">一句话说明</div>
</div>
<!-- 中/底层叠字同构(y 556/752;底层文字换 --charcoal 系) -->
```

| 参数 | 调什么 |
|---|---|
| 3 层 | 如骨架(底 912);层宽 500/1000/1500 |
| 4 层 | w 400/800/1200/1600,h 140,y = 330/486/642/798(底 938) |
| 配色 | 深→浅单向;底层用**浅主色预算混合色**(var(--brand-dark-pale) 类)+细边框+深字——❌ 勿用与页面同底色(off-white 页面配 off-white 底层会隐形,2026-08-05 样张实测踩过) |
| 叠字 | 顶层三角内文字偏下(top 留出尖角);层名 ≤6 字 |

**反 AI 味要点**:✓ 层间 16px 缝比无缝拼接更干净(预设梯形顶边比例固定,微差不强求);❌ 彩虹分层、❌ 每层加图标。

---

### 原型 27 · 循环图(满填)

**用途**:闭环流程(PDCA/增长飞轮/运营闭环)。**何时别用**:单向流程(24);仅 3 节点(chevron 更直给)。
**填充**:满填。结构:**内联 SVG 圆环+箭头(整体截图)** + 中心圆(原生)+ 4 张卫星卡(原生,盖住环的四正点)。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">飞轮标题:转起来的是什么</div>
</div>
<!-- 环形箭头(内联 SVG;圆心=画布 960,630;四正点被卫星卡盖住) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:700px;top:420px;width:520px;height:420px;">
  <svg width="520" height="420" viewBox="0 0 520 420" fill="none" style="stroke:var(--ink-soft)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="260" cy="210" r="150"/><polyline points="371 301 366 316 381 311"/><polyline points="169 321 154 316 159 331"/><polyline points="149 119 154 104 139 109"/><polyline points="351 99 366 104 361 89"/></svg>
</div>
<!-- 中心命题圆 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:850px;top:520px;width:220px;height:220px;border-radius:50%;background:var(--deep-navy);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:850px;top:520px;width:220px;height:220px;text-align:center;">
  <div style="font-size:26px;font-weight:700;color:var(--white);line-height:220px;">核心命题</div>
</div>
<!-- 4 卫星卡(N 790,330 / E 1160,560 / S 790,790 / W 420,560;340×140) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:790px;top:330px;width:340px;height:140px;background:var(--white);border:1px solid var(--border-light);border-radius:12px;padding:24px 28px;">
  <div style="font-size:24px;font-weight:700;color:var(--charcoal);line-height:1.3;">① 环节名</div>
  <div style="font-size:24px;line-height:1.5;color:var(--text-secondary);margin-top:8px;">一句说明,一行半内。</div>
</div>
<!-- E/S/W 卡同构 -->
```

| 参数 | 调什么 |
|---|---|
| 节点数 | 固定 4(N/E/S/W);3 或 ≥5 换原型 |
| 环色 | 单色(炭灰或主色);箭头同色;禁分段彩虹 |
| 中心圆 | 220px 深底白字;命题 ≤8 字 |
| 卫星卡 | 340×140;图标可选(加则 4 张全加) |

**反 AI 味要点**:✓ 环交给 SVG(截图)最干净,节点/文字全原生;❌ 别用 4 个预设箭头形状拼环(对不齐反而业余);卡片盖环点是刻意穿线效果,DOM 序必须环先卡后。

---

### 原型 28 · 中心辐射(满填)

**用途**:一个核心 + 4 个辐射维度(平台+场景/中台+前台/总目标+分领域)。**何时别用**:维度间有流向(27/24);≥5 个辐射点(23 网格)。
**填充**:满填。结构:中心圆 + 正交细连接线(横平竖直,免旋转计算)+ 4 卫星卡。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">一个核心,四个支撑</div>
</div>
<!-- 连接线(先画,在卡下):N 竖线/S 竖线/W 横线/E 横线 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:958px;top:500px;width:4px;height:20px;background:var(--border-medium);"></div>
<div data-object="true" data-object-type="shape" style="position:absolute;left:958px;top:740px;width:4px;height:20px;background:var(--border-medium);"></div>
<div data-object="true" data-object-type="shape" style="position:absolute;left:560px;top:628px;width:290px;height:4px;background:var(--border-medium);"></div>
<div data-object="true" data-object-type="shape" style="position:absolute;left:1070px;top:628px;width:290px;height:4px;background:var(--border-medium);"></div>
<!-- 中心圆 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:850px;top:520px;width:220px;height:220px;border-radius:50%;background:var(--deep-navy);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:850px;top:520px;width:220px;height:220px;text-align:center;">
  <div style="font-size:28px;font-weight:700;color:var(--white);line-height:220px;">核心</div>
</div>
<!-- 4 卫星卡(N 770,330 / S 770,760 / W 180,545 / E 1340,545;380×170) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:770px;top:330px;width:380px;height:170px;background:var(--white);border:1px solid var(--border-light);border-radius:12px;padding:26px 30px;">
  <div style="font-size:26px;font-weight:700;color:var(--charcoal);line-height:1.3;">维度名</div>
  <div style="font-size:26px;line-height:1.5;color:var(--text-secondary);margin-top:10px;">说明两行内,讲清与核心的关系。</div>
</div>
<!-- S/W/E 卡同构(S 770,760;W/E 180/1340,545);其中一张可换浅主色底强调(至多一张) -->
```

| 参数 | 调什么 |
|---|---|
| 卫星数 | 4(N/E/S/W);3 个则撤一条线(别留断线) |
| 连接线 | 4px 灰细线,**无箭头**(辐射非流向) |
| 中心圆 | 220px;词 ≤6 字;可换主色 |
| 强调 | 至多 1 张卫星卡用浅主色底 |

**反 AI 味要点**:✓ 正交连接线(横平竖直)永远不会错;❌ 斜线连接(旋转对不齐即业余)、❌ 卫星卡加阴影堆质感。

---

### 原型 29 · 对比卡阵(满填)

**用途**:A/B 方案对决、新旧对照的图示版(裸排版见原型 12)。**何时别用**:三方以上(19 表格);无对立语义(23)。
**填充**:满填。结构:双卡(800×560)+ 中央 VS 徽章(语义标记,反模式 6 豁免)+ 卡内图标特征行。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">对比结论先行的标题</div>
</div>
<!-- 左卡:旧/保守(白底细边框) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:340px;width:800px;height:560px;background:var(--white);border:1px solid var(--border-light);border-radius:12px;padding:44px;">
  <div style="font-size:22px;font-weight:600;letter-spacing:2px;color:var(--text-tertiary);">过去 / 方案 A</div>
  <div style="font-size:34px;font-weight:700;color:var(--charcoal);margin-top:10px;line-height:1.25;">旧方式名</div>
  <div style="display:flex;align-items:center;gap:14px;margin-top:34px;">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="stroke:var(--text-tertiary)" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><line x1="9" y1="9" x2="15" y2="15"/><line x1="15" y1="9" x2="9" y2="15"/></svg>
    <div style="font-size:26px;line-height:1.5;color:var(--text-primary);">痛点特征一</div>
  </div>
  <!-- 特征行 2-4 同构,margin-top:22px;左右卡行数对齐 -->
</div>
<!-- 右卡:新/推荐(深底) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:1020px;top:340px;width:800px;height:560px;background:var(--deep-navy);border-radius:12px;padding:44px;">
  <div style="font-size:22px;font-weight:600;letter-spacing:2px;color:var(--accent-orange);">现在 / 方案 B</div>
  <div style="font-size:34px;font-weight:700;color:var(--white);margin-top:10px;line-height:1.25;">新方式名</div>
  <div style="display:flex;align-items:center;gap:14px;margin-top:34px;">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="stroke:var(--signal-green)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="8 12.5 11 15.5 16.5 9"/></svg>
    <div style="font-size:26px;line-height:1.5;color:var(--brand-dark-pale);">解法特征一</div>
  </div>
  <!-- 特征行 2-4 同构 -->
</div>
<!-- 中央 VS 徽章(DOM 在双卡之后,压缝) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:905px;top:565px;width:110px;height:110px;border-radius:50%;background:var(--lenovo-red);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:905px;top:565px;width:110px;height:110px;text-align:center;">
  <div style="font-size:36px;font-weight:800;color:var(--white);line-height:110px;">VS</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 双卡 | 800×560 at (100,340)/(1020,340),底 900 |
| 特征行 | 3-4 行/卡,左右行数必须相等(视觉天平) |
| 图标 | 左侧灰 x / 右侧绿勾(语义对立);或两侧同用中性圆点 |
| VS 徽章 | 110px 主色圆,白 36px;压缝位置 x905 居中 |

**反 AI 味要点**:✓ 一侧浅一侧深 = 视觉立场;❌ 双卡同深同浅分不出立场、❌ 每行换图标色。徽章是语义件非装饰件。

---

### 原型 30 · 色带分节页(满填)

**用途**:3-4 个分节论述(每带 = 主张+一句支撑+右侧证据位),替代纯文字条目的"重"版本;章节内导航亦可。**何时别用**:并列特性有图标语义(23 更轻);严格流程(24)。
**填充**:满填。结构:横向纯色带 stack(结构色带,合法——渐变装饰条仍禁,反模式 4 不变)。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">三个主张,逐层推进</div>
</div>
<!-- 色带 stack(3 带,h180 gap20,y=330/530/730,底 910) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:330px;width:1720px;height:180px;background:var(--deep-navy);border-radius:10px;display:flex;align-items:center;padding:0 48px;">
  <svg width="44" height="44" viewBox="0 0 24 24" fill="none" style="stroke:var(--accent-orange)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2" style="fill:var(--accent-orange)" stroke="none"/></svg>
  <div style="margin-left:32px;flex:1;">
    <div style="font-size:28px;font-weight:700;color:var(--white);line-height:1.3;">主张一,一句话说完</div>
    <div style="font-size:22px;line-height:1.5;color:var(--brand-dark-tint);margin-top:8px;">支撑一句:数据或例子。</div>
  </div>
  <div class="num" style="font-size:56px;font-weight:800;color:var(--accent-orange);line-height:1;">01</div>
</div>
<!-- 带 2(--deep-navy-light)/ 带 3(浅底 --card-bg + 深字 + 编号换主色)同构 -->
```

| 参数 | 调什么 |
|---|---|
| 带数/高度 | 3 带 h180(y 330/530/730);4 带 h140 gap 16(y 330/486/642/798) |
| 配色 | 深→浅单向递进(深深/深浅/浅底深字);编号列统一主色 |
| 带内 | 图标 44px(浅带换主色);主张 28px;支撑 22px;右侧编号 56px num |
| 变体 | 左侧深栏导航:480px 深栏(x100,章节目录)+ 右侧 2-3 色带(x620,w1200) |

**反 AI 味要点**:✓ 纯色带是结构分带;❌ 渐变带(装饰指纹)、❌ 每带一色;带内文字 ≤2 行,编号/图标二选一在右侧或左侧,别双侧堆满。

---

## 组 7 · 分析论证(咨询)

> **本组共同纪律**(每页都适用,不在各小节重复):
> 1. **必须有一行来源/口径注**(≥16px,右下或标题下),内容 = 时间范围 + 样本/范围 + 测算方式;
>    估算值标"估算"并给假设。见 `design-principles.md`"数据页的口径纪律"。
> 2. **一页一个论断**:action title 写这页的**结论**(不是"XX 分析"),图形只是它的证据。
> 3. **反脆弱**:结构成立才用(维度不成立别硬凑坐标轴,变动不闭合别画瀑布)——
>    为显得专业硬套分析框架,是最容易被专业读者一眼看穿的外行特征。
> 4. 配色守单色系深浅递进 + 唯一强调色;❌ 彩虹分类、❌ 渐变填充。

### 原型 31 · 执行摘要(满填)

**用途**:第 2 页给决策者的一页全貌(咨询/董事会/尽调必备);读者只看这一页也能拍板。**何时别用**:纯教学/发布 deck(用原型 3 议程);内容不足 3 个支柱(用原型 5 大字观点)。
**填充**:满填 —— 顶部统领结论深色面板(承载"所以呢"),下方 3 支柱等宽裸排,底部来源行贴页脚区。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">建议启动 A 方案,18 个月内可收回投入</div>
</div>
<!-- 统领结论面板(深底,结构色面;高 200,承载核心论断+关键数字) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:300px;width:1720px;height:200px;background:var(--brand-dark);border-radius:8px;"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:150px;top:336px;width:1120px;">
  <div style="font-size:28px;font-weight:700;line-height:1.45;color:var(--on-navy-text);">
    核心判断:瓶颈在数据管道而非模型能力;先修管道可释放现有投入的 60% 闲置产能。
  </div>
</div>
<!-- 面板右侧关键数字(与判断呼应) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1340px;top:340px;width:430px;">
  <div class="num" style="font-size:64px;font-weight:800;color:var(--white);line-height:1;">18<span style="font-size:26px;font-weight:600;">个月</span></div>
  <div style="font-size:20px;line-height:1.4;color:var(--on-navy-sub);margin-top:10px;">投资回收期(基准情景)</div>
</div>
<!-- 3 支柱:方式 C grid,裸排+顶部主色细条(不是卡片) -->
<div data-layout="grid" data-layout-cols="3" data-layout-gap="40" style="position:absolute;left:100px;top:560px;width:1720px;">
  <div data-object="true" data-layout-h="320" style="border-top:3px solid var(--brand-primary);padding-top:28px;">
    <div style="font-size:20px;font-weight:700;letter-spacing:2px;color:var(--brand-primary);">01 现状</div>
    <div style="font-size:30px;font-weight:700;line-height:1.3;color:var(--charcoal);margin-top:16px;">三条产线数据口径不一致</div>
    <div style="font-size:24px;line-height:1.55;color:var(--text-secondary);margin-top:18px;">对账人工耗时占运营工时 22%,月末结账平均延迟 4.5 天。</div>
  </div>
  <!-- 支柱 2(02 主张)/ 支柱 3(03 收益)同构;仅支柱 1 或结论列用主色细条,其余用 --border-medium -->
</div>
<!-- 来源行(本组硬要求) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:990px;width:1720px;">
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);">来源:2025-07 至 2026-06 三产线 ERP 流水(n=41,砍月);回收期为基准情景测算,假设产能利用率维持 78%</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 面板高 | 200(判断 2 行);判断 3 行取 240,支柱区 top 改 600、h 280 |
| 支柱数 | 3(默认);4 个改 `data-layout-cols="4"`、gap 32、标题降 26px |
| 关键数字 | 面板右侧仅放 **1 个**总括数字;多数字改用原型 17 另起一页 |
| 支柱细条 | 仅"结论/主张"那一列用 `--brand-primary`,其余 `--border-medium`(高亮 ≤1 处) |

**反 AI 味要点**:✓ 支柱**裸排 + 顶部细条**(反模式 2:要点默认裸排,不是等宽卡片矩阵);✓ 深色面板承载信息 = 合法结构色面,不是"页底结论条"(它在页**顶**且有内容);❌ 三张等宽阴影卡、❌ 每支柱一个颜色、❌ 标题写"执行摘要"(空标题——标题位要写结论,"执行摘要"四个字放 kicker 或直接省掉)。

**图示化升级**:支柱之间有因果/递进关系时改用原型 24 chevron 流程带;支柱是并列能力项时改原型 23 图标要点网格。

---

### 原型 32 · 议题树 MECE(满填)

**用途**:把一个大问题**分解**为可独立求解的子问题(尽调/诊断/战略议题拆解)。**何时别用**:只是分层不是分解(用 26 金字塔/16 层级);分支超过 3×3(拆两页,或只展开本页要论证的那一支)。
**填充**:满填 —— 左侧根问题,右侧两级分支;1px 连接线走 shape 细条(正交,不斜线)。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">利润缺口可拆成三支,其中两支我们能自主解决</div>
</div>
<!-- 根问题(深底,左侧垂直居中) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:520px;width:340px;height:160px;background:var(--brand-dark);border-radius:8px;"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:130px;top:556px;width:280px;">
  <div style="font-size:26px;font-weight:700;line-height:1.35;color:var(--on-navy-text);">利润缺口<br>为何达 12%?</div>
</div>
<!-- 主干横线(根 → 分支列;y 居中 600) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:440px;top:599px;width:80px;height:2px;background:var(--border-medium);"></div>
<!-- 竖向汇总线(贯穿三分支中心 y 400→800) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:520px;top:400px;width:2px;height:400px;background:var(--border-medium);"></div>
<!-- 分支 1(y 340-460,中心 400):横线 + 分支盒 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:522px;top:399px;width:78px;height:2px;background:var(--border-medium);"></div>
<div data-object="true" data-object-type="shape" style="position:absolute;left:600px;top:340px;width:480px;height:120px;background:var(--card-bg);border-left:3px solid var(--brand-primary);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:628px;top:364px;width:430px;">
  <div style="font-size:26px;font-weight:700;line-height:1.3;color:var(--charcoal);">收入侧:客单价下滑</div>
  <div style="font-size:20px;line-height:1.4;color:var(--text-secondary);margin-top:8px;">贡献缺口 5.1pp · 可自主</div>
</div>
<!-- 叶子(该分支的 2 个子项;x1140,w 680) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:1080px;top:399px;width:60px;height:2px;background:var(--border-light);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1160px;top:344px;width:660px;">
  <div style="font-size:22px;line-height:1.5;color:var(--text-primary);">— 折扣审批层级过松(占 3.2pp)</div>
  <div style="font-size:22px;line-height:1.5;color:var(--text-primary);margin-top:10px;">— 高毛利 SKU 断货(占 1.9pp)</div>
</div>
<!-- 分支 2(中心 600)/ 分支 3(中心 800)同构,y 各 +200;不可自主的支用 --border-medium 左条 -->
<!-- MECE 校验注 + 来源行 -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:900px;width:1720px;">
  <div style="font-size:18px;line-height:1.5;color:var(--text-tertiary);">三支互斥、合计 12.0pp 完全穷尽(5.1 + 4.3 + 2.6);"可自主"= 无需集团审批即可动的杠杆</div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:990px;width:1720px;">
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);">来源:2026 财年管理报表 + 分产品毛利归因(口径:剔除一次性重组费用)</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 分支数 | 3(默认,中心 y 400/600/800,竖线 h400);4 支改 h120 gap 30、中心 y 370/520/670/820 |
| 层级 | 2 级(分支+叶子)是上限;3 级必然挤——第 3 级改下一页展开 |
| 连接线 | 全部**正交** 2px `--border-medium`,叶子线降 1-2px `--border-light`;❌ 斜线(契约不支持 skew) |
| 强调 | 仅"本页要论证的那一支"用 `--brand-primary` 左条,其余灰(高亮 ≤1 处) |

**反 AI 味要点**:✓ **MECE 校验注是这个原型的灵魂** —— 写明"互斥 + 合计穷尽"并给分项和,否则它只是一张树形装饰图;✓ 分支盒用左侧色条 + `--card-bg`,不是四面阴影卡;❌ 斜线连接、❌ 圆角气泡框、❌ 每支一色。宁可只画两级也别把三级塞进一页。

**降级**:分支无量化归因(拿不出各支占比)时,别用本原型——改原型 8 要点列表诚实列问题,或先补数据。

---

### 原型 33 · 评估矩阵(Harvey ball,满填)

**用途**:多方案 × 多准则的取舍评估(选型/供应商比选/优先级裁决);Harvey ball 让读者一眼扫出赢家。**何时别用**:准则 ≤2(用 12 双栏对照);方案 ≤2(用 29 对比卡阵)。
**填充**:满填 —— `<table>` 原生表格 + 每格 `data-shape="pie"`/`ellipse` 圆饼,推荐行整行底纹。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">按四项准则,方案 B 是唯一无短板的选择</div>
</div>
<!-- 表格:方案为行、准则为列;数值列右对齐,评分列居中 -->
<table data-object="true" style="position:absolute;left:100px;top:330px;width:1720px;border-collapse:collapse;">
  <tr style="background:var(--brand-dark);">
    <th style="width:380px;padding:22px 24px;text-align:left;font-size:22px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">方案</th>
    <th style="width:250px;padding:22px 24px;text-align:center;font-size:22px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">实施难度</th>
    <th style="width:250px;padding:22px 24px;text-align:center;font-size:22px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">见效速度</th>
    <th style="width:250px;padding:22px 24px;text-align:center;font-size:22px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">投入</th>
    <th style="width:250px;padding:22px 24px;text-align:center;font-size:22px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">可逆性</th>
    <th style="padding:22px 24px;text-align:left;font-size:22px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">结论</th>
  </tr>
  <tr>
    <td style="padding:26px 24px;font-size:24px;font-weight:700;color:var(--charcoal);border:1px solid var(--border-light);">A 全量替换</td>
    <td style="border:1px solid var(--border-light);"></td><!-- 圆饼由下方 shape 叠放,格内留空 -->
    <td style="border:1px solid var(--border-light);"></td>
    <td style="border:1px solid var(--border-light);"></td>
    <td style="border:1px solid var(--border-light);"></td>
    <td style="padding:26px 24px;font-size:22px;line-height:1.4;color:var(--text-secondary);border:1px solid var(--border-light);">风险集中,不建议</td>
  </tr>
  <!-- 推荐行:整行浅底纹(tr 级 background 是支持特性) -->
  <tr style="background:var(--card-bg);">
    <td style="padding:26px 24px;font-size:24px;font-weight:700;color:var(--brand-primary);border:1px solid var(--border-light);">B 分产线试点</td>
    <td style="border:1px solid var(--border-light);"></td><td style="border:1px solid var(--border-light);"></td>
    <td style="border:1px solid var(--border-light);"></td><td style="border:1px solid var(--border-light);"></td>
    <td style="padding:26px 24px;font-size:22px;line-height:1.4;color:var(--charcoal);border:1px solid var(--border-light);">推荐:无短板</td>
  </tr>
  <!-- 方案 C 同构 -->
</table>
<!-- Harvey ball:满=ellipse 实心;3/4、1/2、1/4 = data-shape="pie" 旋转;空=ellipse 描边 -->
<!-- 每格圆心 = 该列中心 x、该行中心 y;36px 直径 -->
<div data-object="true" data-object-type="shape" data-shape="ellipse" style="position:absolute;left:487px;top:420px;width:36px;height:36px;background:var(--brand-dark);"></div>
<div data-object="true" data-object-type="shape" data-shape="pie" style="position:absolute;left:737px;top:420px;width:36px;height:36px;background:var(--brand-dark);"></div>
<div data-object="true" data-object-type="shape" data-shape="ellipse" style="position:absolute;left:987px;top:420px;width:36px;height:36px;background:transparent;border:2px solid var(--border-medium);"></div>
<!-- 图例 -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:900px;width:1720px;">
  <div style="font-size:18px;line-height:1.5;color:var(--text-tertiary);">● 强 ◕ 较强 ◑ 中等 ◔ 较弱 ○ 弱(四项准则等权;评分由三人独立打分取中位数)</div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:990px;width:1720px;">
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);">来源:2026-07 供应商问卷 + 两轮技术验证;"投入"含首年许可与实施人力(不含内部机会成本)</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 规模 | 3 方案 × 4 准则(默认,行高 ~96px);演讲档表格 ≤6 行含表头,超了拆页 |
| 圆饼 | 36px;满/空用 `ellipse`(实心/描边),半档用 `data-shape="pie"`(1/4、1/2、3/4 靠 `rotate` 调) |
| 定位 | 圆心 x = 列中心、y = 行中心;表格行高变了**必须重算 top**(圆饼是独立叠放对象,不随表格流) |
| 推荐行 | `<tr style="background:var(--card-bg)">` 整行浅底纹 + 方案名换主色;深底纹会压掉圆饼对比度 |

**反 AI 味要点**:✓ 图例必须写**等权与打分方式**(不写就是伪精确);✓ 圆饼单色深浅,❌ 红黄绿交通灯(彩虹分类,且色盲不友好);❌ 每格写"★★★☆☆"(字符星是 AI 味,原生形状才是专业做法);结论列写人话("风险集中,不建议"),不写"综合评分 3.2"。

**降级**:准则权重不等或需要加权总分时,加一列"加权得分"(数字右对齐)并在图例写权重;权重讲不清就别加——伪精确比不精确更糟。

---

### 原型 34 · 瀑布桥图(满填)

**用途**:变动分解 —— 从 A 到 B 之间**发生了什么**(利润桥/成本拆解/增长归因)。咨询最高频的单页。**何时别用**:变动不闭合(起始 + 各增减 ≠ 结束,画出来就是错图);只有总量没有分项(用 17 大数字带)。
**填充**:满填 —— 起止柱落地、中间增减柱**浮空**(靠 `top` 计算),虚线连接相邻柱顶。

> **为什么手工搭而不用 data-chart**:OOXML 没有原生 waterfall 图表类型,pptxgenjs 也没有。
> 用形状拼装反而更好 —— 每根柱在 PPT 里都是可直接拖动的原生形状,客户能自己改数。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">毛利下滑 9.8pp,七成来自折扣失控</div>
</div>
<!-- 绘图区:基线 y=820(0 刻度),柱宽 180,柱距 60;标尺 1pp ↔ 4.2px -->
<!-- 起始柱(落地,深底):58.0pp → h 244,top = 820-244 = 576 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:150px;top:576px;width:180px;height:244px;background:var(--brand-dark);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:150px;top:534px;width:180px;text-align:center;">
  <div class="num" style="font-size:30px;font-weight:800;color:var(--charcoal);line-height:36px;">58.0</div>
</div>
<!-- 连接虚线(前柱右缘 → 本柱左缘,走柱顶 y) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:330px;top:575px;width:60px;height:0;border-top:2px dashed var(--border-medium);"></div>
<!-- 减项柱 1(浮空,主色):-8.4pp → h 35,top 576(顶接前柱顶),底 611 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:390px;top:576px;width:180px;height:35px;background:var(--brand-primary);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:390px;top:534px;width:180px;text-align:center;">
  <div class="num" style="font-size:30px;font-weight:800;color:var(--brand-primary);line-height:36px;">-8.4</div>
</div>
<!-- 减项柱 2(-2.6pp → h 11,top = 611)-->
<div data-object="true" data-object-type="shape" style="position:absolute;left:630px;top:611px;width:180px;height:11px;background:var(--brand-primary);"></div>
<!-- 增项柱(+1.2pp → h 5,向上收:top = 622-5 = 617) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:870px;top:617px;width:180px;height:5px;background:var(--brand-dark-soft);"></div>
<!-- 结束柱(落地,深底):48.2pp → h 202,top = 820-202 = 618 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:1110px;top:618px;width:180px;height:202px;background:var(--brand-dark);"></div>
<!-- 基线(0 刻度) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:820px;width:1720px;height:2px;background:var(--border-medium);"></div>
<!-- X 轴标签(每柱下方两行,与柱同 x) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:150px;top:838px;width:180px;text-align:center;">
  <div style="font-size:20px;font-weight:600;line-height:1.35;color:var(--text-secondary);">2025<br>基准毛利率</div>
</div>
<!-- 右侧结论注(占满剩余宽度,避免右侧空洞) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1380px;top:576px;width:440px;">
  <div style="font-size:24px;line-height:1.55;color:var(--text-secondary);">折扣与断货合计贡献 11.0pp 降幅,是本轮改善的唯一优先项;汇率带来的 +1.2pp 不可持续。</div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:990px;width:1720px;">
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);">来源:2025-2026 财年管理报表毛利归因(口径:剔除一次性重组费用;pp = 百分点)</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 标尺 | 先定 `1 单位 ↔ N px`,全柱共用一把尺;**柱高 = 值 × 尺**,不许目测 |
| 柱位 | 浮空柱 `top` = 前柱累计位置;减项向下延续、增项向上收。搭完必须对着"起始 + 各增减 = 结束"验一遍 |
| 柱数 | 起止 + 3-4 个变动项(5-6 根);更多则合并小项为"其他"或拆页 |
| 配色 | 起止 `--brand-dark`,减项 `--brand-primary`,增项 `--brand-dark-soft`;❌ 红绿对立 |
| 最小可见 | 算出 h<4px 时给 4px 下限,真值写在标签里(否则那根柱看不见) |

**反 AI 味要点**:✓ 连接虚线让"桥"成立(没有它就是一堆散柱);✓ 数值标在柱顶外侧、增减带符号;❌ 柱内渐变、❌ 圆角柱、❌ 3D 立体柱;右侧必须有结论注,否则整页右半是空洞(填充率不合格)。

**降级**:分项凑不齐、无法闭合时**别画瀑布** —— 改原型 18 图表主角放一根趋势线 + 文字说明主因,诚实得多。

---

### 原型 35 · 泳道甘特(满填)

**用途**:实施路径 —— 谁在何时做什么(项目计划/上市节奏/迁移路线)。比原型 14 多一个"责任方"维度。**何时别用**:只有事件没有责任方(用 14 时间线);阶段 ≤3 且无并行(用 24 chevron)。
**填充**:满填 —— 左侧泳道名列,右侧等宽时间网格 + 任务条;里程碑用 `diamond`。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">试点在 Q3 收口,Q4 才具备全量复制条件</div>
</div>
<!-- 时间刻度头(4 季度;网格起点 x=420,每格 350) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:420px;top:300px;width:350px;text-align:center;">
  <div style="font-size:22px;font-weight:700;line-height:40px;color:var(--text-secondary);">Q1</div>
</div>
<!-- Q2/Q3/Q4 同构,x 各 +350(770/1120/1470) -->
<!-- 竖向网格线(季度分界,y 350→870) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:770px;top:350px;width:1px;height:520px;background:var(--border-light);"></div>
<!-- 1120 / 1470 同构 -->
<!-- 泳道 1:交替底纹带(道高 120,y 360) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:360px;width:1720px;height:120px;background:var(--card-bg);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:130px;top:396px;width:270px;">
  <div style="font-size:24px;font-weight:700;line-height:1.3;color:var(--charcoal);">数据平台组</div>
  <div style="font-size:18px;line-height:1.3;color:var(--text-tertiary);margin-top:4px;">负责人:李</div>
</div>
<!-- 任务条:x = 420 + 起始格×350 + 10,w = 跨度×350 - 20(留缝) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:430px;top:398px;width:680px;height:44px;background:var(--brand-dark);border-radius:4px;"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:450px;top:398px;width:640px;height:44px;">
  <div style="font-size:20px;font-weight:600;color:var(--on-navy-text);line-height:44px;">管道重构与口径统一</div>
</div>
<!-- 泳道 2(y 490,白底)/ 3(y 620,card-bg)/ 4(y 750,白底)同构 -->
<!-- 里程碑:diamond 骑在网格线上(28px,竖向居中于该道) -->
<div data-object="true" data-object-type="shape" data-shape="diamond" style="position:absolute;left:1106px;top:406px;width:28px;height:28px;background:var(--brand-primary);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1146px;top:406px;width:300px;height:28px;">
  <div style="font-size:18px;font-weight:600;line-height:28px;color:var(--brand-primary);">M1 口径冻结</div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:990px;width:1720px;">
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);">来源:2026-08 项目章程 v2;时间为自然季度,投入按已确认编制(未含招聘到位假设)</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 泳道数 | 4 道 × 120px(y 360-840);5 道改 h 100;≥6 道拆页(密度档信息块上限) |
| 时间格 | 4 格 × 350px(季度);6 格改 233px、刻度字降 20px。格必须等宽 |
| 任务条 | h 44,条内单行 `line-height:44px`(契约的居中徽章写法);跨度 <1 格时文字移到条外 |
| 底纹 | 泳道交替 `--card-bg` / 白;❌ 每道一色 |
| 里程碑 | `diamond` 28px 压网格线;标签在右侧,不盖条;里程碑 ≤3 个 |

**反 AI 味要点**:✓ 条位与时间**真实对应**(手排甘特最易出"看起来在 Q2 其实压着 Q1");✓ 任务条同色系深浅,靠**位置**表达信息不靠颜色;❌ 彩虹泳道、❌ 渐变条、❌ 逐条阴影。

**降级**:并行不重要、只讲先后 → 原型 24 chevron;只有 3-4 个时点 → 原型 14 时间线。

---

### 原型 36 · 散点定位图(满填)

**用途**:双维度**真实点位**(竞争地图/客户分群/机会评估);比原型 15 的格子精确 —— 读者能看出"离参考线多远"。**何时别用**:只有 3-4 个点或只有定性排序(用 15 象限);维度不成立(硬凑 XY 轴是最大的外行特征)。
**填充**:满填 —— 原生 `data-chart:scatter` 作图 + 右侧解读栏。

> **原生可编辑(已实测)**:`scatter` 走 pptxgenjs 原生 `<c:scatterChart>`,不是截图,客户可在 PPT 里改数。
> **`series[0]` 是 X 轴值**,其后每个 series 为一个 Y 系列,values 长度必须相等。
> 气泡图(第三维 = 大小)**当前渲染器不支持**;需要第三维时把它写进点标注文字。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">六个区域里,只有华东同时具备规模与增速</div>
</div>
<!-- 原生散点图:series[0]=X 轴值,series[1]=Y 值 -->
<div data-object="true" data-chart='{
  "type":"scatter",
  "labels":["X"],
  "series":[
    {"name":"X-Axis","values":[12.4,8.1,22.6,15.2,6.7,18.9]},
    {"name":"区域市场","values":[9.2,14.5,21.3,7.1,4.8,12.0]}
  ],
  "options":{
    "showLegend":false,"lineSize":0,"chartColors":["0A2C63"],
    "catAxisTitle":"市场规模(亿元)","valAxisTitle":"三年复合增速(%)",
    "showCatAxisTitle":true,"showValAxisTitle":true
  }
}' style="position:absolute;left:100px;top:320px;width:1180px;height:580px;"></div>
<!-- 右侧解读栏(结构色面;点名"谁在哪、所以怎样") -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:1340px;top:320px;width:480px;height:580px;background:var(--card-bg);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1380px;top:356px;width:400px;">
  <div style="font-size:20px;font-weight:700;letter-spacing:2px;color:var(--brand-primary);">读图</div>
  <div style="font-size:24px;line-height:1.55;color:var(--charcoal);margin-top:18px;">
    <span style="font-weight:700;">华东(22.6 / 21.3)</span>是唯一落在双高区的市场,规模与增速均列第一。
  </div>
  <div style="font-size:24px;line-height:1.55;color:var(--text-secondary);margin-top:20px;">
    华南规模接近但增速仅 7.1%,属守成型;西北双低,本轮不投。
  </div>
  <div style="font-size:20px;line-height:1.5;color:var(--text-tertiary);margin-top:24px;">参考线 = 六区域加权均值(规模 14.0 / 增速 11.5)</div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:990px;width:1720px;">
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);">来源:2026 行业年鉴 + 内部销售数据(n=6 区域);增速为 2023-2026 CAGR,规模为 2026 预测值(估算,假设渠道结构不变)</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 数据 | `series[0].name` 写 `X-Axis`(X 值),`series[1]` 起为 Y 系列;各 values 长度必须相等 |
| 轴标题 | `catAxisTitle`/`valAxisTitle` + 两个 `show*AxisTitle:true`,**必须带单位** |
| 点样式 | `lineSize:0`(否则散点被连成折线);`chartColors` 单色 |
| 分幅 | 图 1180 + 解读栏 480;❌ 做成 1720 满宽(没有解读栏就没有"所以呢") |
| 分群 | 需分组着色时每群一个 Y 系列并开 `showLegend` |

**反 AI 味要点**:✓ 参考线必须说明它是什么(均值/基准),否则只是装饰;✓ 只标关键 2-3 个点,别给每点加标签框糊成一团;❌ 四象限四种底色;轴不带单位则整图不可读。

**降级**:点数 ≤4 或只有定性判断 → 原型 15 的 2×2 象限格子对少量定性点位更清晰。

---

### 原型 37 · 驱动因素树(满填)

**用途**:把一个指标**按算式**拆到可操作的杠杆(收入 = 客数 × 客单价 × 复购;成本 = 单价 × 用量)。**何时别用**:关系不是算式而是逻辑归类(用 32 议题树);只有两层且无运算(用 17 大数字带)。
**填充**:满填 —— 左侧根指标,右侧因子列 + 运算符徽章;每个因子带当前值与可动空间。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">收入缺口的可动杠杆只有复购率一项</div>
</div>
<!-- 根指标(深底,左侧;算式的等号左边) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:480px;width:360px;height:200px;background:var(--brand-dark);border-radius:8px;"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:130px;top:512px;width:300px;">
  <div style="font-size:24px;font-weight:600;line-height:1.3;color:var(--on-navy-sub);">年收入</div>
  <div class="num" style="font-size:52px;font-weight:800;line-height:1.1;color:var(--white);margin-top:8px;">8.4<span style="font-size:24px;font-weight:600;">亿</span></div>
  <div style="font-size:20px;line-height:1.35;color:var(--on-navy-sub);margin-top:8px;">目标 9.6 亿 · 缺口 1.2 亿</div>
</div>
<!-- 等号徽章(单行居中写法:line-height=高) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:480px;top:560px;width:60px;height:40px;text-align:center;">
  <div style="font-size:36px;font-weight:700;color:var(--text-tertiary);line-height:40px;">=</div>
</div>
<!-- 因子 1(x 560,w 360):浅底 + 左侧色条;三层信息 = 名/值/可动空间 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:560px;top:480px;width:360px;height:200px;background:var(--card-bg);border-left:3px solid var(--border-medium);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:590px;top:512px;width:300px;">
  <div style="font-size:24px;font-weight:600;line-height:1.3;color:var(--text-secondary);">活跃客数</div>
  <div class="num" style="font-size:44px;font-weight:800;line-height:1.1;color:var(--charcoal);margin-top:8px;">12.4<span style="font-size:22px;font-weight:600;">万</span></div>
  <div style="font-size:20px;line-height:1.35;color:var(--text-tertiary);margin-top:8px;">已近渠道上限 · 难动</div>
</div>
<!-- 乘号徽章(x 940) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:940px;top:560px;width:60px;height:40px;text-align:center;">
  <div style="font-size:36px;font-weight:700;color:var(--text-tertiary);line-height:40px;">×</div>
</div>
<!-- 因子 2(x 1020)同构:客单价 · 受合同约束 -->
<!-- 乘号徽章(x 1400) -->
<!-- 因子 3(x 1460,唯一可动项 → 主色左条 + 主色数值,高亮 ≤1 处) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:1460px;top:480px;width:360px;height:200px;background:var(--card-bg);border-left:3px solid var(--brand-primary);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1490px;top:512px;width:300px;">
  <div style="font-size:24px;font-weight:600;line-height:1.3;color:var(--text-secondary);">复购率</div>
  <div class="num" style="font-size:44px;font-weight:800;line-height:1.1;color:var(--brand-primary);margin-top:8px;">31<span style="font-size:22px;font-weight:600;">%</span></div>
  <div style="font-size:20px;line-height:1.35;color:var(--charcoal);margin-top:8px;">同业中位 42% · 可动 11pp</div>
</div>
<!-- 敏感度结论条(承载信息的色带,合法结构色面) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:740px;width:1720px;height:120px;background:var(--brand-dark-soft);border-radius:8px;"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:140px;top:772px;width:1640px;">
  <div style="font-size:26px;font-weight:600;line-height:1.4;color:var(--white);">敏感度:复购率每提升 1pp → 年收入 +0.11 亿。追平同业中位可补足缺口的 92%。</div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:990px;width:1720px;">
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);">来源:2026 财年经营数据;同业中位取六家可比公司披露值(口径:12 个月内二次购买占比)</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 因子数 | 3(默认,w 360 + 徽章 60);2 个改 w 560;4 个改 w 260、字号降一档 |
| 每格三层 | **名 / 当前值 / 可动空间** —— 第三层是这个原型的价值所在,没有它就只是一个算式 |
| 运算符 | `=` `×` `+` `-`,36px 灰;用单行居中写法(`line-height` = 盒高) |
| 高亮 | **只有"可动"的那一个因子**用主色(左条 + 数值);其余灰 |
| 结论条 | 底部敏感度条必填(每变动 1 单位 → 结果变多少),它把树变成决策依据 |

**反 AI 味要点**:✓ 敏感度是灵魂 —— 没有"每 1pp 值多少"就不是驱动树而是装饰算式;✓ 底部色带承载信息,不属反模式 3 的"页底结论条"(那条判负的是**空的**装饰条);❌ 每因子一色、❌ 因子盒四面阴影、❌ 把不能动的因子也标成高亮。

**降级**:拆不出乘法关系(只是并列影响因素)时改原型 32 议题树或 23 图标网格,别用等式伪装严谨。

---

### 原型 38 · 热力评估矩阵(满填)

**用途**:对象 × 维度的**逐格强弱**扫视(能力评估/风险登记/市场吸引力打分);格子多、每格信息少时优于 33 评估矩阵。**何时别用**:格数 ≤6(用 33 Harvey ball,更精确);每格需要文字说明(用 19 表格主角)。
**填充**:满填 —— `<table>` 逐格三档底纹 + 图例;行列表头深色。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">五项能力里,数据治理是全线短板</div>
</div>
<table data-object="true" style="position:absolute;left:100px;top:330px;width:1720px;border-collapse:collapse;">
  <tr style="background:var(--brand-dark);">
    <th style="width:340px;padding:20px 24px;text-align:left;font-size:22px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">业务单元</th>
    <th style="padding:20px 16px;text-align:center;font-size:20px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">数据治理</th>
    <th style="padding:20px 16px;text-align:center;font-size:20px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">流程自动化</th>
    <th style="padding:20px 16px;text-align:center;font-size:20px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">人才储备</th>
    <th style="padding:20px 16px;text-align:center;font-size:20px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">工具就绪</th>
    <th style="padding:20px 16px;text-align:center;font-size:20px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">合规</th>
  </tr>
  <tr>
    <td style="padding:24px;font-size:24px;font-weight:700;color:var(--charcoal);border:1px solid var(--border-light);">华东制造</td>
    <!-- 弱=深主色底+白字;中=主色浅调底+深字;强=浅灰底+灰字(单色系三档,不用红黄绿) -->
    <!-- 中档没有现成令牌:用主色 18% 混白的显式 hex(theme.css 只到 --brand-primary/-dark) -->
    <td style="padding:24px 16px;text-align:center;font-size:22px;font-weight:700;color:var(--white);background:var(--brand-primary);border:1px solid var(--border-light);">弱</td>
    <td style="padding:24px 16px;text-align:center;font-size:22px;font-weight:600;color:var(--charcoal);background:var(--brand-primary-soft);border:1px solid var(--border-light);">中</td>
    <td style="padding:24px 16px;text-align:center;font-size:22px;font-weight:600;color:var(--text-secondary);background:var(--card-bg);border:1px solid var(--border-light);">强</td>
    <td style="padding:24px 16px;text-align:center;font-size:22px;font-weight:600;color:var(--charcoal);background:var(--brand-primary-soft);border:1px solid var(--border-light);">中</td>
    <td style="padding:24px 16px;text-align:center;font-size:22px;font-weight:600;color:var(--text-secondary);background:var(--card-bg);border:1px solid var(--border-light);">强</td>
  </tr>
  <!-- 其余 3-4 行同构 -->
</table>
<!-- 图例(三档色块 + 打分口径) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:890px;width:36px;height:24px;background:var(--brand-primary);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:148px;top:890px;width:200px;height:24px;">
  <div style="font-size:18px;color:var(--text-secondary);line-height:24px;">弱(1-2 分)</div>
</div>
<!-- 中 / 强 图例同构,x 各 +250 -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:930px;width:1720px;">
  <div style="font-size:18px;line-height:1.5;color:var(--text-tertiary);">五级打分由各单元自评 + 咨询团队复核校准,分歧项取复核值</div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:990px;width:1720px;">
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);">来源:2026-07 能力成熟度访谈(5 单元 × 5 维度,n=23 人);"合规"维度含数据出境专项</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 规模 | 4-5 行 × 5 列(演讲档表格 ≤6 行含表头);超了拆页,别缩字号 |
| 三档色 | 弱 `--brand-primary`(白字)/ 中 `var(--brand-primary-soft)`(主色 18% 混白,深字)/ 强 `--card-bg`(灰字)—— **单色系深浅**,不是红黄绿。换预设时按该预设主色重算中档 hex |
| 格内 | 只写"弱/中/强"或分数,**不写句子**(要写句子用原型 19) |
| 图例 | 三档色块 + 分数区间 + 打分方式,三者缺一即为伪精确 |
| 强调 | 靠"弱格连成一列"自然形成视觉信号,不额外加边框高亮 |

**反 AI 味要点**:✓ 单色系三档 —— 红黄绿交通灯是 AI 味且色盲不友好(约 8% 男性无法区分红绿);✓ action title 写**扫出来的结论**("数据治理是全线短板"),不写"能力评估矩阵";❌ 每格加图标、❌ 渐变底纹、❌ 五档以上色阶(超过三档人眼无法可靠比较)。

**降级**:格数 ≤6 时改原型 33 Harvey ball(圆饼比色块更精确);每格都需要解释时改原型 19 表格主角。

---

### 原型 39 · 情景分析(满填)

**用途**:把不确定性摊开 —— 悲观/基准/乐观三案并置 + 各案的关键假设与触发条件。**何时别用**:只有单一预测(用 18 图表主角);三案差异只在一个数字(写进 17 大数字带的脚注即可)。
**填充**:满填 —— 三等宽栏(基准列唯一深色),底部横贯"关键假设"行。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">即使在悲观情景下,项目仍能在 30 个月内回本</div>
</div>
<!-- 三情景栏:方式 C grid,基准列深底(唯一强调) -->
<div data-layout="grid" data-layout-cols="3" data-layout-gap="32" style="position:absolute;left:100px;top:320px;width:1720px;">
  <div data-object="true" data-layout-h="400" style="background:var(--card-bg);padding:36px;">
    <div style="font-size:20px;font-weight:700;letter-spacing:2px;color:var(--text-tertiary);">悲观</div>
    <div class="num" style="font-size:64px;font-weight:800;line-height:1.05;color:var(--charcoal);margin-top:16px;">30<span style="font-size:24px;font-weight:600;">个月</span></div>
    <div style="font-size:22px;line-height:1.4;color:var(--text-secondary);margin-top:10px;">回收期 · IRR 9.2%</div>
    <div style="font-size:24px;line-height:1.55;color:var(--text-primary);margin-top:24px;">渠道恢复慢于预期,复购率仅回到 34%;需追加一轮渠道投入。</div>
  </div>
  <!-- 基准列(深底,唯一强调):background:var(--brand-dark),文字换 on-navy 组 -->
  <div data-object="true" data-layout-h="400" style="background:var(--brand-dark);padding:36px;">
    <div style="font-size:20px;font-weight:700;letter-spacing:2px;color:var(--on-navy-sub);">基准(采用)</div>
    <div class="num" style="font-size:64px;font-weight:800;line-height:1.05;color:var(--white);margin-top:16px;">18<span style="font-size:24px;font-weight:600;">个月</span></div>
    <div style="font-size:22px;line-height:1.4;color:var(--on-navy-sub);margin-top:10px;">回收期 · IRR 21.4%</div>
    <div style="font-size:24px;line-height:1.55;color:var(--on-navy-text);margin-top:24px;">复购率追平同业中位 42%,渠道结构不变;这是本次决策的采用口径。</div>
  </div>
  <!-- 乐观列同构(--card-bg) -->
</div>
<!-- 关键假设行(横贯;情景分析的必要组件) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:760px;width:1720px;height:1px;background:var(--border-medium);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:790px;width:1720px;">
  <div style="font-size:20px;font-weight:700;letter-spacing:2px;color:var(--brand-primary);">三案共同假设与切换触发条件</div>
  <div style="font-size:24px;line-height:1.6;color:var(--text-secondary);margin-top:16px;">
    <span style="font-weight:700;color:var(--charcoal);">共同假设:</span>产能利用率维持 78%、不含并购、汇率按 2026-06 中间价。
    <span style="font-weight:700;color:var(--charcoal);">切换触发:</span>连续两季复购率低于 36% 即切悲观预案。
  </div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:990px;width:1720px;">
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);">来源:三情景财务模型 v3(2026-08);IRR 按 8 年现金流测算(估算,贴现率 9%)</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 栏数 | 3(悲观/基准/乐观);2 案改 `cols="2"`、w 加宽、数字升 72px |
| 强调 | **只有"采用"的那一案深底**(通常是基准);其余浅底(高亮 ≤1 处) |
| 每栏 | 档名 / 关键数字 / 副指标 / 一段驱动说明 —— 四层固定,别加第五层 |
| 假设行 | **共同假设 + 切换触发条件**必填 —— 没有触发条件的情景分析是三个孤立猜测 |

**反 AI 味要点**:✓ 标注哪一案是"采用口径"(读者第一个问题就是这个);✓ 切换触发条件写成可观测指标("连续两季 <36%"),不写"视市场情况";❌ 三案三色(红/黄/绿情景是典型 AI 味)、❌ 三栏等权重呈现(必须有主案)。

**降级**:三案只差一个数字时别单独占页 —— 把区间写进原型 17 的脚注("18 个月;悲观 30/乐观 13")。

---

### 原型 40 · 规模拆解(TAM/SAM/SOM,满填)

**用途**:市场规模从总体逐层收窄到可获取(融资路演/市场进入/新品立项)。**何时别用**:无法给出收窄口径(拍脑袋的三个数比不写更糟);只讲总量(用 17 大数字带)。
**填充**:满填 —— 左侧嵌套梯形(逐层收窄),右侧算式链(每层怎么算出来的)。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">三年内可实际获取 6.8 亿,占可服务市场的 12%</div>
</div>
<!-- 嵌套层(trapezoid 逐层收窄;宽 1000/760/520,h 150,gap 20,居中对齐 x 递增) -->
<div data-object="true" data-object-type="shape" data-shape="trapezoid" style="position:absolute;left:100px;top:340px;width:1000px;height:150px;background:var(--brand-dark);transform:rotate(180deg);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:140px;top:376px;width:920px;">
  <div style="font-size:22px;font-weight:700;letter-spacing:2px;color:var(--on-navy-sub);">TAM 总体可寻址市场</div>
  <div class="num" style="font-size:44px;font-weight:800;line-height:1.15;color:var(--white);margin-top:6px;">142<span style="font-size:22px;font-weight:600;">亿</span></div>
</div>
<div data-object="true" data-object-type="shape" data-shape="trapezoid" style="position:absolute;left:220px;top:510px;width:760px;height:150px;background:var(--brand-dark-soft);transform:rotate(180deg);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:260px;top:546px;width:680px;">
  <div style="font-size:22px;font-weight:700;letter-spacing:2px;color:var(--on-navy-sub);">SAM 可服务市场</div>
  <div class="num" style="font-size:44px;font-weight:800;line-height:1.15;color:var(--white);margin-top:6px;">57<span style="font-size:22px;font-weight:600;">亿</span></div>
</div>
<div data-object="true" data-object-type="shape" data-shape="trapezoid" style="position:absolute;left:340px;top:680px;width:520px;height:150px;background:var(--brand-primary);transform:rotate(180deg);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:380px;top:716px;width:440px;">
  <div style="font-size:22px;font-weight:700;letter-spacing:2px;color:var(--brand-primary-pale);">SOM 可获取市场(3 年)</div>
  <div class="num" style="font-size:44px;font-weight:800;line-height:1.15;color:var(--white);margin-top:6px;">6.8<span style="font-size:22px;font-weight:600;">亿</span></div>
</div>
<!-- 右侧算式链(每层的收窄口径;这是本原型的可信度来源) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1180px;top:340px;width:640px;">
  <div style="font-size:20px;font-weight:700;letter-spacing:2px;color:var(--brand-primary);">收窄口径</div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1180px;top:392px;width:640px;">
  <div style="font-size:24px;line-height:1.55;color:var(--text-primary);">
    <span style="font-weight:700;">142 亿</span> = 全国规上制造企业 3.1 万家 × 年均 IT 支出 45.8 万
  </div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1180px;top:562px;width:640px;">
  <div style="font-size:24px;line-height:1.55;color:var(--text-primary);">
    <span style="font-weight:700;">57 亿</span> = 142 亿 × 40%(已上云且数据量达门槛的比例)
  </div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:1180px;top:732px;width:640px;">
  <div style="font-size:24px;line-height:1.55;color:var(--text-primary);">
    <span style="font-weight:700;">6.8 亿</span> = 57 亿 × 12%(三年目标份额,参照同类产品第 3 年渗透)
  </div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:990px;width:1720px;">
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);">来源:统计局 2025 规上企业名录 + 行业 IT 支出调研(n=180);SOM 份额为估算,参照三家同类产品第 3 年披露渗透率(9-15%)</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 层宽 | 1000/760/520,h 150,gap 20(y 340/510/680,底 830);四层改 h 120 gap 16 |
| 收窄 | `trapezoid` + `rotate(180deg)`(窄边朝下),与原型 25 漏斗同款写法 |
| 算式链 | 每层一行,**必须写清乘了什么系数、系数来自哪** —— 没有算式链的 TAM 页等于三个拍脑袋的数 |
| 配色 | 深 → 浅 → 主色(终点 SOM 用主色);❌ 三层三个色系 |

**反 AI 味要点**:✓ 算式链是可信度的全部来源,标"估算"的项必须给参照;✓ 系数写成可质疑的形式("×40%,已上云且数据量达门槛");❌ 三个同心圆(经典 AI 味且面积比例失真)、❌ 只给三个数不给推导。

**降级**:拿不出收窄口径时**别用本原型** —— 用原型 8 要点列表诚实写"市场规模待验证 + 待补数据清单"(见 `content-deepening.md` 裸主题路径)。

---

### 原型 41 · 成熟度阶梯(满填)

**用途**:能力/流程的分级模型 + **当前位标记**(数字化成熟度/合规等级/团队能力)。**何时别用**:级别之间不是递进而是并列(用 23 图标网格);无法定位当前级(不标当前位的阶梯是空模型)。
**填充**:满填 —— 递升台阶(高度逐级抬升,底对齐),当前级唯一深色 + "我们在这"标记。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">我们在第 2 级,跨到第 3 级是本年度唯一目标</div>
</div>
<!-- 5 级台阶:等宽 324,gap 20(x 步进 344);高度递升 200/260/320/380/440,底对齐 y=860 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:660px;width:324px;height:200px;background:var(--card-bg);border-top:3px solid var(--border-medium);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:130px;top:686px;width:264px;">
  <div class="num" style="font-size:40px;font-weight:800;line-height:1;color:var(--text-tertiary);">L1</div>
  <div style="font-size:24px;font-weight:700;line-height:1.3;color:var(--text-secondary);margin-top:10px;">手工作业</div>
  <div style="font-size:20px;line-height:1.45;color:var(--text-tertiary);margin-top:8px;">口径各自定义,报表人工拼装</div>
</div>
<!-- L2(当前级):深底 + 主色顶条;h 260,y 600 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:444px;top:600px;width:324px;height:260px;background:var(--brand-dark);border-top:3px solid var(--brand-primary);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:474px;top:626px;width:264px;">
  <div class="num" style="font-size:40px;font-weight:800;line-height:1;color:var(--white);">L2</div>
  <div style="font-size:24px;font-weight:700;line-height:1.3;color:var(--on-navy-text);margin-top:10px;">局部自动化</div>
  <div style="font-size:20px;line-height:1.45;color:var(--on-navy-sub);margin-top:8px;">单产线打通,跨线仍需对账</div>
</div>
<!-- "我们在这"标记(当前级正上方) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:444px;top:540px;width:324px;height:44px;text-align:center;">
  <div style="font-size:22px;font-weight:700;color:var(--brand-primary);line-height:44px;">▼ 我们在这</div>
</div>
<!-- L3(目标级):浅底 + 主色虚线边(区别于当前级实心深底);h 320,y 540 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:788px;top:540px;width:324px;height:320px;background:var(--card-bg);border:2px dashed var(--brand-primary);"></div>
<!-- L4(h 380,y 480)/ L5(h 440,y 420)同构:浅底 + --border-medium 顶条 -->
<!-- 基线 -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:860px;width:1720px;height:2px;background:var(--border-medium);"></div>
<!-- 跨级条件注(阶梯的实用价值:说清怎么上去) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:890px;width:1720px;">
  <div style="font-size:22px;line-height:1.5;color:var(--text-secondary);"><span style="font-weight:700;color:var(--charcoal);">L2 → L3 判定条件:</span>三产线口径统一 + 月末结账 ≤2 天 + 对账人工工时下降 50%。</div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:990px;width:1720px;">
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);">来源:参照 CMMI 五级框架自定义(2026-08 内部评估,评估人:数据治理委员会)</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 级数 | 5 级 × 324px(默认);4 级改 w 415;3 级改 w 560 + 字号升一档 |
| 高度 | 递升 200/260/320/380/440,**底对齐** y=860(递升感来自顶边,不是底边) |
| 当前级 | 唯一深底 + 主色顶条 + 正上方"▼ 我们在这" |
| 目标级 | 浅底 + **主色虚线边**(与当前级区分);其余级浅底灰顶条 |
| 跨级条件 | 底部必写"当前→目标"的可观测判定条件 |

**反 AI 味要点**:✓ 当前位与跨级条件是这个原型存在的理由 —— 没有它们就是一张任何公司都能用的通用成熟度图(= 废页);✓ 递升靠高度差,❌ 不画楼梯线/箭头森林;❌ 五级五色、❌ 渐变台阶。

**降级**:级别是并列能力而非递进 → 原型 23 图标网格;只有"现在/目标"两态 → 原型 12 双栏对照。

---

### 原型 42 · 价值链(满填)

**用途**:端到端环节 + 支撑职能,并标出**价值/问题集中在哪一环**(运营诊断/流程重构/成本结构)。**何时别用**:环节无先后(用 23 图标网格);只讲流程步骤不讲价值分布(用 24 chevron)。
**填充**:满填 —— 上排主活动 chevron 带,下方支撑活动格,焦点环唯一深色。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">六成可优化成本集中在仓配一环</div>
</div>
<!-- 主活动带:5 环 chevron(w 356,x 步进 344 制造重叠;h 160,y 340) -->
<div data-object="true" data-object-type="shape" data-shape="chevron" style="position:absolute;left:100px;top:340px;width:356px;height:160px;background:var(--card-bg);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:150px;top:380px;width:280px;">
  <div style="font-size:26px;font-weight:700;line-height:1.3;color:var(--charcoal);">采购</div>
  <div style="font-size:20px;line-height:1.4;color:var(--text-secondary);margin-top:6px;">成本占比 18%</div>
</div>
<!-- 环 2(x 444)同构;环 3(x 788)= 焦点环:深底 + 白字 -->
<div data-object="true" data-object-type="shape" data-shape="chevron" style="position:absolute;left:788px;top:340px;width:356px;height:160px;background:var(--brand-dark);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:838px;top:380px;width:280px;">
  <div style="font-size:26px;font-weight:700;line-height:1.3;color:var(--on-navy-text);">仓配</div>
  <div style="font-size:20px;line-height:1.4;color:var(--on-navy-sub);margin-top:6px;">占比 34% · 可优化 6.2pp</div>
</div>
<!-- 环 4(x 1132)/ 环 5(x 1476)同构浅底 -->
<!-- 焦点标记(焦点环正下方) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:788px;top:520px;width:356px;height:3px;background:var(--brand-primary);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:788px;top:534px;width:400px;">
  <div style="font-size:20px;font-weight:600;line-height:1.4;color:var(--brand-primary);">本次诊断焦点</div>
</div>
<!-- 支撑活动带(横贯细线分区 + 标题) -->
<div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:620px;width:1720px;height:1px;background:var(--border-medium);"></div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:646px;width:1720px;">
  <div style="font-size:20px;font-weight:700;letter-spacing:2px;color:var(--text-tertiary);">支撑职能(横向服务全链)</div>
</div>
<div data-layout="grid" data-layout-cols="4" data-layout-gap="24" style="position:absolute;left:100px;top:700px;width:1720px;">
  <!-- 与焦点环有因果的那格加主色左条,把两层连起来 -->
  <div data-object="true" data-layout-h="200" style="background:var(--card-bg);border-left:3px solid var(--brand-primary);padding:28px;">
    <div style="font-size:24px;font-weight:700;line-height:1.3;color:var(--charcoal);">数据与系统</div>
    <div style="font-size:20px;line-height:1.5;color:var(--text-secondary);margin-top:10px;">WMS 与 TMS 未打通,是仓配问题的技术根因</div>
  </div>
  <!-- 其余 3 格同构(无左条) -->
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:990px;width:1720px;">
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);">来源:2026 H1 成本台账(口径:含分摊后人工与折旧);可优化空间对标同业最优四分位</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 主环数 | 5 环(w 356、x 步进 344);4 环改 w 445 步进 430;6 环改 w 296 步进 288 |
| chevron | 重叠靠 x 步进 < 宽度实现;环内文字左内缩 50px(避开箭头尖) |
| 焦点 | 唯一深底环 + 下方主色细条 + "本次诊断焦点";其余浅底 |
| 支撑带 | 4 格 grid;与焦点环有因果的那格加主色左条 |
| 每环 | 环名 + 一个量化指标(占比/成本/耗时)—— 无指标的价值链只是流程图 |

**反 AI 味要点**:✓ 每环带量化指标 + 焦点唯一,读者立刻知道"看哪里";✓ 支撑职能与主活动的**因果连接**要写出来,否则下半页是无关装饰;❌ 五环五色、❌ 渐变 chevron、❌ 支撑职能写成通用空词("人力资源/财务/IT"三个词 = 废页)。

**降级**:只讲先后不讲价值分布 → 原型 24 chevron 流程带(更轻);环节并列无序 → 原型 23。

---

### 原型 43 · 标杆对标(满填)

**用途**:自身 vs 同业基准逐项对比,标出差距与追平优先级(竞争分析/绩效诊断/尽调)。**何时别用**:只有两个对象(用 12 双栏对照 / 29 对比卡阵);无可信基准来源(编基准比不对标更糟)。
**填充**:满填 —— 表格逐项列指标,落后项整行底纹 + 我们列主色,右侧差距与优先级列。

```html
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
  <div style="font-size:56px;font-weight:700;line-height:1.2;color:var(--charcoal);">五项指标中三项落后中位,复购率差距最大</div>
</div>
<table data-object="true" style="position:absolute;left:100px;top:330px;width:1720px;border-collapse:collapse;">
  <tr style="background:var(--brand-dark);">
    <th style="width:420px;padding:20px 24px;text-align:left;font-size:22px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">指标</th>
    <th style="width:260px;padding:20px 24px;text-align:right;font-size:22px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">我们</th>
    <th style="width:260px;padding:20px 24px;text-align:right;font-size:22px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">同业中位</th>
    <th style="width:260px;padding:20px 24px;text-align:right;font-size:22px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">最优四分位</th>
    <th style="padding:20px 24px;text-align:left;font-size:22px;font-weight:700;color:var(--white);border:1px solid var(--brand-dark);">差距与优先级</th>
  </tr>
  <!-- 落后项:整行浅底纹 + 我们列主色数字(tr 级 background 是支持特性) -->
  <tr style="background:var(--card-bg);">
    <td style="padding:24px;font-size:24px;font-weight:700;color:var(--charcoal);border:1px solid var(--border-light);">复购率</td>
    <td class="num" style="padding:24px;text-align:right;font-size:26px;font-weight:800;color:var(--brand-primary);border:1px solid var(--border-light);">31%</td>
    <td class="num" style="padding:24px;text-align:right;font-size:26px;font-weight:600;color:var(--text-secondary);border:1px solid var(--border-light);">42%</td>
    <td class="num" style="padding:24px;text-align:right;font-size:26px;font-weight:600;color:var(--text-tertiary);border:1px solid var(--border-light);">51%</td>
    <td style="padding:24px;font-size:22px;line-height:1.4;color:var(--charcoal);border:1px solid var(--border-light);">-11pp · 优先级 1</td>
  </tr>
  <!-- 持平/领先项:白底 + 我们列深字(不加主色,高亮留给落后项) -->
  <tr>
    <td style="padding:24px;font-size:24px;font-weight:700;color:var(--charcoal);border:1px solid var(--border-light);">毛利率</td>
    <td class="num" style="padding:24px;text-align:right;font-size:26px;font-weight:800;color:var(--charcoal);border:1px solid var(--border-light);">48.2%</td>
    <td class="num" style="padding:24px;text-align:right;font-size:26px;font-weight:600;color:var(--text-secondary);border:1px solid var(--border-light);">47.5%</td>
    <td class="num" style="padding:24px;text-align:right;font-size:26px;font-weight:600;color:var(--text-tertiary);border:1px solid var(--border-light);">53.0%</td>
    <td style="padding:24px;font-size:22px;line-height:1.4;color:var(--text-secondary);border:1px solid var(--border-light);">+0.7pp · 持平</td>
  </tr>
  <!-- 其余 3 项同构 -->
</table>
<!-- 对标样本说明(本原型的可信度来源) -->
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:900px;width:1720px;">
  <div style="font-size:18px;line-height:1.5;color:var(--text-tertiary);">对标样本:六家可比公司(营收 5-15 亿、同细分赛道);中位与四分位按各家最新年报计算</div>
</div>
<div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:990px;width:1720px;">
  <div style="font-size:16px;line-height:1.5;color:var(--text-tertiary);">来源:各家 2025 年报及公开披露(采集于 2026-07);毛利率口径已按本公司准则重述</div>
</div>
```

| 参数 | 调什么 |
|---|---|
| 规模 | 5 项指标(演讲档表格 ≤6 行含表头);更多按主题拆两页 |
| 基准列 | 中位 + 最优四分位**两列** —— 只给一个基准无法判断"差距是否可追" |
| 强调 | 落后项整行 `--card-bg` + 我们列主色数字;持平/领先项白底深字 |
| 数字列 | 全部**右对齐** + `class="num"`;单位随数字写在同格 |
| 优先级 | 只给差距最大的 1-2 项标"优先级 1/2",其余写"持平/领先/暂缓" |

**反 AI 味要点**:✓ **对标样本必须写清是谁**(几家、什么规模、什么口径)—— 没有样本说明的对标页是最容易被一句话推翻的一页;✓ 口径重述要声明(各家准则不同);❌ 红绿箭头标涨跌(交通灯 AI 味)、❌ 每行都标优先级(全是优先级 = 没有优先级)、❌ 编造"行业平均"。

**降级**:拿不到可信基准时改原型 8 要点列表写"待补对标数据"(见 `content-deepening.md` 待补数据清单),别编基准。

---

## 使用纪律(摘要)

1. 选原型 = **二级选择**:先按 brief 形式列定视觉形式(文字/图示/图表/图片/混合),再从该形式组选原型;写页时只看 brief 指定的原型小节
2. 同原型不连续 >2 页;每 deck ≥6 原型;**纯文字卡片矩阵 ≤2 页**(图标网格不受此限,见反模式 7 结构豁免)
3. **形式分布**按 `design-principles.md` 第五章档位执行(平衡型:纯文字内容页 ≤50%、同形式连排 ≤3 页、每内容页 ≥1 个非文字视觉元素)
4. airy 页(1/2/4/5/6/21)承担节奏,每 3-4 页 1 张;满填页执行内容区 ≥85% 利用率
5. 所有骨架字号为演讲档;换档按 `design-principles.md` 字号阶等比;内容量 <60% 时按 scale-to-fill 上调
6. 原型可组拼(如 18+19 = 20),但一页只用一种"主角"
7. **组 7 分析论证(31-43)附加纪律**:每页必须带来源/口径注(见 `design-principles.md`"数据页的口径纪律");结构不成立时按各原型的"降级"行退回,**不硬套分析框架** —— 编基准、伪精确、拿不出算式链的规模页,比不做分析更糟

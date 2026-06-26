# 02 · 设计系统与视觉模板

> **本文件用途：** 规划阶段第零步，执行 Step 0→D 自创专属 Tc 模板，整份报告全程使用该模板。
>
> ⚠️ **重要：** 本文件必须在完成 `06-workflow.md` 的 S0-1~S0-4 扩写后，且用户确认"继续"后才开始使用。

---

## 核心原则

1. **报告开始前完成第零步**，创建专属 Tc 模板，整份报告全程使用该模板
2. **多样性来源 = 布局变化（≥6 种）+ 配色变化（主基调 60-80% + 对比色 20%）**
3. **禁止在页面生成时切换到父风格**（核心红线）
4. design-system/ 是参考基因库，仅第零步读 1-2 个文件，后续不再读取
5. **背景必须在 Step C 定义 Tc 时完整写出（`body` + `body::before` + `body::after` CSS 片段），此后每页原样复制——即使只生成单页也须先完成背景设计，不得留空或简化**（核心红线）

---

## 🤖 第零步：自创报告专属模板

### 步骤执行流程

```
输入：用户的报告主题 / 风格描述 / 情感诉求
  ↓
Step 0 · 设计意图四问
  用途：谁在看？什么场景？
  基调：极简克制 / 科技精品 / 杂志编辑 / 霓虹赛博 / 有机自然…
  约束：技术/内容/尺寸/语言限制
  记忆点：受众看完后记住的唯一视觉元素
  ↓
Step A · 分析意图
  主题类型（技术/商业/风险/数据/创意…）暗色系还是亮色系？
  ↓
Step B · 按需读取 OR 新建 design-system 风格文件
  ① 在下方索引中找到最匹配的风格文件名
  ② 尝试读取 design-system/[风格名].md
     ┌─ 文件存在 → 提取：背景/卡片/字体/页眉/CSS 变量(:root 块) + 变异点
     └─ 文件不存在 → 立即执行【新建流程】（见下方"★ 新建 design-system 文件"）
  ③ 从文件色盘派生 --c2 / --c3（互补色）
  ↓
Step C · 声明专属模板 Tc（填写下方模板）
  ↓
Step D · 输出维度拆解表
  格式：页码 | 主题 | 布局 | 气质/design-system | Tc 变体 | 图表 | 说明（8-12行）
  "Tc 变体"列填：Tc-主基调 / Tc-对比色 / Tc-辅助色（不写父风格名）
```

---

## ★ 新建 design-system 文件（Step B 文件不存在时强制执行）

> **触发条件：** 在 design-system/ 目录下找不到对应的 .md 文件时，必须先创建再继续。

### 新建流程

```
1. 确定文件名：design-system/[风格名].md（使用索引中的英文名，如 game-rpg.md）
2. 写入以下完整规格（缺一不可）
3. 用 Write 工具创建文件（路径：skills/html-report/design-system/[风格名].md）
4. 文件创建成功后继续 Step B 提取流程
```

### 新建文件模板（AI 填写所有 ___ 字段）

```markdown
# design-system · [风格名] · [气质关键词]

## 气质描述
[3句话：视觉情绪 · 典型场景 · 受众感受]

## 推荐字体
@import url('https://fonts.googleapis.com/css2?family=___:wght@___&family=___&display=swap');

展示字体：___ → 用于标题/大数字/卡片游戏名
正文字体：___ → 用于段落/描述
等宽字体：___ → 用于标签/数据/年份

## :root CSS 变量

\`\`\`css
:root {
  --bg:   ___; /* 页面底色 */
  --card: ___; /* 卡片背景，带透明度 */
  --p:    ___; /* 主强调色 */
  --pm:   ___; /* 主色 10-15% 透明背景 */
  --bd:   ___; /* 主色 20-25% 透明描边 */
  --t:    ___; /* 主文字色 */
  --mt:   ___; /* 次文字色 */
  --dt:   ___; /* 弱文字色（标注/页码） */
  --c1:   var(--p);   /* 图表第一系列 */
  --c2:   ___;        /* 图表第二系列，与 --p 互补 */
  --c3:   ___;        /* 图表第三系列 */
  --danger:  #ef4444;
  --warning: #f59e0b;
  --success: #10b981;
  --info:    #3b82f6;
  --neutral: #94a3b8;
  --font-display: '___ ', serif;
  --font-body:    '___ ', serif;
  --font-mono:    '___ ', monospace;
}
\`\`\`

## 背景三件套

\`\`\`css
body { background: var(--bg); }

body::before {
  content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background:
    /* 纹理层：径向光晕 + 图案 */
    ___;
}

body::after {
  content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background:
    /* 光晕层：氛围渐变 */
    ___;
}
\`\`\`

## 主题专属卡片语言

**形状语言：** ___（描述本风格卡片的形状特征，如"切角六边形""卷草纹框""血条边框"）

**线条风格：**
- 主卡边框：___px `var(--bd)` + `border-radius: ___px`
- 强调左边框：3px `var(--p)` / 语义色（CARD-B/E 专用）
- 顶部装饰线：___（扫光 / 渐变 / 实色）
- 角标装饰：___（切角三角 / 勋章点 / 符文 / 无）

**卡片变体 CSS 片段（本风格特化版）：**
\`\`\`css
/* CARD-STD 本风格实现 */
.card-std {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: ___px;
  ___; /* 本风格特有装饰 */
}
/* CARD-C 数字核心卡 */
.card-c {
  ___; /* 形状 + 背景 */
}
/* CARD-E 语义状态卡 */
.card-e {
  border-radius: 0 ___px ___px 0;
  border-left: 3px solid [语义色];
  background: rgba([语义色], 0.08);
}
\`\`\`

## 典型页眉变体
[HD1/HD2/HD3/HD4 中选一种，描述本风格页眉的具体样式]

## 适用场景
[列举3-5个典型报告主题]

## 禁止事项
- ❌ ___
- ❌ ___
```

---

### Tc 模板定义（AI 填写）

```
【专属模板 Tc · ___(名称)】

继承自：design-system/[A].md → 提取：___
        design-system/[B].md → 提取：___（可选，仅需时读第二个）
变异点：___

★ 设计意图：用途___ 基调___ 约束___ 记忆点___

背景：主背景___ 纹理/光效___（必填：噪点/渐变/几何/光晕 至少一种）
  ⚠️ 背景铁律：在此步骤写出完整 body + body::before + body::after CSS 片段，
     后续每页原样复制该片段，不得简化或省略。即使只生成单页，也必须先在 Tc 中完整定义背景。
卡片：圆角___ 边框___ 阴影___
字体：展示字体___（来自 design-system 推荐字体或@import）正文字体___
页眉：___

核心 CSS 变量（全部来自 design-system，不再使用 04-color-font）：
--bg:___; --card:___; --p:___; --pm:___; --bd:___;
--t:___;  --mt:___;   --dt:___;

多系列图表色（AI 从 design-system 色盘派生，SVG 用 --c1/--c2/--c3）：
--c1: var(--p);   /* 第一系列 = 主色 */
--c2: ___;        /* 第二系列，与 --p 互补 */
--c3: ___;        /* 第三系列（如 design-system 有第三色调）*/

语义固定色（值不变，但须在 :root 中声明）：
--danger:#ef4444; --warning:#f59e0b; --success:#10b981; --info:#3b82f6; --neutral:#94a3b8;

CSS 核心片段（必须包含背景三件套，后续每页同步复制）：
/* ① body 基底色 */
body { background: var(--bg); ... }
/* ② body::before 纹理/速度线/几何图案层 */
body::before { content:''; position:fixed; inset:0; pointer-events:none; z-index:0; ... }
/* ③ body::after 光晕/渐变覆盖层（可选，若有则必写） */
body::after { content:''; position:fixed; inset:0; pointer-events:none; z-index:0; ... }
/* ④ .card / .display-title 等组件样式 */
```

---

## 📁 design-system/ 风格文件索引（27 种，按需读 1-2 个）

| 文件名 | 气质关键词 | 适用场景 |
|--------|-----------|---------|
| `dark-luxury` | 科技感·高端·深夜实验室 | 执行摘要·技术原理·趋势 |
| `editorial-split` | 杂志感·强叙事·左暗右亮 | 案例·风险·对比分析 |
| `terminal-code` | 极客·审计·代码真实感 | 技术实现·漏洞分析 |
| `dashboard-analytical` | 数据驱动·BI报表 | 数据统计·检测评估 |
| `editorial-minimal` | 学术克制·内容为王·负空间 | 概念定义·观点陈述 |
| `neon-cyberpunk` | 高饱和·未来感·视觉冲击 | 威胁情报·攻击溯源 |
| `finance-banking` | 私行精英·金色权威·华尔街 | 金融·投资·年报 |
| `energy-industrial` | 重工业·仪表盘·石油天然气 | 能源·工程·产能 |
| `government-official` | 庄重权威·党政·公文 | 政府·政策·行政 |
| `culture-museum` | 人文气息·展览·艺术典藏 | 文化·非遗·艺术 |
| `travel-vivid` | 自由清新·目的地感 | 旅游·文旅 |
| `legal-profession` | 司法庄重·象牙白权威 | 法律·合规 |
| `engineering-blueprint` | 蓝图精密·工程制图 | 建筑·机械·工程文档 |
| `creative-studio` | 设计感强·视觉实验 | 设计·品牌·创意提案 |
| `consultant-strategy` | 麦肯锡风·框架感·战略 | 战略·咨询·管理 |
| `developer-tech` | 代码终端·极客·GitHub感 | 技术报告·架构 |
| `finance-accounting` | 账本精准·绿色财务 | 财务·会计·审计 |
| `medical-clinical` | 医疗精准·临床数据 | 医疗·健康研究 |
| `academic-research` | 期刊严谨·引文权威 | 学术报告·论文 |
| `science-lab` | 实验精密·误差标注 | 实验·检测·科学数据 |
| `military-tactical` | 作战指挥·战术分析 | 军事·安防·危机 |
| `startup-pitch` | 创业激情·增长故事·VC Pitch | 融资路演·产品发布 |
| `esg-sustainability` | 绿色地球·碳中和·有机 | ESG·碳排放 |
| `retail-commerce` | 商业活力·GMV·大促感 | 销售·电商·消费 |
| `education-tech` | EdTech友好·学习进度 | 教育报告·学情 |
| `healthtech-dark` | 可穿戴·生命体征·AI医疗 | 健康科技·数字医疗 |
| `real-estate` | 地产奢华·城市夜景·铜金 | 房地产·物业 |
| `japanese-minimalism` | 侘寂·和纸·极致留白 | 高端品牌·文化策展 |
| `swiss-international` | 瑞士网格·功能主义 | 品牌手册·设计规范 |
| `news-media` | 报纸头版·突发新闻 | 媒体·舆情·传播 |
| `academic-research` | 期刊严谨·学术权威 | 研究报告·论文摘要 |
| `vaporwave-retro` | 80年代霓虹粉紫·棋盘 | 音乐·潮流·娱乐 |
| `game-rpg` | RPG状态栏·血条·奇幻金 | 游戏·玩家数据 |
| `glitch-corrupt` | 数据损坏·RGB错位 | 网络安全事件·黑客 |
| `punk-zine` | 手撕拼贴·油墨印章 | 亚文化·独立音乐 |
| `anime-shounen` | 热血速度线·燃烧橙金 | 竞技·体育·激励 |
| `light-novel-isekai` | 异世界魔法阵·神圣金 | 奇幻·轻小说·二次元 |
| `cyberpunk-anime` | 攻壳机动队·赛博青洋红 | 科幻·AI趋势·赛博都市 |

> 其余二次元风格：`magical-girl` · `kawaii-pastel` · `dating-sim` · `visual-kei-gothic` · `akihabara-neon` · `pixel-8bit` · `y2k-millennium` · `horror-dark` · `brutalist-web` · `lofi-cassette`

---

## 配色分配原则

```
70% 页面 → 主基调配色
20% 页面 → 对比色（逻辑转折/强调，如风险页用红、防御页用绿）
10% 页面 → 特殊配色（如展望页用粉）
```

| 背景类型 | 规则 |
|---------|------|
| 暗色报告 | 全部页面暗色背景，禁混入纯白 |
| 亮色报告 | 全部页面亮色背景，禁混入深色 |
| 混合报告 | 同一章节内背景一致 |

---

## 🚫 禁止清单

```
❌ 跳过第零步，未完成设计意图四问
❌ Tc 中没有"记忆点"字段
❌ Tc 未写出 CSS 核心片段就开始生成
❌ 一次性预加载 design-system/ 所有文件
❌ 主基调配色使用率 < 50%
❌ 背景色在章节内不一致
❌ 所有页面用同一布局结构（同款超过 3 次）
❌ 卡片全部同款：深色底 + 蓝色边框 + border-radius:6px
❌ 背景纯色无纹理/渐变/光晕
❌ font-family 唯一值为系统字体（PingFang SC/Microsoft YaHei 仅作 fallback）
❌ 展示标题未引入 Google Fonts
❌ 生成时切换回父风格（核心红线）
```

---

## 多样性核查

```
□ Tc 完整定义：记忆点 + 继承来源 + CSS 变量（含 --c2/--c3）+ CSS 片段？
□ **Tc CSS 片段包含背景三件套（body + body::before + body::after）完整代码？**
□ **每页 body/::before/::after 与 Tc 定义完全一致，未被简化或省略？**
□ 所有颜色变量来自 design-system 文件（不引用 04-color-font）？
□ 语义固定色（--danger/--success/--warning 等）已在 :root 声明？
□ 主基调配色 ≥ 60%？
□ 没有连续 3 页相同布局 + 配色组合？
□ 背景色章节内一致？
□ 整份报告全程使用同一 Tc 模板（不得切换父风格）？
□ 10 页使用 ≥6 种不同布局？
□ 展示标题使用了 design-system 推荐的 Google Fonts？
□ 至少 2 页使用业务图谱（diagram-types/）？
```

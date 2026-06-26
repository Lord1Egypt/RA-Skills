# design-system · game-rpg · RPG状态栏·血条·奇幻金

## 气质描述
深夜熔金的档案馆感——沉重的历史积淀与血与火的战争史诗并存。
受众感受如同翻开一本充满勋章印记的魔法典籍，每张卡片都是一块刻有铭文的石板。
数据以骑士勋功册的方式呈现，严肃而充满张力，非娱乐而是纪念。

## 推荐字体
```css
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,400&family=Share+Tech+Mono&display=swap');
```

展示字体：`'Cinzel'` → 页眉标题·节标题·卡片游戏名·大数字（罗马/奇幻感）
正文字体：`'Crimson Pro'` → 段落正文·描述·摘要栏（经典衬线，可读性强）
等宽字体：`'Share Tech Mono'` → 年份·徽章·眉题·数据标签

## :root CSS 变量

```css
:root {
  --bg:   #07080d;                    /* 近黑，带蓝调夜空感 */
  --card: rgba(16, 13, 7, 0.93);      /* 深棕黑，羊皮纸暗面 */
  --p:    #c9a227;                    /* 魔兽黄金，主强调色 */
  --pm:   rgba(201, 162, 39, 0.13);   /* 金色 13% 透明背景 */
  --bd:   rgba(201, 162, 39, 0.24);   /* 金色 24% 描边（CARD-STD 用） */
  --t:    #eaddb8;                    /* 主文字·羊皮纸暖白 */
  --mt:   #a8925e;                    /* 次文字·旧铜色 */
  --dt:   #5e4e30;                    /* 弱文字·烟熏棕（标注/页码） */
  --c1:   var(--p);                   /* 图表第一系列 = 主色金 */
  --c2:   #6ea3d6;                    /* 图表第二系列·联盟钴蓝 */
  --c3:   #c45c3a;                    /* 图表第三系列·部落战火红橙 */
  --danger:  #ef4444;
  --warning: #f59e0b;
  --success: #10b981;
  --info:    #3b82f6;
  --neutral: #94a3b8;
  /* 派生透明变体 */
  --bd-em:     rgba(201,162,39,0.40); /* 强调描边（KPI 切角卡） */
  --bd-subtle: rgba(201,162,39,0.07); /* 极淡线（页脚） */
  --bd-sep:    rgba(255,255,255,0.05);/* SM1 摘要栏顶分隔 */
  /* 字体栈 */
  --font-display: 'Cinzel', 'Noto Serif SC', serif;
  --font-body:    'Crimson Pro', 'Noto Serif SC', serif;
  --font-mono:    'Share Tech Mono', monospace;
}
```

## 背景三件套

```css
body {
  background: var(--bg);
  font-family: var(--font-body);
  color: var(--t);
  position: relative;
}

/* 纹理层：顶部金色光晕 + 右下琥珀渐变 + 横/纵格栅纹 */
body::before {
  content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background:
    radial-gradient(ellipse 70% 55% at 50% -5%,  rgba(201,162,39,0.10) 0%, transparent 60%),
    radial-gradient(ellipse 45% 50% at 90% 110%, rgba(120,70,20,0.18)  0%, transparent 55%),
    repeating-linear-gradient(
      0deg, transparent, transparent 64px,
      rgba(201,162,39,0.018) 64px, rgba(201,162,39,0.018) 65px
    ),
    repeating-linear-gradient(
      90deg, transparent, transparent 80px,
      rgba(201,162,39,0.012) 80px, rgba(201,162,39,0.012) 81px
    );
}

/* 光晕层：左中蓝紫深影 + 右上琥珀微光 */
body::after {
  content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background:
    radial-gradient(ellipse 55% 40% at 15% 60%, rgba(25,18,70,0.22)  0%, transparent 65%),
    radial-gradient(ellipse 30% 30% at 75% 25%, rgba(80,50,10,0.12)  0%, transparent 50%);
}
```

## 主题专属卡片语言

**形状语言：** 切角六边形（战争盾牌感）— 左上角+右下角裁切 8-10px，营造盾牌/铭牌质感。
KPI 卡使用 `clip-path: polygon(8px 0%, 100% 0%, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0% 100%, 0% 8px)`。

**线条风格：**
- 主卡边框：1px `var(--bd)`，CARD-STD 圆角 6-8px
- 切角卡边框：1px `var(--bd-em)`，无 border-radius（clip-path 取代）
- 强调左边框：3px `var(--p)` 或势力语义色（CARD-B/E）
- 顶部装饰线：`linear-gradient(90deg, transparent 10%, var(--p) 50%, transparent 90%)` 扫光线
- 角标装饰：右下/右上切角三角（`::after` border 三角技法），颜色来自卡片主题色

**卡片变体 CSS 片段（game-rpg 特化版）：**

```css
/* CARD-STD — 基础内容卡，石板感 */
.card-std {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 6px;
  box-shadow: inset 0 0 20px rgba(201,162,39,0.03);
}

/* CARD-C — RPG Stat Block 切角六边形 KPI 卡 */
.card-c {
  background: linear-gradient(145deg, rgba(45,34,12,0.96) 0%, rgba(10,8,4,0.98) 100%);
  border: 1px solid var(--bd-em);
  clip-path: polygon(8px 0%, 100% 0%, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0% 100%, 0% 8px);
  box-shadow: 0 0 16px rgba(201,162,39,0.07), inset 0 0 24px rgba(201,162,39,0.04);
  position: relative;
}
/* 顶部扫光 */
.card-c::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1.5px;
  background: linear-gradient(90deg, transparent 10%, var(--p) 50%, transparent 90%);
}
/* 右下角切角填充 */
.card-c::after {
  content: ''; position: absolute; bottom: 0; right: 0;
  width: 0; height: 0; border-style: solid;
  border-width: 0 0 8px 8px;
  border-color: transparent transparent var(--kpi-corner) transparent;
}

/* CARD-B — 透明底+左金条，时间轴/列表条目 */
.card-b {
  background: linear-gradient(90deg, rgba(50,38,14,0.30) 0%, rgba(16,13,7,0.10) 100%);
  border: none;
  border-left: 3px solid var(--p);
  border-radius: 0 3px 3px 0;
}

/* CARD-E — 势力/语义色 tinted 卡（CARD-E 规范：圆角 0 6px 6px 0） */
.card-e-alliance { background: rgba(110,163,214,0.07); border: 1px solid var(--c2-bd); border-left: 3px solid var(--c2); border-radius: 0 6px 6px 0; }
.card-e-horde    { background: rgba(196,92,58,0.08);   border: 1px solid var(--c3-bd); border-left: 3px solid var(--c3); border-radius: 0 6px 6px 0; }
.card-e-scourge  { background: rgba(139,92,246,0.07);  border: 1px solid var(--sc-bd); border-left: 3px solid #8b5cf6; border-radius: 0 6px 6px 0; }
.card-e-danger   { background: rgba(239,68,68,0.07);   border: 1px solid var(--lg-bd); border-left: 3px solid var(--danger); border-radius: 0 6px 6px 0; }

/* CARD-STD 图表框变体 — 金色顶条 + 内壁发光 */
.card-chart {
  background: rgba(12,10,5,0.96);
  border: 1px solid var(--bd);
  border-top: 2px solid var(--p);
  border-radius: 0 0 6px 6px;
  box-shadow: inset 0 6px 24px rgba(201,162,39,0.04), 0 4px 20px rgba(0,0,0,0.4);
}
```

**切角三角变量（需在 :root 中声明）：**
```css
--kpi-corner: rgba(201,162,39,0.30);
--c2-corner:  rgba(110,163,214,0.35);
--c3-corner:  rgba(196,92,58,0.35);
--sc-corner:  rgba(139,92,246,0.32);
--lg-corner:  rgba(239,68,68,0.32);
/* CARD-E 边框变量 */
--c2-bd: rgba(110,163,214,0.20);
--c3-bd: rgba(196,92,58,0.20);
--sc-bd: rgba(139,92,246,0.20);
--lg-bd: rgba(239,68,68,0.20);
```

**大数字 text-shadow（Stat Block 发光效果）：**
```css
text-shadow: 0 0 18px rgba(201,162,39,0.55), 0 0 6px rgba(201,162,39,0.30);
```

## 典型页眉变体

HD2 渐变色条型（推荐）：
- 左侧：3px 垂直金色渐变竖线（`linear-gradient(180deg, transparent, var(--p), transparent)`）+ 眉题（9px mono `var(--dt)` uppercase）+ 标题（18px bold Cinzel `var(--t)`）
- 右侧：徽章（`var(--pm)` 背景 + `var(--bd)` 描边 + `var(--p)` 文字）+ 状态灯（5px `var(--p)` + glow）+ 页码（11px mono `var(--dt)`）
- 背景：`rgba(7,8,13,0.70)` + `border-bottom: 1px solid var(--bd)` + `backdrop-filter: blur(6px)`

## 适用场景
- 游戏宇宙/IP 全览（魔兽/最终幻想/黑暗之魂/艾尔登法环）
- 游戏数据报告（玩家统计/版本更新分析/竞技数据）
- RPG 风格年度报告（公会数据/赛季复盘）
- 奇幻小说/世界观设定文档
- 历史战争纪念/军事史诗类报告

## 禁止事项
- ❌ 纯白或高亮亮色背景（破坏深夜史诗感）
- ❌ 圆润的卡片圆角（>8px）——应使用切角或小圆角
- ❌ 无衬线现代字体作为展示字体（如 Inter/Roboto 作标题）
- ❌ 饱和度过高的霓虹色（赛博风格，非 RPG 风格）
- ❌ 所有卡片使用同一背景色（失去势力/阵营的视觉区分）

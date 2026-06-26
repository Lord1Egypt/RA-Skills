# 魔法少女（Magical Girl）

**气质：** 美少女战士、变身序列、星光魔法、水晶能量
**适用：** 二次元活动、动画数据报告、粉丝分析、偶像企划
**推荐字体：** FP-6（Fraunces + Nunito）或 FP-1（Syne + DM Sans）
**背景类型：** 亮色系（星空粉白 #fdf2f8），流星渐变光晕
**主标题字号：** 44–64px，圆润粗体，发光描边，魔法变身感
**页眉形式：** 粉紫渐变底色，白色标题，右侧星星/爱心装饰，彩虹分割线

---

## 设计特征

- **星光粉**（#f472b6 / #ec4899）+ **魔法紫**（#a855f7 / #c084fc）双主色
- 粉白背景，彩色渐变流星光效
- 爱心 ♥、星星 ✦、蝴蝶结 🎀 等魔法装饰符号（纯 CSS/字符）
- 卡片带彩虹渐变顶线 + 白色毛玻璃底
- 进度条用粉紫渐变发光条，魔法蓄能感

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@1,9..144,900&family=Nunito:wght@400;600;700;800&display=swap');

body { background: #fdf2f8; font-family: 'Nunito','PingFang SC',sans-serif; color: #4a1040; }

/* 流星渐变光晕 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 80% 10%, rgba(244,114,182,0.2) 0%, transparent 45%),
    radial-gradient(ellipse at 20% 80%, rgba(168,85,247,0.15) 0%, transparent 40%),
    radial-gradient(ellipse at 50% 50%, rgba(251,207,232,0.3) 0%, transparent 60%);
}

/* 展示标题（魔法发光描边） */
.display-title {
  font-family: 'Fraunces','Noto Serif SC',serif;
  font-size: 56px; font-weight: 900; font-style: italic;
  letter-spacing: -1.5px; line-height: 0.95;
  background: linear-gradient(135deg, #ec4899, #a855f7, #6366f1);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 12px rgba(236,72,153,0.4));
}

/* 变身口号副标题 */
.magical-subtitle {
  font-family: 'Nunito',sans-serif;
  font-size: 9px; font-weight: 800; letter-spacing: 3px; text-transform: uppercase;
  background: linear-gradient(90deg, #ec4899, #a855f7);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 卡片（白色毛玻璃，彩虹顶线） */
.card {
  background: rgba(255,255,255,0.85);
  border: none;
  border-top: 2px solid transparent;
  border-image: linear-gradient(90deg, #ec4899, #a855f7, #6366f1, #ec4899) 1;
  border-radius: 12px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 6px;
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 20px rgba(236,72,153,0.12), 0 1px 4px rgba(168,85,247,0.1);
}

/* KPI 数字（魔力粉紫） */
.stat-num {
  font-family: 'Fraunces', serif;
  font-size: 50px; font-weight: 900; font-style: italic; line-height: 1;
  background: linear-gradient(135deg, #ec4899, #a855f7);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 8px rgba(236,72,153,0.3));
}

/* 魔法徽章（星星爱心） */
.magic-tag {
  display: inline-flex; align-items: center; gap: 3px;
  border-radius: 100px; padding: 3px 10px;
  font-size: 9px; font-weight: 800; letter-spacing: 0.3px;
}
.magic-tag.pink   { background: rgba(236,72,153,0.1); color: #ec4899; }
.magic-tag.purple { background: rgba(168,85,247,0.1); color: #a855f7; }
.magic-tag.star   { background: rgba(251,191,36,0.12); color: #d97706; }
.magic-tag::before { content: '✦ '; font-size: 8px; }

/* 魔法能量进度条 */
.magic-bar {
  height: 6px; border-radius: 6px;
  background: rgba(236,72,153,0.1);
}
.magic-fill {
  height: 100%; border-radius: 6px;
  background: linear-gradient(90deg, #ec4899, #a855f7, #c084fc);
  box-shadow: 0 0 8px rgba(168,85,247,0.4);
}

/* 彩虹分割线 */
.rainbow-rule {
  height: 2px; border: none;
  background: linear-gradient(90deg, #ec4899, #f97316, #fbbf24, #4ade80, #60a5fa, #a855f7);
  border-radius: 2px; margin: 6px 0; opacity: 0.6;
}

/* 星星装饰点 */
.star-dot {
  display: inline-block; color: #f472b6;
  font-size: 10px; line-height: 1;
}

/* 数据行（梦幻感） */
.magic-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10.5px; padding: 3px 0;
  border-bottom: 1px solid rgba(236,72,153,0.1);
}
.magic-row .label { color: rgba(74,16,64,0.5); }
.magic-row .value { color: #ec4899; font-weight: 700; }

/* 魔法卷轴引用框 */
.spell-box {
  background: linear-gradient(135deg, rgba(236,72,153,0.05), rgba(168,85,247,0.05));
  border: 1px solid rgba(236,72,153,0.2);
  border-radius: 8px; padding: 6px 10px;
  font-size: 10px; font-style: italic; color: rgba(74,16,64,0.7);
  text-align: center;
}
.spell-box::before { content: '✦ '; color: #f472b6; }
.spell-box::after  { content: ' ✦'; color: #a855f7; }
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #fdf2f8;
  --card: rgba(255,255,255,0.85);
  --p:    #ec4899;
  --pm:   rgba(236,72,153,0.08);
  --bd:   rgba(236,72,153,0.15);
  --t:    #4a1040;
  --mt:   #9d174d;
  --dt:   #f9a8d4;
}
/* --p2: #a855f7; (魔法紫副色) */
```

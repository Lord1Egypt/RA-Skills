# Lo-Fi磁带（Lo-Fi Cassette）

**气质：** 老式磁带、咖啡厅昏黄、复古颗粒、学习氛围感
**适用：** 生活方式报告、音乐数据、创意过程、个人成长回顾
**推荐字体：** FP-6（Fraunces + Nunito），温暖手写感
**背景类型：** 亮色系（暗黄暖灯 #f0e6cc / 咖啡牛奶 #ede0c8），磁带标签感
**主标题字号：** 36–50px Fraunces 斜体，字迹温暖，不刻意完美
**页眉形式：** 手写风格，铅笔灰，随意性强，磁带卷标排版

---

## 设计特征

- **暖棕咖啡**（#6b4226 / #92583a）+ **烟草黄**（#b5820a）双主色
- 牛奶咖啡色背景，老照片暖色调
- 卡片模拟磁带标签（手写框，圆角贴纸感）
- 进度条模拟磁带走带（细长波浪线）
- 颗粒噪点 + 暖光晕，vintage 照片感

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;1,9..144,700;1,9..144,900&family=Nunito:wght@300;400;600&display=swap');

body {
  background: #f0e6cc;
  font-family: 'Nunito','PingFang SC',sans-serif;
  color: #3d2b1a;
}

/* 老照片暖光晕 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 50% 50%, rgba(181,130,10,0.08) 0%, transparent 60%),
    radial-gradient(ellipse at 0% 0%, rgba(200,140,60,0.12) 0%, transparent 40%),
    radial-gradient(ellipse at 100% 100%, rgba(120,70,20,0.1) 0%, transparent 40%);
}

/* 胶片颗粒 */
body::after {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:1; opacity:0.25;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.2'/%3E%3C/svg%3E");
  mix-blend-mode: multiply;
}

/* 展示标题（手写磁带感） */
.display-title {
  font-family: 'Fraunces','Noto Serif SC',serif;
  font-size: 46px; font-weight: 900; font-style: italic;
  letter-spacing: -1px; line-height: 1.05;
  color: #3d2b1a;
}

/* 磁带卷标卡片 */
.card {
  background: rgba(255,248,230,0.9);
  border: 1.5px solid rgba(107,66,38,0.25);
  border-radius: 8px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 6px;
  box-shadow:
    0 2px 8px rgba(107,66,38,0.1),
    inset 0 0 20px rgba(181,130,10,0.04);
}

/* KPI 数字（暖棕咖啡） */
.stat-num {
  font-family: 'Fraunces', serif;
  font-size: 48px; font-weight: 900; font-style: italic; line-height: 1;
  color: #6b4226;
}

/* 磁带走带进度条（细波浪） */
.tape-bar {
  height: 6px; border-radius: 0;
  background: rgba(107,66,38,0.1);
  border-top: 1px solid rgba(107,66,38,0.15);
  border-bottom: 1px solid rgba(107,66,38,0.15);
}
.tape-fill {
  height: 100%;
  background: linear-gradient(90deg, #6b4226, #92583a, #b5820a, #92583a);
  background-size: 60px 100%;
}

/* 贴纸感标签 */
.lofi-tag {
  display: inline-flex; align-items: center;
  border-radius: 100px; padding: 3px 10px;
  font-size: 9px; font-weight: 700; letter-spacing: 0.3px;
}
.lofi-tag.coffee { background: rgba(107,66,38,0.12); color: #6b4226; }
.lofi-tag.warm   { background: rgba(181,130,10,0.12); color: #b5820a; }
.lofi-tag.sage   { background: rgba(80,110,70,0.12);  color: #4a6644; }

/* 暖色分割线 */
.tape-rule {
  height: 1px; border: none;
  background: rgba(107,66,38,0.2); margin: 6px 0;
}

/* 数据行（铅笔感） */
.lofi-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10.5px; padding: 3px 0;
  border-bottom: 1px dotted rgba(107,66,38,0.15);
}
.lofi-row .label { color: rgba(61,43,26,0.55); font-weight: 300; }
.lofi-row .value { color: #6b4226; font-weight: 600; }

/* 引用（手写笔记感） */
.handnote {
  background: rgba(255,240,180,0.6);
  border-left: 2.5px solid rgba(181,130,10,0.4);
  padding: 6px 10px; font-size: 10.5px;
  font-family: 'Fraunces',serif; font-style: italic;
  color: rgba(61,43,26,0.7); line-height: 1.5;
}
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #f0e6cc;
  --card: rgba(255,248,230,0.9);
  --p:    #6b4226;
  --pm:   rgba(107,66,38,0.08);
  --bd:   rgba(107,66,38,0.2);
  --t:    #3d2b1a;
  --mt:   rgba(61,43,26,0.6);
  --dt:   rgba(61,43,26,0.35);
}
/* --warm: #b5820a; (烟草黄副色) */
```

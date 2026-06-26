# 可爱马卡龙（Kawaii Pastel）

**气质：** 卡哇伊、马卡龙色系、软糯圆润、少女心爆棚
**适用：** 萌系活动报告、可爱产品数据、生活方式、美食甜品
**推荐字体：** FP-6（Fraunces + Nunito），圆润无锋
**背景类型：** 亮色系（棉花糖白 #fff8fd / 薄荷奶昔 #f0fff8），多巴胺柔和
**主标题字号：** 40–56px Nunito 800，圆角感十足，甜糯不压迫
**页眉形式：** 多色马卡龙圆点装饰，字号可爱，右侧 UwU/OωO 情绪符号

---

## 设计特征

- **马卡龙五色**：草莓粉 #fda4af、薰衣草紫 #c4b5fd、天空蓝 #93c5fd、薄荷绿 #86efac、奶黄 #fde68a
- 超柔和背景（接近纯白，极低饱和度）
- 圆角最大化（border-radius: 16–24px），所有尖角消灭
- 卡片带彩色马卡龙圆点装饰
- 泡泡对话框、星星闪耀、爱心符号无处不在

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

body { background: #fff8fd; font-family: 'Nunito','PingFang SC',sans-serif; color: #3d1a4a; }

/* 马卡龙渐变光晕 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 85% 15%, rgba(253,164,175,0.2) 0%, transparent 40%),
    radial-gradient(ellipse at 15% 85%, rgba(196,181,253,0.18) 0%, transparent 40%),
    radial-gradient(ellipse at 50% 50%, rgba(147,197,253,0.1) 0%, transparent 50%);
}

/* 展示标题（圆润甜糯） */
.display-title {
  font-family: 'Nunito','PingFang SC',sans-serif;
  font-size: 52px; font-weight: 900;
  letter-spacing: -1px; line-height: 1.0;
  color: #c026d3;
  text-shadow: 0 4px 16px rgba(192,38,211,0.15);
}

/* 马卡龙圆角卡片 */
.card {
  background: rgba(255,255,255,0.92);
  border: none;
  border-radius: 20px; padding: 12px 16px;
  display: flex; flex-direction: column; gap: 6px;
  box-shadow:
    0 6px 20px rgba(192,38,211,0.08),
    0 2px 6px rgba(253,164,175,0.12);
}

/* 马卡龙圆点顶部装饰 */
.card-dots {
  display: flex; gap: 5px; margin-bottom: 4px;
}
.card-dots span {
  width: 8px; height: 8px; border-radius: 50%;
}
.card-dots .s { background: #fda4af; }
.card-dots .l { background: #c4b5fd; }
.card-dots .b { background: #93c5fd; }

/* KPI 数字（马卡龙粉紫） */
.stat-num {
  font-family: 'Nunito', sans-serif;
  font-size: 52px; font-weight: 900; line-height: 1; letter-spacing: -1px;
  color: #c026d3;
}
.stat-unit { font-size: 18px; color: #e879f9; margin-left: 2px; }

/* 马卡龙标签（全圆角彩色胶囊） */
.kawaii-tag {
  display: inline-flex; align-items: center; gap: 3px;
  border-radius: 100px; padding: 3px 10px;
  font-size: 9px; font-weight: 800; letter-spacing: 0.3px;
}
.kawaii-tag.pink   { background: rgba(253,164,175,0.25); color: #e11d48; }
.kawaii-tag.purple { background: rgba(196,181,253,0.3);  color: #7c3aed; }
.kawaii-tag.blue   { background: rgba(147,197,253,0.3);  color: #2563eb; }
.kawaii-tag.green  { background: rgba(134,239,172,0.3);  color: #16a34a; }
.kawaii-tag.yellow { background: rgba(253,230,138,0.35); color: #92400e; }

/* 糖果进度条 */
.candy-bar {
  height: 8px; border-radius: 100px;
  background: rgba(192,38,211,0.08);
}
.candy-fill {
  height: 100%; border-radius: 100px;
  background: linear-gradient(90deg, #fda4af, #c4b5fd, #93c5fd);
}

/* 泡泡对话框（NPC 说话） */
.bubble-box {
  background: rgba(253,164,175,0.12);
  border: 1.5px solid rgba(253,164,175,0.35);
  border-radius: 16px; border-bottom-left-radius: 4px;
  padding: 7px 12px; font-size: 10.5px;
  color: rgba(61,26,74,0.75); line-height: 1.5;
  position: relative;
}
.bubble-box::after {
  content:'';
  position: absolute; bottom:-8px; left:12px;
  width:12px; height:8px;
  background: rgba(253,164,175,0.12);
  clip-path: polygon(0 0, 100% 0, 0 100%);
}

/* 星星闪耀分割线 */
.sparkle-rule {
  text-align: center; color: #e879f9;
  font-size: 10px; letter-spacing: 8px; margin: 6px 0;
  opacity: 0.6;
}
/* 内容：✦  ✦  ✦  ✦  ✦ */

/* 数据行（甜糯感） */
.kawaii-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10.5px; padding: 3px 0;
  border-bottom: 1.5px dashed rgba(196,181,253,0.35);
}
.kawaii-row .label { color: rgba(61,26,74,0.45); }
.kawaii-row .value { color: #c026d3; font-weight: 800; }
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #fff8fd;
  --card: rgba(255,255,255,0.92);
  --p:    #c026d3;
  --pm:   rgba(192,38,211,0.08);
  --bd:   rgba(253,164,175,0.3);
  --t:    #3d1a4a;
  --mt:   rgba(61,26,74,0.55);
  --dt:   rgba(61,26,74,0.3);
}
/* 马卡龙五色: #fda4af #c4b5fd #93c5fd #86efac #fde68a */
```

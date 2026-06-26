# 旅游活力（Travel Vivid）

**气质：** 旅行自由、目的地营销、清新活力、度假感
**适用：** 旅游报告、景区规划、文旅活动、目的地品牌
**推荐字体：** FP-5（Bebas Neue + Barlow）或 FP-6（Fraunces + Nunito）
**背景类型：** 亮色系（天蓝 / 珊瑚白渐变）
**主标题字号：** 48–64px 全大写冲击感，或优雅手写衬线
**页眉形式：** 大色块背景页眉，白色标题，右侧目的地标签

---

## 设计特征

- **天蓝**（#0891b2）+ **活力橙珊瑚**（#f97316）双主色，清新明快
- 亮色背景，渐变天空感
- 卡片白色背景 + 圆角 12px，度假轻盈感
- 大标题全大写（Bebas Neue），视觉冲击
- 标签用彩色 pill 徽章，色彩丰富

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;600;700&display=swap');

body { background: #f0f9ff; font-family: 'Barlow','PingFang SC',sans-serif; color: #0c2a3e; }

/* 天空渐变背景 */
body::after {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:-1;
  background: linear-gradient(180deg, #e0f2fe 0%, #f0f9ff 50%, #fff7ed 100%);
}

/* 展示标题（全大写冲击） */
.display-title {
  font-family: 'Bebas Neue','PingFang SC',sans-serif;
  font-size: 58px; font-weight: 400; letter-spacing: 2px;
  line-height: 0.95; color: #0891b2;
  text-shadow: 0 2px 20px rgba(8,145,178,0.2);
}

/* 卡片（白色圆角，轻阴影） */
.card {
  background: rgba(255,255,255,0.9);
  border: none;
  border-radius: 12px; padding: 12px 16px;
  display: flex; flex-direction: column; gap: 5px;
  box-shadow: 0 4px 16px rgba(8,145,178,0.1), 0 1px 4px rgba(0,0,0,0.06);
}

/* KPI 数字 */
.stat-num {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 44px; font-weight: 400; line-height: 1; letter-spacing: 1px;
  color: #0891b2;
}

/* 彩色目的地标签 */
.dest-tag {
  display:inline-flex; align-items:center; gap:4px;
  background: rgba(8,145,178,0.1); border:none;
  border-radius:20px; padding:3px 10px;
  font-size:9px; font-weight:700; color:#0891b2;
  letter-spacing:0.5px; text-transform:uppercase;
}
.dest-tag.orange { background:rgba(249,115,22,0.1); color:#f97316; }
.dest-tag.green  { background:rgba(16,185,129,0.1); color:#10b981; }

/* 活力渐变进度条 */
.vivid-bar {
  height:4px; border-radius:4px;
  background: linear-gradient(90deg, #0891b2, #06b6d4, #38bdf8);
}

/* 图片占位卡（度假感） */
.photo-card {
  background: linear-gradient(135deg, #0891b2, #06b6d4);
  border-radius: 10px; display:flex; align-items:center; justify-content:center;
  font-family:'Bebas Neue',sans-serif; font-size:22px; color:rgba(255,255,255,0.6);
  letter-spacing:2px;
}
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #f0f9ff;
  --card: #ffffff;
  --p:    #0891b2;
  --pm:   rgba(8,145,178,0.1);
  --bd:   rgba(8,145,178,0.15);
  --t:    #0c2a3e;
  --mt:   #374151;
  --dt:   #9ca3af;
}
/* 活力副色 */
/* --accent2: #f97316; (珊瑚橙，活动/促销强调) */
```

# 暗色精品（Dark Luxury）

**气质：** 科技感、高端精致、深夜实验室
**适用：** 执行摘要、技术原理、趋势展望
**推荐字体：** FP-1（Syne + DM Sans）或 FP-4（Cormorant Garamond + Outfit）
**背景类型：** 暗色系
**主标题字号：** 32–42px 渐变裁剪
**页眉形式：** 小大写 eyebrow + 圆点状态灯 + monospace 页码

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

body { background: #05080f; font-family: 'DM Sans','PingFang SC',sans-serif; }

/* 噪点纹理 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:100;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
}

/* 环境光晕 */
.glow {
  position:absolute; border-radius:50%; pointer-events:none;
  background: radial-gradient(ellipse, rgba(R,G,B,0.09) 0%, transparent 65%);
}

/* 展示标题 */
.display-title {
  font-family: 'Syne','PingFang SC',sans-serif;
  font-size: 38px; font-weight: 800;
  letter-spacing: -1.5px; line-height: 1.0;
  background: linear-gradient(135deg, #e2e8f0 30%, ACCENT_COLOR);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 卡片 */
.card {
  background: rgba(13,17,30,0.8);
  border: 1px solid rgba(255,255,255,0.06);
  backdrop-filter: blur(8px);
  border-radius: 8px; padding: 14px 16px;
  display: flex; flex-direction: column; gap: 5px;
}
.card::before {            /* 顶部高光线 */
  content:''; display:block; height:1px; flex-shrink:0;
  background: linear-gradient(90deg, transparent, rgba(ACCENT,0.4), transparent);
  margin: -14px -16px 10px;
}
.card-bar {                /* 左侧色条 */
  position:absolute; left:0; top:14px; bottom:14px;
  width:2px; border-radius:2px;
}

/* 页眉 */
.hd-eyebrow { font-size: 9.5px; letter-spacing: 2.5px; text-transform: uppercase; color: #374151; }
.status-dot { width:5px; height:5px; border-radius:50%; box-shadow: 0 0 8px rgba(R,G,B,0.9); }

/* 统计数字 */
.stat-num {
  font-family: 'Syne', sans-serif;
  font-size: 42px; font-weight: 800;
  line-height: 1; letter-spacing: -2px;
  background: linear-gradient(135deg, COLOR_A, COLOR_B);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.stat-divider {
  position:absolute; left:0; top:8%; height:84%; width:1px;
  background: linear-gradient(180deg, transparent, rgba(ACCENT,0.3), transparent);
}
```

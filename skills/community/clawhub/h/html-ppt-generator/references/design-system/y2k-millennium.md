# Y2K千禧年（Y2K Millennium）

**气质：** 2000年代初、银色金属质感、CD光泽、第一代互联网
**适用：** 科技回顾报告、千禧年文化、互联网历史、复古科技
**推荐字体：** FP-1（Syne + DM Sans），金属感大写
**背景类型：** 暗色系（铬黑 #0c0c14），金属铬光泽渐变
**主标题字号：** 44–60px，银白金属渐变，字间距宽
**页眉形式：** 金属质感横条，泡泡数字页码，半透明毛玻璃感

---

## 设计特征

- **铬银**（#c0c0c0 / #e8e8e8）+ **Y2K蓝**（#4d9fff）+ **幻彩紫**（#9d5fff）
- 铬黑背景 + CD光泽彩虹渐变光晕
- 毛玻璃卡片（backdrop-filter: blur）
- 银色金属渐变标题（metallic shimmer）
- 圆形泡泡组件、像元反光效果

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

body { background: #0c0c14; font-family: 'DM Sans','PingFang SC',sans-serif; color: #d8d8e8; }

/* CD 光泽彩虹光晕 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    conic-gradient(
      from 200deg at 60% 40%,
      rgba(77,159,255,0.06) 0deg,
      rgba(157,95,255,0.06) 90deg,
      rgba(255,100,150,0.05) 180deg,
      rgba(77,255,200,0.05) 270deg,
      rgba(77,159,255,0.06) 360deg
    );
}

/* 铬银金属渐变标题 */
.display-title {
  font-family: 'Syne','PingFang SC',sans-serif;
  font-size: 52px; font-weight: 800;
  letter-spacing: 2px; line-height: 1.0; text-transform: uppercase;
  background: linear-gradient(180deg,
    #ffffff 0%, #d0d0d8 20%, #f0f0f8 40%,
    #a0a0b8 60%, #e8e8f0 80%, #c0c0d0 100%
  );
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 2px 8px rgba(200,200,255,0.3));
}

/* 毛玻璃卡片 */
.card {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  border-top: 1px solid rgba(255,255,255,0.25);
  border-radius: 12px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow:
    0 4px 16px rgba(0,0,0,0.3),
    inset 0 1px 0 rgba(255,255,255,0.15);
}

/* KPI（铬银数字） */
.stat-num {
  font-family: 'Syne', sans-serif;
  font-size: 48px; font-weight: 800; line-height: 1; letter-spacing: 1px;
  background: linear-gradient(180deg, #ffffff 0%, #9090b0 50%, #e0e0f0 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* CD 彩虹圆形泡泡 */
.y2k-bubble {
  width: 32px; height: 32px; border-radius: 50%;
  background: conic-gradient(
    #ff6eb4, #ff9d4d, #ffed4a, #4dff91, #4dcbff, #a64dff, #ff6eb4
  );
  opacity: 0.7; flex-shrink: 0;
}

/* 幻彩标签 */
.y2k-tag {
  display: inline-flex; align-items: center;
  border-radius: 100px; padding: 2px 10px;
  font-size: 9px; font-weight: 700; letter-spacing: 0.5px;
  background: linear-gradient(135deg, rgba(77,159,255,0.15), rgba(157,95,255,0.15));
  border: 1px solid rgba(200,200,255,0.2);
  color: #9dbfff;
}

/* 进度条（铬银） */
.chrome-bar { height: 6px; border-radius: 6px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
}
.chrome-fill { height: 100%; border-radius: 6px;
  background: linear-gradient(90deg, #6080d0, #9dbfff, #d0d8ff, #9dbfff);
  box-shadow: 0 0 8px rgba(150,180,255,0.3); }

/* 银色分割线 */
.chrome-rule {
  height: 1px; border: none;
  background: linear-gradient(90deg,
    transparent, rgba(255,255,255,0.1), rgba(255,255,255,0.25), rgba(255,255,255,0.1), transparent
  );
  margin: 6px 0;
}

/* 数据行 */
.y2k-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10.5px; padding: 3px 0;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.y2k-row .label { color: rgba(216,216,232,0.5); }
.y2k-row .value { color: #b0c8ff; font-weight: 600; }
```

---

## CSS 变量

```css
:root {
  --bg:   #0c0c14;
  --card: rgba(255,255,255,0.06);
  --p:    #9dbfff;
  --pm:   rgba(100,150,255,0.1);
  --bd:   rgba(255,255,255,0.12);
  --t:    #d8d8e8;
  --mt:   #9090a8;
  --dt:   #404060;
}
```

# ESG可持续（ESG Sustainability）

**气质：** 绿色地球、可持续发展、碳中和、企业社会责任
**适用：** ESG报告、碳排放分析、环境评估、可持续发展白皮书
**推荐字体：** FP-6（Fraunces + Nunito）
**背景类型：** 亮色系（有机米绿 #f2f7f0），自然大地感
**主标题字号：** 36–48px Fraunces 可变体衬线，有机曲线感
**页眉形式：** 左侧碳排放目标/年份，右侧报告周期，绿色细线分割

---

## 设计特征

- **森林绿**（#166534 / #16a34a）主色调，碳中和/环保诉求
- 大地有机色辅助（土黄 #a16207，天蓝 #0369a1）
- 背景带细腻有机纹理（噪点或自然渐变）
- 进度条模拟碳排放削减量/可再生能源占比
- 自然素材感卡片（轻绿底，无过度阴影）

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,700;1,9..144,900&family=Nunito:wght@300;400;600;700&display=swap');

body { background: #f2f7f0; font-family: 'Nunito','PingFang SC',sans-serif; color: #14231a; }

/* 有机背景纹理 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 80% 20%, rgba(22,163,74,0.06) 0%, transparent 50%),
    radial-gradient(ellipse at 20% 80%, rgba(3,105,161,0.04) 0%, transparent 40%);
}

/* 展示标题（有机衬线） */
.display-title {
  font-family: 'Fraunces','Noto Serif SC',serif;
  font-size: 44px; font-weight: 900; font-style: italic;
  letter-spacing: -1px; line-height: 1.0;
  color: #166534;
}

/* 卡片（有机绿底，无硬边框） */
.card {
  background: rgba(240,249,240,0.9);
  border: 1px solid rgba(22,163,74,0.15);
  border-radius: 8px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  box-shadow: 0 2px 8px rgba(22,163,74,0.07);
}

/* KPI 数字（森林绿） */
.stat-num {
  font-family: 'Fraunces', serif;
  font-size: 44px; font-weight: 900; line-height: 1; font-style: italic;
  color: #166534;
}

/* 碳排放/指标标签 */
.eco-tag {
  display: inline-flex; align-items: center; gap: 4px;
  border-radius: 100px; padding: 3px 10px;
  font-size: 9px; font-weight: 700; letter-spacing: 0.3px;
}
.eco-tag.green  { background: rgba(22,163,74,0.12); color: #166534; }
.eco-tag.blue   { background: rgba(3,105,161,0.10); color: #0369a1; }
.eco-tag.earth  { background: rgba(161,98,7,0.10);  color: #a16207; }

/* 碳削减进度条 */
.carbon-bar {
  height: 6px; border-radius: 6px;
  background: rgba(22,163,74,0.12);
}
.carbon-fill { height: 100%; border-radius: 6px;
  background: linear-gradient(90deg, #166534, #16a34a, #4ade80); }

/* 指标行（三柱：指标/当期/目标） */
.esg-row {
  display: flex; align-items: center; gap: 8px;
  font-size: 10px; padding: 3px 0;
  border-bottom: 1px solid rgba(22,163,74,0.08);
}
.esg-row .label { flex: 1; color: #374151; }
.esg-row .curr  { color: #166534; font-weight: 700; min-width: 40px; text-align: right; }
.esg-row .tgt   { color: #6b7280; font-size: 9px; min-width: 40px; text-align: right; }

/* 有机分割线 */
.eco-divider {
  height: 1px; border: none;
  background: linear-gradient(90deg, transparent, rgba(22,163,74,0.3), transparent);
  margin: 6px 0;
}
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #f2f7f0;
  --card: rgba(240,249,240,0.9);
  --p:    #166534;
  --pm:   rgba(22,163,74,0.1);
  --bd:   rgba(22,163,74,0.15);
  --t:    #14231a;
  --mt:   #374151;
  --dt:   #6b7280;
}
/* 辅助色 */
/* --water: #0369a1; --earth: #a16207; */
```

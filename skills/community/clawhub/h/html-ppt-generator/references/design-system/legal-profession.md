# 法律律师（Legal Profession）

**气质：** 严谨权威、司法庄重、条文精准、信任感
**适用：** 法律报告、合规分析、案例梳理、法务汇报
**推荐字体：** FP-2（Playfair Display + Source Sans 3）
**背景类型：** 亮色系（象牙白 #fafaf7），低饱和度肃穆感
**主标题字号：** 32–44px 衬线大标题，字距收紧，庄重感
**页眉形式：** 左侧条款编号 + 文件名称，右侧机构/律所，底部深色横线

---

## 设计特征

- **深藏青**（#1e3a5f）+ **深酒红**（#7f1d1d）双主色，司法权威感
- 象牙白背景，接近法律文书纸张质感
- 衬线大标题（Playfair Display），传递传统权威
- 卡片用象牙底色 + 深藏青顶线，无圆角（方正严谨）
- 条款列表用圆点或编号，密集信息排列

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Source+Sans+3:wght@300;400;600&display=swap');

body { background: #fafaf7; font-family: 'Source Sans 3','PingFang SC',sans-serif; color: #1a1a1a; }

/* 展示标题（衬线权威） */
.display-title {
  font-family: 'Playfair Display','Noto Serif SC',serif;
  font-size: 40px; font-weight: 900;
  letter-spacing: -1px; line-height: 1.05;
  color: #1e3a5f;
}

/* 条款副标题 */
.clause-subtitle {
  font-family: 'Source Sans 3',sans-serif;
  font-size: 10px; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
  color: #7f1d1d; opacity: 0.8;
}

/* 卡片（方正，深藏青顶线） */
.card {
  background: #f5f5f0;
  border: 1px solid rgba(30,58,95,0.12);
  border-top: 2px solid #1e3a5f;
  border-radius: 0; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
}

/* KPI 数字（衬线权威蓝） */
.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 40px; font-weight: 900;
  line-height: 1; color: #1e3a5f;
}

/* 条款列表项 */
.clause-item {
  display: flex; gap: 8px; padding: 4px 0;
  border-bottom: 1px solid rgba(30,58,95,0.08);
  font-size: 10.5px; color: #374151;
}
.clause-num {
  color: #7f1d1d; font-weight: 700;
  font-size: 10px; flex-shrink: 0; width: 20px;
}

/* 司法红横线 */
.legal-divider {
  height: 1px; border: none;
  background: linear-gradient(90deg, #7f1d1d 0%, rgba(127,29,29,0.3) 60%, transparent);
  margin: 6px 0;
}

/* 引用/法条框 */
.statute-box {
  background: rgba(30,58,95,0.05);
  border-left: 3px solid #1e3a5f;
  padding: 6px 10px; font-size: 10px;
  font-family: 'Playfair Display',serif; font-style: italic;
  color: #1e3a5f;
}

/* 风险/合规标签 */
.risk-tag {
  display: inline-flex; align-items: center;
  background: rgba(127,29,29,0.08); border: 1px solid rgba(127,29,29,0.2);
  border-radius: 2px; padding: 2px 7px;
  font-size: 8.5px; font-weight: 700; color: #7f1d1d;
  letter-spacing: 0.5px; text-transform: uppercase;
}
.risk-tag.low { background: rgba(30,58,95,0.08); border-color: rgba(30,58,95,0.2); color: #1e3a5f; }
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #fafaf7;
  --card: #f5f5f0;
  --p:    #1e3a5f;
  --pm:   rgba(30,58,95,0.08);
  --bd:   rgba(30,58,95,0.12);
  --t:    #1a1a1a;
  --mt:   #374151;
  --dt:   #9ca3af;
}
/* 辅助强调色 */
/* --accent-red: #7f1d1d; (司法红，风险/警示标注) */
```

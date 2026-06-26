# 新闻传媒（News Media）

**气质：** 报纸编辑、突发新闻、硬核信息、时效冲击
**适用：** 媒体报告、舆情分析、新闻摘要、传播数据
**推荐字体：** FP-2（Playfair Display + Source Sans 3）
**背景类型：** 亮色系（新闻纸白 #fefefe / 微黄 #fffdf8），印刷感
**主标题字号：** 44–64px Playfair 900，报纸头版冲击感，超紧字距
**页眉形式：** 满宽双线页眉（上细下粗），左侧媒体名，中间版次，右侧日期，报纸味

---

## 设计特征

- **墨黑**（#0a0a0a）+ **醒目红**（#dc2626）双主色，突发新闻感
- 新闻纸底色，轻微黄化效果
- 标题字体极大，正文紧凑密排
- 多栏网格布局（模拟报纸分栏）
- 时间戳、版次、通讯社标注等新闻元素

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=Source+Sans+3:wght@300;400;600&display=swap');

body { background: #fffdf8; font-family: 'Source Sans 3','Noto Sans SC',sans-serif; color: #0a0a0a; }

/* 报纸双线页眉 */
.news-masthead {
  border-top: 3px solid #0a0a0a;
  border-bottom: 1px solid #0a0a0a;
  padding: 6px 0; display: flex; align-items: center; gap: 12px;
}
.masthead-name {
  font-family: 'Playfair Display',serif;
  font-size: 22px; font-weight: 900; letter-spacing: -0.5px;
}

/* 头版大标题 */
.display-title {
  font-family: 'Playfair Display','Noto Serif SC',serif;
  font-size: 56px; font-weight: 900; font-style: italic;
  letter-spacing: -2.5px; line-height: 0.9;
  color: #0a0a0a;
}

/* 新闻导语副题 */
.news-deck {
  font-family: 'Source Sans 3',sans-serif;
  font-size: 13px; font-weight: 400; line-height: 1.4;
  color: #374151; border-top: 1px solid #0a0a0a;
  padding-top: 4px; margin-top: 4px;
}

/* 卡片（无装饰，竖线分栏感） */
.card {
  background: #ffffff;
  border: none; border-top: 3px solid #0a0a0a;
  border-radius: 0; padding: 10px 12px;
  display: flex; flex-direction: column; gap: 4px;
}

/* BREAKING / 速报标签 */
.breaking-tag {
  display: inline-flex; align-items: center;
  background: #dc2626; color: #ffffff;
  padding: 2px 7px; font-size: 8.5px; font-weight: 800;
  letter-spacing: 1.5px; text-transform: uppercase;
}

/* KPI / 数据要闻 */
.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 44px; font-weight: 900; line-height: 1; font-style: italic;
  color: #0a0a0a;
}
.stat-num.alert { color: #dc2626; }

/* 分栏竖线 */
.col-rule {
  width: 1px; background: rgba(0,0,0,0.15); align-self: stretch;
}

/* 时间戳 */
.timestamp {
  font-size: 8.5px; color: #6b7280; letter-spacing: 0.5px;
  font-family: 'Source Sans 3',sans-serif;
}

/* 数据条（中性灰） */
.news-bar {
  height: 3px; background: #e5e7eb;
}
.news-fill { height: 100%; background: #0a0a0a; }
.news-fill.alert { background: #dc2626; }
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #fffdf8;
  --card: #ffffff;
  --p:    #0a0a0a;
  --pm:   rgba(0,0,0,0.05);
  --bd:   rgba(0,0,0,0.12);
  --t:    #0a0a0a;
  --mt:   #374151;
  --dt:   #9ca3af;
}
/* --alert: #dc2626; (突发/警示红) */
```

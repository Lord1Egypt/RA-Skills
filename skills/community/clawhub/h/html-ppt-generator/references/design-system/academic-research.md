# 学术研究（Academic Research）

**气质：** 期刊论文、严谨理性、知识权威、学术引用
**适用：** 学术报告、研究成果、论文摘要、高校汇报
**推荐字体：** FP-2（Playfair Display + Source Sans 3）
**背景类型：** 亮色系（学术米白 #f9f8f6），接近印刷纸张感
**主标题字号：** 30–40px 衬线大标题，行距宽松，阅读感优先
**页眉形式：** 左侧期刊/机构名，右侧卷期号/DOI，底部细线，学术规范

---

## 设计特征

- **深石板蓝**（#1e3a5f / #2d5a8e）作为主强调色，严谨学术感
- 米白纸张背景，接近 Nature/Science 排版质感
- 衬线大标题 + 大量正文段落，内容密度高
- 数据图表带刻度标注，精确科学
- 引文框、注释脚注、参考文献列表风格组件

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Source+Sans+3:wght@300;400;600&display=swap');

body { background: #f9f8f6; font-family: 'Source Sans 3','Noto Sans SC',sans-serif; color: #1a1a1a; line-height: 1.6; }

/* 展示标题（期刊大标题） */
.display-title {
  font-family: 'Playfair Display','Noto Serif SC',serif;
  font-size: 36px; font-weight: 900;
  letter-spacing: -0.5px; line-height: 1.15;
  color: #1e3a5f;
}

/* 学科/方向标注 */
.discipline-label {
  font-size: 9px; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
  color: #2d5a8e; opacity: 0.8;
}

/* 卡片（学术白底，左侧蓝边） */
.card {
  background: #ffffff;
  border: 1px solid rgba(30,58,95,0.1);
  border-left: 3px solid #1e3a5f;
  border-radius: 0; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* KPI / 统计量 */
.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 40px; font-weight: 900;
  line-height: 1; color: #1e3a5f; font-style: italic;
}

/* 引文框（论文引用感） */
.citation-box {
  background: rgba(30,58,95,0.04);
  border-left: 2px solid rgba(30,58,95,0.3);
  padding: 6px 10px; font-size: 10px;
  font-style: italic; color: #374151;
  font-family: 'Playfair Display',serif;
}
.citation-box cite { font-size: 9px; color: #6b7280; font-style: normal; }

/* 研究发现列表 */
.finding-item {
  display: flex; gap: 8px; padding: 4px 0;
  border-bottom: 1px solid rgba(30,58,95,0.07);
  font-size: 10.5px;
}
.finding-num { color: #2d5a8e; font-weight: 700; font-size: 10px; width: 18px; flex-shrink: 0; }

/* 数据标注线 */
.data-rule {
  height: 1px; border: none;
  background: rgba(30,58,95,0.15); margin: 6px 0;
}

/* 统计角标 */
.stat-tag {
  display: inline-flex; align-items: center;
  background: rgba(30,58,95,0.07); border: none;
  border-radius: 2px; padding: 2px 6px;
  font-size: 8.5px; font-weight: 600; color: #1e3a5f;
  font-family: 'Source Sans 3',sans-serif; letter-spacing: 0.3px;
}
```

---

## CSS 变量（亮色覆盖）

```css
:root {
  --bg:   #f9f8f6;
  --card: #ffffff;
  --p:    #1e3a5f;
  --pm:   rgba(30,58,95,0.07);
  --bd:   rgba(30,58,95,0.1);
  --t:    #1a1a1a;
  --mt:   #374151;
  --dt:   #9ca3af;
}
```

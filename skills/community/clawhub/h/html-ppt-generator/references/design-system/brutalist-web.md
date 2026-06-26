# 粗野主义（Brutalist Web）

**气质：** 反美学、功能至上、刻意丑陋、互联网早期HTML感
**适用：** 讽刺报告、反叛创意、互联网文化批评、实验性设计
**推荐字体：** 系统字体（Times New Roman + Arial），禁止 Google Fonts
**背景类型：** 纯白（#ffffff）+ 撞色大色块，无任何渐变
**主标题字号：** 混用多种字号，故意错位，无统一规则
**页眉形式：** 完全不对齐，随机颜色背景块，故意看起来"坏了"

---

## 设计特征

- **色彩无规则**：原色（红/黄/蓝/绿）随机分配，故意冲突
- 纯色大色块做背景，完全实色无透明度
- 边框用 4–8px 实线，故意粗，故意错位
- 字体混用：标题 Times，正文 Arial，代码 Courier
- 下划线、全大写、方框、表格——所有元素堆砌

---

## CSS 片段

```css
/* 不引入任何外部字体——粗野主义用系统字体 */

body {
  background: #ffffff;
  font-family: Arial, Helvetica, sans-serif;
  color: #000000;
  margin: 0; padding: 0;
}

/* 展示标题（故意Times，故意大，故意不美） */
.display-title {
  font-family: 'Times New Roman', Times, serif;
  font-size: 64px; font-weight: 900;
  letter-spacing: -3px; line-height: 0.85;
  color: #000000;
  text-decoration: underline;
  text-underline-offset: 6px;
  text-decoration-thickness: 4px;
}
.display-title .invert {
  background: #000000; color: #ffffff;
  padding: 0 4px;
}

/* 原色撞色卡片（故意粗暴） */
.card {
  background: #ffff00; /* 故意用黄色 */
  border: 4px solid #000000;
  border-radius: 0; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 3px;
}
.card.red   { background: #ff0000; color: #ffffff; }
.card.blue  { background: #0000ff; color: #ffffff; }
.card.green { background: #00aa00; color: #ffffff; }
.card.white { background: #ffffff; }

/* KPI 数字（混用字体） */
.stat-num {
  font-family: 'Times New Roman', serif;
  font-size: 56px; font-weight: 900; line-height: 1;
  color: inherit;
  text-decoration: underline wavy;
}

/* 粗边框标签 */
.brut-tag {
  display: inline-flex; border: 3px solid #000000;
  padding: 1px 6px; background: #000000; color: #ffff00;
  font-size: 10px; font-weight: 900; letter-spacing: 1px;
  text-transform: uppercase; font-family: Arial,sans-serif;
}
.brut-tag.inv { background: #ffff00; color: #000000; }
.brut-tag.red { background: #ff0000; color: #ffffff; }

/* 粗实线进度条 */
.brut-bar {
  height: 16px; background: #ffffff;
  border: 3px solid #000000; border-radius: 0;
}
.brut-fill { height: 100%; background: #000000; }
.brut-fill.yellow { background: #ffff00; border-right: 3px solid #000; }

/* 粗暴分割线 */
.brut-rule {
  height: 4px; background: #000000; border: none; margin: 6px 0;
}
.brut-rule.red    { background: #ff0000; }
.brut-rule.yellow { background: #ffff00; border: 2px solid #000; height: 6px; }

/* 数据表格（最原始 HTML 表格感） */
.brut-table { width:100%; border-collapse:collapse; }
.brut-table th, .brut-table td {
  border: 2px solid #000000; padding: 4px 6px;
  font-family: 'Courier New',Courier,monospace;
  font-size: 10px;
}
.brut-table th { background: #000000; color: #ffffff; font-weight: 900; }
.brut-table tr:nth-child(even) td { background: #eeeeee; }

/* 文字块（故意加框） */
.brut-box {
  border: 3px double #000000;
  padding: 6px 8px; font-size: 10px;
  font-family: 'Courier New',monospace;
  background: #ffffcc;
}
```

---

## CSS 变量

```css
:root {
  --bg:   #ffffff;
  --card: #ffff00;
  --p:    #000000;
  --pm:   #eeeeee;
  --bd:   #000000;
  --t:    #000000;
  --mt:   #333333;
  --dt:   #666666;
}
/* 粗野主义没有品牌色——所有颜色都是原色 */
```

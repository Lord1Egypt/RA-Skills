# 极简文字（Editorial Minimal）

**气质：** 学术报告、克制高级、内容为王
**适用：** 概念定义、风险摘要、趋势预测、观点陈述
**推荐字体：** FP-2（Playfair Display + Source Sans 3）或 FP-4（Cormorant Garamond + Outfit）
**背景类型：** 亮色系，米白 `#fafaf8`，禁止任何纹理或光晕
**主标题字号：** 48–64px，纯色无渐变，是页面唯一视觉焦点
**页眉形式：** 一条细分隔线 + 页码，无任何装饰元素

---

## CSS 片段

```css
body { background: #fafaf8; color: #111827; }

/* 超大标题 */
.hero-title { font-size: 56px; font-weight: 900; letter-spacing: -2.5px; line-height: 0.92; color: #111827; }
.hero-accent { color: ACCENT; }   /* 单一强调色，全页仅用一次 */

/* 细分隔线 */
.divider-thin { height: 1px; background: linear-gradient(90deg, #e5e7eb, transparent); margin: 12px 0; }

/* 极简卡片（无背景色，仅左侧色条）*/
.minimal-item { border-left: 3px solid ACCENT; padding: 6px 0 6px 14px; }
.minimal-item-title { font-size: 12px; font-weight: 700; color: #111827; }
.minimal-item-body  { font-size: 11.5px; color: #6b7280; line-height: 1.5; margin-top: 3px; }

/* 大号引用块 */
.pull-quote {
  font-size: 18px; font-weight: 600; color: #111827;
  line-height: 1.4; letter-spacing: -0.3px;
  border-left: 3px solid ACCENT; padding-left: 16px;
}

/* 极简页眉 */
.hd-minimal {
  height: 72px; padding: 0 25px;
  display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid #e5e7eb;
}
.hd-minimal .report-name { font-size: 10px; color: #9ca3af; letter-spacing: 1.5px; text-transform: uppercase; }
.hd-minimal .page-num    { font-size: 10px; color: #9ca3af; font-family: monospace; }
```

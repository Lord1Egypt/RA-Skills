# Design Rules — jp-report

## Color Palette
```
--navy:  #1a2744   headings, borders, footer center text
--blue:  #003087   chapter labels, bullet markers, arch index blocks
--rule:  #c8c8c8   table borders, horizontal rules, dotted lines
--light: #f5f5f5   table zebra rows, dt backgrounds
--sub:   #4a4a4a   body text, captions, footer side text
--text:  #1a1a1a   cover title, high-emphasis values
--white: #ffffff
```
**Rules**: No bright colors. No gradients. No emoji. Navy/white is the dominant contrast.

## Typography
- Body / headings: `"Hiragino Mincho ProN", "Yu Mincho", "MS Mincho", serif` — 明朝体
- Labels / table headers / UI chrome: `"Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif` — ゴシック体
- Numbers / Latin text: `"Times New Roman", serif`

## A4 Page Sizing
| Property | Value |
|----------|-------|
| Screen width | 794px |
| Screen height | 1122px |
| Screen overflow | hidden |
| Print width | 210mm |
| Print height | 297mm |
| @page margin | 0 (all margins via padding) |
| Page body padding | 56px 70px 22px |
| Footer margin | 0 70px |
| Usable content height | ≈ 980px |

## Content Height Reference (for pagination planning)
| Element | Approx height |
|---------|--------------|
| Chapter heading (num + title) | 55px |
| Chapter rule separator (`hr.ch-rule`) | 40px |
| Paragraph, 2 lines | 50px |
| `dl.def` row | 60px |
| Table header row | 35px |
| Table data row | 35px |
| `.notice` callout box | 65px |
| `ul.bul` list item | 28px |
| `.arch` architecture row | 52px |
| Section title `.sec` (incl. margin) | 46px |

## Required CSS

Include this verbatim inside `<style>` in the HTML file:

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --navy: #1a2744; --blue: #003087; --rule: #c8c8c8;
  --light: #f5f5f5; --text: #1a1a1a; --sub: #4a4a4a; --white: #ffffff;
}
body {
  font-family: "Hiragino Mincho ProN","Yu Mincho","MS Mincho","Times New Roman",serif;
  color: var(--text); background: #c8c8c8; font-size: 13px; line-height: 1.8;
}
.page {
  width: 794px; height: 1122px; margin: 32px auto;
  background: var(--white); box-shadow: 0 4px 20px rgba(0,0,0,0.25);
  display: flex; flex-direction: column; overflow: hidden;
}
.page-body { flex: 1; padding: 56px 70px 22px; overflow: hidden; }
.page-footer {
  flex-shrink: 0; border-top: 2px solid var(--navy);
  margin: 0 70px; padding: 9px 0 15px;
  display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
  font-size: 10px; color: var(--sub);
  font-family: "Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;
}
.f-c { text-align: center; color: var(--navy); }
.f-r { text-align: right; }
@page { size: A4; margin: 0; }
@media print {
  body { background: white; }
  .page { width: 210mm; height: 297mm; margin: 0; box-shadow: none; break-after: page; }
}
.doc-badge {
  display: inline-block; font-family: "Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;
  font-size: 10px; letter-spacing: 0.16em; color: var(--sub);
  border: 1px solid var(--rule); padding: 3px 11px; margin-bottom: 60px;
}
.cover-en { font-family: "Times New Roman",serif; font-size: 12px; color: var(--sub); letter-spacing: 0.07em; margin-bottom: 10px; }
.cover-h1 {
  font-size: 27px; font-weight: normal; color: var(--navy); letter-spacing: 0.06em;
  line-height: 1.4; margin-bottom: 10px;
  border-bottom: 3px solid var(--blue); padding-bottom: 16px; display: inline-block;
}
.cover-sub { font-size: 13px; color: var(--sub); }
.cover-rule { border: none; border-top: 1px solid var(--rule); margin: 36px auto 28px; width: 60%; }
.cover-meta { border-collapse: collapse; font-size: 12px; font-family: "Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif; }
.cover-meta td { padding: 6px 0; color: var(--sub); vertical-align: top; }
.cover-meta td:first-child { white-space: nowrap; padding-right: 30px; }
.cover-meta td:last-child { color: var(--text); }
.toc-h {
  font-size: 14px; font-weight: normal; letter-spacing: 0.14em; color: var(--navy);
  border-bottom: 2px solid var(--navy); padding-bottom: 8px; margin-bottom: 30px;
  font-family: "Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;
}
.toc-ul { list-style: none; }
.toc-ul li { display: flex; align-items: baseline; padding: 7px 0; border-bottom: 1px dotted var(--rule); font-size: 13px; }
.toc-ul li:last-child { border-bottom: none; }
.toc-ul li.sub { padding: 5px 0 5px 56px; font-size: 12px; color: var(--sub); }
.t-num { font-family: "Times New Roman",serif; color: var(--blue); min-width: 56px; flex-shrink: 0; }
.toc-ul li.sub .t-num { color: var(--sub); min-width: 32px; font-size: 12px; }
.t-title { flex: 1; }
.t-dots { flex: 1 1 40px; max-width: 120px; border-bottom: 1px dotted #aaa; margin: 0 10px; position: relative; top: -3px; min-width: 30px; }
.t-pg { font-family: "Times New Roman",serif; color: var(--sub); font-size: 12px; min-width: 18px; text-align: right; flex-shrink: 0; }
.ch-num { font-family: "Times New Roman",serif; font-size: 11px; letter-spacing: 0.18em; color: var(--blue); margin-bottom: 4px; font-weight: normal; }
.ch-title { font-size: 17px; font-weight: normal; color: var(--navy); letter-spacing: 0.04em; padding-bottom: 9px; border-bottom: 1px solid var(--rule); margin-bottom: 16px; }
.ch-rule { border: none; border-top: 2px solid var(--navy); margin: 26px 0; }
.sec { font-size: 13px; font-weight: normal; color: var(--navy); letter-spacing: 0.04em; margin: 18px 0 10px; font-family: "Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif; }
.sec::before { content: "■ "; color: var(--blue); }
p { margin-bottom: 10px; color: var(--sub); font-size: 12.5px; }
dl.def { border: 1px solid var(--rule); margin-bottom: 16px; }
dl.def > div { display: grid; grid-template-columns: 185px 1fr; border-bottom: 1px solid var(--rule); }
dl.def > div:last-child { border-bottom: none; }
dl.def dt { background: var(--light); padding: 8px 12px; font-size: 12px; font-family: "Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif; color: var(--navy); font-weight: normal; border-right: 1px solid var(--rule); }
dl.def dd { padding: 8px 12px; font-size: 12px; color: var(--sub); line-height: 1.7; }
ul.bul { list-style: none; margin-bottom: 14px; }
ul.bul li { padding: 3px 0 3px 16px; position: relative; font-size: 12.5px; color: var(--sub); line-height: 1.72; }
ul.bul li::before { content: "・"; position: absolute; left: 0; color: var(--blue); }
.notice { border: 1px solid var(--navy); border-left: 4px solid var(--blue); background: #f7f9fc; padding: 11px 15px; margin-bottom: 16px; font-size: 12px; color: var(--sub); line-height: 1.7; }
.notice strong { color: var(--navy); font-weight: normal; font-family: "Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif; }
.arch { border: 1px solid var(--rule); margin-bottom: 18px; }
.arch-row { display: grid; grid-template-columns: 38px 1fr; border-bottom: 1px solid var(--rule); }
.arch-row:last-child { border-bottom: none; }
.arch-idx { background: var(--blue); color: white; display: flex; align-items: center; justify-content: center; font-family: "Times New Roman",serif; font-size: 15px; }
.arch-cell { padding: 11px 16px; }
.arch-cell strong { display: block; font-size: 12.5px; color: var(--navy); font-weight: normal; font-family: "Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif; margin-bottom: 3px; }
.arch-cell span { font-size: 11.5px; color: var(--sub); }
.arch-arrow { text-align: center; padding: 4px 0; background: var(--light); font-size: 10.5px; color: var(--sub); border-bottom: 1px solid var(--rule); font-family: "Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif; letter-spacing: 0.08em; }
table.t { width: 100%; border-collapse: collapse; margin-bottom: 16px; font-size: 12px; }
table.t th { background: var(--navy); color: white; font-weight: normal; padding: 7px 11px; text-align: left; font-family: "Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif; letter-spacing: 0.03em; }
table.t td { padding: 7px 11px; border: 1px solid var(--rule); color: var(--sub); vertical-align: top; line-height: 1.65; }
table.t tr:nth-child(even) td { background: var(--light); }
```

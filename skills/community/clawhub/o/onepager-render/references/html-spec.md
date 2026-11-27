# 一页纸 HTML 规范（全文）

`assets/onepager.html` 已内置以下全部规则；本文件用于模板缺失时手建，或改造模板时对照。

## 1. 文件与依赖

- 单文件、UTF-8、内联 CSS；除系统字体栈外**零外部依赖**（不要 CDN、不要外链 CSS/JS/字体/图片）。
- 字体栈：`"Source Han Sans SC","Noto Sans CJK SC","PingFang SC","Microsoft YaHei",sans-serif`。
- 打印必须保留背景色：`-webkit-print-color-adjust: exact; print-color-adjust: exact;`。
- 整份 HTML 建议 ≤3MB（含内嵌图片）；超出说明图片未压缩。

## 2. 页面尺寸与分页

```css
@page { size: A4; margin: 0; }
.page {
  width: 210mm; min-height: 297mm;
  padding: 13mm 13mm 17mm;
  break-after: page; page-break-after: always;
}
.page:last-of-type { break-after: auto; }
```

- 每页一个 `<section class="page">`，页间强制分页；正文页数 1–3（3 页需内容侧给出突破理由）。
- 附录页复用 `.page`：`<section class="page page--freshness">`、`<section class="page page--glossary">`。
- 屏幕预览：`body` 灰底、`.page` 白底 + 阴影 + `margin: 6mm auto`；`@media print` 下移除阴影与外边距。

## 3. 字号与行高

| 元素 | 规格 |
|---|---|
| 正文 | 10pt / line-height 1.55 |
| 最小字号 | **9pt**（任何元素不得低于此值） |
| h1（标题） | 17pt / 1.28 |
| h2（小节） | 9pt、字重 600、字间距 .08em，配下边框 |
| h3（卡片小标题） | 10pt |
| 表格 | 9.5pt |
| 时效区块 / 页脚 / 图注 | 9pt |

字号不足时不得靠缩小字号解决——删内容或升页。

## 4. 防断裂

- 卡片、图、表、区块：`break-inside: avoid;`。
- 标题：`break-after: avoid;`（防标题孤行）。
- 页脚：`position: absolute; left/right: 13mm; bottom: 7mm;`（相对 `.page`），不用 `position: fixed`。

## 5. 页面结构骨架

```html
<main>
  <section class="page">
    <header class="doc-head">
      <div class="kicker">{领域 · 主题 · 频率}</div>
      <h1>{题目，≤20 字}</h1>
      <div class="meta">{来源} · {日期}</div>
    </header>
    <div class="lead">{一句话答案/定义，≤40 字}</div>
    <h2>核心要点</h2>
    <ul class="points">…</ul>
    <h2>机制图 / 对比表</h2>
    <div class="figure">…<div class="caption">图注</div></div>
    <h2>易错点 / 边界</h2>
    <ul class="points">…</ul>
    <div class="card"><h3>一句话记忆</h3><p>…</p></div>
    <div class="freshness">…</div>   <!-- 可选，≤4 条 -->
    <div class="footer"><span>{来源}</span><span>第 1 页 / 共 N 页</span></div>
  </section>
  <!-- 第 2/3 页：不再重复大 doc-head，只放 h2 小节 -->
</main>
```

## 6. 图片（原图内嵌）

内容侧已决定保留的截图/数据图，按以下方式内嵌：

```html
<figure class="figure">
  <img src="data:image/jpeg;base64,{BASE64}" alt="{这张图回答什么问题}">
  <div class="caption">图注：这张图说明……（不写“图 1”“如上图”）</div>
</figure>
```

```css
.figure img {
  display: block;
  width: auto;
  max-width: 100%;
  height: auto;
  max-height: 70mm;   /* 1–2 页档；3 页档可用 85mm */
  border: .25mm solid var(--line);
}
.figure { break-inside: avoid; }   /* 图与图注不分离 */
```

硬性要求：

| 项 | 要求 |
|---|---|
| 内嵌方式 | `data:image/...;base64,`，禁止外链 URL |
| 体积 | 单图 ≤400KB、总计 ≤2MB、整份 HTML ≤3MB |
| alt | 必填，写这张图回答什么问题（脚本会检查缺失） |
| 图注 | 图下方 9pt 灰色；`<figure>` 整体 `break-inside: avoid` |
| 灰度 | 彩色标注必须配文字；缩到 80% 仍可分辨 |
| 格式 | 截图/照片用 JPEG（q85），带透明通道或线稿用 PNG |

**不许**用 CSS 的 `max-height` 掩盖超标大图——体积合规要在文件层完成（降采样、裁切），显示层只负责排版。

## 7. 时效区块与术语附录（样式已内置）

- 正文页内：`<div class="freshness">`，放 footer 之前，≤4 条，约 200 字符，`break-inside: avoid`。
- 超过 4 条：改附录页

```html
<section class="page page--freshness">
  <header class="doc-head">
    <div class="kicker">附录 · 不计入知识点页数</div>
    <h1>版本演进与出处</h1>
    <div class="meta">截至 {产品} {版本} 官方文档 · {YYYY-MM-DD} 核实</div>
  </header>
  <table>…</table>
  <div class="footer"><span>来源见各条</span><span>附录页</span></div>
</section>
```

- 术语附录：`page--glossary`，三列（术语 / 全称或中文 / 一句话解释），≤12 行，页脚标"附录页"。
- 两类附录页**不计入** 1–3 页知识点预算（`check_onepager.py` 按类名识别并豁免）。

## 8. 禁止项

| 禁止 | 原因 |
|---|---|
| `position: fixed` | 打印时错位 |
| `vh` / `vw` 单位 | 打印视口不可控 |
| `<details>` | 打印时内容丢失 |
| hover 才可见的内容 | 打印件没有 hover |
| 外部 `<script src>`、CDN Mermaid、外链图片 | 离线/打印会白屏白图 |
| 低于 9pt 的字号 | 打印不可读 |
| 用 CSS 缩小掩盖超大图 | 文件体积与打印质量都会失控 |

## 9. 校验命令

```bash
python scripts/check_onepager.py <file.html>
```

- 退出码 0 = 通过（允许 WARN），1 = 硬失败。
- 脚本检查：页数（1–3）、每页中文字符、最小字号、外部依赖、图/表数量、内嵌图 alt 与体积、标题撞词、时效与术语附录条数。

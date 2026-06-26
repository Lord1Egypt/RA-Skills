# HTML Components — jp-report

Use the right component for each content type. Mix and match within a page.

---

## Cover Page

```html
<div class="page-body" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">
  <div style="width:100%;">
    <div class="doc-badge">[Classification]　｜　[Doc type EN]　｜　Rev. X.X</div>
    <div class="cover-en">[Product name] — [English subtitle]</div>
    <h1 class="cover-h1">[日本語タイトル]</h1>
    <div class="cover-sub">— [日本語サブタイトル] —</div>
    <hr class="cover-rule">
    <table class="cover-meta" style="margin:0 auto;text-align:left;">
      <tr><td>[Label 1]</td><td>[Value 1]</td></tr>
      <tr><td>[Label 2]</td><td>[Value 2]</td></tr>
    </table>
  </div>
</div>
```

---

## TOC Page

```html
<div class="toc-h">目　　　次</div>
<ul class="toc-ul">
  <!-- Chapter entry -->
  <li>
    <span class="t-num">第１章</span>
    <span class="t-title">[Chapter title]</span>
    <span class="t-dots"></span>
    <span class="t-pg">3</span>
  </li>
  <!-- Sub-section entry (indented) -->
  <li class="sub">
    <span class="t-num">1.1</span>
    <span class="t-title">[Section title]</span>
    <span class="t-dots"></span>
    <span class="t-pg">3</span>
  </li>
</ul>
```

---

## Chapter Opening

```html
<div class="ch-num">第X章</div>
<h2 class="ch-title">[Chapter title]</h2>
<p>[Introductory sentence in keigo.]</p>
```

For two chapters on the same page, separate with:
```html
<hr class="ch-rule">
```

---

## Section Title

```html
<div class="sec">X.Y　[Section title]</div>
```

---

## Definition List — for principles, glossaries, key concepts

```html
<dl class="def">
  <div>
    <dt>[Term]</dt>
    <dd>[Full sentence explanation in keigo. 〜しております。]</dd>
  </div>
  <div>
    <dt>[Term 2]</dt>
    <dd>[Explanation.]</dd>
  </div>
</dl>
```

---

## Data Table — for feature lists, spec tables, access control matrices

```html
<table class="t">
  <thead>
    <tr>
      <th style="width:185px">[Column 1]</th>
      <th>[Column 2]</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>[Item]</td><td>[Description in keigo.]</td></tr>
    <tr><td>[Item]</td><td>[Description in keigo.]</td></tr>
  </tbody>
</table>
```

---

## Architecture Stack — for layered system diagrams

```html
<div class="arch">
  <div class="arch-row">
    <div class="arch-idx">Ⅱ</div>
    <div class="arch-cell">
      <strong>[Upper layer name]</strong>
      <span>[Feature 1]　／　[Feature 2]　／　[Feature 3]</span>
    </div>
  </div>
  <div class="arch-arrow">↑　[Relationship description]　↑</div>
  <div class="arch-row">
    <div class="arch-idx">Ⅰ</div>
    <div class="arch-cell">
      <strong>[Lower layer name]</strong>
      <span>[Feature 1]　／　[Feature 2]　／　[Feature 3]</span>
    </div>
  </div>
</div>
```

---

## Notice / Callout Box — for key principles, references, warnings

```html
<div class="notice">
  <strong>【Label】</strong>　[Explanation text in keigo.]
</div>
```

---

## Bullet List — for enumerated items without a table structure

```html
<ul class="bul">
  <li>[Item in full keigo sentence.]</li>
  <li>[Item.]</li>
</ul>
```

---

## Page Footer (required on every page)

```html
<div class="page-footer">
  <div class="f-l">[Product / Company name]</div>
  <div class="f-c">[Document title]　Rev. X.X</div>
  <div class="f-r">[Classification]　｜　[Page number]</div>
</div>
```

Cover and TOC pages omit the page number (just `[Classification]`).
Body pages show `社外秘　｜　3`, `社外秘　｜　4`, etc.

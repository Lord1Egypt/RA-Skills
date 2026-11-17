# Optional animations

默认不做过程动画。只有用户明确说「要演示 / 能重放 / 像原 PPT 那样动」时才用这一页。

## Contract

模板已经提供：

- `// ANIMATIONS_START` / `// ANIMATIONS_END` 是唯一允许写动画函数的插槽
- `data-anim="name"` 写在 `<section class="slide">`
- `anims.name = async (token) => { ... }`
- `token.stop` 为 true 时立刻 return
- `type` / `typeHTML` / `logLine` / `renderTree` / `sleep`
- 按钮：`<button class="btn" data-replay="name">↻ 重放</button>`
- 快捷键 `R` 重放当前页

**不准为了动画改 CSS 或其它 runtime。** 只在动画插槽写函数，只切换原有 class：`.on` / `.lit` / `.read` / `.new` / `.upd` / `.go`。

## Recipe A · 依次点亮

适合 chip、pcard、steps。

```html
<section class="slide" data-anim="reveal" data-title="点亮">
```

```js
anims.reveal = async (tk) => {
  const ids = ['p1', 'p2', 'p3'];
  ids.forEach((i) => $('#' + i).classList.remove('on'));
  for (const i of ids) {
    await sleep(700);
    if (tk.stop) return;
    $('#' + i).classList.add('on');
  }
};
```

## Recipe B · 终端打字

适合 L3。把正文放到空的 `#term-body`，用 `typeHTML` 写入。

```js
anims.term = async (tk) => {
  await typeHTML($('#term-body'), [
    { t: '标题', c: 'h1' },
    { t: '', c: 'hr' },
    { t: '普通句子 ' },
    { t: '链接词', c: 'lk' },
    { t: '\n—— 注释', c: 'cm' },
  ], tk, 22);
};
```

## Recipe C · 树图 + 日志

适合「一层层翻目录」。先在页面放 `<svg class="tree" id="qtree">` 和 `.log`，再用 `renderTree` + `logLine`。节点状态只准用 `lit` / `read` / `new` / `upd`。

## Hard rules

- 一页最多一个 `data-anim`。
- 动画失败时内容必须已经在 HTML 里可见，不能只靠 JS 写入关键结论。
- 不要引入 Motion / GSAP / WebGL。
- 做完仍须通过 `python scripts/validate_deck.py`。

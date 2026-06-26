# Bug：录屏模式下输出内容为空

**日期**：2026-03-14  
**影响版本**：scrape.js v6  
**严重程度**：高（录屏模式完全无法输出内容）

---

## 现象

使用 `--record` 参数启动录屏模式时，脚本能正常运行、正常等待 Grok 回复（日志显示 `[replying]` 阶段内容持续增长），但最终输出：

```
╔══════════════════════════════════════════╗
║  ❌ FAILED — Reply too short              ║
║  Length: 0 chars (min: 100)        ║
║  Forced: false                         ║
╚══════════════════════════════════════════╝

--- Raw new content ---

Grok updates
快速回答
自动
```

`newContent` 只有几个 UI 噪声字符串，完全没有 Grok 的实际回复内容。而同样的 prompt 在不加 `--record` 的无头模式下正常运行。

---

## 根本原因（两个独立 Bug）

### Bug 1：`getNewContent` 降级路径截取位置错误

`getNewContent(beforeText, afterText)` 负责从"发送后的完整页面文本"中减去"发送前的页面文本"，得到新增内容。

逻辑分两步：
1. **精确前缀匹配**：如果 `afterText` 以 `beforeText` 的前 200 个字符开头，则直接切片。
2. **降级路径**：前缀匹配失败时，走 `afterText.slice(beforeText.length - 100)`。

**问题出在降级路径**。原代码：

```js
// 退路：直接返回 afterText 尾部
if (afterText.length > beforeText.length) {
  return afterText.slice(beforeText.length - 100).trim();
}
```

`beforeText.length - 100` 实际上是从 `beforeText` 末尾往前 100 个字符的位置开始截取，**包含了原来 beforeText 末尾的部分内容**，而不是从真正的新增内容起点开始。

**为什么录屏模式会触发降级路径？**  
录屏模式下浏览器以有界面模式（`headless: false`）运行，页面渲染时可能存在额外 UI 元素（工具栏、窗口装饰层等），导致 `document.body.innerText` 的内容结构与无头模式不同。发送前的 `beforeText`（80 字符）的前 200 字符前缀在 `afterText` 里找不到完全匹配，精确前缀匹配失败，进入降级路径，截取到了错误的内容片段（恰好是 UI 噪声字符串 "Grok updates\n快速回答\n自动"）。

---

### Bug 2：`page.video()?.path()` 在 `context.close()` 之后调用

原代码顺序：

```js
await context.close();   // ← 先关闭 context
if (recordTarget !== null) {
  const tmpPath = await page.video()?.path();  // ← 再取视频路径（不可靠）
  ...
}
```

Playwright 要求在 context 关闭**之前**调用 `page.video()` 来获取临时视频文件路径，关闭后该对象的状态不可保证。虽然此 Bug 在本次复现中视频文件实际上保存成功了，但属于时序错误，存在隐患。

---

## 修复方案

### 修复 1：改进 `getNewContent` 降级逻辑

用"在 `afterText` 中定位 `beforeText` 末尾 80 字符"的方式精准找到新增内容起点：

```js
// 修复前（错误）
return afterText.slice(beforeText.length - 100).trim();

// 修复后（正确）
const tailLen = Math.min(beforeText.length, 80);
const tail = beforeText.slice(-tailLen);
const tailIdx = afterText.lastIndexOf(tail);
if (tailIdx !== -1) {
  return afterText.slice(tailIdx + tailLen).trim();
}
// 最后降级：按长度差截取
return afterText.slice(beforeText.length).trim();
```

### 修复 2：在 `context.close()` 之前获取视频路径

```js
// 修复前（错误时序）
await context.close();
const tmpPath = await page.video()?.path();

// 修复后（正确时序）
const videoPendingPath = recordTarget !== null ? await page.video()?.path() : null;
await context.close();
// 之后再用 videoPendingPath 做文件重命名
```

---

## 经验总结

1. **有界面模式 vs 无头模式的 DOM 差异**：`headless: false` 时浏览器可能渲染额外 UI 层，影响 `document.body.innerText` 的内容，不能假设两种模式下页面文本结构完全一致。

2. **降级路径要用"尾部锚定"而非"长度偏移"**：当不能保证前缀完全匹配时，应在目标字符串中搜索已知片段的位置，再从该位置之后截取，而不是直接用 `length` 偏移，后者在有额外插入内容时会错位。

3. **Playwright 资源获取要在生命周期结束前完成**：`page.video()`、`page.screenshot()` 等依赖页面对象的 API，必须在 `context.close()` 之前调用，否则行为不可靠。

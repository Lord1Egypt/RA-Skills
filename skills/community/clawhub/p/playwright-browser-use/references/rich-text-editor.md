# SPA 与富文本编辑器 ⚠️

> ⚠️ **破坏性操作警告：** 以下操作会真实修改网页内容（知识库文档、CMS 页面等）。执行前确认：① 处于编辑/草稿状态而非已发布内容；② 修改内容已经用户确认；③ 保存/发布操作不可逆。

处理知识库、文档系统、CMS（如 Notion/语雀/飞书类页面）中的 SPA 编辑态和富文本编辑器写入。

## 何时使用

满足**任一条件**时，遵循本指南：

- URL/页面属于知识库、文档、笔记、CMS 类站点
- 任务要求创建/编辑/保存文档正文
- 点击"编辑"按钮后 URL 不变但页面状态变化
- snap 中出现 `contenteditable`、编辑器 toolbar、"插入"/"正文"等
- 表单不是普通 input/textarea，而是复杂编辑器

## 核心原则

- **不要**直接用 `innerText`/`textContent` 写 RTE——不会被编辑器状态机接受
- 先确认进入编辑态，再用 Playwright 键盘输入
- 保存后验证内容而不是只看按钮状态

## 流程

### 1. 进入编辑态

```bash
# 先 snap 找到编辑按钮
pw-browser snap

# 点击编辑按钮
pw-browser click <编辑ref>

# 验证进入编辑态
pw-browser run-code "
  return await page.evaluate(() => ({
    hasUpdate: Array.from(document.querySelectorAll('button'))
      .some(b => b.textContent.trim() === '更新'),
    editableCount: document.querySelectorAll('[contenteditable]').length
  }));
"
```

如果 `hasUpdate=true` 或 `editableCount > 0`，继续；否则尝试重试点击。

### 2. 写入内容（RTE）

```bash
pw-browser run-code "
  const editor = page.locator('[contenteditable=\"true\"], [contenteditable=\"plaintext-only\"]').first();
  await editor.click();
  await page.keyboard.press('Control+A');
  await page.keyboard.type('要写入的文本内容');
  await page.waitForTimeout(1000);
  const text = await editor.textContent();
  return text;
"
```

### 3. 保存 ⚠️

> ⚠️ 保存/发布操作不可逆，确认内容无误后再执行。

```bash
pw-browser run-code "
  await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button'))
      .find(b => ['更新','保存','发布','完成'].includes(b.textContent.trim()));
    btn?.click();
  });
  await page.waitForTimeout(3000);
"
```

### 4. 验证

```bash
pw-browser run-code "
  const title = document.querySelector('h1, [class*=title]')?.textContent || document.title;
  const main = document.querySelector('main') || document.body;
  const blocks = Array.from(main.querySelectorAll('p, h1, h2, h3, li'))
    .map(b => b.textContent.trim().slice(0, 80))
    .filter(Boolean);
  return JSON.stringify({ title, sampleBlocks: blocks.slice(0, 10) });
"
```

成功标准：
- `hasUpdate=false`（编辑态已退出）
- 正文包含目标文本
- 标题未被误改或清空
- 没有重复写入的文本

## 弹窗处理

- DOM 浮层（弹窗、抽屉、popover）：通过 snap 识别并 click 关闭按钮
- 原生 JS dialog（alert/confirm/prompt）：用 `pw-browser dialog-accept` / `dialog-dismiss`

## 失败处理

- 点击"编辑"超时后，先检查是否已进入编辑态，不要重复点击
- 后续命令超时，执行 `pw-browser recover` 恢复 daemon
- 恢复后如果已在编辑态，继续输入和保存

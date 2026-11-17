# GPT 审稿踩坑记录

通过实际使用积累的问题和解决方案。

## 2026-06-11 首次成功使用

### 问题1：`/json/new` 返回 405

**现象**：CDP 的 `/json/new?url=...` 接口返回 `HTTP Error 405: Method Not Allowed`，无法通过 HTTP API 打开新标签页。

**解决**：用系统命令 `open -a "Brave Browser" "https://chatgpt.com"` 替代，然后等待 8 秒再查找新标签。

### 问题2：ProseMirror 编辑器文本注入

**现象**：ChatGPT 使用 ProseMirror 富文本编辑器（`#prompt-textarea`），直接设置 `innerHTML` 会触发 JS 语法错误。

**解决**：使用 `document.execCommand('insertText', false, text)` 注入。先 `selectAll` + `delete` 清空，再 `insertText`。

**限制**：`insertText` 似乎对超长文本（>2000 字符）有限制。如果 prompt 很长，考虑拆分或精简。

### 问题3：发送按钮选择器

**现象**：ChatGPT 的发送按钮选择器不稳定，`data-testid="send-button"` 不一定存在。

**解决**：多重回退策略：先尝试 `data-testid`，再尝试 `aria-label`，最后遍历所有 button 找带 SVG 且在 form 内的。

### 问题4：等待回复的时机判断

**现象**：不知道 ChatGPT 什么时候生成完。轮询太快浪费资源，太慢浪费时间。

**解决**：使用"长度稳定性检测"——连续 3 次检测（每次间隔 5 秒）响应长度不变且超过 100 字符，判定为生成完成。

### 问题5：长响应提取被截断

**现象**：CDP `Runtime.evaluate` 返回值有长度限制，一次性提取 5000+ 字符的响应会被截断。

**解决**：分块提取，每次 4000 字符，用 `substring(offset, end)` 拼接。

### 问题6：ChatGPT 回复空消息

**现象**：有时 ChatGPT（特别是 GPT-5 thinking 模式）会返回空消息或只有开头几句话。

**解决**：增加等待时间，使用更稳定的长度检测。如果仍有问题，换用非 thinking 模式的 ChatGPT 标签页。

### 问题7：分批注入长文本 ✅ 已解决（2026-06-11）

**现象**：`insertText` 对超过 1500 字符的文本会截断。第一次测试时 6875 字节的 prompt 只注入了 2559 字符。

**解决**：`gpt_review.py` 添加了分块注入逻辑，每块 1500 字符，循环注入并用小间隔（0.3s）让编辑器稳定。

**验证**：2914 字符的 prompt 成功分 2 块注入，编辑器最终显示 2801 字符，基本完整。

### 问题8：ChatGPT 返回极短内容后判定"稳定"

**现象**：ChatGPT 在 thinking 模式下的首个 token 很短（如"先"字），脚本检测到长度不再变化后过早判定完成。

**解决**：稳定性检测的最低长度阈值从 100 降到 0（解决短响应场景），同时增加 check_interval 时间保证不提前判定。更好的做法：加一个"最小等待时间"（如 15 秒），避免 thinking 模式的首个 token 让脚本误判。

### 问题9：GPT 提取的长响应需要分块

**现象**：CDP `Runtime.evaluate` 返回有长度限制，一次提取 8000+ 字符的回复会被截断。

**解决**：每 4000 字符分块，用 `substring(offset, end)` 拼接。实测 8090 字符成功提取完整（3 块）。

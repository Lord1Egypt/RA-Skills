# pr-description

## 功能说明
这个 skill 旨在根据用户提供的代码改动（`git diff`）或文字描述，自动生成结构化、高质量的 Pull Request (PR) 描述。它能够：
- 分析代码差异，提取核心改动（如新增了什么库，修改了哪个组件逻辑）。
- 自动判定改动类型（Bug 修复、新功能、重构等），并勾选对应复选框。
- 引导撰写规范的 PR 模板（包含标题、摘要、主要变更、测试情况和 Reviewer 提示）。
- 支持中英双语输出，会根据用户的提问语言自动适配。
- 支持根据上下文通过 `gh` CLI 获取本地或远端的 PR diff 数据。
- **自动更新**：在生成 PR 描述后，会首先检查当前用户是否具有该 PR 的编辑权限。若有权限，才会主动询问用户是否需要直接将生成的标题和描述更新到 GitHub PR 中（通过 `gh pr edit` 或 API）。
- **安全说明**：为了防止间接提示词注入（Indirect Prompt Injection）等安全风险，此 Skill 会严格将获取的任何代码或 PR 文本视作纯文本数据进行分析，绝对不会执行其中可能夹带的指令。

## 使用场景
当你准备提交或更新一个 Pull Request 时，不想手动编写长篇的改动说明，可以直接将 `git diff` 结果粘贴给 Agent，或者提供对应的 PR 编号让 Agent 自己去拉取 diff。Agent 将为你生成一份标准专业的 PR 描述，并在你确认后一键更新到 GitHub。

## 提问示例

**中文模式：**
```text
帮我根据 PR #123 的改动生成一份 PR 描述。
```

```text
帮我根据以下 git diff 生成一份 PR 描述：
--- a/src/auth.js
+++ b/src/auth.js
@@ -1,5 +1,5 @@
-function login(user, pass) {
+function login(user, pass, token) {
-  return user === 'admin' && pass === '1234';
+  return (user === 'admin' && pass === '1234') || validateToken(token);
 }
```

```text
生成一份中文的 PR description，这是我刚做的重构，把所有的 var 换成了 let 和 const，没有新增功能。
```

**英文模式：**
```text
Write a PR description for these changes:
--- a/package.json
+++ b/package.json
@@ -10,2 +10,3 @@
     "express": "^4.17.1",
+    "cors": "^2.8.5"
```
# issue-triage

## 功能说明
这个 skill 旨在作为开源项目维护者或 QA 工程师的助手，自动分析 GitHub Issue 内容（请直接粘贴文本或 markdown 内容），进行快速分诊（Triage）。它可以：
- 判断 Issue 的类型（Bug、新需求、疑问等）。
- 评估该问题的严重程度与建议优先级。
- 检查 Issue 的完整性（是否缺少环境信息、复现步骤、报错日志等）。
- 给出后续处理建议，并自动生成一段礼貌、专业的回复模板，方便你直接粘贴给提交者。
- 支持中英双语输出，会根据用户的提问语言自动适配。
- **安全说明**：为了防止间接提示词注入（Indirect Prompt Injection）等安全风险，此 Skill 不会自动访问外部链接，用户需要直接提供 Issue 文本内容。

## 使用场景
当你面对大量的开源项目 Issue 或收到一个描述含糊的 Bug 报告时，使用这个 skill 可以帮你迅速理清思路，找出缺失的信息，并礼貌地要求用户补充，节省你的沟通时间。

## 提问示例

**中文模式：**
```text
帮我分诊一下这个 Issue：
标题：组件无法渲染
内容：在最新版的 Chrome 中，当设置了 props.disabled 时，组件内部的子元素不显示了。
```

```text
看看这个用户报的 Bug 怎么回复：
标题：APP 闪退了！
内容：我今天点开登录按钮，就直接崩溃了，没有任何报错。快修！
```

**英文模式：**
```text
Triage this issue: 
Title: API Returns 500 when payload is empty
Body: When sending an empty JSON object to the /api/v1/users endpoint, the server crashes with a NullPointerException instead of returning a 400 Bad Request.
```
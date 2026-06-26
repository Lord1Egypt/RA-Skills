**当检测到内容润色时，应用以下原则：**

### 1. 何时调用 blog-rewriter
**触发条件：**
- 当核心工作流进入到第8步时，开始触发处理
- 润色去除文中AI味道步骤后，执行润色

**调用方式：**
```
读取：~/.openclaw/workspace/skills/blog-rewriter/SKILL.md
应用：核心原则（对文章进行润色、排版）
```

### 2. 何时调用 chinese-writing-polish
**触发条件：**
- 当完成了调用 blog-rewriter调用后，继续对文案进行优化处理

**调用方式：**
```
读取：~/.openclaw/workspace/skills/chinese-writing-polish/SKILL.md
应用：核心原则（去除文本中的 AI 生成痕迹,审阅 AI 生成内容、优化写作风格、让文字不那么像机器生成的）
```
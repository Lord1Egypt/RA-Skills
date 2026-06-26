**当检测到去除AI味时，应用以下原则：**

### 1. 何时调用 ai-humanizer技能
**触发条件：**
- 当核心工作流进入到第7步时，开始触发处理
- 洗稿完成后仍感觉AI味任然不是"无菌"

**调用方式：**
```
读取：~/.openclaw/workspace/skills/ai-humanizer/SKILL.md
应用：核心原则（AI生成的文本更具人性化。重写文本使其听起来自然、具体且有人情味）
```

### 2. 何时调用 humanizer-zh技能
**触发条件：**
- 当完成了调用 ai-humanizer调用后，仍需要去除AI味调用
- 创意写作领域且基础改写后仍感觉"无菌"

**调用方式：**

```
读取：~/.openclaw/workspace/skills/humanizer-zh/SKILL.md
应用：核心原则（去除文本中的 AI 生成痕迹,审阅 AI 生成内容、优化写作风格、让文字不那么像机器生成的）
```
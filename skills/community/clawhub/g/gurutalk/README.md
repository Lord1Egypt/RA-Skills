<div align="center">

# 大师云 (GuruTalk)

你的大師朋友圈

> *"如果能随时让 Elon Musk 为你的系统设计做优化，让 Charlie Munger 为你的商业决策做「反向思考」排雷，世界会怎样？"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Powered By: Bibliotalk](https://img.shields.io/badge/API-Bibliotalk-blue.svg)](#)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

超越时空的导师天团！将古往今来的顶级思想家、企业家、灵性导师等大师的思想记录蒸馏为**智能体忆库和对话技能**，让**马斯克、乔布斯、纳瓦尔、芒格、富兰克林、曾国藩、南怀瑾**加入你的私人导师团队，进入**言必有据**的对话系统！

</div>

---

## 🚀 核心原则：**言必有据**

现在有很多“角色扮演”或“人格蒸馏”的 AI 智能体，我们的不同在于：**忠实引用本人原话**。

当大师给你建议时：
1. **扎根于本人的思维模型**：不仅语气到位，更是基于其核心认知（如 Musk 的第一性原理，Naval 的杠杆原理）。
2. **充分引用原始语料**：任何一句有价值的建议，系统都将提供`[引用标记]`和<ins>`引用链接`</ins>，点击链接即可查看书籍、演讲、播客、帖子等资料的原始片段。

---

## ⚡ 快速体验: 《The Book of Elon 埃隆之书》

> 🚨 首发爆款：我们利用 Eric Jorgenson 刚发布的五万字巨作《**The Book of Elon 埃隆之书**》，配合其经典推文，为你蒸馏出了首个硬核赛博导师 —— **/elon-musk**。

**当你在设计一个复杂的分布式系统架构时：**

`❯ /elon-musk 我在设计一个高并发 AI API 平台：前面是 API Gateway，后面有用户服务、计费服务、模型路由服务，还有 Kafka、Redis、向量数据库和多个微服务。你觉得这个架构合理吗？`

"Elon Musk" Agent:

⦿ 回到第一性原理：**系统存在的唯一目的，是把用户请求转换为结果**。如果你的系统需要 12 个服务才能完成一次推理请求，那说明设计已经偏离了目标。

工程学有五个步骤，而你应该从第二步开始反复执行：  
**Delete the part or process.** [1]

先尝试删除：
- 独立的模型路由服务（合并到 API 层）
- 不必要的消息队列
- 为“未来规模”准备的过度拆分微服务

如果删掉之后系统还能跑，那它们本来就不该存在。  
一个优秀的系统架构通常**比你最初设计的版本简单 50% 以上**。[1]

- [1]: [*The Book of Elon, Chapter 2*: "If you're not adding things back 10% of the time, you're clearly not deleting enough."](https://bibliotalk.space/q/JnS9Pg)

---

## 💻 安装与使用

### 针对 OpenClaw / Claude Code 用户

我们的架构已全面云 端化，现在安装极度轻巧（无需配置 Python 爬虫和复杂依赖）！

1. **Clone 到你的技能目录**  
   OpenClaw:
   ```bash
   git clone https://github.com/casterkay/gurutalk ~/.openclaw/workspace/skills/gurutalk
   ```
   Claude Code:
   ```bash
   git clone https://github.com/casterkay/gurutalk ~/.claude/skills/gurutalk
   ```
   Codex:
   ```bash
   git clone https://github.com/casterkay/gurutalk ~/.codex/skills/gurutalk
   ```
2. **调用大师云技能**  
   OpenClaw:
   ```
   /skill gurutalk 有哪些上线的大师？
   ```
   Claude Code:
   ```
   /gurutalk 有哪些上线的大师？
   ```
   Codex:
   ```
   $gurutalk 有哪些上线的大师？
   ```
   （接下来仅以 Claude Code 的输入格式为例说明后续步骤）
3. **首次调用时按提示完成初始化**  
   如果还没有设置 API 密钥，Agent 会在对话里引导你完成登录和凭据写入。
4. **招募大师到本地**  
   ```
   /gurutalk 招募 Elon Musk
   ```
5. **向大师提问**  
   ```
   /elon-musk 你觉得我的系统架构合理吗？
   ```
6. **继续追问或结束当前人物对话**  
   后续消息默认继续发送给当前人物，不需要重复输入 `/{figure}`。当你想切换人物时，直接发送另一个 `/{figure} {message}`；当你想退出模拟人物对话时，发送：
   ```
   /gurutalk end
   ```

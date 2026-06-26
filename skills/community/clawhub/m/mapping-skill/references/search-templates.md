# Search Query Templates

## PhD Student Search Templates

### By Research Direction

```
"{research_direction}" PhD student site:github.io OR site:stanford.edu OR site:berkeley.edu OR site:mit.edu
```

```
"{research_direction}" PhD researcher personal homepage
```

```
"{research_direction}" "PhD student" site:linkedin.com/in
```

### By Lab/University

```
"{lab_name}" PhD student site:{university_domain}
```

```
site:{lab_domain} PhD student "{research_direction}"
```

### Chinese Researcher Search

```
{research_direction_cn} 博士生 清华 OR 北大 OR 上海交大 个人主页
```

```
{research_direction_cn} PhD 中国 site:github.io
```

## Research Direction Keywords

### Large Language Model Pre-training

**English Keywords:**
- "large language model pre-training"
- "LLM pre-training"
- "foundation model training"
- "language model scaling"
- "efficient pre-training"
- "data mixing for LLM"
- "training dynamics"

**Chinese Keywords:**
- 大模型预训练
- 大语言模型训练
- 基础模型
- 预训练技术

### Embodied AI / Robotics

**English Keywords:**
- "embodied AI"
- "robot learning"
- "manipulation learning"
- "humanoid robot"
- "dexterous manipulation"
- "sim-to-real transfer"
- "robot foundation model"

**Chinese Keywords:**
- 具身智能
- 机器人学习
- 灵巧操作
- 人形机器人

### Multimodal Learning

**English Keywords:**
- "vision language model"
- "multimodal learning"
- "VLM pre-training"
- "image-text alignment"
- "multimodal foundation model"

**Chinese Keywords:**
- 多模态学习
- 视觉语言模型
- 跨模态预训练

### AI Agents

**English Keywords:**
- "LLM agent"
- "autonomous agent"
- "tool learning"
- "agent planning"
- "multi-agent system"

**Chinese Keywords:**
- 智能体
- AI Agent
- 工具学习

### Reinforcement Learning

**English Keywords:**
- "reinforcement learning"
- "RLHF"
- "reward modeling"
- "policy optimization"
- "offline RL"

**Chinese Keywords:**
- 强化学习
- 人类反馈强化学习
- 奖励建模

## URL Quality Filters

### High-Quality Domains (Priority)

Personal pages:
- `*.github.io`
- `sites.google.com`
- Personal university pages (`~username`)

University domains:
- `stanford.edu`
- `berkeley.edu`
- `mit.edu`
- `cmu.edu`
- `princeton.edu`
- `tsinghua.edu.cn`
- `pku.edu.cn`

Professional networks:
- `linkedin.com/in/`
- `scholar.google.com/citations`

### Domains to Exclude

- News articles (techcrunch, wired, etc.)
- Course pages without researcher info
- Generic department pages
- Job posting sites

# NPC Distill 🎯

> 把零散的语料蒸馏成可演练的 npc,辅助汇报前的预演。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skill Standard](https://img.shields.io/badge/agentskills.io-compatible-blue)](https://agentskills.io)

---

## 这是什么

**这是一个专门用来"蒸馏 npc"的 Skill。**

所谓 npc,就是你工作里绕不开、又需要反复揣摩的那个人——直属上级、合作方、关键客户。
本 Skill 让 AI Agent 帮你把零散语料(聊天记录、邮件、会议纪要)**蒸馏**成一个可演练的 npc,
用于在向真人沟通前做预演。一句话:**输入语料,产出一个能陪你过招的 npc。**

**应用场景**:
- 🎯 **压力测试方案**:模拟 NPC 挑刺,提前发现弱点
- 🎭 **演练汇报**:多轮对话演练,熟悉对方的反应模式
- ✍️ **风格化起草**:写出符合对方偏好的材料,降低被打回概率
- 📊 **决策预判**:重要节点前模拟"他会怎么想这件事"

**核心特点**:
- ✅ **数据全本地**:所有内容存在 `~/npc-distill/memory-*.md`,**不联网,不上传**
- ✅ **代号匿名化**:文件中只用 L001/L002 代号,不存真名
- ✅ **跨宿主兼容**:同一份 Skill 可在 Claude / Hermes / LobsterAI / OpenClaw 等 Agent 中使用
- ✅ **单文件存储**:一人一个 `.md`,纯 Markdown,任何编辑器都能开
- ✅ **MIT 开源**:代码完全透明,可审计可定制

---

## 安装

### 选项 A: Claude.ai / Claude Code

```bash
# Claude Code
git clone https://github.com/bangbangmao666666/npc-distill ~/.claude/skills/npc-distill
cd ~/.claude/skills/npc-distill
pip install -r scripts/requirements.txt
```

Claude.ai 网页版:打开 Settings → Skills → Upload,选择本目录打包的 zip。

### 选项 B: Hermes Agent

```bash
git clone https://github.com/bangbangmao666666/npc-distill ~/.hermes/skills/npc-distill
cd ~/.hermes/skills/npc-distill  
pip install -r scripts/requirements.txt
```

### 选项 C: LobsterAI (有道龙虾) / OpenClaw

```bash
git clone https://github.com/bangbangmao666666/npc-distill ~/.openclaw/skills/npc-distill
# 在 LobsterAI 设置中导入此目录
pip install -r scripts/requirements.txt
```

详细兼容性表见 [`references/agentskills-compat.md`](references/agentskills-compat.md)。

---

## 快速上手

### 第一次使用 (3 分钟)

打开你的 Agent,直接说:

> "我想蒸馏一个 npc。"

Skill 会引导你:
1. 选择 memory 文件位置(默认 `~/npc-distill/`)
2. 给目标人物起一个代号(如 `L001`)
3. 选择关系(直属上级/合作伙伴/客户/其他)

然后立刻可以开始投喂语料。

### 投喂第一条语料

直接粘贴聊天记录、邮件片段或会议纪要:

> "把这段会议纪要中老板的发言喂进去:
> 
> [粘贴文本]"

Skill 会:
1. 询问哪些发言是目标人物说的
2. 抽取信号(质询主题、风格信号、雷区等)
3. **展示完整 diff** 让你确认
4. 确认后写入 `memory-L001.md`

### 第一次压力测试

下周有汇报,先过一遍:

> "我下周要做 Q3 复盘,材料如下:[粘贴方案]
> 
> 帮我做压力测试。"

输出包括:
- 5 个最可能的尖锐提问(每个带证据引用)
- 雷区扫描(方案中哪些表达会踩雷)
- 通关检查清单

完整工作流见 [`templates/`](templates/) 目录。

---

## memory 文件长什么样

打开 `examples/memory-L001-demo.md` 看一个真实示例。结构非常直白:

```markdown
---
npc_id: L001
evidence_count: 32
confidence: high
decision_axes:
  data_vs_intuition: 0.72
  ...
frequent_challenges:
  - theme: ROI测算依据
    weight: 0.85
    evidence: [C-20250312-001, C-20250418-003]
  ...
redlines:
  - 避免"大概""可能"等模糊词
  ...
---

# L001 画像综述

[人类可读的画像描述...]

---

# 语料库

## C-20260201-007 · Q4复盘会
[语料1详细内容]

## C-20251128-002 · 战略会
[语料2详细内容]
```

**一个文件,搞定一个人的全部画像与语料。**
可以放在 iCloud / Dropbox / 坚果云,跨设备同步零成本。

---

## 隐私设计

### 我们做了什么

1. **代号化**:所有文件名、引用都用 `L001`/`L002`,**永远不写真名**
2. **完全本地**:Skill 不联网,不调用任何外部 API,不上传你的 memory
3. **可审计**:全部代码 < 1000 行 Python + Markdown,自己可以一行行看
4. **明文存储**:不加密,因为加密带来的复杂性 > 实际防护价值(如果设备被入侵,加密也保护不了)。建议把整个目录放到加密磁盘(macOS FileVault / Windows BitLocker / Linux LUKS)

### 我们没做的

- ❌ 没有云同步、云备份功能
- ❌ 没有用户系统、不需要注册
- ❌ 没有调用任何 LLM API(那是宿主 Agent 做的事)
- ❌ 没有"自动从网络补全画像"的功能

### 你应该做的

1. **不要把 memory 文件提交到公共仓库**——`.gitignore` 已默认排除 `memory-*.md`
2. **不要在团队共享盘里存**——这是个人工具
3. **不要把真名映射表写在任何文件里**——只在自己脑子里记"L001 = 谁"
4. **必要时启用磁盘加密**——这是比应用层加密更可靠的方案
5. **如果设备共享**——把 `~/npc-distill/` 单独放在一个加密容器里

---

## 边界声明

本工具:

**✅ 可以做的**
- 帮你梳理对方的关注点,降低汇报翻车概率
- 识别你表达中的雷区
- 辅助你写更对胃口的材料
- 提供"如果是他会怎么想"的视角参考

**❌ 不能做的**
- 预测具体决策结果("他会不会同意我的方案?")
- 生成署他人名的对外内容
- 替代真实的人际沟通和信任建立
- 100% 还原一个真实人物——AI 模拟有偏差

任何预演输出末尾都会附:

> ⚠️ 以上为基于历史语料的 AI 模拟,代号 L00X,不代表当事人真实意见。

请你也始终保持这份清醒。

---

## 伦理使用建议

这个工具天然涉及对他人的"建模",有伦理风险。建议:

1. **告知与同意**:如果可能,告诉被分析的人你在用这个工具帮自己沟通——大多数 NPC 会觉得你"用心",而不是"算计"
2. **限于自用**:画像数据是私人工具,不要拿去做政治操作、八卦传播
3. **承认局限**:画像里所有结论都是统计倾向,不是必然预测
4. **定期清理**:关系结束后(离职、合作终止),删除对应 memory 文件

---

## 文件结构

```
npc-distill/
├── SKILL.md                        # 主入口,Agent 读取的核心指令
├── README.md                       # 本文件
├── LICENSE                         # MIT
├── .gitignore                      # 默认排除 memory-*.md
│
├── templates/                      # 5 个工作流模板
│   ├── ingest-text.md              # 文本投喂
│   ├── ingest-url.md               # URL 投喂
│   ├── rehearse-pressure.md        # 压力测试
│   ├── rehearse-dialogue.md        # 对话演练
│   └── draft-with-critique.md      # 起草+批判
│
├── scripts/                        # Python 辅助脚本
│   ├── memory_io.py                # memory 文件读写库
│   ├── update_memory.py            # 增量更新工具
│   ├── extract_segments.py         # 网页相关性筛选
│   └── requirements.txt            # 仅依赖 pyyaml
│
├── examples/                       # 示例
│   └── memory-L001-demo.md         # 一个虚构的成熟画像
│
└── references/                     # 参考文档
    ├── memory-format.md            # memory 文件格式规范
    └── agentskills-compat.md       # 各宿主兼容性
```

---

## 路线图

### v0.2.0 (当前)
- [x] 单文件 memory.md 存储
- [x] 代号化,移除加密
- [x] 多宿主兼容(Claude/Hermes/LobsterAI/OpenClaw)
- [x] 5 个核心工作流
- [x] MIT 开源

### v0.3.0 计划
- [ ] 演练 vs 实际反馈的对比工具,迭代画像准确度
- [ ] 多画像间的对比视图(团队多个利益相关方)
- [ ] 浏览器扩展(选中文本快速投喂)
- [ ] 画像导出为只读分享格式

---

## 贡献

欢迎 PR。重点欢迎以下贡献:

1. **新宿主适配测试**:在新 Agent 框架里试用,反馈兼容性问题
2. **Prompt 模板优化**:templates/ 下任何一个工作流,你觉得能写得更好
3. **多语言版本**:目前 templates 主要是中文,欢迎英文/日文版

不接受的 PR 方向:
- 任何引入云服务依赖的改动
- 任何"自动收集网络信息补全画像"的功能
- 任何加密/密钥管理功能(已决定走"明文+磁盘加密"路线)

---

## License

MIT - 详见 [LICENSE](LICENSE)

---

## 致谢

- 灵感来源:Anthropic Claude Skills 的 Progressive Disclosure 设计
- 兼容标准:[agentskills.io](https://agentskills.io)
- 多宿主验证:LobsterAI (有道龙虾)、Hermes Agent、OpenClaw 社区

# MyKnowledge 避坑指南

> 按场景分类的真实使用问题。每坑：❌ 错在哪 → ✅ 正确做法 → 💡 原理。
> 找不到再看 FAQ.md。

---

## 快速索引

| 场景 | 坑数 |
|------|------|
| [首次使用](#首次使用) | 3 |
| [需求管理](#需求管理) | 4 |
| [智能任务追踪](#智能任务追踪) | 2 |
| [迁移与备份](#迁移与备份) | 2 |
| [权限与错误](#权限与错误) | 3 |
| [平台差异](#平台差异) | 2 |
| [进阶使用](#进阶使用) | 3 |

---

## 首次使用

### 坑 1：跳过引导直接用

❌ 下载后直接说"创建知识库"，结果 AI 没引导，建出来的类型不对。

✅ 让 AI 完成首次引导（约 1 分钟）。引导会问你：知识库类型、自动记录开关。

💡 引导只出现一次，完成后再也不显示。完成后写 `~/.myknowledge/config/skill-state.yaml`。

### 坑 2：在错误目录建项目知识库

❌ 在 `~` 目录下说"创建项目知识库"，结果建在用户目录里。

✅ 先 `cd` 到项目根目录再创建。项目知识库 = `<当前目录>/.myknowledge/`。

💡 全局知识库永远在 `~/.myknowledge/global/`。

### 坑 3：混淆"智能任务追踪"的行为

❌ 以为开了智能任务追踪 AI 就完全不说话——结果 CodeBuddy 还是提示"已自动记录"。

✅ 理解平台差异：
- CodeBuddy/WorkBuddy/Claude：操作前提示用户（AI 会告知）
- OpenClaw + Hook：后台运行（操作后告知），参考 `hooks/openclaw/hook-guide.md`

---

## 需求管理

### 坑 4：手写需求 ID

❌ 手写 `REQ-001` 或 `req-20260610-1`——格式不对，AI 找不到。

✅ 让 AI 生成。格式永远是 `REQ-YYYYMMDD-XXX`（如 `REQ-20260610-001`）。

### 坑 5：状态跳级

❌ `Created` 直接改 `Done`——跳过 `In Progress` 和 `Review`。

✅ 按推荐流转：`Created → In Progress → Review → Done`。例外：`Created → Cancelled` 可以直接。

💡 状态反映进展，跳级会让 PROJECT-STATUS 失真。

### 坑 6：归档后以为需求消失了

❌ 归档后去找，以为被删了。

✅ 归档 = 移到 `archive/` 子目录，不删除。仍可查看、引用。

💡 全局：`~/.myknowledge/global/archive/`，项目：`<项目>/.myknowledge/archive/`。

### 坑 7：会话记录太多淹没了需求文档

❌ 每天自动追加对话，一周后需求文档 500 行，关键信息难找。

✅ 定期让 AI 帮你总结："把过去一周的会话记录整理成要点"。关键决策保留，碎片对话可删。

💡 需求文档的目的是知识沉淀，不是完整日志。

---

## 智能任务追踪

### 坑 8：检测灵敏度不符合个人偏好

💡 智能任务追踪的默认检测阈值适合大多数场景。如果你的工作风格不同，可以微调：

- 觉得**太敏感**（简单对话也触发）→ 提高 `min_keyword_count`（默认 3 → 4-5），或加 `exclude_patterns`
- 觉得**不够敏感**（复杂任务没触发）→ 降低 `min_keyword_count`（默认 3 → 2），或在 `keywords` 加常用术语

修改 `settings.yaml` 即可，无需改代码。这不是 bug，是个人偏好——就像有人喜欢通知多、有人喜欢安静。

### 坑 9：首次确认被跳过

❌ 以为开了智能任务追踪就无需确认——首次触发时 AI 仍然会问。

✅ 这是设计上的安全机制。选择"开启"后不再问。改主意说"开启/关闭自动记录"。

---

## 迁移与备份

### 坑 10：换电脑后知识库"丢失"

❌ 换了电脑，以为 MyKnowledge 会自动同步。

✅ MyKnowledge 是**纯本地**的。迁移方法：
```bash
# 旧电脑
tar -czf myknowledge-backup.tar.gz ~/.myknowledge/

# 复制到新电脑后
tar -xzf myknowledge-backup.tar.gz -C ~/
```

💡 也可以用 git 管理 `~/.myknowledge/`，但注意 `config/skill-state.yaml` 里的平台信息可能不适用新环境。

### 坑 11：备份只备了 Skill 没备用户数据

❌ 只把 `MyKnowledge/` 文件夹复制了，但 `~/.myknowledge/` 没备。

✅ Skill 文件和用户数据是**分离**的：
- Skill：`~/.codebuddy/skills/myknowledge/`（重新下载即可）
- 用户数据：`~/.myknowledge/`（**必须备份**）

---

## 权限与错误

> 💡 **为什么 AI 不自动修复？** MyKnowledge 的设计原则是"不执行任意 shell 命令"——这是安全边界。权限、备份、迁移等操作需要**你**手动确认，AI 会给出明确的修复步骤。

### 坑 12：权限不足导致创建失败

❌ AI 说"无法创建知识库"，不知道怎么办。

✅ 检查目录写入权限：
- 全局知识库：在终端运行 `ls -la ~/` 查看 `~/.myknowledge/` 权限
- 项目知识库：在终端运行 `ls -la` 查看 `.myknowledge/` 权限
- 如无写入权限，请在系统设置或终端中调整目录权限

### 坑 13：配置文件损坏

❌ `skill-state.yaml` 被手动编辑后格式错误，AI 加载异常。

✅ 恢复方法：
```bash
cp ~/.myknowledge/config/skill-state.yaml ~/.myknowledge/config/skill-state.yaml.bak
rm ~/.myknowledge/config/skill-state.yaml
# 重新加载 Skill，会触发首次引导重建配置
```

💡 不要手动编辑 `skill-state.yaml`，让 AI 帮你改。

### 坑 14：不知道说"重新初始化"可以重置

❌ 遇到诡异问题反复折腾，不知道有重置机制。

✅ 直接说"重新初始化 MyKnowledge"——AI 会删除旧配置，重新走首次引导。这是最干净的修复方式。

---

## 平台差异

### 坑 15：从 CodeBuddy 切到 OpenClaw，自动记录行为变了

❌ 习惯了 CodeBuddy 的"AI 告知"，换到 OpenClaw 后以为行为变了，以为坏了。

✅ 提前了解平台差异：
| 平台 | 检测方式 | 用户告知 |
|------|---------|---------|
| CodeBuddy | 意图识别 | 操作前提示 |
| WorkBuddy | 意图识别 | 操作前提示 |
| Claude | 意图识别 | 操作前提示 |
| OpenClaw | Hook（可选） | 操作后告知 |

💡 OpenClaw 的后台运行（操作后告知）需手动启用 Hook：`openclaw hooks enable myknowledge`。

### 坑 16：Claude 的 Hook 没生效

❌ 看了文档以为 Claude 支持 Hook，配置了没反应。

✅ Claude 的 Hook 支持取决于具体环境。目前主要通过意图识别（操作前提示用户）工作。`hooks/claude/hooks.json` 的 `enabled` 默认为 `false`。

---

## 进阶使用

### 坑 17：在多项目间切换时忘了当前知识库

❌ 上午在项目 A 建了需求，下午切到项目 B 说"查看项目进展"，看到的是项目 B 的状态，以为 A 的需求丢了。

✅ 知识库是**目录绑定的**——项目知识库 = 当前目录下的 `.myknowledge/`。切换项目后，`项目进展如何` 看的是新项目的状态。想看旧项目：`cd` 到旧项目目录再说。

💡 用"查看项目状态"前先确认 `pwd`，避免混淆。

### 坑 18：模板复制后不修改占位符

❌ 从 `core/templates/` 复制了模板到需求目录，但 `{{PROJECT_NAME}}`、`{{DATE}}` 等占位符没改，导致文档信息不完整。

✅ 模板是**参考格式**，复制后必须填写实际内容。让 AI 帮你填：说"基于 design-doc-template 模板，帮我写用户认证模块的设计文档"。

💡 不要让 AI 直接复制粘贴模板——让 AI 理解模板结构后**生成**具体内容。

### 坑 19：用 git 管理用户数据但忽略 .gitignore

❌ 把 `~/.myknowledge/` 整个加入 git，结果 `skill-state.yaml` 里的平台信息被同步到其他环境，引发冲突。

✅ 如用 git 管理用户数据，创建 `~/.myknowledge/.gitignore`：
```
config/skill-state.yaml
config/install-source
```
至少排除平台相关的配置文件。参考 [坑 10](#坑-10换电脑后知识库丢失)。

---

## 获取更多帮助

- 常见问题 → [FAQ.md](FAQ.md)
- 详细用法 → [USAGE.md](USAGE.md)
- 快速上手 → [QUICKSTART.md](QUICKSTART.md)
- 遇到 bug → [GitHub Issues](https://github.com/CoderMoray/MyKnowledge/issues)

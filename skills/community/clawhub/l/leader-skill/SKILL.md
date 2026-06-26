---
name: create-leader
description: "Create a leader AI skill, distill leadership style from workplace data, simulate leader decision-making, provide upward management advice, plan career advancement paths, help understand how to replace a leader, analyze leader weaknesses, build leadership capabilities, career strategy, promotion planning, boss simulation, manager skill creation, leadership analysis, upward communication guidance, career development, workplace strategy | 创建领导AI技能，从职场数据中蒸馏领导风格，模拟领导决策，提供向上管理建议，规划职业发展路径，帮助理解如何取代领导，分析领导弱点，构建领导能力，职业策略，晋升规划，老板模拟，经理技能创建，领导力分析，向上沟通指导，职业发展，职场策略，怎么和领导相处，怎么搞定老板，如何替代领导，怎么取代上级，领导模拟器，老板模拟器，创建领导skill，领导skill生成器，向上管理助手，取代路径规划"
argument-hint: "[leader-name-or-slug]"
version: "1.1.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# create-leader - 领导.skill 创建器

## Language / 语言

This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout. Below are instructions in both languages — follow the one matching the user's language.

本 Skill 支持中英文。根据用户第一条消息的语言，全程使用同一语言回复。下方提供了两种语言的指令，按用户语言选择对应版本执行。

---

## 中文版 (Chinese Version)

### 触发条件

当用户说以下任意内容时启动：
- /create-leader
- "帮我创建一个领导 skill"
- "我想蒸馏一个领导"
- "新建领导"
- "给我做一个 XX 领导的 skill"
- "我想创建一个领导skill"
- "帮我做一个老板的skill"
- "我想要一个领导模拟器"
- "怎么创建领导skill"
- "我需要一个向上管理助手"
- "帮我分析一下我的领导"
- "我想知道怎么取代这个领导"
- "如何替代我的上级"
- "创建一个经理skill"
- "领导skill生成器"
- "老板模拟器"
- "职场策略助手"
- "晋升规划"
- "职业发展路径"
- "怎么和领导相处"
- "怎么搞定老板"
- "领导分析"
- "向上沟通指导"

当用户对已有领导 Skill 说以下内容时，进入进化模式：
- "我有新文件" / "追加"
- "这不对" / "他不会这样" / "他应该是"
- /update-leader {slug}
- "更新一下这个领导skill"
- "我有新信息要补充"
- "这个领导不是这样的"

当用户说 /list-leaders 时列出所有已生成的领导。

---

### 核心场景设计

本 Skill 生成三轨结构：

**Track 1：领导力模拟**
- "如果是这位领导，他会怎么决策？"
- "这位领导在这个场景下会说什么？"

**Track 2：向上管理辅助**
- "我该怎么向这位领导汇报？"
- "这个方案怎么说服这位领导？"

**Track 3：取代路径规划（核心差异化）**
- "我该怎么取代这个领导？"
- "这位领导的软肋是什么？"
- "我需要具备什么能力才能坐上这个位置？"

---

### 主流程：创建新领导 Skill

#### Step 1：基础信息录入（4个问题）

只问 4 个问题：

1. **花名/代号（必填）**
2. **基本信息（一句话）**：公司、职级、职位、性别、年龄
   - 示例：字节 2-2 技术总监 男 35岁
3. **领导风格标签（一句话）**：MBTI、管理风格、核心特质、企业文化标签
   - 示例：ENTJ 狮子座 控制欲强 结果导向 画饼大师 喜怒无常
4. **你与他的关系（一句话）**：你的职位、汇报关系、你想从这个skill获得什么
   - 示例：我是他下属，想知道怎么跟他相处/怎么取代他

除代号外均可跳过。收集完后汇总确认再进入下一步。

---

#### Step 2：原材料导入

询问用户提供原材料，展示五种方式供选择：

```
原材料怎么提供？

  [A] 飞书自动采集（推荐）
      输入姓名，自动拉取消息记录 + 文档 + 会议记录 + 周报

  [B] 钉钉自动采集
      输入姓名，自动拉取文档 + 会议记录

  [C] 飞书/钉钉链接
      直接给文档/Wiki/会议记录链接

  [D] 上传文件
      PDF / 图片 / 导出 JSON / 邮件

  [E] 直接粘贴内容
      把他的讲话、邮件、会议记录复制进来
```

可以混用，也可以跳过（仅凭手动信息生成）。

---

#### 方式 A：飞书自动采集（推荐）

首次使用需配置：
```bash
python3 ${SKILL_DIR}/tools/feishu_auto_collector.py --setup
```

群聊采集：
```bash
python3 ${SKILL_DIR}/tools/feishu_auto_collector.py \
  --name "{name}" \
  --output-dir ./knowledge/{slug} \
  --msg-limit 2000 \
  --doc-limit 30
```

私聊采集（需要 user_access_token）：
- 参考 prompts/feishu_private_chat.md 完整流程

**重点采集内容**：
- 他在群聊中的决策过程
- 他给下属的反馈和批评
- 他在周报/月报中的表述
- 他的晋升轨迹和过往成就
- 他与上级的互动方式
- 他开会时的提问和关注点
- 他的用人偏好和提拔标准

---

#### Step 3：分析原材料

将收集到的所有原材料和用户填写的基础信息汇总，按三条线分析：

**线路 A（领导力模拟）**：
- 参考 prompts/leadership_analyzer.md
- 提取：决策模式、沟通风格、用人偏好、风险承受力
- 重点分析：他是如何做决策的？他喜欢什么样的下属？

**线路 B（向上管理）**：
- 参考 prompts/upward_analyzer.md
- 提取：汇报偏好、说服方式、雷区规避
- 重点分析：怎么跟他汇报他才听？他讨厌什么样的人？

**线路 C（取代路径规划）**：
- 参考 prompts/replacement_analyzer.md
- 提取：能力缺口、软肋分析、晋升路径、竞争对手分析
- 重点分析：他的软肋是什么？你需要具备什么能力？

---

#### Step 4：生成并预览

向用户展示三个部分的摘要（各 5-8 行），询问：

```
领导力模拟摘要：
  - 决策风格：{xxx}
  - 用人偏好：{xxx}
  - 沟通方式：{xxx}
  ...

向上管理摘要：
  - 汇报技巧：{xxx}
  - 说服方式：{xxx}
  - 雷区规避：{xxx}
  ...

取代路径规划摘要：
  - 他的软肋：{xxx}
  - 你的差距：{xxx}
  - 关键突破点：{xxx}
  ...
```

确认生成？还是需要调整？

---

#### Step 5：写入文件

用户确认后，执行以下写入操作：

1. 创建目录结构（用 Bash）：
```bash
mkdir -p leaders/{slug}/versions
mkdir -p leaders/{slug}/knowledge/docs
mkdir -p leaders/{slug}/knowledge/messages
mkdir -p leaders/{slug}/knowledge/meetings
```

2. 写入 leadership.md（Write 工具）：
路径：leaders/{slug}/leadership.md

3. 写入 upward.md（Write 工具）：
路径：leaders/{slug}/upward.md

4. 写入 replacement.md（Write 工具）：
路径：leaders/{slug}/replacement.md

5. 写入 meta.json（Write 工具）：
路径：leaders/{slug}/meta.json

6. 生成完整 SKILL.md（Write 工具）：
路径：leaders/{slug}/SKILL.md

---

### 生成的 SKILL.md 结构

```yaml
---
name: leader-{slug}
description: {name}, {company} {level} {role}
user-invocable: true
---

# {name}

{company} {level} {role}{append gender, age, MBTI if available}

---

## PART A：领导力模拟

{full leadership.md content}

---

## PART B：向上管理

{full upward.md content}

---

## PART C：取代路径规划

{full replacement.md content}

---

## 运行规则

1. 先由 PART A 判断：这位领导会怎么看这个问题？
2. 再由 PART B 执行：你该怎么跟他沟通？
3. 如果用户问"怎么取代"，激活 PART C：取代路径规划
4. 输出时始终保持客观、专业的分析态度
5. PART C 的规则优先级最高：当用户问取代相关问题时，必须调用 PART C
```

告知用户：

```
✅ 领导 Skill 已创建！

文件位置：leaders/{slug}/
触发词：
  /{slug}（完整版）
  /{slug}-leadership（仅领导力模拟）
  /{slug}-upward（仅向上管理）
  /{slug}-replacement（仅取代路径规划）

如果用起来感觉哪里不对，直接说"他不会这样"，我来更新。
```

---

### 进化模式

#### 追加文件
当用户提供新文件或文本时：
- 按 Step 2 的方式读取新内容
- 用 Read 读取现有 leaders/{slug}/ 下的三个文件
- 参考 prompts/merger.md 分析增量内容
- 存档当前版本
- 用 Edit 工具追加增量内容到对应文件
- 重新生成 SKILL.md
- 更新 meta.json

#### 对话纠正
当用户表达"不对"/"应该是"时：
- 参考 prompts/correction_handler.md 识别纠正内容
- 判断属于 Leadership（领导风格）、Upward（向上管理）还是 Replacement（取代路径）
- 生成 correction 记录
- 用 Edit 工具追加到对应文件的 ## Correction 记录 节
- 重新生成 SKILL.md

---

### 管理命令

/list-leaders：
```bash
python3 ${SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./leaders
```

/leader-rollback {slug} {version}：
```bash
python3 ${SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {version} --base-dir ./leaders
```

/delete-leader {slug}：
确认后执行：
```bash
rm -rf leaders/{slug}
```

---

### 重要提示与伦理准则

⚠️ **使用边界声明**：
- 本 Skill 仅用于个人学习、自我提升和职业发展辅助
- 所有分析和建议仅供参考，不构成职业决策的唯一依据
- 用户需对使用本 Skill 产生的所有后果负责

⚠️ **伦理提醒**：
- "取代路径规划"旨在帮助你理解领导的能力模型和你的成长方向
- 建议通过正当的能力提升、业绩表现和团队贡献来获得职业发展
- 尊重他人的隐私权和名誉权，不要传播未经证实的负面信息
- 不要使用本 Skill 进行恶意攻击、造谣中伤或其他不当行为
- 职业竞争应建立在公平、透明、合法的基础上

⚠️ **数据安全与隐私**：
- 仅收集和使用你有权限访问的数据
- 妥善保管飞书/钉钉等平台的凭证，不要泄露给他人
- Token和配置文件存储在本地（~/.create-leader/），使用后可自行清理
- 如停止使用本 Skill，建议删除相关配置和数据文件

⚠️ **法律责任声明**：
- 本 Skill 的开发者不对用户的使用方式和后果承担责任
- 用户需确保使用本 Skill 符合所在国家/地区的法律法规
- 用户需确保遵守所在公司的规章制度和数据安全政策
- 如对使用边界有疑问，建议咨询专业法律或人力资源顾问

---

---

## English Version

### Trigger Conditions

Activate when the user says any of the following:
- /create-leader
- "Help me create a leader skill"
- "I want to distill a leader"
- "New leader"
- "Make a skill for XX leader"
- "I want to create a leader skill"
- "Help me make a boss skill"
- "I want a leader simulator"
- "How to create a leader skill"
- "I need an upward management assistant"
- "Help me analyze my manager"
- "I want to know how to replace this leader"
- "How to take my boss's position"
- "Create a manager skill"
- "Leader skill generator"
- "Boss simulator"
- "Workplace strategy assistant"
- "Promotion planning"
- "Career development path"
- "How to work with my boss"
- "How to handle my manager"
- "Leadership analysis"
- "Upward communication guide"

Enter evolution mode when the user says:
- "I have new files" / "append"
- "That's wrong" / "He wouldn't do that" / "He should be"
- /update-leader {slug}
- "Update this leader skill"
- "I have new information to add"
- "This leader isn't like that"

List all generated leaders when the user says /list-leaders.

---

### Core Scenarios

This skill generates a three-track structure:

**Track 1: Leadership Simulation**
- "If this leader were here, how would he decide?"
- "What would this leader say in this scenario?"

**Track 2: Upward Management Assistance**
- "How should I report to this leader?"
- "How to convince this leader of this proposal?"

**Track 3: Replacement Path Planning (Core Differentiator)**
- "How can I replace this leader?"
- "What are this leader's weaknesses?"
- "What capabilities do I need to take this position?"

---

### Main Flow: Create a New Leader Skill

#### Step 1: Basic Information Collection (4 questions)

Only ask 4 questions:

1. **Alias / Codename (required)**
2. **Basic info (one sentence)**: Company, level, role, gender, age
   - Example: ByteDance L2-2 Engineering Director Male 35
3. **Leadership style tags (one sentence)**: MBTI, management style, core traits, corporate culture tags
   - Example: ENTJ Leo control-oriented results-driven promises a lot moody
4. **Your relationship (one sentence)**: Your position, reporting line, what you want from this skill
   - Example: I'm his subordinate, want to know how to work with him/how to replace him

Everything except the alias can be skipped. Summarize and confirm before moving to the next step.

---

#### Step 2: Source Material Import

Ask the user how they'd like to provide materials:

```
How would you like to provide source materials?

  [A] Feishu Auto-Collect (Recommended)
      Enter name, auto-pull messages + docs + meeting notes + weekly reports

  [B] DingTalk Auto-Collect
      Enter name, auto-pull docs + meeting notes

  [C] Feishu/DingTalk Links
      Provide doc/wiki/meeting note links directly

  [D] Upload Files
      PDF / images / exported JSON / emails

  [E] Paste Text
      Copy-paste his speeches, emails, meeting notes
```

Can mix and match, or skip entirely (generate from manual info only).

---

#### Option A: Feishu Auto-Collect (Recommended)

First-time setup:
```bash
python3 ${SKILL_DIR}/tools/feishu_auto_collector.py --setup
```

Group chat collection:
```bash
python3 ${SKILL_DIR}/tools/feishu_auto_collector.py \
  --name "{name}" \
  --output-dir ./knowledge/{slug} \
  --msg-limit 2000 \
  --doc-limit 30
```

Private chat collection (requires user_access_token):
- See prompts/feishu_private_chat.md for complete flow

**Key Collection Content**:
- His decision-making process in group chats
- His feedback and criticism to subordinates
- His statements in weekly/monthly reports
- His promotion trajectory and past achievements
- How he interacts with superiors
- His questions and focus points in meetings
- His hiring preferences and promotion criteria

---

#### Step 3: Analyze Source Materials

Combine all collected materials and user-provided info, analyze along three tracks:

**Track A (Leadership Simulation)**:
- Refer to prompts/leadership_analyzer.md
- Extract: decision patterns, communication style, hiring preferences, risk tolerance
- Key analysis: How does he make decisions? What kind of subordinates does he like?

**Track B (Upward Management)**:
- Refer to prompts/upward_analyzer.md
- Extract: reporting preferences, persuasion methods, minefield avoidance
- Key analysis: How to report so he listens? What kind of people does he hate?

**Track C (Replacement Path Planning)**:
- Refer to prompts/replacement_analyzer.md
- Extract: capability gaps, weakness analysis, promotion path, competitor analysis
- Key analysis: What are his weaknesses? What capabilities do you need?

---

#### Step 4: Generate and Preview

Show the user a summary of the three parts (5-8 lines each), ask:

```
Leadership Simulation Summary:
  - Decision style: {xxx}
  - Hiring preferences: {xxx}
  - Communication style: {xxx}
  ...

Upward Management Summary:
  - Reporting techniques: {xxx}
  - Persuasion methods: {xxx}
  - Minefield avoidance: {xxx}
  ...

Replacement Path Planning Summary:
  - His weaknesses: {xxx}
  - Your gaps: {xxx}
  - Key breakthrough points: {xxx}
  ...
```

Confirm generation? Or need adjustments?

---

#### Step 5: Write Files

After user confirmation, execute the following:

1. Create directory structure (Bash):
```bash
mkdir -p leaders/{slug}/versions
mkdir -p leaders/{slug}/knowledge/docs
mkdir -p leaders/{slug}/knowledge/messages
mkdir -p leaders/{slug}/knowledge/meetings
```

2. Write leadership.md (Write tool):
Path: leaders/{slug}/leadership.md

3. Write upward.md (Write tool):
Path: leaders/{slug}/upward.md

4. Write replacement.md (Write tool):
Path: leaders/{slug}/replacement.md

5. Write meta.json (Write tool):
Path: leaders/{slug}/meta.json

6. Generate full SKILL.md (Write tool):
Path: leaders/{slug}/SKILL.md

---

### Generated SKILL.md Structure

```yaml
---
name: leader-{slug}
description: {name}, {company} {level} {role}
user-invocable: true
---

# {name}

{company} {level} {role}{append gender, age, MBTI if available}

---

## PART A: Leadership Simulation

{full leadership.md content}

---

## PART B: Upward Management

{full upward.md content}

---

## PART C: Replacement Path Planning

{full replacement.md content}

---

## Execution Rules

1. PART A decides first: How would this leader view this problem?
2. PART B executes: How should you communicate with him?
3. If user asks "how to replace", activate PART C: Replacement Path Planning
4. Always maintain an objective, professional analytical tone in output
5. PART C rules have highest priority: When user asks replacement-related questions, must call PART C
```

Inform the user:

```
✅ Leader Skill created!

Location: leaders/{slug}/
Commands:
  /{slug} (full version)
  /{slug}-leadership (leadership simulation only)
  /{slug}-upward (upward management only)
  /{slug}-replacement (replacement path planning only)

If something feels off, just say "he wouldn't do that" and I'll update it.
```

---

### Evolution Mode

#### Append Files
When user provides new files or text:
- Read new content using Step 2 methods
- Read existing three files under leaders/{slug}/ with Read
- Refer to prompts/merger.md for incremental analysis
- Archive current version
- Use Edit tool to append incremental content to relevant files
- Regenerate SKILL.md
- Update meta.json

#### Conversation Correction
When user expresses "that's wrong" / "he should be":
- Refer to prompts/correction_handler.md to identify correction content
- Determine if it belongs to Leadership, Upward, or Replacement
- Generate correction record
- Use Edit tool to append to ## Correction Log section of relevant file
- Regenerate SKILL.md

---

### Management Commands

/list-leaders:
```bash
python3 ${SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./leaders
```

/leader-rollback {slug} {version}:
```bash
python3 ${SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {version} --base-dir ./leaders
```

/delete-leader {slug}:
After confirmation:
```bash
rm -rf leaders/{slug}
```

---

### Important Notes & Ethical Guidelines

⚠️ **Usage Boundaries**:
- This skill is for personal learning, self-improvement, and career development assistance only
- All analysis and recommendations are for reference only and do not constitute the sole basis for career decisions
- Users are solely responsible for all consequences of using this skill

⚠️ **Ethical Reminder**:
- "Replacement Path Planning" is designed to help you understand the leader's capability model and your growth direction
- Career advancement through legitimate capability improvement, performance, and team contribution is recommended
- Respect others' privacy and reputation, do not spread unsubstantiated negative information
- Do not use this skill for malicious attacks, defamation, or other inappropriate behavior
- Career competition should be based on fair, transparent, and legal principles

⚠️ **Data Security & Privacy**:
- Only collect and use data you have permission to access
- Safeguard Feishu/DingTalk and other platform credentials, do not disclose to others
- Tokens and config files are stored locally (~/.create-leader/), you can clean them up after use
- If you stop using this skill, it is recommended to delete related configs and data files

⚠️ **Legal Liability Disclaimer**:
- The developer of this skill is not responsible for how users use it or the consequences
- Users must ensure use of this skill complies with laws and regulations in their country/region
- Users must ensure compliance with their company's policies and data security rules
- If in doubt about usage boundaries, consult professional legal or HR advisors

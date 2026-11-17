---
name: one-novel-skill
version: 1.0.0
description: "融合级中文小说创作。从零开书到长篇日更，四层反AI防护，12套L2检测，创作宪法/澄清决策/时间线校验，多视角对抗式审查。你说'帮我写个小说'，剩下的我来做。零配置自适应LLM，支持Ollama任意模型/OpenClaw/DeepSeek/OpenAI/Claude/Gemini/通义千问/智谱/月之暗面/百川/自定义端点，安装即用。"
context: fork
agent: general-purpose
model: inherit
allowed-tools:
  - read_file
  - write_to_file
  - replace_in_file
  - execute_command
  - search_file
  - search_content
  - list_dir
  - delete_file
---

# 全能小说创作 — 零配置自适应引擎

> **安装即用，零配置。** 自动检测环境中所有可用的 LLM——Ollama（任意模型）/ OpenClaw / DeepSeek / OpenAI / Claude / Gemini / 通义千问 / 智谱 / 月之暗面 / 百川 / 自定义 OpenAI-compatible 端点。
>
> **CodeBuddy Skill 模式**：AI 宿主直接生成，无需任何外部 LLM API。
> **本地 Python 模式**：设置任一 API Key 环境变量，自动发现并使用。

---

## 模式判断（每轮对话第一步）

1. 检查环境变量 `CB_NATIVE_MODE`
2. 若 `CB_NATIVE_MODE=1` 且有外部 LLM 可用 → **本地模式**，调用 `python run.py`
3. 否则 → **Skill 模式**，AI 直接按下方工作流生成

---

## Skill 模式工作流（默认）

### 一、初始化项目

用户说"帮我写个小说"时：

1. 确认题材、平台、风格（可提供选项让用户选择）
2. 确认完成后，创建项目目录结构：
   ```
   书名/
   ├── 设定/  世界观.md / 人物/ / 势力.md / 关系.md
   ├── 大纲/  故事大纲.md / 卷规划.md / 伏笔.md
   ├── 正文/  第NNN章.txt
   ├── 追踪/  角色状态.md / 时间线.md / 上下文.md
   └── state.json
   ```
3. 用 `write_to_file` 创建 `state.json`：
   ```json
   {
     "version": "1.0.0",
     "meta": {"title": "书名", "platform": "平台", "genre": "题材"},
     "progress": {"written": 0, "total_planned": 10, "last_chapter": 0},
     "characters": {}, "settings": [], "plot": {"hooks": [], "resolved_hooks": [], "arcs": []},
     "timeline": [], "readers": {"阅读率": 1.0, "评论情绪": "neutral", "警告": []},
     "foreshadows": [], "character_states": {}, "global_memory": {}, "payoff_ledger": []
   }
   ```
4. 生成世界观、人物设定、大纲（写入对应文件）

### 二、写章节

**每章流程：**

#### Step 1: 准备上下文
- 用 `read_file` 读取 `追踪/角色状态.md`、`追踪/伏笔.md`、`state.json`
- 用 `read_file` 读取上一章正文（如有）

#### Step 2: 生成章节（AI 直接生成）
按照以下要求生成正文：

**写作规范（P0 必须遵守）：**
- 禁用词：不用"毋庸置疑/值得一提的是/总而言之/命运的齿轮/从某种意义上说"
- 禁用句式：不用"不是A而是B"结构、不用"他知道/他感到/她觉得"直接告情绪
- 禁用结尾：不用章末感悟总结、不用"他不知道的是..."
- **身体法则**：用具体动作替代抽象情绪。不说"他很生气"，写"他把杯子砸在桌上"
- **拉不说推**：用三样具体细节替代结论性评价
- **痒的法则**：每章结尾必须是新问题而非旧答案

**写作规范（P1 建议遵守）：**
- 对话用动作替代"说道/问道"标签
- 感官描写每场景至少 2 种
- 句长有变化，不全部 25-35 字
- 章节字数：番茄 2000-2500 / 起点 3000-5000 / 七猫 2000-3000 / 飞卢 2000-3000

**平台差异化：**
- 番茄：前三章必出金手指，每章断钩子，节奏极快
- 起点：可慢热，质量优先，世界观可铺垫
- 七猫：情感线优先，女性角色有事业线
- 飞卢：500字内给系统，爽字第一

**生成时注入以下资料（从 references/ 读取）：**
- 开篇模板（前3章）：`references/original/genre-opening-templates.md`
- 钩子密度：`references/original/hook-density-model.md`
- 打脸节奏（爽文）：`references/original/face-slapping-rhythm.md`

#### Step 3: 写入正文
用 `write_to_file` 写入 `正文/第NNN章.txt`，**纯文本，不含 Markdown 格式**。

#### Step 4: 运行检测（Python 脚本）
```bash
python run.py detect --file 正文/第NNN章.txt
```
若检测结果 ≥ YELLOW：
- 阅读检测报告，识别 Top 3-5 问题
- 用 `replace_in_file` 修正正文中的问题
- 重新检测，直到 GREEN

#### Step 5: 更新状态
- 用 `replace_in_file` 更新 `追踪/角色状态.md`（角色位置/情绪/关系变化）
- 用 `replace_in_file` 更新 `追踪/伏笔.md`（新伏笔/已回收伏笔）
- 用 `replace_in_file` 更新 `state.json` 的 progress

### 三、续写/批量推进

用户说"续写"或"写第X到Y章"时：
1. 读取 `state.json` 获取当前进度
2. 循环执行 Step 1-5，每章独立完成
3. 每 3 章汇总一次进度

### 四、去AI味

用户说"太AI了"或"去味"时：
1. 用 `read_file` 读取正文
2. 用 `python run.py detect --file 正文/第NNN章.txt` 获取详细问题
3. 逐项修复：
   - 删减法：Filler 短语、空洞修饰、无效铺垫
   - 替换法：路标词→自然过渡，总结腔→直接陈述
   - 打破法：工整句式→长短变化，固定模板→具体描写
   - 具体化：抽象情绪→动作/环境，概括判断→细节支撑
4. 修复后重新检测

### 五、深度审查

用户说"审查第X章"时：
1. 用 `read_file` 读取正文
2. 从 5 个视角分析（在回复中输出，不写文件）：
   - 读者视角：阅读体验、爽点/毒点
   - 编辑视角：节奏、逻辑、商业化
   - 毒舌视角：毫不留情的批评
   - 一致性视角：人设/时间线/伏笔
   - AI 检测视角：运行 `python run.py detect`
3. 输出审查报告

### 六、导入外部小说

用户说"导入小说"并提供文件路径时：
```bash
python run.py import --file 路径
```

---

## 本地模式（CB_NATIVE_MODE=1）

**零配置自适应。** 设置任一 LLM 的 API Key 环境变量即可：

| Provider | 环境变量 | 自动检测 |
|----------|---------|:--------:|
| Ollama（任意本地模型） | 无需（自动检测 `ollama list`） | ✅ |
| OpenClaw Gateway | 自动检测 `~/.openclaw/openclaw.json` | ✅ |
| DeepSeek | `DEEPSEEK_API_KEY` | ✅ |
| 通义千问（阿里云） | `DASHSCOPE_API_KEY` | ✅ |
| 智谱 GLM | `ZHIPU_API_KEY` | ✅ |
| 月之暗面 Kimi | `MOONSHOT_API_KEY` | ✅ |
| 百川 | `BAICHUAN_API_KEY` | ✅ |
| OpenAI | `OPENAI_API_KEY` | ✅ |
| Claude（Anthropic） | `ANTHROPIC_API_KEY` | ✅ |
| Gemini（Google） | `GEMINI_API_KEY` | ✅ |
| 自定义端点 | `CUSTOM_LLM_BASE` + `CUSTOM_LLM_MODEL` | ✅ |

```bash
# 查看自动发现的 provider
python run.py providers

# 生成 5 章（自动选择最优 provider）
python run.py generate --chapters 5

# 检测单章
python run.py detect --file 正文/第001章.txt

# 章节对比（人设漂移/时间线/伏笔/场景衔接）
python run.py compare --chapter 3

# 生成数据报告（字数/角色出场率/钩子密度/P0违规）
python run.py report

# 查看状态
python run.py status

# 回滚
python run.py rollback --chapter 3
```

---

## 
---

## Agent 执行指令（使用指南）

> 本章节定义了 Agent 在每种场景下应该做什么、调什么脚本、用什么参数。这是操作手册，不是功能列表。

### 0.1 Agent 职责边界

| 操作类型 | 执行方式 | 说明 |
|---------|---------|------|
| 项目初始化 | **Agent LLM** | 直接生成目录结构和设定文件，用户确认后写入 |
| 设定阶段 | **Agent LLM** | 世界观/人物/大纲/伏笔，直接生成，用户确认后写入 |
| 正文生成（每章） | **Agent LLM + 脚本** | 生成正文写入，调 detect 检测，按报告修订 |
| AI味检测 | **调脚本** | python run.py detect --file <file> |
| 深度审查（5视角） | **Agent LLM** | 直接输出审查报告给用户，不写文件 |
| 章节对比 | **调脚本** | python run.py compare --chapter N |
| 状态管理 | **直接读写文件** | state.json + 追踪/ 目录 |
| 回滚 | **调脚本** | python run.py rollback --chapter N |
| 数据报告 | **调脚本** | python run.py report |
| 导入外部小说 | **调脚本** | python run.py import --file <file> |

### 0.2 脚本调用速查

bash:
  python run.py status                   # 项目状态
  python run.py generate --chapters 5    # 生成章节
  python run.py detect --file 正文/第001章.txt  # AI味检测
  python run.py compare --chapter 3      # 章节对比
  python run.py report                   # 数据报告
  python run.py rollback --chapter 3     # 回滚
  python run.py import --file 作品.txt   # 导入小说
  python run.py providers                # 查看可用LLM

### 0.3 标准工作流（每章循环）

1. Agent 准备上下文: 读取 state.json + 追踪/*.md + 上一章正文
2. Agent 生成正文 -> 写入 正文/第NNN章.txt
3. 执行: python run.py detect --file 正文/第NNN章.txt
4. GREEN -> 步骤5; YELLOW -> 修订后重测; RED -> 重写（最多2轮）
5. 更新: 角色状态.md + 伏笔.md + 时间线.md + state.json
6. 报告完成 -> 下一章

### 0.4 检测结果解析

输出JSON含: status(GREEN/YELLOW/RED), issues[], score
GREEN=通过, YELLOW=修订后通过, RED=必须重写

### 0.5 错误恢复协议

脚本失败: 确认路径 -> pip install -> 降级手动检测
检测门禁2轮仍失败: 标记为需人工介入

写作铁律（写每章前必读）

### P0 — 绝对禁止
| 类别 | 内容 |
|------|------|
| 禁用词 | 毋庸置疑、不可否认、值得一提的是、总而言之、众所周知、命运的齿轮、从某种意义上说、由此可见、综上所述 |
| 禁用句式 | "不是A，而是B"结构、"仿佛/犹如/宛若……一般"、"眼中闪过一丝/嘴角勾起一抹"、"他知道/她感到/她觉得" |
| 禁用结尾 | 章末感悟总结、"他不知道的是……"、"总的来说/总而言之"式收尾 |
| 标点 | 连续 `!!!` 或 `??` 堆砌 |

### P1 — 强烈建议避免
| 类别 | 内容 |
|------|------|
| 句式 | "与此同时/紧接着/就在这时"开头、"随着……"段首、连续3句以上相同结构 |
| 副词 | "缓缓/慢慢/轻轻/悄悄" 每千字 ≤4 次 |
| 对话 | 所有角色说话方式一样、对话标签超过50%用"说道/问道" |
| 情感 | 直接告知情绪，缺少动作/环境展示 |

---



## 章节契约系统

每章正文写作前，先生成章节契约，用户确认后再动笔。

契约格式：
- 章节编号
- 必达节拍（3-5项，本章必须完成的情节推进）
- 禁止事项（本章禁止的操作）
- 目标情绪（读者读完后应有的情绪）
- 章末钩子（结尾钩子目标）
- 张力曲线（上升/下降/峰值/低谷）
- 风险等级（低/中/高）及说明

流程：
1. Agent 根据细纲和当前状态生成契约
2. 用户确认或修改
3. 确认后开始正文写作
4. 写作完成后契约归档到 追踪/章节契约/ 目录

---

## 写前分析预览

每章正文写作前，生成写前分析预览展示给用户确认。

预览内容：
- 前文摘要（上一章关键进展）
- 角色状态快照（主角/配角当前实力、位置、情绪）
- 活跃伏笔（当前未回收的伏笔清单）
- 本章风险标记（契约中标注的风险）
- 完成标准（达到什么状态可以交付）

流程：
1. 读取 追踪/ 目录下的所有文件
2. 生成写前分析预览
3. 用户确认或调整提示词
4. 确认后进入正文生成

---

## L2-L4 语义层审查

python run.py detect 完成 L1 机械层后，Agent 执行以下三层审查：

### L2 风格一致性
- 叙述视角一致（无POV跳跃）
- 角色语音统一（遮名辨人）
- 句长方差 >= 8

### L3 内容质量
- 情节逻辑自洽（六条连续性法则）
- 角色弧光推进
- 世界观一致
- 伏笔管理追踪
- 无连续500字纯描写

### L4 阅读体验
- 温度感：具体 > 抽象
- 独特性：只有本书才有的表达
- 翻页驱动力：章末有追问冲动
- 人味：像真人写的

### 六条连续性法则
1. 角色伤势、情绪、关系、秘密、能力随身记
2. 世界规则限制和代价不随意突破
3. 每章伏笔新增/推进/回收
4. 以弱胜强需铺垫、计谋或代价
5. 主角升级需过程、风险或瓶颈
6. 反派有目标、资源和行动逻辑

---

## 短故事模式

用户请求短故事时自动切换，不走长篇流程。

### 三阶段流程
SS0 平台识别与选题：目标平台、类型、字数、核心反转确认
SS1 人物与大纲：主角锚点>=2，三至五幕结构
SS2 正文生成与平台适配：生成->检测->平台格式校验->定稿

### 字数体系
- 微小说：500-1000字（小红书、头条）
- 超短篇：1000-3000字（小红书、知乎）
- 标准短篇：6000-15000字（番茄、七猫）
- 知乎盐选：8000-30000字

### 红线
- 开篇200字未进核心冲突 -> 重写开头
- 中段无情绪推进 -> 插入爆点
- 结尾无反转或无情绪落点 -> 重写结尾

---

## 叙事结构增强

### 反直觉追问法（每章规划时）
1. 本章最想让读者意外的是什么？
2. 读者读完应有什么情绪？
3. 本章推进了谁的成长弧光？

### 八段式章节结构
1. 本章目标 -> 2. 有利出现 -> 3. 困难降临
4. 积极应对 -> 5. 突发转折 -> 6. 认知颠覆
7. 本章高潮 -> 8. 悬念留钩

### 升番逻辑
信息揭露逐级升级：基础揭示 -> 进阶揭示 -> 出乎意料

### 情绪生理反应置换表
- 愤怒 -> 手背青筋暴起、一拳砸在桌上
- 恐惧 -> 后背发凉、牙齿打颤
- 悲伤 -> 喉咙发紧、眼眶发酸
- 紧张 -> 手心出汗、反复检查
- 放松 -> 肩膀垮下来、长出一口气

---

## 记忆与学习系统

### 触发学习
- 用户显式纠正（不要这样写、改回之前的风格）
- 同一修正出现三次
- 用户说记住这个

### 四层记忆消歧
宪法记忆（全书设定、世界观法则）优先级最高
结构治理记忆（总纲、卷规划）次之
项目运行记忆（任务日志、伏笔、时间线）再次
会话工作记忆（本章目标、场景链）最低

原则：宪法级设定不能被日常写作中的临时决策覆盖。

---

## 平台文章模式

### 两阶段流程
A0 选题与结构：平台、文章类型、核心观点、大纲确认
A1 正文生成与平台排版：生成->原创性检查->平台格式校验->定稿

### 文章字数体系
- 小红书笔记：300-1000字
- 知乎回答：500-3000字
- 头条资讯：800-2000字
- 公众号文章：1500-5000字

---

## 多智能体协作模式（长篇）

项目配置中设置协作模式：

串行：单个智能体顺序写作（中短篇）
并行：多个子智能体并行写作（中长篇，速度优先）
团队：协调者->架构师->写手->编辑（百万字史诗）

团队模式角色：
- 协调者：分配任务、追踪进度、解决冲突
- 架构师：维护章节契约和世界观一致性
- 写手：按契约生成章节草稿
- 编辑：执行质量审查


## 文件功能清单

| 文件/目录 | 功能 |
|-----------|------|
| `state.json` | 全书状态（进度/角色/伏笔） |
| `正文/第NNN章.txt` | 章节正文（纯文本） |
| `追踪/` | 角色状态、时间线、伏笔追踪 |
| `设定/` | 世界观、人物设定、势力关系 |
| `大纲/` | 故事大纲、卷规划 |
| `run.py` | CLI 入口（status/detect/generate/rollback） |
| `detectors/` | 6 套 AI 检测引擎（纯 Python，不依赖 LLM） |
| `engine/` | 生成管线引擎（本地模式使用） |
| `references/` | 写作技法参考资料库（150+ 篇） |
| `engine/chapter_compare.py` | 章节对比引擎（人设漂移/时间线/伏笔/场景） |
| `engine/rolling_planner.py` | 指南针+视野滚动规划（长篇不一次规划全部） |
| `engine/session_state.py` | WAL协议+三文件进度系统（防上下文丢失） |
| `engine/character_cognition.py` | 角色认知信息差模型（防穿帮） |
| `engine/prompt_registry.py` | Prompt 统一注册中心（10个内置Prompt） |
| `engine/user_preferences.py` | 用户偏好持久化系统（跨会话学习） |
| `engine/soul_skill.py` | 角色灵魂系统（20个核心原型） |

---

## 已知局限

1. **Skill 模式**：AI 直接生成的文本质量取决于宿主 AI 模型能力
2. **检测覆盖**：Python 检测脚本独立于 LLM，可检测禁用词/句式/结构，但无法做语义级分析
3. **本地模式**：需至少一个外部 LLM provider 可用

---

## 核心引擎清单

| 引擎 | 功能 | 灵感来源 |
|------|------|---------|
| `generator.py` | 12 provider 零配置自适应 LLM | — |
| `pipeline.py` | 5 阶段生成管线 | — |
| `quality_gate.py` | 多引擎质量门禁 + 自动修正 | — |
| `rolling_planner.py` | 指南针+视野滚动规划 | ainovel-cli |
| `session_state.py` | WAL 协议 + 三文件进度系统 | planning-with-files + proactive-agent |
| `character_cognition.py` | 角色认知信息差模型（防穿帮） | QMAI SoulSkill |
| `chapter_compare.py` | 5 维度章节对比 | — |
| `l2_modules.py` | 12 套反 AI 痕迹模块 | humanizer / Humanizer-zh |
| `detectors/` | 6 套 AI 检测引擎 | QMAI |
| `reference_engine.py` | 150+ 篇资料索引 + pipeline 注入 | — |

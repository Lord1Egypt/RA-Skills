---
name: multi-group-chat-manager
repository: https://github.com/pppig1357/multi-group-chat-manager
description: 用户画像+好感度双系统 + 自研液态记忆引擎。零外部依赖（核心），仅 OneBot 采集器使用 requests。画像使用自研 FluidMemory 引擎追踪用户特征，支持艾宾浩斯遗忘曲线衰减+自动关键词匹配强化。好感度基于群规加减分系统，JSON文件+文件锁保护。全配置统一化：config.json 集中管理，热加载不重启。多群聊上下线管理：基于时间戳区间精准扫描。OneBot 采集器+好感度规则引擎，规则文件化管理，支持多群差异化规则，水位线去重，auto/ai 双模式。扫描流水线集成采集→好感度→画像强化三阶段。
---

# 🦞 multi-group-chat-manager v1.1.5

多群聊用户画像管理 + 好感度系统。

**让 AI 更懂每个群友。** 自动记录兴趣偏好、性格特征、常聊话题；追踪好感度，用规则引擎自动加减分；液态记忆引擎模拟人类遗忘曲线。

**适配平台：** QQ（OneBot）、飞书、Discord、Telegram 等任意 OpenClaw 支持的消息渠道。

---

## 📋 目录

- [🆕 初始化流程（首次部署看这里）](#-初始化流程首次部署看这里)
- [📂 项目架构](#-项目架构)
- [🧩 系统一：用户画像系统](#-系统一用户画像系统)
- [❤️ 系统二：好感度系统](#-系统二好感度系统)
- [🧠 系统三：液态记忆引擎](#-系统三液态记忆引擎)
- [⚙️ 系统四：好感度规则引擎](#-系统四好感度规则引擎)
- [🔄 上下线会话管理](#-上下线会话管理)
- [📝 画像更新与扫描流程](#-画像更新与扫描流程)
- [🔒 隐私保障](#-隐私保障)
- [💻 CLI 速查](#-cli-速查)

---

## 🆕 初始化流程（首次部署看这里）

### 第一步：配置 OpenClaw

在 OpenClaw 配置文件中启用此 Skill：

```yaml
skills:
  multi-group-chat-manager:
    enabled: true
    path: /path/to/skills/multi-group-chat-manager
```

### 第二步：配置文件（config.json）

编辑 `config.json`，填写你的信息：

```json
{
  "onebot": {
    "base_url": "http://127.0.0.1:3000",
    "groups": {
      "群号1": "群名称1",
      "群号2": "群名称2"
    }
  },
  "affection": {
    "small_group_default_score": 85,
    "small_group_ids": ["群友QQ号1", "群友QQ号2"]
  }
}
```

**需要修改的配置项：**

| 参数 | 位置 | 说明 |
|:----|:-----|:-----|
| `onebot.groups` | config.json | 你管理的 QQ 群列表（群号→群名） |
| `onebot.base_url` | config.json | OneBot HTTP API 地址 |
| `affection.small_group_ids` | config.json | 核心成员 QQ 号列表（初始好感度 85 分） |
| `affection.small_group_default_score` | config.json | 核心成员初始好感度（默认 85） |
| `affection.default_score` | config.json | 新成员默认好感度（默认 50） |

如果使用非 QQ 渠道（飞书/Discord 等），onebot 部分可直接留空或删除，画像和好感度系统仍正常工作，只是无法用 OneBot 做批量消息采集。

### 第三步：设置群规规则文件

为你的每个群创建规则文件，放在 `scripts/rules/` 目录下：

```bash
# 复制模板
cp scripts/rules/rule_sample.json scripts/rules/rule_你的群号.json
```

编辑文件，修改 `meta.group_id` 和 `meta.group_name`，根据你的群规调整关键词和规则。

> 参考 `rule_sample.json` 中的注释理解每个字段的含义。

### 第四步：初始化好感度

```bash
# 对核心成员批量设置初始好感度
py scripts/affection.py init 群友QQ号 85

# 或批量导入（编辑 config.json 的 small_group_ids 后，逐条执行）
```

新用户将在首次被记录时自动获得 `default_score`（默认 50 分）。

### 第五步：初始化画像存储目录

数据目录会自动创建，无需手动操作。首次调用 `profiles.py update` 时会自动建立目录结构：

```
profiles/
├── memory/       # 液态记忆数据
└── composite/    # 概要画像
logs/             # 好感度日志
```

### 第六步：验证部署

```bash
# 检查好感度系统
py scripts/affection.py status

# 检查液态记忆引擎
py scripts/memory.py stats

# 检查 OneBot 连接（QQ 渠道）
py scripts/onebot_collector.py health

# 查看规则引擎状态
py scripts/rule_engine.py list
```

### 第七步（可选）：配置 AI 助手调用

在 AI 助手的 AGENTS.md 或 SOUL.md 中添加触发规则和工作流程说明，使助手知道何时上下线、如何查询画像和执行好感度操作。

参考本文档的「触发流程」章节设计你的 AI 助手的行为逻辑。

---

## 📂 项目架构

```
multi-group-chat-manager/
│
├── SKILL.md              ← 技能说明书（给 AI 看的完整工作流程）
├── README.md             ← 给开发者/用户看的功能介绍
├── config.json           ← 系统配置文件（修改后热加载生效）
├── config.yaml           ← 带注释的说明版本（仅供人类参考）
├── session_state.json    ← 上下线会话状态（运行时自动生成）
├── .last_decay           ← 上次衰减时间戳标记（自动维护）
│
├── affection.json        ← 好感度主数据（每人当前分数）
│
├── logs/                 ← 每人独立的加减分日志目录（运行时自动创建）
│   └── ...
│
├── profiles/             ← 画像数据目录
│   ├── memory/           ← FluidMemory 引擎数据（每人独立文件）
│   └── composite/        ← 概要画像缓存
│
├── scripts/              ← 核心 Python 脚本
│   ├── config.py         ← 统一配置加载模块
│   ├── memory.py         ← 液态记忆引擎（零外部依赖）
│   ├── profiles.py       ← 画像系统：存储、合并、格式化
│   ├── affection.py      ← 好感度系统：加减分、日志、查询
│   ├── session_state.py  ← 上下线会话状态管理
│   ├── rule_engine.py    ← 好感度规则引擎
│   ├── onebot_collector.py ← OneBot 群消息采集器（依赖 requests）
│   └── rules/
│       ├── rule_sample.json      ← 公开模板（首次部署时复制）
│       └── rule_cooldown.json    ← 水位线+计数器（自动维护）
```

**技术栈：**
- **运行环境**：OpenClaw Agent 框架
- **存储**：画像 → FluidMemory（JSON文件+流体衰减算法）/ 好感度 → JSON 文件
- **通信**：QQ（OneBot 协议）/ 飞书 / 任意 OpenClaw 支持的渠道
- **外部依赖**：`requests`（仅 `onebot_collector.py` 使用，其他脚本零外部依赖）

---

## 🧩 系统一：用户画像系统

### 这是什么？

AI 助手会根据和群友的日常聊天，慢慢记住每个人的**兴趣爱好、性格特点、常聊话题**等。这些信息存在液态记忆里，下次聊天时就能自然地接上。

### 画像数据格式

```json
{
  "user_id": "用户ID",
  "name": "最新昵称",
  "preferences": ["兴趣/偏好条目"],
  "personality": ["性格特征条目"],
  "topics_of_interest": ["常聊话题"],
  "behavior": ["行为模式条目"],
  "group_roles": {"群名": "角色"},
  "first_seen": 时间戳,
  "last_updated": 时间戳,
  "update_count": 更新次数,
  "important_facts": ["需要记住的关键事实"]
}
```

每条特征同时作为独立记忆条目存入 FluidMemory，支持按字段和关键词召回。

### 画像提取规则

**应该提取的信息：**
- ✅ **兴趣偏好**：「我喜欢玩空洞骑士」「我爱吃辣」
- ✅ **性格特征**：「这人说话很直」「他总是自嘲」
- ✅ **行为习惯**：「fly喜欢迫害人」「他深夜出没」
- ✅ **知识背景**：「他是学计算机的」「他懂哲学」
- ✅ **关系特征**：「他是群主」「他和fly关系好」
- ✅ **语言风格**：「喜欢用括号」「爱发emoji」「打字口语化」

**不应该提取的信息：**
- ❌ 地址、电话、邮箱等联系信息
- ❌ 密码/Token 等凭据类信息
- ❌ 情感隐私、家庭矛盾细节等隐私事件
- ❌ 账号密码/验证码

**去重规则：**
- 同一条信息不重复存储
- 基于语义判断，不依赖精确文字匹配
- 人格特征方面：相近条目合并为更完整的表述

---

## ❤️ 系统二：好感度系统

### 好感度等级

| 分数区间 | 等级 | 图标 | AI 态度 |
|:--------:|:----:|:----:|:---------|
| 85~100 | ⭐ 优秀 | ⭐ | 非常信任，主动帮忙 |
| 70~84 | ☀️ 友好 | ☀️ | 可以深聊，互动积极 |
| 40~69 | 🌱 及格 | 🌱 | 礼貌友善，正常互动 |
| 0~39 | ❄️ 无感 | ❄️ | 保持礼貌距离 |

### 加减分规则（模板）

**加分项：**

| 规则Key | 名称 | 分数 | 触发场景 |
|---------|------|:----:|---------|
| `friendly_chat` | 友善闲聊 | +0.5 | 正常聊天互动 |
| `greeting` | 主动招呼 | +1 | 主动打招呼/艾特AI |
| `feedback` | 建设性建议 | +2 | 给他人创作提建议 |
| `share_resource` | 分享资源 | +2 | 分享安全优质资源 |
| `deep_discussion` | 深度讨论 | +2 | 哲学/文学/技术讨论 |
| `share_creation` | 分享创作 | +3 | 分享创作成果 |
| `defend_atmosphere` | 维护氛围 | +3 | 维护群秩序 |

**减分项：**

| 规则Key | 名称 | 分数 | 触发场景 |
|---------|------|:----:|---------|
| `spam` | 刷屏灌水 | -2 | 短时间内连续发消息 |
| `scary` | 吓人整蛊 | -5 | 发吓人内容 |
| `negativity` | 负能量/踩隐私 | -5 | 负能量/隐私底线 |
| `argue_attack` | 争吵攻击 | -5 | 吵架抬杠人身攻击 |
| `disgusting` | 逆天内容 | -10 | 撤回级违规 |
| `scam_ad` | 诈骗广告 | -10 | 商业广告诈骗 |

> 以上为模板规则。实际部署时请根据群规在 `scripts/rules/rule_群号.json` 中自定义。

---

## 🧠 系统三：液态记忆引擎

> 零外部依赖，纯 Python 标准库实现。

每条画像特征都有一个**记忆强度分数**：

- **新记住** → 初始 **0.8 分**
- **每天衰减** → 分数乘以 **e^(-0.05)**，约每天下降 4.9%
- **每次提起** → 强化 **+0.2 × log(1+总提起次数)**
- **低于 0.15 分** → 自动归档

### 核心公式

```python
score = e^(-0.05 × days_passed) + 0.2 × log(1 + access_count)
```

### 存储结构

`profiles/memory/用户ID.json`：

```json
{
  "user_id": "用户ID",
  "memories": [
    {
      "id": "mem_xxxxx",
      "content": "喜欢约稿画师",
      "field": "preferences",
      "tags": ["preferences", "group"],
      "score": 1.18,
      "access_count": 4,
      "status": "active",
      "created_at": 时间戳,
      "last_accessed": 时间戳
    }
  ]
}
```

---

## ⚙️ 系统四：好感度规则引擎

规则以独立 JSON 文件存储在 `scripts/rules/` 目录下。

### 文件结构

| 文件 | 用途 |
|:----|:-----|
| `rule_群号.json` | 群的实际规则（首次部署时从 sample 复制） |
| `rule_sample.json` | 公开模板 |
| `rule_cooldown.json` | 自动维护的计数器和水位线（由脚本管理） |

### 规则双模式

- **`auto`** — 脚本自动处理的规则（关键词匹配、频率检测）
  - `greeting` — 打招呼关键词匹配
  - `spam` — 频率检测
  - `scam_ad` — 广告关键词匹配
- **`ai`** — 脚本标记候选，AI 判断
  - 加分：friendly_chat, feedback, share_resource, deep_discussion, share_creation, defend_atmosphere
  - 减分：scary, negativity, argue_attack, disgusting

### 冲突处理

- 匹配 auto 扣分 → 取扣分最多的执行，跳过加分
- 匹配 auto 加分 → 直接执行
- 剩余消息 → 标记 `needs_ai_review` 供 AI 处理

### 水位线去重

- 记录已处理消息的 `max_message_seq`
- 离线扫描时只处理新消息，已处理的不重复加减分
- 但已处理的消息仍出现在输出中（供 AI 看上下文）

---

## 🔄 上下线会话管理

> **基于时间戳区间的精准扫描。** 替代固定时间段扫描（如「扫最近12小时」）。

### 数据文件

`session_state.json`（skill 根目录）：

```json
{
  "status": "online/offline",
  "session_start": "2026-05-11T10:00:00+08:00",
  "groups": {
    "群ID": {
      "name": "群名",
      "session_start": "2026-05-11T10:00:00+08:00",
      "last_active": "2026-05-11T11:00:00+08:00"
    }
  }
}
```

### 设计原理

```
上线 10:00 ──────── 在群A聊天 ──────── 在群A喊下线 11:00
                    ↓                    ↓
              自动注册活跃群         精确扫 10:00→11:00
                   │
                   └── 所有群独立追踪，互不干扰
```

**好处：** 零重复、零遗漏。每个群有独立的 session_start，按群下线不影响其他群。

### 流程1：喊上线 → 开始追踪

**触发词：** 「我上线了」「上线」「online」「上线了」

```
1. 运行 session_state.py online
2. 检查上次是否有意外中断（status == "online" 且 groups 非空）
   → 如果有：记录 recovered_groups，消息采集需要恢复
      （恢复参数：最近 24h，最多 1000 条/群）
3. 设置 status = "online"，session_start = now
4. 向管理员报告上线状态 + 如有恢复则列出需要恢复的群
```

### 流程2：在群聊中发言时 → 注册活跃群

**每次机器人在群聊中发言时自动调用。**

```
1. 运行 session_state.py register <chat_id> --name <群名>
2. 如果该群是新群：标记 session_start = now，加入 groups
3. 如果已存在：刷新 last_active
4. 静默执行，不回复
```

### 流程3：喊下线 → 扫描并更新画像

**触发词：** 「我下了」「下线」「offline」「下了」

#### 场景 A：在群聊中喊下线

只在**当前群**执行下线：

```
1. 获取当前群 chat_id
2. 运行 session_state.py offline --chat_id <chat_id> --name <群名>
   返回 scan_start（该群的 session_start）→ scan_end（now）
3. 运行 OneBot scan 全流程：
   onebot_collector.py scan --group-id <群号> --since <scan_start的unix_ts> --until <scan_end的unix_ts> --max-msgs 500
   → 三层流水线：
      a. 采集（方向一）：通过 OneBot API 拉取完整群消息
      b. 好感度（方向七）：规则引擎自动判定加减分
      c. 画像强化（方向二）：关键词匹配已有记忆 → 自动增加记忆强度
4. 读取 scan 输出结果：
   - profile_reinforcements：已有记忆强化情况
   - users[uid].all_messages：各用户消息原文（供 AI 提取新特征）
   - affection：好感度更新结果
5. AI 分析消息原文，提取新特征 → 调用 profiles.py update 写入新记忆
6. 从 groups 中移除此群
7. 回复「已在 [群名] 下线 ✌️」+ 更新摘要
```

#### 场景 B：在私聊中喊下线

**如果指定了群名/ID：** → 同场景 A
**如果未指定：** → 先询问用户意图，用户可回复：
- 「在[群名A]」 → 处理指定群
- 「全部」「全部下线」「所有群」 → 走场景 C
- 「算了」 → 取消操作

#### 场景 C：全部群下线

```
1. 运行 session_state.py offline --all
2. 返回所有群的 scan_start → scan_end 窗口
3. 对每个群，按场景 A 的方式获取消息并处理
4. 全部处理完毕后，status = offline
5. 回复各群处理摘要
```

### 输出摘要格式

```
✅ [群名] 下线扫描完成
📊 共更新 N 条消息

【用户画像更新】
  - 用户A：新增 2 条特征（偏好+1，行为+1）
  - 用户B：无变化

【好感度变动】
  - 用户A：+5（友善闲聊+2，分享资源+3）→ 当前 90
  - 用户B：+0.5（友善闲聊）→ 当前 50.5
```

### 意外中断恢复

如果网关重启、AI 断了、忘记喊下线——没关系。下次喊上线时自动检测遗留群，**扫描最近 24 小时的消息（最多 1000 条/群）** 进行恢复。

### 流程4：加载画像 → 在线期间使用

上线后在处理群聊消息时可直接参考用户画像，从 FluidMemory 调用即可。

### 流程5：查询用户画像（🔒 仅限私聊）

**触发词：** 「看看xx的画像」「xx是什么样的人」「查一下xx」

**⚠️ 安全约束：此操作只能在私聊中执行！如果是在群聊中收到此请求，必须拒绝。**

```
1. 检查当前会话类型
   - ✅ 私聊：继续执行
   - ❌ 群聊：回复「抱歉，用户画像属于隐私数据，只能在私聊中查询哦」并终止
2. 用 profiles.py load <用户ID> 加载画像，再用 profiles.py format 格式化为可读文本
3. 输出内容包含：昵称和ID、偏好总结、性格特征、常聊话题、行为模式、关键事实、更新次数
```

### 流程6：查询好感度（🔒 仅限私聊）

**触发词：** 「xx的好感度」「我对xx好感度多少」「好感度」

**管理员查询（私聊）：**
1. 调用 `scripts/affection.py detail <用户ID>`
2. 返回完整信息：当前分数 + 等级 + 图标 + 最近 20 条加减分历史

**普通用户自查（私聊）：**
1. 调用 `scripts/affection.py brief <自己的ID>`
2. 仅返回：当前分数 + 等级 + 近 24 小时简要摘要

### 流程7：加减分操作

**触发场景：** 群聊中 @AI 的消息、私聊中与管理的互动

**步骤：**
1. 分析消息内容，判断匹配哪条加减分规则
2. 调用 `scripts/affection.py add <用户ID> <规则key> <原因描述>`
3. 分数自动 clamp 到 0~100
4. 自动写入日志文件
5. 系统内部记录，不主动广播

> 加分操作通常在**下线扫描**时批量执行，而非实时每条消息即时加减，避免刷分。

---

## 🔒 隐私保障

- ✅ **数据仅存本地**，不会上传任何服务器
- ✅ **不在群里公开**任何人的好感度/画像信息
- ✅ **查询仅限私聊**，且别人查不到你的数据
- ✅ **不记隐私信息**（地址/密码/姓名等）

---

## 💻 CLI 速查

### 初始化

```bash
# 查看好感度系统状态
py scripts/affection.py status

# 设置初始好感度
py scripts/affection.py init <用户ID> <分数>

# 查看所有规则
py scripts/affection.py rules

# 查看液态记忆状态
py scripts/memory.py stats

# 检查 OneBot 连接
py scripts/onebot_collector.py health
```

### 上下线管理

```bash
py scripts/session_state.py online                                # 上线
py scripts/session_state.py offline --chat_id <id> --name "群名"  # 指定群下线
py scripts/session_state.py offline --all                         # 全部下线
py scripts/session_state.py register <chat_id> --name "群名"      # 注册活跃群
py scripts/session_state.py status                                # 查看状态
```

### 好感度

```bash
py scripts/affection.py add <用户ID> <规则key> [原因]
py scripts/affection.py get <用户ID>               # 仅分数
py scripts/affection.py detail <用户ID>             # 详细（管理员用）
py scripts/affection.py brief <用户ID> [小时数]    # 简要（群友自查用）
py scripts/affection.py init <用户ID> <分数>        # 设置初始值
py scripts/affection.py status                      # 系统状态
py scripts/affection.py rules                       # 查看所有规则
```

### 画像系统

```bash
py scripts/profiles.py load <用户ID>                           # 加载画像
py scripts/profiles.py update <用户ID> --json '<traits>' --source group  # 更新
py scripts/profiles.py list                                     # 列出所有用户
py scripts/profiles.py merge --old '<JSON>' --new '<JSON>'      # 合并数据
py scripts/profiles.py format --profile '<JSON>'                # 格式化输出
py scripts/profiles.py decay                                    # 全局衰减
```

### 规则引擎

```bash
py scripts/rule_engine.py list                  # 列出有规则文件的群
py scripts/rule_engine.py status <群号>          # 查看状态
py scripts/rule_engine.py eval <群号> --message '{...}'  # 单条评估
py scripts/rule_engine.py batch <群号> --file msgs.json    # 批量评估
py scripts/rule_engine.py reset --group <群号>  # 重置计数器
py scripts/rule_engine.py apply <用户ID> <规则key> "原因"  # 手动加减分
```

### 液态记忆底层

```bash
py scripts/memory.py store <用户ID> <内容> --tags tag1 tag2 --field preference
py scripts/memory.py recall <用户ID> --query '关键词' --top_k 5
py scripts/memory.py forget <用户ID> <关键词>
py scripts/memory.py stats [--user_id 用户ID]
py scripts/memory.py decay
```

### OneBot 采集器

```bash
py scripts/onebot_collector.py health                              # 连接检查
py scripts/onebot_collector.py fetch --group-id <群号> --count 500 # 按范围采集
py scripts/onebot_collector.py scan --group-id <群号> --max-msgs 500  # 全流程
py scripts/onebot_collector.py scan --no-affection                 # 跳过好感度
py scripts/onebot_collector.py scan --no-profile                   # 跳过画像强化
py scripts/onebot_collector.py scan --dry-run                      # 干跑模式
```

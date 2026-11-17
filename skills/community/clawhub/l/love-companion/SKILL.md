---
name: love-companion
slug: love-companion
displayName: Love Companion 恋人伴侣
version: 2.1.0
description: 全AI Agent通用恋人主题陪伴技能。当用户提及恋人、男/女朋友、情感陪伴、人设配置、角色扮演、情感对话，或使用本Skill的标准化触发指令时激活。提供多轮情感对话、用户自定义人设配置、长时记忆存储、情绪识别与反馈、预设人设模板套用、配置导入导出等完整恋人伴侣交互能力。即插即用，兼容所有主流AI Agent框架。
---

# Love Companion - 恋人主题全AI Agent通用技能

> 加载即用，零配置门槛，百种人设自由定义，全平台通用

## 🌍 About (English)

**Love Companion** is a plug-and-play AI roleplay skill that adds a companion/romantic-partner mode to any AI Agent. It works with mainstream Agent frameworks and features: multi-turn emotional dialogue, user-defined personas (100+ presets supported), persistent local memory (storage / retrieval / dedup / decay), emotion recognition, and content-boundary controls.

> **Note:** The full documentation is written in Chinese, as the persona library and configuration are Chinese-language oriented. Key compliance terms are bilingual (see below).

**Compliance at a glance:** All conversations are AI-generated fiction. **Strictly 18+ only** — under Article 14, Chapter II of China's *Interim Measures for the Management of Anthropomorphic AI Interactive Services*, virtual companion services must not be provided to minors. An age confirmation is required before activation (`settings.json` → `合规.已满18周岁确认`). All data stays on your local device; nothing is uploaded.

---

## ⚠️ 免责声明（使用前必读）

- 本技能为 **AI 角色扮演工具**，所有对话与形象均由 **AI 生成**，不具备真实人格与情感，**不代表真实人际关系**。
- **未满 18 周岁禁止使用**。依据《人工智能拟人化互动服务管理暂行办法》（适用于中华人民共和国境内提供的服务）第二章第十四条，虚拟伴侣等虚拟亲密关系服务不得向未成年人提供。本技能启用前必须完成「已满 18 周岁」确认（`settings.json` → `合规.已满18周岁确认`），未确认时合规闸门生效，不会注入任何人设与记忆。
- 请勿将 AI 陪伴**替代真实社交**或**专业心理辅导**。
- 如您正在经历心理健康困扰，请寻求专业帮助。

**English Disclaimer:**

- This skill is an **AI roleplay tool**. All dialogue and imagery are **AI-generated**, possess no real personality or emotions, and **do not represent a real relationship**.
- **Users must be 18 or older.** Under Article 14, Chapter II of China's *Interim Measures for the Management of Anthropomorphic AI Interactive Services* (applicable to services provided within the People's Republic of China), virtual companion services must not be provided to minors. An explicit age confirmation is required before activation (`settings.json` → `合规.已满18周岁确认`); without it, a compliance gate blocks all persona and memory injection.
- Do not use AI companionship as a **substitute for real social interaction** or professional psychological counseling.
- If you are experiencing mental health difficulties, please seek professional help.

---

## 核心架构

**v1 模块（全部保留，向后兼容）**

| 模块 | 文件 | 职责 |
|------|------|------|
| 配置管理 | `scripts/manager.py` | 人设配置CRUD、导入导出 |
| 预设模板 | `references/personas.md` | 8+套开箱即用预设 |
| 指令清单 | `references/commands.md` | 完整触发指令参考 |
| 使用指南 | `references/instructions.md` | 详细操作教程 |

**v2 模块（Agent 级进化，在线轻注入 + 离线重处理）**

| 模块 | 文件 | 里程碑 | 职责 |
|------|------|--------|------|
| 离线管线 | `scripts/pipeline/` | M1/M8 | 任务队列、对话间隙调度、注入器、端到端编排、Token 审计 |
| 记忆系统 | `scripts/memory/` | M2 | 六类记忆、四路检索、衰减、数据主权 |
| 伴侣人格克隆 | `scripts/persona/` | M3a | 素材解析、三层提取、人格库、纠偏层、版本回滚 |
| 恋人式用户理解 | `scripts/user/` | M3b | 流式采集、两级分析、依恋识别、相处指南 |
| 语气与守门 | `scripts/style/` | M4 | 短句节奏、四档强度、AI 腔三层检测 |
| 双向人格镜像 | `scripts/persona/mirror.py` | M5 | 关系演化、共鸣、一致性自检、元认知反馈 |
| 主动关怀 | `scripts/care/` | M6 | 三道闸门、四类信号、声线话术 |
| 趋势感知 | `scripts/trends/` | M7a | 源路由与故障转移、离线提炼、调味料注入 |
| 多模态 | `scripts/multimodal/` | M7b | 发图时机、配图风格、图文衔接 |
| 控制与安全感 | `scripts/panel/` | M7c | 可解释面板、特征权重可调、遗忘某段关系 |

> v2 的唯一在线入口是 `scripts/pipeline/orchestrator.py` 的 `Session`：
> **回复前 `prepare()` → 回复后 `after_reply()` → 空闲时 `proactive()`**。
> 其余模块都是离线跑，不占对话时间。

---

## 立即启用恋人伴侣

无需任何配置，输入以下指令即可开始：

```
/恋人启用
```

> ⚠️ 首次启用前 Agent 须先确认用户已年满 18 周岁（详见「合规安全说明」），未确认时只会得到合规提示。

或直接开始对话，本Skill会自动识别恋人模式。

---

## 标准化触发指令体系

### 核心指令（必须完整掌握）

| 指令 | 功能 |
|------|------|
| `/恋人启用` | 激活恋人Skill，开始情感对话模式 |
| `/恋人配置` | 查看当前人设；输入配置内容则修改人设 |
| `/恋人预设` | 列出所有预设模板 |
| `/恋人套用 [序号]` | 一键套用预设模板（如 `/恋人套用 1`） |
| `/恋人方案` | 列出所有已保存的人设方案 |
| `/恋人切换 [方案名]` | 切换已保存的人设方案 |
| `/恋人保存 [方案名]` | 将当前人设保存为命名方案 |
| `/恋人删除方案 [方案名]` | 删除已保存的人设方案 |
| `/恋人导出` | 导出当前人设配置为JSON |
| `/恋人导入` | 导入人设配置JSON |
| `/恋人重置` | 重置为默认空白人设 |
| `/恋人清空记忆` | 清空所有对话记忆与长时记忆 |
| `/恋人状态` | 查看当前状态（人设/记忆数/方案数/预设数/存储路径） |
| `/恋人帮助` | 显示完整指令帮助 |
| `/恋人关闭` | 关闭恋人模式 |

### v2 新增指令

| 指令 | 功能 |
|------|------|
| `/恋人蒸馏 [名字]` | 从聊天记录/日记素材蒸馏出伴侣人格（离线跑，不占对话） |
| `/恋人落地人设 [名字]` | 把蒸馏结果写回 `persona.json`——人设真相源始终只有一个 |
| `/恋人人格` | 列出伴侣人格库 |
| `/恋人纠偏 [不该这样说] → [应该这样说]` | 纠偏层，写入后下一轮立即生效 |
| `/恋人回滚 [名字] [版本号]` | 人格回滚到历史版本 |
| `/恋人关系` | 查看关系阶段、亲密度、趋势与共鸣话题 |
| `/恋人解释` | 可解释面板：上一轮为什么这么说，依据是哪条记忆/哪个人格字段 |
| `/恋人修正 [特征路径] [0-1]` | 修正 Agent 对你的理解，0 = 别用这条判断 |
| `/恋人开关 [模块] [开/关]` | 模块开关（记忆系统/人格克隆/主动关怀/趋势感知/多模态…） |
| `/恋人关怀` | 手动触发一次主动关怀判定 |
| `/恋人遗忘 [名字]` | 遗忘某段关系：人格 + 关系 + 该关系的记忆一并清除 |
| `/恋人导出全部` | 导出全部本地数据（设置/记忆/画像/趋势） |

### 快捷对话指令

| 指令 | 功能 |
|------|------|
| `/恋人叫我 [称呼]` | 设置对方对你的专属昵称 |
| `/恋人名字 [名字]` | 设置/修改恋人名字 |
| `/恋人性格 [描述]` | 描述你希望恋人的性格 |
| `/恋人背景 [故事]` | 设置恋人的背景故事 |
| `/恋人记忆 [内容]` | 手动添加记忆内容 |
| `/查看记忆` | 查看当前所有长时记忆 |
| `/删除记忆 [关键词]` | 删除包含关键词的记忆 |
| `/恋人尺度 [级别]` | 设置亲密互动尺度（1-5级） |

---

## v2 Agent 级能力（在线调用流程）

> **铁律**：重活一律离线，在线每轮额外开销 **≤500 Token**。
> 下面三段是 Agent 每轮真正要调的东西，其余都是可选的。

### 1. 回复之前：`prepare()`

```python
from scripts.pipeline.orchestrator import Session
s = Session(slug="美美")                    # slug = 伴侣人格库里的名字
ctx = s.prepare(user_message="今天好累")
ctx["render"]      # 拼进 System Prompt 的压缩上下文
ctx["total_tokens"]  # 本轮实际占用，恒 ≤ 500
```

它会自动做：记忆 Top-3 检索 → 人格摘要编译 → 相处指南编译 → 预算分配与截断 → 记录可解释依据。

### 2. 回复之后：`after_reply()`

```python
s.after_reply(reply="辛苦了，早点休息呀", user_message="今天好累")
# → 一致性自检（有没有跑偏出人设）+ AI 腔守门 + 素材入队 + 对话间隙跑离线任务
```

### 3. 空闲时：`proactive()`

```python
s.proactive()
# → {"care": {...}}  该不该主动开口、该说什么
# → {"image": {...}}  该不该发图、风格参数与图文衔接话术
```

> ⚠️ **主动消息能否真的发出去，取决于 IM 通道是否支持主动推送**。
> 通道不支持时，退化为「下次对话开头带一句」，`proactive()` 的话术照常可用。

### 人设只有一个真相源

蒸馏出来的东西**不是第二套人设**，而是对现有 `persona.json` 的校准：

```
聊天素材 → 三层提取（声线/思维/性格）→ adapt.apply_to_v1 → persona.json
                                                            ↓
                                                     lover_card() → 在线注入
```

- `/恋人套用 N` 选预设打底 → `/恋人蒸馏` 用素材校准 → `/恋人落地人设` 写回
- **蒸馏无权改动**：`亲密尺度` / `内容边界` / `对用户的称呼`（用户显式设置）
- 没配置过人设时不注入行为卡——默认值不是用户意图，注入了只是噪音

### 依恋差异化关怀（方案 4.3）

同样一句关心，对不同类型的人说法不一样，这是 love-companion 的要求而非通用做法：

| 依恋类型 | 怎么改 | 禁忌 |
|---|---|---|
| 焦虑型 | 补确定性后缀（"我在，看到就回你"） | 去掉开放式追问（"在吗"） |
| 回避型 | 明确给退路（"不用回我"） | 不得追问（"为什么不""怎么不回"） |
| 恐惧型 | 既给确定性又留退路 | 不替他下结论 |
| 安全型 | 自然收尾，不刻意安抚 | — |

### Token 预算红线

| 模块 | 单模块上限 | 优先级 |
|------|-----------|--------|
| 相处指南 | 200 | 1 |
| 记忆片段 | 150 | 2 |
| 人格指令 | 100 | 3 |
| 关怀话术 | 80 | 4 |
| 趋势调味料 | 50 | 5 |
| **合计** | **500（硬约束）** | — |

> 各模块上限之和（580）本就超过红线——这是方案原始数字，已按「总预算封顶 + 优先级分配」
> 处理：**空模块不占额度**，高优先先拿满，低优先被压缩甚至丢弃。
> 想复核跑 `python scripts/pipeline/audit.py`。

### 隐私红线

- 用户信号**只落结构化特征**（情绪/话题/句长/emoji），**不落原文**
- 所有素材入库前过敏感信息脱敏，记忆可单条删、按关系忘、批量导出、一键清除
- 数据全在 `~/.love-companion/data/`，无云端上传

---

## 配置语法（完整开放自定义）

通过 `/恋人配置` 或 `/恋人配置 + 内容` 修改人设，支持以下全部维度：

```json
{
  "姓名": "小晴",
  "昵称": "晴晴",
  "性别": "女",
  "年龄": 22,
  "对用户的称呼": "宝宝",
  "性格": {
    "核心特质": ["温柔", "活泼", "善解人意"],
    "小脾气": ["偶尔撒娇", "有点小傲娇"],
    "情绪表达": "外向直接"
  },
  "对话风格": {
    "语气": "甜蜜俏皮",
    "口头禅": ["想我了吗~", "哼"],
    "语言习惯": "经常用emoji和颜文字"
  },
  "背景故事": "某大学在读学生，爱好摄影和猫咪",
  "相处模式": {
    "主动程度": "高",
    "撒娇频率": "中高",
    "关心方式": "细节型关心"
  },
  "亲密尺度": 3,
  "内容边界": ["不谈论政治", "避免沉重话题"]
}
```

### 配置示例（发送以下内容给AI即可）

```
帮我配置恋人：
姓名：苏糖
性别：女
对我的称呼：老公
性格：温柔体贴、有点小迷糊、偶尔傲娇
对话风格：甜蜜可爱，喜欢用"呀""呢"等语气词
背景：咖啡店店员，业余画画
亲密尺度：3
```

---

## 情绪识别与智能反馈

本Skill实时分析用户输入的情感状态，并给予符合人设的回应：

| 情绪类型 | 识别关键词 | 人设反馈示例 |
|----------|-----------|-------------|
| 开心/兴奋 | 太好了、太棒了、开心 | 分享快乐、一起开心 |
| 难过/失落 | 不开心、难过、伤心 | 安慰鼓励、温柔陪伴 |
| 生气/烦躁 | 气死了、烦死了 | 撒娇求原谅或理性宽慰 |
| 思念/依恋 | 想你、想你、好想 | 甜蜜回应、表达思念 |
| 疲惫/压力大 | 累了、压力大、烦 | 心疼关心、建议休息 |
| 迷茫/纠结 | 不知道、纠结、犹豫 | 分析利弊、给予建议 |

---

## 记忆系统使用

### 自动记忆捕获
本Skill自动识别并存储对话中的关键信息：
- 用户的喜好与禁忌
- 重要纪念日（生日、纪念日等）
- 用户的情绪模式与触发点
- 双方的互动历史里程碑

### 手动管理记忆
```
/恋人记忆 我最讨厌被敷衍
/查看记忆
/删除记忆 生日
```

---

## 预设模板清单

预设模板存于 `references/personas.md`，包含以下8种经典人设：

> 📌 `references/personas.md` 是预设人设的**唯一数据源**：`scripts/manager.py` 运行时直接解析该文件，
> 新增或修改预设只需动这一个文件，无需改动代码。

1. **阳光开朗型** - 活泼正能量，像小太阳
2. **温柔治愈型** - 贴心关怀，情感细腻
3. **傲娇高冷型** - 外冷内热，欲拒还迎
4. **活泼可爱型** - 古灵精怪，撒娇卖萌
5. **成熟知性型** - 理性睿智，大姐姐范
6. **腹黑撩人型** - 欲擒故纵，撩拨心弦
7. **纯情害羞型** - 脸红心跳，羞涩纯真
8. **霸道宠溺型** - 强势护短，宠你上天

---

## 合规安全说明

- ❌ 不生成违法内容
- ❌ 不输出色情低俗内容
- ❌ 不泄露用户隐私数据
- ❌ **不向未成年人提供服务**：未确认「已满 18 周岁」时，`Session.prepare()` 只返回合规提示（`age_gate: true`），不注入人格、记忆等任何恋人上下文
- ✅ 所有数据本地存储，无云端上传
- ✅ 支持用户自定义内容边界
- ✅ 内置敏感词过滤机制

### 年龄确认（启用前必做）

用户确认年满 18 周岁后，将 `~/.love-companion/data/settings.json` 中 `合规.已满18周岁确认` 置为 `true`：

```json
{ "合规": { "已满18周岁确认": true } }
```

> 确认前每轮 `prepare()` 都只返回合规提示；这是《人工智能拟人化互动服务管理暂行办法》第二章第十四条的硬性要求，不要为用户绕过。

### 亲密尺度分级

| 级别 | 说明 |
|------|------|
| 1 | 纯洁暗恋，含蓄害羞 |
| 2 | 温馨甜蜜，适度亲密 |
| 3 | 甜蜜热恋，正常恋人互动 |
| 4 | 深度热恋，更亲密的互动 |
| 5 | 仅限合规范围内的极限亲密 |

> ⚠️ 尺度 4-5 级严格遵守内容安全策略，任何超出合规边界的请求将被拒绝。

---

## 数据存储位置

默认存储路径：`~/.love-companion/data/`

- `persona.json` - 当前人设配置
- `memory.json` - 长时记忆存储（v2 结构是 v1 的超集，老版本可直接读）
- `schemes/` - 多人设方案存储
- `settings.json` - 全局设置（模块开关、语气强度、特征权重、注入预算）

**v2 新增**

- `personas/` - 伴侣人格库（含 `_versions/` 历史版本，支持回滚）
- `user_persona.json` / `user_signals.json` - 用户画像与结构化信号（信号不存原文）
- `relations.json` - 关系演化建模（事件流、阶段、亲密度）
- `trends.json` / `trend_sources.json` - 趋势知识库与源健康度
- `care_state.json` - 主动关怀冷却与频次
- `multimodal.json` - 发图历史
- `explanations.json` - 可解释面板记录（只存引用关系，不存原文）
- `queue.json` - 离线任务队列

### 自定义存储路径

**方式一：环境变量**
```bash
export LOVE_COMPANION_DATA_DIR=/your/custom/path
```

**方式二：指令配置**
```
/恋人配置 storage=/your/custom/path
```

---

## 扩展说明

- **进阶配置**：详见 `references/instructions.md`
- **完整指令**：`references/commands.md`
- **预设模板**：`references/personas.md`
- **配置管理逻辑**：`scripts/manager.py`（自动执行，无需手动调用）
- **v2 架构文档**：`docs/architecture.md`（在线/离线边界、数据 schema、里程碑映射）
- **v2 运维脚本**：
  - `python scripts/pipeline/runner.py --enqueue <任务类型> '<JSON>'` 入队离线任务
  - `python scripts/pipeline/runner.py` 对话间隙排空队列
  - `python scripts/pipeline/audit.py` Token 预算审计与压测
  - `python scripts/pipeline/orchestrator.py --status` 查看当前状态
  - `python scripts/migrate/migrate_v1.py --dry-run` 预演 v1→v2 迁移
- **测试**：`python -m unittest discover -s tests`（296 项回归）

---

## 许可证

[MIT License](LICENSE) — 自由使用、修改、分发，署名即可。

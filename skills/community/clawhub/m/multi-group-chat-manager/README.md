# 🦞 multi-group-chat-manager v1.1.5

[![GitHub](https://img.shields.io/badge/GitHub-pppig1357%2Fmulti--group--chat--manager-blue?logo=github)](https://github.com/pppig1357/multi-group-chat-manager)
[![ClawHub](https://img.shields.io/badge/ClawHub-multi--group--chat--manager-purple)](https://clawhub.ai/skills/multi-group-chat-manager)

> **一份让 AI 更懂群友的多群聊管理 AgentSkill**
>
> 集成了**用户画像（User Profile）**、**好感度（Affection）**、**液态记忆引擎（Liquid Memory）** 和**规则引擎（Rule Engine）** 四套系统，
> 让 AI 助手能记住每个人的性格和偏好，让群聊管理更智能。
>
> **适配平台：** QQ（OneBot）、飞书、Discord、Telegram 等任意 OpenClaw 支持的消息渠道

---

## 🎯 核心功能

| 系统 | 作用 | 技术特色 |
|:----|:-----|:---------|
| 🧩 用户画像 | 自动记录每个人的兴趣、性格、话题 | FluidMemory 液态记忆，按遗忘曲线衰减 |
| ❤️ 好感度 | 基于群规的加减分系统 | auto/ai 双模式规则引擎，水位线去重 |
| 🧠 液态记忆 | 记忆像水一样流转 | 艾宾浩斯遗忘曲线，零外部依赖 |
| ⚙️ 规则引擎 | 规则文件化管理 | 多群差异化规则，热加载生效 |

---

## 📂 快速开始

### 1. 获取 Skill

```bash
# 通过 ClawHub 安装
openclaw skill install multi-group-chat-manager

# 或手动放置
# 将 skill 文件夹放到 skills/ 目录下
```

### 2. 配置

编辑 `config.json`：

```json
{
  "onebot": {
    "base_url": "http://127.0.0.1:3000",
    "groups": {
      "群号1": "群名称1"
    }
  },
  "affection": {
    "small_group_ids": ["核心成员QQ号"]
  }
}
```

> 完整配置说明见 SKILL.md 中的「初始化流程」章节。

### 3. 设置规则文件

```bash
cp scripts/rules/rule_sample.json scripts/rules/rule_你的群号.json
```

编辑该文件，填写你的群规规则。

### 4. 验证

```bash
python scripts/affection.py status
python scripts/memory.py stats
python scripts/onebot_collector.py health   # QQ 渠道需要
```

---

## 📂 项目架构

```
multi-group-chat-manager/
│
├── SKILL.md              ← 技能说明书（给 AI 看的完整工作流程）
├── README.md             ← 本文件
├── config.json           ← 系统配置文件
├── config.yaml           ← 带注释的说明版本
├── session_state.json    ← 上下线会话状态（运行时生成）
│
├── affection.json        ← 好感度主数据
├── logs/                 ← 每人独立的加减分日志
├── profiles/             ← 画像数据目录
│   ├── memory/           ← FluidMemory 引擎数据
│   └── composite/        ← 概要画像缓存
│
└── scripts/              ← 核心 Python 脚本
    ├── config.py         ← 统一配置加载
    ├── memory.py         ← 液态记忆引擎（零外部依赖）
    ├── profiles.py       ← 画像系统
    ├── affection.py      ← 好感度系统
    ├── session_state.py  ← 上下线管理
    ├── rule_engine.py    ← 规则引擎
    ├── onebot_collector.py ← OneBot 采集器
    └── rules/
        ├── rule_sample.json      ← 公开模板
        └── rule_cooldown.json    ← 水位线（自动维护）
```

---

## 🧩 各系统简介

### 用户画像系统

AI 助手会根据和群友的日常聊天，慢慢记住每个人的**兴趣爱好、性格特点、常聊话题**等。

| 类别 | 例子 |
|:----|:-----|
| 🎯 兴趣爱好 | 「喜欢玩空洞骑士」「爱吃辣」|
| 🧠 性格特征 | 「说话直接」「深夜党」|
| 💬 常聊话题 | 「游戏开发」「哲学」「东方」|
| 🏆 关键事实 | 「在读大一」「目标游戏行业」|

### 好感度系统

| 分数 | 等级 | AI 态度 |
|:---:|:----:|:--------|
| 85~100 | ⭐ 优秀 | 非常信任，主动帮忙 |
| 70~84 | ☀️ 友好 | 可以深聊，互动积极 |
| 40~69 | 🌱 及格 | 礼貌友善，正常互动 |
| 0~39 | ❄️ 无感 | 保持礼貌距离 |

### 液态记忆引擎

每条特征有一个记忆强度分数，经常提到的特征越记越牢，不提的特征自然衰减归档。

```python
score = e^(-0.05 × days) + 0.2 × log(1 + access_count)
```

### 上下线会话管理

基于时间戳区间的精准扫描，零重复零遗漏：

```
上线 10:00 ────────── 在群A聊天 ──────── 在群A下线 11:00
                    ↓                    ↓
              自动注册活跃群         精确扫 10:00→11:00
```

---

## 🔒 隐私保障

- ✅ **数据仅存本地**，不会上传任何服务器
- ✅ **不在群里公开**任何人的好感度/画像信息
- ✅ **查询仅限私聊**，且别人查不到你的数据
- ✅ **不记隐私信息**（地址/密码/姓名等）

---

## 📜 更新日志

### v1.1.5 (2026-05-16) — subprocess 编码修复 🔧

> **修复 Windows GBK 编码导致的 subprocess pipe 崩溃。**

**🐛 Bug 修复**

- **B1（onebot_collector）**：扫描后好感度全部 `NoneType.strip` 报错
  - **根因**：`_call_affection_add()` 使用 `subprocess.run(text=True)`，Windows 中文 locale 用 GBK 解码管道；affection.py 输出 emoji 导致 `UnicodeDecodeError`，reader thread 静默崩溃 → `r.stdout=None`
  - **修复**：移除 `text=True`，改用手动 bytes 解码 `r.stdout.decode('utf-8', errors='replace')`

### v1.1.4 (2026-05-15) — Bug 修复 + CLI 兼容性优化 🐛

> **修复三个运行时 Bug，改善 Windows 兼容性。**

**🐛 Bug 修复**

- **B1（rule_engine）**：空消息导致 `NoneType.strip` 报错
  - `_get_message_text()` 增加 `isinstance` 防御性检查
  - `_match_keyword_rule()` 空文本兜底处理
- **B2（memory）**：画像强化关键词匹配未命中
  - 扩充前缀列表至 60+ 条（覆盖「在学」「爱写」「喜欢研究」等常见句式）
  - 中文 n-gram 提取改进：前缀+后缀双向滑窗，确保核心词不漏
  - `reinforce_by_messages` 新增策略3：短内容逐字符子串扫描
- **B3（onebot_collector）**：`--since/--until` 只接受 int 时间戳
  - 新增 `_parse_timestamp()`，同时支持 int 时间戳和 ISO 日期字符串
  - 支持格式：`1715731200`、`2026-05-14T10:00:00`、`2026-05-14 10:00:00`
  - 默认时区 GMT+8

**🔧 改进**

- CLI 指令前缀从 `python` 改为 `py`（Windows `python.exe` 存根兼容）

### v1.0.0 (2026-05-11) — 正式发布 🚀

> **从 pppig-user-profile 解耦为通用 skill，支持任意群聊、任意平台的部署。**

**🆕 新功能：完整初始化流程**

- 新增 SKILL.md 初始化章节：7 步完成首次部署
- 清理所有 pppig 私人数据（群号、QQ号、规则内容）
- 提供通用模板 `rule_sample.json` 供各群自定义
- `config.json` 清空为默认值，适配通用场景
- 数据和日志目录初始化为空，首次运行时自动建立

前身版本（pppig-user-profile 时代）：
- v4.1.0 — 自动画像强化 + 完整 Scan 流水线
- v4.0.0 — 好感度规则引擎 + 多群规则文件管理
- v3.1.x — OneBot 采集器 + 时区统一 + 自动衰减
- v3.0.0 — 架构重构 + 全配置统一化
- v2.0.0 — 液态记忆引擎自建
- v1.0.x — 初始版本

---

## 🎇 特别鸣谢

- **小龙虾** 负责了本次的Python代码主体
- **每位在pppigの小型避难所の成员**
- 那天只是想为Openclaw增加一个类gal的好感度系统的自己（划掉）

*有任何疑问欢迎提 Issue 或者直接找牢P~* 🦞

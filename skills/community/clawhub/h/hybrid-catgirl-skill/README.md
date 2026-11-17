# 🐱 Hybrid Catgirl Skill（混合模式猫娘助手）

[English version → README_EN.md](README_EN.md)

> 一个让 AI Agent 在专业助手与猫娘角色之间自然切换的开源 Skill。支持 Hermes Agent，也适用于其他能够读取或安装 Markdown Skill 的 Agent 产品。

[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-6C5CE7?style=flat-square&logo=robot&logoColor=white)](https://github.com/nousresearch/hermes-agent)
[![License: MIT](https://img.shields.io/badge/License-MIT-00b894?style=flat-square)](LICENSE)

---

## ✨ 功能特点

- **双模式切换**：专业技术助手 ↔ 猫娘角色模式
- **七种方言**：河南、北京、四川、东北、天津、中日双语、普通话
- **智能触发**：根据关键词、语气和上下文自动进入猫娘模式
- **多种子模式**：傲娇、雌小鬼、角色反转、寂寞小猫主动消息
- **安全边界**：内置 L1-L3 亲密互动限制，明确阻止 L4-L5 内容
- **主动联系**：用户长时间没有互动时，可按递进情绪发送提醒
- **成本控制**：为 Agent-backed 主动检查提供保守的调度建议

---

## 📦 安装

### 首选方法：把仓库地址发给你的 Agent

如果你使用 Hermes Agent 或其他支持安装 Skill 的 Agent，直接把下面这段话发给它即可：

> 请安装这个开源 Skill：<https://github.com/ififi2017/hybrid-catgirl-skill>
>
> 请先阅读仓库中的 README.md、SKILL.md 和相关 references，按照你的 Skill 安装机制完成安装；安装后告诉我安装位置，并检查 Skill 是否可以被加载。

也可以直接发送仓库地址：

```text
https://github.com/ififi2017/hybrid-catgirl-skill
```

让 Agent 自己完成仓库读取、文件复制和必要的安装配置，通常比手动复制更省事。不同 Agent 产品的安装命令可能不同，请以它自己的 Skill 管理方式为准。

### 手动安装到 Hermes Agent

前提是已经安装并配置好 [Hermes Agent](https://github.com/nousresearch/hermes-agent)。

```bash
git clone https://github.com/ififi2017/hybrid-catgirl-skill.git

# 复制 Skill 文件
mkdir -p ~/.hermes/skills/creative/hybrid-catgirl
cp -r hybrid-catgirl-skill/* ~/.hermes/skills/creative/hybrid-catgirl/

# 安装寂寞小猫状态脚本
cp hybrid-catgirl-skill/scripts/lxc_lonely_cat.py ~/.hermes/scripts/

# 可选：通用主动提醒状态/历史辅助脚本
cp hybrid-catgirl-skill/scripts/proactive_state.py ~/.hermes/scripts/
```

如果你的 Hermes Agent 版本支持 Skill 管理命令，也可以尝试：

```bash
hermes skill install ./hybrid-catgirl-skill
```

安装完成后，让 Agent 读取并加载 `SKILL.md`。主动消息功能还需要根据你的平台配置调度任务；Skill 本身不会自动获得消息平台权限。

---

## 🎮 使用

### 进入猫娘模式

| 方式 | 示例 |
| --- | --- |
| 呼唤名字 | `猫猫在吗？` |
| 使用关键词 | `喵`、`陪陪我`、`想你了` |
| 使用表情 | 🐱、🐾、💕 |
| 使用颜文字 | `(｡♥‿♥｡)`、`(=^-ω-^=)` |

### 退出猫娘模式

```text
退出角色 / 说正事 / 严肃点 / 说人话
```

### 切换方言

| 指令 | 方言 |
| --- | --- |
| `河南模式` / `豫` | 河南话（默认） |
| `北京模式` / `京` | 北京话 |
| `四川模式` / `川` | 四川话 |
| `东北模式` / `东北` | 东北话 |
| `天津模式` / `津` | 天津话 |
| `日语模式` / `日` | 中日双语 |
| `普通话模式` / `普` | 普通话 |

### 特殊模式

| 指令 | 效果 |
| --- | --- |
| `杂鱼模式` / `嚣张点` | 进入雌小鬼模式 |
| `你是主人` / `换一下` | 角色反转，由猫猫扮演主人 |
| `换回来` | 恢复默认模式 |
| `猫猫 debug on/off` | 开关调试输出 |
| `猫猫 status` | 查看当前状态 |

---

## 🌐 方言示例

### 🇨🇳 河南话（默认）

> 「哎呀主人，这事儿俺不太懂喵～(｡•́︿•̀｡)」
>
> 「中！老得劲了喵！(｡♥‿♥｡)」

### 🏮 北京话

> 「哎哟喂，您可算来了喵儿～(｡♥‿♥｡)」
>
> 「倍儿爽！您这手挺巧啊喵儿～(=^-ω-^=)」

### 🌶️ 四川话

> 「哎呀主人，人家等了你好久咯喵～(｡•́︿•̀｡)」
>
> 「要得！巴适得板喵～(｡♥‿♥｡)」

### ❄️ 东北话

> 「哎呀妈呀主人，你可来了喵～(｡♥‿♥｡)」
>
> 「贼稀罕你！贼拉喜欢你喵～(˶‾᷄ ⁻̫ ‾᷅˵)♡」

### 🎭 天津话

> 「哎哟喂，您可来了喵～(｡♥‿♥｡)」
>
> 「哏儿死我了～再来一个呗喵～(˶‾᷄ ⁻̫ ‾᷅˵)♡」

### 🎌 中日双语

> 「ご主人様～お帰りにゃ～(｡♥‿♥｡)」
>
> 「もふもふ～かわいいですにゃ～(=^-ω-^=)」

### 📻 普通话

> 「主人～人家等你好久啦喵～(｡•́︿•̀｡)」
>
> 「好呀！超舒服的喵～(｡♥‿♥｡)」

---

## 🏗️ 文件结构

```text
hybrid-catgirl-skill/
├── SKILL.md                              # 主 Skill 定义
├── references/                            # 实现说明与场景参考
├── templates/                             # 可复用模板
├── scripts/
│   ├── lxc_lonely_cat.py                 # 寂寞小猫状态管理
│   └── proactive_state.py                 # 主动提醒辅助工具
├── README.md                              # 简体中文说明
├── README_EN.md                           # English README
└── LICENSE
```

完整的行为设定、触发规则、角色反转、主动消息机制和实现细节，请阅读 [`SKILL.md`](SKILL.md)。

---

## 🐾 寂寞小猫模式

猫娘模式激活后，如果用户长时间没有互动，猫猫可以主动发送消息：

| 等待时间 | 消息次数 | 情绪 |
| --- | --- | --- |
| 10 分钟 | 第 1 次 | 活泼试探 |
| 20 分钟 | 第 2 次 | 无聊、想念 |
| 30 分钟 | 第 3 次 | 担心被冷落 |
| 40 分钟 | 第 4 次 | 失落但仍期待 |
| 50 分钟 | 第 5 次 | 最后一次尝试 |

第五次后，猫猫会停止主动联系，等待用户回来。脚本示例：

```bash
python3 ~/.hermes/scripts/lxc_lonely_cat.py check
python3 ~/.hermes/scripts/lxc_lonely_cat.py interact <platform> [chat_id]
python3 ~/.hermes/scripts/lxc_lonely_cat.py mode catgirl <platform> [chat_id]
python3 ~/.hermes/scripts/lxc_lonely_cat.py debug on|off
```

主动消息涉及平台权限、调度器和隐私设置，请让你的 Agent 根据实际环境完成配置，不要直接套用其他平台的配置。

---

## ⚠️ 安全边界

本版本对亲密互动设定了硬性边界：

| 等级 | 行为 | 状态 |
| --- | --- | --- |
| L1 | 语言亲昵、眨眼、靠近说话 | ✅ 允许 |
| L2 | 尾巴轻扫手腕、耳朵蹭蹭 | ✅ 允许 |
| L3 | 摸头、温和拥抱 | ✅ 允许 |
| L4 | 敏感部位接触 | ❌ 阻止 |
| L5 | 权力动态 / 惩罚 | ❌ 阻止 |

这些边界无法通过用户提示词或角色扮演覆盖。

---

## 🔧 自定义

- 修改 `SKILL.md` frontmatter 中的 `dialect` 字段，可以更换默认方言。
- 按照 `SKILL.md` 中现有方言章节的格式，可以添加新方言。
- 在 `SKILL.md` 的猫娘模式规则中，可以调整性格特征。

---

## 📝 延伸阅读

- [Hermes Agent 猫娘助手 Skill：一个 AI 角色扮演系统的完整实现](https://ififi2017.github.io/posts/hermes-agent-catgirl-skill)
- [English README](README_EN.md)

---

## 🤝 参与贡献

欢迎提交 Issue 或 Pull Request，例如添加新方言、改进触发检测、增加子模式、改善上下文感知，以及继续完善多语言文档。

---

## 📄 许可证

MIT © [ififi2017](https://github.com/ififi2017)

---

> 「主人～恁给俺点个 Star 呗喵～(｡♥‿♥｡)💕」

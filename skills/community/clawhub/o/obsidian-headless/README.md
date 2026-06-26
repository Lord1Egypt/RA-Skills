# Obsidian Headless

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Shell](https://img.shields.io/badge/shell-bash-blue.svg)

> 在无显示器、无 GUI 的环境下，通过自然语言指令管理 Obsidian 笔记仓库

---

## 为什么需要这个工具？

- **SSH 远程服务器**上想管理 Obsidian 笔记？
- **无显示器环境**（VPS、Docker、NAS）需要使用 Obsidian？
- 不想每次都**启动 Obsidian GUI** 桌面应用？
- 希望通过**自然语言**而不是复杂命令来管理笔记？

**Obsidian Headless** 就是为解决这些场景而生的工具。

---

## 功能特性

### 核心功能
- ✍️ **创建笔记** - 支持子目录、多行内容
- 🗑️ **删除笔记** - 智能确认，防止误删
- 👁️ **查看笔记** - 快速预览内容
- 🔍 **搜索笔记** - 标题搜索、内容搜索、模糊搜索
- 📅 **日记功能** - 自动创建/追加今日日记
- 📂 **列出管理** - 列出所有笔记和文件夹

### 使用体验
- 🗣️ **自然语言** - `obs创建笔记 想法` 而不是 `touch note.md`
- 🔤 **大小写不敏感** - `OBS创建笔记` 也可以
- 🔗 **灵活分隔** - `obs-创建笔记`、`obs_创建笔记` 都支持
- 📄 **多行内容** - 文件名和内容可以用换行符分隔

### 安全保障
- 🛡️ **路径遍历防护** - 阻止 `../etc/passwd` 攻击
- ✅ **删除验证** - 确保只能删除仓库内文件
- 🔒 **输入验证** - 阻止非法字符和控制字符

---

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/imakid/obsidian-headless.git
cd obsidian-headless

# 安装（可选，添加 obs 别名到 shell）
./install.sh
```

或直接运行：
```bash
./obs "obs创建笔记 测试笔记"
```

### 首次使用

运行任意命令时会提示输入 Obsidian 仓库路径：

```
首次使用 Obsidian Headless
==========================

请输入 Obsidian 仓库路径: /path/to/your/vault
✓ 有效的 Obsidian 仓库
✓ 已保存配置
```

### 基本使用

```bash
# 创建笔记
obs创建笔记 待办清单
obs创建笔记 项目/想法 这个项目的核心目标是...

# 创建多行内容笔记
obs创建笔记 会议记录
# 会议主题：周会
## 参会人员
- Alice
- Bob

# 搜索笔记
obs搜索内容 home assistant
obs模糊搜索 openclaw

# 今天日记
obs今天日记 今天完成了技能发布...

# 查看笔记
obs查看笔记 待办清单

# 列出所有
obs列出所有
```

---

## 完整指令列表

| 指令 | 功能 | 示例 |
|------|------|------|
| `obs创建笔记 [文件名] [内容]` | 创建新笔记 | `obs创建笔记 想法` |
| `obs删除笔记 [文件名]` | 删除笔记（带确认） | `obs删除笔记 旧笔记` |
| `obs查看笔记 [文件名]` | 显示笔记内容 | `obs查看笔记 欢迎` |
| `obs搜索标题 [关键词]` | 搜索文件名 | `obs搜索标题 项目` |
| `obs搜索内容 [关键词]` | 搜索文件内容 | `obs搜索内容 docker` |
| `obs模糊搜索 [关键词]` | 标题+内容搜索 | `obs模糊搜索 ai` |
| `obs今天日记 [内容]` | 创建/追加日记 | `obs今天日记 今天...` |
| `obs列出所有` | 列出所有笔记 | `obs列出所有` |
| `obs列出文件夹` | 列出所有文件夹 | `obs列出文件夹` |
| `obs最近笔记` | 最近修改的笔记 | `obs最近笔记` |
| `obs修改库路径` | 修改仓库路径 | `obs修改库路径` |

**格式说明**：`obs` 前缀大小写不敏感，支持空格、`-`、`_`、`::` 等分隔符。

---

## 使用场景示例

### 场景 1：SSH 远程管理
```bash
ssh my-server
obs创建笔记 服务器配置/nginx配置
# 粘贴配置内容...
obs列出所有
```

### 场景 2：快速记录想法
```bash
obs创建笔记 灵感/新产品想法
# 产品名称：XXX
## 核心功能
1. ...
2. ...
```

### 场景 3：项目管理
```bash
obs创建笔记 项目A/需求文档 需求分析...
obs创建笔记 项目A/进度表 当前进度...
obs模糊搜索 项目A
```

---

## 依赖要求

### 必需（通常已预装）
- `bash` - 脚本解释器
- `find`, `grep` - 搜索工具
- `mkdir`, `touch`, `rm`, `cat` - 文件操作
- `date`, `chmod` - 系统命令
- `head`, `tail`, `cut`, `awk` - 文本处理

### macOS 用户注意
旧版 macOS 可能缺少 `realpath`：
```bash
brew install coreutils
```

### 可选（推荐）
- `ripgrep (rg)` - 更快的搜索速度

---

## 配置

### 环境变量
```bash
export OBSIDIAN_VAULT=/path/to/your/vault
```

### 配置文件位置
```
~/.config/obsidian-headless/vault-path
```

删除此文件可重置配置。

---

## 安全说明

- ✅ **路径遍历防护** - 阻止 `../../../etc/passwd` 等攻击
- ✅ **删除验证** - 确保只能删除仓库内的文件
- ✅ **输入验证** - 验证文件名，阻止非法字符
- ✅ **配置权限** - 配置文件权限设置为 644

---

## 与其他工具对比

| 工具 | 依赖 Obsidian GUI | 支持自然语言 | 无头环境 | 搜索速度 |
|------|------------------|-------------|---------|---------|
| Obsidian GUI | ✅ 必须 | ❌ 不支持 | ❌ 不支持 | 快 |
| obsidian-cli | ✅ 需要索引 | ⚠️ 有限 | ❌ 不支持 | 慢 |
| **Obsidian Headless** | ❌ 不需要 | ✅ 完整支持 | ✅ 专门设计 | 快 (rg) |

---

## 开发背景

这个工具最初是为了解决在 **OpenClaw 自动化环境** 中管理 Obsidian 笔记的需求。在无显示器的服务器上，无法启动 Obsidian GUI，但又需要：
- 创建和编辑笔记
- 搜索已有内容
- 管理日记

于是诞生了 **Obsidian Headless** - 一个真正为无头环境设计的 Obsidian 管理工具。

---

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

[MIT](LICENSE) © 2026 Obsidian Headless Contributors

---

## 相关链接

- 📦 [OpenClaw](https://github.com/openclaw/openclaw) - AI 自动化框架
- 📝 [Obsidian](https://obsidian.md/) - 强大的知识管理工具
- 🦞 [ClawHub](https://clawhub.com) - OpenClaw 技能市场

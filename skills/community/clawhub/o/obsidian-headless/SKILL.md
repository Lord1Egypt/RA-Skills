---
name: obsidian-headless
description: 在无显示器/无 GUI 环境下通过自然语言指令管理 Obsidian 笔记仓库。支持创建笔记、删除笔记（带确认）、搜索标题、搜索内容、模糊搜索、创建日记等功能。当用户需要在无头服务器、SSH 环境、或没有安装 Obsidian 桌面应用的情况下管理 Obsidian 笔记时使用此技能。触发词包括"obsidian", "笔记", "搜索笔记", "创建笔记", "删除笔记", "今天日记", "无头 obsidian", "命令行 obsidian"。
---

# Obsidian Headless - 无头 Obsidian 管理工具

在无显示器/无 GUI 环境下通过自然语言指令管理 Obsidian 笔记仓库。

## 适用场景

- 在 SSH 远程服务器上管理 Obsidian 笔记
- 无显示器环境（如 VPS、Docker 容器）
- 不想启动 Obsidian GUI 桌面应用时
- 需要通过脚本自动化管理笔记时

## 文档

- **USAGE.md** - 完整使用手册（包含快速参考、详细说明、示例、故障排除）

## 目录结构

```
obsidian-headless/
├── obs                    # 便捷入口脚本
├── install.sh             # 安装脚本
├── SKILL.md              # 本文件（技能说明）
├── USAGE.md              # 完整使用手册
├── bin/
│   └── obsidian-headless.sh   # 主程序
├── examples/
│   └── examples.sh       # 使用示例脚本
└── tests/
    └── test.sh           # 测试脚本
```

## 配置文件

首次使用时会提示输入仓库路径，配置保存在：
```
~/.config/obsidian-headless/vault-path
```

## 快速开始

### 1. 安装

```bash
cd ~/.openclaw/skills/obsidian-headless
./install.sh
```

或手动使用：
```bash
~/.openclaw/skills/obsidian-headless/obs "obs指令"
```

### 指令格式

所有指令都支持 `obs` 前缀（**大小写不敏感**），`obs` 和指令之间可以有**空格、-、_、: 等连接符**：

| 格式 | 示例 |
|------|------|
| `obs指令` | `obs创建笔记 新笔记` |
| `obs 指令` | `obs 创建笔记 新笔记` |
| `obs-指令` | `obs-创建笔记 新笔记` |
| `OBS指令` | `OBS创建笔记 新笔记` |

**推荐使用 `obs指令` 格式**，避免误触。

### 2. 配置仓库路径

**首次使用：**
运行任意命令时会提示输入仓库路径，路径会保存到配置文件中供后续使用。

```
首次使用 Obsidian Headless
==========================

请输入 Obsidian 仓库路径: /home/user/my-vault
✓ 已保存配置
```

**手动配置（可选）：**

方式 1 - 环境变量（优先级最高）：
```bash
export OBSIDIAN_VAULT=/path/to/your/vault
```

方式 2 - 删除配置文件重新输入：
```bash
rm ~/.config/obsidian-headless/vault-path
# 下次运行时会重新提示输入
```

### 3. 使用

```bash
# 使用安装后的快捷命令
obs "创建笔记 新想法"

# 或直接调用
~/.openclaw/skills/obsidian-headless/obs "搜索内容 home assistant"
```

## 支持的指令

### 创建笔记
```
obs创建笔记 [文件名] [可选内容]
```

**说明：**
- `文件名` 支持路径，如 `文件夹/笔记名` 或 `笔记名`
- 如果**只输入文件名**（无内容），创建**空笔记文件**
- 如果**输入了内容**，内容**直接写入文件**，不会自动添加标题
- 笔记的标题需要用户在 `内容` 中自行定义（如 `# 我的标题`）
- **文件名和内容之间可以用空格或换行符分隔**

**示例：**
- `obs创建笔记 待办清单` → 创建空文件 `待办清单.md`
- `obs创建笔记 项目想法 这个项目的核心目标是...` → 文件内容为 "这个项目的核心目标是..."
- `obs创建笔记 AI/总结 # AI 总结\n\n今天学习了...` → 文件内容包含自定义标题

**多行内容示例：**
```
obs创建笔记 笔记名
# 标题
内容第一行
内容第二行
```

### 删除笔记（带确认）
```
obs删除笔记 [文件名]
```

**删除确认流程：**

**单个匹配时：**
```
即将删除笔记:
  标题: xxx
  路径: /path/to/xxx.md

  内容预览 (共 15 行):
    # xxx
    ...

请回复确认:
  [Y] 确认删除
  [N] 取消
```

**多个匹配时：**
```
找到多个匹配的笔记:

  [1] 笔记A
      位置: folder1/
      大小: 20 行

  [2] 笔记B
      位置: folder2/
      大小: 35 行

请回复要删除的笔记编号 (或 0 取消)
```

### 查看笔记内容
```
obs查看笔记 [文件名]
```

### 搜索笔记标题
```
obs搜索标题 [关键词]
```

### 搜索笔记内容
```
obs搜索内容 [关键词]
```

### 模糊搜索（标题+内容）
```
obs模糊搜索 [关键词]
```

### 创建/打开今天日记
```
obs今天日记 [可选内容]
```

自动在 `日记/` 文件夹下创建 `YYYY-MM-DD.md`

### 修改库路径
```
obs修改库路径
obs修改库目录
obs更改路径
obs切换仓库
```

交互式修改仓库路径，保存到配置文件。

**示例：**
- `obs修改库路径` → 提示输入新路径
- `obs-修改库目录` → 同上

### 列出所有笔记
```
obs列出所有
```

### 列出所有文件夹
```
obs列出文件夹
```

### 显示最近修改的笔记
```
obs最近笔记
```

## 前置要求

1. **Obsidian 仓库：** 首次使用时会提示输入仓库路径

2. **依赖:**
   - `bash` (必须)
   - `find` (必须)
   - `grep` (必须)
   - `ripgrep (rg)` (推荐，搜索更快)

3. **安装 ripgrep：**
   ```bash
   # Ubuntu/Debian
   sudo apt install ripgrep
   
   # macOS
   brew install ripgrep
   ```

## 测试

运行测试脚本验证功能：

```bash
cd ~/.openclaw/skills/obsidian-headless
./tests/test.sh
```

## 查看示例

运行示例脚本查看各种用法：

```bash
cd ~/.openclaw/skills/obsidian-headless
./examples/examples.sh
```

## 与 obsidian-cli 的对比

| 功能 | obsidian-cli | obsidian-headless |
|------|-------------|-------------------|
| 依赖 Obsidian GUI | 是（需要索引） | 否 |
| search-content | 依赖索引，常失败 | 使用 ripgrep，可靠 |
| 删除确认 | 无 | 有（显示预览） |
| 多匹配处理 | 无 | 列出序号选择 |
| 自然语言支持 | 有限 | 完整支持 |
| 无头环境 | 不支持 | 专门设计 |

## 故障排除

### 提示"未找到 Obsidian 仓库路径"
1. 首次使用时会自动提示输入路径
2. 或手动设置环境变量：
   ```bash
   export OBSIDIAN_VAULT=/path/to/your/vault
   ```
3. 或删除配置重新输入：
   ```bash
   rm ~/.config/obsidian-headless/vault-path
   ```

### 修改已保存的仓库路径
```bash
# 方法1: 使用环境变量覆盖
export OBSIDIAN_VAULT=/new/path

# 方法2: 删除配置，下次重新输入
rm ~/.config/obsidian-headless/vault-path
```

### 搜索速度慢
安装 ripgrep：
```bash
sudo apt install ripgrep  # Ubuntu/Debian
brew install ripgrep       # macOS
```

### 删除时找不到笔记
使用更精确的标题，或使用"模糊搜索"先找到准确标题。

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `obs` | 便捷入口，推荐日常使用 |
| `bin/obsidian-headless.sh` | 主程序 |
| `install.sh` | 安装脚本，设置别名和快捷方式 |
| `tests/test.sh` | 功能测试 |
| `examples/examples.sh` | 使用示例 |

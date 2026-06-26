# Obsidian CLI 使用指南

> 给 Agent 看的快速入门文档

## 简介

Obsidian CLI 是官方命令行工具（v1.12+），通过 IPC 与 Obsidian 客户端通信，实现金库自动化管理。

## 安装

### 1. 安装 Obsidian
下载安装：[https://obsidian.md/download](https://obsidian.md/download)

### 2. 启用 CLI
在 Obsidian 中：设置 → 通用 → 启用 CLI

### 3. 确保 Obsidian 在运行
CLI 需要 Obsidian 客户端在后台运行才能工作。

---

## 快速使用

### 查看版本和帮助
```bash
obsidian version
obsidian help
```

### 查看当前金库信息
```bash
obsidian vault                    # 完整信息
obsidian vault info=name          # 仅金库名
obsidian vault info=path          # 仅路径
```

---

## 日常笔记

```bash
obsidian daily                    # 打开今日笔记
obsidian daily:read               # 读取今日笔记内容
obsidian daily:append content="- [ ] 任务"   # 追加内容
```

---

## 文件操作

```bash
obsidian read file=笔记名         # 读取笔记（支持 wikilink 解析）
obsidian read path="文件夹/笔记.md"  # 按路径读取

obsidian create name=新笔记 content="内容"   # 创建笔记

obsidian open file=笔记名          # 在 Obsidian 中打开
obsidian open file=笔记名 newtab  # 在新标签页打开

obsidian append file=笔记 content="追加内容"   # 追加到笔记
obsidian prepend file=笔记 content="前置内容"  # 前置到笔记

obsidian delete file=笔记         # 删除到回收站
obsidian delete file=笔记 permanent  # 永久删除

obsidian move file=旧笔记 to="新文件夹/新笔记.md"  # 移动/重命名
```

---

## 搜索

```bash
obsidian search query="关键词"           # 搜索金库
obsidian search query="TODO" matches     # 显示匹配上下文
obsidian search query="项目" path="工作" limit=10  # 限定范围
obsidian search:open query="关键词"      # 在 Obsidian 中打开搜索
```

---

## 任务管理

```bash
obsidian tasks daily                # 今日笔记中的任务
obsidian tasks daily todo           # 未完成的任务
obsidian tasks all todo             # 金库中所有未完成任务

obsidian task daily line=3 toggle   # 切换任务状态
obsidian task daily line=3 done    # 标记完成
```

---

## 标签和属性

```bash
obsidian tags all counts           # 所有标签及数量
obsidian tags file=笔记            # 特定文件的标签

obsidian properties all counts     # 所有属性及数量
obsidian properties file=笔记      # 特定文件的属性

obsidian property:read name=属性名 file=笔记    # 读取属性
obsidian property:set name=属性名 value=值 file=笔记  # 设置属性
```

---

## 链接和结构

```bash
obsidian backlinks file=笔记       # 链接到该笔记的文件
obsidian links file=笔记           # 该笔记的出链

obsidian orphans                   # 孤立文件（无任何链接）
obsidian unresolved               # 损坏的链接
```

---

## 搜索技巧

### 常用参数
- `file=<名称>` - 按名称（支持 wikilink 解析）
- `path=<路径>` - 按精确路径
- `format=json` - JSON 格式输出
- `verbose` - 详细信息
- `total` - 仅计数

### 示例
```bash
# 搜索并限制结果数
obsidian search query="项目" limit=5

# 搜索特定文件夹
obsidian search query="TODO" path="工作"

# 统计匹配数量
obsidian search query="error" total
```

---

## 安装 Skill（给 Agent 用）

### OpenClaw 环境安装

```bash
# 克隆完整仓库到 skills 目录
git clone https://github.com/kepano/obsidian-skills.git ~/.openclaw/workspace/skills/obsidian-skills
```

注意：必须克隆完整仓库，目录结构应为：
```
~/.openclaw/workspace/skills/obsidian-skills/skills/<skill-name>/SKILL.md
```

OpenClaw 会自动发现 `~/.openclaw/workspace/skills/` 下的所有 SKILL.md 文件。

### 重启 OpenClaw
安装后需要重启 Gateway 让 Skill 生效：
```bash
openclaw gateway restart
```

---

## 可用 Skills

| Skill | 用途 |
|-------|------|
| `obsidian-markdown` | 创建和编辑 Obsidian  flavored Markdown |
| `obsidian-bases` | 创建和编辑 Obsidian Bases 数据库 |
| `json-canvas` | 创建和编辑 JSON Canvas 文件 |
| `obsidian-cli` | 通过 CLI 与 Obsidian 交互 |
| `defuddle` | 从网页提取干净 Markdown |

---

## 注意事项

1. **Obsidian 必须运行** - CLI 通过 IPC 与 Obsidian 通信
2. **路径格式** - 使用 `file=` 时不加 `.md`，使用 `path=` 时需要完整路径
3. **参数语法** - 有空格的值需要加引号：`content="Hello world"`
4. **多金库支持** - `vault=金库名` 必须作为第一个参数

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| Cannot connect | 确保 Obsidian 正在运行，且 CLI 已启用 |
| Command not found | 将 obsidian 添加到 PATH |
| Linux IPC 不工作 | 检查是否有 PrivateTmp 限制 |


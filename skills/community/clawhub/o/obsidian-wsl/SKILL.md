---
name: obsidian-wsl
description: 通过 notesmd-cli 操作 Obsidian 知识库 — 搜索、创建、编辑、移动、删除笔记及管理 frontmatter，无需 Obsidian 运行。
metadata:
  {
    "openclaw":
      {
        "emoji": "💎",
        "requires": { "bins": ["notesmd-cli"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "yakitrak/yakitrak/notesmd-cli",
              "bins": ["notesmd-cli"],
              "label": "安装 notesmd-cli (brew)",
            },
          ],
      },
  }
---

# Obsidian WSL Skill

基于 `notesmd-cli`（v0.3.0+，原 obsidian-cli）操作 Obsidian 知识库。notesmd-cli 无需 Obsidian 运行即可工作，适合脚本、自动化和纯终端环境。

## 环境配置

### 知识库发现

`notesmd-cli` 通过 `~/.config/obsidian/obsidian.json` 发现知识库。在有 Obsidian 桌面端的系统上会自动生成；在无头服务器或无 GUI 的环境中需手动创建：

```json
{
  "vaults": {
    "my-brain": {
      "path": "/home/user/vaults/my-brain"
    }
  }
}
```

- 键名可以是任意唯一 ID，CLI 使用目录名作为知识库名称
- 路径必须为绝对路径，不支持 `~` 展开
- 支持多个知识库：

```json
{
  "vaults": {
    "personal": {
      "path": "/home/user/vaults/personal"
    },
    "work": {
      "path": "/home/user/vaults/work"
    }
  }
}
```

### 设置默认知识库

```bash
notesmd-cli set-default "my-brain"
notesmd-cli set-default --open-type editor
```

### 编辑器配置

无 Obsidian GUI 时，建议配置默认使用终端编辑器：

```bash
export EDITOR="vim"   # 或 code、nano 等
notesmd-cli set-default --open-type editor
```

所有支持 `--open` 的命令均可加 `--editor`（或 `-e`）在终端编辑器中打开。

## 常用命令速查

### 查看状态

```bash
notesmd-cli print-default              # 查看默认知识库名称和路径
notesmd-cli print-default --path-only  # 仅输出路径
notesmd-cli list-vaults                # 列出所有已注册知识库
```

### 搜索

```bash
notesmd-cli search                     # 交互式模糊搜索笔记名称
notesmd-cli search --editor            # 搜索并在编辑器中打开
notesmd-cli search-content "关键词"     # 搜索笔记内容
notesmd-cli search-content "关键词" --no-interactive  # 非交互，输出 grep 风格结果
notesmd-cli search-content "关键词" --format json      # JSON 输出，适合脚本
```

### 列出目录

```bash
notesmd-cli list                       # 列出知识库根目录
notesmd-cli list "子目录名"             # 列出子目录内容
```

### 读取笔记

```bash
notesmd-cli print "笔记名"             # 输出笔记内容
notesmd-cli print "路径/笔记名"         # 按路径输出
```

### 创建笔记

```bash
notesmd-cli create "笔记名"            # 创建空笔记
notesmd-cli create "文件夹/笔记名" --content "内容"  # 创建带内容的笔记
notesmd-cli create "笔记名" --content "内容" --append   # 追加内容
notesmd-cli create "笔记名" --content "内容" --overwrite  # 覆盖已有笔记
notesmd-cli create "笔记名" --content "内容" --open --editor  # 创建并在编辑器中打开
```

中间目录会自动创建。

### 移动/重命名

```bash
notesmd-cli move "旧路径" "新路径"      # 移动或重命名，自动更新知识库内所有链接
notesmd-cli move "旧路径" "新路径" --open --editor  # 移动后在编辑器中打开
```

### 删除

```bash
notesmd-cli delete "笔记路径"           # 删除笔记（谨慎使用）
```

### Daily Notes

```bash
notesmd-cli daily                      # 创建/打开今日笔记
notesmd-cli daily --editor             # 在编辑器中打开
```

如果知识库中存在 `.obsidian/daily-notes.json`，CLI 会读取其中的 folder、format、template 配置。

### Frontmatter 管理

```bash
notesmd-cli frontmatter "笔记名" --print                    # 查看 frontmatter
notesmd-cli frontmatter "笔记名" --edit --key "status" --value "done"  # 编辑字段
notesmd-cli frontmatter "笔记名" --delete --key "draft"     # 删除字段
```

## 直接操作文件系统

对于简单读写操作，直接操作知识库中的 `.md` 文件同样有效，Obsidian 会自动检测变更：

- 读取：直接读取知识库中的 `.md` 文件
- 编辑：直接修改文件
- 注意：直接文件操作不会自动更新 wikilinks，如需重命名请使用 `notesmd-cli move`

## 排除文件

CLI 尊重 Obsidian 的排除设置（Settings -> Files & Links -> Excluded Files）：

- `search`：排除的笔记不出现在模糊搜索中
- `search-content`：排除的文件夹不会被搜索
- 其他命令（open、move、print、frontmatter）仍可访问排除的文件

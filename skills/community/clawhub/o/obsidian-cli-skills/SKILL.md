# Obsidian CLI 探索记录

> 更新时间：2026-03-05

## 简介

Obsidian CLI 是一个命令行工具，用于操作 Obsidian vault（笔记库）。它可以完成搜索、创建、移动、删除笔记等操作。

## 环境配置

- **默认 Vault**：`/Users/luoxiaohei/.openclaw/obsidian_workspace`
- **设置默认 Vault**：`obsidian-cli set-default "<vault路径>"`

---

## 命令列表

### 1. create - 创建笔记

```bash
obsidian-cli create "笔记名" --content "内容"
```

**参数：**
| 参数 | 简写 | 说明 |
|------|------|------|
| --content | -c | 笔记内容 |
| --open | -o | 创建后打开笔记 |
| --overwrite | -o | 覆盖已存在的笔记 |
| --append | -a | 追加到已存在的笔记 |
| --vault | -v | 指定 vault 名称 |

**示例：**
```bash
obsidian-cli create "新笔记" --content "这是笔记内容"
obsidian-cli create "test-note" --content "This is a test note" --open
```

---

### 2. print - 打印笔记内容

```bash
obsidian-cli print "笔记名"
```

**示例：**
```bash
obsidian-cli print "test-note"
# 输出: This is a test note
```

---

### 3. search - Fuzzy 搜索

```bash
obsidian-cli search "关键词"
```

**说明：** 交互式搜索，会打开 Obsidian 让你选择笔记。

---

### 4. search-content - 全文搜索

```bash
obsidian-cli search-content "关键词"
```

**说明：** 在笔记内容中搜索包含指定关键词的笔记。

**⚠️ 注意：** 当前版本测试有问题，可能需要指定 vault 参数。

---

### 5. move - 移动/重命名笔记

```bash
obsidian-cli move "旧路径" "新路径"
```

**特点：** 移动时会自动更新 wiki 链接。

**示例：**
```bash
obsidian-cli move "test-note" "test-note-moved"
# 输出: Moved note from .../test-note.md to .../test-note-moved.md
```

---

### 6. delete - 删除笔记

```bash
obsidian-cli delete "笔记名"
```

**示例：**
```bash
obsidian-cli delete "test-note-moved"
# 输出: Deleted note: /Users/luoxiaohei/.openclaw/obsidian_workspace/test-note-moved.md
```

---

### 7. frontmatter - 查看/修改 YAML 头信息

```bash
# 查看 frontmatter
obsidian-cli frontmatter "笔记名" --print

# 修改 frontmatter
obsidian-cli frontmatter "笔记名" --edit --key "key名" --value "值"

# 删除 frontmatter
obsidian-cli frontmatter "笔记名" --delete --key "key名"
```

**示例：**
```bash
# 查看
obsidian-cli frontmatter "test-note" --print

# 添加/修改
obsidian-cli frontmatter "test-note" --edit --key "tags" --value "test,cli"

# 删除
obsidian-cli frontmatter "test-note" --delete --key "draft"
```

---

### 8. daily - 创建/打开每日笔记

```bash
obsidian-cli daily
```

**说明：** 自动创建或打开当天的每日笔记（格式：YYYY-MM-DD.md）。

---

### 9. open - 在 Obsidian 中打开笔记

```bash
obsidian-cli open "笔记名"
```

**示例：**
```bash
obsidian-cli open "my-note"
```

---

### 10. print-default - 查看默认 Vault

```bash
obsidian-cli print-default
obsidian-cli print-default --path-only  # 只显示路径
```

**输出示例：**
```
Default vault name:  obsidian_workspace
Default vault path:  /Users/luoxiaohei/.openclaw/obsidian_workspace
```

---

### 11. set-default - 设置默认 Vault

```bash
obsidian-cli set-default "vault名称或路径"
```

**示例：**
```bash
obsidian-cli set-default "obsidian_workspace"
obsidian-cli set-default "/Users/luoxiaohei/.openclaw/obsidian_workspace"
```

---

### 12. completion - 生成自动补全脚本

```bash
obsidian-cli completion [shell]
```

**支持的 shell：** bash, zsh, fish, powershell

**示例：**
```bash
obsidian-cli completion zsh
```

---

## 常用命令速查

| 功能 | 命令 |
|------|------|
| 查看默认 vault | `obsidian-cli print-default` |
| 设置默认 vault | `obsidian-cli set-default "vault名"` |
| 创建笔记 | `obsidian-cli create "名" --content "内容"` |
| 查看笔记 | `obsidian-cli print "名"` |
| 搜索笔记名 | `obsidian-cli search "关键词"` |
| 全文搜索 | `obsidian-cli search-content "关键词"` |
| 移动/重命名 | `obsidian-cli move "旧" "新"` |
| 删除笔记 | `obsidian-cli delete "名"` |
| 查看头信息 | `obsidian-cli frontmatter "名" --print` |
| 修改头信息 | `obsidian-cli frontmatter "名" --edit --key "x" --value "y"` |
| 每日笔记 | `obsidian-cli daily` |
| 在 Obsidian 打开 | `obsidian-cli open "名"` |

---

## 注意事项

1. **Vault 路径**：CLI 通过 `~/Library/Application Support/obsidian/obsidian.json` 获取 vault 信息
2. **Wiki 链接**：`move` 命令会自动更新 wiki 链接，这是相比普通 mv 的优势
3. **搜索问题**：`search-content` 在部分环境可能有兼容性问题
4. **默认 Vault**：建议先设置默认 vault，避免每次都要指定 `-v` 参数

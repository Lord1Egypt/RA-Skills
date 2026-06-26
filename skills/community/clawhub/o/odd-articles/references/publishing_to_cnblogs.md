# 博客园发布工具

> 不依赖 manifest，可直接发布 Markdown 文件到博客园

---

### 环境变量支持

在 `local/.env` 中读取 `CNBLOGS_TOKEN`，避免每次输入 token：

## 使用方式

### 基本用法

```bash
python3 "${SKILL_DIR}/scripts/publish_to_cnblogs.py" <markdown文件> --token ${CNBLOGS_TOKEN} [--title <标题>] [--preview]
```

### Windows 示例

```bash
# 推荐方式：使用绝对路径
python ${SKILL_DIR}/scripts/publish_to_cnblogs.py article.md --token ${CNBLOGS_TOKEN}

# 或先切换到脚本目录
cd "${SKILL_DIR}/scripts"
python publish_to_cnblogs.py ../article.md --token ${CNBLOGS_TOKEN}
```

---

## 获取 PAT

1. 登录博客园 → https://i.cnblogs.com/
2. 点击账号设置 → Access Tokens
3. 创建新 Token（建议设置过期时间）

---

## 参数说明

| 参数 | 简写 | 必填 | 说明 |
|------|------|------|------|
| `<input>` | - | 是 | Markdown 文件路径 |
| `--token` | `-t` | 是 | 博客园 PAT（Personal Access Token） |
| `--title` | `-T` | 否 | 文章标题（默认从 `# 标题` 提取） |
| `--description` | `-d` | 否 | 文章摘要（自动提取前几段） |
| `--post-type` | - | 否 | 文章类型，默认 `BlogPost`，可选 `Article` |
| `--preview` | `-p` | 否 | 仅预览，不实际发布 |

---

## 功能特性

### 自动提取信息

- **标题**：自动从 Markdown 文件的第一级标题提取（`# 标题`）
- **摘要**：自动提取文章前几段作为摘要（最多 200 字）
- **内容格式**：自动设置为 Markdown 格式

### 编码处理

脚本已内置 UTF-8 编码处理，解决 Windows 下的中文显示问题。

---

## 常见问题

### "No such file or directory"

**原因**：Windows 路径格式问题

**解决方案**：
1. 使用绝对路径，如 `/path/to/article.md`
2. 或先切换到脚本所在目录，使用相对路径

### 编码错误

**解决方案**：脚本已内置 UTF-8 编码处理，如仍有问题，请确保：
- Markdown 文件使用 UTF-8 编码保存
- 终端支持 UTF-8 显示

### Token 从环境变量读取

在 `local/.env` 中设置 `CNBLOGS_TOKEN`，脚本会自动读取：

```bash
# local/.env
CNBLOGS_TOKEN=your_token_here
```

---

## 完整示例

### 示例 1：基本发布

```bash
python publish_to_cnblogs.py article.md --token ${CNBLOGS_TOKEN}
```

### 示例 2：指定标题

```bash
python publish_to_cnblogs.py article.md --token ${CNBLOGS_TOKEN} --title "我的第一篇博客"
```

### 示例 3：预览模式

```bash
python publish_to_cnblogs.py article.md --token ${CNBLOGS_TOKEN} --preview
```

### 示例 4：指定文章类型

```bash
python publish_to_cnblogs.py article.md --token ${CNBLOGS_TOKEN} --post-type Article
```

---

## 返回结果

### 成功

[OK] Published successfully! Post ID: 12345678 [INFO] Response: {"id": "12345678", "postId": "12345678", ...}


### 失败

[ERROR] Failed: {"error": "Invalid token"}


---

## 相关文件

- 脚本位置：`scripts/publish_to_cnblogs.py`
- 配置文件：`local/.env`
- 环境变量：`CNBLOGS_TOKEN`

---
name: juejin-publisher
version: 1.0.2
license: MIT
description: 掘金文章自动发布技能。通过掘金官方 API（Cookie 鉴权），支持将 Markdown 文章一键发布到稀土掘金平台，支持设置分类、标签、摘要和封面图。
metadata:
  openclaw:
    emoji: "⛏️"
    category: publishing
  clawdbot:
    emoji: "⛏️"
    requires:
      bins: ["python3", "curl"]
    install: []
---

# 掘金文章自动发布

本技能通过掘金官方 API，将 Markdown 文章自动发布到**稀土掘金**平台，无需打开浏览器，全程命令行完成。

## ⚙️ 快速配置

### 1. 获取掘金 Cookie

1. 打开浏览器，登录 [掘金](https://juejin.cn)
2. 按 `F12` 打开开发者工具 → Network 标签
3. 随便点击一个请求（如 `query_user_info`）
4. 在 Request Headers 中找到 `Cookie` 字段，复制完整内容
5. 将 Cookie 填入配置文件（见下方步骤 2）

> ⚠️ Cookie 有效期约 30 天，过期后需重新获取

### 2. 配置凭证文件

```bash
# 在 skill 根目录创建配置文件
cp /data/workspace/skills/juejin-publisher/juejin.env.example \
   /data/workspace/skills/juejin-publisher/juejin.env

# 编辑配置文件，填入你的 Cookie
nano /data/workspace/skills/juejin-publisher/juejin.env
```

配置文件内容：
```bash
# 掘金登录 Cookie（从浏览器 F12 获取）
JUEJIN_COOKIE="sessionid=xxx; ..."

# 默认分类 ID（可选，默认：后端）
# 常用分类 ID 见 references/category_ids.md
JUEJIN_DEFAULT_CATEGORY_ID="6809637769959178254"

# 默认标签 ID（逗号分隔，可选）
# 常用标签 ID 见 references/tag_ids.md
JUEJIN_DEFAULT_TAG_IDS="6809640408797167623"
```

---

## 🚀 使用指南

### 方式 A：智能助手（推荐）

直接对我说：
> "帮我把 `article.md` 发布到掘金，分类是前端，标签是 Vue.js"

我会自动：
1. 读取 `juejin.env` 获取 Cookie
2. 解析 Markdown 文件的 frontmatter（标题、摘要、封面等）
3. 调用掘金 API 创建草稿并发布
4. 返回文章链接

### 方式 B：命令行脚本

```bash
# 赋予执行权限
chmod +x /data/workspace/skills/juejin-publisher/scripts/publish.py

# 基本用法（使用默认分类和标签）
python3 /data/workspace/skills/juejin-publisher/scripts/publish.py article.md

# 指定分类和标签
python3 /data/workspace/skills/juejin-publisher/scripts/publish.py article.md \
  --category "6809637767543259144" \
  --tags "6809640407484334093,6809640445233070094"

# 仅创建草稿，不发布
python3 /data/workspace/skills/juejin-publisher/scripts/publish.py article.md --draft-only
```

---

## 📝 Markdown 文件格式

文章顶部支持 frontmatter 元数据（可选）：

```markdown
---
title: 我的技术文章标题
description: 这里是文章摘要，建议 50-100 字，会显示在文章列表中
cover: https://example.com/cover.jpg
category_id: "6809637767543259144"
tag_ids: "6809640407484334093,6809640445233070094"
---

# 正文内容开始

这里是 Markdown 正文...
```

> 如果 frontmatter 中没有提供 `title`，脚本会自动取 Markdown 第一个 `# 标题` 作为文章标题。

---

## 📚 常用分类 ID

| 分类名称 | category_id |
|---------|-------------|
| 前端 | `6809637767543259144` |
| 后端 | `6809637769959178254` |
| Android | `6809635626879549454` |
| iOS | `6809635627209637895` |
| AI | `6809637773935378440` |
| 工具 | `6809637771511070734` |
| 阅读 | `6809637772874219534` |

## 🏷️ 常用标签 ID

| 标签名称 | tag_id |
|---------|--------|
| Python | `6809640408797167623` |
| JavaScript | `6809640407484334093` |
| Vue.js | `6809640445233070094` |
| React | `6809640407484334100` |
| Go | `6809640408797167624` |
| Docker | `6809640445233070095` |
| AI | `6809640445233070096` |

> 完整标签列表见 `references/tag_ids.md`，或通过以下命令查询：
> ```bash
> python3 /data/workspace/skills/juejin-publisher/scripts/query_tags.py "关键词"
> ```

---

## 🛠️ 故障排查

| 现象 | 原因 | 解决方案 |
|------|------|---------|
| `err_no: 1` | Cookie 失效 | 重新登录掘金并获取新 Cookie |
| `brief_content 长度不符` | 摘要太短或太长 | 摘要需 50-100 字 |
| `category_id 无效` | 分类 ID 错误 | 参考上方常用分类 ID 表 |
| `tag_ids 无效` | 标签 ID 错误 | 运行 `query_tags.py` 查询正确 ID |
| `文章重复` | 标题已存在 | 修改标题或删除掘金上的旧草稿 |

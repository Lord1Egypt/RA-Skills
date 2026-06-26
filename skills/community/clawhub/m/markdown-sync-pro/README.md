# Markdown Sync Pro

Markdown 一键同步到 Notion、GitHub Wiki、Medium 等平台

## 支持的平台

| 平台 | 状态 | 说明 |
|------|------|------|
| GitHub Wiki | ✅ | 发布到仓库 Wiki |
| Notion | 📝 | 创建 Notion 页面 |
| Medium | 📝 | 发布文章（需要 API Token） |
| 本地 HTML | ✅ | 导出为 HTML 文件 |

## 安装

作为 OpenClaw Skill 使用:
```bash
clawhub install markdown-sync-pro
```

或直接使用:
```bash
git clone https://github.com/kimi-claw/skill-markdown-sync-pro.git
cd skill-markdown-sync-pro
./bin/publish --help
```

## 使用方法

### 基本用法

```bash
/publish article.md --to github --repo owner/repo
```

### 发布到多个平台

```bash
/publish article.md --to github,notion,medium
```

### 预览转换结果

```bash
/publish article.md --dry-run
```

## 平台配置

### GitHub Wiki

```bash
export GITHUB_TOKEN=your_github_token
/publish article.md --to github --repo username/repo
```

### Notion

```bash
export NOTION_TOKEN=secret_xxx
export NOTION_PARENT_PAGE=page_id
/publish article.md --to notion
```

### Medium

```bash
export MEDIUM_TOKEN=your_medium_token
/publish article.md --to medium
```

## License

MIT

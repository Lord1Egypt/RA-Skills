# Mtime / 时光网

## 常用模式

### 首页热门 / 编辑精选
```bash
opencli mtime hot --limit 5
opencli mtime hot --limit 5 -f json
```

### 最新新闻
```bash
opencli mtime news --limit 5
opencli mtime latest --limit 5
```

### 本周 / 年度热读
```bash
opencli mtime weekly --limit 5
opencli mtime yearly --limit 5
```

## 最小说明

- `mtime hot` 返回首页热门 / 编辑精选，字段包括：`title`、`desc`、`image`、`link`、`section`。
- `mtime news` 与 `mtime latest` 当前都从 `news.mtime.com` 的“最新”列表抓取。
- `mtime weekly` / `mtime yearly` 分别对应 `news.mtime.com/hot/` 与 `news.mtime.com/hot/year/`。
- 新闻列表类命令当前返回：`title`、`subtitle`、`date`、`url`、`image`。
- `image` 当前是图片外链，不是下载后的本地文件。
- 对 Telegram，若要稳定显示图片预览，不要直接裸发图片链接；优先使用 Markdown 链接触发预览。
- 若一次发送多条，建议控制在 3–5 条，避免 Telegram 预览过长或折叠不稳定。

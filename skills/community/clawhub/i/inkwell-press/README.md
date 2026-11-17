# Inkwell

**一行命令，从 Markdown 到发布 —— 不只是排版。**

Markdown → 公众号 HTML → 杂志封面 → 社交卡片 → 剪贴板 / 公众号草稿箱。

> ⚠️ **数据安全须知 — 请先阅读**：
>
> Inkwell **不是纯本地工具**，以下操作会对外传输数据：
> - 配置了 `GITHUB_TOKEN` 时，图片会上传到 **GitHub + jsDelivr CDN**（公网可访问）
> - `publish --target clipboard` 会**覆盖系统剪贴板**内容
> - `publish --target wechat` 会将文章发送到**微信服务器**
> - ⚠️ 如果正文里包含外链图片（`http://` / `https://`），`run` **默认会下载这些图片**以生成本地预览版 ——
>   这会产生出网请求，且**不受环境变量配置影响**
>
> **在离线、内网、机密文档、不信任的 Markdown 或 CI 环境中，请务必加 `--no-embed-external`**：
> ```bash
> inkwell run article.md --theme graphite-minimal --no-embed-external
> ```
>
> 详见 SKILL.md「Safety & Data Handling」一节。

## 为什么需要它

写完一篇文章，花在「排版 + 封面 + 配图 + 多平台适配 + 发布」上的时间常常超过 1 小时。
Inkwell 把这条流水线压成一条命令：

```bash
inkwell run article.md --theme moyu-green
```

产出可直接粘进公众号编辑器，样式不崩、图片不丢。

## 覆盖环节

| 环节 | 能力 |
|------|------|
| 排版 | Markdown → 公众号兼容 HTML（15 套主题，文字节点自动包 `<span leaf="">`） |
| 图片 | PIL 压缩 + GitHub Contents API 上传 + jsDelivr CDN 外链 + base64 本地预览双轨 |
| 封面 | 杂志风封面（21:9 + 1:1，可选 PNG 截图） |
| 卡片 | 小红书 3:4 轮播等 11 个平台社交卡片 |
| 合规 | 敏感词 / 广告法极限词 / 平台违规词扫描 |
| 发布 | 富文本写入剪贴板 / 公众号草稿箱（正文图与封面自动转存微信图床） |
| 辅助 | 选题搜索、草稿生成、字数统计、目录生成、设计质量审计 |

## 安装

```bash
# 固定版本（推荐，避免上游变更引入未审查代码）
pip3 install "inkwell-press==0.8.1"
```

⚠️ 发行名是 `inkwell-press`，不是 `inkwell`（后者是无关的 Qt 主题包）。

建议在隔离的虚拟环境中安装，不要以 root 身份执行。

## 与同类工具的区别

doocs/md、mdnice 只做排版一环；Inkwell 覆盖从 Markdown 到发布的整条链路。

## 技术栈

Python 3.11+ · Pillow · MIT · 197 条测试 · CI 三平台矩阵

## 链接

- 仓库：https://github.com/lijinhongucl-pixel/inkwell
- 更新日志：https://github.com/lijinhongucl-pixel/inkwell/blob/main/CHANGELOG.md
- Issues：https://github.com/lijinhongucl-pixel/inkwell/issues

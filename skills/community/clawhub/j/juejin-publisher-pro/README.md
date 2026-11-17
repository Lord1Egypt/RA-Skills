# juejin-publisher-pro

> 掘金没有官方发布 API——这个 skill 把浏览器能做的全做成了命令，且每个口径都用真实账号全链路验证过（2026-09 实发过审）。

## 能做什么

- **掘金全自动**：`publish 文章.md` 一条龙 = 建草稿（分类+双标签+50~100 字摘要）→ PIL 生成 192×128 封面并 CDP 上传 → 挂专栏（column_ids）→ 发布 → 审核状态自检
- **登录零手工**：`login` 拉起浏览器扫码，自动收割 Cookie（实测约 1 年有效）与真实设备 uuid（随机值会被 WAF 掐 TLS）
- **知乎半自动**：`zhihu 文章.md` 开写文章页，自动填标题 + Markdown→HTML 注入编辑器，发布按钮人工点（无公开 API，尊重风控）
- **机审避坑内置**：URL/域名字符串门禁（「推广类」驳回重灾区）、审核状态机解读（status 0=审核中不是失败）

## 快速开始

```bash
cp scripts/publish.py <你的写作目录>/ && cd <你的写作目录>
uv add websockets pillow
uv run publish.py login        # 扫码
uv run publish.py preview 我的文章.md
uv run publish.py publish 我的文章.md
```

文章用 Markdown + frontmatter（双平台标题 / description 50~100 字 / tags 自动映射掘金真实标签）。

## 与原版 juejin-publisher 的差异

本 skill 是 2026-09 接口口径的全面重制：设备 uuid WAF 规避、真实草稿 ID 字段修正、双标签上限、专栏 column_ids 挂载、PIL 自动封面、审核状态查询、机审驳回修复流程、知乎 CDP 注入。

## License

MIT

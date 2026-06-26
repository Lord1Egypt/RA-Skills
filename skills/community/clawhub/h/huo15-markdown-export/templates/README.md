# 主题选择决策树

| 场景 | 选哪个主题 | 输出格式 | 推荐脚本 |
|---|---|---|---|
| 个人技术博客 / 长文随笔 | `typora-newsprint` | HTML / PDF | `md2pdf` / `md2html` |
| 夜间阅读 / 投影演示 | `typora-night` | HTML | `md2html` |
| 开源项目文档 / GitHub README | `github` | HTML / PDF | `md2pdf` |
| 学术论文初稿 | `academic` | PDF | `md2pdf` |
| 微信公众号发布 | `wechat` | HTML(内联 CSS) | `md2wechat` |
| 小红书长图文 | `xiaohongshu` | PNG 长图 | `md2image` |
| 公司对外报告 / 客户提案 | `huo15-brand` | PDF(带页眉页脚) | `md2pdf` |
| 内部 changelog / 版本对比 | `huo15-brand` | PDF | `md-diff` |

## 想做新主题?

把这个目录里任何一个 CSS 复制为 `themes/<my-theme>.css`,改完在 `scripts/lib/render.js` 的 `AVAILABLE_THEMES` 数组加上名字即可。

主题文件**只允许**写视觉样式——不要在主题里塞 JS,不要 import 远程字体(打印会卡)。

## reference.docx(Word 模板)

`md2docx` 走 Pandoc,默认用本目录的 `reference.docx` 作为字体/页眉模板。

**没有 reference.docx 也能跑**——Pandoc 用内置默认模板。但如果你想要"火一五品牌的 Word 输出":

```bash
# 1. 先用 Pandoc 生成默认 reference.docx
pandoc -o reference.docx --print-default-data-file reference.docx

# 2. 用 Word 打开,改字体(中文 → 等线 / 英文 → Calibri)、改样式、加页眉 logo

# 3. 替换本目录的 reference.docx
mv ~/Downloads/my-reference.docx /Users/jobzhao/workspace/projects/openclaw/huo15-skills/huo15-markdown-export/templates/reference.docx
```

## pdf-print.css

控制 PDF 打印时的额外规则:页眉页脚、避免标题孤行、表格不跨页。**改它会影响所有 PDF 输出**——慎改。

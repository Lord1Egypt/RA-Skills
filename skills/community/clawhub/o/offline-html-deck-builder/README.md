# 离线 HTML 演示稿生成器

这是一个 Codex 技能和起步模板，用来把提案、汇报、复盘和产品叙事做成离线单文件 HTML 演示稿。

适合下面这些场景：

- PDF 太难改。
- PPT 风格老是漂。
- 在线链接有权限或加载问题。
- 读者只需要一个干净的本地成品。

## 适合谁用

- 经常做内部分享、复盘、提案、产品叙事的运营、产品、研究者。
- 不想装 PowerPoint 或 Keynote 也不想学 Reveal.js。
- 想要一个"双击就能打开、单文件可发邮件、不挑浏览器"的演示稿。

## 快速开始

1. 复制 `assets/basic-deck-template.html` 到本地，改名 `deck.html`。
2. 按 `SKILL.md` 写页面大纲，每页一个 `<section>`。
3. 用 `references/deck-checklist.md` 做一次自检：链接、字体、字号、图片权重。
4. 浏览器双击 `deck.html` 打开看效果。

## 文件

- `README.md`：本文件。
- `LICENSE`：MIT 许可证。
- `SKILL.md`：工作流说明。
- `assets/basic-deck-template.html`：单文件起步模板。
- `references/deck-checklist.md`：离线 QA 清单。

## 工作流

1. 先看源材料。
2. 先写文案优先的页面大纲。
3. 再做成单文件 HTML 演示稿。
4. 本地打开并检查。

## 运行环境

只用一个 HTML 文件，不引外部 CDN，不引网络字体，本地双击即可。需要浏览器支持 ES2017 即可，Chrome / Edge / Safari 近三年版本都通过。

## 反馈与贡献

有问题或想贡献，开 Issue 即可。如果想贡献一份新模板，放到 `assets/` 下并补上对应的 `SKILL.md` 段落即可。

## 许可证

MIT。

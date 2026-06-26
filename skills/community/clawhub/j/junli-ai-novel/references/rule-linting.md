# 规则化文本检查

用于把部分高频写作问题，从“经验提醒”进一步沉淀成可复用、可维护的规则。

默认定位：

- 这不是替代人工审稿的万能器
- 它只负责抓高频、低语义歧义、适合规则化的问题
- 它优先服务长篇项目的稳定性，而不是追求文学审美自动评分
- 它现在支持“关键词 + 正则 + 证据摘录”，但依然只是静态预审，不等于完成语义审稿

## 当前规则范围

当前优先覆盖 3 类问题：

- AI 套语
- 结尾升华 / 结尾总结
- 视角越权提示
- 对白说明感
- 正文解释腔
- 转场连接词过密

相关命令：

- `python3 scripts/chapter_pipeline.py lint <章节文件路径>`
- `python3 scripts/chapter_pipeline.py dialogue-pass <章节文件路径>`
- `python3 scripts/chapter_pipeline.py consistency <章节文件路径> --project-path <项目目录>`
- `python3 scripts/chapter_pipeline.py review <章节文件路径> --project-path <项目目录>`

规则文件放在：

- `rules/novel-lint/*.yaml`

## 规则字段

每条规则至少包含：

- `id`
- `name`
- `description`
- `severity`
- `scope`
- `type`
- `threshold`
- `message`
- `keywords`

## scope 约定

- `full`：全章检查
- `ending`：只检查结尾段

后续可扩展：

- `dialogue`
- `heading`
- `outline`
- `intent`

## 使用原则

1. 先把高频问题做成规则，不要一开始就追求覆盖所有文学判断。
2. 规则命中后只输出提示，不直接替换正文。
3. 同一个问题如果经常误报，就调 scope、threshold 或关键词，不要强上复杂判断。
4. 规则层主要服务：
   - 写后快速报警
   - 长篇项目批量巡检
   - 把经验变成可复用资产

## 当前最适合规则化的问题

- AI 微表情套语
- 感悟式结尾
- 感叹式结尾
- 视角越权提示
- 标题疲劳
- 重复钩子词

## 不适合直接规则化的问题

- 人物弧线是否高级
- 这章是否真的好看
- 审美是否打动读者
- 整体题材是否有爆款潜力

这些仍应由长篇治理、人工判断和阶段/卷审计负责。

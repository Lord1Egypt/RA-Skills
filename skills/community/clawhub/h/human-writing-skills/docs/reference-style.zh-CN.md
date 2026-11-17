# 参考文风对齐

这个模块把明确输入的参考资料转化为可迁移的写作特征，而不是复制原文内容。

## 激活门槛

只有以下任一信号存在时才激活：

- 一个或多个 `--reference` 文件
- 明确的 `--reference-style` 指令
- 任务中出现“参考这段文风”“贴近该笔调”“match this voice”等明确要求

单独输入 `--context` 永远不会激活文风对齐。`context` 保存剧情事实和连续性，
`reference` 只提供文风证据。前文章节若既是事实来源又是文风来源，应分别传入。

## 提炼维度

模型先生成内部文风卡，观察视角、句长和停顿、词汇层级、意象密度、场景描写、
人物描写、对白节拍、情绪表达和转场方式，再按当前文体有选择地应用。

长参考资料会在全局字符预算内抽取开头、中段和结尾。与其塞入整本书，更推荐
提供几段真正具有代表性的材料。

## 事实优先级与边界

人物、关系、时间线、世界规则和剧情事实始终以用户输入及 `--context` 为准。
不得从参考资料复制人名、事件、结论、标志性句子或独特比喻。对于在世作者或
辨识度极高的作者，只提炼高层技法，例如“短句、克制、动作白描”，不做近似复刻。

## 写作与审稿

```powershell
human-writing-skills build --style fiction --reference sample.md --task "续写下一章。"
human-writing-skills audit --draft chapter.md --reference sample.md --profile style-match
human-writing-skills pipeline --draft chapter.md --reference sample.md --auto --output-dir audit
```

流水线中只有 `style-match` 阶段接收参考资料，逻辑、人物、关系、物理、数字和校对
阶段不会被范文内容干扰。

# 改写保真、统计与保守修复

这三类工具都按需使用。普通生成不会加载原文对照、统计计算或机械清理规则，避免
无关模块占用 Token。

## 三种输入材料

| 输入 | 负责什么 | 激活条件 |
| --- | --- | --- |
| `--original` | 被改写文本的原意 | 只有明确传入时才启用 `rewrite-fidelity` |
| `--reference` | 可迁移的文风特征 | 只有明确范文或文风要求时启用 |
| `--source` | 事实证据 | 只用于论文、公文、新闻、法律、技术等严肃文本 |

不要把 `--reference` 当成事实来源。除非同一份材料又被明确作为范文传入，否则
`--original` 只约束语义，不要求模仿原文写法。

## 保持原意的改写

```powershell
human-writing-skills build --style self-media --original original.md --task "不增加事实，只改得更清楚。"
human-writing-skills audit --draft revised.md --original original.md --profile fidelity
human-writing-skills pipeline --draft revised.md --original original.md --auto --output-dir audit
```

`fidelity` 会比较实体、数字、正反关系、不确定程度、时间顺序、因果、比较标准、
归因和限制条件，并标出遗漏、扩大、反转、错归因、乱序和凭空新增。它保护的是
意思，不要求保留原文的病句或啰嗦表达。

## 快捷 Humanize 与声音保护

```powershell
human-writing-skills humanize --draft original.md --style fiction --mode quick
human-writing-skills humanize --draft original.md --style fiction --mode deep
human-writing-skills audit --draft revised.md --original original.md --profile preservation
```

`quick` 只加载表层模式、原意保真和 `voice-ambiguity-preservation`；`deep`
才追加套话、公式结构、段落推进、不完美语流和编辑循环。除非显式传入
`--with-examples`，示例库不会占用 prompt。

`preservation` 会对照原文检查有意义的含混、重复、母题、迟疑、潜台词、人物
口吻和未结互动压力。它必须提供 `--original`，不会进入自动流水线，并且要把这些
特征与指代不清、漏字和真实语病区分开。

## 可选文体统计

```powershell
human-writing-skills stats --draft article.md --style self-media
human-writing-skills pipeline --draft article.md --auto --with-stats --output-dir audit
```

统计包括句长和段长变化、移动平均词汇丰富度（MATTR）、重复三元组比例与显式
连接词密度。中文、日文主要使用汉字/假名字符 Token，拉丁字母语言和阿拉伯文
使用 Unicode 单词型 Token，不同分词体系的 MATTR 不能直接横向比较；短文本会
标为低置信度。项目不使用容易被篇幅强烈影响的原始词形符比作为结论。

这些指标只用于编辑诊断，不用于判断作者身份。应在相同语言、文体和目标声音中
比较，而不是套一个万能阈值。

## 保守修复预览

```powershell
human-writing-skills fix --draft article.md --preview
human-writing-skills fix --draft article.md --output cleaned.md
human-writing-skills fix --draft article.md --apply
```

默认只预览。自动修改仅限高置信机械残留，例如成稿中的聊天助手结尾，以及少量
语义等价的空头引导语和英文冗长表达。它不会自动改写观点、数字、比较结构、人物
口吻或需要上下文判断的句法。

## 连续“比”比较

同句出现两个有效“比”分句时，扫描器给出复核信号 `STR002`；小说、网文、
自媒体和一般文字中出现三个以上时，升级为高风险 `STR004`。论文与新闻中的必要
数据比较会被抑制。修改时保留比较标准明确且各自承载独立事实的部分，把纯装饰性
递进改成一个观察、动作、意象或后果。`fix` 不会机械删除这些句子。

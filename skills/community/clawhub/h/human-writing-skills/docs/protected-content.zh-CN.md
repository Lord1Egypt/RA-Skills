# 受保护内容校验

## 按需激活

自动保护采用严格门槛：

- 使用 `academic-paper`、`formal-document`、`news-report` 生成严肃文本时自动开启。
- 未指定类型的法律和技术成稿，必须同时命中多项文书特征才开启。
- 小说、网文、自媒体、普通问答、搞怪文本和角色扮演默认不开启。
- 单独出现一个数字、链接或专有名词，不足以触发保护模块。
- 用户显式使用 `--protect-content` 或 `--protect-term` 时，无条件开启。

审稿材料特征不足时，可以指定 `--document-type legal`、`technical`、
`academic-paper`、`formal-document` 或 `news-report`；误判时可指定叙事类型关闭自动保护。多阶段
流水线只在最后一个合适阶段加载一次自动保护清单，不在每轮重复占用 tokens。

模块还会锁定主张、研究结果、限制条件、归因对象和结论的肯否方向。CLI 可以机械
识别部分缩写、标准号、产品标识和 `《正式名称》`，但不会假装自己能准确识别所有
人名和机构名；重要专有名词应使用 `--protect-term` 明确指定。

润色和改写可能悄悄改掉百分比、引文编号、公式、链接、代码、原话或指定术语。
保护分成两步：

1. 审稿时加入 `--protect-content` 或 `--protect-term`，让模型收到保护清单；发现
   疑似错误只能报告，不能自行改数值。
2. 改写完成后运行 `verify`，对原文和候选稿做确定性比较。

```powershell
human-writing-skills audit --draft original.md --protect-content --protect-term "星港计划"
human-writing-skills verify --source original.md --candidate revised.md --protect-term "星港计划"
```

退出码 `0` 表示原文保护项仍然存在；退出码 `1` 表示至少一项缺失或发生改变。
候选稿新增的数字等内容会单独列出。这个工具只检查文字是否被改，不判断原始事实
本身是否正确。

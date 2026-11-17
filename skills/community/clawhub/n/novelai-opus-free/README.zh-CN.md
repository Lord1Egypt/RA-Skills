# OpenClaw NovelAI Opus Free

这是一个专门面向 Opus 订阅、同时保留实测免费图片编辑能力的“零 NovelAI 图片 Anlas”OpenClaw Skill 变体。

它保留小说写作、剧情规划、Prompt 设计、账户查询、费用估算、标签建议和本地记录。在 Opus、正常分辨率、单张、28 steps 以内且估算明确为 `0 Anlas` 时，允许文生图、图生图、局部重绘、已有 Vibe 生图、标注，以及部分 Director 工具。

它会禁止：

- 新的 Vibe 编码；
- Director 去背景；
- Precise Reference；
- Enhance；
- 专用放大；
- 批量、高分辨率、超过 28 steps、多样本和并行生图；
- 任何扣 Anlas 的降级或重试。

第一次成功完成零 Anlas 验证后，同一会话内只要计费参数不变，就可以持续复用验证结果，不设置时间或次数上限。新会话、OpenClaw/MCP 重启、参数变化、工具报错、账户警告或用户主动要求复查时，才重新执行完整验证。

图片操作遇到网络断开、MCP 临时故障、429、临时 5xx 等明确的临时失败时，首次失败后最多顺序重试 3 次，且参数完全不变。参数错误、鉴权/扣费错误、账户或 Usage Limit 异常，以及无法确认服务端是否已经处理请求的情况，不会自动重试。

## 重要区别

“零 Anlas”不等于“没有任何使用额度或费用”：

- Opus 的 V5 免费图片会消耗独立的 V5 Usage Limit；
- 如果 OpenClaw 把文字请求交给第三方模型，第三方模型可能单独收费；
- 网络、主机和其他模型的费用不属于本 Skill 的控制范围。

## 使用边界

如果不是 Opus、费用估算工具缺失、返回空值、返回未知、V5 Usage Limit 已耗尽，或者余额审计发现扣点，Skill 会拒绝或停止后续图片操作。它不会因为用户说“我接受收费”就放行。

想使用新的 Vibe 编码、去背景、Precise Reference、Enhance、专用放大、批量或高分辨率，请改用父项目中的高级版 `openclaw-novelai`。

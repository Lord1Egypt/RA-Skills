# 伏笔回收清单

把章节摘要或短段落变成清楚的伏笔追踪表：你能一眼看到线索从哪里埋下、是否兑现，以及下一步该在哪个已有剧情节点回收。它只依据你提供的材料，不续写整本小说，也不输出总评分。

![伏笔回收清单推广图](assets/promo-1600x900.png)

## 安装

```bash
npx skills add xxjrq/novel-foreshadow-map-cn
```

## 使用

粘贴单次章节、场景摘要或原文短段落；可附章节号、角色关系和已知后续节点。结果包含“伏笔/线索、首次埋点、证据摘述、已兑现/待兑现/待确认、回收位置”。一次最多100行；更长内容请分批发送。

缺少前后章节、角色关系或关键事件时，Skill 会先列出缺项，并保留“待确认”，不会把猜测写成结论。

## 样例

- [成功样例](fixtures/success.md)：跨章节线索的已兑现清单。
- [资料不足样例](fixtures/failure.md)：如何明确缺项而不臆测。

## 参考与许可证

业务用途参考：[story-skills](https://github.com/danjdewhurst/story-skills) 的公开仓库及其 [revision-continuity Skill](https://github.com/danjdewhurst/story-skills/blob/main/skills/revision-continuity/SKILL.md)。本仓库的说明、流程和示例均为原创，未复制其文本或代码；本仓库以 [MIT-0](LICENSE) 发布。

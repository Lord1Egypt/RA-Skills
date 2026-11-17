# 小说考据资料卡

![小说考据资料卡推广图](assets/promo-1600x900.png)

把你已有的摘录、官方链接和设定问题，整理成可追溯的小说资料卡：哪些事实能写进正文、出处在哪里、可采取什么叙事处理、还缺什么证据一目了然。它只处理你交来的材料，不用猜测替代证据，也不会冒充历史、医疗或法律专业结论。

## 输入与结果

输入是单次章节、场景或短文相关的用户材料（文字、摘录、最多 100 行表格，或可访问的官方链接）和一个明确的设定问题；可附时代、地点和叙事目标。结果是一张 Markdown 资料卡，包含来源定位的可用事实、明确标注为“创作推导”的写作建议、证据边界和待补资料。内容超过边界时会要求分批，绝不假称已经读完全文。

## 安装

```bash
npx skills add xxjrq/novel-research-notes-cn
```

## 使用示例

把材料和问题一起交给 Skill，例如：

```text
根据我贴出的两条港务记录，守夜人能否在 1926 年凌晨用电话通知警署？请给出设定资料卡。
```

- [成功输入](fixtures/success-input.md) → [成功交付](fixtures/success-example.md)：证据足够时的事实表、来源定位与叙事建议。
- [缺料输入](fixtures/failure-input.md) → [缺料交付](fixtures/failure-example.md)：医疗相关材料不足时如何停止推断并说明边界。

## 边界

- 仅把用户材料或用户提供的官方链接直接支持的内容列为事实。
- 资料不足时给出具体缺项，而不是编造出处、页码或结论。
- 历史、医疗、法律话题只整理材料，不构成专业意见；现实决策请复核权威一手来源或咨询合格专业人士。

## 自检

在本目录运行：

```bash
python3 scripts/self_test.py
```

该检查只验证本仓库的必需文件、命名、元数据、示例链接和 PNG 资产，不声称验证模型生成质量。

## 来源与许可证

本 Skill 为原创说明与示例；业务方向仅参考 [story-skills research](https://github.com/danjdewhurst/story-skills/tree/main/skills/research)，已核对其 [MIT 许可证](https://github.com/danjdewhurst/story-skills/blob/main/LICENSE)，未复制其文本或代码。项目采用 [MIT-0](LICENSE)。

# 读者反馈改稿待办

![读者反馈改稿待办推广图](assets/promo-1600x900.png)

把已收到的读者或编辑意见，整理成可直接执行的小说改稿待办。输入反馈和章节摘要，得到去重问题组、受影响章节、优先级、完成标准及每项依据；它不会重新评分，也不会伪造读者评价。

## 输入与结果

输入单次章节、场景或短文的读者/编辑意见，以及章节编号、标题或摘要。输出为：

- 去重后的问题组与合并依据
- 每组可确认的影响章节
- 高/中/低优先级改稿动作与完成标准
- 需要补充的材料或无法确认的边界

表格最多100行；更长的材料请按章节分批。缺少反馈或章节摘要时，Skill 会列出缺项，不假装读完或补造结论。

## 安装

```bash
npx skills add xxjrq/novel-feedback-actionlist-cn
```

## 使用

粘贴反馈与章节摘要后说：“请整理成改稿待办。” 可直接参考：[成功样例](fixtures/success.md)｜[缺料样例](fixtures/failure.md)。

## 自检

```bash
python3 scripts/self_test.py
```

## 来源与许可证

本 Skill 为原创的中文工作流与样例；仅参考 [story-skills 的 feedback-triage 用途说明](https://github.com/danjdewhurst/story-skills/blob/main/skills/feedback-triage/SKILL.md)，未复制其内容或代码。许可证见 [MIT-0](LICENSE)。

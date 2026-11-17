# 角色成长弧线卡

![角色成长弧线卡推广图](assets/promo-1600x900.png)

把零散的角色资料变成一张可写、可核对的成长弧线卡：明确角色的欲望、缺陷、转折、最终选择，以及它们该落在什么章节。适合中文小店经营者、小说作者和自媒体创作者设计人物故事线。

## 你会得到什么

一张独立 Markdown 卡片，可直接粘贴到任意写作工具，包含：

- 已知事实及其章节依据
- 核心欲望与核心缺陷
- 起点、受压、转折、终局四阶段弧线
- 可场景化的最终选择与代价
- 章节锚点清单和待确认项

它不会续写小说，也不会把缺失信息编造成事实。

## 输入

提供角色设定、故事概要、已写章节三项。完整示例见 [fixtures/success/lin-wan.json](fixtures/success/lin-wan.json)。

```json
{
  "角色设定": {"角色名": "林晚", "身份": "花店店主"},
  "故事概要": "她想守住花店，却必须学会与妹妹合作。",
  "已写章节": [{"编号": "第1章", "关键事件": "她拒绝求助。"}]
}
```

若缺少任一项，Skill 会只指出缺失字段并停止；参见 [失败样例](fixtures/failure/missing-chapters.json)。

## 使用

将上述输入和“请按角色成长弧线卡生成”交给支持 Markdown Skill 的写作助手。它会遵循 [SKILL.md](SKILL.md) 的固定卡片格式。输入原有字段和值会原样保留；推断会标为“创作建议”，无法判断的内容会列为“待确认”。

## 自检

```bash
python3 scripts/self_test.py
```

该命令仅校验仓库结构、元数据、图片尺寸与成功/失败样例契约；真实行为由 [SKILL.md](SKILL.md) 的 Markdown 工作流定义，不存在伪造的业务引擎。

## 来源与许可证

参考范围与未采用说明见 [sources/chinese-novelist-skill.md](sources/chinese-novelist-skill.md)。本仓库采用 [MIT-0](LICENSE)。

## 安装

```bash
npx skills add xxjrq/novel-character-arc-cn
```

## 完整输出示例

查看 [成功输出](fixtures/forward-success.md) 和 [缺资料响应](fixtures/forward-failure.md)，对照上述输入样例了解实际交付内容。

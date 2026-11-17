# 小说投稿梗概包

![小说投稿梗概包推广图](assets/promo-1600x900.png)

把已有小说素材快速整理成编辑可读的投稿资料：一次交付 300、800、1500 字三档梗概和人物关系摘要，保留完整结局与关键因果。

## 你会得到什么

- 适配不同投稿要求的三档梗概
- 清楚呈现人物关系、冲突与变化的摘要
- 已知事实、建议和待确认事项的明确区分

这是一项纯 Markdown Skill：不需要服务、第三方 API 或登录。它只整理你提供的资料，不进行小说评分、市场判断或章节写作。

## 使用

提供完整故事概要、逐章摘要和投稿长度要求。最小输入见 [fixtures/success.json](fixtures/success.json)。Skill 会依照 [SKILL.md](SKILL.md) 的输出格式生成资料包。

若缺少关键字段，会明确指出缺项而不编造，见 [fixtures/failure-missing-fields.json](fixtures/failure-missing-fields.json)。

## 本地检查

```bash
python3 scripts/self_test.py
```

该检查仅验证仓库结构、元数据、素材尺寸和成功/失败样例的数据形状；不模拟语言模型，也不把格式检查误报为梗概质量验证。

## 来源与许可

用途参考与许可证说明见 [sources.md](sources.md)。本仓库使用 [MIT-0](LICENSE)。

## 安装

```bash
npx skills add xxjrq/novel-synopsis-pack-cn
```

## 完整输出示例

查看 [成功输出](fixtures/forward-success.md) 和 [缺资料响应](fixtures/forward-failure.md)，对照上述输入样例了解实际交付内容。

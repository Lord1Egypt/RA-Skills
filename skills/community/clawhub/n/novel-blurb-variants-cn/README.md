# 小说简介与封底文案

![小说简介与封底文案推广图](assets/promo-1600x900.png)

把已有故事梗概变成读者愿意继续看的封底简介：一次交付三种定位不同、且不泄露禁剧透点的中文版本，并附一句可用于商品页或宣传物料的卖点。

适合中文小店经营者、小说作者与自媒体创作者。它只产出书籍简介，不做封面设计、视频推文分镜或投稿梗概。

## 输入与结果

提供以下真实信息：

- 故事梗概：主角、起点、冲突、关系或选择，以及可公开的剧情范围。
- 类型：例如悬疑、言情、历史、科幻、治愈成长。
- 禁剧透点：任何不可公开的身份、反转、结局、人物生死或关键线索；没有时写“无”。

Skill 返回：

- 情绪与人物、冲突与类型、主题与气质三种简介（每版 120–220 字）。
- 一句 18–36 字、无剧透且可感知的卖点。

## 使用

在请求中调用 `$novel-blurb-variants-cn`，并按如下形式提供素材：

```text
故事梗概：九十年代末，县城电台夜班主持人林岚收到一盘匿名磁带……
类型：悬疑成长
禁剧透点：磁带录制者、姐姐下落、旧矿区事件真相、结局人物生死
```

若缺少任一关键字段，Skill 会明确指出缺失项，不编造人物、剧情或类型。完整成功样例在 [`fixtures/success.json`](fixtures/success.json)：其中 `expected_output` 明确三版简介的定位、字数、卖点和禁剧透验收条件。仅缺类型的失败样例在 [`fixtures/failure-missing-type.json`](fixtures/failure-missing-type.json)：其中 `expected_error` 规定只要求补充“类型”。

## 自测

在本仓库根目录运行：

```sh
sh scripts/self-test.sh
```

该命令验证发布结构、元数据、PNG 尺寸及样例验收契约；它不会声称生成了真实文案。真实文案质量、事实忠实度和剧透控制仍须按 fixture 中的预期条件审阅模型输出。

## 来源与许可证

公开用途参考与采用边界记录在 [sources/attribution.md](sources/attribution.md)。本仓库以 [MIT-0](LICENSE) 发布。

## 安装

```bash
npx skills add xxjrq/novel-blurb-variants-cn
```

## 完整输出示例

查看 [成功输出](fixtures/forward-success.md) 和 [缺资料响应](fixtures/forward-failure.md)，对照上述输入样例了解实际交付内容。

# 人物知情状态账本

把跨场景的“谁何时知道什么”变成可核查账本，迅速发现人物在获知前就使用信息的连续性问题。输入按故事顺序的场景、事实编号与人物亲历/告知/推测的非空原文证据；结果给出人物×事实知情矩阵、首次得知场景、确信/猜测/未知状态，以及提前使用信息的位置。没有人物证据的项会标为未知，只有推测则标猜测；没有场景顺序或证据时先请求补充，不以读者所知替代人物所知。

![人物知情状态账本：追踪每个人何时知道关键事实，提前发现获知前使用信息](assets/promo-1600x900.png)

```bash
npx skills add xxjrq/novel-knowledge-state-ledger-cn
```

## 适用范围

适合最多 10 名人物、30 项事实、20 个场景的小说连续性核对。只追踪信息传播；不评价叙事视角风格，也不设计伏笔回收。

## 输入格式

每个场景按故事发生顺序排列。证据包含 `character`、`fact`、`type` 和 `quote`；`type` 可为 `experienced`、`told`、`inferred` 或 `used`。

```json
{"characters":["甲","乙"],"facts":[{"id":"F-密钥","text":"密钥藏在钟楼"}],"scenes":[{"id":"S1","evidence":[{"character":"甲","fact":"F-密钥","type":"experienced","quote":"甲亲手藏入钟楼。"}]}]}
```

## 交付参考与自检

- [成功输入](fixtures/success-input.json)：乙在第 3 场获告知、却在第 2 场使用密钥。
- [成功输出](fixtures/success-output.json)：标出乙的首次知情为 `S3`，并单列 `S2` 的提前使用。
- [失败输入](fixtures/failure-input.json) 与 [失败交付](fixtures/failure-output.md)：仅有角色名时请求场景和证据，不能生成矩阵。

```bash
node scripts/self-test.mjs
```

自检会真实运行成功样例与缺料失败样例。无需浏览器、账号或外部服务。

## 来源与许可

业务用途曾核对 [story-skills 的 revision-continuity 页面](https://github.com/danjdewhurst/story-skills/blob/main/skills/revision-continuity/SKILL.md)，本仓库的说明、流程和样例均为原创，未复制其文本或代码。仓库采用 [MIT License](LICENSE)。

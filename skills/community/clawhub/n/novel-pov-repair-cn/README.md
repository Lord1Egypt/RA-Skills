# 叙事视角诊断与修订

把一段小说场景和指定视角人物交给它，即可得到可定位的 POV 越界、原因说明，以及不改变情节的最小修订片段。它只修正具体视角跳跃，不把任务扩展成通用润色、去 AI 味或综合审稿。

![推广图](assets/promo-1600x900.png)

## 安装

```bash
npx skills add xxjrq/novel-pov-repair-cn
```

## 使用

```text
使用 $novel-pov-repair-cn 检查以下文本。视角人物：林岚，第三人称限知。请定位越界并给出最小修订，保留原有动作、台词和人物知道的信息。
场景文本：粘贴本次要检查的章节、场景或短文。
```

## 输入与结果

输入：单个章节、场景或短文，以及视角人物（建议同时说明第一/第三人称和限知范围）。单次仅处理一批材料；表格最多 100 行，超出时请分批。

结果：逐处列出原句片段、是否越界、越界原因，以及保持原情节的改写片段。缺少场景文本或视角人物时，会直接列出缺项，不虚构上下文。

可复制的实际参考交付：[成功样例](fixtures/success.md)｜[缺项样例](fixtures/failure.md)。

完整执行结果：[成功输出](fixtures/forward-success.md)｜[缺料输出](fixtures/forward-failure.md)。单项缺料示例：[仅缺视角人物](fixtures/failure-missing-viewpoint.md)｜[仅缺文本](fixtures/failure-missing-text.md)。修订保留原有动作、台词与人物知情，不把内心活动改成新对话。

## 自检

```bash
node scripts/self-test.mjs
```

该命令只检查本仓库的结构、元数据、图标尺寸和示例内容，不依赖其他 Skill、网络或本机绝对路径。

## 来源与许可

业务定位参考了 [story-skills / scene-craft](https://github.com/danjdewhurst/story-skills/blob/main/skills/scene-craft/SKILL.md) 的公开写作技能方向；本仓库的说明、流程与样例均为原创，未复制其文本或代码。仓库采用 [MIT License](LICENSE)。

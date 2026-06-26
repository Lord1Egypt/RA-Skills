# NextFromKnowledge

Don't just connect knowledge. Turn it into the next action, plan, or decision.

`NextFromKnowledge` 是“知识行动官”这条产品线的第一版可发布仓库。它承接 `LinkMind` / `Knowledge Connector` 之后的阶段，把笔记、调研、会议纪要和知识图谱结果，压缩成真正能推进事情的下一步。

它要解决的问题很直接:
- 知道了很多，然后呢
- 这些知识足够支持什么决定
- 现在先做动作、做计划，还是先跑一个小实验
- 还缺什么信息才真的会改变结论

## 适合的输入

- 研究笔记
- 会议纪要
- 访谈摘要
- 脑暴记录
- strategy memo
- Knowledge Connector 的搜索或图谱结果

## 核心命令

```bash
nfk next-step --file notes.md
nfk next-step --text "用户访谈里 5 次提到 onboarding 不清楚，本周只有 2 天开发时间，先安排 3 个新用户验证首页文案"
nfk plan --file research.md --horizon 7d
nfk decide --file options.md --options "方案A,方案B,方案C"
nfk experiment --file summary.md
nfk gaps --file summary.md
nfk analyze --file summary.md --json
```

## 输出方向

默认输出会落到这几类之一:
- 下一步动作
- 短计划
- 决策建议
- 最小实验
- 关键缺口

它不是总结器。它的默认目标是推动事情继续往前。

## 仓库结构

```text
next-from-knowledge/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── RELEASE.md
├── clawhub.json
├── package.json
├── agents/openai.yaml
├── references/action-frames.md
├── bin/cli.js
├── src/index.js
├── test/test.js
└── scripts/publish.sh
```

## 本地验证

```bash
node test/test.js
node bin/cli.js next-step --text "用户访谈重复提到首屏不清楚，本周只有 2 天开发时间，先安排 3 个新用户验证首页文案"
```

## 建议安装名

```bash
clawhub install next-from-knowledge
```

## 发布

```bash
npm run publish:clawhub
```

或直接执行:

```bash
sh ./scripts/publish.sh
```

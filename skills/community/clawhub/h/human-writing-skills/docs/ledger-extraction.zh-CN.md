# 连续性账本自动提取

`extract-ledger` 用来降低长篇审查的起步成本。它不假装能在本地推断正史，也不会自行调用模型；
它只编译一份有边界、以证据为先的提取 Prompt，供已接入的写作 Agent 生成**待确认账本**。

```powershell
human-writing-skills extract-ledger `
  --draft chapters-01-10.md `
  --context novel-ledger.md `
  --output ledger-extraction-prompt.md
```

把生成的 Prompt 交给你实际使用的模型运行，再审核其中的变更，最后才合并到正式账本。

## 提取范围

- 人物当前状态、携带道具、服装、伤势、能力与资源消耗；
- 承诺、债务、未解问题、信息边界和互动欠账；
- 占位、相对位置、阻隔、可触达对象和明确写出的移动过渡；
- 不能因“文中没再提到”就被擅自改写的冲突项与未知项。

每条记录都必须带证据，并标记为 `observed`（观察到）、`inferred`（推断）、`conflicted`
（冲突）或 `unknown`（未知）。除非新正文明确改变，否则旧账本仍是权威。

它让维护账本更省力，但不取代编辑判断。确认事实、解决冲突后，再把正式账本传给
`audit --context`、`pipeline --context` 或 `chunk-audit --outline`。

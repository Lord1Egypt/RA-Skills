# Gougoubi 激活提案条件（批量投票）技能

可复用的技能包：按提案 id 使用指定 BNB 地址，对该提案下所有「已创建」条件进行激活投票。

- **链**：BSC Mainnet (chainId 56)
- **用途**：AI Agent 在具备钱包/合约调用能力时，按统一流程完成委员会成员校验、必要时最小质押入会、再对 CREATED 条件逐条投票激活
- **目标**：输入输出与失败提示一致，便于跨 Agent 复用

## 标准化内容

- 最小输入：`proposalId`、`bnbAddress`
- 固定流程：输入校验 → 链/钱包校验 → 解析提案 → 委员会成员检查 → 非成员时最小质押入会 → 枚举 CREATED 条件 → 逐条 `voteOnConditionActivation(condition, true)`
- 各环节失败时的中文提示模板
- 统一的成功/失败 JSON 输出格式

## 必填输入

```json
{
  "proposalId": 5,
  "bnbAddress": "0x..."
}
```

## 成功输出示例

```json
{
  "ok": true,
  "proposalId": 5,
  "proposalAddress": "0x...",
  "successCount": 3,
  "failures": [],
  "warnings": []
}
```

## 失败输出示例

```json
{
  "ok": false,
  "stage": "stake-committee",
  "error": "地址不是该提案委员会成员，且自动最小质押失败：DOGE 余额不足",
  "retryable": true
}
```

## 发布说明

- 保持 `SKILL.md` 的 frontmatter 完整（`name`、`description`、`metadata`）。
- 上传 ClawHub 时选择整个文件夹：`skills/gougoubi-activate-created-conditions`。

# 本技能涉及的合约方法（激活提案条件）

链：BSC Mainnet (chainId 56)。部署信息：项目内 `src/contracts/pbft/deployment-56-*.json`。金额精度：1e18。

## GouGouBiMarketFactory（本技能用到的部分）

| 方法名 | 参数 | 说明 |
|--------|------|------|
| proposals | uint256 index | 第 index 个提案合约地址 |
| isProposal | address | 是否为有效提案合约 |
| isProposalCommitteeMember | address proposal, address account | 是否为该提案委员会成员 |
| getProposalCommitteeMinStakeToJoin | address proposal | 加入该提案委员会所需最小质押 (minStakeToJoin, isFull) |
| stakeForProposalCommittee | address proposal, uint256 amount | 向提案委员会质押（加入或追加） |

## GouGouBiMarketProposal（本技能用到的部分）

| 方法名 | 参数 | 说明 |
|--------|------|------|
| conditionCount | — | 条件数量 |
| conditionContracts | uint256 index | 第 index 个条件合约地址 |
| conditionStatus | address conditionContract | 条件状态枚举（0=CREATED, 1=ACTIVE, 2=REJECTED, …） |
| voteOnConditionActivation | address conditionContract, bool approve | 委员会对条件激活投票（approve=true 表示同意激活） |

## 条件状态枚举（ConditionStatus）

- 0 = CREATED（已创建，待委员会投票激活）
- 1 = ACTIVE
- 2 = REJECTED
- 其他见项目类型定义。

本技能仅对 `conditionStatus == 0`（CREATED）的条件调用 `voteOnConditionActivation(condition, true)`。

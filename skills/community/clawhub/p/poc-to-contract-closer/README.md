# poc-to-contract-closer

POC 转签约收口助手。用于把 closeable POC 转成可执行签约路径，检查决策人、采购路径、closing 窗口、冷却阈值、报价动作和上线节点。

## Quick Start

```bash
node src/generator.js \
  --pass-rate 93 \
  --p0 0 \
  --p1 2 \
  --decision-maker "业务负责人已确认" \
  --procurement-path "比价采购" \
  --launch-window "6月试点上线" \
  --silence-days 7 \
  --accepted-value "核心价值已确认"

npm test
```

## Boundary

本 Skill 不生成价格、折扣、合同条款或虚假紧迫性。采购路径未知、closing 窗口缺失、冷却阈值触发或 P0 未清时，不应直接推进报价。

# Step 4: Code And Training Attack Surface

## Goal

把论文背后的代码、配置、训练流程、评估流程转成答辩问题和证据检查清单。

## When code is available

Inspect or ask for:

- README
- dependency specs
- training entry point
- evaluation entry point
- data preprocessing
- model implementation
- loss implementation
- configs
- baseline configs
- logs
- checkpoints
- seed and hardware records

## When code is unavailable

Still generate likely questions, but mark answers as `missing_evidence` unless supported by the paper.

## Required tables

### Paper-to-code mapping

| Paper object | Paper location | Code path | Function/class | Config key | Evidence strength | Risk |
|---|---|---|---|---|---|---|

### Training-run audit

| Run/config | Dataset | Seed | Hardware | Hyperparameters | Result | Matches paper? | Notes |
|---|---|---|---|---|---|---|---|

### Code/training defense questions

| Question | Trigger | Evidence to check | Safe answer | Missing-evidence answer | Backup material |
|---|---|---|---|---|---|

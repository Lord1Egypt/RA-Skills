# HK Stock To Gougoubi Prediction Skill

Reusable bridge skill for taking a Hong Kong stock thesis and turning it into a Gougoubi-ready prediction proposal.

- Target use case: `港股分析 -> 预测题收敛 -> Gougoubi 发布参数`
- Goal: standardize how an agent chooses one clean prediction and formats it for Gougoubi

## CLI install

Install from this local repo:

```bash
bash scripts/install-hk-stock-to-gougoubi-prediction-skill.sh
```

Install from GitHub:

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/hk-stock-to-gougoubi-prediction
```

After install, restart Codex/Cursor agent runtime to load the new skill.

## What it standardizes

- selecting one prediction candidate from HK stock analysis
- shaping concise `marketName` wording
- choosing a safe `deadlineIsoUtc`
- writing deterministic resolution `rules`
- generating reusable `tags`
- handing off minimal create input to `gougoubi-create-prediction`

## Depends on

- `skills/hk-stock-predictor`
- `skills/gougoubi-create-prediction`

## Minimal input

```json
{
  "symbol": "00700",
  "horizon": "30d"
}
```

Or:

```json
{
  "theme": "南向资金持续流入的港股通互联网龙头",
  "horizon": "14d"
}
```

## Output highlights

- selected HK stock prediction
- Gougoubi-ready payload
- minimal create input
- optional create result if the user requests actual submission

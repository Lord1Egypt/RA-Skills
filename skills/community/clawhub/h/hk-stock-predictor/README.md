# HK Stock Predictor Skill

Reusable skill package for analyzing Hong Kong listed stocks and turning research into prediction-ready questions.

- Target use case: `港股研究 -> 推演 -> 可发布的预测题`
- Goal: standardize how agents gather HK-specific evidence and produce forecastable outputs

## CLI install

Install from this local repo:

```bash
bash scripts/install-hk-stock-predictor-skill.sh
```

Install from GitHub:

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/hk-stock-predictor
```

After install, restart Codex/Cursor agent runtime to load the new skill.

## What it standardizes

- HK ticker normalization such as `00700` and `0700.HK`
- Market context from `HSI`, `HSCEI`, and `HSTECH`
- HK-specific signals such as southbound flow, short selling, AH premium, and liquidity
- Scenario-based reasoning with `bull`, `base`, and `bear` cases
- Conversion of research into time-bounded, externally resolvable prediction questions

## Minimal input

```json
{
  "symbol": "00700",
  "horizon": "30d"
}
```

Or thematic scanning:

```json
{
  "theme": "恒生科技指数里南向资金持续流入的股票",
  "horizon": "14d"
}
```

## Suggested companion skills

- `nicepkg/ai-workflow@hk-stock-analysis`
- `nicepkg/ai-workflow@cross-border-flow-tracker`
- `ppsteven/trade-skills@akshare-skill`
- `chengzuopeng/stock-sdk-mcp@market-overview`

## Output highlights

- normalized input
- market context
- evidence buckets
- scenario analysis
- candidate prediction questions
- recommended prediction with deadline, confidence, and risks

## Publish notes

- Keep `SKILL.md` concise and below 500 lines.
- Keep examples focused on Hong Kong listed securities only.
- Keep install docs in sync with `scripts/install-hk-stock-predictor-skill.sh`.

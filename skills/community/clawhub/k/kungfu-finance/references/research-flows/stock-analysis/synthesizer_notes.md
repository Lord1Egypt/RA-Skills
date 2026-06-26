# Stock Analysis Synthesizer Notes

Sources:

- `serverless-tianshan-api/src/handlers/analyse_research/prompt/skill_stock_prompts.py`
- `modules/step-9-output.md`

## Final Report Rules

- Conclusion first
- Short, direct, table-first structure
- No exact target price
- Use rating directly
- Include risk and thesis failure conditions
- Include comparable-valuation table
- Include catalyst calendar
- Include debate result integration if steps `7a/7b/8` were run

## Debate Integration

If the debate stage modifies or overturns the thesis:

- the report must include the correction
- the final rating must reflect the revised verdict

If the debate upholds the thesis:

- the report should state that the conclusion remained stable after committee-style debate

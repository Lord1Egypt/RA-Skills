# World Cup market discovery

Use this recipe when checking the live slate:

1. Query `q="World Cup"` first; generic terms like `fixture` may return nothing and broad terms like `vs` may return unrelated markets.
2. Filter questions with the pattern `World Cup: <team A> vs <team B> - <outcome>`.
3. Canonicalize team names with `scripts/team_names.py` before pricing or comparing against the model.
4. Price the outcome side with the matchup model, then inspect `get_market_context(..., my_probability=...)` for warnings and recommendations.
5. Keep the raw market label in the report, but use the canonical team names for lookup.

Useful examples from this session:
- `World Cup: Czechia vs South Africa - Czechia`
- `World Cup: Mexico vs Korea Republic - Korea Republic`
- `World Cup: Switzerland vs Bosnia and Herzegovina - Draw`

Avoid treating the first search hit as the final answer; score the matchup text and verify the outcome label.
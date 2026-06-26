# Gotchas — McKinsey Research

## Sub-agent Quality
- Sub-agents return shallow analysis when the prompt is too long and unfocused. Keep each prompt under 800 words with a clear single objective.
- Batch 2 agents don't actually benefit from Batch 1 results because each sub-agent is isolated. Pass key findings from Batch 1 as context summaries (not full reports) into Batch 2 prompts.
- Sub-agents that fail silently produce empty or template-like output. Always validate output length (minimum 500 words per analysis).

## Data Quality
- TAM numbers from web_search are often 2-3 years old. Always note the source date and adjust with CAGR.
- The Saudi/Gulf market has limited English-language data online. Use Arabic search queries alongside English ones. Key sources: GASTAT, CMA, SAMA, Monsha'at reports.
- Competitor data for MENA startups is sparse. Crunchbase and MAGNiTT are better sources than generic web search.
- Financial projections without real unit economics are fiction. If user doesn't provide cost structure, flag assumptions prominently rather than inventing numbers.

## Report Quality
- The final synthesis (Prompt 12) tends to repeat the same insights across 3-4 sections. Deduplicate aggressively and cross-reference sections instead.
- Executive summaries that exceed 3 paragraphs defeat their purpose. Enforce strict length limits.
- Arabic reports with mixed English brand names need consistent formatting. Keep brand names, technical terms, and metrics in English; narrative in Arabic.

## User Input
- Vague product descriptions lead to generic analysis across all 12 prompts. If description is under 50 words, ask for clarification before proceeding.
- Users at "idea stage" don't benefit from Financial Model or detailed Pricing analysis. Adapt scope to company stage.
- Users often skip optional fields. The analysis quality drops significantly without pricing and cost structure data. Nudge for these specifically.

## Execution
- Running all 12 analyses for every request wastes tokens. Adapt based on company stage (see SKILL.md Adaptive Stage Logic).
- Web search rate limits can hit when 4+ sub-agents search simultaneously. Stagger Batch 1 launches by 5 seconds.
- HTML report generation can fail if any section contains unescaped characters. Sanitize all sub-agent outputs before assembly.

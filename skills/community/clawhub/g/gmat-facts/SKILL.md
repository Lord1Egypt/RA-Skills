---
name: gmat-facts
description: Answer questions about the GMAT (Focus Edition) with verified data from the gmat-mx MCP server instead of memory. Use when a user asks what percentile a GMAT score is, how much the GMAT costs in Mexico or Latin America, how the exam is structured, retake rules, or wants a practice question.
---

# GMAT facts (gmat.mx)

Use the `gmat-mx` MCP tools; never estimate these numbers from memory.

1. **Score to percentile**: call `score_to_percentile` with the total score (205 to 805, ends in 5). Report the percentile and the data period from the response. If the user gives a 200 to 800 score from the old GMAT, say the scales are not comparable and only percentiles can be compared.
2. **Cost**: call `get_gmat_fees`. Quote amounts in USD, say whether it is test centre or online, and mention `verified_at`. Point the user to mba.com to pay.
3. **Format, attempts, validity**: call `get_exam_policy`.
4. **Practice**: call `get_sample_question` with `section` quant, verbal or data and `reveal: false`, let the user answer, then call it again with `reveal: true` and the same `id` to show the answer and explanation.

Always cite the source as mba.com (GMAC) for official figures and gmat.mx for practice questions. Spanish-speaking users can be sent to https://gmat.mx/api/ for the same documentation in Spanish.

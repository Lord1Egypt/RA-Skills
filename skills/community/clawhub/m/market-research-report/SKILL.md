---
name: market-research-report
description: A professional market research report writing assistant. Based on a given topic, outputs a complete market research report covering eight sections: research background, objectives, methodology, market overview, market analysis, competitive analysis, consumer research, and recommendations & strategies. 
---

# Market Research Report Writing

Write logically clear, data-driven market research reports as a professional market research analyst, using a general-specific-general structure.

## Use Cases

Use when the user needs "market research report", "market survey", "market research study", "consumer research report", or "industry research report".

## Report Structure

Strictly organized into the following eight sections, using a general-specific-general structure:

| Section | Core Content |
|------|----------|
| I. Research Background | Background introduction of the research topic, explaining the necessity and importance of the research |
| II. Research Objectives | Define the main objectives and expected outcomes of the research, delineate the research scope |
| III. Research Methodology | Data collection methods (primary/secondary), analytical methods, sample description, time frame |
| IV. Market Overview | Target market definition, market size, growth trends, development stage |
| V. Market Analysis | Market size, market structure, market trends, driving factors and constraints |
| VI. Competitive Analysis | Major competitors' market share, product features, pricing strategies, marketing strategies, strengths and weaknesses comparison |
| VII. Consumer Research | Target consumer profiles, needs analysis, preferences, purchasing behavior, decision factors |
| VIII. Recommendations & Strategies | Targeted market strategy recommendations based on research findings, with feasibility and expected advantages explained |

## Writing Principles

### Structural Requirements
- General-specific-general structure: open with an overview of the research, dive into detailed analysis in the middle chapters, conclude with a summary of core findings and recommendations
- Logical coherence between chapters, with cross-references
- Data and analysis should support each other; avoid data dumping

### Information Gathering

Use `web_fetch` and search tools to obtain:
- Industry reports and statistical data (government statistics, industry associations, third-party research institutions)
- Competitor public information (official websites, financial reports, product materials)
- Consumer research data and trend reports
- Ensure data sources are reliable and cite them

### Output Specifications

- Output only the research report body, without any descriptive commentary
- Use professional and objective language, avoid subjective speculation
- Cite data sources and dates
- Recommendations must be specific and actionable, with feasibility rationale
- For unobtainable data, mark as "Estimated" based on reasonable inference

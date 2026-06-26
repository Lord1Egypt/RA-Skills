---
name: llm-researcher
description: |
  LLM paper and project researcher. Analyze LLM-related papers and GitHub projects,
  then classify and organize them by specified categories. Use cases: (1) get the latest progress in the LLM field, (2) track the latest research in specific directions
compatibility: Requires network access, MINERU_API_KEY for PDF parsing, and Python (for scripts/pdf_to_md.py)
metadata:
   author: durunsheng
   version: "1.0.6"
   clawdbot:
      requires:
         env:
         - MINERU_API_KEY
---

## Pre-Execution Confirmation (Required)
1. Before starting any step in this skill, first ask the user whether Python is installed and `MINERU_API_KEY` is configured in the current environment. Explain the purpose: to run `scripts/pdf_to_md.py` to convert paper PDFs into Markdown (the terminal must be able to run `python` or `python3`). If Python is missing, help the user install it. If `MINERU_API_KEY` is missing, guide the user to https://mineru.net/apiManage/docs to obtain an API key.
2. Ask the user how many entries to retrieve from each data source.
3. Ask the user which parameter to use when calling the script to extract Markdown from PDF links:
   - `introduction`: only return Markdown content that strictly matches the first-level `# Introduction` heading
   - `all`: return the full Markdown content converted from the entire paper
4. Ask the user for the output report language.
Do not start this skill's core workflow until the above confirmations are complete.

## Default Data Sources
1. **alphaxiv** - 
   - `https://www.alphaxiv.org/?sort=Hot&interval=7+Days`
   - `https://www.alphaxiv.org/?source=GitHub&interval=7+Days&sort=Hot`
2. **GitHub Trending** - `https://github.com/trending?since=weekly`

- If the user does not specify a quantity, retrieve at most `10` entries from each data source by default.
- Use only the default data sources listed above. Do not add new data source URLs.

## Tool Usage Priority
When retrieving paper lists, project lists, paper links, and `arXiv ID`s from web pages, try the following in order:
1. **Browser tools first**: For dynamic web pages, first use browser tools to open, scroll, click, and observe page content. If a page cannot be opened, it is usually due to network issues; trying two more times often works.
2. **Web scraping tools second**: If browser tools cannot reliably retrieve the content, then try web scraping.
3. **Web-to-Markdown fallback**: As a last fallback, use `https://r.jina.ai/example.com` to read the page as Markdown.
4. **If none of the above methods work**: Skip the item and state the reason in the final report.


## Overall Workflow
### Phase 1: Discover Entries and Build the Task Queue
1. For paper pages, prioritize extracting the `arXiv ID` from the page content.
2. For GitHub projects, record the project title and repository URL. An `arXiv ID` is not required.
3. Deduplication rules:
   - Deduplicate papers primarily by `arXiv ID`
   - Deduplicate GitHub projects primarily by repository URL
   - If a unique identifier is missing, deduplicate by title
4. Organize the entries to be analyzed into a task queue for the current run.

### Phase 2: Execute Tasks One by One
- Maintain the task queue and process `pending` entries sequentially. Do not launch subagents.
- Before processing each entry, execute `attempt += 1`.
- After processing is complete, write the result to the success or failure collection:
  - Success: set `status = "done"` and write `completedAt`
  - Failure: set `status = "failed"` and write `error` and `completedAt`
- Failure of a single task must not affect subsequent tasks. Continue processing the remaining entries.

## Execution Rules
Directly complete content retrieval, analysis, classification, and result aggregation for each entry.


### Paper Tasks
If `source` is `arxiv`:
1. Prioritize using the existing `arXiv ID`.
2. If an `arXiv ID` is obtained, construct the paper PDF link:
   - `https://arxiv.org/pdf/{arxiv-id}.pdf`
3. Call the script to extract Markdown from the PDF link, explicitly passing the user's choice with `--range`:
   - `python scripts/pdf_to_md.py https://arxiv.org/pdf/{arxiv-id}.pdf tmp_llm_research/{arxiv-id}.md --range introduction`
   - `python scripts/pdf_to_md.py https://arxiv.org/pdf/{arxiv-id}.pdf tmp_llm_research/{arxiv-id}.md --range all`
4. `--range` parameter description:
   - `introduction`: only return Markdown content that strictly matches the first-level `# Introduction` heading
   - `all`: return the full Markdown content converted from the entire paper
5. Read `tmp_llm_research/{arxiv-id}.md`.
6. Analyze the paper's core problem, method, contributions, applicable scenarios, and limitations based on the extracted paper Markdown.
7. Classify strictly according to the top-level categories in `references/categories.md`.
8. If the `arXiv ID` cannot be obtained reliably, do not fabricate an ID and do not directly replace the Markdown with a web summary. Mark the task as `failed` and state in the error: "Unable to reliably obtain arXiv ID".

### GitHub Project Tasks
If `source` is `github`:
1. Prioritize using browser tools to read the repository home page, README, and project description.
2. If browser tools cannot retrieve enough content, then try web scraping tools.
3. If the result is still unstable, use the `r.jina.ai` version of the page as a fallback.
4. If all of the above methods are limited, but the repository home page still shows the repository name, description, topics, or a small amount of text from the page structure, a "brief analysis" based on that visible information is allowed.
5. Explain the paper/project content in simple, easy-to-understand language. When information is complete, be as detailed as possible. When information is limited, clearly state the inference boundaries.
6. Classify strictly according to the top-level categories in `references/categories.md`.

### Analysis Result Format

Maintain success and failure result collections in memory during the current run for final aggregation. Each result should include at least the following fields:

```json
{
  "id": "{sequence number}",
  "title": "{title}",
  "url": "{URL}",
  "source": "{arxiv|github}",
  "arxivId": "{arXiv ID, or null for GitHub}",
  "category": "{category name}",
  "authors": "{authors or organizations; use Unknown if unknown}",
  "analysis": "{explain the content in simple, easy-to-understand language; the more detailed, the better}",
  "status": "{done or failed; include the reason if failed}",
  "attempt": "{current attempt count}",
  "completedAt": "{ISO timestamp}"
}
```

## Final Report
After all tasks are complete, write the final Markdown report to the `output` folder. The file name format must be `YYYYMMDDHHmm.md`.
After the final report is successfully written, delete the entire `tmp_llm_research` folder.
The final report must include:

- `# Report Summary`, including at least: `Total`, `Success`, `Failed`, and `Retried Success`.
- `# Details`, aggregated by `category`. Entries under each category must include at least: `title`, `url`, `source`, `authors`, and `analysis`.
- `# Trending`, summarizing the common trends, hot directions, and potential changes reflected by this batch of papers and projects.


## Notes
- Failure of a single task does not affect other tasks. Continue processing the remaining tasks.
- All original links must be preserved so the final report can be traced back to the sources.
- Clean up `tmp_llm_research` only after the final Markdown report has been successfully written, to avoid affecting the final aggregation.
- If environment limitations mean that only limited information can be obtained for some entries, state this honestly in the final report. Do not pretend it is a complete in-depth analysis.

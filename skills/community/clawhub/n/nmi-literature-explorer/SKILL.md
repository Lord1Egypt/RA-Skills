---
name: nmi-literature-explorer
description: Find, verify, and analyze papers published in Nature Machine Intelligence (NMI) using official Nature and Springer Nature sources. Use for NMI paper searches by year, topic, author, or method; paper summaries; comparisons; topic trends; and citation or related-work exploration. By default, use items labeled Article in the NMI archive.
---

# NMI Literature Explorer

Help researchers discover and understand NMI publications from evidence they can verify. Respond in the user's language. Answer the question they asked; do not reduce every request to a trend chart or a fixed report.

## Scope and source rules

- Treat the NMI article archive and the individual Nature article page as the canonical source for whether an item appeared in NMI, its displayed content type, publication dates, DOI, authors, abstract, and available full text.
- Use the Springer Nature Meta API as an optional discovery and metadata aid. Its coverage and query behavior may differ from the NMI archive. Verify candidate records against the Nature page before presenting them as NMI papers.
- Use official publisher pages and APIs as evidence. Do not present search snippets, third-party indexes, or model memory as verification. If a third-party source helps discover a candidate, confirm it on the official article page before including it.
- Link factual claims to the relevant official article page, and include the DOI when available. State the date searched when the answer depends on a changing archive.
- Do not infer editorial decisions, peer-review outcomes, or acceptance probabilities from published papers or journal metrics. Publicly available review-time metrics are not acceptance rates.
- Respect publisher access terms and article licenses. Do not bypass paywalls, automate broad site scraping, or reproduce substantial copyrighted text. A bibliographic record or abstract is not a substitute for full-text access.

## Default corpus

Use items labeled Article in the NMI archive unless the user asks for another content type or a broader corpus. The archive and NMI content-type guidance distinguish research Articles from Reviews, Perspectives, Analysis, News & Views, and other formats. Preserve the publisher's displayed type; do not silently merge them.

If an item is described by NMI as a Reusability Report or another special format, identify that distinction in the answer even if the archive groups it under Article. If the user asks for all NMI content, include the requested types and report the type alongside every item.

Interpret year as the Nature archive's year filter unless the user specifies another convention. When the difference matters, distinguish online publication date from issue or print date. For an in-progress year, report the search date and describe the set as publications found so far.

## Workflow

1. **Resolve the question.** Identify the topic or named entity, time range, desired content types, and whether the user wants a list, paper-level explanations, comparisons, trends, or related work. Make a reasonable default from context; ask only when an ambiguity would materially change the search.
2. **Search the NMI archive.** Use the official archive's year, Article Type, and search controls. For broad topics, search several likely synonyms and method or application terms. Do not rely on one exact phrase when relevant papers may use different wording.
3. **Verify candidates.** Open each candidate's official Nature page. Confirm journal, title, DOI, authors, publication date, and content type. Remove false matches and disclose when the archive or API search may be incomplete.
4. **Read the available evidence.** Prefer the full article and its methods, results, figures, and supplementary information when they are openly accessible. If only the abstract or metadata is available, label the summary as abstract-based and do not invent methods, experiments, results, or application details.
5. **Explain each paper.** Separate the research problem, contribution, method or system, evaluation evidence, and application setting. Distinguish a demonstrated use in the paper from a proposed or potential application. Report limitations only when the paper supports them.
6. **Connect papers when asked.** Label the basis of each connection: an explicit citation/reference, a shared method, a shared task or application, or topical similarity inferred from the papers. Do not imply that topical similarity proves citation, influence, or a direct research lineage.
7. **Synthesize trends carefully.** Define the search terms, years, archive types, and date searched. Count only a corpus whose search and screening rules are stated. Treat topic labels as the analyst's coding unless NMI explicitly supplies them. Avoid claims about acceptance likelihood or future success.
8. **Present traceable results.** Use a compact table for multiple papers, followed by interpretation when useful. Link each paper to its official page. Place citations close to the claims they support, and distinguish publisher facts from your own synthesis.

## Optional metadata helper

The Python 3.10+ script at scripts/springer_nature_search.py makes one request to the Springer Nature Meta API and prints metadata only. Use it only when an API key is configured in the process environment as SN_API_KEY. Never ask the user to paste a secret into chat, put a key in a file, print it, or include a key-bearing request URL in the answer.

The script searches a quoted phrase and/or year within the publication constraint Nature Machine Intelligence. It returns one bounded page of results; it does not crawl, paginate, download full text, save a corpus, or replace archive verification. The user's query is sent to Springer Nature. If the script is unavailable, the key is absent, or the API does not return useful results, continue with the official NMI archive.

## Answer quality

- For a paper list, include title, authors, publication date, content type, short contribution, and official link.
- For a question about applications, identify the concrete domain, users or system, task, and evaluation setting when the article establishes them. Mark speculative implications as interpretation.
- For comparisons, use the same dimensions across papers and cite the evidence for each comparison.
- For topic trends, report counts only with the corpus definition and acknowledge that keyword search can miss papers and matching terms can produce false positives.
- If evidence is unavailable or conflicting, say what could not be verified and what source or access would resolve it.


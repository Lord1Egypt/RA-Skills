## Description: <br>
Verify academic paper citations using a three-tier fallback pipeline across a local FTS5 database, Semantic Scholar, and OpenAlex, with support for single checks and batch reference-list audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diamond2nv](https://clawhub.ai/user/diamond2nv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, reviewers, and literature-survey authors use this skill to check whether cited papers exist, including citations from LLM-generated papers or batch reference lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Citation titles, arXiv IDs, or batch reference contents may be sent to Semantic Scholar or OpenAlex when remote lookup modes are used. <br>
Mitigation: Use local source mode for confidential or unpublished reference lists, and use remote API lookup only when sharing those citation details is acceptable. <br>
Risk: Optional Semantic Scholar and OpenAlex credentials or contact details may be used for higher rate limits. <br>
Mitigation: Store S2_API_KEY and OPENALEX_POLITE_EMAIL in environment variables, and avoid placing credentials in prompts, shared files, or audit inputs. <br>
Risk: Short titles, missing local databases, rate limits, or network errors can produce SUSPECTED, NOT_FOUND, or ERROR results. <br>
Mitigation: Prefer full titles or arXiv IDs, review per-source status details, and retry or cross-check failed remote lookups before relying on the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diamond2nv/hfpclawer-citation-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python snippets, and citation audit status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audit statuses include VERIFIED, SUSPECTED, NOT_FOUND, and ERROR; remote lookups may query Semantic Scholar or OpenAlex unless local-only mode is used.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

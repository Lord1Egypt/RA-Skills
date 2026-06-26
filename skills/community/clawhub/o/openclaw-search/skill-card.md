## Description: <br>
Run web, multi-source, or last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, and structured retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run AIsa-backed web, academic, smart, full-text, and multi-source search workflows, then turn results into research briefs, comparisons, or structured evidence summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, target URLs, and related research context are sent to the AIsa API. <br>
Mitigation: Use only when that sharing is acceptable; avoid secrets, confidential internal documents, and proprietary topics unless approved. <br>
Risk: The skill requires a sensitive AISA_API_KEY credential. <br>
Mitigation: Store the key in the environment, limit access to trusted users, and avoid exposing it in prompts, logs, or committed files. <br>


## Reference(s): <br>
- [Openclaw Search on ClawHub](https://clawhub.ai/baofeng-tech/openclaw-search) <br>
- [AIsa API endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and Python 3; search queries and URLs are sent to AIsa.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
High-accuracy web search and research via Parallel.ai API. Optimized for AI agents with rich excerpts and citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pntrivedy](https://clawhub.ai/user/pntrivedy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and research agents use this skill to run web research, fact-checking, company and person research, and multi-hop search through Parallel.ai with cited results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A default Parallel.ai API key fallback is bundled in the artifact and could route searches through an unknown account. <br>
Mitigation: Set PARALLEL_API_KEY to an account-controlled key before use, remove or override bundled fallback keys, and avoid relying on the included default key. <br>
Risk: Search queries and task inputs are sent to Parallel.ai services. <br>
Mitigation: Do not submit secrets, regulated data, or proprietary queries unless that external processing is approved for the use case. <br>
Risk: The setup instructions install the Parallel Python SDK from the package ecosystem. <br>
Mitigation: Pin and verify the Python dependency before installation in controlled environments. <br>


## Reference(s): <br>
- [Parallel.ai documentation](https://docs.parallel.ai) <br>
- [Parallel.ai platform](https://platform.parallel.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted search results or JSON search result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include URLs, titles, excerpts, publish dates, search IDs, and API usage statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

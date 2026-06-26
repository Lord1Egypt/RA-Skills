## Description: <br>
Given an arXiv ID or URL, Paper Digest fetches the paper, reads up to five key cited papers through sub-agents, and writes a prose executive digest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[damoonsh](https://clawhub.ai/user/damoonsh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and researchers use Paper Digest to turn an arXiv paper into a concise Markdown executive summary with context from important cited papers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public arXiv pages and may reuse cached paper summaries that are stale or incomplete. <br>
Mitigation: Review or clear saved summaries in ~/.openclaw/workspace/papers/ when freshness or accuracy matters. <br>
Risk: Citation resolution, paper extraction, or sub-agent summarization can miss context or produce an inaccurate digest. <br>
Mitigation: Verify important claims, metrics, and citations against the source papers before relying on the generated report. <br>


## Reference(s): <br>
- [Paper Digest on ClawHub](https://clawhub.ai/damoonsh/paper-digest) <br>
- [arXiv example paper URL](https://arxiv.org/abs/2305.11206) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown prose document saved to the OpenClaw workspace, with cached Markdown paper summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Citation summaries are cached under ~/.openclaw/workspace/papers/; missing citation URLs fall back to plain-text citations after one retry.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata; artifact frontmatter lists 0.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

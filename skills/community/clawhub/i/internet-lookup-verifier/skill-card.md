## Description: <br>
Verify information by performing an internet lookup before answering questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AmanGarg1999](https://clawhub.ai/user/AmanGarg1999) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to verify factual answers with current internet sources before responding. It is intended for concise source-backed answers and uncertainty reporting when sources conflict or cannot be found. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries or fetched pages may expose secrets, private personal details, proprietary business information, or regulated data if users include them in factual questions. <br>
Mitigation: Use the skill only for public or shareable factual questions and redact sensitive details before lookup. <br>
Risk: Search results can be incomplete, stale, low quality, or conflicting, so a source-backed response can still be uncertain. <br>
Mitigation: Require explicit source support for claims and report uncertainty when sources disagree or no source supports the answer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AmanGarg1999/internet-lookup-verifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise Markdown answer with supporting source URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include snippets or an uncertainty note when sources conflict or no supporting source is found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Reverse-engineers job descriptions across jargon translation, company culture inference, resume matching, and negotiation signals, producing Markdown and shareable HTML reports through a configured OpenAI-compatible LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to analyze job descriptions, compare optional resume content, and identify jargon, culture signals, resume fit, and negotiation cues before applying or interviewing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive job descriptions or resume content may be sent to the configured LLM endpoint. <br>
Mitigation: Use a trusted or local endpoint for sensitive material and avoid submitting resume details unless the endpoint is approved. <br>
Risk: URL input contacts the target job site and depends on page scraping. <br>
Mitigation: Use text paste or file input when external site contact, scraping reliability, or privacy is a concern. <br>
Risk: Dependency ranges are not pinned with a lockfile. <br>
Mitigation: Pin and review dependencies before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ucsdzehualiu/skills/jd-truth-detector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, HTML, Guidance] <br>
**Output Format:** [Markdown and HTML report files with CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated from user-provided job-description input and optional resume content using the configured LLM endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
NexSolve AI connects industry pain points with AI developers through bilingual task submission, open-need listing, detail retrieval, and agent-assisted feasibility analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxz0119](https://clawhub.ai/user/zxz0119) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI builders use this skill to submit bilingual industry pain-point reports to the NexSolve AI need marketplace, browse open needs, and retrieve issue details for feasibility analysis and contact-awareness guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided reports and optional contact details may be published to a GitHub issue. <br>
Mitigation: Warn users before submission, avoid secrets or private business details, and confirm the destination repository and visibility before creating an issue. <br>
Risk: The security evidence notes no separate confirmation step before publication. <br>
Mitigation: Require explicit user confirmation before invoking the submission workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zxz0119/nexsolve-ai) <br>
- [NexSolve AI repository referenced by artifact](https://github.com/zxz0119/NexSolve-AI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-oriented text returned to the agent, including created-issue confirmations, issue lists, and issue detail summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GitHub token configured for the target repository's issue workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence; artifact package files declare 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

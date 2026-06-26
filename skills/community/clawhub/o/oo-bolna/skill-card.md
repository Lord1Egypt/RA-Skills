## Description: <br>
Bolna (bolna.ai). Use this skill for ANY Bolna request: searching and reading data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to inspect Bolna voice agents, execution history, raw execution logs, and workspace user or wallet summaries through OOMOL's oo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Bolna agents, execution history, raw execution logs, and workspace/user wallet summaries, which may contain sensitive information. <br>
Mitigation: Install and use it only with an intended OOMOL-connected Bolna account, and treat returned data as sensitive. <br>
Risk: Future write or destructive connector actions could alter or remove Bolna data. <br>
Mitigation: Review action tags, payloads, and expected effects, and obtain explicit user approval before running write or destructive actions. <br>


## Reference(s): <br>
- [Bolna homepage](https://www.bolna.ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub Bolna skill](https://clawhub.ai/oomol/oo-bolna) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OOMOL-connected Bolna account and may expose sensitive workspace, execution, log, wallet, or user data.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

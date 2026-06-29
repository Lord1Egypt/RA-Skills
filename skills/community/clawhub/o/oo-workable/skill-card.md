## Description: <br>
Provides read-only Workable candidate and job search and retrieval through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiting and people operations users can ask an agent to list Workable jobs and candidates or retrieve candidate and job details from a connected Workable account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve Workable candidate and job information through an OOMOL-connected account. <br>
Mitigation: Connect only trusted OOMOL and Workable accounts, keep use to read requests, and review retrieved recruiting data before sharing it. <br>
Risk: Workable connector contracts can change over time. <br>
Mitigation: Inspect the live action schema before constructing payloads, as the artifact instructs. <br>


## Reference(s): <br>
- [ClawHub Workable Skill Page](https://clawhub.ai/oomol/oo-workable) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [Workable Homepage](https://www.workable.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with oo CLI bash commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live Workable connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

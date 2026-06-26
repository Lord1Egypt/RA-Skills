## Description: <br>
Analyzes a target company's technology stack and AI compute needs to produce a customer technical profile for AI compute sales. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales engineers, account teams, and AI infrastructure specialists use this skill to research a company from a name or domain and summarize its technology stack, GPU demand level, inference/training mix, signal sources, and sales entry points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound web requests for the company or domain provided by the user. <br>
Mitigation: Use only public company names or domains where that external lookup is acceptable, and avoid internal hostnames, private IPs, or confidential prospect lists. <br>
Risk: Generated profiles and optional output files may contain business research data. <br>
Mitigation: Store output files with appropriate access controls and clean them up when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dashiming/pans-tech-profile) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Plain text, JSON, or Markdown company technical profile; optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a company name or domain, optional deep analysis, and an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

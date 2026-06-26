## Description: <br>
Run Mission Control visual QA over SSH using Puppeteer screenshots and basic DOM checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Highlander89](https://clawhub.ai/user/Highlander89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to run authorized visual checks against Mission Control pages from a configured remote host. It captures screenshots and reports basic page structure checks for each supplied URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs code on a configured SSH host. <br>
Mitigation: Use only a trusted remote host and review the SSH target and URLs before running visual checks. <br>
Risk: Screenshots may capture internal, authenticated, or personal data. <br>
Mitigation: Treat saved screenshots as sensitive output and avoid URLs that include secrets in query strings. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; runtime output includes PNG screenshots and a JSON summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted SSH target with Node.js, Chromium, and Puppeteer available.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

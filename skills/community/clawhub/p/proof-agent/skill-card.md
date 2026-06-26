## Description: <br>
Adversarial verification of AI-generated work. Spawns an independent verifier to check for false claims, broken code, and security issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreagriffiths11](https://clawhub.ai/user/andreagriffiths11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to route AI-generated work through an independent adversarial verification workflow before accepting changes, especially when multiple files or sensitive areas are involved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fact-check helper can send URLs, package names, GitHub action references, or similar identifiers from checked files to external services. <br>
Mitigation: Review files for private URLs, internal package names, unreleased repository references, and secrets before running fact-checking. <br>
Risk: The workflow relies on a separate verifier; self-verification weakens the intended review boundary. <br>
Mitigation: Use an independent verifier agent or reviewer and provide only the original request, changed files, and approach summary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andreagriffiths11/proof-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown verification prompts and verdicts with shell command helpers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PASS, FAIL, or PARTIAL verdicts with command evidence; helper scripts can emit terminal reports.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

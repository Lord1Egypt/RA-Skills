## Description: <br>
fal.ai lets an agent operate fal.ai through an OOMOL-connected account by using the oo CLI connector for model discovery, pricing, queue status, results, and request cancellation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect fal.ai model endpoints, estimate pricing, manage queued fal requests, retrieve completed results, and fetch JWKS data for webhook verification through their connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate fal.ai through the user's OOMOL-connected account and includes a write action for request cancellation. <br>
Mitigation: Install it only when that account access is intended, and confirm the exact payload and effect before running write actions. <br>
Risk: The setup instructions include shell-based oo CLI installation commands. <br>
Mitigation: Prefer a verified installation method for the oo CLI before running connector commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-fal-ai) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>
- [fal.ai homepage](https://fal.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or summarize JSON responses returned by the oo CLI connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

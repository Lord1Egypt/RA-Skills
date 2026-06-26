## Description: <br>
Normalizes short Japanese smart-home STT transcripts into structured intents and slots, with confidence scoring and confirmation handling before downstream device execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t0yohei](https://clawhub.ai/user/t0yohei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to normalize Japanese smart-home voice transcripts after STT before routing them to device-control logic. It is most relevant for light and air-conditioner commands, while downstream integrations should explicitly allow any additional prepared domains before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downstream hooks could auto-execute returned curtain or TV intents even though the public scope emphasizes lights and air conditioners. <br>
Mitigation: Keep a strict allowlist of executable device domains and only enable curtain or TV control after explicit review and tests. <br>
Risk: Ambiguous or incomplete voice transcripts can be misclassified into actionable smart-home commands. <br>
Mitigation: Honor the returned needsConfirmation flag and ask for confirmation whenever confidence is low or required slots are missing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/t0yohei/japanese-smart-home-command-normalizer) <br>
- [Design](references/design.md) <br>
- [Domains](references/domains.md) <br>
- [OpenClaw integration notes](references/openclaw-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance plus JavaScript and JSON result shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces normalized intent, confidence, confirmation flag, slots, and candidate matches; it does not call device APIs directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

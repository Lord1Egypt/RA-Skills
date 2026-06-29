## Description: <br>
Turn scattered local sources into a source-constrained evidence notebook for incident, release, and maintainer decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiepu110](https://clawhub.ai/user/jiepu110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and incident responders use this skill to turn approved local sources into a decision packet that separates facts, conflicts, assumptions, and conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive data could be included in source material and then summarized into the notebook. <br>
Mitigation: Use only approved sources and redact secrets, credentials, and irrelevant personal data before using the skill. <br>
Risk: The agent could present unsupported conclusions as facts. <br>
Mitigation: Keep answers source-constrained, cite source anchors, and label unsupported claims as inferences or questions. <br>
Risk: Broad web research or external indexing could expand the evidence set beyond what was approved. <br>
Mitigation: Avoid broad web research unless explicitly requested and do not upload or index evidence externally by default. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiepu110/oc-evidence-notebook) <br>
- [GitHub repository mentioned by skill](https://github.com/Star-Ring-Protocol/openclaw-gateway-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown decision packet with source lists, evidence cards, conflict lists, and source-constrained answers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should keep claims tied to approved sources and label unsupported claims as inferences or questions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

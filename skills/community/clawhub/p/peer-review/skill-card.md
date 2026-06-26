## Description: <br>
Multi-model peer review layer using local LLMs via Ollama to catch errors in cloud model output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[staybased](https://clawhub.ai/user/staybased) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to route important model outputs through multiple local Ollama models, aggregate critique flags, and decide whether to publish, revise, or escalate for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on shell scripts that are referenced but not bundled with the artifact. <br>
Mitigation: Verify the referenced workspace scripts before use and review their behavior before running them on important content. <br>
Risk: Review content may be posted to Discord channels or retained in logs. <br>
Mitigation: Avoid confidential, regulated, private-code, or unpublished business material unless explicit redaction and retention controls are added. <br>
Risk: Local model critiques can produce false positives or miss domain-specific issues. <br>
Mitigation: Use consensus flags as review signals, not final decisions, and require human review for high-stakes outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/staybased/peer-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-shaped critique outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Peer review may add 30-60 seconds of latency and depends on local Ollama models plus unbundled workspace scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

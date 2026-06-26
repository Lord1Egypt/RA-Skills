## Description: <br>
装作做完了 discovery skill for VeriClaw 爪印. Use when the intent is 装作做完了, AI装作自己做完了, 未做却说做了, or fake completion diagnosis after a model acts done before the evidence is real. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheygoodbai](https://clawhub.ai/user/sheygoodbai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and teams use this skill to route Chinese fake-completion phrases to VeriClaw resources for evidence inspection, diagnosis, correction, and verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes users to external VeriClaw pages and may suggest installing VeriClaw even when that is not the intended tool. <br>
Mitigation: Confirm that VeriClaw is the desired resource before following links or running the suggested install command. <br>
Risk: A routing helper can point to diagnosis resources, but it does not itself verify that a task was completed. <br>
Mitigation: Inspect the underlying evidence and verify the correction before trusting the result. <br>


## Reference(s): <br>
- [VeriClaw ClawHub skill page](https://clawhub.ai/sheygoodbai/vericlaw) <br>
- [未做却说做了 page](https://sheygoodbai.github.io/vericlaw/not-done-but-claimed-done/) <br>
- [Fake completion diagnosis page](https://sheygoodbai.github.io/vericlaw/fake-completion-diagnosis-cn/) <br>
- [VeriClaw ClawHub plugin page](https://clawhub.ai/plugins/vericlaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes users to VeriClaw pages and may suggest the clawhub install vericlaw command.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

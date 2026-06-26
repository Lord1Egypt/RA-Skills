## Description: <br>
Routes Chinese fake-completion discovery intents such as 未做却说做了 to VeriClaw evidence, diagnosis, intervention, and verification resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheygoodbai](https://clawhub.ai/user/sheygoodbai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill when a user describes fake completion in Chinese, including cases where an AI claims work is done without evidence. The skill routes that intent to VeriClaw pages for evidence inspection, diagnosis, intervention, and verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill links to separate VeriClaw skill and plugin resources outside this small routing artifact. <br>
Mitigation: Review the linked VeriClaw skill and plugin before installing or relying on them. <br>
Risk: Routing guidance could become stale if linked VeriClaw pages move or change. <br>
Mitigation: Verify the referenced pages during release review and update the skill when routes change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sheygoodbai/not-done-but-claimed-done) <br>
- [VeriClaw ClawHub skill](https://clawhub.ai/sheygoodbai/vericlaw) <br>
- [VeriClaw plugin page](https://clawhub.ai/plugins/vericlaw) <br>
- [未做却说做了 page](https://sheygoodbai.github.io/vericlaw/not-done-but-claimed-done/) <br>
- [Fake completion diagnosis page](https://sheygoodbai.github.io/vericlaw/fake-completion-diagnosis/) <br>
- [VeriClaw review kit](https://sheygoodbai.github.io/vericlaw/review-kit/) <br>
- [Search intents](references/search-intents.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with links and occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes user intent to VeriClaw resources; does not run code or request credentials.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

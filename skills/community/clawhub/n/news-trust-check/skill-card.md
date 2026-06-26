## Description: <br>
Verify suspicious news, announcements, screenshots, and viral claims using a high-trust source pool (official channels + Chinese mainstream media + international mainstream media + fact-check sites). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helloeveryworlds](https://clawhub.ai/user/helloeveryworlds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and support teams use this skill to assess whether suspicious news, viral screenshots, announcements, or circulating messages are credible and what action to take. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fact-checking output could be mistaken for a guarantee on sensitive financial, legal, medical, security, or urgent money-transfer claims. <br>
Mitigation: Use the skill as a fact-checking aid and verify sensitive claims directly with official sources before acting. <br>
Risk: The helper script may miss context because it scores only keyword indicators. <br>
Mitigation: Treat helper output as an initial risk screen and base the final verdict on cross-checked official, mainstream media, and fact-check sources. <br>


## Reference(s): <br>
- [High-Trust Source Pool (CN + Global)](references/high-trust-sources.md) <br>
- [ClawHub release page](https://clawhub.ai/helloeveryworlds/news-trust-check) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, JSON] <br>
**Output Format:** [Markdown structured verdict with optional JSON risk score from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Python helper is a quick keyword risk screen only; final trust judgments should rely on verified sources.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Neta API space and world-view browsing skill for exploring worldbuilding, sub-spaces, playable content, characters, and activity structure by space or hashtag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huxiuhan](https://clawhub.ai/user/huxiuhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to browse Neta spaces, lore, sub-spaces, collections, characters, and gameplay content before answering informational or gameplay-structure questions. It is not intended for concrete media creation, which the source skill delegates to neta-creative. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a globally installed third-party Neta CLI package. <br>
Mitigation: Install only if the @talesofai/neta-skills package is trusted; pin or verify the package version before global installation. <br>
Risk: The skill requires a NETA_TOKEN credential for API access. <br>
Mitigation: Provide NETA_TOKEN through a secure environment or secret manager, and avoid pasting, printing, or logging the token. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huxiuhan/neta-space) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NETA_TOKEN and Neta CLI access for live Neta API browsing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Analyzes a Go/Weiqi position from an image or board state and uses KataGo to recommend a next move at beginner, intermediate, or advanced playing strength. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imcaptor](https://clawhub.ai/user/imcaptor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and Go players use this skill to analyze board photos or text board states, choose the side to move and desired playing strength, and receive a KataGo-backed next-move recommendation with supporting candidate data and visual overlays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional HTTP mode can expose a long-running tunnelled service protected by bearer links. <br>
Mitigation: Prefer the local CLI workflow; if HTTP mode is needed, keep it on localhost or use --no-tunnel unless remote access is required. <br>
Risk: Minted access links can grant analysis access until they expire. <br>
Mitigation: Protect minted links like passwords, rotate the secret to revoke outstanding links, and stop the resident service when finished. <br>
Risk: Board-photo recognition errors can make the recommended move unreliable. <br>
Mitigation: Review the generated recognition overlay and source-result image before relying on the recommendation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imcaptor/go-next-move) <br>
- [English README](README.en.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON analysis results, and optional generated image files for recognition overlays and move recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local KataGo for analysis; optional HTTP mode can mint bearer-token links for faster image-upload workflows.] <br>

## Skill Version(s): <br>
0.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

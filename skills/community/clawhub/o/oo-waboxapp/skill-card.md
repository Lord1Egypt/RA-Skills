## Description: <br>
waboxapp (waboxapp.com). Use this skill for ANY waboxapp request: reading, creating, and updating data through the OOMOL waboxapp connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect the live waboxapp connector schema, check the connected WhatsApp account status, and send WhatsApp chats, images, links, or media through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected waboxapp account. <br>
Mitigation: Install and run it only in a trusted ClawHub maintainer environment, and rely on OOMOL server-side credential injection instead of exposing raw tokens. <br>
Risk: Write actions can send WhatsApp chats, images, links, and media through the connected account. <br>
Mitigation: Confirm the exact action payload and expected effect with the user before running any action tagged as write. <br>
Risk: Server security evidence marks the release as suspicious and says review is warranted because an autoreview helper grants nested Codex full local authority by default. <br>
Mitigation: Review the autoreview helper before use, consider disabling YOLO behavior, and be cautious with fallback reviewer CLIs because generated diffs may be sent to those tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-waboxapp) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [waboxapp homepage](https://www.waboxapp.com) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Action execution returns JSON from the oo connector, including data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: artifact frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

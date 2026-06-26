## Description: <br>
ima (ima.qq.com). Use this skill for ANY ima request: reading, creating, and updating data through the OOMOL-connected ima connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate Tencent ima through an OOMOL-connected account. It supports reading and searching knowledge bases, folders, items, media, notebooks, and notes, and can create, append, import, upload, or add content when the user confirms write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can change data in the connected ima account, including creating notes, appending content, importing URLs, uploading files, or adding notes to knowledge bases. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running actions tagged as write, and inspect the live connector schema before constructing payloads. <br>
Risk: The skill depends on an authenticated OOMOL-connected ima account and may prompt setup, account connection, or billing steps when access is unavailable. <br>
Mitigation: Use existing authentication when available, run setup only after relevant command failures, and review requested permissions or account connection steps before proceeding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-ima) <br>
- [ima homepage](https://ima.qq.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON responses from the oo CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

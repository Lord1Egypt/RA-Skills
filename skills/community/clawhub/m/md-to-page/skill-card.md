## Description: <br>
Convert Markdown files into styled, scrollable wide-screen HTML pages with dark/light themes, animations, and rich directive components for web articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LZ-Web3](https://clawhub.ai/user/LZ-Web3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and content maintainers use this skill to turn Markdown notes, outlines, and long-form articles into shareable HTML pages with theme switching, styled tables, image handling, and directive components. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review flagged a helper that can run nested review with sandbox and approval bypass enabled by default. <br>
Mitigation: Install only in a trusted maintainer environment and run review workflows without bypass mode, such as --no-yolo or AUTOREVIEW_YOLO=0. <br>
Risk: Private diffs or sensitive content could be exposed if fallback external reviewers are enabled. <br>
Mitigation: Disable fallback external reviewers for private work and require an explicit target, reason, confirmation, and verification step for moderation or migration commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LZ-Web3/md-to-page) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Guidance] <br>
**Output Format:** [HTML file with Markdown and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a standalone HTML page; optional image embedding can read local images and encode them into the output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Convert Markdown files into high-contrast, mobile-friendly PNG images optimized for Telegram and social media sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nowhere1975](https://clawhub.ai/user/nowhere1975) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content authors use this skill to convert Markdown documents into readable mobile PNG images for Telegram and social media sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown is rendered as active browser HTML without network blocking or clear warnings for untrusted files. <br>
Mitigation: Use only trusted Markdown, or change the skill to disable raw HTML/scripts and block browser network requests before processing untrusted content. <br>
Risk: Playwright is required for rendering but is not pinned in package.json. <br>
Mitigation: Confirm the Playwright installation and version in the target environment before relying on repeatable rendering. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nowhere1975/md-to-image) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image file plus command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates 1080px-wide PNG files in /tmp/md-to-img with height based on the rendered Markdown content.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

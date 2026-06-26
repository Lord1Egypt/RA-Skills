## Description: <br>
Converts Markdown files or Markdown text in the current workspace into polished PNG images with selectable themes and output sizes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiulanzhu](https://clawhub.ai/user/qiulanzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content authors use this skill to turn Markdown documentation, snippets, or notes into shareable PNG screenshots without leaving the current workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes md2png-cli@1.0.2 from npm, so users depend on the trustworthiness of that local CLI package. <br>
Mitigation: Verify and install md2png-cli@1.0.2 intentionally before use; the skill checks local availability with npx --no-install and does not auto-download it during execution. <br>
Risk: The skill creates PNG output and may create a temporary Markdown file when converting direct text input. <br>
Mitigation: Run it only in the workspace that contains the Markdown to convert, use simple relative filenames, and confirm temporary Markdown files are removed after conversion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiulanzhu/md2png) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports note, vitality, gradient, antiquity, classic, dark, minimal, sakura, ocean, and tech themes; supports mobile, tablet, laptop, and desktop sizes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

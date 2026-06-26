## Description: <br>
Generate high-density editorial HTML info cards in a modern magazine and Swiss-international style, then capture them as ratio-specific screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaom](https://clawhub.ai/user/shaom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, content creators, and developers use this skill to turn supplied text or core information into structured editorial HTML cards and optional ratio-specific screenshot commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendered cards may contact Google Fonts during screenshot rendering. <br>
Mitigation: Use bundled or system fonts, or remove the font import, before rendering confidential, unpublished, or offline-only content. <br>
Risk: PNG capture depends on a local Chrome or Chromium binary. <br>
Mitigation: Install a supported browser binary or set CHROME_BIN before running the screenshot helper. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shaom/infocard-skills) <br>
- [Editorial Card Prompt](references/editorial-card-prompt.md) <br>
- [Supported Ratios](references/ratios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown response containing a density sentence, a complete HTML code block, optional screenshot command, and a readability self-check.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports fixed visual ratios including 3:4, 4:3, 1:1, 16:9, 9:16, 2.35:1, 3:1, and 5:2; PNG capture requires Chrome or Chromium.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

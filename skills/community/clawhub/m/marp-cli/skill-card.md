## Description: <br>
Convert Markdown to presentations via CLI, including HTML, PDF, PowerPoint (PPTX), PNG, and JPEG outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killgfat](https://clawhub.ai/user/killgfat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, educators, and technical writers use this skill to generate Marp CLI commands and workflow guidance for converting Markdown slide decks into presentation, document, and image formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill suggests running the `marp` command from the user's PATH. <br>
Mitigation: Install and use this skill only when the local `marp` binary is trusted. <br>
Risk: Server mode can expose slide directories over HTTP if bound to a shared or untrusted network interface. <br>
Mitigation: Use server mode only for directories intended to be shared and avoid `HOST=0.0.0.0` on shared or untrusted networks. <br>
Risk: Local file access and raw HTML can increase exposure when processing untrusted slide decks. <br>
Mitigation: Enable local file access or raw HTML only for trusted slide decks. <br>


## Reference(s): <br>
- [Marp CLI homepage](https://github.com/marp-team/marp-cli) <br>
- [ClawHub skill page](https://clawhub.ai/killgfat/marp-cli) <br>
- [QUICKSTART.md](QUICKSTART.md) <br>
- [EXAMPLES.md](EXAMPLES.md) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Assumes a trusted `marp` binary is available on PATH; browser-backed conversions may require Chrome, Edge, or Firefox.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

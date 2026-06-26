## Description: <br>
Use when creating slide decks, presentations, product requirement docs with diagrams, or converting markdown to PDF/PPTX/HTML slides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patoo0x](https://clawhub.ai/user/patoo0x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and product teams use this skill to create Marp slide decks, convert Markdown presentations to PDF/PPTX/HTML/images, and structure presentation-ready product documentation with diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local file access, HTML rendering, CDN scripts, and globally installed diagram tools can expose or execute content outside the slide source when used with untrusted decks. <br>
Mitigation: Enable those options only for trusted decks and trusted assets, and review generated commands before running them. <br>
Risk: Serving a slide directory locally can expose files from directories the user did not intend to share. <br>
Mitigation: Serve only the specific directory needed for preview and keep unrelated files outside that directory. <br>


## Reference(s): <br>
- [Marp Documentation](https://marp.app) <br>
- [Marpit Framework](https://marpit.marp.app) <br>
- [Marp CLI](https://github.com/marp-team/marp-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, configuration examples, and slide templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local files, optional HTML rendering, CDN scripts, or external diagram tools when the user chooses those Marp workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

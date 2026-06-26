## Description: <br>
Create, edit, preview, and export web-native slide decks with the open-slide React framework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windrichie](https://clawhub.ai/user/windrichie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to scaffold, author, iterate on, preview, and export React-based slide decks with the open-slide framework. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to install npm or pnpm packages, pip dependencies, Playwright, and Chromium. <br>
Mitigation: Use a controlled environment, review dependency installation commands before execution, and prefer pinned dependency versions where possible. <br>
Risk: Generated PDFs, static builds, or ZIP archives may contain content that should not be shared publicly. <br>
Mitigation: Review generated artifacts before sharing or deployment. <br>
Risk: The optional CDP export path can connect to an already-running browser session. <br>
Mitigation: Use the CDP option only when deliberately exporting through a trusted browser session. <br>


## Reference(s): <br>
- [Open Slide release page](https://clawhub.ai/windrichie/open-slide) <br>
- [open-slide upstream framework](https://github.com/1weiho/open-slide) <br>
- [Open-slide Slide Authoring Reference](references/authoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create slide source files, static HTML builds, PDFs, and ZIP archives.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

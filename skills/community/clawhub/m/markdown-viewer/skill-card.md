## Description: <br>
Live markdown viewer for AI pair-editing. When you collaborate, the updates render instantly. Works with any AI agent and web browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI-agent users use this skill to install and run a local Markdown preview server so Markdown files update live in a browser during pair-editing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The localhost viewer can read files addressed through the view path, which may expose sensitive local files if used broadly. <br>
Mitigation: Start the server with a project root limit, such as mdview --root <your-project>, and only open files intended for preview. <br>
Risk: The skill installs and runs the third-party npm package @wipcomputer/markdown-viewer. <br>
Mitigation: Install only when the package publisher is trusted in the target environment. <br>
Risk: The preview server may continue running in the background after use. <br>
Mitigation: Stop the background server when the preview session is finished, especially on shared machines. <br>


## Reference(s): <br>
- [Markdown Viewer ClawHub page](https://clawhub.ai/parkertoddbrooks/markdown-viewer) <br>
- [npm package @wipcomputer/markdown-viewer](https://www.npmjs.com/package/@wipcomputer/markdown-viewer) <br>
- [Artifact-declared GitHub project](https://github.com/wipcomputer/wip-markdown-viewer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes npm installation, localhost server startup, browser open commands, and operational notes.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Converts HTML content from strings, files, or web URLs into Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipingme](https://clawhub.ai/user/sipingme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert HTML snippets, local HTML files, or selected webpage content into Markdown for documentation, migration, and content capture workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL fetching can reach unintended or sensitive web resources if the target URL is not checked. <br>
Mitigation: Confirm the exact URL before use and avoid internal services, private metadata endpoints, authenticated pages, and other sensitive targets. <br>
Risk: File conversion can read or overwrite paths the user did not intend. <br>
Mitigation: Confirm input and output paths before execution and avoid paths containing secrets or files that should not be modified. <br>
Risk: The skill depends on an external npm package for conversion behavior. <br>
Mitigation: Install and run it only when the external package and publisher are trusted for the environment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/sipingme/html-to-markdown-skill) <br>
- [API documentation](references/api.md) <br>
- [Quick start guide](references/quick-start.md) <br>
- [npm package](https://www.npmjs.com/package/@siping/html-to-markdown-node) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown content or JSON command responses with Markdown payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write converted Markdown to a user-specified output file when converting local HTML files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

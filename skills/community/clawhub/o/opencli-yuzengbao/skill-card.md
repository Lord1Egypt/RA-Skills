## Description: <br>
OpenCLI Universal CLI Hub helps agents use OpenCLI commands to turn websites, Electron apps, and local tools into command-line interfaces with support for public APIs, browser-authenticated sites, and structured output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzengbaao](https://clawhub.ai/user/yuzengbaao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to install and run OpenCLI, discover available site and tool commands, retrieve data from supported services, and create new adapters for websites or local tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The browser bridge can access logged-in website sessions. <br>
Mitigation: Use a separate Chrome profile with limited accounts and remove or disable the extension and daemon when not actively using the skill. <br>
Risk: Registered local CLIs may expose sensitive local capabilities to agent workflows. <br>
Mitigation: Register only low-risk tools, avoid sensitive credentials or administrative CLIs, and review commands before execution. <br>
Risk: The setup command installs an external npm package and depends on a browser extension. <br>
Mitigation: Pin and verify the npm package and extension source before use instead of relying on an unreviewed latest install. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuzengbaao/opencli-yuzengbao) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with command examples and structured-output options including JSON, CSV, YAML, and Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may depend on Node.js, a connected browser bridge, Chrome login state, and registered local CLI tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

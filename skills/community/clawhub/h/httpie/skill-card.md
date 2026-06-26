## Description: <br>
HTTPie command-line HTTP client guidance for API testing, request debugging, authentication, sessions, uploads, downloads, and formatted responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to construct, review, and run HTTPie commands for REST API testing, debugging, authentication, file transfer, proxy configuration, and session-based workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to install packages, run live HTTP requests, and execute credential-bearing commands. <br>
Mitigation: Require explicit confirmation before package installs, bootstrap commands, live requests, uploads, downloads, or any request containing credentials. <br>
Risk: Authentication tokens, passwords, cookies, and saved HTTPie sessions may be exposed through command history, verbose logs, or session files. <br>
Mitigation: Use environment variables or interactive prompts for real secrets, avoid verbose logging with tokens, inspect session files, and clear saved sessions when finished. <br>
Risk: Proxy changes or TLS verification changes can alter request routing or weaken transport security. <br>
Mitigation: Require user approval before proxy configuration changes or TLS verification changes, especially when using certificate bypass options. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-big-cabbage/httpie) <br>
- [HTTPie homepage](https://httpie.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include HTTP request examples, troubleshooting steps, installation commands, credential-handling guidance, and session-management instructions.] <br>

## Skill Version(s): <br>
0.1.1 (source: evidence release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

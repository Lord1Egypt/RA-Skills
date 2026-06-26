## Description: <br>
Isolated agent runtime for code execution, live preview URLs, browser automation, 50+ tools (ffmpeg, sqlite, pandoc, imagemagick), LLM inference, and persistent memory - all via CLI or HTTP, no SDK or API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shassingh09](https://clawhub.ai/user/shassingh09) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use PaperPod to run code, manage files and processes, expose preview URLs, automate browser tasks, call AI endpoints, and store small persistent state in an isolated remote sandbox. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PaperPod tokens grant access to the user's remote sandbox. <br>
Mitigation: Treat the token like a password, prefer environment or CLI authentication over embedding it in files, and rotate or refresh credentials when needed. <br>
Risk: The skill can execute code, run background processes, expose public preview URLs, automate browsers, and persist data in an external paid sandbox. <br>
Mitigation: Review commands before use, avoid sending secrets or private files unless necessary, monitor running processes, exposed ports, browser sessions, memory contents, and billing, and clean up resources after use. <br>
Risk: Public preview URLs can expose unauthenticated services. <br>
Mitigation: Expose only intended ports, bind services as documented, avoid sensitive unauthenticated endpoints, and stop exposed services when no longer needed. <br>


## Reference(s): <br>
- [PaperPod homepage](https://paperpod.dev) <br>
- [PaperPod documentation](https://paperpod.dev/docs) <br>
- [PaperPod API Reference](references/api-reference.md) <br>
- [Shell Tools Reference](references/shell-tools.md) <br>
- [ClawHub skill page](https://clawhub.ai/shassingh09/paperpod) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Code, Files, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, HTTP examples, endpoint references, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce public preview URLs, browser artifacts, AI outputs, and persistent memory entries through PaperPod services.] <br>

## Skill Version(s): <br>
2.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

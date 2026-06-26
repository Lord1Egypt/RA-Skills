## Description: <br>
Async/await error handling auditor that scans JavaScript, TypeScript, Python, and Go code for unhandled async errors such as floating promises, async route handlers without error boundaries, unsafe Promise or asyncio usage, ignored goroutine errors, and missing Node.js unhandled rejection listeners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to audit async error handling before production deployment or CI enforcement. It reports likely unhandled async failures and suggests concrete remediation patterns for JavaScript/TypeScript, Python asyncio and FastAPI/aiohttp, and Go goroutines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads source files under the directory selected for analysis. <br>
Mitigation: Run it against a specific project or subdirectory rather than a broad home or workspace folder. <br>
Risk: Static pattern matching can produce false positives or miss context-specific async error handling. <br>
Mitigation: Review each finding and proposed fix before changing production code or enabling the CI fail gate. <br>


## Reference(s): <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-async-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style audit report with severity-grouped findings, matched source snippets, remediation code examples, and an optional CI fail-gate command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports AE001-AE010 findings with file paths, line numbers, severity, descriptions, matched text, fixes, and per-check counts.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

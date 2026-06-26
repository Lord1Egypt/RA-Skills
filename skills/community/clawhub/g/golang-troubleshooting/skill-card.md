## Description: <br>
Troubleshoot Golang programs systematically - find and fix the root cause. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to debug Go bugs, crashes, deadlocks, flaky behavior, performance symptoms, and production incidents with a root-cause-first workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debugging workflows can expose API keys, database URLs, Authorization headers, cookies, request bodies, or response bodies. <br>
Mitigation: Redact secrets and sensitive payload data before sharing logs, traces, profiles, or command output. <br>
Risk: Production pprof or Delve access can reveal sensitive runtime information or increase operational exposure. <br>
Mitigation: Keep pprof and Delve access authenticated, network-restricted, temporary, and disabled when troubleshooting is complete. <br>


## Reference(s): <br>
- [Golang Troubleshooting on ClawHub](https://clawhub.ai/samber/golang-troubleshooting) <br>
- [Project homepage](https://github.com/samber/cc-skills-golang) <br>
- [General Debugging Methodology](references/methodology.md) <br>
- [Common Go Bugs](references/common-go-bugs.md) <br>
- [Test-Driven Debugging](references/testing-debug.md) <br>
- [Concurrency Debugging](references/concurrency-debug.md) <br>
- [Performance Troubleshooting](references/performance-debug.md) <br>
- [pprof Reference](references/pprof.md) <br>
- [Diagnostic Tools](references/diagnostic-tools.md) <br>
- [Production Debugging](references/production-debug.md) <br>
- [Compilation Issues](references/compilation.md) <br>
- [Code Review Red Flags](references/code-review-flags.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Go diagnostics, tests, code edits, profiling commands, debugger commands, and configuration changes for the user's project.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

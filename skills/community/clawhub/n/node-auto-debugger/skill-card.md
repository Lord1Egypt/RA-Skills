## Description: <br>
Scans Node.js, Express, Next.js, and React projects for backend, frontend, configuration, and optional build issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jengajojo](https://clawhub.ai/user/jengajojo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Node.js web applications for common runtime, security, hydration, SSR, configuration, and build issues before release or while debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads source files under the selected Node.js project. <br>
Mitigation: Run it only on projects you intend to scan, and avoid exposing unrelated or sensitive directories as the target path. <br>
Risk: The skill creates or overwrites AUTO-DEBUG-REPORT.md in the scanned project. <br>
Mitigation: Review or back up any existing report file before running the scanner in a working tree. <br>
Risk: The optional --build mode executes the target project's npm build script. <br>
Mitigation: Use --build only after reviewing package.json scripts, preferably in a sandbox with minimal secrets available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jengajojo/node-auto-debugger) <br>
- [Publisher profile](https://clawhub.ai/user/jengajojo) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes AUTO-DEBUG-REPORT.md in the scanned project and exits with code 1 when critical issues are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

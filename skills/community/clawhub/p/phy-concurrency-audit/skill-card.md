## Description: <br>
Static concurrency and race-condition auditor for Go, Java, Python, and Node.js/TypeScript codebases, focused on CWE-362 race conditions and CWE-367 TOCTOU patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to review source trees for common race-condition and TOCTOU patterns across Go, Java, Python, and Node.js/TypeScript. It is intended to produce local static-analysis findings and remediation guidance without external API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The embedded scanner appears broken, which can make users believe concurrency or TOCTOU checks ran when they did not. <br>
Mitigation: Fix the startup failure, add execution tests for the scanner, and review scan results manually before relying on coverage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-concurrency-audit) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with embedded Python code and optional JSON scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local static scanner output; security evidence says the embedded scanner appears broken and must be fixed and tested before relying on its coverage.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

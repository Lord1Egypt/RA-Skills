## Description: <br>
Runs PowerShell scripts in a restricted environment with command allowlists, timeout controls, output limits, file isolation guidance, and pre-execution safety checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to evaluate or run PowerShell scripts with pre-execution checks, timeout protection, command restrictions, and output controls. It is most relevant for controlled script execution, batch tasks, log analysis, and PowerShell code testing where the sandbox configuration is reviewed before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release claims sandbox protections for untrusted scripts, but the authoritative security summary says the safety claims are stronger than the documented test coverage supports. <br>
Mitigation: Treat the skill as experimental or review-only until file isolation, output and resource limits, and host/.NET capability restrictions are tested, documented, and independently reviewed. <br>
Risk: The artifact documents an AllowNetwork option and broader configurations that can weaken execution restrictions. <br>
Mitigation: Keep network access disabled for untrusted scripts, use stricter timeout and output limits, and review custom allowlists before deployment. <br>
Risk: Documented test coverage does not include file path isolation, output limit enforcement, or .NET type restriction tests. <br>
Mitigation: Add and pass tests for those controls before relying on the skill to execute untrusted scripts in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/powershell-sandbox) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [TEST_RESULTS.md](artifact/TEST_RESULTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with PowerShell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include timeout values, output limits, working-directory settings, allowlist settings, exit-code interpretation, and security review guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence, package.json, SKILL.md, TEST_RESULTS.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

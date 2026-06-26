## Description: <br>
Env Doctor validates .env files for common configuration issues, leaked secrets, duplicates, missing variables, placeholders, and syntax errors with a dependency-free Python script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit local .env files before committing, deploying, or sharing configuration. It helps identify possible secret leaks, duplicate keys, missing variables against an example file, empty values, placeholders, and syntax issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports can expose sensitive variable names, file paths, line numbers, and malformed-line snippets. <br>
Mitigation: Keep reports local and avoid publishing or broadly logging them, especially in CI. <br>
Risk: The skill reads selected .env files, which may contain secrets. <br>
Mitigation: Run it only on intended local files and review output before sharing results with other systems or users. <br>


## Reference(s): <br>
- [Env Doctor ClawHub release](https://clawhub.ai/Johnnywang2001/jrv-env-doctor) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text report or structured JSON from the local checker, plus concise agent guidance when summarizing results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes distinguish healthy files, detected issues, and possible secret leaks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Solve competitive programming problems on NCCUOJ by fetching problem statements, writing solutions, submitting code, and checking results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyjjrt](https://clawhub.ai/user/andyjjrt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and students use this skill to work through NCCUOJ public or contest problems: retrieve statements, create local solution files, run sample tests, submit accepted languages, and inspect judging results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: NCCUOJ credentials may be exposed when passed as command-line arguments or entered in shared terminals. <br>
Mitigation: Use the skill only on a trusted private machine and avoid passing real passwords through visible command histories or shared sessions. <br>
Risk: Reusable login cookies are stored in the workspace and could be reused if the workspace is shared or retained. <br>
Mitigation: Protect the .nccuoj/cookies.txt file, remove it after use, and avoid sharing workspaces that contain it. <br>
Risk: The NCCUOJ base URL can be overridden, which could send credentials or submissions to an unintended service. <br>
Mitigation: Keep NCCUOJ_BASE_URL unset or pointed only at the official NCCUOJ site before running the helper scripts. <br>
Risk: Submitting code changes account state and may affect contest participation. <br>
Mitigation: Confirm the target problem, contest, language, and source file before running submit commands. <br>


## Reference(s): <br>
- [NCCUOJ skill release on ClawHub](https://clawhub.ai/andyjjrt/nccuoj) <br>
- [NCCUOJ](https://nccuoj.ebg.tw) <br>
- [NCCUOJ API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown problem statements, source code files, JSON submission results, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes problem and solution files under .nccuoj/ and may store session cookies in .nccuoj/cookies.txt.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Track baby sleep, feeding, diapers, and growth via the Huckleberry CLI. Use when the user asks about logging baby activities, starting/stopping sleep, bottle feeding, diaper changes, or growth measurements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayhickey](https://clawhub.ai/user/jayhickey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and caregivers use this skill to get command-line guidance for recording baby sleep, feeding, diaper, and growth events with the unofficial Huckleberry CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides use of an unofficial CLI that may handle sensitive Huckleberry account credentials and child activity records. <br>
Mitigation: Install only if the unofficial package and its dependencies are trusted, prefer interactive login, protect the local config file, and avoid storing real passwords in shell history or shared environment files. <br>
Risk: Incorrect child, unit, amount, or timing arguments could log inaccurate care records. <br>
Mitigation: Review the selected child, units, amounts, and timing before executing logging commands. <br>


## Reference(s): <br>
- [Huckleberry](https://huckleberrycare.com/) <br>
- [huckleberry-api](https://github.com/Woyken/py-huckleberry-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes authentication setup guidance and optional JSON-oriented CLI usage.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

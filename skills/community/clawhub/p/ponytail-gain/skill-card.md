## Description: <br>
Show ponytail measured impact as a scoreboard: less code, less cost, more speed, from the benchmark medians. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dietrichgebert](https://clawhub.ai/user/dietrichgebert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users invoke this skill to display a one-shot Ponytail benchmark scoreboard for code, cost, and speed impact. The output is meant to communicate published benchmark medians without claiming repository-specific savings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the published benchmark figures as proof of savings in their own repository. <br>
Mitigation: Present the figures as benchmark medians only and avoid reporting per-repository savings without a measured baseline. <br>
Risk: A display-oriented skill could be misused if expanded to make changes or persist state. <br>
Mitigation: Keep invocation limited to a one-shot scoreboard and review any future changes for file edits, persistence, credentials, or privileged access. <br>


## Reference(s): <br>
- [Ponytail repository](https://github.com/DietrichGebert/ponytail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown/plain text scoreboard with ASCII bars] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One-shot display; no file edits, mode changes, persistence, credentials, or privileged access are requested.] <br>

## Skill Version(s): <br>
4.8.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

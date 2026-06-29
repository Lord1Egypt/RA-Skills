## Description: <br>
Learnings Skill logs failures, corrections, patterns, version rules, approach preferences, and behavioral corrections to a MeiliSearch index for fast recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enjuguna](https://clawhub.ai/user/enjuguna) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to log, search, auto-extract, and distill lessons from failures, corrections, preferences, and version rules so future actions can account for past mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The learnings index may retain sensitive workflow history, including mistakes, fixes, preferences, and selected memory-note content. <br>
Mitigation: Use a trusted local or controlled MeiliSearch instance, protect MEILI_KEY, review dry-run output before --apply, and avoid logging tokens, passwords, customer data, or raw output that may contain secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/enjuguna/learnings) <br>
- [Publisher profile](https://clawhub.ai/user/enjuguna) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write learning entries to a MeiliSearch index and generate a LEARNINGS.md summary when apply mode is used.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

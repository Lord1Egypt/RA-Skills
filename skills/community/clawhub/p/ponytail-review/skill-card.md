## Description: <br>
Review a diff for over-engineering and identify deletions, standard-library replacements, native platform features, speculative abstractions, and shorter equivalents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dietrichgebert](https://clawhub.ai/user/dietrichgebert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill during code review to find unnecessary complexity in diffs and get terse suggestions for what to remove or simplify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally gives terse deletion and simplification suggestions that may miss correctness, security, or performance concerns. <br>
Mitigation: Use it as a complexity-focused pass and run a normal review for bugs, security, and performance before relying on the results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dietrichgebert/skills/ponytail-review) <br>
- [Project homepage](https://github.com/DietrichGebert/ponytail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text review findings, one line per finding] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ends with a net lines possible summary when findings exist; says Lean already. Ship. when there is nothing to cut.] <br>

## Skill Version(s): <br>
4.8.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

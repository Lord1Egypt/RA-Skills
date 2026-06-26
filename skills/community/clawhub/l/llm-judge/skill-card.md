## Description: <br>
Compares two or more code implementations against a specification or requirements document and ranks them using structured evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering reviewers use this skill to compare competing repository implementations against the same spec, score them across functionality, security, tests, overengineering, and dead code, and produce a ranked verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run tests or project commands inside repositories being judged, which can execute arbitrary project code and consume local resources. <br>
Mitigation: Use it only on repositories you trust or can isolate in a sandboxed environment. <br>
Risk: The final ranking depends on extracted facts and judge outputs, so incomplete facts or invalid intermediate JSON can lead to misleading conclusions. <br>
Mitigation: Follow the hard gates that require JSON parsing, complete per-repository facts, complete per-dimension scores, and consistency between the JSON report and Markdown summary. <br>


## Reference(s): <br>
- [Fact Schema](references/fact-schema.md) <br>
- [Judge Agent Instructions](references/judge-agents.md) <br>
- [Repo Agent Instructions](references/repo-agent.md) <br>
- [Scoring Rubrics](references/scoring-rubrics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands] <br>
**Output Format:** [Markdown summary plus .beagle/llm-judge-report.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes weighted scores, rankings, verdict, and per-dimension justifications.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

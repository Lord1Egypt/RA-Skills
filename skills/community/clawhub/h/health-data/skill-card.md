## Description: <br>
Analyze Apple Health exports with local shell tooling to summarize activity, steps, sleep, record types, and source counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppopen](https://clawhub.ai/user/ppopen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and technically capable users can use this skill to inspect Apple Health exports locally, summarize common health records, and extract bounded JSON slices for further analysis. It is intended for workflows where sensitive health data should remain on the user's machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apple Health exports and derived summaries can contain PHI/PII such as biometric, sleep, heart-rate, location, and activity data. <br>
Mitigation: Keep exports and derived files local, avoid sharing raw values without explicit consent and appropriate review, and delete copies after analysis. <br>
Risk: Unbounded JSON export can produce very large sensitive outputs. <br>
Mitigation: Use --limit for exploratory exports and prefer --out so JSON is written to a restricted local file. <br>
Risk: The security evidence reports a clean verdict but also describes a low-confidence pass. <br>
Mitigation: Review the skill files and commands before installing or running the skill in a sensitive environment. <br>


## Reference(s): <br>
- [Health Data on ClawHub](https://clawhub.ai/ppopen/health-data) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples; script output is plain text summaries or JSON records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may contain PHI/PII and should be treated as sensitive derived health data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

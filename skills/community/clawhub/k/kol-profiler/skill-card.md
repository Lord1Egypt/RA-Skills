## Description: <br>
Analyze physician academic influence and collaboration networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze physician publication impact, collaboration networks, and KOL profiles for identification, collaboration mapping, advisory board planning, and speaker selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: KOL profiling outputs may be sensitive business or healthcare-related analysis. <br>
Mitigation: Use publication data you are authorized to process, keep generated files in an appropriate workspace, and delete outputs when they are no longer needed. <br>
Risk: The skill runs a local Python script and may read input files or write outputs in the workspace. <br>
Mitigation: Review inputs and output paths before execution and run the script in a controlled workspace. <br>


## Reference(s): <br>
- [KOL Profiler on ClawHub](https://clawhub.ai/aipoch-ai/kol-profiler) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text profile output and JSON-compatible analysis data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read local publication data and write generated outputs to the workspace when an output path is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

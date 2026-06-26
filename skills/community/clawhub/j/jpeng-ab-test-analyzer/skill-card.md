## Description: <br>
Analyze A/B test results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analytics practitioners use this skill to run or automate A/B test analysis workflows and return structured results for downstream reporting or integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires AB_API_KEY, which could be exposed through prompts, logs, source control, or shared shell history. <br>
Mitigation: Use a least-privilege API key and keep it out of prompts, logs, source control, and shared shell history. <br>
Risk: The artifact references scripts/ab_test_analyzer.py, but no executable analyzer script is bundled. <br>
Mitigation: Inspect any separately obtained analyzer script before running it and verify that the input and output paths are expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-ab-test-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with bash commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AB_API_KEY for configuration; the referenced analyzer script is not bundled in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

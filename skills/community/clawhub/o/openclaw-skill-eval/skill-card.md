## Description: <br>
Skill evaluation framework for testing trigger rate, quality comparison with and without a skill, model comparison, and latency profiling through agent-driven sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xiaoxing9](https://clawhub.ai/user/Xiaoxing9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to evaluate OpenClaw skills for trigger accuracy, quality improvement, model behavior, and latency. It helps compare agent outputs, collect session histories, and generate analysis reports for iterative skill improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluation transcripts and full session histories may be saved in the workspace. <br>
Mitigation: Avoid using the skill on sensitive or production conversations unless the output directory and retention policy are controlled. <br>
Risk: The HTML viewer can stop an existing local process on its selected port. <br>
Mitigation: Choose an unused local port before launching the viewer. <br>
Risk: Untrusted spreadsheet or report artifacts could be opened in the local viewer. <br>
Mitigation: Review the source and only open trusted generated artifacts in the viewer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xiaoxing9/openclaw-skill-eval) <br>
- [README](README.md) <br>
- [Usage Guide](USAGE.md) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON report artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes evaluation results, transcripts, histories, and optional HTML review artifacts to the configured workspace.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
深度测评各模型在 OpenClaw 上的实际表现，支持中文理解/代码/推理/工具调用多维度评估。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leosheep821-debug](https://clawhub.ai/user/leosheep821-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and evaluators use this skill to benchmark model behavior in OpenClaw across Chinese comprehension, coding, tool-use reasoning, complex reasoning, and response speed. It provides a standard test set, scoring dimensions, model configuration notes, and a Markdown report format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider API keys and model configuration changes may expose credentials or consume provider quota. <br>
Mitigation: Review any models.json changes before use, prefer dedicated low-privilege provider API keys, and monitor provider quota or cost during benchmark runs. <br>
Risk: Benchmark results may be misleading if prompts, scoring rubrics, or response-time measurements are applied inconsistently. <br>
Mitigation: Use the provided standard test set and weighted scoring dimensions consistently, and document deviations in the generated report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leosheep821-debug/model-benchmark) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown benchmark plan and report template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes weighted evaluation dimensions, standard prompts, scoring criteria, API-key notes, and a model report outline.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
JSON Utils helps agents parse, repair, validate, and batch-process JSON from files, JSONL, tool calls, and unreliable LLM outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikikari](https://clawhub.ai/user/kikikari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to make JSON handling more reliable when consuming LLM output, validating tool-call payloads, or processing groups of JSON and NDJSON files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The command-line batch processor can read multiple local files and write a JSONL output file when an output path is supplied. <br>
Mitigation: Run it only on intended files and review output paths before execution. <br>
Risk: The skill depends on Python packages such as pydantic, json-repair, and jsonschema. <br>
Mitigation: Install documented dependencies from trusted package sources and pin versions where reproducibility is required. <br>
Risk: Automatic JSON repair may accept malformed model output by changing syntax. <br>
Mitigation: Validate repaired data against a Pydantic model or JSON Schema before using it in downstream tools. <br>


## Reference(s): <br>
- [JSON Utils API Reference](references/api_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/kikikari/json-utils) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; CLI tools can emit JSON, JSONL, pretty-printed JSON, and validation summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch processing can parallelize local JSON file handling and optionally write JSONL result files when an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

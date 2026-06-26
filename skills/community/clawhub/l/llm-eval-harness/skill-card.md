## Description: <br>
Evaluate LLM outputs systematically by running test suites, scoring responses for accuracy, relevance, safety, and consistency, comparing models, and detecting regressions in AI applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI product teams use this skill to design and run evaluation suites, compare model behavior, detect prompt regressions, and produce concise quality reports for LLM applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to execute model-generated code during coding evaluations without detailed safety boundaries. <br>
Mitigation: Run coding evaluations only in a disposable sandbox or container with no sensitive credentials, minimal filesystem access, restricted network access, and explicit approval before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/llm-eval-harness) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with examples, tables, YAML snippets, and report outlines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces evaluation rubrics, dataset structures, model-comparison summaries, regression notes, and recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

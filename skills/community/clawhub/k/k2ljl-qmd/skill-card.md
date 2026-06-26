## Description: <br>
Searches and retrieves local Markdown knowledge bases with qmd using BM25 keyword search, vector semantic search, and hybrid LLM re-ranking modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidsteelerose](https://clawhub.ai/user/davidsteelerose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to search indexed Markdown notes, documentation, meeting transcripts, and other local knowledge bases, then retrieve specific documents or snippets for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexed Markdown notes become searchable by the agent. <br>
Mitigation: Index only Markdown folders you are comfortable making searchable, and avoid collections containing secrets unless that exposure is deliberate. <br>
Risk: Optional LLM re-ranking may expose query context depending on qmd CLI configuration. <br>
Mitigation: Verify how qmd handles embeddings and LLM re-ranking before using it with private notes. <br>
Risk: The skill depends on installing an external qmd CLI. <br>
Mitigation: Install only if you trust the external qmd CLI and its installation source. <br>


## Reference(s): <br>
- [QMD Markdown Search on ClawHub](https://clawhub.ai/davidsteelerose/k2ljl-qmd) <br>
- [qmd GitHub repository](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON-oriented command output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agents to use qmd commands with --json for structured output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

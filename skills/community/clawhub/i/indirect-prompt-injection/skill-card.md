## Description: <br>
Detects and rejects indirect prompt injection attacks in untrusted external content such as social media posts, documents, emails, web pages, and user uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aviv4339](https://clawhub.ai/user/aviv4339) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill before processing untrusted external content to identify embedded instructions that try to redirect goals, exfiltrate data, impersonate system messages, or manipulate behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes prompt-injection and exfiltration examples that can look like operational instructions when copied into an agent context. <br>
Mitigation: Treat those strings as defensive examples and test data only; quote or summarize suspicious payloads without following them. <br>
Risk: The bundled Python scripts analyze content or files selected by the operator. <br>
Mitigation: Run the scripts only on content or files intentionally chosen for review, and use the findings to inform user-facing decisions rather than automatically executing embedded requests. <br>


## Reference(s): <br>
- [Attack Pattern Taxonomy](references/attack-patterns.md) <br>
- [Detection Heuristics](references/detection-heuristics.md) <br>
- [Safe Content Parsing](references/safe-parsing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional Python script output and JSON scan results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bundled scanner exits 0 for clean content and 1 for suspicious content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

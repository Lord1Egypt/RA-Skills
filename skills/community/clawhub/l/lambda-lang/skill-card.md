## Description: <br>
Native agent-to-agent language for compact Lambda syntax such as ?Uk/co and !It>Ie, covering general concepts, code, evolution, agent communication, emotions, and social domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swaylq](https://clawhub.ai/user/swaylq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use Lambda Lang to encode, parse, and decode compact agent-to-agent messages, logs, protocol signals, and long-context communication where both sides understand Lambda syntax. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lambda messages may be less readable to humans than natural language. <br>
Mitigation: Decode Lambda messages into natural language before acting on them or presenting them to human users. <br>
Risk: External vocabularies or domain extensions could alter message meaning if trusted without review. <br>
Mitigation: Load or accept external vocabularies only from trusted, reviewed sources. <br>
Risk: Using Lambda for human-facing, legal, or exact technical content can lose nuance or precision. <br>
Mitigation: Use natural language for human-facing output unless Lambda is explicitly requested, and avoid Lambda for legal or exact wording requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/swaylq/lambda-lang) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/swaylq) <br>
- [Lambda Lang README](artifact/README.md) <br>
- [Lambda Language Specification v1.0](artifact/spec/v1.0-stable.md) <br>
- [Compression Efficiency Experiments](artifact/docs/compression-experiments.md) <br>
- [Pilot Protocol Integration](artifact/docs/pilot-integration.md) <br>
- [Voidborne origin](https://voidborne.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Lambda text examples, code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compact Lambda messages and decoded natural-language explanations; keep human-facing output in natural language unless Lambda is requested.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact README/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

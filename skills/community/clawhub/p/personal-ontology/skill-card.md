## Description: <br>
Help users build and maintain a Personal Ontology - a Palantir-style graph of Objects (identity, beliefs, predictions, goals) and Links (relationships between them) that enables AI-driven decision-making and life alignment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levineam](https://clawhub.ai/user/levineam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to build and maintain a markdown-based personal ontology from notes, goals, beliefs, predictions, and projects. The ontology helps an agent surface alignment checks, stale predictions, contradictions, and goal-to-project relationships for user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and summarize sensitive personal notes while building or maintaining the ontology. <br>
Mitigation: Use a narrow folder scope, exclude sensitive journals or archives, and require user consent before bootstrap or passive scans. <br>
Risk: Stored ontology suggestions and state files may preserve sensitive beliefs, goals, predictions, or personal history. <br>
Mitigation: Keep suggestion and state file locations visible to the user, and document how to delete or disable them. <br>
Risk: Ontology-derived guidance could steer future decisions using outdated, incorrect, or unreviewed personal data. <br>
Mitigation: Require user review before every write and periodically surface stale predictions, contradictions, and orphaned goals or projects. <br>


## Reference(s): <br>
- [Personal Ontology ClawHub listing](https://clawhub.ai/levineam/personal-ontology) <br>
- [README](artifact/README.md) <br>
- [Setup Guide](artifact/SETUP.md) <br>
- [Bootstrap Guide](artifact/bootstrap.md) <br>
- [Heuristics](artifact/heuristics.md) <br>
- [Guided Prompts](artifact/prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions, ontology templates, configuration guidance, and optional Mermaid graph output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user review before committing ontology updates; optional Node script renders Mermaid, ASCII, or SVG views from ontology files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

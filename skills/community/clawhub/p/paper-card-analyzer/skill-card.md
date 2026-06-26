## Description: <br>
Analyze `paper-parse` outputs and generate a research-oriented paper card directly in natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chen-Li-17](https://clawhub.ai/user/Chen-Li-17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill after paper parsing to turn `*_content.md` and `*_parsed.json` artifacts into structured paper-card summaries, reproducibility notes, and revision history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local paper-card outputs and may overwrite existing paper-card.md or paper-card.json files in the target folder. <br>
Mitigation: Before use, check the target folder for existing paper-card outputs and preserve earlier versions when needed. <br>
Risk: Paper summaries can be misleading if parsed paper inputs omit evidence or if unsupported claims are introduced during revision. <br>
Mitigation: Use only evidence from `*_content.md` and `*_parsed.json`, mark missing support as not clearly stated, and review each revision before relying on the card. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Chen-Li-17/paper-card-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown and JSON files with a Markdown feedback log] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves paper-card.md, paper-card.json, and paper-card-feedback.md beside the parsed paper inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

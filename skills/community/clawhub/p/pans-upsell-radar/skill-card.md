## Description: <br>
Pans Upsell Radar helps AI compute sales teams identify GPU-usage, team-growth, model-launch, and business-growth signals, then score expansion opportunities and suggest follow-up timing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and account teams use this skill to analyze local customer and signal data for AI compute upsell opportunities, expansion recommendations, and follow-up timing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores customer and opportunity data locally under ~/.qclaw, which may include confidential sales information. <br>
Mitigation: Use only authorized customer data, review or replace the bundled sample records, and control access to the local skill data directory. <br>
Risk: Broad scans can generate recommendations across customer lists without case-by-case review. <br>
Mitigation: Prefer explicit customer analysis commands for sensitive accounts and review suggested actions before using them in customer communications. <br>


## Reference(s): <br>
- [Pans Upsell Radar on ClawHub](https://clawhub.ai/dashiming/pans-upsell-radar) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain-text CLI reports with structured sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes local JSON data under ~/.qclaw/skills/pans-upsell-radar/data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

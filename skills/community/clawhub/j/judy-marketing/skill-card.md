## Description: <br>
Judy Marketing coordinates lead discovery, outbound outreach, content creation, and marketing strategy for the Judy marketing agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szzg007](https://clawhub.ai/user/szzg007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams and agent operators use this skill to find and enrich prospects, plan outbound campaigns, draft marketing content, and prepare lead or campaign outputs. It is intended for workflows involving contact data and external communications that require human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles contact data for lead enrichment and outreach. <br>
Mitigation: Use a dedicated Apollo key with limited access, keep exported contact files in controlled storage, and define deletion and retention rules. <br>
Risk: Generated recipient lists or messages could be used for inappropriate or non-compliant outreach. <br>
Mitigation: Require human review of recipient lists and messages before outreach and confirm compliance with privacy, anti-spam, opt-out, and platform rules. <br>
Risk: Secrets or exported contact data could be exposed through logs, commits, or shared output paths. <br>
Mitigation: Avoid logging or committing secrets and review output locations before storing or sharing generated CSV or JSON files. <br>


## Reference(s): <br>
- [Judy Agent Documentation](artifact/JUDY-AGENT.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/szzg007/judy-marketing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and file-output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce lead lists, campaign plans, marketing copy, CSV or JSON output references, and summary reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

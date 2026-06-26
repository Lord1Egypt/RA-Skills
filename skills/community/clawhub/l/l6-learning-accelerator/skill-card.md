## Description: <br>
Provides time-aware memory retrieval by combining vector similarity with temporal relevance and tracks learning progress for study management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyblhl](https://clawhub.ai/user/wyblhl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and learners use this skill to rank notes or memories with vector and time-based signals, parse time-related queries, and summarize learning progress across study sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may activate the skill when a user only intended a general learning or memory query. <br>
Mitigation: Use explicit prompts when invoking the skill and review generated retrieval or progress summaries before relying on them. <br>
Risk: Imported or exported progress JSON can contain learning notes, session details, or untrusted data. <br>
Mitigation: Keep import and export paths inside the workspace, avoid importing untrusted JSON, and treat exported files as potentially sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wyblhl/l6-learning-accelerator) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill metadata](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript code and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local retrieval results, temporal date ranges, progress reports, and optional JSON import/export data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

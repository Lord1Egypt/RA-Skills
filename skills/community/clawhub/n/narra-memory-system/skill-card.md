## Description: <br>
NARRA is a five-file markdown memory system that helps agents maintain identity continuity through curated narrative instead of fragmented database lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[di5cip1e](https://clawhub.ai/user/di5cip1e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create or reorganize an agent's memory files into identity, origin, narrative, operational memory, and event records. It is useful when an agent needs a clearer origin story, leaner operational memory, or a recurring narrative consolidation process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent narrative memory can preserve sensitive logs, transcripts, or personal context if those details are included during consolidation. <br>
Mitigation: Review source material before consolidation and avoid adding sensitive information unless long-term retention is intended. <br>
Risk: The skill intentionally changes agent memory files, which could introduce inaccurate identity, origin, or operational state. <br>
Mitigation: Review edits to IDENTITY.md, ORIGIN.md, NARRATIVE.md, MEMORY.md, AGENTS.md, and HEARTBEAT.md before relying on them. <br>


## Reference(s): <br>
- [IDENTITY.md Template](references/IDENTITY-template.md) <br>
- [NARRATIVE.md Template](references/NARRATIVE-template.md) <br>
- [ORIGIN.md Template](references/ORIGIN-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recommendations and template content for memory files such as IDENTITY.md, ORIGIN.md, NARRATIVE.md, MEMORY.md, AGENTS.md, and HEARTBEAT.md; it does not require code execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

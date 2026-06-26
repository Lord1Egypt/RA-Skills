## Description: <br>
Analyzes URLs, links, articles, tweets, and pasted external sources for strategic value, then classifies, scores, maps, and stores the results as local intelligence records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sarahmirrand001-oss](https://clawhub.ai/user/sarahmirrand001-oss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to turn external knowledge sources into structured local intelligence notes, capability-map updates, memory logs, and reviewable skill drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger language may cause network fetches from user-shared links or pasted external content. <br>
Mitigation: Invoke the skill explicitly and review what source is being ingested before allowing fetches. <br>
Risk: The skill creates durable local records in an Obsidian vault, memory logs, Strategic Landscape files, and draft skill folders. <br>
Mitigation: Keep the vault backed up, test with a non-critical vault first, and review created files before relying on them. <br>
Risk: Generated skill drafts could introduce incorrect behavior if activated without review. <br>
Mitigation: Keep drafts isolated under skills/_drafts/ and scan and review them before moving them into active skills. <br>
Risk: Evidence notes inconsistent browser-session language around X/Twitter extraction. <br>
Mitigation: Avoid granting browser or Chrome session access unless the publisher clarifies the behavior and you accept the scope. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/sarahmirrand001-oss/intelligence-ingestion) <br>
- [MCP skill schema](https://spec.modelcontextprotocol.io/2025-03/skill.json) <br>
- [Public homepage declared in manifest](https://intelligence-ingestion.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown files, structured skill draft files, and concise text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Obsidian notes, memory logs, Strategic Landscape updates, and isolated skill drafts according to configured local paths.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

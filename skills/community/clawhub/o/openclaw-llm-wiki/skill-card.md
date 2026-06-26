## Description: <br>
Create and maintain a persistent LLM-maintained knowledge base (wiki) following Andrej Karpathy's pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pathanaawej0-dot](https://clawhub.ai/user/pathanaawej0-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to have an agent create and maintain a persistent local Markdown wiki from curated source documents, including source summaries, entity and concept pages, indexes, logs, and maintenance reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive source documents may be reflected in derived wiki summaries, indexes, or logs. <br>
Mitigation: Keep sensitive documents out of `llm-wiki/raw/` unless local derived summaries and logs are acceptable. <br>
Risk: The agent creates and updates local Markdown files while maintaining the wiki. <br>
Mitigation: Review planned file changes before accepting them and keep raw source documents immutable. <br>
Risk: Agent-maintained wiki pages may become stale, incomplete, or contradictory as new sources are added. <br>
Mitigation: Use the skill's maintenance checks to find stale claims, contradictions, orphan pages, and missing cross-references before relying on the wiki. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pathanaawej0-dot/openclaw-llm-wiki) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown files and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a local llm-wiki directory with raw sources, wiki pages, an index, logs, and schema guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

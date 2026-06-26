## Description: <br>
Granola archive: search, sync freshness, notes, transcripts, panels, SQL counts, and Graincrawl repo work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclaw](https://clawhub.ai/user/openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use Graincrawl to search local Granola notes, transcripts, and panels, check archive freshness, refresh stale sources, and report exact date spans or source gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent access to local Granola meeting notes, transcripts, panels, and cache or API-derived content. <br>
Mitigation: Install only for agents that should inspect and summarize that archive, and review outputs before sharing sensitive information. <br>
Risk: The configured Go install uses a moving @latest module version. <br>
Mitigation: Pin and review the upstream graincrawl version before use in sensitive or controlled environments. <br>


## Reference(s): <br>
- [Graincrawl repository](https://github.com/openclaw/graincrawl) <br>
- [ClawHub Graincrawl listing](https://clawhub.ai/openclaw/graincrawl) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with inline shell commands, JSON snippets, and SQL snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include absolute date spans, note titles, source gaps, exact counts, and transcript or panel availability.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

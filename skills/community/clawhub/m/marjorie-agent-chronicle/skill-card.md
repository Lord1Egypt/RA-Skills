## Description: <br>
AI-powered diary generation for agents - creates rich, reflective journal entries (400-600 words) with Quote Hall of Fame, Curiosity Backlog, Decision Archaeology, and Relationship Evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate diary-style Markdown reflections from an agent's recent sessions, including wins, frustrations, learnings, quotes, curiosities, decisions, and relationship notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session logs and diary context may be sent to SkillBoss API Hub for generation. <br>
Mitigation: Review config.json before use, set SKILLBOSS_API_KEY only in trusted environments, run with --dry-run first, and avoid submitting sensitive session content. <br>
Risk: Generated diary entries and derived notes can be written into persistent memory files. <br>
Mitigation: Disable memory_integration or sensitive sections when persistence is not desired, and use --no-persistent when appropriate. <br>
Risk: HTML export may load remote stylesheet resources. <br>
Mitigation: Avoid HTML export or review exported HTML settings when remote resource loading is a concern. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/marjorie-agent-chronicle) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [README](README.md) <br>
- [Example configuration](config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with optional HTML or PDF exports and JSON task payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates 400-600 word diary entries and can write persistent memory files when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact files declare 0.6.2 in SKILL.md and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

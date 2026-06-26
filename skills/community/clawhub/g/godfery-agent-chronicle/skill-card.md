## Description: <br>
Agent Chronicle generates reflective, AI-written diary entries from recent agent session context, with optional quote, curiosity, decision, relationship, and export workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their operators use Agent Chronicle to turn recent session logs and diary memory into reflective daily journal entries, persistent quote, curiosity, and decision notes, and optional PDF or HTML exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent session logs, diary context, and persistent notes may be sent to SkillBoss API Hub during generation. <br>
Mitigation: Review memory files for secrets before generation, use --emit-task or --dry-run to inspect payloads, and run with SKILLBOSS_API_KEY only when that data sharing is acceptable. <br>
Risk: Diary entries and indexes can persist personal notes, quotes, decisions, and relationship context beyond the immediate session. <br>
Mitigation: Use --no-persistent for sensitive days, keep private diary settings, and review memory/diary before sharing or exporting. <br>
Risk: Broad trigger phrases may start diary generation when the user only intended a related discussion. <br>
Mitigation: Avoid broad trigger-based use unless diary generation is explicitly desired; run the scripts manually for tighter control. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/godferylindsay/godfery-agent-chronicle) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [config.example.json](artifact/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown diary entries, JSON task payloads, and optional PDF or HTML exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists entries and optional quote, curiosity, decision, and relationship indexes under memory/diary; generated entries target roughly 400-600 words.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

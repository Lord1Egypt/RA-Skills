## Description: <br>
Octo Mention helps agents build and maintain confidence-scored nickname, alias, and mention mappings for OpenClaw group members using authoritative member fields and message-history evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovejing0306](https://clawhub.ai/user/lovejing0306) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of OpenClaw group agents use this skill to identify group members by uid, aliases, nicknames, and bot names, then maintain a local mention mapping database for later lookup. It is most useful when an agent needs to resolve ambiguous human-facing names into stable member identities across one or more groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated mapping files can expose group member identities, aliases, group context, and message evidence. <br>
Mitigation: Keep openclaw.json and openclaw.md private, avoid committing generated files, and restrict filesystem access to the mapping database and lookup script. <br>
Risk: Nickname and alias mappings may be wrong, ambiguous, stale, or based on limited message evidence. <br>
Mitigation: Use confidence scores, evidence counts, conflicts, rejected aliases, and manual correction or locking workflows before relying on a mapping in sensitive workflows. <br>


## Reference(s): <br>
- [Octo Mention on ClawHub](https://clawhub.ai/lovejing0306/octo-mention) <br>
- [Publisher profile](https://clawhub.ai/user/lovejing0306) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON mention mappings, Markdown summaries, command-line guidance, and lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates a local persons database keyed by uid, with confidence scores, evidence snippets, conflicts, group provenance, manual corrections, and optional time-decayed lookup results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

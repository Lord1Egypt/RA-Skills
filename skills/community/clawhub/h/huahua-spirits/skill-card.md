## Description: <br>
Huahua Spirits gives each user a deterministic companion spirit with a personality, rarity, attributes, local growth state, and bilingual card-style interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiye1997](https://clawhub.ai/user/baiye1997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to add a lightweight ambient companion to an agent, including spirit generation, display cards, mood and bond tracking, and short personality-driven interactions. It is for companionship and presentation, not for completing work tasks on the user's behalf. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce ambient companion messages without an explicit command. <br>
Mitigation: Install it only where passive companion chatter is acceptable, and disable idle or hook integrations in sensitive workflows. <br>
Risk: Identity-based seeds and companion history may reveal personal or message context if real platform IDs or message snippets are retained. <br>
Mitigation: Use a pseudonymous seed in sensitive or shared environments, review or clear assets/companion.json periodically, and disable hook-react logging when snippets should not be stored. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/baiye1997/huahua-spirits) <br>
- [README](README.md) <br>
- [Product Specification](SPEC.md) <br>
- [Species Guide](references/species-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style companion cards, ASCII sprites, JSON command responses, and short bilingual text responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Node.js helpers generate deterministic spirit data and update a small local companion state file.] <br>

## Skill Version(s): <br>
1.4.7 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Detects ambiguous pronouns, vague referents, and bare imperatives in user messages and flags them for resolution using conversation context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to surface ambiguous references in prompts so the agent can resolve obvious referents, state assumptions when needed, or ask before acting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an always-on prompt hook and records local metadata about scans and resolved references. <br>
Mitigation: Install only where local prompt scanning is acceptable, review or clear files under ~/.claude/skills/pronoun-resolver/.claude/, and use the documented .claude/pronoun-resolver-disabled file to disable it for a workspace. <br>
Risk: Resolved references can still point to the wrong target when conversation context is unclear. <br>
Mitigation: Follow the documented confidence tiers: act silently only for high-confidence cases, state assumptions for medium-confidence cases, and ask the user when confidence is low or context is missing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text hook flags with command guidance for optional local logging] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally; no external API calls are described in the artifact.] <br>

## Skill Version(s): <br>
0.11.0 (source: server evidence, frontmatter, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

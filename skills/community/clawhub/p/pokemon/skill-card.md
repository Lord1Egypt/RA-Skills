## Description: <br>
CLI for AI agents to lookup Pokemon info for their humans. Uses PokeAPI. No auth required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffaf](https://clawhub.ai/user/jeffaf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent look up Pokemon names, stats, type matchups, and abilities from PokeAPI without authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed bundle only contains documentation, so installed wrapper and script files may not be represented in the reviewed artifact. <br>
Mitigation: Verify the installed pokemon wrapper and scripts are included from the expected install source and scan them before use. <br>
Risk: The skill makes network requests to PokeAPI and depends on the availability and accuracy of that external service. <br>
Mitigation: Use the skill for lookup assistance, review important results before relying on them, and expect failures if PokeAPI is unavailable. <br>


## Reference(s): <br>
- [ClawHub Pokemon Skill](https://clawhub.ai/jeffaf/pokemon) <br>
- [PokeAPI](https://pokeapi.co) <br>
- [PokeAPI v2 Documentation](https://pokeapi.co/docs/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bash, curl, and jq; makes read-only requests to PokeAPI and requires no authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

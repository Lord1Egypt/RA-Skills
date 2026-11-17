## Description:

Pokeinfo lets an agent query Pokemon information from PokeAPI by name or ID and return localized details such as stats, abilities, types, moves, sprites, and optional cry audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisluo5311](https://clawhub.ai/user/chrisluo5311)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up Pokemon data through an agent or command-line workflow, including localized names and labels. Agents can also request a converted Pokemon cry audio file for messaging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice mode trusts URLs returned by an external API for cry audio.

Mitigation: Use voice mode cautiously and add outbound URL allowlisting for expected PokeAPI and raw GitHub asset hosts before deployment in sensitive environments.

Risk: Voice mode uses unsafe temporary files for downloaded and converted cry audio.

Mitigation: Use secure per-run temporary files and clean them after sending the voice message; disable voice mode on shared machines until this is addressed.

Risk: The server security verdict is suspicious pending review.

Mitigation: Review and scan the skill before installation, and run it with least privilege on machines that do not hold sensitive data.

## Reference(s):

- [ClawHub Pokeinfo Skill](https://clawhub.ai/chrisluo5311/skills/pokeinfo)
- [PokeAPI Documentation](https://pokeapi.co/docs/v2)
- [PokeAPI](https://pokeapi.co)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Plain text with optional JSON voice marker and localized labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save language settings under ~/.config/pokeinfo/config.json and may create converted voice audio files under the system temporary directory.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

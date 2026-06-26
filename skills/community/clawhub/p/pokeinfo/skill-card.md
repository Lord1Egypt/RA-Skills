## Description: <br>
Pokeinfo queries Pokemon details from PokeAPI by name or ID, including stats, abilities, types, moves, sprites, cries, and localized output across nine languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisluo5311](https://clawhub.ai/user/chrisluo5311) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Pokeinfo to retrieve formatted Pokemon data and optional cry audio for chat or agent workflows without API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to public Pokemon data hosts and depends on their availability and returned data. <br>
Mitigation: Allow only the expected public Pokemon data hosts, handle request failures clearly, and avoid presenting unavailable data as verified. <br>
Risk: Optional voice output creates a temporary local audio file and emits its path. <br>
Mitigation: Use the voice_path only to send the requested Pokemon cry, then clean up temporary files according to the host application's retention policy. <br>
Risk: Static capability metadata flags sensitive credentials even though the security evidence says no API keys or credentials appear required. <br>
Mitigation: Do not configure secrets for this skill; review installation only for expected public network access and local file handling. <br>


## Reference(s): <br>
- [PokeAPI documentation](https://pokeapi.co/docs/v2) <br>
- [ClawHub Pokeinfo listing](https://clawhub.ai/chrisluo5311/pokeinfo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Localized plain text with URLs, shell command examples, and optional JSON voice-file descriptors.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Language settings are stored locally; optional voice output creates a temporary OGG Opus file path for the requested Pokemon cry.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

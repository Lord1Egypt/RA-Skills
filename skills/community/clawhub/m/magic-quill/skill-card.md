## Description: <br>
Magic Quill generates themed OpenClaw Spellbook YAML mapping files from a topic, URL, or explicit theme, using public spell-list references when available and heuristic fallback when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wynnsu](https://clawhub.ai/user/wynnsu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Magic Quill to create or refresh themed YAML spell mappings for OpenClaw Spellbook, usually under a spells directory. The generated mappings require the OpenClaw Spellbook hook before the themed spell names can be used in agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator contacts public web, search, and API sources and can fetch user-provided URLs. <br>
Mitigation: Avoid localhost or private/internal URLs and review the listed reference URLs before enabling the generated mappings. <br>
Risk: The generator writes YAML to a user-controlled output path. <br>
Mitigation: Keep --out inside the intended spells directory and review the generated YAML before using it with the Spellbook hook. <br>


## Reference(s): <br>
- [Magic Quill ClawHub page](https://clawhub.ai/wynnsu/magic-quill) <br>
- [Publisher profile](https://clawhub.ai/user/wynnsu) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Files, Shell commands, Guidance] <br>
**Output Format:** [YAML file with console status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a themed spell mapping file, commonly under spells/<theme-slug>.yaml, and may include spell-list reference URLs as comments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Parse YAML/JSON/TOML front-matter from strings or files using the gray-matter library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract, inspect, strip, test, or stringify front-matter in Markdown and other content files. It is suited for metadata handling in documentation, static-site, and content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script may run an unpinned npm install for gray-matter on first use. <br>
Mitigation: Preinstall a reviewed, pinned gray-matter dependency in a controlled environment before using the skill. <br>
Risk: The parser reads local files or stdin and can surface file contents in agent output. <br>
Mitigation: Run it only on files the agent is intended to read, and review outputs before sharing them outside the workspace. <br>


## Reference(s): <br>
- [gray-matter API Reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/openlark/gray-matter) <br>
- [OpenLark publisher profile](https://clawhub.ai/user/openlark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and JavaScript examples; the bundled script emits JSON, YAML, text, or boolean output depending on flags.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read from files or stdin, parse with custom delimiters or languages, and stringify JSON data into front-matter.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

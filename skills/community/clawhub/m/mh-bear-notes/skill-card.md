## Description: <br>
Create, search, and manage Bear notes via grizzly CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create, read, append to, search, and manage Bear notes on macOS through the grizzly CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to read or change local Bear notes through the third-party grizzly CLI. <br>
Mitigation: Review note-writing actions before approving them and use dry-run or URL preview options when appropriate. <br>
Risk: Bear API tokens are sensitive and may appear in shared logs, shell snippets, or loosely protected files. <br>
Mitigation: Store the token with restrictive file permissions, avoid exposing real tokens in logs or prompts, and prefer token-file based configuration. <br>
Risk: The install metadata uses the latest grizzly module version, which may change over time. <br>
Mitigation: Pin or review the grizzly version before installation in managed or commercial environments. <br>


## Reference(s): <br>
- [Bear](https://bear.app) <br>
- [grizzly CLI module](https://github.com/tylerwince/grizzly) <br>
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/mh-bear-notes) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and TOML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Bear note identifiers, JSON callback output, x-callback-url previews, and local configuration paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

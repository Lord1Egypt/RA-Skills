## Description: <br>
OpenStartMenuInk scans Windows Start Menu shortcuts, caches them locally, and opens matching applications by name using fuzzy matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Flychicks](https://clawhub.ai/user/Flychicks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Windows users and assistants use this skill to launch installed Start Menu applications from natural-language or text requests without manually finding shortcuts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans Windows Start Menu shortcut folders and stores installed-application shortcut names in a local cache. <br>
Mitigation: Install only on devices where local shortcut inventory caching is acceptable, and review or clear the cache if installed-application information is sensitive. <br>
Risk: Fuzzy matching can open an unintended application when the requested name is ambiguous. <br>
Mitigation: Use specific application names and confirm the target before relying on approximate matches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Flychicks/openstartmenuink) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Text with shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only; uses fuzzy app-name matching and a locally cached shortcut index.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.schema.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

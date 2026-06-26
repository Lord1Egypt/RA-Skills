## Description: <br>
Security audit tool for Claw Skills that scans skill folders for quality issues, security vulnerability patterns, documentation completeness, and code-documentation consistency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vimvem](https://clawhub.ai/user/vimvem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use ict to audit individual or installed Claw skills, generate trust scores, compare versions, and produce human-readable or JSON findings before review or deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads the skill folders it is pointed at. <br>
Mitigation: Run it only against skill folders you intend to inspect and are comfortable exposing to local analysis. <br>
Risk: Running ict.py performs an update check against api.clawhub.ai. <br>
Mitigation: Use it in environments where this outbound update check is acceptable. <br>
Risk: Bundled test samples intentionally contain vulnerable patterns for detection. <br>
Mitigation: Do not manually execute bundled test sample files; treat them as scanner fixtures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vimvem/ict) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON] <br>
**Output Format:** [Plain text audit reports or JSON objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI exit codes distinguish pass, review, fail, and error states.] <br>

## Skill Version(s): <br>
4.0.8 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

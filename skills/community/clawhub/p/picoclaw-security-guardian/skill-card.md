## Description: <br>
Picoclaw security posture skill with advisory awareness, configuration drift detection, and supply-chain verification guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
Developers and security operators use this skill to assess Picoclaw gateway posture, check advisory feed state, detect configuration drift, and verify release artifacts before trusting deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated profiles and reports can expose local paths, file metadata, hashes, and secret-marker counts. <br>
Mitigation: Review --watch, --artifact, --config, and --output paths before running the skill and store generated outputs under the intended Picoclaw security directory. <br>
Risk: Unsigned advisory or checksum modes reduce assurance and are not suitable for normal production verification. <br>
Mitigation: Use signed advisory feeds and detached signature verification by default; reserve unsigned modes for short, documented troubleshooting windows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/picoclaw-security-guardian) <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-producing Node.js scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Profile and verification outputs can include local paths, file sizes, modes, hashes, and secret-marker counts.] <br>

## Skill Version(s): <br>
0.0.3 (source: frontmatter, skill.json, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

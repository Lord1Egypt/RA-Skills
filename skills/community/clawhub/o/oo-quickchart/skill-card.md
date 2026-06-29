## Description: <br>
QuickChart helps agents build chart image URLs, QR code URLs, and chart short URLs through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to generate QuickChart chart image URLs, QR code URLs, and chart short URLs while inspecting the live connector schema before sending payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creating a QuickChart short URL changes external service state. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running create_chart_short_url. <br>
Risk: Assuming connector fields can produce malformed or unintended requests. <br>
Mitigation: Fetch the live connector schema before constructing action payloads. <br>
Risk: Setup and login commands can install software or authenticate the OOMOL CLI. <br>
Mitigation: Run setup or login steps only after an oo command fails with the matching documented error. <br>


## Reference(s): <br>
- [QuickChart homepage](https://quickchart.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return QuickChart URLs and connector JSON responses when actions are run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

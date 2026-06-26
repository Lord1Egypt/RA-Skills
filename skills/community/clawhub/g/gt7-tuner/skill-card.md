## Description: <br>
AI tuning assistant for Gran Turismo 7 that helps an agent read GT7 settings screenshots, use GT Pro Tune, and return optimized car setup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IamSteveBot](https://clawhub.ai/user/IamSteveBot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and agent users use this skill to tune Gran Turismo 7 cars for specific tracks, driving styles, and setup goals. The agent extracts or confirms car settings, helps operate GT Pro Tune, and summarizes suspension, transmission, and differential recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require an agent to access a user's GT Pro Tune account. <br>
Mitigation: Keep credentials out of chat and logs, store them securely, and explicitly approve any browser login. <br>
Risk: OCR-extracted GT7 settings may be wrong or incomplete when screenshots are unclear. <br>
Mitigation: Confirm extracted values with the user before submitting them to GT Pro Tune or applying the resulting tune. <br>
Risk: The workflow may upload screenshots or operate GT Pro Tune through browser automation. <br>
Mitigation: Ask for explicit user approval before screenshot upload or browser actions involving the GT Pro Tune account. <br>


## Reference(s): <br>
- [GT7 tuning knowledge base](references/gt7-tuning-knowledge.md) <br>
- [GT Pro Tune](https://app.gtprotune.com/) <br>
- [GT Pro Tune registration](https://app.gtprotune.com/register) <br>
- [ClawHub release page](https://clawhub.ai/IamSteveBot/gt7-tuner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with tuning values, checklists, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OCR confidence checks, unit conversions, browser automation steps, and GT7 tuning recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
PPTClaw helps agents create and edit presentation decks by writing slide JSON files, validating deck structure, and using the pptclaw CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pptclaw](https://clawhub.ai/user/pptclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation-building agents use this skill to create, inspect, edit, validate, and open local presentation deck folders made of manifest and slide JSON files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or running the pptclaw CLI may execute third-party package code on the local machine. <br>
Mitigation: Confirm that the pptclaw npm package is trusted before global installation, and approve CLI commands before executing them. <br>
Risk: Image search and download commands can contact external services and import third-party media into a deck. <br>
Mitigation: Use image search and downloads only for approved queries and URLs, and review imported media rights and contents before relying on the deck. <br>
Risk: Direct slide JSON edits can create malformed decks or unreadable slide layouts. <br>
Mitigation: Run pptclaw validate on the target deck and review rendered slides before presenting or distributing the output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pptclaw/pptclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON, TypeScript, HTML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deck-creation and editing guidance for local files, including manifest.json, slide JSON, validation steps, and optional CLI commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

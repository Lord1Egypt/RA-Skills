## Description: <br>
Creates a single PowerPoint .pptx pitch deck for investor, product launch, sales, fundraising, startup pitch, or business proposal scenarios using OfficeCLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iceyliu](https://clawhub.ai/user/iceyliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business teams use this skill to plan and generate professional pitch decks as PowerPoint files. It supports deck structures, slide patterns, charts, styled tables, stat callouts, transitions, validation, and speaker notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill tells the agent to download and run an unpinned OfficeCLI installer or updater before creating slides. <br>
Mitigation: Install and review a pinned OfficeCLI version separately, then remove or ignore the automatic curl/bash installer and updater block. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iceyliu/officecli-pitch-deck) <br>
- [Creating a Pitch Deck](creating.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Guidance] <br>
**Output Format:** [PowerPoint .pptx file plus Markdown with inline OfficeCLI shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The expected deliverable is one .pptx file with speaker notes on content slides and validation performed with officecli validate.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Screen startup pitch decks from a VC or angel investor perspective by parsing deck structure with SoMark, researching key claims with web search, and producing a concise pre-meeting investment memo with an investment signal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soul-code](https://clawhub.ai/user/soul-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and startup evaluators use this skill to screen inbound pitch decks, prepare for founder meetings, and compare deck claims against external research before deciding whether to proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pitch decks are sent to SoMark for parsing. <br>
Mitigation: Use the skill only for decks whose confidentiality requirements are compatible with SoMark's privacy, retention, and security terms. <br>
Risk: Company and founder details may be used in external web searches. <br>
Mitigation: Avoid searching sensitive or NDA-restricted details unless external research is permitted for the deck. <br>
Risk: The skill requires SOMARK_API_KEY. <br>
Mitigation: Store the API key as a secret, do not paste it into chat, and rotate it if exposure is suspected. <br>
Risk: Parsed deck outputs are written to a local output directory. <br>
Mitigation: Choose an appropriate local directory, restrict access where needed, and remove generated files when they are no longer required. <br>


## Reference(s): <br>
- [Pitch Screener on ClawHub](https://clawhub.ai/soul-code/pitch-screener) <br>
- [SoMark Login](https://somark.tech/login) <br>
- [SoMark Workbench Purchase](https://somark.tech/workbench/purchase) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown investment memo with parser output files in Markdown and JSON, plus shell command examples for deck parsing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local pitch deck file path and SOMARK_API_KEY; parsed outputs are written to the selected local output directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

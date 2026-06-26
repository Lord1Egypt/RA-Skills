## Description: <br>
Auto-fill and submit Malaysia Digital Arrival Card (MDAC) forms for travelers entering Malaysia, including required traveler details, field selection, slider CAPTCHA handling, and form submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sidyangx](https://clawhub.ai/user/sidyangx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers or their agents use this skill to prepare and submit Malaysia Digital Arrival Card entries with passport, travel, contact, and accommodation details. It is intended for repeated MDAC filing workflows, especially Singapore-to-Johor travel scenarios described in the artifact. <br>

### Deployment Geography for Use: <br>
Malaysia <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates a protected government immigration workflow and intentionally bypasses the site's CAPTCHA. <br>
Mitigation: Prefer a fill-only flow where the traveler completes CAPTCHA manually and gives explicit confirmation before submission. <br>
Risk: Passport, travel, contact, and accommodation details may be exposed through command-line arguments, shell history, process listings, or generated screenshots. <br>
Mitigation: Store traveler data in a restricted local JSON file, avoid command-line JSON for real personal details, and delete any screenshots containing sensitive information. <br>
Risk: Incorrect traveler details can be submitted automatically to an official immigration service. <br>
Mitigation: Require the traveler to review all populated fields before submission and keep a confirmation record of what was submitted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sidyangx/mdac-filler) <br>
- [Official MDAC Registration Page](https://imigresen-online.imi.gov.my/mdac/main?registerMain) <br>
- [MDAC Field Reference](references/field-values.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run Playwright browser automation, submit traveler data to the official MDAC website, and optionally save screenshots.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Parses parcel vertex coordinates from images or text, generates Ovitalmap-compatible vertex and boundary CSVs, categorizes parcels by country code and provider, and archives records in a per-country database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeromeex](https://clawhub.ai/user/jeromeex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and field teams use this skill to convert parcel coordinate inputs into Ovitalmap import CSVs and maintain a local per-country parcel archive with provider metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local archive can persist parcel coordinates, provider names, and official cadastre identifiers, and coordinate matches can reveal archived metadata to later users. <br>
Mitigation: Decide workspace archive access and retention before use, restrict archive files to authorized users, and review archive-hit metadata before sharing outputs. <br>
Risk: Ambiguous coordinates, provider names, or official IDs can lead to incorrect country assignment, provider matching, or parcel coding. <br>
Mitigation: Ask targeted clarification questions, inspect script results before writing files, and confirm ambiguous provider or registration matches with the user. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/jeromeex/skills/ovitalmap-parcel-csv) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Guidance] <br>
**Output Format:** [CSV files plus concise Markdown or text delivery notes and JSON script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates paired Ovitalmap vertex and boundary CSV files and may update local archive CSVs.] <br>

## Skill Version(s): <br>
2.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

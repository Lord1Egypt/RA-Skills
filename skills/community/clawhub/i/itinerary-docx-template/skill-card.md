## Description: <br>
Generate tourism itinerary DOCX by replacing only matched itinerary sections inside a provided Chinese template document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nnswjlll](https://clawhub.ai/user/nnswjlll) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travel-agency operators and itinerary authors use this skill to turn simplified Chinese day-by-day route text into a styled DOCX itinerary based on a supplied template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated DOCX files may silently remove tables or contract-related sections even when template terms are expected to remain unchanged. <br>
Mitigation: Use only copies of templates, pass --keep-contract when legal terms, pricing tables, or standards must be preserved, and manually inspect generated documents before sending them to clients or relying on them for contracts or compliance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nnswjlll/itinerary-docx-template) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration] <br>
**Output Format:** [DOCX file generated from a source template and UTF-8 text input] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python-docx and a matching template layout; the script prints the output DOCX path after generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

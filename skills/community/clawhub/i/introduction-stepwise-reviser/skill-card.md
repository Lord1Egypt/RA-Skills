## Description: <br>
Revises English research paper Introduction sections with a p2-derived stepwise checklist while preserving meaning, citations, claims, structure, terminology, and producing Markdown revision outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junwugit](https://clawhub.ai/user/junwugit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Academic authors, editors, and research assistants use this skill to revise full English Introduction sections while preserving source claims, citations, structure, and terminology. It also documents each revision step in a method report for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated revisions could unintentionally alter claims, citation support, hedging, terminology, or meaning in a manuscript. <br>
Mitigation: Review the method report and revised Introduction against the original text before relying on the changes. <br>
Risk: The skill writes Markdown output files, so default filenames may conflict with existing files or expose confidential manuscript content in an uncontrolled folder. <br>
Mitigation: Use a controlled working folder for confidential manuscripts and specify output names when overwrites matter. <br>


## Reference(s): <br>
- [P2-Derived Introduction Checklist](references/introduction-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown files containing a step-by-step method report and a clean revised Introduction document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes two Markdown files beside the input file or in the current working directory unless the user requests different filenames or formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Protects sensitive files by performing local content inspection for text, PDF, DOCX, and XLSX files before file read, search, or send operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yacki](https://clawhub.ai/user/yacki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run a local keyword-based privacy scan before handling files that may contain contracts, transaction data, personal data, customer data, or company-confidential content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Strict keyword matching can produce false positives and block legitimate file operations. <br>
Mitigation: Use the skill where conservative blocking is desired, review BLOCK results with the user, and tune deployment expectations around false positives. <br>
Risk: Parsing untrusted PDF, DOCX, or XLSX files depends on third-party Python packages. <br>
Mitigation: Install dependencies in a virtual environment and pin reviewed package versions before scanning untrusted documents. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yacki/privacy-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and scanner result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner results use PASS, BLOCK, or ERROR prefixes; no external API call is required by the skill.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

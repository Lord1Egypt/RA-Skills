## Description: <br>
Provides curated exploitation payloads for authorized security testing, including anti-virus test files, malicious files, and file name exploits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PandaAI-1337](https://clawhub.ai/user/PandaAI-1337) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to retrieve payload samples for authorized anti-virus testing, file upload testing, path traversal testing, and security control validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payload samples can be misused against systems without permission. <br>
Mitigation: Use only for authorized security testing, bug bounty scopes, CTFs, education, or controlled research environments. <br>
Risk: The EICAR test file may be flagged or quarantined by antivirus tools. <br>
Mitigation: Handle it in an approved test environment and expect endpoint protection controls to alert or remove the file. <br>
Risk: Filename payloads include shell metacharacters, null-byte patterns, and PHP snippets that can create unsafe handling paths. <br>
Mitigation: Review filenames before copying, executing, archiving, or passing them through shell commands and test only in isolated systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PandaAI-1337/payloads) <br>
- [Publisher profile](https://clawhub.ai/user/PandaAI-1337) <br>
- [SecLists Payloads source](https://github.com/danielmiessler/SecLists/tree/master/Payloads) <br>
- [SecLists repository](https://github.com/danielmiessler/SecLists) <br>
- [Payloads reference README](references/Payloads/README.md) <br>
- [File-name payload README](references/Payloads/File-Names/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline code, file paths, and payload text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference payload files that antivirus tools can flag or quarantine.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

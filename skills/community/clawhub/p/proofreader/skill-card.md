## Description: <br>
Proofreader helps agents check Chinese and English text for typos, grammar issues, style consistency, document consistency, readability, and proofreading reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to proofread Chinese or English text, receive correction suggestions, align style and terminology, score readability, and produce a concise proofreading report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled generic command-line utility can retain user input and command history under the proofreader data directory. <br>
Mitigation: Use scripts/proofread.sh for proofreading, and avoid scripts/script.sh with sensitive text unless local add/search/export behavior and retained logs are intentional. <br>
Risk: Installing or running the package without review may expose users to behavior outside the proofreading function. <br>
Mitigation: Review the skill before installing and limit use to the proofreading script when that is the intended workflow. <br>


## Reference(s): <br>
- [Proofreader ClawHub page](https://clawhub.ai/bytesagain3/proofreader) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown proofreading prompts, correction tables, revised text, readability summaries, and shell command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include corrected text, issue lists, style recommendations, consistency scores, readability scores, and report summaries.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

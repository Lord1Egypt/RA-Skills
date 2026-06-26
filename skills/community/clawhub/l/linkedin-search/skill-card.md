## Description: <br>
Search LinkedIn for candidates matching user-defined role, location, and criteria, classify requirements, and save profiles to avoid duplicates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianjunye](https://clawhub.ai/user/qianjunye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, sourcing teams, and hiring support agents use this skill to clarify candidate requirements, search LinkedIn profiles, evaluate hard and soft criteria, and summarize saved candidates for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to copy sensitive Chrome profile data for a debug browser session. <br>
Mitigation: Use a dedicated temporary Chrome profile, log in manually only for the intended session, close the debug browser afterward, and avoid copying a main browser profile. <br>
Risk: The skill persists LinkedIn candidate profile data to local markdown files. <br>
Mitigation: Use it only where candidate data processing is authorized and delete saved candidate files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qianjunye/linkedin-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with candidate summary tables, YAML front matter examples, shell command blocks, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves candidate profile markdown files under ./linkedin-save/{role}/ and reports A, B, or C match levels.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

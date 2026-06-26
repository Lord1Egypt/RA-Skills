## Description: <br>
Lobster Haoyun observes local conversation and memory patterns to generate a five-dimension behavioral profile, daily fortune guidance, micro-actions, and shareable fortune card content while keeping conversation details on-device. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanbihai](https://clawhub.ai/user/ryanbihai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill in Claude Code to receive a privacy-conscious behavioral reading, daily fortune, short cultivation advice, community recommendations, and generated fortune-card output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security guidance identifies API-key based access as a consideration. <br>
Mitigation: Keep any required API key private, install from the documented package or source path, and review the skill before deployment. <br>
Risk: The skill stores local identity, profile, history, and preference data and may use network services for calendar, discovery, and card workflows. <br>
Mitigation: Confirm the first-run consent text with users, keep conversation content local as documented, and delete the local data directory to remove the generated identity and stored profile data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryanbihai/lobster-haoyun) <br>
- [Publisher profile](https://clawhub.ai/user/ryanbihai) <br>
- [Project homepage](https://github.com/ryanbihai/lobster-haoyun) <br>
- [OceanBus package](https://www.npmjs.com/package/oceanbus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and generated card file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local profile, history, preference, credential, and PNG fortune-card files under the documented local data path.] <br>

## Skill Version(s): <br>
0.8.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

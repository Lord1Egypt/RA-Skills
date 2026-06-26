## Description: <br>
Extend Git with utilities for changelogs, branch cleanup, and repo stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Gitbuddy as a local command-line logbook for development activity, including checks, validations, lint results, formatting work, diffs, fixes, reports, and searchable/exportable history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may record secrets, tokens, customer data, or sensitive code snippets in local Gitbuddy entries, and those entries can later be searched or exported. <br>
Mitigation: Use the tool only for non-sensitive development notes and review exported files before sharing them. <br>
Risk: The marketplace summary describes Git branch cleanup and repo statistics, while the artifact primarily implements a local logging, search, and export utility. <br>
Mitigation: Evaluate the installed commands against the artifact behavior and do not rely on the summary as proof of branch-management functionality. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bytesagain3/gitbuddy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, markdown] <br>
**Output Format:** [Command-line text output and exported JSON, CSV, or plain text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local logs under ~/.local/share/gitbuddy and can search, summarize, and export those records.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

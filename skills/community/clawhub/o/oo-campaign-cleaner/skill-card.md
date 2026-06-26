## Description: <br>
Campaign Cleaner helps agents manage email campaign analysis through an OOMOL-connected Campaign Cleaner account, including listing campaigns, retrieving analysis payloads, checking status, downloading PDF reports, submitting HTML for processing, and checking credits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to operate Campaign Cleaner through an OOMOL-connected account for email campaign analysis workflows. It supports read operations, campaign submission, deletion, credit lookup, and PDF analysis retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected Campaign Cleaner account and therefore depends on sensitive credentials managed outside the artifact. <br>
Mitigation: Install and use it only when the user intends to connect Campaign Cleaner through OOMOL; do not request or expose raw API keys in prompts or command output. <br>
Risk: Campaign submission changes live Campaign Cleaner state and may consume service credits. <br>
Mitigation: Confirm the exact HTML payload, target account context, and expected effect with the user before running the write action. <br>
Risk: Campaign deletion removes saved Campaign Cleaner data. <br>
Mitigation: Require explicit user approval for the campaign ID and destructive effect before running the deletion action. <br>


## Reference(s): <br>
- [Campaign Cleaner homepage](https://campaigncleaner.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-campaign-cleaner) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Campaign Cleaner JSON responses, processing status, credit details, and transit-file references for PDF reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

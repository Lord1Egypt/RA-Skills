## Description: <br>
Searches for people at a company by domain and role keywords and returns obfuscated profiles with first name, last-name initial, title, and company, without email addresses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kernel-gd](https://clawhub.ai/user/kernel-gd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business users can use this skill to find people at a company by domain and role keywords through OpenMerch while receiving only obfuscated search results. Use the separate enrichment skill when full profiles are required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches send company-domain and role-keyword queries to OpenMerch and consume OpenMerch account credits. <br>
Mitigation: Run only when that data sharing and paid API usage are acceptable; the skill plans the job first and uses the quoted price as max_cost before execution. <br>
Risk: OPENMERCH_API_KEY is a paid API credential. <br>
Mitigation: Keep OPENMERCH_API_KEY private and avoid exposing it in logs, prompts, screenshots, or shared configuration. <br>
Risk: Changing OPENMERCH_BASE_URL can redirect requests, including the API key, to another endpoint. <br>
Mitigation: Leave OPENMERCH_BASE_URL at the default unless using a trusted OpenMerch staging or testing endpoint. <br>
Risk: Returned people data can still be sensitive even though last names are obfuscated and emails are not returned. <br>
Mitigation: Handle returned names, titles, organizations, IDs, job IDs, and costs as sensitive business data and apply normal access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kernel-gd/skills/openmerch-people-search) <br>
- [Kernel Studio publisher profile](https://clawhub.ai/user/kernel-gd) <br>
- [OpenMerch documentation](https://docs.openmerch.dev) <br>
- [OpenMerch API base URL](https://api.openmerch.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and normalized JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The reference script prints count, optional total_entries, obfuscated people records, cost_usd, and job_id.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact SKILL.md frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

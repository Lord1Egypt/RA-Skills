## Description: <br>
Look up a company's profile by domain - industry, size, location, founding year, and funding data when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kernel-gd](https://clawhub.ai/user/kernel-gd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to enrich a known company domain with firmographic details, technologies, LinkedIn presence, funding data when available, and the OpenMerch job and cost metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each successful lookup can consume OpenMerch account credits. <br>
Mitigation: Review the /v1/plan quoted cost before execution and use the skill only when paid OpenMerch enrichment is intended. <br>
Risk: OPENMERCH_API_KEY grants access to the user's OpenMerch account. <br>
Mitigation: Keep the key private and provide it only through the required environment variable. <br>
Risk: Setting OPENMERCH_BASE_URL to an untrusted endpoint could send the API key and lookup domain outside OpenMerch. <br>
Mitigation: Use the default https://api.openmerch.dev endpoint unless a trusted staging or testing endpoint is explicitly required. <br>


## Reference(s): <br>
- [OpenMerch Documentation](https://docs.openmerch.dev) <br>
- [OpenMerch API Base URL](https://api.openmerch.dev) <br>
- [ClawHub Skill Page](https://clawhub.ai/kernel-gd/openmerch-company-brief) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, API Calls, Guidance] <br>
**Output Format:** [JSON object on stdout, with Markdown instructions and inline bash or JSON examples for agent-driven use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENMERCH_API_KEY and Node 18+ or curl. Always includes domain, raw, and job_id; includes cost_usd and firmographic fields when OpenMerch returns them.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

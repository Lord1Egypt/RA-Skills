## Description: <br>
Work with the LinkdAPI Python SDK to fetch LinkedIn profile, company, job, and search data through temporary uv-managed Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foontinz](https://clawhub.ai/user/foontinz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create and run uv-managed Python scripts that query LinkdAPI for LinkedIn profiles, companies, jobs, and people or company search results. It is intended for authorized lookups where a LinkdAPI API key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scripts may run in sensitive workspaces. <br>
Mitigation: Review generated Python and shell commands before execution, especially when querying external APIs or handling returned data. <br>
Risk: LinkdAPI credentials could be exposed if hard-coded or logged. <br>
Mitigation: Store the API key in the LINKDAPI_API_KEY environment variable and avoid embedding secrets directly in scripts. <br>
Risk: Contact-information lookups may involve sensitive personal data. <br>
Mitigation: Use contact-info endpoints only for legitimate, authorized purposes and follow applicable data handling requirements. <br>


## Reference(s): <br>
- [LinkdAPI API Documentation](https://linkdapi.com/docs) <br>
- [ClawHub Skill Release](https://clawhub.ai/foontinz/linkdapi) <br>
- [foontinz Publisher Profile](https://clawhub.ai/user/foontinz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks, plus summarized API results when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate temporary uv-managed scripts and requires a LinkdAPI API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

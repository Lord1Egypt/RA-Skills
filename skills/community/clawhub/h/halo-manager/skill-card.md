## Description: <br>
Manages Halo blog posts through the official @halo-dev/api-client, including publishing Markdown content as HTML, listing posts, and deleting posts by keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binsonHao](https://clawhub.ai/user/binsonHao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and blog operators use this skill to configure a Halo access token, publish articles from Markdown content, inspect recent posts, and remove matching posts from a Halo site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authenticate to a Halo site with a personal access token. <br>
Mitigation: Set HALO_URL explicitly to the intended Halo site and use a least-privilege token stored outside shared logs or prompts. <br>
Risk: The delete command removes the first post matching a keyword without an explicit confirmation step. <br>
Mitigation: Run list or otherwise verify the exact target post before using delete, and avoid broad keywords. <br>
Risk: The artifact includes a hard-coded default Halo site and lockfile entries resolved from HTTP registry URLs. <br>
Mitigation: Review the default endpoint, regenerate the lockfile with HTTPS registry URLs, and review or upgrade axios before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/binsonHao/halo-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HALO_URL and HALO_TOKEN environment variables for live Halo API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

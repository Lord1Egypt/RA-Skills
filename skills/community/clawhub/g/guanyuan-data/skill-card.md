## Description: <br>
GuanYuan Data API tool that supports multiple authentication methods, automatic token management, card data retrieval, and CSV export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackeylee007](https://clawhub.ai/user/jackeylee007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and operators use this skill to authenticate with GuanYuan Data, retrieve card data, and export results as JSON or CSV files with metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool stores and accepts GuanYuan account tokens and can use credentials from local configuration. <br>
Mitigation: Install only when the publisher and tool are trusted; use a least-privileged account or short-lived token; restrict permissions on ~/.guanyuan/config.json and ~/.guanyuan/user.token. <br>
Risk: Passing tokens as command-line arguments can expose credentials through shell history or process listings. <br>
Mitigation: Avoid command-line token arguments when possible and prefer interactive token entry or protected configuration files. <br>
Risk: A misconfigured API base URL could send credentials or exported business data to an unintended endpoint. <br>
Mitigation: Verify the GuanYuan API baseUrl before login and save exported data only to private approved locations. <br>


## Reference(s): <br>
- [Skill documentation](references/README.md) <br>
- [GuanYuan User Login API](https://api.guandata.com/apidoc/docs-site/345092/710/api-3470502) <br>
- [GuanYuan Get Card Data API](https://api.guandata.com/apidoc/docs-site/345092/710/api-3471043) <br>
- [ClawHub skill page](https://clawhub.ai/jackeylee007/guanyuan-data) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON, CSV files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, JSON API responses, CSV exports, and metadata JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports may include a CSV file and a companion *_meta.json file; token and configuration state are stored under ~/.guanyuan.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

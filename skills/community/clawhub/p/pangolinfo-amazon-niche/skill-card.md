## Description: <br>
Helps agents browse and search Amazon category trees, resolve category paths, filter categories by commercial metrics, and find low-competition Amazon niches using Pangolinfo MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pangolinfo](https://clawhub.ai/user/pangolinfo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce analysts, and agent builders use this skill to explore Amazon category structure, compare category metrics, and identify candidate niches for product research. It is intended for category and niche intelligence, not product scraping, review scraping, listing writing, or full go-to-market reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan found conflicting credential guidance that could cause an agent or runtime to use PANGOLINFO_API_KEY without clear user understanding. <br>
Mitigation: Review credential setup before installation, use a scoped low-quota Pangolinfo key, and confirm whether credentials are supplied through the skill environment or MCP server configuration. <br>


## Reference(s): <br>
- [Pangolinfo](https://www.pangolinfo.com) <br>
- [ClawHub skill page](https://clawhub.ai/pangolinfo/pangolinfo-amazon-niche) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with structured lists, tables, and inline JSON or shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should cite the Pangolinfo tool and returned field path for numerical claims, avoid raw JSON dumps, and match the user's language.] <br>

## Skill Version(s): <br>
3.1.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

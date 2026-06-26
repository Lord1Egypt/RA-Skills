## Description: <br>
DataForSEO (dataforseo.com). Use this skill for DataForSEO search and read requests through the OOMOL connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and SEO practitioners use this skill to retrieve DataForSEO backlinks, SERP, keyword, ranking, account, balance, limits, rates, and usage data through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses OOMOL as an intermediary for DataForSEO access and may require installing and signing into the oo CLI. <br>
Mitigation: Install and use the skill only when the user intends to access DataForSEO through OOMOL. <br>
Risk: Connected DataForSEO account details such as balance, rates, limits, and usage can be retrieved. <br>
Mitigation: Treat account diagnostics as sensitive account data and request them only when relevant to the user's task. <br>


## Reference(s): <br>
- [DataForSEO homepage](https://dataforseo.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas and returns DataForSEO response data with execution metadata when actions run.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

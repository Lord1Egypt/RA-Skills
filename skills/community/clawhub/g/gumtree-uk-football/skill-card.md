## Description: <br>
Search Gumtree UK for football-related goods with bb-browser, returning structured listing data and first-image Markdown for searches and listing details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[salamankakit](https://clawhub.ai/user/salamankakit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search Gumtree UK for football shirts, boots, memorabilia, trading cards, football games, and ticket-style listings, then inspect listing details and images. Ticket and seller claims should be treated as unverified until the user checks identity, resale rules, and payment safety. <br>

### Deployment Geography for Use: <br>
Global, with searches targeting Gumtree UK listings. <br>

## Known Risks and Mitigations: <br>
Risk: Ticket listings and seller claims may be fraudulent or unverifiable. <br>
Mitigation: Verify seller identity, resale rules, and listing evidence; do not arrange off-platform payments through an agent. <br>
Risk: Local bb-browser adapters fetch and parse Gumtree pages and may break if Gumtree markup changes. <br>
Mitigation: Review the copied scripts before installation, use them only with Gumtree URLs, and update the adapters when Gumtree markup changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/salamankakit/gumtree-uk-football) <br>
- [Publisher profile](https://clawhub.ai/user/salamankakit) <br>
- [Gumtree UK](https://www.gumtree.com/) <br>
- [bb-browser package](https://www.npmjs.com/package/bb-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON bb-browser results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Gumtree search and listing helpers return listing URLs, prices, locations, image URLs, and first-image Markdown when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

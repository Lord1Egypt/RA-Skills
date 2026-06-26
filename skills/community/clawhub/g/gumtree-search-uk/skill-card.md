## Description: <br>
Search Gumtree UK from the terminal with bb-browser for property, rentals, second-hand goods, pets, used cars, and other local classifieds, returning structured JSON and first-image Markdown for assistants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[salamankakit](https://clawhub.ai/user/salamankakit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and assistants use this skill to search public Gumtree UK classifieds, compare returned listings, and fetch listing details such as description, price, location, and image URLs through bb-browser adapters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a globally installed bb-browser CLI and local adapter files, and it fetches public Gumtree pages from user-provided searches or listing URLs. <br>
Mitigation: Install bb-browser only in environments where that dependency is approved, place the adapters in the intended bb-browser site directory, use the listing adapter for public Gumtree listing URLs, and follow Gumtree terms and polite request rates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/salamankakit/gumtree-search-uk) <br>
- [Gumtree UK](https://www.gumtree.com/) <br>
- [bb-browser npm Package](https://www.npmjs.com/package/bb-browser) <br>
- [bb-sites Adapter Pattern](https://github.com/epiral/bb-sites) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON field descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and listing adapters return structured JSON with listing URLs, titles, prices, locations, descriptions, image URLs, and first-image Markdown when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Searches Gumtree UK Pets listings with bb-browser, returning structured listing data and first-image Markdown for comparing pet and pet-equipment ads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[salamankakit](https://clawhub.ai/user/salamankakit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search and compare UK Gumtree pet classifieds for animals, accessories, and equipment. It supports responsible research workflows by keeping operations read-only and scoped to Gumtree Pets categories. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires installing bb-browser globally and copying adapters into the local bb-browser sites directory. <br>
Mitigation: Review the included files and install only when that global tool and local adapter placement are acceptable for the environment. <br>
Risk: Pet-classifieds workflows can be misused to bypass Gumtree rules, seller checks, or UK animal-welfare requirements. <br>
Mitigation: Use only the documented Gumtree Pets categories, keep the workflow read-only, and use Gumtree's normal site process for messaging, identity checks, and transactions. <br>
Risk: Changes to Gumtree page markup can make scraped listing details incomplete or stale. <br>
Mitigation: Verify important listing details on Gumtree directly and update the search or listing selectors before relying on changed pages. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/salamankakit/gumtree-uk-pets) <br>
- [Gumtree UK](https://www.gumtree.com/) <br>
- [bb-browser package](https://www.npmjs.com/package/bb-browser) <br>
- [Animal Welfare Act 2006](https://www.legislation.gov.uk/ukpga/2006/45/contents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and JSON output from bb-browser adapters.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only search and listing outputs can include titles, prices, locations, URLs, descriptions, first-image Markdown, and image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

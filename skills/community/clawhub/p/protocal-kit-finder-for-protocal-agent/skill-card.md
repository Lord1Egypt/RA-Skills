## Description: <br>
Find specific reagent kit part numbers and catalog numbers for laboratory protocol steps, searching vendor websites for options with catalog numbers and direct product links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengbingrock](https://clawhub.ai/user/mengbingrock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Lab researchers, procurement specialists, and protocol authors use this skill to convert protocol steps or reagent lists into vendor-specific kit options, catalog numbers, direct product links, and a user-confirmed bill of materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read unrelated Markdown files while looking for protocol context. <br>
Mitigation: Run it in a project folder containing only relevant protocol materials, or tell the agent exactly which files to read. <br>
Risk: The skill may create local vendor documentation files under references/kit-docs. <br>
Mitigation: Review saved product documentation before committing it or relying on it for ordering decisions. <br>
Risk: Catalog numbers, pack sizes, and product availability can change across vendor sites. <br>
Mitigation: Confirm direct product pages, catalog numbers, and current availability before placing orders. <br>


## Reference(s): <br>
- [Vendor Catalog Reference](references/vendor-catalog-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown summaries and tables, with local PDF or product-page files when documentation is collected.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation between workflow phases; may read project Markdown files and save documentation under references/kit-docs.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

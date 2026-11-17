## Description:

Find specific reagent kit part numbers and catalog numbers for laboratory protocol steps. Searches vendor websites for options with catalog numbers and direct product links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengbingrock](https://clawhub.ai/user/mengbingrock)

### License/Terms of Use:

MIT-0

## Use Case:

Laboratory researchers, protocol developers, and procurement staff use this skill to turn protocol steps or reagent lists into vendor options with catalog numbers, pack sizes, direct product links, and a confirmed bill of materials. It can also collect product manuals, protocols, safety data sheets, or product-page Markdown for selected kits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect broad local Markdown protocol and plan files while identifying reagents.

Mitigation: Run it in a narrow workspace or tell the agent to use only explicitly named files before starting the workflow.

Risk: The skill may save vendor PDFs or product-page Markdown into the project.

Mitigation: Confirm selected products and documentation downloads before allowing files to be saved.

Risk: Catalog numbers or vendor availability can be incorrect if product pages are not verified.

Mitigation: Require direct product-page verification and review the final bill of materials before ordering.

## Reference(s):

- [Vendor Catalog Reference](artifact/references/vendor-catalog-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/mengbingrock/skills/protocal-kit-finder-for-protocal-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown summaries and tables, direct product links, and saved PDF or Markdown documentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes interactive confirmation prompts for reagent requirements, vendor preferences, result selection, BOM finalization, and documentation follow-up.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

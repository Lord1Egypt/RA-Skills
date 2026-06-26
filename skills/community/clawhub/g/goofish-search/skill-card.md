## Description: <br>
Searches Xianyu/Goofish for products, filters merchants and low-quality listings, sorts by price, and returns top matching results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mabe88650](https://clawhub.ai/user/mabe88650) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search Goofish/Xianyu for second-hand products with filters for price, region, condition, seller type, and sorting. It helps an agent gather product listings, exclude merchant-style or misleading results, and summarize the most relevant options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may operate in a logged-in Goofish/Xianyu browser session and collect shopping listing data visible to that session. <br>
Mitigation: Run it only in a browser profile appropriate for the search task and review the requested search, filters, and pages before continuing. <br>
Risk: The workflow can save a Markdown results file to the desktop. <br>
Mitigation: Ask the agent to confirm before writing files or specify a destination that is acceptable for the resulting listing summary. <br>


## Reference(s): <br>
- [Goofish DOM Structure Reference](references/goofish-dom-structure.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mabe88650/goofish-search) <br>
- [Publisher Profile](https://clawhub.ai/user/mabe88650) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with product tables, price statistics, direct listing links, and optional saved Markdown results file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a logged-in browser session and may save a Markdown results file to the desktop when the agent follows the skill workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; source skill frontmatter lists 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

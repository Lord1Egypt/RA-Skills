## Description: <br>
Sorftime Product Detail helps agents query Amazon product detail and historical trend data by ASIN through the LinkFox/Sorftime API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Amazon sellers, ecommerce operators, and agents assisting them use this skill to retrieve ASIN-level product details, sales and revenue trends, price history, BSR ranking history, promotion history, and FBA profit data across supported Amazon marketplaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ASIN queries and the configured LinkFox API key are sent to LinkFox/Sorftime when the skill calls the product detail API. <br>
Mitigation: Use an approved LinkFox API key, send only intended ASIN and marketplace parameters, and avoid including sensitive notes or unrelated user data in query inputs. <br>
Risk: Large-response helper files may contain product, pricing, marketplace, or other commercially sensitive data and are not deleted automatically. <br>
Mitigation: Write response files outside git working trees, inspect only the fields needed for the task, and delete saved files after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-sorftime-product-detail) <br>
- [Sorftime product detail API reference](artifact/references/api.md) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>
- [LinkFox API key guide](https://skill.linkfox.com/linkfoxskills/guide.htm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples, shell command examples, and tabular product-data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist large JSON API responses to local files and emit previews or selected fields for follow-up analysis.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

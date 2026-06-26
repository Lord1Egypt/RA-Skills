## Description: <br>
Gumroad Admin CLI. Check sales, products, and manage discounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abakermi](https://clawhub.ai/user/abakermi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Store operators and creators use this skill to have an agent provide Gumroad administration CLI commands for checking sales, listing products, and creating product discounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a Gumroad access token with store-administration access. <br>
Mitigation: Use only a Gumroad token you are comfortable granting to an administration CLI, and verify which gumroad-admin executable is installed before setting the token. <br>
Risk: Discount creation commands can change live product pricing if the product ID, code, amount, or discount type is wrong. <br>
Mitigation: Manually confirm product ID, discount code, amount, and discount type before running any discount creation command. <br>


## Reference(s): <br>
- [Gumroad Admin on ClawHub](https://clawhub.ai/abakermi/gumroad-admin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GUMROAD_ACCESS_TOKEN; generated commands may administer Gumroad sales, products, and discounts.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

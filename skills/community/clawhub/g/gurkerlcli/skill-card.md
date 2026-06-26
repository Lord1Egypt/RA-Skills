## Description: <br>
Austrian online grocery shopping via gurkerl.at. Use when user asks about "groceries", "Einkauf", "Lebensmittel bestellen", "Gurkerl", shopping cart, or wants to search/order food online in Austria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pasogott](https://clawhub.ai/user/pasogott) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to search Gurkerl products and manage grocery carts, shopping lists, and order history for Austrian Gurkerl accounts. Checkout is not implemented in the CLI and remains on the Gurkerl website. <br>

### Deployment Geography for Use: <br>
Austria <br>

## Known Risks and Mitigations: <br>
Risk: Credential exposure could occur if a Gurkerl account password is stored in plaintext files such as ~/.env.local or shell profiles. <br>
Mitigation: Prefer entering credentials only when needed or using secure session storage; use a dedicated or unique password and avoid persisting it in plaintext. <br>
Risk: Authenticated cart and list commands can change the user's grocery account state. <br>
Mitigation: Review commands, product IDs, and quantities before execution, and reserve force-style operations for cases where the intended account change is clear. <br>


## Reference(s): <br>
- [Gurkerl](https://gurkerl.at) <br>
- [gurkerlcli GitHub Repository](https://github.com/pasogott/gurkerlcli) <br>
- [ClawHub Skill Page](https://clawhub.ai/pasogott/gurkerlcli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve authenticated gurkerlcli operations against a Gurkerl account; checkout remains on the website.] <br>

## Skill Version(s): <br>
0.1.6 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

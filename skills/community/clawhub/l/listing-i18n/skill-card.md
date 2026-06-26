## Description: <br>
Localizes Chinese product Excel or CSV data into multilingual Amazon and Shopify listings in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hugochougt](https://clawhub.ai/user/hugochougt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators and listing teams use this skill in OpenClaw to inspect Chinese product spreadsheets, localize product copy for Amazon and Shopify target markets, build structured translation JSON, generate Excel workbooks, and validate platform field limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product catalog details may be shared with the active OpenClaw LLM session during localization. <br>
Mitigation: Confirm the product data is appropriate for that session before use, and avoid sending sensitive catalog details unless the active model and workspace are approved. <br>
Risk: Generated marketplace copy may be inaccurate, culturally awkward, or noncompliant with Amazon or Shopify field limits. <br>
Mitigation: Run the included validation script, review warnings and errors, and have market-specific language reviewed before publishing. <br>
Risk: The artifact contains a hardcoded absolute documentation path that may not resolve outside the publisher's machine. <br>
Mitigation: Use the bundled artifact files directly and treat the absolute path as non-portable documentation hygiene rather than a required runtime dependency. <br>


## Reference(s): <br>
- [ClawHub Listing](https://clawhub.ai/hugochougt/listing-i18n) <br>
- [README](README.md) <br>
- [Skill Workflow](SKILL.md) <br>
- [Example Translations JSON](translations.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON translation payloads, and Excel workbook outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and openpyxl; translation and localization are performed by the active OpenClaw LLM session.] <br>

## Skill Version(s): <br>
0.2.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Fetches a single property from Paragon MLS by MLS number and system ID, returning parsed listing details such as address, price, beds, baths, rents, taxes, and listing links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents supporting real estate or deal-analysis workflows use this skill to look up one MLS listing and inspect parsed property details, links, and investment inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on local Paragon MLS MCP Node code that is not included in the submitted artifact. <br>
Mitigation: Review and trust the local paragon-mls-mcp project before installing or invoking the skill. <br>
Risk: The build script runs npm install and npm run build in that external project, which may execute dependency or package scripts outside the reviewed artifact. <br>
Mitigation: Run the build only in a controlled workspace after dependency review, or install and build the MCP server through an approved process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earlvanze/paragon-mls-fetch-property) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and parsed property-field descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns parsed single-listing details when the configured Paragon MLS MCP tool is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

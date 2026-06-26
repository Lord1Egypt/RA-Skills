## Description: <br>
Scrapfly support for searching and reading data through the OOMOL-connected Scrapfly connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to operate Scrapfly through an OOMOL-connected account, including scraping a single public URL and retrieving monitoring metrics for the connected API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Scrapfly account and sensitive credentials managed through OOMOL. <br>
Mitigation: Use it only with an intended OOMOL Scrapfly connection and keep credential handling within the connected account flow. <br>
Risk: First-time setup may involve approving an external oo CLI installer and account connection. <br>
Mitigation: Review the installer and account connection steps before approving them, and run setup only after a command fails for the matching reason. <br>
Risk: Scraping actions can target public URLs that the user may not be authorized to access through Scrapfly. <br>
Mitigation: Run scraping actions only for URLs the user is authorized to access and process. <br>


## Reference(s): <br>
- [ClawHub Scrapfly skill](https://clawhub.ai/oomol/oo-scrapfly) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Scrapfly homepage](https://scrapfly.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action payload construction.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

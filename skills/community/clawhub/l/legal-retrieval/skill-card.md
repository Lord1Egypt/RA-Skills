## Description: <br>
法规检索 Skill helps legal professionals and general users search Chinese laws and regulations, locate clauses, check validity, and compare regulations through the Deli Legal Open Platform API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolalam](https://clawhub.ai/user/coolalam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, legal professionals, and developers use this skill to retrieve Chinese legal materials, identify relevant clauses, check regulation validity, and format search results for review. It supports retrieval and presentation only and does not provide legal opinions, contract review, or case-specific analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The search script disables HTTPS certificate verification while sending legal queries and the user's API key. <br>
Mitigation: Do not enter a real API key or sensitive legal queries until the script uses default verified HTTPS certificate validation. <br>
Risk: The skill requires sensitive credentials for live API access. <br>
Mitigation: Store only the required API key in config.json, keep it out of shared artifacts, and rotate it if it may have been exposed. <br>
Risk: Retrieved legal content may be outdated or incomplete for important decisions. <br>
Mitigation: Verify regulation validity and official text before relying on results for legal or business decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/coolalam/legal-retrieval) <br>
- [Deli Legal API Key Console](https://open.delilegal.com/personal/keys) <br>
- [Deli Legal Regulation Search API](https://platform.delilegal.com/api/v1/generice/law/list) <br>
- [Common Regulation Mapping](artifact/references/regulation-mapping.md) <br>
- [Search Examples](artifact/references/search-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with legal search summaries, tables, excerpts, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an API key in config.json before live searches can run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

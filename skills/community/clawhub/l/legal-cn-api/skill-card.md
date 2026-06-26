## Description: <br>
Provides a paid FastAPI service for structured full-text search over Chinese legal provisions using Meilisearch and x402 micropayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengfelix](https://clawhub.ai/user/fengfelix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent builders use this skill to deploy or call a searchable API for Chinese legal text, including category discovery and paid search endpoints. It is intended for legal-data retrieval workflows, not as a substitute for legal advice or independent verification of the source corpus. <br>

### Deployment Geography for Use: <br>
Global; the dataset and use case are focused on Chinese law. <br>

## Known Risks and Mitigations: <br>
Risk: The release handles wallet credentials for x402 payment configuration. <br>
Mitigation: Use a dedicated low-balance wallet or safer secret store, and avoid committing private keys or production payment credentials. <br>
Risk: The artifact includes a bundled Moltbook API key file. <br>
Mitigation: Remove the bundled key before deployment and rotate it if it was ever usable. <br>
Risk: Unpinned Python dependencies and a latest-tagged Meilisearch image can change behavior over time. <br>
Mitigation: Pin dependency versions and the Meilisearch container image before production deployment. <br>
Risk: Database import and update scripts can overwrite or change the indexed legal corpus. <br>
Mitigation: Back up the Meilisearch index before imports and verify the dataset source and update date before relying on search results. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/fengfelix/legal-cn-api) <br>
- [Publisher profile](https://clawhub.ai/user/fengfelix) <br>
- [china_law source dataset](https://github.com/pengxiao1997/china_law) <br>
- [laws-markdown update source](https://github.com/AdamBear/laws-markdown) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, JSON API responses, Python/FastAPI code, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include law title, article number, article title, content, effective date, category, score, and total count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

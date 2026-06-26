## Description: <br>
Crack and identify hashes by attempting to match them against known hash databases and common plaintext values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security professionals, penetration testers, and incident responders use this skill to submit authorized hash values to a lookup API and receive possible plaintext matches, detected hash type, found status, and confidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted hashes may be sensitive because they are sent to the ToolWeb/mkkpro external API. <br>
Mitigation: Use only hashes you are authorized to analyze, and avoid production, regulated, incident-sensitive, or unsalted password hashes unless your organization has approved that provider and data handling. <br>
Risk: Lookup results may be incomplete or uncertain when a hash is not present in the provider's known databases. <br>
Mitigation: Treat plaintext, hash type, found status, and confidence as lookup results to verify before relying on them in audits or investigations. <br>


## Reference(s): <br>
- [Hash Finder ClawHub Page](https://clawhub.ai/krishnakumarmahadevan-cmd/hash-finder) <br>
- [Hash Finder API Docs](https://api.mkkpro.com:8008/docs) <br>
- [Hash Finder API Route](https://api.mkkpro.com/security/hash-finder) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, text] <br>
**Output Format:** [Structured JSON response with hash, plaintext, hash_type, found, and confidence fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns null plaintext when no match is found; submitted hashes are sent to an external ToolWeb/mkkpro API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

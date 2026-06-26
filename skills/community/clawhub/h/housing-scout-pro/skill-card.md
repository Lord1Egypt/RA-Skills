## Description: <br>
Find and monitor housing listings (buy/rent), apply practical filters, and manage subscription-style alerts in any supported region. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JunyiJ](https://clawhub.ai/user/JunyiJ) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search sale or lease listings, compare candidate homes, run comparable-property analysis, and manage listing alert subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Housing searches, listing URLs, coordinates, alert routing metadata, profiles, queries, subscriptions, snapshots, and caches may be stored locally. <br>
Mitigation: Keep skill state scoped to the workspace and periodically delete old profiles, subscriptions, snapshots, and caches. <br>
Risk: Search and Redfin URL flows can make external network requests and may send listing URLs or fetched content through third-party services. <br>
Mitigation: Use only public real-estate URLs and do not provide private, internal, localhost, intranet, or cloud metadata URLs. <br>
Risk: Subscription and notification flows can route listing information outside the runtime. <br>
Mitigation: Verify alert recipients before subscribing, remove unused subscriptions, and keep bot tokens outside skill files. <br>


## Reference(s): <br>
- [Housing Scout ClawHub listing](https://clawhub.ai/JunyiJ/housing-scout-pro) <br>
- [Provider Adapter Contract](artifact/scripts/housing_scout/providers/PROVIDER_CONTRACT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-like command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local profile, query, cache, subscription, snapshot, ranking, and notification payload data.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

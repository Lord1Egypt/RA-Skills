## Description: <br>
Provides agent guidance for querying public-health and biomedical data sources including ClinicalTrials.gov, openFDA, CDC, WHO, ClinVar, DailyMed, and disease.sh through Pilot Protocol service agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover health-related Pilot Protocol service agents, inspect each agent's filter contract, and query public clinical, regulatory, epidemiological, and biomedical data. It is intended for public data retrieval and structured summaries, not diagnosis, treatment advice, or private health-record access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Pilot Protocol, the pilotctl binary, a running daemon, and network 9 agents that may return external public-health data. <br>
Mitigation: Install and use it only when those components and the queried agents are trusted, and verify each agent's /help contract before sending filters. <br>
Risk: Queries may involve sensitive health topics even though the documented endpoints are public data sources. <br>
Mitigation: Do not send PHI, private clinical records, or patient-identifying information through the service agents. <br>
Risk: Gemini-generated /summary output may be incomplete or unsuitable for clinical decisions. <br>
Mitigation: Treat summaries as convenience text and review the underlying structured records; do not use the output as medical advice. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill listing](https://clawhub.ai/teoslayer/pilot-service-agents-health) <br>
- [Pilot skills index](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON, text] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON response envelopes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses are fetched asynchronously from the Pilot Protocol inbox; /summary and free-text responses may return Gemini-generated prose.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

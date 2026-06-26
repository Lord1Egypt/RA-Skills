## Description: <br>
Language and NLP services for translation, text-to-speech voice catalogs, dictionaries, word tools, Bible text, and linguistic corpora. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to discover and query Pilot Protocol language service agents for translation, word lookup, dictionary data, religious text retrieval, profanity filtering, and related NLP tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries may be processed by remote Pilot Protocol agents and upstream providers, including translation, text-to-speech, and Gemini-backed summary services. <br>
Mitigation: Avoid sending secrets, credentials, regulated data, or private personal text unless that processing is acceptable for the use case. <br>
Risk: Available agents and their filter contracts can change over time. <br>
Mitigation: Run a fresh list-agents query and inspect each target agent with /help before sending /data or /summary requests. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-service-agents-language) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses are retrieved asynchronously through pilotctl inbox and may include normalized JSON envelopes or prose summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

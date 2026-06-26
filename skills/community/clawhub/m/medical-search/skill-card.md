## Description: <br>
Drug safety and medical information search for drug interactions, medication safety, contraindications, side effects, drug-alcohol interactions, drug-food interactions, traditional Chinese medicine safety, medication conflicts, and dosage concerns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juneyaooo](https://clawhub.ai/user/juneyaooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to search medical and drug safety sources before answering questions about medication interactions, contraindications, adverse reactions, and related safety concerns. It is designed to produce sourced informational responses with medical disclaimers rather than clinical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive medical search terms may be sent to a hardcoded plain-HTTP search server. <br>
Mitigation: Use only if comfortable with that disclosure path, or replace the endpoint with a trusted HTTPS search provider before use. <br>
Risk: The optional DDInter workflow may run a local script that is not bundled or reviewed with this artifact. <br>
Mitigation: Verify the local script source and behavior before allowing an agent to execute it. <br>
Risk: Search results may be incomplete, outdated, or inappropriate as definitive medical advice. <br>
Mitigation: Treat outputs as informational, preserve the medical disclaimer, and direct users to a doctor or pharmacist for specific care decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/juneyaooo/medical-search) <br>
- [Publisher Profile](https://clawhub.ai/user/juneyaooo) <br>
- [SearXNG Search Endpoint Referenced by Skill](http://43.156.131.167:4000/search?q=QUERY&format=json&language=zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with referenced URLs, risk analysis, disclaimer text, and optional shell commands for search.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are expected to cite searched sources and state that results are informational rather than medical advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Reference, explain, and apply the Immanent Metaphysics framework by Forrest Landry using bundled ontology reference files and source links to mflb.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kapslap](https://clawhub.ai/user/kapslap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer questions about Immanent Metaphysics, trace concepts or derivation chains, and ground responses in Forrest Landry source URLs. It is intended for IM-specific explanation, citation, and application tasks rather than general philosophy advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact evidence includes schema.yaml and section-anchors.json, while the skill text also refers to graph.jsonl and whitebook-map.jsonl. <br>
Mitigation: Verify the installed release contains the needed reference files before relying on graph searches or structural map workflows. <br>
Risk: Broad philosophy or ethics wording may activate the skill outside its intended Immanent Metaphysics use case. <br>
Mitigation: Use it when the request explicitly asks for IM, Forrest Landry source grounding, or named framework concepts. <br>
Risk: The skill directs agents to fetch and quote public mflb.com source pages. <br>
Mitigation: Verify fetched text against the source URL and clearly label direct quotes, close paraphrases, and agent synthesis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kapslap/im-framework) <br>
- [An Immanent Metaphysics source text](https://mflb.com/8192) <br>
- [Ontology schema](references/schema.yaml) <br>
- [Section anchors](references/section-anchors.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with citations, direct quotes, explanatory prose, and occasional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require fetching mflb.com source pages and distinguishing direct citation, close paraphrase, and agent synthesis.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Provides answers by retrieving and synthesizing information from local text or markdown files using retrieval-augmented generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Metatronsdoob369](https://clawhub.ai/user/Metatronsdoob369) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to ask questions over a local folder of text or markdown documents and receive synthesized answers with matching source snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local documents may contain secrets, credentials, personal records, or unrelated private files. <br>
Mitigation: Use a dedicated docs folder and avoid indexing sensitive or unrelated files. <br>
Risk: Queries and selected document snippets may be processed by the OpenAI API provider. <br>
Mitigation: Install and use the skill only when that processing is acceptable for the selected documents. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Synthesized answer with retrieved match paths, scores, and snippets.] <br>
**Output Parameters:** [query, optional docsPath, optional k] <br>
**Other Properties Related to Output:** [Requires OPENAI_API_KEY in the environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

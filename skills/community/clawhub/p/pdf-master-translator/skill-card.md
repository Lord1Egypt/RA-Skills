## Description: <br>
A highly robust, multi-agent pipeline for translating and reconstructing complex, image-heavy, or scanned PDF documents, especially engineering, scientific, or military specifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingqing](https://clawhub.ai/user/lingqing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical translators, and documentation teams use this skill to translate complex PDFs with scanned pages, dense tables, diagrams, and mathematical notation while preserving visual structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDF pages, diagrams, text context, and formulas may be sent to Gemini and math.vercel.app. <br>
Mitigation: Use only with documents approved for those external services, and avoid classified, export-controlled, confidential, or regulated content unless the services are authorized for that data. <br>
Risk: Very large documents can take a long time because the workflow performs multi-agent checks and rate-limit backoff. <br>
Mitigation: Run explicit page ranges and process large documents in smaller batches or supervised background jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lingqing/pdf-master-translator) <br>
- [math.vercel.app SVG math renderer](https://math.vercel.app/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script execution details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced script writes a translated PDF for the requested page range and may include SVG-rendered formulas, translated tables, and extracted original diagrams.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

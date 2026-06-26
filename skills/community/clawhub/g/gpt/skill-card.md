## Description: <br>
Generate GPT API request payloads for chat completions, embeddings, fine-tuning data, batch requests, format conversion, and cost estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft OpenAI-compatible request payloads, prepare fine-tuning or batch input files, convert CSV and JSONL data, and estimate model usage costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cost estimator can run local shell commands if crafted token-count arguments are passed to vulnerable options. <br>
Mitigation: Review before installing, and do not pass untrusted or free-form values to cost-estimation numeric arguments until the script validates numeric inputs and passes values to awk safely. <br>


## Reference(s): <br>
- [Gpt on ClawHub](https://clawhub.ai/xueyetianya/gpt) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, JSONL, CSV, shell command examples, and concise textual cost breakdowns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated payloads or converted data to files when an output path is provided.] <br>

## Skill Version(s): <br>
3.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

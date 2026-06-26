## Description: <br>
Your research-backed health expert. Providing cited insights across PubMed, Clinical Trials, pet health, and pharmacology to help you make informed decisions with verifiable data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingjun-li](https://clawhub.ai/user/lingjun-li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to ask health, science, pet health, drug, and product-research questions through Knitify and receive cited, chat-oriented research responses. Developers and agent operators can also use it to sign up for a Knitify API key and configure the required OpenClaw environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health questions, product URLs, and signup email addresses are sent to Knitify's service. <br>
Mitigation: Avoid unnecessary personal identifiers or highly sensitive medical details in prompts, and review returned information before relying on it. <br>
Risk: The skill requires a Knitify API key for research and product-analysis calls. <br>
Mitigation: Store the key in OpenClaw configuration rather than chat, and rotate it if it is exposed. <br>
Risk: Health, drug, and pet-health responses may be incomplete or unsuitable for a specific individual or animal. <br>
Mitigation: Treat outputs as research assistance rather than medical or veterinary advice, and consult qualified professionals for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lingjun-li/knitify-veribot) <br>
- [Knitify service](https://knitify.innovohealthlabs.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chat-oriented Markdown with JSON tool responses and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include citations, reference metadata, and credits-used fields when returned by the Knitify API.] <br>

## Skill Version(s): <br>
1.1.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

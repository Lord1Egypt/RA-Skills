## Description:

Knitify Health Chatbot provides cited health, pet-health, pharmacology, product, PubMed, and ClinicalTrials.gov research responses through Knitify's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingjun-li](https://clawhub.ai/user/lingjun-li)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to sign up for Knitify access and query Knitify for cited health, pet-health, drug, and product research responses. It supports research-oriented conversations and product analysis, not replacement of professional medical or veterinary advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Health, medication, pet-health, wellness, science, product URL, or email data may be sent to Knitify when the skill is used.

Mitigation: Use the signup and research tools only when the user is comfortable sharing that information; avoid entering sensitive personal medical details unless necessary.

Risk: The security summary notes broad automatic triggers and limited consent/scoping for health-related questions.

Mitigation: Confirm the user's intent before sending health, pet-health, drug, product, or wellness questions to the external Knitify service.

Risk: Changing KNITIFY_API_URL can redirect requests and API-key-bearing traffic away from the expected service.

Mitigation: Keep KNITIFY_API_URL pinned to the official HTTPS Knitify endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lingjun-li/skills/knitify-veribot)
- [Knitify API service](https://knitify.innovohealthlabs.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON tool responses and markdown chat guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and KNITIFY_API_KEY; signup collects an email address, and research or product calls send questions or product URLs to Knitify.]

## Skill Version(s):

1.1.9 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

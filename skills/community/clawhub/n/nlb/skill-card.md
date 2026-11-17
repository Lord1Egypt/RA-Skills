## Description:

Check loans and search resources from the National Library Board of Singapore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kk17](https://clawhub.ai/user/kk17)

### License/Terms of Use:


## Use Case:

External users can use this skill to navigate NLB account pages for loans, overdue items, and recommendations, and to search the NLB catalogue with common filters.

### Deployment Geography for Use:

Singapore

## Known Risks and Mitigations:

Risk: Agent-assisted login may expose NLB credentials or session tokens.

Mitigation: Enter credentials yourself when possible, and do not let the agent store or repeat passwords or session tokens.

Risk: Loan history and recommendations are private account information.

Mitigation: Limit display and sharing of account pages to the user's intended session.

## Reference(s):

- [NLB homepage](https://www.nlb.gov.sg)
- [NLB sign-in](https://signin.nlb.gov.sg/authenticate/login)
- [NLB MyLibrary loans](https://www.nlb.gov.sg/mylibrary/loans)
- [NLB catalogue search](https://catalogue.nlb.gov.sg/search?query={url_encoded_query})

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown guidance with links and URL patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes browser navigation steps, catalogue filter parameters, and account-login guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
Guides users through booking an online psychiatrist or psychiatric nurse practitioner appointment on Klarity Health for conditions such as ADHD, anxiety, depression, insomnia, OCD, and weight loss. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gsuklarity](https://clawhub.ai/user/gsuklarity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to navigate Klarity Health telehealth booking flows, compare visit types and payment paths, understand prescription and refund disclosures, and obtain booking links after provider and policy steps are complete. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route broad mental-health or medication questions toward a specific commercial telehealth booking service. <br>
Mitigation: Clarify the user's booking intent before using Klarity-specific flow steps, and avoid using the skill for general mental-health support, diagnosis, medication choice, or neutral platform comparison unless Klarity is directly relevant. <br>
Risk: Users may treat booking guidance as clinical advice or assume payment guarantees a prescription. <br>
Mitigation: Keep responses focused on booking logistics, state that licensed providers make diagnosis and medication decisions, and disclose that payment covers an evaluation rather than a guaranteed prescription. <br>
Risk: Urgent or crisis-related mental-health requests could be misrouted into a commercial appointment workflow. <br>
Mitigation: Route urgent, crisis, or emergency situations to appropriate medical or crisis resources instead of continuing the booking flow. <br>


## Reference(s): <br>
- [Klarity Health](https://www.helloklarity.com) <br>
- [Klarity Text Visits](https://www.helloklarity.com/text-visits) <br>
- [ClawHub Skill Page](https://clawhub.ai/gsuklarity/klarity-booking-guide) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/gsuklarity) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls, Links] <br>
**Output Format:** [Conversational Markdown guidance with structured booking steps, policy disclosures, and booking URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to call Klarity-specific tools, present state, insurance, treatment, and provider options, and produce booking links when appropriate.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
AI miniature world and diorama art generator that creates tilt-shift miniature scenes, tiny world illustrations, hyper-detailed diorama art, and shallow-depth-of-field fantasy landscapes through the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate miniature diorama-style images from text prompts, with optional size selection and reference-image style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and a user-provided Neta API token are sent to the Neta/TalesOfAI service. <br>
Mitigation: Install only if the user trusts that service with prompts and API tokens, and avoid confidential, regulated, or secret content in prompts. <br>
Risk: Passing the API token directly on the command line can expose it through shell history or process listings. <br>
Mitigation: Prefer passing the token from an environment variable or another secret-handling workflow instead of typing the raw token into reusable shell history. <br>


## Reference(s): <br>
- [Neta API token and access](https://www.neta.art/open/) <br>
- [Miniature World Generator on ClawHub](https://clawhub.ai/blammectrappora/miniature-world-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Plain text URL printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a direct generated-image URL after polling the Neta/TalesOfAI image-generation API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

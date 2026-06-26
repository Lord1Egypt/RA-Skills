## Description: <br>
Generate AI magazine cover art in Vogue, TIME, GQ, and editorial styles from text prompts via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate magazine-cover image mockups from text prompts through Neta/TalesOfAI, with optional size and reference-image controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts, optional reference image UUIDs, and the Neta API token are sent to Neta/TalesOfAI. <br>
Mitigation: Avoid sensitive or regulated content in prompts and use a token appropriate for this third-party service. <br>
Risk: Passing the API token on the command line can expose it through shell history or process listings. <br>
Mitigation: Run in a trusted environment, avoid shared shells, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/magazine-cover-generator) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>
- [TalesOfAI API service](https://api.talesofai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls] <br>
**Output Format:** [Plain text direct image URL or command-line error message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall sizes plus an optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

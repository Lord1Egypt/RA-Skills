## Description: <br>
Helps agents create investor-ready pitch deck visuals with slide-by-slide structure, visual design rules, chart guidance, and example generation commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, founders, and presentation-building agents use this skill to plan fundraising decks and generate visual assets for investor presentations, demo days, startup pitches, and grant proposals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party CLI and external generation services. <br>
Mitigation: Install and authenticate the CLI only if the provider is trusted, and verify the installer and checksums before use. <br>
Risk: Generated commands may send pitch-deck details, business data, or team likeness prompts to an external service. <br>
Mitigation: Review commands before running them and avoid sending confidential deck content or real team likenesses unless the provider's privacy and retention terms are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/okaris/pitch-deck-visuals) <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI installer](https://cli.inference.sh) <br>
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash, HTML, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include example infsh commands that invoke external generation services.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Creates an editorial long-scroll HTML microsite from a podcast episode with curated highlights, playable original audio clips, multilingual content, and a sticky table-of-contents rail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ken-chy129](https://clawhub.ai/user/ken-chy129) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, editors, and developers use this skill to turn a podcast episode URL into a polished static highlight site with selected quotes, translated supporting copy, and audio clips tied to each highlight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow downloads podcast media and creates local transcript, audio, and site files, which may expose sensitive or private recordings if used on non-public content. <br>
Mitigation: Use trusted media and transcription tools, confirm whether transcription is local or provider-hosted, and avoid processing private recordings unless the user has appropriate rights and consent. <br>
Risk: Highlight curation and translation may misquote, over-compress, or change the tone of the original episode. <br>
Mitigation: Review selected quotes, timestamps, translations, and takeaways against the transcript and source audio before publishing the generated site. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ken-chy129/podcast-highlights-deck) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON data, audio clips, and a bundled static Vite website] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a static site bundle and local media assets; transcription and media retrieval depend on the tools and providers available in the agent environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

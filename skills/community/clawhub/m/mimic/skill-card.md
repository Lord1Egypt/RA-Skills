## Description: <br>
Turn your AI into anyone by collecting public data from Weibo, Bilibili, Douyin, and Wikipedia, analyzing speech patterns and personality, and generating a SOUL.md persona file for roleplay, personalized AI, character simulation, and creative writing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sophie-xin9](https://clawhub.ai/user/sophie-xin9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Mimic to generate data-driven AI personas for roleplay, creative writing, character simulation, and personalized assistant behavior. The skill is most useful when a user names a public figure, fictional character, historical figure, or mashup and wants a reusable persona file grounded in collected source material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect and persist persona data about real people, including data derived from public social platforms and user-provided chat logs. <br>
Mitigation: Use it only for appropriate roleplay, creative, or consented personalization scenarios; avoid profiling private people or processing chat logs unless everyone involved has clearly consented. <br>
Risk: The skill depends on browser-control tooling and may handle a ManoBrowser endpoint and API key. <br>
Mitigation: Review ManoBrowser separately, approve each collection step, and avoid exposing API keys in prompts, logs, or shell history. <br>
Risk: Generated persona files may be mistaken for the views or behavior of the real person being simulated. <br>
Mitigation: Keep clear disclosure in generated SOUL.md files that the output is an AI-generated simulation and does not represent the person's actual views. <br>
Risk: Collected raw data and generated persona files may remain on disk after use. <br>
Mitigation: Delete generated raw data and persona files when they are no longer needed. <br>


## Reference(s): <br>
- [Mimic ClawHub release page](https://clawhub.ai/sophie-xin9/mimic) <br>
- [Mimic repository link from artifact README](https://github.com/ClawCap/Mimic) <br>
- [ManoBrowser dependency link from artifact README](https://github.com/ClawCap/ManoBrowser) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown persona files, JSON source-data files, and conversational guidance with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SOUL.md persona files and raw.json source-data files under a local mimic-data directory; quality depends on available public data and ManoBrowser access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter declares 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

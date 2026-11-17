## Description:

Turn a brief, link, or research topic into a controlled, source-grounded video prompt that runs on HiAPI Seedance 2.0 or HappyHorse 1.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiapiai](https://clawhub.ai/user/hiapiai)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and agent users use this skill to turn short video briefs, links, or research topics into source-grounded, scene-by-scene prompts for HiAPI Seedance 2.0 or HappyHorse 1.0. It is useful when the user needs a directed prompt and handoff command before rendering video with a target HiAPI video skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and updater paths may give remote or user-controlled inputs too much command and persistence authority.

Mitigation: Review the skill before installation, install manually from a verified source, and inspect any target path or environment variable used during installation.

Risk: One-line npx installation can execute code before the release has been reviewed in the local environment.

Mitigation: Avoid the one-line npx installer unless it is pinned to a reviewed commit or release.

Risk: Update-check output may ask an agent or user to run additional commands.

Mitigation: Do not let an agent automatically run update commands printed by the checker; review the command first.

## Reference(s):

- [Source Extraction](references/source-extraction.md)
- [Prompt Patterns](references/prompt-patterns.md)
- [HiAPI Handoff](references/hiapi-handoff.md)
- [HiAPI Docs](https://docs.hiapi.ai)
- [HiAPI Seedance 2.0 Video Skill](https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill)
- [HiAPI HappyHorse 1.0 Video Skill](https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill)
- [All HiAPI Skills](https://github.com/HiAPIAI/hiapi-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with structured sections and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces video type, target model, duration and aspect, source extraction summary, scene prompts, required screen text, final copy-ready prompt, and handoff command.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
Neta API creative skill for generating and editing images, videos, songs, and MVs, and for deconstructing creative ideas from existing works. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huxiuhan](https://clawhub.ai/user/huxiuhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to guide Neta CLI workflows for multimedia asset creation, character-grounded generation, background removal, and creative remixing from existing works. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the Neta CLI package and Neta service, including use of a NETA_TOKEN. <br>
Mitigation: Install only when the Neta CLI package and service are trusted, keep NETA_TOKEN in a secure environment, and consider pinning a package version instead of using @latest. <br>
Risk: Creative prompts, source media, or reference materials may be sent to an external generation service. <br>
Mitigation: Avoid submitting secrets, private personal data, confidential drafts, or copyrighted material unless the user has rights and is comfortable sending it to Neta services. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huxiuhan/neta-creative) <br>
- [Best Practices for Image Generation](references/image-generation.md) <br>
- [Best Practices for Video Generation](references/video-generation.md) <br>
- [Best Practices for Song Generation](references/song-creation.md) <br>
- [Best Practices for Song MVs](references/song-mv.md) <br>
- [Best Practices for Character Search](references/character-search.md) <br>
- [Best Practices for Creative Remix](references/collection-remix.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a NETA_TOKEN environment variable and the Neta CLI package.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

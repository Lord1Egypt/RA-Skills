## Description:

Generate music and audio with AceStep Audio 1.5 through a user-configured ComfyUI server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshinejnjn](https://clawhub.ai/user/sunshinejnjn)

### License/Terms of Use:

BSD 3-Clause

## Use Case:

External users and developers use this skill to turn a music description and optional lyrics into an audio track through their configured ComfyUI installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured ComfyUI endpoint receives music prompts, lyrics, and any configured API key.

Mitigation: Use a trusted endpoint and HTTPS for remote connections, and avoid sending sensitive prompt content.

Risk: Automatic deletion of the server-side generated audio requires a separate plugin and may stop after repeated failures, leaving the file on the server.

Mitigation: Tell the user about cleanup before running; verify deletion when retention matters, and use --keep when they want the server copy retained.

## Reference(s):

- [AceStep Audio 1.5 model](https://huggingface.co/AceStep/AceStep1.5)
- [AceStep-ComfyUI](https://github.com/AceStep/AceStep-ComfyUI)
- [ComfyUI-Audio nodes](https://github.com/ligersearch/ComfyUI-Audio)
- [ComfyUI-VideoHelperSuite](https://github.com/Fannovel16/ComfyUI-VideoHelperSuite)
- [Purge after retrieval plugin](https://github.com/sunshinejnjn/comfyui-purge-after-retrieval)
- [Attribution and workflow notes](references/attribution.md)
- [CLI reference](references/cli-reference.md)
- [Image-first guidance](references/image-first.md)

## Skill Output:

**Output Type(s):** [Audio files, Guidance, Configuration instructions]

**Output Format:** [Generated audio file (MP3) with concise Markdown delivery details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Music is generated from text tags and optional lyrics; reference images are used only to derive text and are not uploaded.]

## Skill Version(s):

0.4.14 (source: frontmatter, VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Exports accessible Feishu/Lark documents to a local, self-contained Markdown folder with downloaded media assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theosunny](https://clawhub.ai/user/theosunny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document operators use this skill to export Feishu/Lark documents into local Markdown packages for archiving, migration, review, or downstream editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document content may cause unexpected network requests during asset download.

Mitigation: Use the skill only with trusted Feishu/Lark documents and run exports in a restricted network environment.

Risk: Output path or overwrite behavior may write outside the intended destination.

Mitigation: Run exports from a dedicated workspace, set an explicit output directory, and inspect the generated path before using the files.

Risk: Sensitive documents may be copied locally with downloaded assets.

Mitigation: Avoid exporting sensitive documents until the temporary-file, URL-validation, output-path, overwrite, and download-size issues are fixed.

Risk: The documented global upgrade command can modify the user's global npm and skill environment.

Mitigation: Use the global upgrade command only in a controlled environment where global npm and skill changes are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theosunny/skills/lark-to-anything)
- [Publisher profile](https://clawhub.ai/user/theosunny)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; generated output is an index.md file and an assets folder.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads images and whiteboard thumbnails when available; failed downloads keep original links or placeholders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

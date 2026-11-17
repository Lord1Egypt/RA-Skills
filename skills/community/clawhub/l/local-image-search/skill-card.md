## Description:

Fast local image search using macOS Spotlight or fd. Search images by name, date, location, or metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaomenghuan](https://clawhub.ai/user/zhaomenghuan)

### License/Terms of Use:


## Use Case:

Developers, creators, and other local-machine users use this skill to find image files quickly by filename, date, location metadata, or supported image type without manually browsing folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted search patterns can cause unsafe behavior in search_by_name.sh.

Mitigation: Review or harden the script before installation, and only pass trusted patterns unless fd and grep are protected with -- delimiters.

Risk: copy_results.sh can duplicate arbitrary local files from a piped result list.

Mitigation: Review the result list before copying and use only an explicitly chosen destination folder.

Risk: Local photos and GPS metadata can expose private information.

Mitigation: Scope searches to specific folders and avoid broad home-directory searches unless that exposure is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaomenghuan/skills/local-image-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and script usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are local filesystem paths produced by shell commands or helper scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

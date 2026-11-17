## Description:

Organize, index, and search local photo libraries with AI-powered metadata and safe file handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to index local photo libraries, search photos by content, date, location, or person, detect duplicates, and plan non-destructive organization or metadata workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a persistent local index containing sensitive photo paths, dates, camera data, GPS-derived locations, descriptions, and person tags.

Mitigation: Use it only after review, keep the index in a trusted local library location, and confirm that users are comfortable storing these records.

Risk: Reverse geocoding GPS data and face-based tagging can expose or amplify sensitive location and identity information.

Mitigation: Ask for explicit confirmation before reverse geocoding GPS data or applying person tags.

Risk: Metadata writes may alter original photos if commands are applied directly.

Mitigation: Keep edits on copies only and use review manifests before bulk operations.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON file conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local index sidecars, review manifests, and non-destructive file operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

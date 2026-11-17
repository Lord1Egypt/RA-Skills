## Description:

Manage local images by category with original and thumbnail storage, enabling fast tag, date, category, and keyword search through a JSON index file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaobu2020](https://clawhub.ai/user/xiaobu2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual users can use this skill to save local image files into categorized workspace folders, generate thumbnails, and search a JSON index by tag, date, category, or keyword.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and metadata are copied into persistent local workspace storage.

Mitigation: Avoid saving highly sensitive receipts or people photos unless retention and deletion are managed outside the skill.

Risk: Stored image metadata may be untrusted when other users or automation can add records.

Mitigation: Review displayed metadata before relying on it and restrict write access to the image index where appropriate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaobu2020/skills/image-manager)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Plain text and JSON records from Python command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves original images, 300x300 thumbnails, and a persistent JSON index in the local workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

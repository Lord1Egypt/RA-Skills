## Description:

Search Z-Library, retrieve book metadata and download limits, and download books through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can search for books, inspect book details and account download limits, and retrieve book files through their connected Z-Library account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs remote installer scripts whose release cannot be verified from the provided artifact.

Mitigation: Install the oo CLI separately using a reviewed, verified release, and require approval before fallback installation.

Risk: Downloading a book uploads it to OOMOL transit storage and consumes account quota; storage access and retention should be checked.

Mitigation: Confirm the upload is intended, check account quota, and review storage access and retention before downloading.

Risk: The safety guidance describes downloads as read-only even though book downloads upload content to transit storage.

Mitigation: Treat downloads as an external upload and explain the storage and quota effects before proceeding.

## Reference(s):

- [Z-Library](https://z-lib.org)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, Files, Shell commands]

**Output Format:** [JSON action requests and connector responses; downloaded book files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an installed, signed-in oo CLI and a connected Z-Library account.]

## Skill Version(s):

1.0.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

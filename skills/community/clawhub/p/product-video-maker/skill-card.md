## Description:

Turn product photos or a store URL into a polished product video with Pexo by uploading media, submitting the user's request, polling the hosted service, and returning the final asset URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pexo](https://clawhub.ai/user/pexo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create product videos for e-commerce listings, ads, or social channels. The agent handles Pexo setup, media upload, request relay, polling, preview selection, revision requests, and final delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials can be exposed if the Pexo config file or environment is mishandled.

Mitigation: Protect PEXO_API_KEY, restrict permissions on ~/.pexo/config, and rotate the key if exposure is suspected.

Risk: The shared shell helper sources ~/.pexo/config, so unsafe shell content in that file can execute locally.

Mitigation: Keep ~/.pexo/config limited to simple PEXO_BASE_URL and PEXO_API_KEY assignments from a trusted source.

Risk: Product prompts and uploaded media are sent to Pexo's hosted backend.

Mitigation: Use only a trusted Pexo endpoint and avoid uploading confidential product images or sensitive prompts unless that transfer is acceptable.

Risk: Fetched result assets may be downloaded into a local ~/.pexo/tmp cache.

Mitigation: Use restrictive local permissions, set PEXO_TMP_DIR to an appropriate writable location when needed, and remove cached assets that should not remain on disk.

## Reference(s):

- [Product Video Maker on ClawHub](https://clawhub.ai/pexo/skills/product-video-maker)
- [Pexo](https://pexo.ai)
- [Setup Checklist](references/SETUP-CHECKLIST.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown with shell command snippets, project links, JSON status details, and final asset URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PEXO_API_KEY, PEXO_BASE_URL, curl, jq, and file; video generation is asynchronous and normally requires polling before delivery.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

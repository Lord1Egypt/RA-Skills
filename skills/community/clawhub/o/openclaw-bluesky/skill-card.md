## Description:

Bluesky/AT Protocol orchestration skill for authenticated interaction with the Bluesky Social network: post, reply, like, repost, quote, bookmark, and upload media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heather-herbert](https://clawhub.ai/user/heather-herbert)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure authenticated Bluesky and AT Protocol interactions, including posting, replying, quoting, liking, reposting, media uploads, and private bookmarks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can authenticate and perform public Bluesky account actions such as posting, replying, liking, reposting, quoting, and uploading media.

Mitigation: Install it only for accounts where agent-driven actions are allowed, and add a confirmation step before public writes.

Risk: The skill requires a Bluesky app password and can change account engagement state if the credential is exposed or misused.

Mitigation: Use a revocable app password, provide it only through secure environment configuration, and never use a primary account password.

Risk: A custom PDS endpoint or unpinned atproto dependency can expand operational or supply-chain risk.

Mitigation: Verify BSKY_PDS is a trusted HTTPS endpoint and consider pinning the atproto dependency before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/heather-herbert/skills/openclaw-bluesky)
- [AT Protocol Docs](https://atproto.com/)
- [Bluesky Developer Docs](https://docs.bsky.app/)
- [Bluesky Social PDS](https://bsky.social)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code references, shell commands, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bluesky handle, app password, trusted PDS endpoint, and the atproto Python dependency.]

## Skill Version(s):

0.1.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

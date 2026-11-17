## Description:

Use this skill to read, create, and update Rakuraku Seisan data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Rakuraku Seisan users use this skill to download journal files, check CSV import results, and import master CSV data through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code or introduce persistent agent skills without clearly scoped approval.

Mitigation: Install a reviewed CLI version separately and disable unwanted agent-skill synchronization.

Risk: Business data sent for imports may be processed by OOMOL, and confidential CSV files could be exposed if made public.

Mitigation: Confirm OOMOL may process the data, approve each import's contents, and avoid publicly exposing confidential CSVs.

## Reference(s):

- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Rakuraku Seisan product page](https://www.rakus.co.jp/rakurakucloud/seisan/)
- [Rakuraku Seisan API documentation](https://success-navi.rakurakucloud.jp/seisan/manual/detail/1236)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-rakuraku-seisan)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Files, Guidance]

**Output Format:** [JSON connector responses, downloaded CSV/TXT or ZIP files, and Markdown guidance with inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads may be temporary URLs; CSV and TXT exports retain MS932 encoding.]

## Skill Version(s):

1.0.2 (source: artifact frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

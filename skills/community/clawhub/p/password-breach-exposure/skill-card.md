## Description:

Checks passwords against the Have I Been Pwned corpus using k-anonymity, classifies breach exposure, and produces an account rotation-priority queue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Individuals and families auditing reused passwords use this skill to check breach-corpus exposure and prioritize account password changes and two-factor authentication follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unchecked passwords may be labeled safe, producing misleading rotation priorities.

Mitigation: Wait for corrected nickname handling and evidence-based assessment before relying on the rotation queue.

Risk: Actual passwords could be exposed through chat or inventory files.

Mitigation: Use the local hidden password prompt and keep actual passwords out of chat and inventory files.

Risk: The local cache retains full password hashes.

Mitigation: Protect or delete scripts/data/pwned_cache.json.

## Reference(s):

- [Breach Exposure Reference Playbook](references/exposure-playbook.md)
- [Have I Been Pwned Pwned Passwords API](https://api.pwnedpasswords.com/range/)
- [ClawHub skill page](https://clawhub.ai/voronindenis5/skills/password-breach-exposure)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Terminal reports with exposure bands and a ranked account-rotation queue]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Password checks use network lookups; the bundled breach catalog supports offline assessment.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

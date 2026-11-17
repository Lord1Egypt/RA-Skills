## Description:

Check your PopUp referral link, track earnings, and see referred vendor status. Earn $100 per vendor who subscribes annually.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eliaskress](https://clawhub.ai/user/eliaskress)

### License/Terms of Use:


## Use Case:

PopUp organizers use this skill to view their referral code, referral share URL, earnings, account balance, and referred vendor statuses. The skill is read-only and is intended for explicit referral dashboard requests rather than autonomous outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Maintainer commands in the README run an unpinned ClawHub CLI version.

Mitigation: Use a pinned or locally vetted ClawHub CLI version before publishing or updating the skill.

Risk: The README shows a real token being passed directly as a command-line argument.

Mitigation: Avoid putting real tokens in command-line arguments and rotate any token previously used that way.

Risk: The skill requires a bearer token through POPUP_API_KEY to retrieve referral data.

Mitigation: Store POPUP_API_KEY securely, restrict access to authorized users, and rotate the token if it is exposed.

## Reference(s):

- [PopUp Referrals ClawHub Skill Page](https://clawhub.ai/eliaskress/skills/popup-referrals)
- [PopUp Organizer API Base URL](https://usepopup.com/api/v1/organizer)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown referral dashboard summary based on PopUp referral API data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POPUP_API_KEY. The referenced API is read-only for referral data and returns JSON responses wrapped in a data object.]

## Skill Version(s):

1.1.0 (source: server release metadata, changelog, and README publish command)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

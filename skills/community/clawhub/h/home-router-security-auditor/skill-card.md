## Description:

Use when setting up, auditing, or suspecting trouble with a home router — generates the civilian-grade hardening checklist (WPA3/WPA2 transition, WPS off, UPnP off, admin password + remote management, firmware freshness), decodes router-speak on the admin page, runs a local-network device inventory with flagging of unknown clients, and interprets the scary-sounding options (guest VLAN isolation, DNS rebinding protection) so defaults actually get changed instead of scrolled past.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Home router owners and household administrators use this skill to harden router settings, understand admin-page options, inventory devices on a network they control, and record a security baseline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inventory results can include devices on networks the user does not control, and device identification is manual.

Mitigation: Run inventory only on networks you control and identify listed devices manually.

Risk: Router setting changes, resets, or reflashing can interrupt connectivity or require recovery details.

Mitigation: Establish working wired access before disabling Wi-Fi administration; obtain model-specific recovery instructions and ISP settings before resetting or reflashing.

Risk: A baseline may not reflect the router's actual settings, and notes could expose credentials.

Mitigation: Verify settings manually before relying on the baseline and keep passwords out of baseline notes.

## Reference(s):

- [Router Hardening Field Reference](references/hardening-guide.md)
- [Clawhub skill listing](https://clawhub.ai/voronindenis5/skills/home-router-security-auditor)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands, JSON]

**Output Format:** [Markdown checklists and explanations, terminal inventory output, and a JSON baseline record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The network inventory is read-only; the baseline records router model, firmware, date, and notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

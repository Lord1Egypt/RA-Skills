## Description:

Use this skill when a process-safety team wants to draft, run, or review one IEC 61882 / CCPS HAZOP node worksheet, including node definition, design intent, deviations, safeguards, risk scoring, LOPA flags, recommendations, and chair review boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Process-safety teams use this skill to structure one HAZOP node review and draft the worksheet package for qualified team review. It supports node setup, design-intent capture, deviation analysis, recommendation tracking, and LOPA/SIL referral flags without replacing formal sign-off.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Facility, P&ID, recipe, vendor, incident, and personnel information used with this skill may be sensitive.

Mitigation: Treat those inputs and outputs as confidential and avoid unnecessary disclosure in prompts, examples, or shared artifacts.

Risk: A draft HAZOP worksheet could be mistaken for approved process-safety sign-off.

Mitigation: Keep outputs as draft support and require qualified multidisciplinary HAZOP team, HAZOP chair, and process-safety responsible-person review before action.

Risk: Risk scoring can be misleading if the facility risk matrix or LOPA-trigger criteria are missing or invented.

Mitigation: Use only the facility-supplied risk matrix and LOPA-trigger criteria; stop before scoring when those inputs are unavailable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/archlab-space/skills/hazop-node-analysis-worksheet)
- [Open-Skill-Hub Issues](https://github.com/archlab-space/Open-Skill-Hub/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown draft HAZOP package with worksheet tables and review lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft support for qualified HAZOP team review; does not authorize startup, MOC/PSSR closure, LOPA/SIL decisions, or QRA.]

## Skill Version(s):

0.1.2 (source: server release evidence and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

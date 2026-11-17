## Description:

Health Buddy Pro helps an agent estimate meal nutrition from photos or text, track hydration, supplements, activity, and custom health metrics, and produce goal check-ins and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill with an AI agent to log meals from photos or text, track daily nutrition and wellness metrics, and receive informational coaching summaries. It is an informational wellness tool, not medical advice or a medical device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health information may be logged or summarized by the skill.

Mitigation: Review before installing if you plan to log private health information, and keep generated data and configuration files private.

Risk: Local-only privacy claims are incomplete because the artifacts also describe optional Supabase/Vercel dashboard storage.

Mitigation: Avoid optional cloud dashboard use unless you have reviewed where health data is stored and who can access it.

Risk: Health, nutrition, supplement, and medication-adjacent outputs may be mistaken for professional advice.

Mitigation: Keep the medical disclaimer visible, consult qualified professionals for medical decisions, and reject unsafe diet or extreme restriction requests.

Risk: Promotional recommendations may appear in health conversations.

Mitigation: Review recommendations for relevance and separate wellness guidance from product promotion.

## Reference(s):

- [Health Buddy Pro on ClawHub](https://clawhub.ai/nollio/skills/normieclaw-health-buddy-pro)
- [README](artifact/README.md)
- [Security Audit](artifact/SECURITY.md)
- [Setup Prompt](artifact/SETUP-PROMPT.md)
- [Dashboard Specification](artifact/dashboard-kit/DASHBOARD-SPEC.md)
- [Photo-Based Meal Logging Example](artifact/examples/photo-meal-logging.md)
- [Daily Nutrition Summary Example](artifact/examples/daily-summary.md)
- [Goal Check-In Example](artifact/examples/goal-checkin.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Conversational text or Markdown, JSON log/configuration updates, and setup shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local health logs and configuration files; optional dashboard materials describe Supabase/Vercel-backed storage.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

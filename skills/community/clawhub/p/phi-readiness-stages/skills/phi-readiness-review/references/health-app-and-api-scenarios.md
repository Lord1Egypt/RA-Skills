# Health App and API Scenarios

Last reviewed: March 17, 2026.

Use this reference when the reviewed workflow is a mobile app, patient app, consumer health app, device platform, provider-connected application, customer-hosted product, or API integration where HIPAA scope and role are easy to overstate.

## Core rule

Health-related data is not automatically PHI or ePHI for HIPAA purposes. Determine scope by role, relationship, and workflow, not by health branding alone.

## Questions to answer

- Is the app or service offered on behalf of a covered entity or business associate?
- Is the app selected by the individual for their own use?
- Does the app access provider data at the individual's direction under a patient access workflow?
- Does support, telemetry, backups, remote management, or analytics create access to PHI?
- Does the deployment model change the answer between SaaS, customer-hosted, and managed-service variants?
- Can free text, attachments, uploads, exports, support tickets, or logs pull PHI into a workflow that is otherwise marketed as non-PHI?

## Conservative scenario rules

### Individual-selected consumer app

If the app is chosen by the individual and is not acting on behalf of a covered entity, health plan, clearinghouse, or business associate, do not automatically place the reviewed workflow inside HIPAA scope. Flag FTC, state-law, or consumer-health review separately when relevant.

### App or service acting on behalf of a regulated party

If the service creates, receives, maintains, or transmits PHI on behalf of a covered entity or business associate, treat business-associate or subcontractor analysis as likely relevant and require contract evidence before PRS-3.

### Patient-directed API access

If the app receives PHI from a provider API at the individual's direction, do not assume the app becomes a business associate solely because it receives PHI. Review who chose the app, who the app is serving, and whether it is acting on behalf of the regulated entity.

### Customer-hosted or white-label software

Split the assessment by deployment and support model. Customer-hosted software with no vendor access is not the same as vendor-operated SaaS or customer-hosted software with telemetry, debugging, backups, or remote administration.

### Unintended PHI ingress

If the current workflow is non-PHI by design but PHI ingress is only theoretical or incidental, do not inflate the current PRS stage automatically. Keep the current stage scoped honestly, record the PHI-ingress risk, and name the boundary controls required before future PHI use.

If live forms, uploads, chat, support channels, or logs intentionally accept or routinely receive PHI today, do not treat that as a future-only gap. Reassess the current scope as potentially PHI-bearing and apply the corresponding role, evidence, and stage logic.

## Evidence to seek

- contract or onboarding language showing who the app serves
- API authorization model and intended recipient
- BAA or explicit reasoning why a BAA is not required for the scoped workflow
- deployment, support, telemetry, and analytics design
- data-class rules for free text, attachments, exports, tickets, and logs
- examples or records showing whether PHI ingress is hypothetical, blocked, observed, or intentionally accepted in live use

## Output guidance

- separate current HIPAA scope from future PHI-prepared state
- distinguish theoretical PHI ingress from observed or intentionally accepted PHI ingress
- state when adjacent FTC or state-law review is still needed
- name the exact missing fact when the role conclusion is uncertain

## Verify these official sources live

- `Resources for Mobile Health Apps Developers` in `references/source-registry.md`
- `Access right, health apps, and APIs` in `references/source-registry.md`, together with its current-law limitation notice
- `Important notice regarding individuals' right of access to health records` in `references/source-registry.md` when patient-directed API access matters
- `Who must comply with HIPAA privacy standards` in `references/source-registry.md`
- `Business associates guidance` in `references/source-registry.md`
- `Cloud computing guidance` in `references/source-registry.md` when hosting or management is relevant

# Applicability and Role Matrix

Use this matrix before assigning a PRS stage. PRS describes workload readiness, but HIPAA applicability and role still matter because they change the evidence and contracting expectations.

This matrix is a PRS assessment aid, not a legal determination.

## Output categories

Use one of these outputs:

- likely covered entity
- likely business associate
- likely subcontractor
- likely outside HIPAA scope for the reviewed workflow
- unclear from available evidence

## Decision matrix

| Likely role | Typical indicators | Evidence to seek | PRS impact |
| --- | --- | --- | --- |
| Covered entity | health plan, health care clearinghouse, or health care provider conducting covered electronic transactions in the reviewed workflow | service description, transaction model, customer or patient relationship, organizational documentation | Privacy Rule, Security Rule, and Breach Notification considerations are usually directly relevant |
| Business associate | creates, receives, maintains, or transmits PHI on behalf of a covered entity or another business associate as part of a function or service | service boundary, PHI flow, contract structure, BAA analysis, hosting or operational role | BAA and vendor-role analysis become stage-gating before PRS-3 |
| Subcontractor | vendor to a business associate that creates, receives, maintains, or transmits PHI on behalf of that business associate | subcontracting chain, service role, PHI path, contract chain | inherited controls and downstream contract analysis become important |
| Outside HIPAA scope for the reviewed workflow | no PHI in scope, or the reviewed service does not create, receive, maintain, or transmit PHI in the actual scoped model | scoped data statement, deployment model, support boundary, architecture | current state may still be PRS-0 or PRS-1 if preparing for future PHI use |
| Unclear | critical facts are missing | deployment model, support model, contract role, PHI flow, customer responsibility split | reduce confidence and cap conclusions conservatively |

## Special cases

### Customer-hosted software

If the vendor provides software that the customer runs entirely within the customer's environment, do not assume the vendor is outside HIPAA scope. Review:

- whether vendor personnel can access PHI for support, operations, or debugging
- whether telemetry, backups, logs, or remote management leave the customer environment
- whether the contract or support model creates a business-associate role

### Health apps and patient-directed access

Do not assume a health app is inside HIPAA scope just because it handles health-related data. Review whether:

- the app is acting on behalf of a covered entity or business associate
- the app is chosen by the individual for their own use
- the app receives provider data at the individual's direction rather than as part of a provider-operated service
- adjacent FTC or state-law issues are more relevant than HIPAA for the reviewed workflow

### Cloud and managed infrastructure

Do not assume `infrastructure only` means `outside HIPAA scope`. HHS cloud guidance can make a provider a business associate when it maintains ePHI on behalf of a regulated entity, even if the data is encrypted and the provider does not view it in the ordinary course.

### Non-HIPAA but health-related workflows

A workflow may be outside HIPAA scope and still trigger other privacy, consumer-health, or breach rules. If so, say that the workflow is outside HIPAA scope for PRS purposes and flag adjacent legal review separately.

## Conservative rules

- If role depends on contract structure not provided, use `likely` or `unclear`.
- If PHI flow is only hypothetical and the current workload is non-PHI by design, do not inflate the current PRS stage.
- If current scope is non-PHI and PHI ingress is only theoretical or incidental, record that as a boundary risk and future-state gap, not as automatic evidence of current live PHI use.
- If live forms, uploads, chat, support tickets, logs, or similar workflows intentionally accept or routinely receive PHI, treat that as evidence the current scope may already include PHI and reassess the role, stage, and evidence requirements accordingly.
- If the deployment or support model materially changes the role analysis, treat that as a scope split, not a small caveat.

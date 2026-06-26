# ThumbGate Prevention Rules: Medical & Dental Appointment Pilot

| Rule ID | Name | Description | Severity |
| :--- | :--- | :--- | :--- |
| MED-001 | PHI_PROTECTION | Block and redact Social Security Numbers or detailed diagnosis text in logs. | Critical |
| MED-002 | SPECIALTY_MATCH | Appointment type (e.g., Surgery) must match Practitioner specialty (e.g., Surgeon). | High |
| MED-003 | INSURANCE_GATE | Verify insurer is in the `accepted_plans.json` list before booking. | High |
| MED-004 | EMERGENCY_911 | Trigger immediate "Call 911" disclaimer for keywords: "chest pain", "bleeding", "unconscious". | Critical |
| MED-005 | DOUBLE_BOOKING | Block any appointment ID already present in the `confirmed_slots` index. | High |
| MED-006 | MIN_NOTICE | Appointments must be scheduled at least 4 hours in advance. | Medium |
| MED-007 | CLINIC_HOURS | Reject requests for slots outside 08:00 - 18:00 Mon-Fri. | High |
| MED-008 | AGE_CONSENT | For patients < 18, MUST ask for parent/guardian name before booking. | Medium |
| MED-009 | CANCEL_WINDOW | Cancellations must be made > 24 hours in advance; trigger fee warning. | Low |
| MED-010 | NO_ADVICE | Reject requests for "diagnosis" or "prescription refills"; trigger handoff. | High |

# Collaboration Status Card

## Project Overview

| Field | Value |
| --- | --- |
| Project | Internal support knowledge assistant pilot |
| Time range | August 18–21, 2026 |
| Phase | Controlled pilot preparation |
| Overall status | Proceeding with one content risk and one staging dependency |
| Summary | Prepare access, staging, and permission tests before the controlled pilot. |
| Evidence | The launch remains a controlled pilot. |

## Progress

| Progress | Status | Evidence |
| --- | --- | --- |
| Pilot scope set to 40 employees | Confirmed | The pilot will include 40 employees. |

## Confirmed Decisions

| Decision | Result | Confirmed by | Evidence |
| --- | --- | --- | --- |
| Answer traceability | Every answer must cite its source | Project notes | every answer must cite its source |
| Content scope | HR policy content is excluded | Project notes | HR policy content is out of scope |

## Owner × Deadline Actions

| Action | Owner | Deadline | Deliverable | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| Send the access list | Maya Chen | Aug 19, 16:00 | Access list | Pending | send the access list by Aug 19, 16:00 |
| Deploy the staging build | Leo Park | Aug 20, 12:00 | Staging build | Pending | deploy the staging build by Aug 20 |
| Update the refund article | Not provided | Not provided | Updated article | Needs assignment | No owner or deadline has been assigned |

## Risks / Blockers / Dependencies

| Type | Description | Impact | Mitigation | Owner | Evidence |
| --- | --- | --- | --- | --- | --- |
| Risk | The refund article is outdated | Answers may use stale guidance | Assign an owner and deadline | Not provided | The refund article is outdated |
| Dependency | QA waits for the staging build | Permission testing cannot start | Deliver staging by Aug 20 | Leo Park | QA starts after the staging build |

## Cross-functional Relationships

| From | To | Collaboration item | Status | Evidence |
| --- | --- | --- | --- | --- |
| Engineering | QA | Staging handoff for permission testing | Pending | QA starts after the staging build |

## Human Review Required

| Item | Reason | Confirm with | Evidence |
| --- | --- | --- | --- |
| Refund article owner and deadline | Neither field is assigned | Knowledge owner | No owner or deadline has been assigned |

## JSON Output

```json
{
  "project_overview": {
    "project_name": "Internal support knowledge assistant pilot",
    "time_range": "August 18–21, 2026",
    "current_phase": "Controlled pilot preparation",
    "overall_status": "Proceeding with one content risk and one staging dependency",
    "summary": "Prepare access, staging, and permission tests before the controlled pilot.",
    "evidence": "The launch remains a controlled pilot."
  },
  "progress": [
    {"item": "Pilot scope set to 40 employees", "status": "Confirmed", "evidence": "The pilot will include 40 employees."}
  ],
  "confirmed_decisions": [
    {"decision": "Answer traceability", "result": "Every answer must cite its source", "confirmed_by": "Project notes", "evidence": "every answer must cite its source"},
    {"decision": "Content scope", "result": "HR policy content is excluded", "confirmed_by": "Project notes", "evidence": "HR policy content is out of scope"}
  ],
  "action_items": [
    {"task": "Send the access list", "owner": "Maya Chen", "department": "Operations", "ddl": "Aug 19, 16:00", "deliverable": "Access list", "status": "Pending", "evidence": "send the access list by Aug 19, 16:00"},
    {"task": "Deploy the staging build", "owner": "Leo Park", "department": "Engineering", "ddl": "Aug 20, 12:00", "deliverable": "Staging build", "status": "Pending", "evidence": "deploy the staging build by Aug 20"},
    {"task": "Update the refund article", "owner": "Not provided", "department": "Knowledge management", "ddl": "Not provided", "deliverable": "Updated article", "status": "Needs assignment", "evidence": "No owner or deadline has been assigned"}
  ],
  "risks_dependencies": [
    {"type": "Risk", "description": "The refund article is outdated", "impact": "Answers may use stale guidance", "mitigation": "Assign an owner and deadline", "owner": "Not provided", "evidence": "The refund article is outdated"},
    {"type": "Dependency", "description": "QA waits for the staging build", "impact": "Permission testing cannot start", "mitigation": "Deliver staging by Aug 20", "owner": "Leo Park", "evidence": "QA starts after the staging build"}
  ],
  "cross_department_relationships": [
    {"from": "Engineering", "to": "QA", "collaboration_item": "Staging handoff for permission testing", "status": "Pending", "evidence": "QA starts after the staging build"}
  ],
  "needs_human_confirmation": [
    {"item": "Refund article owner and deadline", "reason": "Neither field is assigned", "suggested_confirm_with": "Knowledge owner", "evidence": "No owner or deadline has been assigned"}
  ]
}
```

# Application Status Tracking

## Purpose
Monitor where applications are in the processing pipeline, track against published timelines, and know when to take action.

## When to Use
- "What's the status of my application?"
- "It's been X weeks, is this normal?"
- "Should I follow up on my application?"

## Common Processing Stages

### US Visa Processing
| Stage | Description | Typical Duration |
|-------|-------------|------------------|
| Received | Application submitted to USCIS/consulate | - |
| Fee Processed | Payment confirmed | 1-2 weeks |
| Biometrics Scheduled | Fingerprint/photo appointment letter sent | 2-6 weeks |
| Biometrics Completed | Fingerprints taken | Same day |
| Under Review | Case being processed | Varies widely |
| RFE Issued | Request for Evidence sent | Action required |
| RFE Response Received | Additional documents received | Review continues |
| Interview Scheduled | Interview date assigned | 1-4 weeks notice |
| Interview Completed | Attended interview | Decision pending |
| Approved | Application approved | Next steps provided |
| Administrative Processing | Additional review needed | Days to months |
| Document Issued | Visa/passport being produced | 1-2 weeks |
| Delivered | Passport returned to applicant | Varies |

### Canada Immigration (Express Entry)
| Stage | Description |
|-------|-------------|
| Profile Created | Express Entry profile submitted |
| In Pool | Awaiting Invitation to Apply (ITA) |
| ITA Received | 60 days to submit application |
| Application Submitted | Complete application to IRCC |
| AOR Received | Acknowledgment of Receipt |
| Medicals Passed | Medical exam approved |
| Background Check | Security screening |
| Biometrics Requested | Fingerprint/photo needed |
| Biometrics Completed | Info submitted |
| Review in Progress | Application being reviewed |
| PPR Requested | Passport Request for visa stamp |
| COPR Issued | Confirmation of Permanent Residence |

## Processing Time Analysis

### Published vs. Actual
```
Application: I-485 Adjustment of Status
Service Center: NBC (National Benefits Center)

Published Processing Time: 8-14 months
Your Timeline: 10 months
Status: WITHIN NORMAL RANGE ✅

Breakdown:
• Application received: Jan 15, 2024
• Biometrics: Mar 10, 2024 (+54 days)
• Currently: Under Review
• Expected decision: Sep-Nov 2024
```

### When to Be Concerned
- Beyond published timeline + 30 days
- No status change in 90+ days after biometrics
- RFE response received 60+ days ago with no update
- Interview completed 120+ days ago with no decision

### Escalation Options
1. **Case Inquiry** (online or phone)
   - Available when beyond normal processing time
   - Submit through USCIS website

2. **Congressional Inquiry**
   - Contact your Representative or Senator
   - They can inquire on your behalf
   - Often effective for stalled cases

3. **Ombudsman (USCIS)**
   - For systemic issues or significant delays
   - Last resort after other options

## Data Structure

```json
{
  "applications": [
    {
      "id": "APP-12345",
      "visa_type": "I-485",
      "country": "USA",
      "service_center": "NBC",
      "current_stage": "under-review",
      "status": "active",
      "created_at": "2024-01-15",
      "milestones": [
        {"stage": "submitted", "date": "2024-01-15"},
        {"stage": "fee-processed", "date": "2024-01-22"},
        {"stage": "biometrics-scheduled", "date": "2024-02-10"},
        {"stage": "biometrics-completed", "date": "2024-03-10"},
        {"stage": "under-review", "date": "2024-03-15"}
      ],
      "processing_notes": "Within normal range for NBC",
      "follow_up_date": "2024-09-15"
    }
  ]
}
```

## Tracking Commands

```bash
# Check if processing time is normal
python scripts/check_processing_time.py \
  --application-id "APP-12345" \
  --service-center "NBC"

# Log milestone
python scripts/track_application.py \
  --action update \
  --id "APP-12345" \
  --status "interview-scheduled" \
  --notes "Interview scheduled for April 20, 2024"

# Generate timeline report
python scripts/generate_timeline_report.py \
  --application-id "APP-12345"
```

## Output Format

```
APPLICATION STATUS REPORT
APP-12345: I-485 Adjustment of Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current Status: Under Review
Service Center: NBC (National Benefits Center)
Filed: January 15, 2024 (75 days ago)

TIMELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Jan 15  ✓ Application Submitted
Jan 22  ✓ Fee Processed (+7 days)
Feb 10  ✓ Biometrics Scheduled (+25 days)
Mar 10  ✓ Biometrics Completed (+54 days)
Mar 15  → Under Review (+59 days)

PROCESSING TIME ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Published Range: 8-14 months
Your Position: Month 2.5
Status: ✅ Within normal range

Average for similar cases: 11 months
Estimated completion: October-December 2024

⚠️  If no update by September 15, consider:
    • Case inquiry through USCIS
    • Congressional inquiry if significantly delayed

MILESTONES AHEAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ Interview Scheduled (if required for your category)
☐ Request for Evidence (if additional docs needed)
☐ Approval Notice
☐ Card/Document Production
☐ Document Delivery

RECENT ACTIVITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mar 1: Case status changed to "actively reviewing"
Feb 15: Biometrics appointment notice received

NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Continue monitoring case status weekly
2. Ensure mailing address is current
3. Keep employment authorization valid (if applicable)
4. Notify USCIS of any address changes within 10 days

⚠️  IMPORTANT: Processing times are estimates only.
    Actual times vary by case complexity and service center workload.
```

## Status Change Notifications

When application status changes:
1. Log new milestone with date
2. Compare to typical timeline
3. Update any dependent deadlines (work authorization expiry, etc.)
4. Notify user of significance
5. Adjust follow-up date if needed

## Common Delays and Causes

| Delay Type | Possible Causes | Action |
|------------|-----------------|--------|
| Background check | Common name, security flags | Wait, may take months |
| Administrative processing | Additional review needed | Wait, can take weeks to months |
| Missing documents | RFE issued | Respond promptly with complete docs |
| Service center backlog | High volume | Normal, wait or inquire if beyond timeline |
| Interview waiver review | Eligibility being determined | Wait for decision |

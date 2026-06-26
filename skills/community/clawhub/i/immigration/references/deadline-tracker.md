# Deadline and Timeline Tracker

## Purpose
Track all immigration-related deadlines, document expiry dates, and processing milestones with proactive alerts.

## When to Use
- "Track my application"
- "What deadlines do I have?"
- "When does my [document] expire?"
- "Set reminder for [date]"

## Deadline Types

### Application Deadlines
| Type | Description | Alert Timing |
|------|-------------|--------------|
| Submission Deadline | Last day to file application | 7, 30 days before |
| Response Deadline | Reply to RFE or inquiry | 7, 14 days before |
| Appeal Deadline | Window to file appeal | 14, 30 days before |
| Interview Date | Scheduled visa interview | 7, 1 day before |

### Document Expiry
| Document | Typical Validity | Alert Timing |
|----------|-----------------|--------------|
| Passport | 5-10 years | 180, 90, 30 days |
| Medical Exam | 6 months | 30, 7 days |
| Police Clearance | 6-12 months | 30, 7 days |
| Bank Statements | 3-6 months | Recurring monthly |
| Visa/Status | Varies | 90, 60, 30 days |

### Processing Milestones
| Milestone | Description | Tracking |
|-----------|-------------|----------|
| Receipt Notice | Application received | Date received |
| Biometrics | Fingerprint/photo appointment | Date scheduled |
| Interview Scheduled | Interview date set | Date, location |
| Decision Rendered | Approved/denied/pending | Status update |

## Data Structure

```json
{
  "deadlines": [
    {
      "id": "uuid",
      "application_id": "APP-12345",
      "type": "document-expiry",
      "title": "Medical Exam Expires",
      "description": "I-693 medical examination for AOS",
      "date": "2024-09-01",
      "alert_dates": ["2024-08-01", "2024-08-25"],
      "status": "active",
      "priority": "high",
      "notes": "Must complete new exam before filing I-485"
    },
    {
      "id": "uuid",
      "application_id": "APP-12345",
      "type": "submission-deadline",
      "title": "Response to RFE Due",
      "description": "Reply to Request for Evidence",
      "date": "2024-04-15",
      "alert_dates": ["2024-04-08", "2024-04-12"],
      "status": "active",
      "priority": "urgent",
      "notes": "Need additional tax documents and employment letter"
    }
  ],
  "alert_log": [
    {
      "deadline_id": "uuid",
      "alert_date": "2024-03-01",
      "sent": true,
      "acknowledged": false
    }
  ]
}
```

## Script Usage

```bash
# Add new deadline
python scripts/add_deadline.py \
  --type "document-expiry" \
  --date "2024-09-01" \
  --title "Medical Exam Expires" \
  --description "I-693 for adjustment of status" \
  --priority high

# List upcoming deadlines
python scripts/list_deadlines.py \
  --days 60 \
  --priority urgent,high

# Mark deadline complete
python scripts/update_deadline.py \
  --deadline-id "uuid" \
  --status completed

# Check for expiring documents
python scripts/list_deadlines.py \
  --type "document-expiry" \
  --days 90
```

## Output Format

```
UPCOMING DEADLINES
Generated: March 1, 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 URGENT (Within 7 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Response to RFE Due
  Date: April 15, 2024 (45 days)
  Application: I-485 Adjustment of Status
  Action: Submit additional tax documents and employment letter
  Priority: URGENT

⚠️  HIGH PRIORITY (Within 30 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Biometrics Appointment
  Date: March 25, 2024 (24 days)
  Location: USCIS Application Support Center
  Action: Attend fingerprinting appointment
  Bring: Appointment notice, Photo ID

📅 UPCOMING (Within 90 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Medical Exam Expires
  Date: September 1, 2024 (184 days)
  Document: I-693 Medical Examination
  Action: Schedule new medical exam
  Notes: Use civil surgeon from USCIS list only

• Passport Expires
  Date: December 15, 2024 (289 days)
  Document: Passport (Country: India)
  Action: Renew passport at embassy/consulate
  Notes: Start process 6 months before expiry

COMPLETED DEADLINES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☑ Application Submitted - Feb 15, 2024
☑ Biometrics Fee Paid - Feb 16, 2024

ALERT SETTINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Urgent: 7 and 1 days before
• High: 30 and 7 days before
• Normal: 60 and 30 days before
```

## Alert System

### Priority Levels
1. **Urgent** - Red flag, immediate action required
2. **High** - Important, plan accordingly
3. **Normal** - Standard tracking
4. **Low** - Informational only

### Alert Timing
Configure alerts based on deadline type:
```bash
# Set custom alert schedule
python scripts/add_deadline.py \
  --type "submission-deadline" \
  --date "2024-06-01" \
  --alerts "30,14,7,1"
```

### Missed Deadline Protocol
If a deadline is missed:
1. Log missed deadline with reason
2. Identify consequences (if any)
3. Generate next steps (appeal, extension request, etc.)
4. Update application status

## Processing Time Tracking

### Compare to Published Times
```bash
# Check if application is within normal range
python scripts/check_processing_time.py \
  --application-id "APP-12345" \
  --visa-type "I-485" \
  --service-center "NBC"

# Output:
# Your application: 120 days since filing
# Published range: 8-14 months
# Status: Within normal range ✅
```

### When to Follow Up
- Beyond published processing time + 30 days
- Status hasn't changed in 90+ days
- Biometrics completed 60+ days ago with no update

### Escalation Paths
1. Case Inquiry (online)
2. Contact Center call
3. Congressman/Congresswoman inquiry
4. Ombudsman (if significant delay)

## Calendar Integration

### Export Deadlines
```bash
# Export to ICS format for calendar import
python scripts/export_deadlines.py \
  --format ics \
  --output immigration_deadlines.ics
```

### Sync Reminders
- System reminders at alert dates
- Weekly summary of upcoming deadlines
- Monthly review of all active applications

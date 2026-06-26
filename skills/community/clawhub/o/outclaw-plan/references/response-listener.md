# Response Listener Reference

Inbound response detection, classification, and routing logic.

## Detection Methods

### Email
- Periodic `gmail.search_messages` for replies to outreach threads
- Match by `thread_id` from sent messages
- Also scan inbox for messages from prospect's email address
- Poll interval: every 15 minutes during business hours, every hour outside

### Slack
- Monitor for DMs from prospect (if applicable)
- Watch for mentions in shared channels
- Poll interval: every 10 minutes

### WhatsApp
- Poll WhatsApp MCP for new messages from prospect's number
- Check read receipts for engagement signals
- Poll interval: every 15 minutes

### LinkedIn
- Browser check of LinkedIn messaging inbox
- Look for new messages from campaign targets
- Poll interval: every 30 minutes (rate-limited)

## Response Classification

The `response-analyst` subagent classifies each detected response:

| Classification | Definition | Example |
|---------------|-----------|---------|
| POSITIVE | Interested, wants to meet or learn more | "Sounds interesting, let's chat next week" |
| NEUTRAL | Acknowledgment, asks questions, needs more info | "What's the pricing?" / "Tell me more" |
| NEGATIVE | Not interested, asks to stop | "Not a fit right now" / "Please remove me" |
| OOO | Out of office or auto-reply | "I'm away until May 5th" |
| IRRELEVANT | Unrelated response in same thread | Newsletter auto-reply, system notification |

## Adaptive Behavior

### POSITIVE Response
1. Immediately pause all pending follow-ups for this campaign
2. Notify user: "{Name} replied to your {channel}! They're interested in {topic}. I've paused the {next_touchpoint} that was scheduled for {date}."
3. Propose meeting-scheduling plan (draft reply + Calendly link if available)
4. Log to Leadbay: "Reply: POSITIVE. {summary}. Follow-ups paused."

### NEUTRAL Response
1. Pause pending follow-ups
2. Notify user with response content
3. Draft a response addressing their questions using learned style
4. Present revised plan for approval
5. Log to Leadbay: "Reply: NEUTRAL. {summary}. Response drafted."

### NEGATIVE Response
1. Cancel all pending follow-ups permanently
2. Mark campaign as completed (declined)
3. Notify user
4. Add prospect to do-not-contact list
5. Log to Leadbay: "Reply: NEGATIVE. Prospect not interested. Campaign closed."

### OOO Response
1. Parse return date from auto-reply
2. Reschedule all pending follow-ups to after return date + 1 business day
3. Notify user of reschedule
4. Log to Leadbay: "Auto-reply: OOO until {date}. Follow-ups rescheduled."

### IRRELEVANT Response
1. Continue follow-up sequence as planned
2. No notification to user
3. No Leadbay note (noise filtering)

## Plan Revision Flow

When a meaningful response arrives mid-sequence:

1. Agent immediately pauses all scheduled follow-ups for that campaign
2. Notifies user with response content and context
3. Proposes revised plan:
   - Draft reply addressing the response
   - Updated follow-up sequence (if applicable)
   - Next steps recommendation
4. User approves revision → updated plan replaces old one
5. Campaign continues with revised sequence

## Thread Tracking

Maintain a mapping of campaign touchpoints to message identifiers:

```json
{
  "campaign_id": "sarah-chen-acme",
  "threads": {
    "email": {
      "thread_id": "thread_xyz",
      "message_ids": ["msg_001", "msg_002"],
      "prospect_email": "sarah@acme.com"
    },
    "linkedin": {
      "conversation_id": "conv_abc",
      "prospect_profile": "linkedin.com/in/sarachen"
    }
  }
}
```

This enables accurate response matching even when prospects reply on a different channel than where outreach was sent.

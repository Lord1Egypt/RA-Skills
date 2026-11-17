# Google Calendar use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/google-calendar

## Detect and Resolve Scheduling Conflicts

Review upcoming events, identify overlapping meetings, and find alternative time slots without disrupting other commitments.

- Apps: Google Calendar
- Tools: `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`, `GOOGLECALENDAR_FIND_FREE_SLOTS`, `GOOGLECALENDAR_PATCH_EVENT`

> Review my Google Calendar for the next seven days and identify overlapping events, tightly scheduled meetings, and potential scheduling conflicts. Check free and busy time slots before recommending alternatives. For each conflict, show the affected events, their current times, and possible replacement slots that preserve meeting durations. Consider relevant attendee availability when accessible. Do not reschedule, cancel, or delete events until I approve the exact changes. Present the findings in a table with a prioritized list of recommended actions.

## Prepare for Upcoming Business Meetings

Gather relevant meeting details, identify preparation requirements, and organize agendas for customer, supplier, and business meetings.

- Apps: Google Calendar, Gmail
- Tools: `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`, `GOOGLECALENDAR_EVENTS_GET`

> Review my upcoming Google Calendar events for the next five business days. Identify meetings that may require preparation and summarize their titles, times, attendees, descriptions, and relevant context available in the event details. Where connected email access is available, find related conversations and extract important questions, decisions, deadlines, and outstanding issues. Create a preparation checklist and suggested agenda for each relevant meeting. Clearly distinguish information found in existing records from assumptions. Do not send emails or modify calendar events.

## Schedule Meetings From Natural Language

Turn scheduling requests into calendar events while checking availability, duration, attendees, and reminders.

- Apps: Google Calendar
- Tools: `GOOGLECALENDAR_QUICK_ADD`, `GOOGLECALENDAR_FIND_FREE_SLOTS`, `GOOGLECALENDAR_CREATE_EVENT`

> Help me schedule the meeting described in my request using Google Calendar. Interpret the intended date, time, duration, time zone, meeting title, and attendees. Check my calendar for conflicts and suggest suitable alternatives if the requested slot is unavailable. Ask for clarification when an essential detail is ambiguous. Before creating the event, show the proposed details and obtain my confirmation. After approval, create the event and verify the result. Do not invite unintended attendees or overwrite existing events.

## Manage Supplier Follow-Ups

Connect supplier meetings with business emails and Shopify inventory needs to help ensure important purchasing and delivery discussions are not missed.

- Apps: Google Calendar, Gmail, Shopify
- Tools: `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`, `GOOGLECALENDAR_FIND_EVENT`

> Review my upcoming supplier-related calendar events. For each meeting, identify relevant supplier correspondence, outstanding delivery questions, expected replenishment dates, and inventory concerns. Compare supplier details with Shopify inventory and product availability where those records are accessible. Prepare a meeting checklist covering stock levels, delivery dates, pending orders, and decisions required. If a new supplier meeting is created, prepare the checklist for that event. Do not change inventory, send supplier emails, or modify meetings without approval.

## Organize Customer Follow-Up Meetings

Prepare customer meetings using relevant email history and Shopify order information so that unresolved customer issues can be addressed efficiently.

- Apps: Google Calendar, Gmail, Shopify
- Tools: `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`, `GOOGLECALENDAR_FIND_EVENT`

> Review upcoming customer follow-up meetings in my calendar. Where relevant email and Shopify data are accessible, identify the customer concern, associated order, current fulfillment status, previous communication, and outstanding questions. Prepare a concise briefing with the issue summary, verified facts, suggested agenda, and proposed next steps. Flag missing information that needs verification before making commitments to the customer. Do not expose unrelated customer information or send messages automatically. Present the brief in a structured table followed by a meeting checklist.

## Automate Meeting Reminders and Preparation

Use calendar event notifications to identify upcoming meetings and prepare timely reminders and checklists.

- Apps: Google Calendar
- Tools: `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`, `GOOGLECALENDAR_PATCH_EVENT`

> Help me organize reminders for important Google Calendar meetings. Identify events that require preparation, and propose reminders at appropriate intervals before each meeting. For supplier meetings, include inventory and delivery checks; for customer meetings, include relevant correspondence and order details; for marketing meetings, include campaign performance and pending decisions. Avoid duplicate reminders and respect existing event settings. Show the proposed reminder schedule before making changes. Where event-start notifications are available, use them to prepare a timely checklist. Do not alter existing reminders without my approval.

## Coordinate Marketing Campaign Meetings

Schedule and prepare marketing reviews by combining calendar commitments with Google Ads, Analytics, and Shopify performance information.

- Apps: Google Calendar, Google Ads, Google Analytics, Shopify
- Tools: `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`

> Review my upcoming marketing meetings and identify the reports or decisions needed for each one. Where connected data is available, summarize Google Ads spend and conversions, Google Analytics traffic and ecommerce behavior, and Shopify orders and revenue. Highlight significant changes, tracking discrepancies, and campaign optimization opportunities. Prepare a concise agenda with supporting metrics and recommended discussion points. If a follow-up meeting is needed, propose available calendar slots and wait for approval before creating it. Do not change live campaigns or calendar events automatically.

## Keep Team Calendars Organized

Review accessible calendars, organize event visibility, and identify sharing or scheduling issues.

- Apps: Google Calendar
- Tools: `GOOGLECALENDAR_LIST_CALENDARS`, `GOOGLECALENDAR_ACL_LIST`, `GOOGLECALENDAR_CALENDAR_LIST_UPDATE`

> Review the calendars accessible to me and summarize their names, visibility settings, and relevant upcoming events. Identify overlapping commitments and calendars that may need clearer organization. Where appropriate, recommend calendar colors, display settings, or separate calendars for suppliers, customers, internal meetings, and marketing activities. If access permissions need adjustment, show the existing permission and proposed change before applying it. Do not delete calendars, clear events, or change sharing permissions without explicit approval.

## Track Meeting Changes and Cancellations

React to new, updated, cancelled, or deleted events so that meeting preparation and follow-up plans remain accurate.

- Apps: Google Calendar
- Tools: `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`, `GOOGLECALENDAR_EVENTS_GET`, `GOOGLECALENDAR_FIND_EVENT`

> Help me keep business meeting preparation synchronized with Google Calendar changes. When a new event is created, identify whether it relates to a supplier, customer, marketing activity, or internal meeting and prepare the relevant checklist. When an event is updated, summarize the changed date, time, attendees, or details and explain what preparation needs to change. When an event is cancelled or deleted, identify any associated follow-ups that may need rescheduling. When an attendee changes their RSVP, summarize the impact where relevant. Do not automatically contact attendees or create replacement events without approval.

## Generate a Weekly Business Schedule

Produce a weekly overview of meetings, preparation tasks, conflicts, and outstanding follow-ups across connected business workflows.

- Apps: Google Calendar, Gmail, Shopify
- Tools: `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS`, `GOOGLECALENDAR_FIND_FREE_SLOTS`

> Prepare a weekly business schedule summary from my Google Calendar. Include upcoming meetings, event times, attendees where available, potential conflicts, preparation requirements, and pending follow-ups. Connect relevant Gmail correspondence and Shopify business information where accessible. Highlight supplier meetings requiring inventory checks, customer meetings requiring order reviews, and marketing meetings requiring performance reports. Recommend suitable time slots for unresolved tasks based on calendar availability. Present a concise weekly overview, a prioritized preparation checklist, and suggested schedule adjustments. Do not create, move, cancel, or delete events without my approval.

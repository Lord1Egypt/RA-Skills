---
name: meet
description: >
  Complete meeting intelligence system. Trigger whenever someone needs to run a meeting,
  prepare for one, recover from one that went badly, or fix a culture where meetings have
  become the enemy of work. Also triggers on phrases like "prepare for my meeting",
  "write an agenda", "we have too many meetings", "nothing gets decided in our meetings",
  "I have a difficult conversation coming up", or any scenario where people need to be
  in a room — or on a call — and something important needs to happen.
---

# Meet

## The Meeting Nobody Needed

At some point today, somewhere in the world, forty-seven people are sitting in a conference
room for a one-hour meeting that could have been a two-paragraph email. They know this.
The person who called the meeting knows this. Nobody says it.

At the same time, somewhere else, two people are exchanging their fourteenth email on a
decision that would take four minutes to resolve if they just talked.

Bad meeting culture does not have one failure mode. It has two: too many meetings that
should not exist, and too few of the conversations that should.

This skill fixes both.

---

## Meeting Classification
```
MEETING_TYPES = {
  "decision":      {
    "purpose":    "A specific decision must be made before people leave",
    "required":   "Decision owner, options pre-circulated, clear criteria",
    "failure":    "Leaving without a decision documented and assigned"
  },
  "alignment":     {
    "purpose":    "Everyone needs the same understanding of something",
    "required":   "What specifically needs to be aligned, why async failed",
    "failure":    "Sharing information that could have been an email"
  },
  "creative":      {
    "purpose":    "Generate options, ideas, or approaches that require real-time interaction",
    "required":   "Diverge before converge — all ideas before evaluation",
    "failure":    "HiPPO effect — highest paid person's opinion dominates early"
  },
  "relationship":  {
    "purpose":    "Build trust, connection, and shared context that enables future work",
    "required":   "Intentional structure — this does not happen by accident",
    "failure":    "Filling with status updates instead of genuine connection"
  },
  "should_not_exist": {
    "status_update":  "Use async tools — weekly written update replaces 30 min standup",
    "one_way_info":   "Record a video or write it — do not call 20 people to read slides",
    "FYI_meeting":    "If no one needs to say or do anything, it is not a meeting"
  }
}
```

---

## The Pre-Meeting System
```
MEETING_PREPARATION = {
  "agenda_design": {
    "structure": """
      AGENDA_TEMPLATE = {
          "title":        "Meeting name that states the purpose",
          "objective":    "One sentence: what will be true after this meeting that is not true before",
          "pre_read":     "Material people must read BEFORE — not during",
          "items":        [
              {
                  "topic":    "Specific discussion point",
                  "owner":    "Person leading this item",
                  "time":     "Minutes allocated",
                  "type":     "inform | discuss | decide",
                  "output":   "What we need from this item"
              }
          ],
          "decisions_needed": "Pre-listed so everyone arrives prepared",
          "parking_lot":      "Where off-topic items go — not ignored, not derailing"
      }
    """,
    "rules": ["Send agenda minimum 24 hours before",
               "No pre-read longer than 10 minutes",
               "Last item is always next actions — who does what by when"]
  },

  "attendee_audit": """
    def should_attend(person, meeting):
        roles = {
            "decider":      person.must_approve_outcome,
            "contributor":  person.has_unique_input_others_lack,
            "implementer":  person.will_execute_the_decision,
            "informed":     False  # Send the notes — do not attend
        }
        return any([roles["decider"], roles["contributor"], roles["implementer"]])

    # Amazon rule: if two pizzas cannot feed everyone, the meeting is too big
    # Optimal decision meeting size: 5-8 people
  """
}
```

---

## Running the Meeting
```
FACILITATION_FRAMEWORK = {
  "opening": {
    "first_90_seconds": ["State the objective — not the agenda",
                          "Confirm decision authority — who can say yes",
                          "Set the clock — visible timer creates urgency"],
    "parking_lot":       "Visible place for off-topic items — keeps meeting on track
                           without making people feel dismissed"
  },

  "discussion_management": {
    "silence_is_data":   "Silence after a question means people are thinking — let it breathe",
    "dominant_voice":    "Thank you for that — let us hear from someone who has not spoken",
    "tangent_response":  "That is important — let us put it in the parking lot and come back",
    "circular_discussion": """
      def detect_circular_discussion(transcript):
          if same_points_repeated_3_times:
              intervene("We are going in circles. Let me name the two positions I am hearing.
                          [Position A] versus [Position B]. Can we agree on what information
                          would resolve this?")
    """
  },

  "decision_making": {
    "RAPID_framework": {
      "Recommend":  "Person who develops the proposal",
      "Agree":      "Person whose agreement is required",
      "Perform":    "Person who executes the decision",
      "Input":      "Person consulted but not blocking",
      "Decide":     "Single person who makes the final call"
    },
    "principle":   "Every decision needs exactly one Decider. Not consensus. Not majority.
                    One person who is accountable for the outcome."
  },

  "closing": {
    "last_5_minutes": ["Read back every decision made",
                        "Confirm every action item: owner + deadline",
                        "State what will be communicated to people not in the room",
                        "Rate the meeting 1-5 — one word per person"],
    "never_end_without": "Written next actions before people leave the room"
  }
}
```

---

## The After-Meeting System
```
MEETING_NOTES = {
  "what_to_capture": {
    "decisions":     "Every decision with the reasoning — not just what, but why",
    "actions":       "Owner, task, deadline — three fields, no exceptions",
    "parking_lot":   "Every item with assigned follow-up owner",
    "not_decisions": "Discussion content is optional — decisions and actions are mandatory"
  },

  "distribution": {
    "timing":    "Within 2 hours — memory degrades fast",
    "audience":  "Everyone who attended + everyone who needs to know the outcome",
    "format":    "Decisions first, then actions, then discussion summary if needed"
  },

  "accountability": """
    def track_actions(action_items):
        for action in action_items:
            if approaching_deadline(action) and not complete(action):
                send_reminder(action.owner, days_before=2)
            if past_deadline(action) and not complete(action):
                escalate_to_meeting_organizer(action)
  """
}
```

---

## Fixing Meeting Culture
```
CULTURE_FIX = {
  "audit_first": """
    def meeting_audit(calendar):
        for meeting in calendar.recurring:
            evaluate({
                "last_cancellation_missed":   was it missed when cancelled,
                "output_per_session":         what is produced each time,
                "could_be_async":             would Loom or doc work instead,
                "attendee_engagement":         do people actually contribute
            })
        kill_or_redesign(meetings_failing_audit)
  """,

  "principles": ["Default to async — meetings are the expensive option",
                  "Protect deep work blocks — no meeting before 10am or after 3pm (example)",
                  "Meeting-free day per week — Wednesday is common",
                  "No meeting without agenda — if you cannot write the objective, cancel it",
                  "Standing meetings get audited quarterly — most should die eventually"]
}
```

---

## Quality Check Before Delivering

- [ ] Meeting type identified — decision, alignment, creative, or relationship
- [ ] Agenda has a single stated objective not just a list of topics
- [ ] Attendee list audited — no passengers
- [ ] Decision authority identified if decision meeting
- [ ] Action item format includes owner and deadline
- [ ] Meeting notes distributed within 2 hours
- [ ] Recurring meetings flagged for audit if culture question raised

# Event Flexibility Classification Rules

Used by: `sands.conflicts`

Classify each event in a conflict pair as FIXED, FLEXIBLE, or AMBIGUOUS.

---

## FIXED — cannot be easily rescheduled

Apply FIXED when any of these are true:
- External attendees present (attendee email domain differs from user's)
- Title contains: call, meeting, interview, sync, standup, review (with others),
  appointment, doctor, dentist, flight, train, reservation, class, course,
  workshop, concert, show, game, lesson, visit, patient, therapy, session,
  checkup, consultation, screening
- **Title contains service/appointment keywords**: massage, spa, haircut, salon,
  therapy, treatment, MRI, scan, x-ray, bloodwork, lab, dental, medical,
  physician, specialist, chiropractor, acupuncture, physical therapy
- **Title contains meal-with-others keywords**: dinner, lunch, breakfast, brunch
  (implies external party)
- Event has a conference link (Google Meet, Zoom, Teams, Webex)
- Event is recurring (any recurrence pattern)
- Work calendar busy block

---

## FLEXIBLE — likely movable with low friction

Apply FLEXIBLE when **all** of these are true:
- No external attendees
- Title contains: gym, workout, run, walk, errand, personal, reading,
  focus time, deep work, solo lunch, groceries, cleaners, ikebana,
  flower market, meditation, yoga (personal practice), journaling
- No conference link
- No fixed external venue with a reservation

**Caveat:** Keyword matching alone can misclassify. "Walk" in "Walk it Out: Feet, Balance and Gait Mastery" is a workshop/class (FIXED), not a personal walk (FLEXIBLE). Check for class/workshop/course/mastery/lesson modifiers.

---

## AMBIGUOUS — signals are mixed

Apply AMBIGUOUS when:
- Classification signals conflict (e.g., "gym class" — "class" suggests fixed,
  but could be a drop-in)
- Insufficient metadata to determine
- Title is generic ("meeting", "event", "appointment") with no attendee data

Present AMBIGUOUS with an explanation of the uncertainty.

---

## Output Format Per Conflict

```
CONFLICT: [Event A] overlaps [Event B] by X minutes

  Event A: [title] — FIXED
  Reason: external attendees, conference link

  Event B: [title] — FLEXIBLE
  Reason: no attendees, personal activity keyword

  Suggested resolution: Move [Event B].
  Candidate times: [offer 2-3 alternatives if determinable]
```

Never suggest moving a FIXED event unless both events are FIXED, in which case
surface the conflict for the user to resolve manually.

---

## Classification Algorithm (Cron-Compatible Pattern)

```python
def classify_event(ev):
    title = ev.get('summary', '').lower()
    calendar = ev.get('calendar', '')
    attendees = ev.get('attendees', [])
    conference = ev.get('conference', {})
    location = ev.get('location', '').lower()
    recurring = ev.get('recurring', False)

    # FIXED signals
    fixed_signals = []

    # External attendees
    for att in attendees:
        email = att.get('email', '')
        if email and not email.endswith(('@gmail.com', '@googlemail.com')):
            fixed_signals.append('external attendees')
            break

    # Title keywords - fixed
    fixed_keywords = [
        'call', 'meeting', 'interview', 'sync', 'standup', 'review',
        'appointment', 'doctor', 'dentist', 'flight', 'train', 'reservation',
        'class', 'course', 'workshop', 'concert', 'show', 'game', 'lesson',
        'visit', 'patient', 'therapy', 'session', 'checkup', 'consultation',
        'screening', 'massage', 'spa', 'haircut', 'salon', 'treatment',
        'mri', 'scan', 'x-ray', 'bloodwork', 'lab', 'dental', 'medical',
        'physician', 'specialist', 'chiropractor', 'acupuncture',
        'dinner', 'lunch', 'breakfast', 'brunch', 'mastery', 'training'
    ]
    for kw in fixed_keywords:
        if kw in title:
            fixed_signals.append(f'title keyword: {kw}')
            break

    if conference:
        fixed_signals.append('conference link')
    if recurring:
        fixed_signals.append('recurring event')
    if 'work' in calendar.lower():
        fixed_signals.append('work calendar busy block')

    # FLEXIBLE signals
    flexible_keywords = [
        'gym', 'workout', 'run', 'walk', 'errand', 'personal', 'reading',
        'focus time', 'deep work', 'solo lunch', 'groceries', 'cleaners',
        'ikebana', 'flower market', 'meditation', 'yoga', 'journaling'
    ]
    flexible_signals = []
    for kw in flexible_keywords:
        if kw in title:
            flexible_signals.append(f'title keyword: {kw}')
            break

    no_external = not any('external attendees' in s for s in fixed_signals)
    no_conference = not conference
    no_fixed_venue = not any(v in location for v in ['spa', 'clinic', 'hospital', 'office', 'restaurant', 'salon'])

    if flexible_signals and no_external and no_conference and no_fixed_venue:
        return 'FLEXIBLE', flexible_signals

    if fixed_signals:
        return 'FIXED', fixed_signals

    return 'AMBIGUOUS', ['insufficient metadata or mixed signals']
```
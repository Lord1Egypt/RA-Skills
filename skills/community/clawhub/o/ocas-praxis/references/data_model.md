# Praxis Data Model

## Event
```json
{"id":"string","timestamp":"string","domain":"string","context_summary":"string","outcome_type":"string — success|failure|correction|observation","outcome_summary":"string","evidence":["string"],"user_visible_impact":"string"}
```

## MicroLesson
```json
{"id":"string","event_ids":["string"],"lesson_text":"string","confidence":"string — high|med|low","scope":"string","status":"string — proposed|accepted|rejected"}
```

## BehaviorShift
```json
{"id":"string","source_lesson_ids":["string"],"shift_text":"string","status":"string — proposed|active|merged|expired|rejected","activation_reason":"string","created_at":"string","last_reviewed_at":"string","expiry_condition":"string|null","priority":"number"}
```

## Debrief
```json
{"id":"string","related_event_ids":["string"],"summary":"string","accepted_changes":["string"],"rejected_changes":["string"],"open_questions":["string"]}
```

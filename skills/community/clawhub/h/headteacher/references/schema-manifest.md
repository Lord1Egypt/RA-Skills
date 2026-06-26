# Schema Manifest

This file defines the unified semantic model used by `班主任.Skill`.

## System stance

The skill is built around two core capability families:

1. data record and retrieval
2. automated artifact generation

The underlying modeling principle is:

- separate stable objects from ongoing events
- use structured data as the source of truth
- treat Office outputs as generated artifacts, not primary storage

For the headteacher domain, this means:

- `student_master` is the stable object layer
- scores, conduct, daily observations, parent communication, and schedules are event or assignment layers
- artifacts such as seat plans, duty schedules, or parent meeting slides are generated from those layers

## Data operation modes

### Write modes

- one-time import
  - initialize a workspace from rosters, existing spreadsheets, legacy bases, or notes
- dynamic append / update
  - record new exams, observations, discipline events, contacts, and schedule changes

### Read modes

- longitudinal read
  - follow one student across time
  - useful for growth tracking, interventions, and parent communication
- horizontal read
  - inspect a set of students or the whole class at one time slice
  - useful for one exam, one week, one seating cycle, or one duty cycle

## Core entities

### 1. `class_profile`

One record per class workspace.

Suggested fields:

- class_name
- academic_year
- current_term
- headteacher
- default_backend
- workspace_status
- notes

### 2. `student_master`

The authoritative student roster and profile table.

Suggested fields:

- name
- student_id
- student_number
- gender
- class_name
- term
- elective_subjects
- previous_school
- dorm_building
- dorm_room
- dorm_bed
- guardian_1_name
- guardian_1_relation
- guardian_1_phone
- guardian_2_name
- guardian_2_relation
- guardian_2_phone
- national_id
- address
- focus_tags
- notes

### 3. `exam_batch`

Metadata about each assessment batch.

Suggested fields:

- exam_name
- exam_id
- exam_date
- term
- exam_type
- subject_scope
- source
- notes

### 4. `score_detail`

Long-form score storage. One row should represent one student, one exam batch, one subject.

Suggested fields:

- student_ref
- exam_ref
- subject
- score
- class_rank
- grade_rank
- grade_level
- absent_flag
- source_column
- notes

### 5. `growth_event`

A unified event stream for learning follow-up, conduct, class duties, and positive recognition.

Suggested fields:

- title
- student_ref
- event_date
- domain
- event_type
- evaluation
- tags
- score_delta
- description
- evidence
- recorder
- status

### 6. `parent_contact`

For calls, messages, visits, and follow-up tasks.

Suggested fields:

- subject
- student_ref
- contact_date
- channel
- counterpart
- summary
- next_action
- status
- attachments

### 7. `seat_assignment`

Suggested fields:

- version
- student_ref
- effective_date
- row
- column
- zone
- deskmate
- reason
- active_flag

### 8. `duty_assignment`

Suggested fields:

- title
- student_ref
- cycle_start
- cycle_end
- role
- group_name
- leader_flag
- replacement_note
- makeup_status

### 9. `committee_assignment`

Suggested fields:

- role_name
- student_ref
- start_date
- end_date
- active_flag
- notes

### 10. `artifact_record`

Suggested fields:

- artifact_title
- artifact_type
- related_entity
- template_name
- local_path
- remote_url
- created_at
- sync_status
- params_summary

## Migration note

If the user provides an existing subject-teacher Base:

- treat mixed score columns as import material, not as the final model
- unpivot subject-specific score columns into `score_detail`
- migrate generic activity logs into `growth_event`

## Backend mapping

- Feishu Base: fully implemented in v1
- Notion: database/page structure only in v1
- Obsidian: folders/templates only in v1

## Artifact generation note

The standard model should support at least these downstream generation tasks:

- seat plans or duty schedules arranged by selected student attributes
- parent meeting PPT generated from score records plus daily performance records
- notices, visit records, and talk records generated from structured context

---
name: learning-path-designer
description: >
  Use this skill when an L&D professional, instructional designer, HR business partner,
  or corporate training manager needs to design a structured learning path for a role,
  competency gap, or upskilling initiative. Covers competency gap analysis, Bloom's
  taxonomy–aligned objective writing, modality selection, module sequencing, and
  assessment design. Produces a DRAFT learning path curriculum map for L&D-lead review
  before content development begins.
---

# Learning Path Designer

Build structured, competency-aligned corporate learning paths that connect skill gaps to learning objectives, content modalities, and measurable outcomes — before committing to content development.

## Flow

### Phase 1 — Learner and Context Intake

Ask one question at a time:
1. Target audience: job title, level (individual contributor / manager / senior leader), and department
2. Business driver: new hire onboarding / upskilling / role transition / compliance / leadership development / certification prep
3. Organization and industry context (affects whether regulatory compliance modules must be flagged as mandatory)
4. Existing content inventory: list any courses, job aids, videos, or SME sessions already available that may be reused
5. Constraints: maximum hours per week available for learning, preferred modalities (eLearning / VILT / OJT / hybrid), LMS platform if known
6. Target completion date or rollout milestone

### Phase 2 — Competency and Skill Gap Definition

Ask the user to provide a competency model or role profile, or prompt them to define competencies directly.

For each competency, collect:
- Competency name
- Current proficiency level of the target learner: Novice / Developing / Proficient / Expert
- Target proficiency level required
- Source of the gap data (manager assessment, skill survey, performance review, certification requirement)

Build and display the Competency Gap Matrix:

| Competency | Current Level | Target Level | Gap | Priority |

Ask for confirmation before continuing. If a gap exists for a regulated topic (safety, financial, clinical, data privacy), flag that module as mandatory compliance training.

### Phase 3 — Learning Objective Writing

For each high-priority gap, write 1–3 learning objectives using Bloom's taxonomy verbs matched to the target proficiency level:

- Novice → Remember / Understand: define, describe, identify, explain, recognize
- Developing → Apply / Analyze: use, demonstrate, compare, classify, differentiate
- Proficient → Evaluate / Create: design, assess, construct, critique, build

Objective format: "Upon completing this module, the learner will be able to [Bloom's verb] [knowledge or skill] [condition or standard]."

Display objectives for each competency and ask for feedback before proceeding.

### Phase 4 — Module Design

For each objective or objective cluster, define one module:
- Module title (action-oriented, clear)
- Competency covered
- Learning objective(s)
- Recommended modality: eLearning / VILT / on-the-job task / job aid / coaching / assessment / simulation / microlearning
- Estimated duration (label as "Estimated")
- Prerequisites (other modules that must come first)
- Existing content mapped from Phase 1 inventory (if any)
- Content status: Existing / Build / Buy / Curate

Flag all compliance-mandatory modules prominently.

### Phase 5 — Learning Path Sequencing

Arrange modules into a recommended sequence using these rules:
1. Foundational modules before advanced modules (prerequisite dependencies respected)
2. Scaffolded progression within each competency cluster (simple to complex)
3. Practice and application modules after conceptual modules
4. Culminating assessment or performance task at the end

Produce a Learning Path Sequence Table:

| Week / Sprint | Module Title | Modality | Duration | Competency | Objective | Content Status |

### Phase 6 — Assessment Design

For each competency cluster, define:
- Formative check: quiz, reflection prompt, or scenario embedded within the module
- Summative assessment: performance task, certification exam, manager observation rubric, or 360-degree feedback item
- Proficiency unlock criteria: what score or observable behavior signals "Proficient achieved"
- Kirkpatrick evaluation level targeted: 1 Reaction / 2 Learning / 3 Behavior / 4 Results

### Phase 7 — DRAFT Learning Path Assembly

Produce the full DRAFT learning path document in this order:
1. Learning Path Overview (audience, business driver, total estimated duration, rollout date)
2. Competency Gap Matrix
3. Learning Objectives by competency
4. Module Catalog (all modules with modality, duration, prerequisites, content status)
5. Sequenced Learning Path Table
6. Assessment Plan (formative + summative per competency, Kirkpatrick level)
7. Build / Buy / Curate Task List (all modules not marked Existing, with owner placeholder)
8. L&D Lead Review Block

Add this block at the end:

```
DRAFT — L&D LEAD REVIEW REQUIRED
Reviewed by: _________________________ Date: ________

This learning path must be reviewed by a qualified L&D professional before
content development begins. Duration estimates are preliminary.
```

## Key Rules

- **One question at a time**: Never ask for multiple pieces of information in a single prompt.
- **Bloom's accuracy**: Match Bloom's level to the target proficiency — do not use Evaluate or Create objectives for Novice learners.
- **Existing content first**: Before recommending new builds, always check whether existing content from the Phase 1 inventory can be mapped or adapted.
- **Compliance modules are mandatory**: If the role or industry context triggers required regulatory training (OSHA, HIPAA, financial licensing, data privacy), flag these modules as mandatory and sequence them before role-specific content.
- **Duration honesty**: Label all time estimates as "Estimated" — actual durations depend on content design decisions made later.
- **Scope boundary**: This skill designs the plan; it does not create course content, eLearning scripts, facilitator guides, or assessment items. Recommend next steps for content development after delivery.
- **K-12 scope**: This skill is for corporate and professional development. For K-12 lesson planning, use `education/lesson-plan-architect`.

## Output Format

DRAFT learning path document containing:
- Competency Gap Matrix (current vs. target proficiency per competency)
- Learning objectives (Bloom's taxonomy–aligned per gap)
- Module catalog (modality, duration, prerequisites, content status)
- Sequenced Learning Path Table (week/sprint view)
- Assessment plan (formative + summative per competency cluster, Kirkpatrick level)
- Build/buy/curate task list with owner placeholders
- L&D lead review block

## Feedback

If you encounter a specialized compliance framework, non-corporate education context, or LMS constraint this skill doesn't handle, share it at https://github.com/archlab-space/Open-Skill-Hub/issues.

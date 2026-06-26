---
name: organizer
description: >
  Organize information, tasks, ideas, projects, notes, files, workflows, and priorities
  into clear structures that are easier to understand and act on. Use when someone needs
  order, categorization, simplification, or a usable system instead of scattered inputs.
---

# Organizer

Organization is not about making things look tidy.

It is about making things easier to understand, navigate, decide, and use.

Most disorder is not caused by having too much information.
It is caused by having no structure for what matters, what belongs together,
what should happen next, and what can be ignored.

This skill helps turn scattered material into practical order.

## Trigger Conditions

Use this skill when the user needs to:
- organize notes, ideas, tasks, files, or projects
- sort information into categories or systems
- structure messy inputs into a usable format
- clean up a workflow, board, tracker, or document set
- create naming, grouping, or hierarchy logic
- reduce clutter and improve findability
- turn raw information into an organized operating system
- build a repeatable structure for ongoing work

Also trigger when the user says things like:
- "Help me organize this"
- "This is messy"
- "How should I structure this"
- "Put this in order"
- "I need a better system"
- "How do I categorize this"
- "Turn this into something usable"

## Core Principle

A good organizing system does not merely sort things.

It makes future action easier.

The test of organization is not whether it looks neat.
It is whether someone can quickly find what they need, understand the structure,
and know what to do next.

## What This Skill Does

This skill helps:
- define organizing logic before rearranging content
- group items by function, meaning, priority, or workflow
- create categories, folders, tags, sections, or hierarchies
- separate active material from archive material
- reduce duplication, clutter, and confusion
- improve usability, visibility, and maintenance
- turn scattered collections into clearer working systems

## Default Outputs

Depending on the request, produce one or more of the following:

1. Organization System  
A proposed structure showing categories, groups, levels, and logic.

2. Folder or Section Architecture  
A practical hierarchy for files, notes, projects, or resources.

3. Cleanup Plan  
A step-by-step method for sorting, merging, archiving, and simplifying.

4. Categorization Framework  
Rules for how items should be grouped and labeled.

5. Workflow Organizer  
A structure that arranges work by stage, ownership, or priority.

6. Organization Audit  
A diagnosis of why the current system feels cluttered, confusing, or hard to maintain.

## Response Rules

When responding:
- define what is being organized
- identify what decisions the structure should support
- choose organizing logic before creating categories
- reduce clutter instead of moving clutter around
- separate active, reference, and archived material when useful
- prefer simple systems that can be maintained
- make labels intuitive and distinct
- optimize for usability, not aesthetic over-design

## Organizer Architecture
~~~python
ORGANIZER_ARCHITECTURE = {
  "core_elements": {
    "object": "What is being organized",
    "purpose": "Why it needs to be organized",
    "logic": "The principle used for grouping and structure",
    "containers": "Folders, categories, sections, boards, or groups",
    "labels": "How items are named and distinguished",
    "states": "Active, pending, reference, archive, or other meaningful conditions",
    "maintenance": "How the system stays usable over time"
  },
  "guiding_questions": [
    "What exactly is being organized",
    "What should become easier after organizing",
    "What belongs together and why",
    "What should stay active versus archived",
    "What labels will make sense later",
    "How much complexity can the user realistically maintain"
  ]
}
~~~

## Organizer Workflow
~~~python
ORGANIZER_WORKFLOW = {
  "step_1_define_object": {
    "purpose": "Clarify what needs structure",
    "examples": [
      "notes",
      "files",
      "ideas",
      "tasks",
      "projects",
      "research material",
      "client records",
      "content pipeline"
    ]
  },
  "step_2_define_purpose": {
    "purpose": "Clarify what the organization system should improve",
    "examples": [
      "findability",
      "clarity",
      "faster execution",
      "better review",
      "reduced duplication",
      "easier handoff"
    ]
  },
  "step_3_choose_logic": {
    "purpose": "Select the organizing principle",
    "options": [
      "by project",
      "by client",
      "by workflow stage",
      "by topic",
      "by priority",
      "by time horizon",
      "by reference vs action"
    ]
  },
  "step_4_group_items": {
    "purpose": "Create clear containers",
    "rules": [
      "Categories should be distinct enough to reduce confusion",
      "Too many containers create maintenance drag",
      "Use broad buckets first, then refine only when needed"
    ]
  },
  "step_5_define_labels_and_states": {
    "purpose": "Make the system readable and actionable",
    "outputs": [
      "naming rules",
      "status labels",
      "archive rules",
      "priority markers",
      "review markers"
    ]
  },
  "step_6_define_maintenance": {
    "purpose": "Keep the system from decaying",
    "methods": [
      "weekly cleanup",
      "archive completed items",
      "merge duplicates",
      "remove dead categories",
      "review naming consistency"
    ]
  }
}
~~~

## Common Organizer Types
~~~python
ORGANIZER_TYPES = {
  "file_organizer": {
    "use_when": "The user needs structure for folders and files",
    "focus": ["folder hierarchy", "naming conventions", "archive logic", "findability"]
  },
  "project_organizer": {
    "use_when": "The user needs to arrange ongoing work clearly",
    "focus": ["project buckets", "status grouping", "ownership", "priority"]
  },
  "note_organizer": {
    "use_when": "The user has scattered notes or ideas",
    "focus": ["topics", "reference vs action", "connections", "retrievability"]
  },
  "task_organizer": {
    "use_when": "The user needs order across tasks and commitments",
    "focus": ["priority", "context", "deadline", "next action", "review cadence"]
  },
  "content_organizer": {
    "use_when": "The user needs structure for ideas, drafts, and published assets",
    "focus": ["pipeline stage", "topic", "platform", "status", "reuse potential"]
  },
  "operations_organizer": {
    "use_when": "The user needs system order for recurring business work",
    "focus": ["workflow grouping", "owners", "SOP sections", "handoff clarity"]
  }
}
~~~

## Organization Logic
~~~python
ORGANIZATION_LOGIC = {
  "principles": [
    "Organize for retrieval and action, not just storage",
    "Every category should answer a practical question",
    "Archive aggressively when items no longer need active attention",
    "Labels should still make sense after time passes",
    "Simple systems survive better than clever systems",
    "Good organization reduces both confusion and maintenance effort"
  ],
  "common_failures": [
    "Too many categories",
    "Overlapping labels",
    "No archive layer",
    "Everything kept active forever",
    "Systems built around ideal behavior rather than real behavior",
    "Rearranging without deciding the underlying logic"
  ],
  "corrections": [
    "Choose one primary organizing principle",
    "Reduce the number of active buckets",
    "Separate active, reference, and archive",
    "Use plain-language labels",
    "Define maintenance rules before scale creates chaos"
  ]
}
~~~

## Organizer Output Format

### Organization Summary
- Object Being Organized:
- Purpose of Organization:
- Organizing Logic:
- Main Categories or Sections:
- Labeling Rules:
- Active vs Archive Rules:
- Maintenance Process:
- Risks or Confusion Points:
- Recommended Next Step:

## Boundaries

This skill helps design and improve organizing systems, structures, and categorization logic.

It does not replace legal, compliance, records-retention, accounting, HR, or regulated
information-governance advice. For sensitive or regulated environments, outputs should be
adapted to the user's jurisdiction, industry requirements, and internal policies.

## Quality Check Before Delivering

- [ ] The object being organized is clearly defined
- [ ] The organizing purpose is explicit
- [ ] A primary organizing logic is chosen
- [ ] Categories are distinct and usable
- [ ] Labels are simple and durable
- [ ] Active and archive rules are clear
- [ ] Maintenance is realistic
- [ ] The next step is concrete

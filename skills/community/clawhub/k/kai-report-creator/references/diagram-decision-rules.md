# Diagram Decision Rules

Load this file whenever a diagram or diagram-like structure is being considered.

## Core Rule

Only draw a diagram when it materially reduces comprehension cost.

If the same idea is already clear in one short paragraph or list, keep it as prose.

## Go / No-Go Check

Use a diagram only when the content is primarily about one or more of these relationship types:

- `directionality`
- `dependency`
- `branching`

These are the cases where a diagram can remove ambiguity instead of adding visual ceremony.

## No-Go Cases

Parallel points should stay as prose or list.

Three to five principles should stay as prose or list.

If prose explains it clearly, do not draw a diagram.

If the structure is only "a few named buckets", prefer prose, `callout`, or `list`.

## Type Selection

- Use `sequence` only when the message flow between actors matters.
- Use `flowchart` only when the reader must follow a path, branch, or decision tree.
- Use `tree` only when the hierarchy itself is the message.
- Use `mindmap` only when the center-to-branch expansion is truly the useful structure.

## Downgrade Rule

Preferred downgrade: `callout` or `list`.

When the content is still useful but not diagram-worthy, keep the content and downgrade the component rather than forcing a schematic shape.

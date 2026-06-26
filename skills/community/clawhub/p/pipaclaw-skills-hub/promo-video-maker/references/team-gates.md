# Team Gates

## Stage list

- `intake`
- `project-select-or-create`
- `quote`
- `story`
- `character`
- `scene`
- `storyboard`
- `audio`
- `video`
- `assembly`
- `review`
- `poll`
- `handoff`

## Gate rules

### Leave `intake` only when:
- the output type is known
- the mode is known or explicitly assumed
- there is enough brief detail to quote the next step

### Leave `project-select-or-create` only when:
- an existing project is selected
- or a new project is created
- or the task is confirmed as `one-shot`

### Leave `quote` only when:
- estimated credits are shown
- the next paid step is clear
- budget blockers are visible

### Leave `story` only when:
- premise, structure, or script for the next downstream stage exists

### Leave `storyboard` only when:
- there is a usable shot/beat structure for generation or edit planning

### Leave `audio` only when:
- voice or BGM instructions are usable for execution

### Leave `video` only when:
- generation tasks are launched or a complete video output exists

### Leave `assembly` only when:
- the edit or composition result is persisted or explicitly marked as pending

### Leave `review` only when:
- the next action is obvious
- the user can either continue, revise, or open the workspace

## Failure handling

- `one-shot`: return task failure, reason, and retry path
- `project`: keep the project, mark the failed stage, and suggest resume or retry

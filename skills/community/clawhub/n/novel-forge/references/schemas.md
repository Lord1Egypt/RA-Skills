# Schemas

## Project state

```json
{
  "project": {
    "title": "",
    "genre": "",
    "audience": "",
    "targetChapters": 0,
    "chapterWordRange": [0, 0],
    "status": "draft|active|paused|completed",
    "executionMode": "single-agent|multi-agent",
    "premise": "",
    "tabooList": [],
    "bootstrapLocked": false,
    "latestChapterIndex": 0,
    "lastCheckpoint": "",
    "resumeFrom": "",
    "resumeMode": "new|continue|truncated|checkpoint"
  },
  "models": {
    "orchestrator": "provider/model-id",
    "worldbuilding": "provider/model-id|n/a",
    "characters": "provider/model-id|n/a",
    "outline": "provider/model-id|n/a",
    "style": "provider/model-id|n/a",
    "writer": "provider/model-id|n/a",
    "reviewer": "provider/model-id|n/a",
    "memory": "provider/model-id|n/a"
  },
  "canon": {
    "hard": [],
    "soft": [],
    "world": {},
    "characters": [],
    "timeline": [],
    "factions": []
  },
  "planning": {
    "outline": {},
    "batchOutline": {
      "windowStart": 0,
      "windowEnd": 0,
      "locked": false,
      "stale": false
    },
    "volumes": [],
    "chapters": [],
    "currentBeat": {},
    "partialDrafts": []
  },
  "style": {
    "candidates": [],
    "selected": "",
    "rules": []
  },
  "memory": {
    "fullSummary": "",
    "recentSummaries": [],
    "openLoops": [],
    "characterStates": {},
    "foreshadowing": [],
    "recoverySummary": "",
    "lastKnownState": ""
  }
}
```

## Character dossier

Required fields:
- name
- role
- appearance
- personality
- behavior logic
- goals
- secrets
- relationships
- growth arc
- speech pattern
- OOC red lines
- allowed exceptions
- function in story
- canon status (locked | soft | provisional)

## Chapter beat sheet

Required fields:
- chapter number
- chapter goal
- viewpoint
- time / place
- opening state
- conflict
- emotional movement
- key dialogue
- ending hook
- state deltas
- forbidden deviations
- relevant canon slice
- unresolved plot loops

## Recovery checkpoint

Use this when a chapter is truncated or a draft must be resumed.

Required fields:
- resume mode
- last stable sentence or beat
- known canon facts
- unknowns that must not be invented
- partial draft source
- next action
- user confirmation required

`state/current.json` should mirror the latest recovery checkpoint in a compact form so resume flows do not need to reconstruct it from multiple prose files. Treat it as a required write target after each accepted chapter.

## Review checklist

Check:
- bootstrap gate status
- canon consistency
- character consistency
- style consistency
- timeline consistency
- pacing
- hook strength
- beat adherence
- plot continuity
- whether any hard fact changed without author confirmation
- whether the resume state matches the last reliable checkpoint

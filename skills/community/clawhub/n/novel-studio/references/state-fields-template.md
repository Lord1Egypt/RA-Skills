# State Fields Template

Use this as a quick reference for important `.novel-state.json` fields.

```json
{
  "workflow": {
    "currentStage": "polishing",
    "currentSubstage": null,
    "lastCompletedStage": "drafting",
    "nextStage": "proofreading",
    "status": "awaiting_user_approval"
  },
  "approvals": {
    "discoveryApproved": true,
    "planningApproved": true,
    "characterApproved": true,
    "openingApproved": true,
    "draftingApproved": true,
    "polishingApproved": false,
    "proofreadingApproved": false,
    "finalApproved": false,
    "titleConfirmed": true,
    "workingTitleApproved": false
  },
  "artifacts": {
    "hotSearchScan": true,
    "userPreference": true,
    "topicReport": true,
    "trackDecision": true,
    "ideaDoc": true,
    "styleBible": true,
    "mainlineSpec": true,
    "outlineDoc": true,
    "characterSummary": true,
    "chapterSkeleton": true,
    "openingDesign": true,
    "recapDoc": true,
    "worldLedger": true,
    "foreshadowLedger": true,
    "relationshipLedger": true,
    "resourceLedger": true,
    "characterFiles": true,
    "manuscriptFiles": true,
    "feishuSynced": false
  },
  "batch": {
    "active": true,
    "chapterRange": "第1章",
    "chapterCount": 1,
    "scopeConfirmed": true,
    "chapterPlanExists": true,
    "chapterPlanApproved": true,
    "draftComplete": true,
    "polishingComplete": true,
    "proofreadingComplete": false,
    "recapUpdated": false,
    "awaitingNextBatchDecision": false,
    "focus": "开篇立钩子 + 主角气质建立",
    "attractionPoints": ["隐藏实力", "打脸前奏"],
    "climaxTarget": "第3章结尾反转",
    "chapterTasks": [
      {
        "chapterLabel": "第1章",
        "manuscriptPath": "manuscript/第1章_你配不上我.md",
        "phase": "polishing",
        "phaseStatus": "awaiting_user_review",
        "lastSummary": "第1章润色待审核",
        "blockers": [],
        "updatedAt": "2026-03-28T10:00:00Z"
      }
    ],
    "pendingProgressItems": []
  },
  "autoPilot": {
    "active": true,
    "goalChapter": "第10章",
    "goalCondition": "proofreading_completed",
    "startedAt": "2026-03-29T09:00:00Z",
    "startedBy": "后续你来主控，继续到第10章结束",
    "lastProgressAt": "2026-03-29T10:00:00Z",
    "lastProgressSummary": "第3章润色中",
    "stopReason": null,
    "stoppedAt": null,
    "awaitingManualResume": false
  },
  "review": {
    "currentGate": "waiting_polishing_feedback",
    "brainstormMode": "cliche_exhaustion",
    "brainstormFocus": "story_engine",
    "brainstormRound": "mutation",
    "selectedBranch": "story-planning/版本B",
    "lastUserFeedbackSummary": "语气还不够稳，主角魅力不足",
    "lastRevisionFocus": "加强主角吸引点和场景语气统一",
    "lastDriftRiskSummary": "第3章旁白开始变得过于中性",
    "lastLedgerRiskSummary": "黑箱权限变化尚未回填到资源账本",
    "lastRejectedReason": null,
    "finalDecision": "conditional pass",
    "finalDeliveryReady": false,
    "finalBlockingIssues": [
      "第12章收束仍偏弱，需要补强终局情绪"
    ],
    "finalReviewSummary": "整体可读性稳定，但仍有阻塞项，暂不建议交付"
  },
  "narrativeIntelligence": {
    "timeline": {
      "enabled": true,
      "lastUpdatedBatch": "第10章",
      "lastTouchedChapters": ["第10章"],
      "openTemporalRisks": []
    },
    "cfpg": {
      "foreshadowTriples": [],
      "tripleCounts": {
        "total": 0,
        "pending": 0,
        "fulfilled": 0,
        "broken": 0,
        "expired": 0
      },
      "lastUpdatedBatch": "第10章"
    },
    "theoryOfMind": {
      "characterBeliefs": [],
      "beliefConflicts": [],
      "lastUpdatedBatch": "第10章"
    },
    "consistency": {
      "contradictionCandidates": [],
      "evidenceChains": [],
      "lastCheckStage": "proofreading",
      "openCriticalIssues": []
    },
    "styleRisk": {
      "clichePatterns": ["重复使用隐藏实力钩子"],
      "lastCokeScore": 0.37,
      "noveltyAxes": ["规则显形方式", "主角解决问题的代价结构"],
      "lastClicheScanStage": "proofreading"
    },
    "revisionActions": []
  },
  "revision": {
    "active": true,
    "feedbackType": "plot_feedback",
    "feedbackSummary": "加强前三章羞辱感和翻盘钩子",
    "affectedStages": ["drafting", "polishing"],
    "affectedFiles": [
      "05_本轮章节规划.md",
      "manuscript/第1章_你配不上我.md"
    ],
    "overrideMode": "add_on",
    "scopeSummary": "回改本轮章节规划和第1章开篇节奏",
    "conflictSummary": "不覆盖既定主线，只加强开篇吸引力",
    "revisionPlanSummary": "先改规划，再改正文，再复核润色结论",
    "resultSummary": null,
    "currentRevisionGate": "awaiting_revision_plan_approval",
    "awaitingUserApproval": true,
    "lastClosedRevision": null
  },
  "notes": {
    "platformProfile": "起点模式",
    "primaryTrack": "规则异变都市",
    "secondaryFlavor": "悬疑调查",
    "styleBibleVersion": "v1"
  },
  "blockingIssues": [
    "Formal revision active: awaiting_revision_plan_approval"
  ]
}
```

Autopilot notes:
- `goalChapter` stores the normalized terminal chapter label, while `goalCondition` records the completion contract.
- `lastProgressAt` / `lastProgressSummary` capture the latest merged progress surfaced during automation.
- `stopReason` stays `null` while automation is active; when stopped, record explicit values such as `blocked: 人物口吻漂移`, `user_interruption`, or `goal_reached`.

Cliche Exhaustion Loop notes:
- branch selection, canonical backfill, and cleanup stay parent-owned supervisor actions.
- use staging branch artifacts as review scaffolding only; only a branch `05_定稿结论.md` may authorize canonical backfill.
- `brainstormMode` stays `cliche_exhaustion` in this slice.
- `brainstormRound` stores a round label such as `mutation` or `enumeration`, not a numeric counter.
- `selectedBranch` uses the stage-prefixed branch key form, for example `story-planning/版本B`.
- keep `review.brainstormMode`, `review.brainstormFocus`, `review.brainstormRound`, and `review.selectedBranch` explicit when the overlay is active.
- keep `narrativeIntelligence.styleRisk.noveltyAxes` and `narrativeIntelligence.styleRisk.lastClicheScanStage` explicit so later tasks extend one contract instead of inventing a new one.

Narrative-intelligence notes:
- `narrativeIntelligence.*` is parent-owned derived state. Subagents do not write these fields directly.
- `timeline` / `cfpg` / `theoryOfMind` refresh on accepted drafting, polishing, and proofreading results.
- accepted proofreading refresh also updates `consistency.*`; `openCriticalIssues` can stop autopilot and later fold into final-review blockers.

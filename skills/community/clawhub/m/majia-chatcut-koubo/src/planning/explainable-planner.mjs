const NARRATIVE_ROLES = [
  "hook",
  "problem",
  "contrast-or-example",
  "method",
  "result",
  "soft-cta",
];

function ratioDurationSeconds(words) {
  if (words.length === 0) return 0;
  const first = words[0].range;
  const last = words.at(-1).range;
  if (words.some((word) =>
    word.range.rate.numerator !== first.rate.numerator
    || word.range.rate.denominator !== first.rate.denominator
  )) {
    throw new TypeError("planner requires a single transcript timebase");
  }
  return (
    (last.end - first.start)
    * first.rate.denominator
    / first.rate.numerator
  );
}

function signal(signalId, kind, value, unit, basisRefs) {
  return {signalId, kind, value, unit, basisRefs};
}

function pendingApproval() {
  return {required: true, status: "pending"};
}

function decision(decisionId, kind, subjectRef, reasonCodes, evidenceRefs) {
  return {
    decisionId,
    kind,
    subjectRef,
    reasonCodes,
    evidenceRefs: [...new Set(evidenceRefs)].sort(),
    approval: pendingApproval(),
  };
}

export function buildExplainableScorecard(
  transcript,
  editPlan,
  {scorecardId = "content_scorecard_001", lowConfidence = 0.85} = {},
) {
  if (
    transcript.projectId !== editPlan.projectId
    || transcript.transcriptId !== editPlan.transcriptId
    || transcript.revision !== editPlan.transcriptRevision
  ) {
    throw new TypeError("planner input revisions do not match");
  }
  const wordById = new Map(
    transcript.words.map((word) => [word.wordId, word]),
  );
  const keptSegments = editPlan.segments
    .filter((segment) => segment.action === "keep")
    .toSorted((left, right) => left.order - right.order);
  const keptWordIds = [...new Set(
    keptSegments.flatMap((segment) => segment.sourceWordIds),
  )];
  const openingWords = transcript.words.filter((word) => {
    const seconds = (
      word.range.start
      * word.range.rate.denominator
      / word.range.rate.numerator
    );
    return seconds < 60;
  });
  const lowConfidenceWords = transcript.words.filter(
    (word) => word.confidence < lowConfidence,
  );
  const riskWords = transcript.words.filter(
    (word) => word.riskFlags.some((flag) => flag !== "none"),
  );
  const evidenceWords = transcript.words.filter(
    (word) => word.evidenceRefs.length > 0,
  );
  const durationSeconds = ratioDurationSeconds(openingWords);
  const removedSegments = editPlan.segments.filter(
    (segment) => segment.action === "remove",
  );
  const reorderedSegments = editPlan.segments.filter(
    (segment) => segment.action === "reorder",
  );

  const signals = [
    signal(
      "signal_total_words",
      "total-words",
      transcript.words.length,
      "count",
      transcript.words.map((word) => word.wordId),
    ),
    signal(
      "signal_kept_words",
      "kept-words",
      keptWordIds.length,
      "count",
      keptWordIds,
    ),
    signal(
      "signal_opening_words",
      "opening-words",
      openingWords.length,
      "count",
      openingWords.map((word) => word.wordId),
    ),
    signal(
      "signal_opening_density",
      "opening-density",
      durationSeconds === 0 ? 0 : openingWords.length / durationSeconds,
      "words-per-second",
      openingWords.map((word) => word.wordId),
    ),
    signal(
      "signal_low_confidence",
      "low-confidence-words",
      lowConfidenceWords.length,
      "count",
      lowConfidenceWords.map((word) => word.wordId),
    ),
    signal(
      "signal_content_risk",
      "risk-flagged-words",
      riskWords.length,
      "count",
      riskWords.map((word) => word.wordId),
    ),
    signal(
      "signal_evidence_coverage",
      "evidence-coverage",
      transcript.words.length === 0
        ? 0
        : evidenceWords.length / transcript.words.length,
      "ratio",
      evidenceWords.map((word) => word.wordId),
    ),
    signal(
      "signal_removed_segments",
      "removed-segments",
      removedSegments.length,
      "count",
      removedSegments.map((segment) => segment.segmentId),
    ),
    signal(
      "signal_reordered_segments",
      "reordered-segments",
      reorderedSegments.length,
      "count",
      reorderedSegments.map((segment) => segment.segmentId),
    ),
  ];

  const narrativeCandidates = keptSegments
    .slice(0, NARRATIVE_ROLES.length)
    .map((segment, index) => ({
      candidateId: `narrative_candidate_${String(index + 1).padStart(3, "0")}`,
      role: NARRATIVE_ROLES[index],
      sourceSegmentId: segment.segmentId,
      sourceWordIds: [...segment.sourceWordIds],
      currentOrder: segment.order,
      suggestedOrder: index + 1,
      rationaleCodes: [
        "POSITIONAL_CANDIDATE_ONLY",
        "SOURCE_CONTENT_REUSED",
        "HUMAN_SEMANTIC_REVIEW_REQUIRED",
      ],
      inventedContent: false,
      approval: pendingApproval(),
    }));

  const decisionQueue = narrativeCandidates.map((candidate, index) =>
    decision(
      `decision_narrative_${String(index + 1).padStart(3, "0")}`,
      "narrative-role",
      candidate.sourceSegmentId,
      ["HUMAN_SEMANTIC_REVIEW_REQUIRED"],
      candidate.sourceWordIds.flatMap(
        (wordId) => wordById.get(wordId)?.evidenceRefs ?? [],
      ),
    ));
  for (const word of lowConfidenceWords) {
    decisionQueue.push(decision(
      `decision_confidence_${word.wordId}`,
      "low-confidence",
      word.wordId,
      ["LOW_CONFIDENCE_SOURCE_WORD"],
      word.evidenceRefs,
    ));
  }
  for (const word of riskWords) {
    decisionQueue.push(decision(
      `decision_risk_${word.wordId}`,
      "content-risk",
      word.wordId,
      ["CONTENT_RISK_REQUIRES_REVIEW"],
      word.evidenceRefs,
    ));
  }
  for (const segment of [...removedSegments, ...reorderedSegments]) {
    decisionQueue.push(decision(
      `decision_edit_${segment.segmentId}`,
      "destructive-edit",
      segment.segmentId,
      ["DESTRUCTIVE_EDIT_REQUIRES_APPROVAL"],
      segment.sourceWordIds.flatMap(
        (wordId) => wordById.get(wordId)?.evidenceRefs ?? [],
      ),
    ));
  }

  return {
    $schema: "https://github.com/maojiebc/majia-chatcut-koubo/schemas/content-scorecard.schema.json",
    schemaVersion: "1.0.0",
    scorecardId,
    projectId: transcript.projectId,
    transcriptId: transcript.transcriptId,
    transcriptRevision: transcript.revision,
    editPlanId: editPlan.planId,
    method: "deterministic-structural-v1",
    signals,
    narrativeCandidates,
    decisionQueue,
    predictionPolicy: {
      viralityProbability: "not-produced",
      generatedText: false,
    },
  };
}

export function auditExplainableScorecard(
  scorecard,
  transcript,
  editPlan,
) {
  const findings = [];
  const expected = buildExplainableScorecard(
    transcript,
    editPlan,
    {scorecardId: scorecard.scorecardId},
  );
  if (JSON.stringify(scorecard) !== JSON.stringify(expected)) {
    findings.push({
      code: "PLANNER_SCORECARD_DRIFT",
      pointer: "/",
      severity: "error",
    });
  }
  return {
    status: findings.length === 0 ? "passed" : "failed",
    scorecardId: scorecard.scorecardId,
    findings,
  };
}

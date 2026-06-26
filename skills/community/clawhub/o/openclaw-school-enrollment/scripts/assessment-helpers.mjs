export const phaseOrder = [
  "baseline_testing",
  "course_resolving",
  "package_fetching",
  "supplies_procuring",
  "package_installing",
  "capability_activating",
  "graduation_testing",
  "graduation_ready"
];

export function resolvePreviousPhase(phase) {
  const index = phaseOrder.indexOf(phase);

  if (index === 0) {
    return "enrollment_reporting";
  }

  if (index > 0) {
    return phaseOrder[index - 1];
  }

  throw new Error(`Unknown phase: ${phase}`);
}

const assessmentRangeMap = {
  baseline: {
    minScore: 40,
    maxScore: 65
  },
  graduation: {
    minScore: 70,
    maxScore: 90
  }
};

export function pickAssessmentScore(min, max, random = Math.random) {
  return Math.floor(random() * (max - min + 1)) + min;
}

export function resolveAssessmentRange({ kind, score, reused }) {
  if (kind === "baseline" && reused) {
    return {
      minScore: score,
      maxScore: score
    };
  }

  return assessmentRangeMap[kind];
}

export function buildAssessmentMessages({ kind, score, reused }) {
  if (kind === "baseline") {
    return {
      started: "已开始入学测试。",
      completed: reused
        ? `入学测试完成，沿用首次入学测试成绩 ${score} 分。`
        : `入学测试完成，当前得分 ${score} 分。`
    };
  }

  return {
    started: "已开始毕业测试。",
    completed: `毕业测试完成，当前得分 ${score} 分。`
  };
}

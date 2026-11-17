import {contentHash} from "../planning/preview-approval.mjs";

function clampRange(startSec, endSec, durationSec) {
  const start = Math.max(0, Math.min(durationSec, startSec));
  const end = Math.max(start, Math.min(durationSec, endSec));
  return {startSec: start, endSec: end};
}

function score(candidate) {
  return (candidate.complexity ?? 0)
    + (candidate.privacy ? 100 : 0)
    + (candidate.kind === "retake" ? 20 : 0)
    + (candidate.kind === "pause" ? 10 : 0);
}

function addWindow(windows, candidate) {
  const existing = windows.find((item) =>
    item.windowRef === candidate.windowRef
    || (item.startSec === candidate.startSec && item.endSec === candidate.endSec),
  );
  if (existing) {
    existing.coverage = [...new Set([
      existing.reason,
      ...(existing.coverage ?? []),
      candidate.reason,
    ])];
    return;
  }
  windows.push(candidate);
}

export function selectRepresentativeWindows({
  durationSec,
  candidates = [],
  hasScreenCapture = false,
  samplePolicy = null,
} = {}) {
  if (!Number.isFinite(durationSec) || durationSec <= 0) {
    throw new Error("PREVIEW_DURATION_INVALID");
  }
  const openingSec = samplePolicy?.openingSec ?? (durationSec <= 180 ? 30 : 60);
  const windows = [{
    windowRef: "logical:sample-opening",
    reason: "opening",
    ...clampRange(0, openingSec, durationSec),
  }];
  const ranked = [...candidates].sort((left, right) => score(right) - score(left) || left.startSec - right.startSec);
  const complex = ranked[0];
  if (complex && samplePolicy?.includeComplexWindow !== false) {
    addWindow(windows, {
      windowRef: `logical:${complex.id}`,
      reason: "complex-cut",
      ...clampRange(complex.startSec, complex.endSec, durationSec),
    });
  }
  for (const kind of ["retake", "pause"]) {
    const candidate = ranked.find((item) => item.kind === kind);
    if (candidate) {
      addWindow(windows, {
        windowRef: `logical:${candidate.id}`,
        reason: kind === "retake" ? "retake-cut" : "pause-treatment",
        ...clampRange(candidate.startSec, candidate.endSec, durationSec),
      });
    }
  }
  const privacyCandidates = ranked.filter((item) => item.privacy);
  for (const candidate of privacyCandidates) {
    addWindow(windows, {
      windowRef: `logical:${candidate.id}`,
      reason: "privacy-and-screen",
      ...clampRange(candidate.startSec, candidate.endSec, durationSec),
    });
  }
  if (hasScreenCapture && privacyCandidates.length === 0) {
    addWindow(windows, {
      windowRef: "logical:screen-privacy-review",
      reason: "privacy-review-required",
      ...clampRange(0, Math.min(durationSec, openingSec), durationSec),
    });
  }
  if (samplePolicy?.includeEnding === true || (!samplePolicy && durationSec > 600)) {
    addWindow(windows, {
      windowRef: "logical:sample-ending",
      reason: "ending",
      ...clampRange(durationSec - 10, durationSec, durationSec),
    });
  }
  return windows;
}

export function createSampleFingerprint({
  plan,
  style,
  layout,
  captions,
  timelineRevision,
  windows,
} = {}) {
  return {
    plan: contentHash(plan),
    style: contentHash(style),
    layout: contentHash(layout),
    captions: contentHash(captions),
    timelineRevision,
    sample: contentHash({windows, plan, style, layout, captions, timelineRevision}),
  };
}

export function sampleApprovalCard({decisions = [], treatments = {}} = {}) {
  const removed = decisions.filter((item) => item.status === "applied" && item.action.includes("remove")).length;
  const paused = decisions.filter((item) => item.type === "pause" && item.status === "applied").length;
  const protectedCount = decisions.filter((item) => item.status !== "applied" && item.approvalRequired).length;
  return {
    title: "代表样片已做好",
    handled: [
      `处理 ${removed} 处明显口误或重说`,
      `压缩 ${paused} 处长停顿`,
      `保留 ${protectedCount} 个需要你决定的内容点`,
      treatments.captions ? "样片局部字幕仅供确认，整片字幕会在结构锁定后生成" : "本次未做字幕",
    ],
    notPerformed: ["未重排观点", "未添加音乐、动态图形或补充画面", "未导出"],
    choices: ["继续整片", "再自然一点", "再紧一点", "查看高风险项"],
  };
}

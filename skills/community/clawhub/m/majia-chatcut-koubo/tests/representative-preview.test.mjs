import assert from "node:assert/strict";
import test from "node:test";

import {
  createSampleFingerprint,
  sampleApprovalCard,
  selectRepresentativeWindows,
} from "../src/orchestration/preview-selector.mjs";

test("短片开场样片为 30 秒，中长片为 60 秒", () => {
  const short = selectRepresentativeWindows({durationSec: 90});
  assert.deepEqual(short[0], {
    windowRef: "logical:sample-opening",
    reason: "opening",
    startSec: 0,
    endSec: 30,
  });
  const medium = selectRepresentativeWindows({durationSec: 181});
  assert.equal(medium[0].endSec, 60);
});

test("Profile 样片策略会控制开场长度与片尾窗口", () => {
  const windows = selectRepresentativeWindows({
    durationSec: 120,
    samplePolicy: {openingSec: 20, includeComplexWindow: true, includeEnding: true},
  });
  assert.equal(windows[0].endSec, 20);
  assert.equal(windows.at(-1).reason, "ending");
});

test("超过十分钟的长片包含片尾窗口", () => {
  const windows = selectRepresentativeWindows({durationSec: 601});
  assert.deepEqual(windows.at(-1), {
    windowRef: "logical:sample-ending",
    reason: "ending",
    startSec: 591,
    endSec: 601,
  });
  assert.equal(selectRepresentativeWindows({durationSec: 600}).some((item) => item.reason === "ending"), false);
});

test("代表样片覆盖复杂切点、重说、停顿和隐私窗口", () => {
  const windows = selectRepresentativeWindows({
    durationSec: 720,
    hasScreenCapture: true,
    candidates: [
      {id: "pause-1", kind: "pause", startSec: 50, endSec: 53, complexity: 20},
      {id: "retake-1", kind: "retake", startSec: 100, endSec: 105, complexity: 40},
      {id: "privacy-1", kind: "privacy", startSec: 200, endSec: 204, complexity: 10, privacy: true},
      {id: "privacy-2", kind: "privacy", startSec: 300, endSec: 304, complexity: 8, privacy: true},
    ],
  });
  const reasons = new Set(windows.flatMap((item) => [item.reason, ...(item.coverage ?? [])]));
  for (const reason of ["opening", "complex-cut", "retake-cut", "pause-treatment", "privacy-and-screen", "ending"]) {
    assert.ok(reasons.has(reason), reason);
  }
  assert.equal(windows.filter((item) => item.reason === "privacy-and-screen" || item.coverage?.includes("privacy-and-screen")).length, 2);
  assert.equal(new Set(windows.map((item) => `${item.startSec}:${item.endSec}`)).size, windows.length);
});

test("窗口范围被夹在素材时长内且非法时长拒绝", () => {
  const windows = selectRepresentativeWindows({
    durationSec: 20,
    candidates: [{id: "outside", kind: "retake", startSec: -5, endSec: 50, complexity: 1}],
  });
  assert.ok(windows.every((item) => item.startSec >= 0 && item.endSec <= 20));
  for (const durationSec of [0, -1, Number.NaN, Number.POSITIVE_INFINITY]) {
    assert.throws(() => selectRepresentativeWindows({durationSec}), /PREVIEW_DURATION_INVALID/u);
  }
});

test("样片 fingerprint 对相同输入稳定，对任一批准维度变化敏感", () => {
  const base = {
    plan: [{action: "remove-false-start"}],
    style: {pacing: "balanced"},
    layout: {states: ["A"]},
    captions: {enabled: true},
    timelineRevision: "rev-current",
    windows: [{windowRef: "logical:sample-opening", startSec: 0, endSec: 30}],
  };
  const first = createSampleFingerprint(base);
  assert.deepEqual(createSampleFingerprint(structuredClone(base)), first);
  for (const [key, value] of [
    ["plan", [{action: "keep"}]],
    ["style", {pacing: "tight"}],
    ["layout", {states: ["A", "B"]}],
    ["captions", {enabled: false}],
    ["timelineRevision", "rev-new"],
  ]) {
    const changed = createSampleFingerprint({...base, [key]: value});
    assert.notEqual(changed[key], first[key], key);
    assert.notEqual(changed.sample, first.sample, `${key}:sample`);
  }
});

test("确认卡明确默认未做增强、重排与导出", () => {
  const card = sampleApprovalCard({
    decisions: [{
      type: "false-start",
      action: "remove-false-start",
      status: "applied",
      approvalRequired: false,
    }],
    treatments: {captions: true},
  });
  assert.equal(card.title, "代表样片已做好");
  assert.ok(card.notPerformed.some((item) => item.includes("未重排")));
  assert.ok(card.notPerformed.some((item) => item.includes("音乐")));
  assert.ok(card.notPerformed.some((item) => item.includes("未导出")));
  assert.ok(card.choices.includes("继续整片"));
});

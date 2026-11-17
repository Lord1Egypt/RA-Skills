import assert from "node:assert/strict";
import test from "node:test";
import {preflightSession} from "../src/orchestration/session-preflight.mjs";
import {routeOfficialSkills} from "../src/orchestration/official-skill-router.mjs";

const NOW = "2026-09-30T08:00:00Z";
const treatments = {arollCleanup: true, smoothAudio: true, captions: true};
function observation(overrides = {}) {
  return {
    surface: "hosted", skillSource: "hosted-plugin",
    skills: ["chatcut-plugin-basics", "talking-head-guide", "verification", "transcription"],
    capabilities: ["project-read", "timeline-read", "timeline-write", "transcript-read", "speech-edit", "caption-read", "caption-write", "composed-preview"],
    observedAt: "2026-09-30T07:59:00Z", expiresAt: "2026-09-30T08:59:00Z",
    toolSchemaFingerprint: `sha256:${"a".repeat(64)}`, provenance: "live", ...overrides,
  };
}
const check = (overrides = {}) => preflightSession({observation: observation(), treatments, now: NOW, ...overrides});
const codes = (result) => result.findings.map((item) => item.code);

test("缺少会话时不根据版本或空能力表推断就绪", () => {
  const result = check({observation: null});
  assert.equal(result.contractReady, false);
  assert.equal(result.surface, "unknown");
  assert.ok(codes(result).includes("SESSION_OBSERVATION_REQUIRED"));
});

test("当前 hosted 会话只证明声明的合同齐全，不证明媒体或生产稳定", () => {
  const result = check();
  assert.equal(result.contractReady, true);
  assert.equal(result.verificationScope, "declared-session-contract");
  assert.equal(result.mediaVerified, false);
  assert.equal(result.stableClaimEligible, false);
});

test("Desktop 使用自身指令，不要求或回退到 hosted Skills", () => {
  const result = check({observation: observation({surface: "desktop", skillSource: "signed-desktop", skills: []})});
  assert.equal(result.contractReady, true);
  assert.deepEqual(result.route.required, []);
  assert.equal(result.route.instructionSource, "current-desktop-instructions");
  assert.equal(check({surface: "hosted", observation: observation({surface: "desktop", skillSource: "signed-desktop"})}).contractReady, false);
  assert.ok(codes(check({observation: observation({surface: "desktop"})})).includes("SESSION_SKILL_SOURCE_MISMATCH"));
});

test("能力缺失、过期、未来时间、超长有效期和模拟记录都不得放行", () => {
  const inputs = [
    [{capabilities: ["project-read"]}, "SESSION_CAPABILITY_MISSING"],
    [{skills: []}, "SESSION_SKILL_MISSING"],
    [{expiresAt: NOW}, "SESSION_OBSERVATION_STALE"],
    [{observedAt: "2026-10-01T08:00:00Z"}, "SESSION_OBSERVATION_STALE"],
    [{expiresAt: "2026-10-10T08:00:00Z"}, "SESSION_OBSERVATION_STALE"],
    [{provenance: "simulation"}, "SESSION_SIMULATION_ONLY"],
    [{unexpectedPrivateId: "do-not-accept"}, "SESSION_OBSERVATION_INVALID"],
  ];
  for (const [overrides, code] of inputs) {
    const result = check({observation: observation(overrides)});
    assert.equal(result.contractReady, false, code);
    assert.ok(codes(result).includes(code), code);
  }
});

test("字幕显示修改不要求剪切能力；原声替换仍要求 voice 和本地写入能力", () => {
  const captionOnly = check({textTarget: "caption-display", treatments: {captions: true}, observation: observation({capabilities: ["project-read", "timeline-read", "caption-read", "caption-write", "composed-preview"]})});
  assert.equal(captionOnly.contractReady, true);
  const replacement = check({textTarget: "spoken-replacement", treatments: {}});
  assert.equal(replacement.contractReady, false);
  assert.ok(replacement.route.required.includes("voice"));
  assert.ok(codes(replacement).includes("SESSION_CAPABILITY_MISSING"));
  assert.equal(check({textTarget: "clarify"}).contractReady, false);
});

test("新官方能力按需路由，普通稳剪不自动加载", () => {
  const baseline = routeOfficialSkills();
  assert.equal(baseline.required.includes("video-translation"), false);
  assert.equal(baseline.required.includes("digital-human"), false);
  const requested = routeOfficialSkills({needsVideoTranslation: true, needsDigitalHuman: true});
  assert.ok(requested.required.includes("video-translation"));
  assert.ok(requested.required.includes("digital-human"));
});

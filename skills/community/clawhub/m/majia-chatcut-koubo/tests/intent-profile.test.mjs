import assert from "node:assert/strict";
import test from "node:test";

import {inferIntent, starterPromptRoutes} from "../src/orchestration/intent-router.mjs";
import {routeOfficialSkills} from "../src/orchestration/official-skill-router.mjs";
import {
  createProjectBrief,
  loadOrchestrationProfiles,
  profileFingerprint,
  selectProfile,
} from "../src/orchestration/profile-selector.mjs";

test("四个 starter prompt 都路由到约定动作和模式", () => {
  for (const {prompt, expected} of starterPromptRoutes()) {
    const actual = inferIntent(prompt);
    assert.equal(actual.action, expected.action, prompt);
    assert.equal(actual.mode, expected.mode, prompt);
  }
});

test("未知或空意图安全降级为 stable assist", () => {
  for (const input of ["", "帮我看看这个素材"]) {
    const route = inferIntent(input);
    assert.equal(route.action, "run");
    assert.equal(route.mode, "stable");
    assert.equal(route.automationLevel, "assist");
  }
});

test("只有用户明确说出的增强项才会打开", () => {
  const profile = selectProfile({mode: "pro"});
  const implicit = createProjectBrief({
    route: inferIntent("给当前口播做专业增强"),
    profile,
  });
  for (const name of ["restructure", "broll", "motionGraphics", "music", "generatedMedia", "export"]) {
    assert.equal(implicit.treatments[name], false, name);
  }

  const explicit = createProjectBrief({
    route: inferIntent("给当前口播加音乐和 MG，最后导出 MP4"),
    profile,
  });
  assert.equal(explicit.treatments.music, true);
  assert.equal(explicit.treatments.motionGraphics, true);
  assert.equal(explicit.treatments.export, true);
  assert.equal(explicit.treatments.broll, false);
});

test("明确否定优先于增强关键词，稳剪模式不会被否定词劫持", () => {
  const route = inferIntent("稳剪，但不要音乐/MG/B-roll/导出");
  assert.equal(route.mode, "stable");
  assert.equal(route.action, "run");
  for (const name of ["music", "motionGraphics", "broll", "export"]) {
    assert.equal(route.requestedTreatments[name], false, name);
    assert.equal(route.deniedTreatments[name], true, name);
  }
  const brief = createProjectBrief({route, profile: selectProfile({mode: "stable"})});
  for (const name of ["music", "motionGraphics", "broll", "export"]) {
    assert.equal(brief.treatments[name], false, name);
  }
});

test("延后执行路由为 audit，但仍保留用户想审核的项目", () => {
  const route = inferIntent("需要 B-roll 和 MG，但先不要真正添加，确认后再做");
  assert.equal(route.action, "review");
  assert.equal(route.automationLevel, "audit");
  assert.equal(route.requestedTreatments.broll, true);
  assert.equal(route.requestedTreatments.motionGraphics, true);
});

test("四套 Profile 按快剪、长片和录屏确定性选择", () => {
  assert.equal(selectProfile().id, "balanced-stable");
  assert.equal(selectProfile({mode: "fast", durationSec: 60}).id, "tight-short");
  assert.equal(selectProfile({durationSec: 300}).id, "trust-longform");
  assert.equal(selectProfile({hasScreenCapture: true, durationSec: 30}).id, "screen-demo");
  assert.throws(() => selectProfile({mode: "fast", hasScreenCapture: true, durationSec: 30}), /PROFILE_COMBINATION_UNSUPPORTED/u);
  assert.throws(() => selectProfile({mode: "fast", durationSec: 1000}), /PROFILE_COMBINATION_UNSUPPORTED/u);
  assert.equal(loadOrchestrationProfiles().length, 4);
});

test("Profile fingerprint 稳定且 selector 返回独立副本", () => {
  const first = selectProfile();
  const second = selectProfile();
  assert.equal(profileFingerprint(first), profileFingerprint(second));
  first.defaults.treatments.music = true;
  assert.equal(second.defaults.treatments.music, false);
});

test("缺参表单只在至少两项缺失时触发且最多五项", () => {
  const route = inferIntent("稳剪当前口播");
  const profile = selectProfile();
  const oneMissing = createProjectBrief({route, profile, missingFields: ["goal"]});
  assert.equal(oneMissing.intake.asked, false);

  const manyMissing = createProjectBrief({
    route,
    profile,
    missingFields: ["goal", "pacing", "output", "captions", "enhancements", "goal"],
  });
  assert.equal(manyMissing.intake.asked, true);
  assert.equal(manyMissing.intake.missingFields.length, 5);
  assert.equal(new Set(manyMissing.intake.missingFields).size, manyMissing.intake.missingFields.length);
});

test("官方 Skill 路由保持本包为轻量编排层", () => {
  const baseline = routeOfficialSkills({stage: "preflight"});
  assert.deepEqual(baseline.required, ["chatcut-plugin-basics", "talking-head-guide", "verification"]);
  assert.equal(baseline.exportRouted, false);

  const enhanced = routeOfficialSkills({
    stage: "sample_ready",
    treatments: {captions: true, music: true, motionGraphics: true, generatedMedia: true, export: true},
    exportAuthorized: false,
  });
  for (const skill of ["transcription", "music", "create-motion-graphics", "video-gen"]) {
    assert.ok(enhanced.required.includes(skill), skill);
  }
  assert.equal(enhanced.required.includes("export"), false);
});

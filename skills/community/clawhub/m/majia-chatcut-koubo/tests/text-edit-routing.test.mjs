import assert from "node:assert/strict";
import test from "node:test";
import fs from "node:fs";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import {runFakeOneClickSession} from "../src/orchestration/orchestrator.mjs";
import {inferIntent} from "../src/orchestration/intent-router.mjs";
import {createProjectBrief, selectProfile} from "../src/orchestration/profile-selector.mjs";
import {classifyRisk, normalizeDecision, assertDecisionCanApply} from "../src/orchestration/risk-classifier.mjs";
import {inferTextEdit} from "../src/orchestration/text-edit-router.mjs";

function brief(intent) {
  const route = inferIntent(intent);
  return createProjectBrief({route, profile: selectProfile({mode: route.mode})});
}

test("只改字幕不能启动口播剪切或音频平滑", () => {
  const result = brief("只改字幕，别剪原声，也不要替换原声");
  assert.equal(result.textEdit.target, "caption-display");
  assert.equal(result.textEdit.changesSpokenAudio, false);
  assert.equal(result.treatments.arollCleanup, false);
  assert.equal(result.treatments.smoothAudio, false);
  assert.equal(result.treatments.captions, true);
});

test("识别错误只修转写，不默许生成语音或基础字幕重做", () => {
  const result = brief("原声没错，修正转写里的识别错误");
  assert.equal(result.textEdit.target, "transcript-repair");
  assert.equal(result.treatments.arollCleanup, false);
  assert.equal(result.treatments.captions, false);
  assert.equal(result.treatments.generatedMedia, false);
});

test("原声替换需要独立高风险审批，不能借样片批准放行", () => {
  assert.equal(brief("替换原声里说错的词").textEdit.requiresExplicitApproval, true);
  assert.equal(classifyRisk({type: "spoken-replacement"}), "high");
  const decision = normalizeDecision({type: "spoken-replacement", reason: "已确认的局部修复", evidenceRefs: ["logical:source-audio"], approvalRef: "logical:sample-approval"});
  assert.throws(() => assertDecisionCanApply(decision, {approvals: [{approvalRef: "logical:sample-approval", kind: "sample", status: "approved", scope: ["logical:decision-dec-001"]}]}), (error) => error.code === "RISK_HIGH_APPROVAL_REQUIRED");
});

test("模糊或混合文字目标只生成澄清，不进入默认剪切", () => {
  for (const intent of ["把这里的文字删掉", "改字幕，并替换原声"]) {
    const result = brief(intent);
    assert.equal(result.textEdit.target, "clarify");
    assert.equal(result.treatments.arollCleanup, false);
  }
  assert.equal(inferTextEdit("不要修改字幕"), null);
  assert.equal(inferTextEdit("稳剪当前口播"), null);
  assert.equal(brief("稳剪当前口播").treatments.arollCleanup, true);
});

test("窄文字任务的模拟决定不得假称已经执行口播清理", () => {
  const suite = JSON.parse(fs.readFileSync(new URL("../fixtures/runtime/scenarios.json", import.meta.url), "utf8"));
  const scenario = structuredClone(suite.scenarios.find((item) => item.scenarioId === "scenario-happy-path"));
  scenario.intent = "只改字幕，别剪原声";
  const result = runFakeOneClickSession(scenario);
  assert.equal(result.recovery.objectCount, 0);
  assert.ok(result.decisionLog.decisions.every((item) => item.status === "proposed"));
});

test("文字目标与默认处理、时序和审批字段必须一致", () => {
  const ajv = new Ajv2020({strict: true});
  addFormats(ajv);
  const validate = ajv.compile(JSON.parse(fs.readFileSync(new URL("../schemas/runtime/project-brief.schema.json", import.meta.url), "utf8")));
  const value = brief("只改字幕");
  assert.equal(validate(value), true);
  for (const corrupted of [
    {...value, treatments: {...value.treatments, arollCleanup: true}},
    {...value, textEdit: {...value.textEdit, changesSpokenAudio: true}},
    {...value, textEdit: {...value.textEdit, preservesTiming: false}},
  ]) assert.equal(validate(corrupted), false);
  const replacement = brief("替换原声");
  assert.equal(validate({...replacement, textEdit: {...replacement.textEdit, requiresExplicitApproval: false}}), false);
});

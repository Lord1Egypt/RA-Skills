import fs from "node:fs";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import {routeOfficialSkills} from "./official-skill-router.mjs";

const schema = JSON.parse(fs.readFileSync(new URL("../../schemas/runtime/session-observation.schema.json", import.meta.url), "utf8"));
const ajv = new Ajv2020({allErrors: true, strict: true});
addFormats(ajv);
const validate = ajv.compile(schema);

// This checks a declared session contract. It never connects, edits, or proves media quality.
export function preflightSession({observation = null, surface = "auto", treatments = {}, textTarget = null, now = new Date().toISOString()} = {}) {
  const findings = [];
  const add = (code, message) => findings.push({code, message});
  if (!["auto", "hosted", "desktop"].includes(surface)) throw new Error("SESSION_SURFACE_INVALID");
  if (!Number.isFinite(Date.parse(now))) throw new Error("SESSION_TIME_INVALID");
  if (observation !== null && !validate(observation)) {
    add("SESSION_OBSERVATION_INVALID", "当前会话记录格式不完整，需重新读取工具与能力。");
    observation = null;
  }
  const selected = surface === "auto" ? observation?.surface ?? "unknown" : surface;
  const route = routeOfficialSkills({surface: selected, treatments, textTarget});
  if (!observation) {
    add("SESSION_OBSERVATION_REQUIRED", "先读取当前 ChatCut 会话；无法从项目版本推断连接环境。");
  } else {
    if (selected !== observation.surface) add("SESSION_SURFACE_MISMATCH", "所选环境与会话记录不一致，先核对目标项目。");
    const expectedSources = selected === "desktop" ? ["signed-desktop", "managed-desktop"] : ["hosted-plugin"];
    if (!expectedSources.includes(observation.skillSource)) add("SESSION_SKILL_SOURCE_MISMATCH", "当前指令来源与连接环境不一致，需加载对应官方指令。");
    const time = Date.parse(now);
    const observed = Date.parse(observation.observedAt);
    const expires = Date.parse(observation.expiresAt);
    if (observed > time || expires <= time || expires <= observed || expires - observed > 86_400_000) {
      add("SESSION_OBSERVATION_STALE", "会话记录已过期或时间无效，需重新读取当前能力。");
    }
    if (observation.provenance !== "live") add("SESSION_SIMULATION_ONLY", "模拟记录只供离线检查，不能放行真实工具调用。");
    for (const skill of route.required) {
      if (!observation.skills.includes(skill)) add("SESSION_SKILL_MISSING", `缺少本次需要的官方 Skill：${skill}`);
    }
    const required = new Set(["project-read", "timeline-read", "composed-preview"]);
    if (textTarget === "clarify") add("TEXT_TARGET_REQUIRED", "先确定修改字幕、转写、剪切还是原声替换。");
    if (textTarget === "caption-display" || treatments.captions) {
      required.add("caption-read");
      required.add("caption-write");
    }
    if (textTarget === "transcript-repair") {
      required.add("transcript-read");
      required.add("transcript-repair");
    }
    if (textTarget === "spoken-replacement") {
      required.add("voice-generation");
      required.add("timeline-write");
    }
    if (textTarget === "speech-cut" || treatments.arollCleanup || treatments.restructure) {
      required.add("transcript-read");
      required.add("speech-edit");
      required.add("timeline-write");
    }
    if (treatments.smoothAudio) required.add("timeline-write");
    if (treatments.broll) required.add("timeline-write");
    for (const [treatment, capability] of Object.entries({music: "music", motionGraphics: "motion-graphics", generatedMedia: "media-generation", export: "export"})) {
      if (treatments[treatment]) required.add(capability);
    }
    for (const capability of required) {
      if (!observation.capabilities.includes(capability)) add("SESSION_CAPABILITY_MISSING", `当前环境缺少所需能力：${capability}`);
    }
  }
  return {
    surface: selected,
    route,
    contractReady: findings.length === 0,
    verificationScope: "declared-session-contract",
    mediaVerified: false,
    stableClaimEligible: false,
    observation: observation ? {
      observedAt: observation.observedAt,
      expiresAt: observation.expiresAt,
      toolSchemaFingerprint: observation.toolSchemaFingerprint,
      provenance: observation.provenance,
    } : null,
    findings,
    nextAction: findings[0]?.message ?? "按当前官方指令确认项目与授权范围，再制作代表样片。",
  };
}

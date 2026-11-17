#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const args = process.argv.slice(2);
let root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
if (args.length > 0) {
  if (args.length !== 2 || args[0] !== "--root" || !args[1]) {
    console.error("Usage: node scripts/check-version-drift.mjs [--root <repository-root>]");
    process.exit(2);
  }
  root = path.resolve(args[1]);
}
const read = (relativePath) => fs.readFileSync(path.join(root, relativePath), "utf8");
const errors = [];

try {
const packageManifest = JSON.parse(read("package.json"));
const packageVersion = packageManifest.version;
const packageLock = JSON.parse(read("package-lock.json"));
const nodeVersion = read(".node-version").trim();
const nodeVersionMatch = /^(\d+)\.(\d+)\.(\d+)$/.exec(nodeVersion);
const nodeMajor = nodeVersionMatch ? Number(nodeVersionMatch[1]) : null;
const expectedNodeEngine = nodeMajor !== null
  ? `>=${nodeVersion} <${nodeMajor + 1}`
  : null;
const ciWorkflow = read(".github/workflows/ci.yml");
const policyVersion = JSON.parse(read("rules/policy.json")).version;
const ruleRegistry = JSON.parse(read("rules/registry.json"));
const themeKitVersions = [
  "assets/theme-kit/package.json",
  "assets/theme-kit/manifest.json",
  "assets/theme-kit/tokens/themes.json",
].map((relativePath) => ({
  relativePath,
  version: JSON.parse(read(relativePath)).version,
}));
const currentProfilePolicyVersions = [
  "fixtures/profiles/local/profile.source.json",
  "templates/operating-profile.template.json",
  "templates/local-config-example/profile/landscape.example.json",
].map((relativePath) => ({
  relativePath,
  version: JSON.parse(read(relativePath)).policyVersion,
}));
const skill = read("SKILL.md");
const readme = read("README.md");
const readmeEnglish = read("README.en.md");
const changelog = read("CHANGELOG.md");
const architectureSvg = read("04-项目设计与路线图/系统架构.svg");
const migrationGuide = read("04-项目设计与路线图/V1.3.1迁移指南.md");
const roadmap = read("04-项目设计与路线图/公开路线图.md");
const captionReference = read("02-剪辑方法手册/07-字幕与术语.md");
const openAiAgent = read("agents/openai.yaml");
const liveCanaryReport = JSON.parse(read(`reports/live-canary-v${packageVersion}.json`));
const orchestrationProfiles = [
  "balanced-stable",
  "tight-short",
  "trust-longform",
  "screen-demo",
].map((id) => ({id, document: JSON.parse(read(`profiles/${id}.json`))}));
const workflowDocuments = [
  "one-click-stable",
  "fast-cut",
  "pro-enhance",
  "resume",
  "official-skill-map",
].map((id) => ({id, document: read(`workflows/${id}.md`)}));

const skillVersion = skill.match(/^metadata:\s*\n\s+version:\s*([^\s]+)\s*$/m)?.[1];
const changelogVersion = changelog.match(/^## V(\d+\.\d+\.\d+)\b/m)?.[1];

if (skillVersion !== packageVersion) {
  errors.push(`SKILL metadata version ${skillVersion ?? "<missing>"} != package ${packageVersion}`);
}
if (changelogVersion !== packageVersion) {
  errors.push(`latest CHANGELOG version ${changelogVersion ?? "<missing>"} != package ${packageVersion}`);
}
if (packageLock.version !== packageVersion) {
  errors.push(`package-lock version ${packageLock.version ?? "<missing>"} != package ${packageVersion}`);
}
if (packageLock.packages?.[""]?.version !== packageVersion) {
  errors.push(`package-lock root version ${packageLock.packages?.[""]?.version ?? "<missing>"} != package ${packageVersion}`);
}
if (!expectedNodeEngine) {
  errors.push(`.node-version: invalid semantic version ${nodeVersion || "<missing>"}`);
} else {
  if (packageManifest.engines?.node !== expectedNodeEngine) {
    errors.push(`package engines.node ${packageManifest.engines?.node ?? "<missing>"} != ${expectedNodeEngine}`);
  }
  if (packageLock.packages?.[""]?.engines?.node !== expectedNodeEngine) {
    errors.push(`package-lock engines.node ${packageLock.packages?.[""]?.engines?.node ?? "<missing>"} != ${expectedNodeEngine}`);
  }
}
if (!ciWorkflow.includes("node-version-file: .node-version")) {
  errors.push(".github/workflows/ci.yml: Node setup must use .node-version");
}
if (packageManifest.scripts?.["validate:rules"] !== "node scripts/validate-rule-registry.mjs") {
  errors.push("package.json: validate:rules must invoke the Rule Registry gate");
}
if (!packageManifest.scripts?.verify?.includes("npm run validate:rules")) {
  errors.push("package.json: verify must include the Rule Registry gate");
}
if (packageManifest.scripts?.["validate:plans"] !== "node scripts/validate-plan-bundle.mjs --bundle fixtures/plan-bundles/valid/bundle.json") {
  errors.push("package.json: validate:plans must invoke the canonical plan bundle gate");
}
if (!packageManifest.scripts?.verify?.includes("npm run validate:plans")) {
  errors.push("package.json: verify must include the plan bundle gate");
}
if (packageManifest.scripts?.["validate:planner"] !== "node scripts/validate-explainable-planner.mjs --transcript fixtures/plan-bundles/valid/transcript.json --edit-plan fixtures/plan-bundles/valid/edit-plan.json --expected fixtures/planning/valid/content-scorecard.json") {
  errors.push("package.json: validate:planner must reproduce the canonical scorecard");
}
if (!packageManifest.scripts?.verify?.includes("npm run validate:planner")) {
  errors.push("package.json: verify must include the explainable planner gate");
}
if (packageManifest.scripts?.["validate:srt"] !== "node scripts/srt-bridge.mjs diff --srt fixtures/srt/valid/captions.srt --sidecar fixtures/srt/valid/captions.sidecar.json") {
  errors.push("package.json: validate:srt must diff the canonical SRT fixture");
}
if (!packageManifest.scripts?.verify?.includes("npm run validate:srt")) {
  errors.push("package.json: verify must include the SRT bridge gate");
}
if (!packageManifest.scripts?.["validate:preview"]?.startsWith("node scripts/validate-preview-approval.mjs --preview fixtures/preview/valid/preview-bundle.json")) {
  errors.push("package.json: validate:preview must invoke the canonical preview fixture");
}
if (!packageManifest.scripts?.verify?.includes("npm run validate:preview")) {
  errors.push("package.json: verify must include the preview approval gate");
}
if (packageManifest.scripts?.["validate:recovery"] !== "node scripts/validate-recovery-fixtures.mjs") {
  errors.push("package.json: validate:recovery must invoke recovery fixtures");
}
if (!packageManifest.scripts?.verify?.includes("npm run validate:recovery")) {
  errors.push("package.json: verify must include the recovery fixture gate");
}
if (packageManifest.scripts?.["validate:capabilities"] !== "node scripts/validate-capability-profile.mjs --profile fixtures/capabilities/valid/unverified-profile.json --as-of 2026-07-24T12:00:00Z") {
  errors.push("package.json: validate:capabilities must audit the dated unverified profile");
}
if (!packageManifest.scripts?.verify?.includes("npm run validate:capabilities")) {
  errors.push("package.json: verify must include the capability profile gate");
}
if (packageManifest.scripts?.["validate:media"] !== "node scripts/validate-media-release.mjs --report fixtures/media-qa/valid/release-report.json") {
  errors.push("package.json: validate:media must invoke the canonical release report");
}
if (!packageManifest.scripts?.verify?.includes("npm run validate:media")) {
  errors.push("package.json: verify must include the media release gate");
}
if (packageManifest.scripts?.["validate:distribution"] !== "node scripts/validate-distribution-pack.mjs --pack fixtures/distribution/valid/distribution-pack.json --as-of 2026-07-24") {
  errors.push("package.json: validate:distribution must invoke the dated canonical pack");
}
if (!packageManifest.scripts?.verify?.includes("npm run validate:distribution")) {
  errors.push("package.json: verify must include the distribution pack gate");
}
if (packageManifest.scripts?.["validate:feedback"] !== "node scripts/validate-feedback-governance.mjs --event fixtures/feedback/valid/event.json --queue fixtures/feedback/valid/suggestion-queue.json") {
  errors.push("package.json: validate:feedback must invoke the privacy-safe governance fixtures");
}
if (!packageManifest.scripts?.verify?.includes("npm run validate:feedback")) {
  errors.push("package.json: verify must include the feedback governance gate");
}
if (packageManifest.scripts?.["validate:extensions"] !== "node scripts/validate-extensions.mjs") {
  errors.push("package.json: validate:extensions must invoke the extension pack gate");
}
if (!packageManifest.scripts?.verify?.includes("npm run validate:extensions")) {
  errors.push("package.json: verify must include the extension pack gate");
}
for (const [scriptName, command] of Object.entries({
  "validate:runtime-contracts": "node scripts/validate-runtime-fixtures.mjs",
  "validate:docs-routing": "node scripts/validate-docs-routing.mjs",
  "validate:live-claim": "node scripts/validate-live-canary-claim.mjs",
  "smoke:one-click:fake": "node scripts/smoke-one-click.mjs",
})) {
  if (packageManifest.scripts?.[scriptName] !== command) {
    errors.push(`package.json: ${scriptName} must invoke ${command}`);
  }
  if (!packageManifest.scripts?.verify?.includes(`npm run ${scriptName}`)) {
    errors.push(`package.json: verify must include ${scriptName}`);
  }
}
for (const command of [
  "run",
  "status",
  "review",
  "approve-decisions",
  "approve-sample",
  "request-revision",
  "resume",
  "report",
]) {
  if (!packageManifest.scripts?.[command]?.includes("src/cli/koubo.mjs")) {
    errors.push(`package.json: missing ${command} user-flow command`);
  }
}
if (packageManifest.bin?.["majia-koubo"] !== "src/cli/koubo.mjs") {
  errors.push("package.json: majia-koubo bin must point to src/cli/koubo.mjs");
}
if (ruleRegistry.policyVersion !== policyVersion) {
  errors.push(`rules/registry.json: policyVersion ${ruleRegistry.policyVersion ?? "<missing>"} != hard policy ${policyVersion}`);
}
if (!architectureSvg.includes(`· v${packageVersion} ·`)) {
  errors.push(`04-项目设计与路线图/系统架构.svg: footer version does not match ${packageVersion}`);
}
for (const profile of currentProfilePolicyVersions) {
  if (profile.version !== policyVersion) {
    errors.push(`${profile.relativePath}: policyVersion ${profile.version ?? "<missing>"} != hard policy ${policyVersion}`);
  }
}
const canonicalThemeKitVersion = themeKitVersions[0].version;
for (const asset of themeKitVersions.slice(1)) {
  if (asset.version !== canonicalThemeKitVersion) {
    errors.push(`${asset.relativePath}: version ${asset.version ?? "<missing>"} != theme kit package ${canonicalThemeKitVersion}`);
  }
}
for (const [name, document] of [["README.md", readme], ["README.en.md", readmeEnglish]]) {
  if (!document.includes(`skill-v${packageVersion}-blue`)) {
    errors.push(`${name}: version badge does not match ${packageVersion}`);
  }
  if (!document.includes(`**V${packageVersion}`)) {
    errors.push(`${name}: latest version history does not mention V${packageVersion}`);
  }
}
if (!readme.includes("七执行状态")) errors.push("README.md: missing seven-state capability wording");
if (!readmeEnglish.includes("seven-state")) errors.push("README.en.md: missing seven-state capability wording");
if (readmeEnglish.includes("five-state")) errors.push("README.en.md: stale five-state capability wording");
for (const [name, document] of [["README.md", readme], ["README.en.md", readmeEnglish]]) {
  if (!document.includes("04-项目设计与路线图/公开路线图.md")) {
    errors.push(`${name}: missing public roadmap link`);
  }
}
for (const marker of [
  "V1.3.1",
  "Rule Registry",
  "Creator OS IR",
  "live capability canary",
  "不是发布时间或版本承诺",
  "Rule Registry foundation — SHIPPED",
  "Rational Time + Creator OS IR v0 — SHIPPED",
  "SRT bridge — SHIPPED",
  "Explainable planner foundation — SHIPPED",
  "Preview approval gate — SHIPPED",
  "Recoverable executor + evidence foundation — SHIPPED",
  "Capability profile + live route gate — SHIPPED",
  "Local Media QA + export authorization gate — SHIPPED",
  "Distribution pack foundation — SHIPPED",
  "Feedback governance foundation — SHIPPED",
  "R7 · 一句话稳剪产品层 — OFFLINE SHIPPED / LIVE UNVERIFIED",
  "stableClaimEligible=true",
]) {
  if (!roadmap.includes(marker)) {
    errors.push(`04-项目设计与路线图/公开路线图.md: missing governance marker ${marker}`);
  }
}
const skillLineCount = skill.split(/\r?\n/u).length;
if (skillLineCount < 200 || skillLineCount > 300) {
  errors.push(`SKILL.md: expected 200-300 lines, got ${skillLineCount}`);
}
if (!openAiAgent.includes("$majia-chatcut-koubo")) {
  errors.push("agents/openai.yaml: default prompt must explicitly name $majia-chatcut-koubo");
}
for (const workflow of workflowDocuments) {
  if (!workflow.document.includes("UNVERIFIED")) {
    errors.push(`workflows/${workflow.id}.md: missing explicit UNVERIFIED live boundary`);
  }
}
for (const profile of orchestrationProfiles) {
  if (profile.document.id !== profile.id || profile.document.version !== "1.0.0") {
    errors.push(`profiles/${profile.id}.json: identity/version drift`);
  }
  const treatments = profile.document.defaults?.treatments ?? {};
  for (const disabled of ["restructure", "broll", "motionGraphics", "music", "generatedMedia", "export"]) {
    if (treatments[disabled] !== false) {
      errors.push(`profiles/${profile.id}.json: ${disabled} must default to false`);
    }
  }
}
if (liveCanaryReport.releaseVersion !== packageVersion) {
  errors.push(`live canary releaseVersion ${liveCanaryReport.releaseVersion ?? "<missing>"} != package ${packageVersion}`);
}
if (liveCanaryReport.stableClaimEligible !== false && !liveCanaryReport.eligibility?.eligible) {
  errors.push("live canary report: stable claim cannot be enabled without eligible evidence");
}
for (const [name, document] of [
  ["README.md", readme],
  ["README.en.md", readmeEnglish],
  ["04-项目设计与路线图/V1.3.1迁移指南.md", migrationGuide],
  ["02-剪辑方法手册/07-字幕与术语.md", captionReference],
]) {
  if (!document.includes("--root <profile-config-root>")
    && !document.includes("--root <profile 配置根目录>")) {
    errors.push(`${name}: caption validation example must declare its profile root`);
  }
}
for (const marker of [
  "validatedTimelineRevisions",
  "validatedSourceRevisions",
  "sourceAssetId",
  "sourceWordKey",
  "sourceText",
  "correction",
  "shortCardEvidence",
]) {
  if (!migrationGuide.includes(marker)) {
    errors.push(`04-项目设计与路线图/V1.3.1迁移指南.md: missing caption contract marker ${marker}`);
  }
  if (!captionReference.includes(marker)) {
    errors.push(`02-剪辑方法手册/07-字幕与术语.md: missing caption contract marker ${marker}`);
  }
}

if (errors.length > 0) {
  for (const error of errors) console.error(`FAIL ${error}`);
  console.error(`version drift audit failed: ${errors.length} error(s)`);
  process.exitCode = 1;
} else {
  console.log(`version drift audit passed: repository surfaces agree on v${packageVersion}`);
}
} catch (error) {
  const code = error instanceof SyntaxError
    ? "INVALID_JSON"
    : error?.code ?? "READ_FAILED";
  console.error(`version drift audit unavailable: ${code}`);
  process.exitCode = 2;
}

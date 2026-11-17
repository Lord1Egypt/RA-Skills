import {inferTextEdit} from "./text-edit-router.mjs";

const ROUTES = Object.freeze([
  {action: "resume", pattern: /(?:继续|恢复|接着|上次|resume)/iu},
  {
    action: "review",
    pattern: /(?:只.*(?:审核|审阅|方案)|先(?:不要|别|不)(?:真正)?(?:添加|应用|执行|改|写)|确认后再做|review|audit)/iu,
  },
  {action: "run", mode: "fast", pattern: /(?:快剪|快速草稿|短口播|尽快出样片)/iu},
  {action: "run", mode: "stable", pattern: /(?:马甲稳剪|一键稳剪|稳剪|ChatCut.*口播|口播.*(?:口误|停顿|字幕)|剪干净)/iu},
  {action: "run", mode: "pro", pattern: /(?:专业增强|双画面|画中画|B-?roll|MG|动效|音乐|多平台|录屏演示)/iu},
]);

const TREATMENT_SIGNALS = Object.freeze({
  captions: /(?:字幕|caption)/iu,
  broll: /(?:B-?roll|补画面)/iu,
  motionGraphics: /(?:MG|动效|动态图形)/iu,
  music: /(?:音乐|BGM)/iu,
  restructure: /(?:重排|重组|钩子前置)/iu,
  generatedMedia: /(?:生成图片|生成视频|生成素材)/iu,
  export: /(?:导出|成片文件|MP4)/iu,
});

const LOCAL_DENIAL = /(?:不要|别|不加|不做|不需要|无需|禁止|关闭|去掉|取消|without|no\s+)/iu;

function occurrences(pattern, text) {
  const flags = pattern.flags.includes("g") ? pattern.flags : `${pattern.flags}g`;
  return [...text.matchAll(new RegExp(pattern.source, flags))];
}

function treatmentIsDenied(text, pattern) {
  return occurrences(pattern, text).every((match) => {
    const prefix = text.slice(0, match.index ?? 0);
    const clause = prefix.slice(Math.max(
      prefix.lastIndexOf("，"),
      prefix.lastIndexOf(","),
      prefix.lastIndexOf("。"),
      prefix.lastIndexOf("；"),
      prefix.lastIndexOf(";"),
      prefix.lastIndexOf("！"),
      prefix.lastIndexOf("!"),
      prefix.lastIndexOf("？"),
      prefix.lastIndexOf("?"),
    ) + 1);
    return LOCAL_DENIAL.test(clause);
  });
}

export function inferIntent(input) {
  const text = String(input ?? "").trim();
  if (text.length === 0) {
    return {
      matched: false,
      action: "run",
      mode: "stable",
      automationLevel: "assist",
      requestedTreatments: {},
      reason: "empty-intent",
    };
  }
  const route = ROUTES.find((candidate) => candidate.pattern.test(text));
  const requestedTreatments = Object.fromEntries(
    Object.entries(TREATMENT_SIGNALS)
      .filter(([, pattern]) => pattern.test(text))
      .map(([name, pattern]) => [name, !treatmentIsDenied(text, pattern)]),
  );
  const deniedTreatments = Object.fromEntries(
    Object.entries(requestedTreatments)
      .filter(([, authorized]) => !authorized)
      .map(([name]) => [name, true]),
  );
  const auditOnly = route?.action === "review";
  return {
    matched: Boolean(route),
    action: route?.action ?? "run",
    mode: route?.mode ?? "stable",
    automationLevel: auditOnly ? "audit" : "assist",
    requestedTreatments,
    deniedTreatments,
    textEdit: inferTextEdit(text),
    reason: route ? `matched-${route.action}-${route.mode ?? "existing"}` : "safe-stable-default",
  };
}

export function starterPromptRoutes() {
  return Object.freeze([
    {prompt: "稳剪当前口播", expected: {action: "run", mode: "stable"}},
    {prompt: "继续上次剪辑", expected: {action: "resume", mode: "stable"}},
    {prompt: "只做口误清理和字幕，先不要改时间线", expected: {action: "review", mode: "stable"}},
    {prompt: "给当前口播做专业增强", expected: {action: "run", mode: "pro"}},
  ]);
}

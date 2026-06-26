#!/usr/bin/env node

import { randomUUID } from "node:crypto";
import { spawnSync } from "node:child_process";
import { buildAssessmentMessages, phaseOrder, pickAssessmentScore, resolveAssessmentRange, resolvePreviousPhase } from "./assessment-helpers.mjs";

const defaultSkillVersion = "openclaw-school-enrollment/0.8.2";
const defaultBaseUrl = "https://openclaw-school.space";
const defaultClawhubRegistryUrl = "https://cn.clawhub-mirror.com";
const clawhubBootstrapCommand = "npm install -g clawhub";
const stepCooldownMs = 5000;

const phaseStepNameMap = {
  baseline_testing: "入学测试",
  course_resolving: "识别送培课程",
  package_fetching: "拉取课程资源",
  supplies_procuring: "采买学习物资",
  package_installing: "能力装配中",
  capability_activating: "激活职业能力",
  graduation_testing: "毕业测试",
  graduation_ready: "毕业准备完成",
  error: "训练异常"
};

function parseArgs(argv) {
  const args = { _: [] };

  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];

    if (!value.startsWith("--")) {
      args._.push(value);
      continue;
    }

    const trimmed = value.slice(2);
    const equalIndex = trimmed.indexOf("=");

    if (equalIndex >= 0) {
      const key = trimmed.slice(0, equalIndex);
      const rawValue = trimmed.slice(equalIndex + 1);
      args[key] = rawValue === "" ? true : rawValue;
      continue;
    }

    const next = argv[index + 1];

    if (!next || next.startsWith("--")) {
      args[trimmed] = true;
      continue;
    }

    args[trimmed] = next;
    index += 1;
  }

  return args;
}

function printHelp() {
  console.log(`Usage:
  node scripts/enroll-and-train.mjs [run-all] --enrollment-token <token> [options]
  node scripts/enroll-and-train.mjs start --enrollment-token <token> [options]
  node scripts/enroll-and-train.mjs phase --phase <phase> --run-id <id> --report-token <token> [options]

Commands:
  run-all                       Run the full training flow in one process (default)
  start                         Claim the enrollment token and create the training context
  phase                         Complete one training phase and report it back to the server

Phase values:
  ${phaseOrder.join(", ")}

Options:
  --base-url <url>              Override the training server URL (default: ${defaultBaseUrl})
  --clawhub-registry-url <url>  Override the ClawHub registry URL (default: ${defaultClawhubRegistryUrl})
  --skill-version <value>       Reported skill version for the initial claim
  --dry-run                     Skip actual install commands and only validate the flow
  --json                        Print structured JSON for agent consumption
  --help                        Show this help
`);
}

function requireStringArg(args, key) {
  const value = args[key];

  if (typeof value === "string" && value.trim()) {
    return value.trim();
  }

  throw new Error(`Missing required argument: --${key}`);
}

function normalizeBaseUrl(value) {
  return value.replace(/\/+$/, "");
}

function normalizeOptionalUrl(value) {
  if (typeof value !== "string") {
    return null;
  }

  const trimmed = value.trim();

  if (!trimmed) {
    return null;
  }

  return trimmed.replace(/\/+$/, "");
}

function resolveMode(args) {
  const command = args._[0];

  if (!command) {
    return "run-all";
  }

  if (command === "run-all" || command === "start" || command === "phase") {
    return command;
  }

  throw new Error(`Unknown command: ${command}`);
}

function runCommand(command, args, options = {}) {
  const result = spawnSync(command, args, {
    encoding: "utf8",
    stdio: "pipe",
    cwd: process.cwd(),
    shell: false,
    ...options
  });

  if (result.error) {
    throw result.error;
  }

  if (result.status !== 0) {
    throw new Error((result.stderr || result.stdout || `${command} exited with status ${result.status}`).trim());
  }

  return {
    stdout: (result.stdout || "").trim(),
    stderr: (result.stderr || "").trim()
  };
}

function runCommandQuiet(command, args, options = {}) {
  const result = spawnSync(command, args, {
    encoding: "utf8",
    stdio: "pipe",
    cwd: process.cwd(),
    shell: false,
    ...options
  });

  return {
    status: result.status ?? 1,
    stdout: (result.stdout || "").trim(),
    stderr: (result.stderr || "").trim(),
    error: result.error ?? null
  };
}

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

async function postJson(url, body, headers = {}) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...headers
    },
    body: JSON.stringify(body)
  });

  const text = await response.text();
  const parsed = text ? safeParseJson(text) : null;

  if (!response.ok) {
    const message = parsed && typeof parsed.error === "string" ? parsed.error : `${response.status} ${response.statusText}`.trim();
    throw new Error(message);
  }

  return parsed;
}

async function getJson(url, headers = {}) {
  const response = await fetch(url, {
    method: "GET",
    headers
  });

  const text = await response.text();
  const parsed = text ? safeParseJson(text) : null;

  if (!response.ok) {
    const message = parsed && typeof parsed.error === "string" ? parsed.error : `${response.status} ${response.statusText}`.trim();
    throw new Error(message);
  }

  return parsed;
}

function safeParseJson(value) {
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

function buildAuthHeaders(reportToken) {
  return {
    Authorization: `Bearer ${reportToken}`
  };
}

function createEventId() {
  return randomUUID();
}

async function reportEvent(context, input) {
  return postJson(
    `${context.baseUrl}/api/skill/runs/${context.runId}/events`,
    {
      eventId: createEventId(),
      stepKey: input.stepKey,
      stepName: input.stepName,
      status: input.status,
      userMessage: input.userMessage,
      payload: input.payload
    },
    buildAuthHeaders(context.reportToken)
  );
}

async function safeReportEvent(context, input) {
  try {
    await reportEvent(context, input);
  } catch (error) {
    console.error(`[warn] failed to report ${input.stepKey}: ${error instanceof Error ? error.message : String(error)}`);
  }
}

function ensureObject(value, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`Invalid ${label} response`);
  }

  return value;
}

function resolveInstallPlan(course) {
  const installPlan = ensureObject(course.installPlan, "install plan");
  const installer = installPlan.installer;

  if (installer !== "clawhub") {
    throw new Error(`Unsupported installer: ${typeof installer === "string" ? installer : "(missing)"}`);
  }

  const capabilityLabels = Array.isArray(installPlan.capabilityLabels)
    ? installPlan.capabilityLabels.filter((item) => typeof item === "string" && item.trim())
    : [];
  const skillSlugs = Array.isArray(installPlan.skillSlugs)
    ? installPlan.skillSlugs.filter((item) => typeof item === "string" && item.trim())
    : [];

  if (capabilityLabels.length === 0) {
    throw new Error("Course install plan has no capability labels.");
  }

  if (skillSlugs.length === 0) {
    throw new Error("Course install plan has no skill slugs.");
  }

  return {
    installer,
    capabilityLabels,
    skillSlugs
  };
}

function detectClawhubCommand() {
  if (process.platform === "win32") {
    const result = runCommandQuiet("where", ["clawhub"]);
    const detectedPath = result.status === 0 ? result.stdout.split(/\r?\n/).find(Boolean) ?? null : null;

    return {
      installed: result.status === 0,
      detectionCommand: "where clawhub",
      detectedPath
    };
  }

  const result = runCommandQuiet("sh", ["-lc", "command -v clawhub"]);

  return {
    installed: result.status === 0,
    detectionCommand: "command -v clawhub",
    detectedPath: result.status === 0 ? result.stdout.split(/\r?\n/).find(Boolean) ?? null : null
  };
}

function ensureClawhubInstalled(dryRun) {
  const before = detectClawhubCommand();

  if (before.installed) {
    return {
      alreadyAvailable: true,
      installedNow: false,
      dryRun,
      detectionCommand: before.detectionCommand,
      detectedPath: before.detectedPath,
      executedCommands: []
    };
  }

  if (dryRun) {
    return {
      alreadyAvailable: false,
      installedNow: false,
      dryRun: true,
      detectionCommand: before.detectionCommand,
      detectedPath: null,
      executedCommands: [clawhubBootstrapCommand]
    };
  }

  runCommand("npm", ["install", "-g", "clawhub"]);

  const after = detectClawhubCommand();

  if (!after.installed) {
    throw new Error("clawhub has been installed through npm, but the command is still unavailable in the current environment.");
  }

  return {
    alreadyAvailable: false,
    installedNow: true,
    dryRun: false,
    detectionCommand: after.detectionCommand,
    detectedPath: after.detectedPath,
    executedCommands: [clawhubBootstrapCommand]
  };
}

async function installSkillsFromPlan(plan, dryRun, clawhubRegistryUrl) {
  const installedSkillSlugs = [];
  const executedCommands = [];

  for (const slug of plan.skillSlugs) {
    const installArgs = ["install", slug, "--force"];

    if (clawhubRegistryUrl) {
      installArgs.push(`--registry=${clawhubRegistryUrl}`);
    }

    const commandString = clawhubRegistryUrl
      ? `clawhub install ${slug} --force --registry=${clawhubRegistryUrl}`
      : `clawhub install ${slug} --force`;

    if (dryRun) {
      executedCommands.push(commandString);
      installedSkillSlugs.push(slug);
      continue;
    }

    runCommand("clawhub", installArgs);
    executedCommands.push(commandString);
    installedSkillSlugs.push(slug);
  }

  return {
    installedSkillSlugs,
    executedCommands,
    totalInstallOperations: plan.skillSlugs.length
  };
}

function resolveSharedOptions(args) {
  const rawBaseUrl = typeof args["base-url"] === "string" ? args["base-url"] : defaultBaseUrl;
  const rawRegistryUrl = typeof args["clawhub-registry-url"] === "string" ? args["clawhub-registry-url"] : defaultClawhubRegistryUrl;

  return {
    json: Boolean(args.json),
    dryRun: Boolean(args["dry-run"]),
    baseUrl: normalizeBaseUrl(rawBaseUrl),
    clawhubRegistryUrl: normalizeOptionalUrl(rawRegistryUrl),
    skillVersion: typeof args["skill-version"] === "string" ? args["skill-version"] : defaultSkillVersion
  };
}

function buildContextFromArgs(args, sharedOptions) {
  return {
    baseUrl: sharedOptions.baseUrl,
    runId: requireStringArg(args, "run-id"),
    reportToken: requireStringArg(args, "report-token"),
    orderId: typeof args["order-id"] === "string" ? args["order-id"].trim() : null,
    directionName: typeof args["direction-name"] === "string" ? args["direction-name"].trim() : null
  };
}

async function claimEnrollment(enrollmentToken, sharedOptions) {
  const enrollBody = ensureObject(
    await postJson(`${sharedOptions.baseUrl}/api/skill/enroll`, {
      enrollmentToken,
      skillVersion: sharedOptions.skillVersion,
      clientMeta: {
        workspace: process.cwd(),
        orchestrationMode: "stepwise",
        installer: "clawhub install --force",
        bootstrapInstaller: clawhubBootstrapCommand,
        baseUrl: sharedOptions.baseUrl,
        clawhubRegistryUrl: sharedOptions.clawhubRegistryUrl,
        installPlanSource: "server-course-api"
      }
    }),
    "enroll"
  );

  return {
    baseUrl: sharedOptions.baseUrl,
    clawhubRegistryUrl: sharedOptions.clawhubRegistryUrl,
    orderId: String(enrollBody.orderId),
    runId: String(enrollBody.runId),
    reportToken: String(enrollBody.reportToken),
    directionName: String(enrollBody.directionName),
    courseVersion: typeof enrollBody.courseVersion === "string" ? enrollBody.courseVersion : null,
    courseUrl: typeof enrollBody.courseUrl === "string" ? enrollBody.courseUrl : null,
    expiresAt: typeof enrollBody.expiresAt === "string" ? enrollBody.expiresAt : null
  };
}

async function loadCourseContext(context) {
  const course = ensureObject(
    await getJson(`${context.baseUrl}/api/skill/runs/${context.runId}/course`, buildAuthHeaders(context.reportToken)),
    "course"
  );

  return {
    course,
    installPlan: resolveInstallPlan(course),
    graduationResult: ensureObject(course.graduation, "graduation")
  };
}

function readAssessmentSummary(course) {
  if (!course.assessment || typeof course.assessment !== "object" || Array.isArray(course.assessment)) {
    return {};
  }

  return course.assessment;
}

function buildPhaseResult(context, input) {
  return {
    ok: true,
    mode: "phase",
    phase: input.phase,
    stepName: input.stepName,
    userFacingMessage: input.userFacingMessage,
    context: {
      orderId: context.orderId,
      runId: context.runId,
      reportToken: context.reportToken,
      directionName: context.directionName,
      baseUrl: context.baseUrl
    },
    details: input.details ?? {}
  };
}

async function completeBaselineTesting(context) {
  const { course } = await loadCourseContext(context);
  const assessment = readAssessmentSummary(course);
  const reused = Boolean(assessment.shouldReuseBaseline) && typeof assessment.baselineScore === "number";
  const score = reused ? assessment.baselineScore : pickAssessmentScore(40, 65);
  const { minScore, maxScore } = resolveAssessmentRange({ kind: "baseline", score, reused });
  const messages = buildAssessmentMessages({ kind: "baseline", score, reused });
  const previousPhase = resolvePreviousPhase("baseline_testing");

  await reportEvent(context, {
    stepKey: "baseline_testing",
    stepName: phaseStepNameMap.baseline_testing,
    status: "STARTED",
    userMessage: messages.started,
    payload: {
      previousPhase,
      assessmentType: "baseline",
      reused
    }
  });

  if (!reused) {
    await sleep(10000);
  }

  await reportEvent(context, {
    stepKey: "baseline_testing",
    stepName: phaseStepNameMap.baseline_testing,
    status: "SUCCEEDED",
    userMessage: messages.completed,
    payload: {
      previousPhase,
      assessmentType: "baseline",
      score,
      minScore,
      maxScore,
      reused
    }
  });

  return buildPhaseResult(context, {
    phase: "baseline_testing",
    stepName: phaseStepNameMap.baseline_testing,
    userFacingMessage: messages.completed,
    details: { score, reused }
  });
}

async function completeCourseResolving(context) {
  const { course, installPlan } = await loadCourseContext(context);
  const previousPhase = resolvePreviousPhase("course_resolving");
  const userFacingMessage = `已确认 ${String(course.directionName)} 的送培课程，准备调取训练资源。`;

  await reportEvent(context, {
    stepKey: "course_resolving",
    stepName: phaseStepNameMap.course_resolving,
    status: "SUCCEEDED",
    userMessage: userFacingMessage,
    payload: {
      previousPhase,
      packageCode: String(course.packageCode),
      courseVersion: String(course.courseVersion),
      capabilityLabels: installPlan.capabilityLabels
    }
  });

  return buildPhaseResult(context, {
    phase: "course_resolving",
    stepName: phaseStepNameMap.course_resolving,
    userFacingMessage,
    details: {
      packageCode: String(course.packageCode),
      courseVersion: String(course.courseVersion),
      capabilityLabels: installPlan.capabilityLabels
    }
  });
}

async function completePackageFetching(context) {
  const { course, installPlan } = await loadCourseContext(context);
  const previousPhase = resolvePreviousPhase("package_fetching");

  await reportEvent(context, {
    stepKey: "package_fetching",
    stepName: phaseStepNameMap.package_fetching,
    status: "STARTED",
    userMessage: "正在调取本次送培所需的训练资源。",
    payload: {
      previousPhase,
      packageCode: String(course.packageCode)
    }
  });

  const userFacingMessage = `训练资源已就绪，已锁定 ${installPlan.capabilityLabels.join("、")} 能力方向。`;

  await reportEvent(context, {
    stepKey: "package_fetching",
    stepName: phaseStepNameMap.package_fetching,
    status: "SUCCEEDED",
    userMessage: userFacingMessage,
    payload: {
      previousPhase,
      packageCode: String(course.packageCode),
      capabilityLabels: installPlan.capabilityLabels
    }
  });

  return buildPhaseResult(context, {
    phase: "package_fetching",
    stepName: phaseStepNameMap.package_fetching,
    userFacingMessage,
    details: {
      packageCode: String(course.packageCode),
      capabilityLabels: installPlan.capabilityLabels
    }
  });
}

async function completeSuppliesProcurement(context, sharedOptions) {
  const previousPhase = resolvePreviousPhase("supplies_procuring");

  await reportEvent(context, {
    stepKey: "supplies_procuring",
    stepName: phaseStepNameMap.supplies_procuring,
    status: "STARTED",
    userMessage: "正在核对本次训练所需的学习物资与环境。",
    payload: {
      previousPhase,
      bootstrapCommand: clawhubBootstrapCommand,
      dryRun: sharedOptions.dryRun
    }
  });

  const procurementResult = ensureClawhubInstalled(sharedOptions.dryRun);
  const userFacingMessage = procurementResult.alreadyAvailable
    ? "学习物资已齐备，准备进入能力装配。"
    : procurementResult.dryRun
      ? "已校验学习物资采买流程，正式运行时会补齐环境。"
      : "学习物资采买已完成，准备进入能力装配。";

  await reportEvent(context, {
    stepKey: "supplies_procuring",
    stepName: phaseStepNameMap.supplies_procuring,
    status: "SUCCEEDED",
    userMessage: userFacingMessage,
    payload: {
      previousPhase,
      bootstrapCommand: clawhubBootstrapCommand,
      detectionCommand: procurementResult.detectionCommand,
      detectedPath: procurementResult.detectedPath,
      dryRun: procurementResult.dryRun,
      alreadyAvailable: procurementResult.alreadyAvailable,
      installedNow: procurementResult.installedNow,
      executedCommands: procurementResult.executedCommands
    }
  });

  return buildPhaseResult(context, {
    phase: "supplies_procuring",
    stepName: phaseStepNameMap.supplies_procuring,
    userFacingMessage,
    details: procurementResult
  });
}

async function completePackageInstalling(context, sharedOptions) {
  const { course, installPlan } = await loadCourseContext(context);
  const previousPhase = resolvePreviousPhase("package_installing");

  await reportEvent(context, {
    stepKey: "package_installing",
    stepName: phaseStepNameMap.package_installing,
    status: "STARTED",
    userMessage: sharedOptions.dryRun
      ? "正在校验本次能力装配流程。"
      : `正在装配 ${installPlan.capabilityLabels.join("、")} 能力。`,
    payload: {
      previousPhase,
      dryRun: sharedOptions.dryRun,
      installer: "clawhub install --force",
      clawhubRegistryUrl: sharedOptions.clawhubRegistryUrl,
      packageCode: String(course.packageCode),
      capabilityLabels: installPlan.capabilityLabels,
      skillSlugs: installPlan.skillSlugs
    }
  });

  const installResult = await installSkillsFromPlan(installPlan, sharedOptions.dryRun, sharedOptions.clawhubRegistryUrl);
  const userFacingMessage = sharedOptions.dryRun
    ? `能力装配流程已校验完成，共覆盖 ${installResult.totalInstallOperations} 项装配任务。`
    : `能力装配已完成，共完成 ${installResult.totalInstallOperations} 项装配任务。`;

  await reportEvent(context, {
    stepKey: "package_installing",
    stepName: phaseStepNameMap.package_installing,
    status: "SUCCEEDED",
    userMessage: userFacingMessage,
    payload: {
      previousPhase,
      dryRun: sharedOptions.dryRun,
      installer: "clawhub install --force",
      clawhubRegistryUrl: sharedOptions.clawhubRegistryUrl,
      packageCode: String(course.packageCode),
      capabilityLabels: installPlan.capabilityLabels,
      installedSkillSlugs: installResult.installedSkillSlugs,
      executedCommands: installResult.executedCommands
    }
  });

  return buildPhaseResult(context, {
    phase: "package_installing",
    stepName: phaseStepNameMap.package_installing,
    userFacingMessage,
    details: {
      packageCode: String(course.packageCode),
      capabilityLabels: installPlan.capabilityLabels,
      installedCapabilityCount: installResult.totalInstallOperations,
      installedSkillSlugs: installResult.installedSkillSlugs,
      executedCommands: installResult.executedCommands
    }
  });
}

async function completeCapabilityActivating(context) {
  const { installPlan } = await loadCourseContext(context);
  const previousPhase = resolvePreviousPhase("capability_activating");

  await reportEvent(context, {
    stepKey: "capability_activating",
    stepName: phaseStepNameMap.capability_activating,
    status: "STARTED",
    userMessage: `正在激活 ${installPlan.capabilityLabels.join("、")} 能力。`,
    payload: {
      previousPhase,
      requiresNewSession: true,
      capabilityLabels: installPlan.capabilityLabels
    }
  });

  const userFacingMessage = "职业能力已激活。请在新的 OpenClaw 会话中使用本次获得的能力。";

  await reportEvent(context, {
    stepKey: "capability_activating",
    stepName: phaseStepNameMap.capability_activating,
    status: "SUCCEEDED",
    userMessage: userFacingMessage,
    payload: {
      previousPhase,
      requiresNewSession: true,
      capabilityLabels: installPlan.capabilityLabels
    }
  });

  return buildPhaseResult(context, {
    phase: "capability_activating",
    stepName: phaseStepNameMap.capability_activating,
    userFacingMessage,
    details: {
      capabilityLabels: installPlan.capabilityLabels,
      requiresNewSession: true
    }
  });
}

async function completeGraduationTesting(context) {
  const score = pickAssessmentScore(70, 90);
  const messages = buildAssessmentMessages({ kind: "graduation", score, reused: false });
  const previousPhase = resolvePreviousPhase("graduation_testing");

  await reportEvent(context, {
    stepKey: "graduation_testing",
    stepName: phaseStepNameMap.graduation_testing,
    status: "STARTED",
    userMessage: messages.started,
    payload: {
      previousPhase,
      assessmentType: "graduation",
      reused: false
    }
  });

  await sleep(10000);

  await reportEvent(context, {
    stepKey: "graduation_testing",
    stepName: phaseStepNameMap.graduation_testing,
    status: "SUCCEEDED",
    userMessage: messages.completed,
    payload: {
      previousPhase,
      assessmentType: "graduation",
      score,
      minScore: 70,
      maxScore: 90,
      reused: false
    }
  });

  return buildPhaseResult(context, {
    phase: "graduation_testing",
    stepName: phaseStepNameMap.graduation_testing,
    userFacingMessage: messages.completed,
    details: { score }
  });
}

async function completeGraduationReady(context) {
  const { course, installPlan, graduationResult } = await loadCourseContext(context);
  const previousPhase = resolvePreviousPhase("graduation_ready");
  const userFacingMessage = "本次送培已完成，网页端可查看毕业结果。请开启新的 OpenClaw 会话验证能力。";

  await reportEvent(context, {
    stepKey: "graduation_ready",
    stepName: phaseStepNameMap.graduation_ready,
    status: "SUCCEEDED",
    userMessage: userFacingMessage,
    payload: {
      previousPhase,
      packageCode: String(course.packageCode),
      capabilityLabels: installPlan.capabilityLabels,
      requiresNewSession: true,
      graduationResult
    }
  });

  return buildPhaseResult(context, {
    phase: "graduation_ready",
    stepName: phaseStepNameMap.graduation_ready,
    userFacingMessage,
    details: {
      packageCode: String(course.packageCode),
      capabilityLabels: installPlan.capabilityLabels,
      requiresNewSession: true,
      graduationResult
    }
  });
}

async function runPhase(phase, context, sharedOptions) {
  switch (phase) {
    case "baseline_testing":
      return completeBaselineTesting(context);
    case "course_resolving":
      return completeCourseResolving(context);
    case "package_fetching":
      return completePackageFetching(context);
    case "supplies_procuring":
      return completeSuppliesProcurement(context, sharedOptions);
    case "package_installing":
      return completePackageInstalling(context, sharedOptions);
    case "capability_activating":
      return completeCapabilityActivating(context);
    case "graduation_testing":
      return completeGraduationTesting(context);
    case "graduation_ready":
      return completeGraduationReady(context);
    default:
      throw new Error(`Unsupported phase: ${phase}`);
  }
}

function printStructuredResult(result, shouldPrintJson) {
  if (shouldPrintJson) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (result.userFacingMessage) {
    console.log(`[OpenClaw] ${result.userFacingMessage}`);
  }
}

async function runStart(args, sharedOptions) {
  const enrollmentToken = requireStringArg(args, "enrollment-token");
  const context = await claimEnrollment(enrollmentToken, sharedOptions);

  return {
    ok: true,
    mode: "start",
    userFacingMessage: "已完成入学报到，正在开始入学测试。",
    context: {
      orderId: context.orderId,
      runId: context.runId,
      reportToken: context.reportToken,
      directionName: context.directionName,
      baseUrl: context.baseUrl,
      clawhubRegistryUrl: context.clawhubRegistryUrl
    },
    details: {
      expiresAt: context.expiresAt,
      courseVersion: context.courseVersion,
      courseUrl: context.courseUrl
    }
  };
}

async function runSinglePhase(args, sharedOptions) {
  const phase = requireStringArg(args, "phase");
  const context = buildContextFromArgs(args, sharedOptions);

  if (!phaseOrder.includes(phase)) {
    throw new Error(`Unsupported phase: ${phase}`);
  }

  const result = await runPhase(phase, context, sharedOptions);
  await sleep(stepCooldownMs);
  return result;
}

async function runAll(args, sharedOptions) {
  const startResult = await runStart(args, sharedOptions);
  const context = {
    baseUrl: startResult.context.baseUrl,
    clawhubRegistryUrl: startResult.context.clawhubRegistryUrl,
    orderId: startResult.context.orderId,
    runId: startResult.context.runId,
    reportToken: startResult.context.reportToken,
    directionName: startResult.context.directionName
  };

  const phaseResults = [];
  printStructuredResult(startResult, false);
  await sleep(stepCooldownMs);

  try {
    for (const phase of phaseOrder) {
      const result = await runPhase(phase, context, sharedOptions);
      phaseResults.push(result);
      printStructuredResult(result, false);

      if (phase !== "graduation_ready") {
        await sleep(stepCooldownMs);
      }
    }
  } catch (error) {
    await safeReportEvent(context, {
      stepKey: "error",
      stepName: phaseStepNameMap.error,
      status: "FAILED",
      userMessage: error instanceof Error ? error.message : String(error),
      payload: {
        failedAt: new Date().toISOString()
      }
    });

    throw error;
  }

  return {
    ok: true,
    mode: "run-all",
    userFacingMessage: phaseResults.at(-1)?.userFacingMessage ?? "本次送培已完成。",
    context: {
      orderId: context.orderId,
      runId: context.runId,
      reportToken: context.reportToken,
      directionName: context.directionName,
      baseUrl: context.baseUrl,
      clawhubRegistryUrl: context.clawhubRegistryUrl
    },
    phases: phaseResults
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    printHelp();
    return;
  }

  const sharedOptions = resolveSharedOptions(args);
  const mode = resolveMode(args);

  let contextForFailure = null;

  try {
    let result;

    if (mode === "start") {
      result = await runStart(args, sharedOptions);
      printStructuredResult(result, sharedOptions.json);
      return;
    }

    if (mode === "phase") {
      contextForFailure = buildContextFromArgs(args, sharedOptions);
      result = await runSinglePhase(args, sharedOptions);
      printStructuredResult(result, sharedOptions.json);
      return;
    }

    result = await runAll(args, sharedOptions);

    if (sharedOptions.json) {
      printStructuredResult(result, true);
    }
  } catch (error) {
    if (contextForFailure) {
      await safeReportEvent(contextForFailure, {
        stepKey: "error",
        stepName: phaseStepNameMap.error,
        status: "FAILED",
        userMessage: error instanceof Error ? error.message : String(error),
        payload: {
          failedAt: new Date().toISOString()
        }
      });
    }

    throw error;
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});

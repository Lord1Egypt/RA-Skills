#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { executeTransactionalBatch } from "../../main-image-editor/lib/task-orchestrator.js";
import { aggregateDelivery } from "../lib/delivery.js";
import { parsePptRequest } from "../lib/ppt-parser.js";
import { buildBatchPreviewTasks, deriveBatchExportSpec } from "../lib/task-builder.js";

function parseArgs(argv) {
  const args = {
    request: "",
    dryRun: false,
    force: false,
    index: "",
    threshold: undefined,
    outputDir: "",
    timeoutMs: undefined,
    copyPsdLocal: false,
    help: false,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--request") {
      args.request = argv[i + 1] || "";
      i += 1;
    } else if (arg === "--dry-run") {
      args.dryRun = true;
    } else if (arg === "--force") {
      args.force = true;
    } else if (arg === "--index") {
      args.index = argv[i + 1] || "";
      i += 1;
    } else if (arg === "--threshold") {
      args.threshold = Number(argv[i + 1]);
      i += 1;
    } else if (arg === "--output-dir") {
      args.outputDir = argv[i + 1] || "";
      i += 1;
    } else if (arg === "--timeout-ms") {
      args.timeoutMs = Number(argv[i + 1]);
      i += 1;
    } else if (arg === "--copy-psd-local") {
      args.copyPsdLocal = true;
    } else if (arg === "--help" || arg === "-h") {
      args.help = true;
    }
  }
  return args;
}

function readRequest(filePath) {
  const resolved = path.resolve(filePath);
  const raw = fs.readFileSync(resolved, "utf8");
  return JSON.parse(raw);
}

function printResultAndExit(payload, code) {
  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
  process.exit(code);
}

function normalizeRequest(base, args) {
  const request = { ...(base || {}) };
  const exec = request.execution || {};
  request.execution = {
    ...exec,
    dryRun: Boolean(args.dryRun || exec.dryRun),
    force: Boolean(args.force || exec.force),
    indexPath: args.index || exec.indexPath,
    rollbackPolicy: "rollback_all",
    bundleZip: exec.bundleZip !== false,
    // Timeout: CLI flag > request JSON > default (10 min for large PSD files)
    timeoutMs: Number.isFinite(args.timeoutMs)
      ? args.timeoutMs
      : Number.isFinite(exec.timeoutMs)
        ? exec.timeoutMs
        : 600_000,
    // Copy PSD to local temp dir before processing to avoid external-drive I/O bottleneck
    copyPsdLocal: Boolean(args.copyPsdLocal || exec.copyPsdLocal),
  };
  if (Number.isFinite(args.threshold)) {
    request.confidenceThreshold = Number(args.threshold);
  }
  request.fallbackPolicy =
    request.fallbackPolicy === "structured_only" ? "structured_only" : "structured_first_with_ocr";
  request.delivery = {
    ...(request.delivery || {}),
    ...(args.outputDir ? { outputDir: args.outputDir } : {}),
  };
  return request;
}

function resolveFailures(executed = []) {
  return executed
    .filter((item) => item.status === "error")
    .map((item) => ({
      pageId: item.pageId,
      slideIndex: item.slideIndex,
      code: item.code || "E_EXEC_FAILED",
      message: item.message || "Unknown execution failure.",
    }));
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help || !args.request) {
    process.stdout.write(
      "Usage: run-ppt-task-orchestrator.js --request <request.json> [--dry-run] [--force] [--index <index>] [--threshold <0-1>] [--output-dir <dir>] [--timeout-ms <ms>] [--copy-psd-local]\n",
    );
    process.exit(args.help ? 0 : 1);
  }

  let request;
  try {
    request = normalizeRequest(readRequest(args.request), args);
  } catch (error) {
    printResultAndExit(
      {
        status: "error",
        code: "E_TASK_INVALID",
        message: `Cannot read request: ${error.message}`,
      },
      1,
    );
  }

  const parsed = await parsePptRequest(request);
  if (!parsed.ok) {
    printResultAndExit(
      {
        requestId: request.requestId || `ppt-task-request-${Date.now()}`,
        status: "error",
        code: parsed.code,
        message: parsed.message,
      },
      1,
    );
  }

  const built = buildBatchPreviewTasks({ pages: parsed.pages });
  if (!built.ok) {
    printResultAndExit(
      {
        requestId: request.requestId || `ppt-task-request-${Date.now()}`,
        status: "error",
        code: built.code,
        message: built.message,
      },
      1,
    );
  }

  // Apply globalConfig from Slide 1 (if present) — outputDir, dateFolder, copyPsdLocal hints.
  const globalConfig = parsed.globalConfig || {};
  if (globalConfig.outputDir && !request.delivery?.outputDir) {
    request.delivery = {
      ...(request.delivery || {}),
      outputDir: globalConfig.outputDir,
    };
  }
  // If globalConfig says date folder, append today's date to the outputDir.
  if (globalConfig.dateFolder && request.delivery?.outputDir) {
    const today = new Date();
    const dateStr = `${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, "0")}${String(today.getDate()).padStart(2, "0")}`;
    request.delivery.outputDir = `${request.delivery.outputDir}/${dateStr}`;
    request.delivery.skipTimestampSubdir = true; // signal to aggregateDelivery
  }
  // globalConfig copyPsdLocal hint: apply if not already explicitly set.
  if (globalConfig.copyPsdLocal && !request.execution?.copyPsdLocal) {
    request.execution = { ...(request.execution || {}), copyPsdLocal: true };
  }

  const threshold = Number.isFinite(Number(request.confidenceThreshold))
    ? Number(request.confidenceThreshold)
    : 0.8;
  const execution = request.execution || {};
  const exportSpec = deriveBatchExportSpec(built.sortedPages);
  const exports = [
    {
      format: "png",
      mode: exportSpec.mode,
      folderName: `ppt-task-${Date.now()}`,
    },
  ];

  const executionResult = executeTransactionalBatch({
    previewTasks: built.previewTasks,
    threshold,
    force: Boolean(execution.force),
    dryRun: Boolean(execution.dryRun),
    indexPath: execution.indexPath,
    bundleZip: exportSpec.bundleZip && execution.bundleZip !== false,
    bundle: {
      zipName: `ppt-task-${Date.now()}.zip`,
    },
    exports,
    keepBackups: false,
    timeoutMs: execution.timeoutMs,
    copyPsdLocal: Boolean(execution.copyPsdLocal),
  });

  const taskMetaById = built.taskMetaById;
  const executedWithPage = (executionResult.result.executed || []).map((item) => {
    const meta = taskMetaById.get(item.taskId) || {};
    return {
      ...item,
      pageId: meta.pageId || item.taskId,
      slideIndex: meta.slideIndex || 0,
      parseMode: meta.parseMode || "structured",
    };
  });

  let delivery = {
    deliveryDir: "",
    bundleZipPath: "",
  };
  const finalStatus = executionResult.result.status;
  if (finalStatus !== "error" && finalStatus !== "needs_confirmation") {
    delivery = await aggregateDelivery({
      requestId: request.requestId || `ppt-task-request-${Date.now()}`,
      delivery: request.delivery || {},
      dryRun: Boolean(execution.dryRun),
      executed: executedWithPage,
    });
  }

  const failures = resolveFailures(executedWithPage);
  const payload = {
    requestId: request.requestId || `ppt-task-request-${Date.now()}`,
    status: finalStatus,
    code: executionResult.result.code,
    summary: executionResult.result.summary,
    threshold,
    dryRun: Boolean(execution.dryRun),
    forced: Boolean(execution.force),
    parsedPages: parsed.pages,
    executed: executedWithPage,
    deliveryDir: delivery.deliveryDir || undefined,
    bundleZipPath: delivery.bundleZipPath || undefined,
    failures,
    rolledBack: executionResult.result.rolledBack,
    rollbackCount: executionResult.result.rollbackCount,
  };
  printResultAndExit(payload, finalStatus === "error" ? 1 : 0);
}

main().catch((error) => {
  printResultAndExit(
    {
      status: "error",
      code: "E_EXEC_FAILED",
      message: error instanceof Error ? error.message : String(error),
    },
    1,
  );
});

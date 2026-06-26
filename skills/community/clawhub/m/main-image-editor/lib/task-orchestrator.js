import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { resolvePsdPath, DEFAULT_INDEX } from "../../psd-automator/lib/index-resolver.js";
import { expandHome } from "../../psd-automator/lib/paths.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const runTaskScript = path.resolve(__dirname, "../../psd-automator/scripts/run-task.js");

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function writeJsonTemp(prefix, payload) {
  const dir = path.join(os.tmpdir(), "openclaw-main-image-editor");
  ensureDir(dir);
  const filePath = path.join(
    dir,
    `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2)}.json`,
  );
  fs.writeFileSync(filePath, JSON.stringify(payload, null, 2), "utf8");
  return filePath;
}

function runPsdAutomator(taskPath, params) {
  const args = [runTaskScript, "--task", taskPath];
  if (params.indexPath) {
    args.push("--index", params.indexPath);
  }
  if (params.dryRun) {
    args.push("--dry-run");
  }
  const result = spawnSync("node", args, {
    encoding: "utf8",
    // Default 10 min; large PSD files (200MB+) from external drives need more time.
    timeout: params.timeoutMs || 600_000,
  });
  if (result.error && result.error.code === "ETIMEDOUT") {
    return {
      process: result,
      payload: {
        status: "error",
        code: "E_EXEC_TIMEOUT",
        message: "psd-automator runner timed out.",
      },
    };
  }
  const text = (result.stdout || result.stderr || "").trim();
  let parsed;
  if (text) {
    try {
      parsed = JSON.parse(text);
    } catch {
      parsed = {
        status: "error",
        code: "E_EXEC_FAILED",
        message: text,
      };
    }
  } else {
    parsed = {
      status: "error",
      code: "E_EXEC_FAILED",
      message: "Runner returned empty output.",
    };
  }
  return { process: result, payload: parsed };
}

function resolveTargetPath(task, indexPath) {
  const resolved = resolvePsdPath({
    exactPath: task.exactPath,
    fileHint: task.fileHint,
    indexPath: path.resolve(expandHome(indexPath || DEFAULT_INDEX)),
  });
  return resolved;
}

function backupTarget(pathToBackup) {
  const stamp = new Date()
    .toISOString()
    .replace(/[-:TZ.]/g, "")
    .slice(0, 14);
  const backupPath = `${pathToBackup}.txn-bak.${stamp}`;
  fs.copyFileSync(pathToBackup, backupPath);
  return backupPath;
}

// Copy a PSD/PSB to a local temp directory so Photoshop I/O runs on local SSD
// instead of a potentially slow external/network drive. Returns the local path.
function copyPsdToLocal(sourcePath, label) {
  const dir = path.join(os.tmpdir(), "openclaw-psd-local");
  ensureDir(dir);
  const ext = path.extname(sourcePath) || ".psd";
  const localPath = path.join(
    dir,
    `psd-${label || "local"}-${Date.now()}-${Math.random().toString(16).slice(2)}${ext}`,
  );
  fs.copyFileSync(sourcePath, localPath);
  return localPath;
}

function cleanupPaths(paths = []) {
  for (const p of paths) {
    if (!p) continue;
    try {
      if (fs.existsSync(p)) {
        const stat = fs.statSync(p);
        if (stat.isDirectory()) {
          fs.rmSync(p, { recursive: true, force: true });
        } else {
          fs.rmSync(p, { force: true });
        }
      }
    } catch {
      // best effort cleanup
    }
  }
}

function parseAvailableLayersFromMessage(message) {
  const text = String(message || "");
  const marker = "AVAILABLE_LAYERS:";
  const idx = text.indexOf(marker);
  if (idx < 0) return [];
  const tail = text.slice(idx + marker.length);
  const firstLine = (tail.split(/\r?\n/)[0] || "").split(/\.\s*(?:\r?直线:|line:)/)[0] || "";
  return firstLine
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function remapEditsByAvailableLayers(edits, availableLayers) {
  if (!Array.isArray(edits) || edits.length === 0 || availableLayers.length === 0) return null;
  const looseMatch = (a, b) => {
    const left = String(a || "").trim();
    const right = String(b || "").trim();
    if (!left || !right) return false;
    if (left === right) return true;
    if (left.includes(right) || right.includes(left)) return true;
    const leftTail = left.length > 1 ? left.slice(1) : left;
    const rightTail = right.length > 1 ? right.slice(1) : right;
    return Boolean(
      (leftTail && (right.includes(leftTail) || rightTail.includes(leftTail))) ||
      (rightTail && (left.includes(rightTail) || leftTail.includes(rightTail))),
    );
  };
  const replaceWithin = (line, source, target) => {
    const value = String(line || "");
    if (!value) return "";
    if (value.includes(source)) {
      return value.replace(source, target);
    }
    if (source.length > 1) {
      const tail = source.slice(1).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const relaxed = new RegExp(`[A-Za-z&€¥￥]?${tail}`);
      if (relaxed.test(value)) {
        return value.replace(relaxed, target);
      }
    }
    return "";
  };
  const pickBestLayer = (needle) => {
    const n = String(needle || "").trim();
    if (!n) return "";
    const candidates = availableLayers
      .map((layer) => {
        const l = String(layer || "").trim();
        if (!l) return null;
        if (!looseMatch(l, n)) return null;
        // lower score is better
        let score = 1000;
        if (l === n) score = 0;
        else if (l.startsWith(n) || l.endsWith(n)) score = 8 + Math.abs(l.length - n.length);
        else if (l.includes(n) || n.includes(l)) score = 16 + Math.abs(l.length - n.length);
        else score = 40 + Math.abs(l.length - n.length);
        return { layer: l, score };
      })
      .filter(Boolean)
      .sort((a, b) => a.score - b.score);
    return candidates[0]?.layer || "";
  };
  let changed = false;
  const remapped = edits.map((edit) => {
    const name = String(edit.layerName || "").trim();
    if (!name) return edit;
    const exact = availableLayers.find((layer) => layer === name);
    if (exact) return edit;
    if (edit.op === "replace_text" && edit.newText) {
      const byTarget = pickBestLayer(edit.newText);
      if (byTarget) {
        changed = true;
        const rewritten = replaceWithin(byTarget, name, edit.newText);
        const keepStructure = byTarget.includes(edit.newText) ? byTarget : edit.newText;
        return {
          ...edit,
          layerName: byTarget,
          // Prefer structure-preserving rewrite; when source is already replaced,
          // keep the full candidate copy instead of collapsing into short target text.
          newText: rewritten || keepStructure,
        };
      }
    }
    const contains = pickBestLayer(name);
    if (!contains) return edit;
    changed = true;
    if (edit.op === "replace_text" && edit.newText) {
      const rewritten = replaceWithin(contains, name, edit.newText);
      const keepStructure = contains.includes(edit.newText) ? contains : edit.newText;
      return {
        ...edit,
        layerName: contains,
        newText: rewritten || keepStructure,
      };
    }
    return { ...edit, layerName: contains };
  });
  return changed ? remapped : null;
}

export function buildPsdTask(previewTask, opts = {}) {
  return {
    taskId: previewTask.taskId,
    input: {
      exactPath: previewTask.exactPath,
      fileHint: previewTask.fileHint,
      edits: previewTask.edits.map((item) => {
        if (item.op === "place_image") {
          // Preserve all place_image specific fields.
          return {
            op: "place_image",
            imagePath: item.imagePath || "",
            layerName: item.layerName || "",
            position: item.position || "top",
            visible: item.visible !== false,
            targetArtboard: item.targetArtboard || "",
          };
        }
        return {
          layerName: item.layerName,
          newText: item.newText,
          op: item.op,
        };
      }),
    },
    workflow: {
      sourceMode: "inplace",
    },
    output: {
      psd: { mode: "overwrite" },
      exports: Array.isArray(opts.exports) ? opts.exports : [],
      bundle: opts.bundle || {},
    },
    options: {
      styleLock: true,
      createBackup: false,
      retryOnLockedFile: true,
      maxRetries: 2,
      bundleZip: opts.bundleZip === true,
      ...(opts.matchImagePath ? { matchImagePath: opts.matchImagePath } : {}),
    },
  };
}

export function shouldRequireConfirmation(previewTasks, threshold, force = false, dryRun = false) {
  if (dryRun || force) return false;
  return previewTasks.some((task) => Number(task.minConfidence) < Number(threshold));
}

export function executeTransactionalBatch(params) {
  const threshold = Number.isFinite(Number(params.threshold)) ? Number(params.threshold) : 0.8;
  const previewTasks = params.previewTasks || [];
  if (previewTasks.length === 0) {
    return {
      ok: false,
      result: {
        status: "error",
        code: "E_TASK_INVALID",
        message: "No preview tasks to execute.",
      },
    };
  }

  if (shouldRequireConfirmation(previewTasks, threshold, params.force, params.dryRun)) {
    return {
      ok: true,
      result: {
        status: "needs_confirmation",
        code: "E_LOW_CONFIDENCE",
        summary: `Low confidence tasks detected (threshold=${threshold}).`,
        threshold,
        dryRun: false,
        forced: false,
        previewTasks,
      },
    };
  }

  const indexPath = params.indexPath || DEFAULT_INDEX;
  const copyPsdLocal = Boolean(params.copyPsdLocal);
  const rollbackRecords = [];
  const localCopyPaths = new Set();
  const producedPaths = new Set();
  const executed = [];

  // Snapshot map: originalPath → stable local snapshot (copied once from the
  // original before any task runs). Each task gets its own working copy from
  // the snapshot, so multiple tasks targeting the same PSD always start from
  // the same pristine state — the original file is never modified.
  const psdSnapshots = new Map();

  try {
    for (let taskIdx = 0; taskIdx < previewTasks.length; taskIdx++) {
      const task = previewTasks[taskIdx];
      const resolved = resolveTargetPath(task, indexPath);
      if (!resolved.ok) {
        if (copyPsdLocal) {
          // Snapshot-isolation: record error and continue; originals are untouched.
          executed.push({
            taskId: task.taskId,
            status: "error",
            resolvedPath: "",
            psdOutputPath: "",
            pngOutputPaths: [],
            selectedPngPath: "",
            bundleZipPath: "",
            code: resolved.code || "E_FILE_NOT_FOUND",
            message: resolved.message || "Target PSD resolve failed.",
          });
          continue;
        }
        throw {
          code: resolved.code || "E_FILE_NOT_FOUND",
          message: resolved.message || "Target PSD resolve failed.",
          taskId: task.taskId,
        };
      }

      // --copy-psd-local: snapshot-isolation mode.
      // 1. Take one snapshot of each unique original PSD (copy from original once).
      // 2. Each task gets a fresh working copy from the snapshot, NOT from the
      //    original. This means multiple tasks on the same PSD each start from
      //    the same pristine state even after previous tasks have modified it.
      // 3. No write-back to the original: exports (PNG/ZIP) are the deliverables.
      //    The original file on disk is never touched.
      let workingPath = resolved.path;
      let localCopyPath = "";
      if (copyPsdLocal) {
        if (!psdSnapshots.has(resolved.path)) {
          const snap = copyPsdToLocal(resolved.path, "snap");
          psdSnapshots.set(resolved.path, snap);
          localCopyPaths.add(snap);
        }
        const snapshot = psdSnapshots.get(resolved.path);
        localCopyPath = copyPsdToLocal(snapshot, "work");
        localCopyPaths.add(localCopyPath);
        workingPath = localCopyPath;
        // No rollback record needed: original is never modified.
      } else {
        const backupPath = backupTarget(resolved.path);
        rollbackRecords.push({ originalPath: resolved.path, backupPath });
      }

      const taskWithLocalPath = copyPsdLocal
        ? { ...task, exactPath: workingPath, fileHint: "" }
        : task;

      // Per-task unique export path to prevent PNG overwriting when multiple
      // tasks target the same PSD (same source → same default export filename).
      // Strategy:
      //   single mode  → fileName = "<taskId>.png"  (e.g. "P001.png")
      //   layer_sets   → folderName gets a unique subfolder (e.g. "ppt-task-xxx/000-P001/")
      // This ensures each task's PNG is independently named at the point of export,
      // so collisions are impossible even if tasks share the same output directory.
      const taskSubfolder = `${String(taskIdx).padStart(3, "0")}-${task.taskId}`;
      const taskExports = (params.exports || []).map((exp) => {
        const isLayerSets = exp.mode === "layer_sets";
        // Per-task artboardName overrides any global setting; propagate to export spec.
        const artboardName = task.artboardName || exp.artboardName || "";
        return {
          ...exp,
          folderName: exp.folderName ? `${exp.folderName}/${taskSubfolder}` : taskSubfolder,
          artboardName,
          // For single-file exports, override fileName with the taskId so the
          // file is named "P001.png" instead of "<psdName>.png".
          ...(!isLayerSets && !artboardName && !exp.fileName ? { fileName: `${task.taskId}.png` } : {}),
        };
      });

      const psdTask = buildPsdTask(taskWithLocalPath, {
        exports: taskExports,
        bundle: params.bundle,
        bundleZip: params.bundleZip,
        matchImagePath: params.screenshotPath,
      });
      const tempTaskPath = writeJsonTemp("main-image-task", psdTask);
      let run = runPsdAutomator(tempTaskPath, {
        indexPath,
        dryRun: Boolean(params.dryRun),
        timeoutMs: params.timeoutMs,
      });
      cleanupPaths([tempTaskPath]);

      let payload = run.payload || {};
      if (payload.code === "E_LAYER_NOT_FOUND" && typeof payload.message === "string") {
        const availableLayers = parseAvailableLayersFromMessage(payload.message);
        const remappedEdits = remapEditsByAvailableLayers(task.edits, availableLayers);
        if (remappedEdits && remappedEdits.length > 0) {
          const retryTask = buildPsdTask(
            { ...task, edits: remappedEdits },
            {
              exports: taskExports,
              bundle: params.bundle,
              bundleZip: params.bundleZip,
              matchImagePath: params.screenshotPath,
            },
          );
          const retryTaskPath = writeJsonTemp("main-image-task-retry", retryTask);
          run = runPsdAutomator(retryTaskPath, {
            indexPath,
            dryRun: Boolean(params.dryRun),
            timeoutMs: params.timeoutMs,
          });
          cleanupPaths([retryTaskPath]);
          payload = run.payload || payload;
        }
      }
      const status =
        payload.status === "success" || payload.status === "dry-run" ? "success" : "error";
      executed.push({
        taskId: task.taskId,
        status,
        resolvedPath: payload.resolvedPath,
        psdOutputPath: payload.psdOutputPath,
        pngOutputPaths: payload.pngOutputPaths || [],
        selectedPngPath: payload.selectedPngPath,
        bundleZipPath: payload.bundleZipPath,
        code: payload.code,
        message: payload.message,
      });

      if (status === "success") {
        // Only track produced paths for non-copyPsdLocal mode rollback.
        if (!copyPsdLocal) {
          for (const p of payload.pngOutputPaths || []) producedPaths.add(p);
          if (payload.bundleZipPath) producedPaths.add(payload.bundleZipPath);
        }
      } else {
        if (copyPsdLocal) {
          // Snapshot-isolation: original PSD untouched. Record the error and
          // keep going — remaining tasks can still succeed independently.
          continue;
        }
        throw {
          code: payload.code || "E_EXEC_FAILED",
          message: payload.message || "psd-automator execution failed.",
          taskId: task.taskId,
        };
      }

      // copyPsdLocal mode: no write-back. Original PSD is never modified;
      // the exported PNG(s) are the only deliverables per task.
    }

    const successCount = executed.filter((e) => e.status === "success").length;
    const totalCount = previewTasks.length;
    const batchStatus = params.dryRun
      ? "dry-run"
      : successCount === totalCount
        ? "success"
        : successCount > 0
          ? "partial_success"
          : "error";
    const batchSummary = params.dryRun
      ? "Dry-run completed. No file changes committed."
      : successCount === totalCount
        ? "Batch execution completed."
        : `Partial success: ${successCount}/${totalCount} tasks succeeded.`;

    return {
      ok: batchStatus !== "error",
      result: {
        status: batchStatus,
        code: batchStatus === "error" ? "E_EXEC_FAILED" : "OK",
        summary: batchSummary,
        threshold,
        dryRun: Boolean(params.dryRun),
        forced: Boolean(params.force),
        previewTasks,
        executed,
        rolledBack: false,
        rollbackCount: 0,
      },
    };
  } catch (error) {
    let rollbackCount = 0;
    for (const record of rollbackRecords) {
      try {
        fs.copyFileSync(record.backupPath, record.originalPath);
        rollbackCount += 1;
      } catch {
        // keep best-effort rollback
      }
    }
    cleanupPaths([...producedPaths]);
    return {
      ok: false,
      result: {
        status: "error",
        code: error?.code || "E_EXEC_FAILED",
        summary: error?.message || "Transactional batch failed.",
        threshold,
        dryRun: Boolean(params.dryRun),
        forced: Boolean(params.force),
        previewTasks,
        executed,
        rolledBack: rollbackCount > 0,
        rollbackCount,
      },
    };
  } finally {
    // Keep backups for debugging only when keepBackups=true.
    if (!params.keepBackups) {
      cleanupPaths(rollbackRecords.map((x) => x.backupPath));
    }
    // Always clean up local PSD copies (working copies + snapshots).
    cleanupPaths([...localCopyPaths]);
    cleanupPaths([...psdSnapshots.values()]);
  }
}

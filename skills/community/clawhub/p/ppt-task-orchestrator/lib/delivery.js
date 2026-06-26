import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import JSZip from "jszip";

function expandHome(inputPath) {
  if (!inputPath) return "";
  const value = String(inputPath);
  if (value === "~") return os.homedir();
  if (value.startsWith("~/")) return path.join(os.homedir(), value.slice(2));
  return value;
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function safeFileName(value) {
  return String(value || "")
    .replace(/[^\w.-]+/g, "_")
    .replace(/^_+|_+$/g, "");
}

function selectImagePath(item) {
  if (item.selectedPngPath) return item.selectedPngPath;
  if (Array.isArray(item.pngOutputPaths) && item.pngOutputPaths.length > 0) {
    return item.pngOutputPaths[0];
  }
  return "";
}

export async function aggregateDelivery(params = {}) {
  const requestId = params.requestId || `ppt-task-${Date.now()}`;
  const deliveryConfig = params.delivery || {};
  const dryRun = Boolean(params.dryRun);
  const executed = Array.isArray(params.executed) ? params.executed : [];
  const copySelectedOnly = deliveryConfig.copySelectedOnly !== false;

  const root =
    path.resolve(
      expandHome(deliveryConfig.outputDir || path.join(".openclaw", "deliveries", requestId)),
    ) || path.resolve(path.join(".openclaw", "deliveries", requestId));
  // When skipTimestampSubdir is set (e.g. global config with dateFolder), use the
  // outputDir directly instead of appending a requestId-timestamp subdirectory.
  const deliveryDir = deliveryConfig.skipTimestampSubdir
    ? root
    : path.join(root, `${safeFileName(requestId)}-${Date.now()}`);
  const zipName = deliveryConfig.zipName || "all-images.zip";
  const bundleZipPath = path.join(deliveryDir, zipName);

  if (dryRun) {
    return {
      deliveryDir,
      bundleZipPath,
      copiedCount: 0,
      copiedFiles: [],
    };
  }

  ensureDir(deliveryDir);
  const copiedFiles = [];
  // Track used filenames within this delivery to avoid silent overwrites.
  const usedNames = new Set();
  for (const item of executed) {
    if (item.status !== "success") continue;
    const pageId = safeFileName(item.pageId || `slide-${item.slideIndex || "x"}`);
    // Always deliver all exported PNGs (not just the first "selected" one).
    // Multiple artboards from a single task (e.g. P002 logo → 前N首焦 + 续航首焦)
    // each get their own file named {pageId}-{artboardBaseName}{ext}.
    const allPaths = item.pngOutputPaths || [];
    const candidates = allPaths.length > 0 ? allPaths : [selectImagePath(item)];
    let index = 0;
    for (const sourcePath of candidates) {
      if (!sourcePath || !fs.existsSync(sourcePath)) continue;
      const ext = path.extname(sourcePath) || ".png";
      const baseName = path.basename(sourcePath, ext);
      // Prefer {pageId}-{artboardName} naming; fall back to {pageId}-{n} if needed.
      let fileName = `${pageId}-${baseName}${ext}`;
      if (usedNames.has(fileName)) {
        fileName = `${pageId}-${index + 1}${ext}`;
      }
      usedNames.add(fileName);
      const targetPath = path.join(deliveryDir, fileName);
      fs.copyFileSync(sourcePath, targetPath);
      copiedFiles.push(targetPath);
      index += 1;
    }
  }

  const zip = new JSZip();
  for (const copiedPath of copiedFiles) {
    const data = fs.readFileSync(copiedPath);
    zip.file(path.basename(copiedPath), data);
  }
  const buffer = await zip.generateAsync({
    type: "nodebuffer",
    compression: "DEFLATE",
    compressionOptions: { level: 6 },
  });
  fs.writeFileSync(bundleZipPath, buffer);
  return {
    deliveryDir,
    bundleZipPath,
    copiedCount: copiedFiles.length,
    copiedFiles,
  };
}

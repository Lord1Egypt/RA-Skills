import { spawnSync } from "node:child_process";
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

function toConfidence(raw, fallback = 0.9) {
  const num = Number(raw);
  if (!Number.isFinite(num)) return fallback;
  if (num < 0) return 0;
  if (num > 1) return 1;
  return num;
}

function xmlDecode(text) {
  return String(text || "")
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replaceAll("&amp;", "&")
    .replaceAll("&quot;", '"')
    .replaceAll("&apos;", "'");
}

function extractSlideTextLines(xml) {
  // Extract text at paragraph level: all <a:t> nodes inside one <a:p> are merged
  // into a single line. This prevents fragmentation where PPTX splits a single
  // visible string (e.g. "sourcePsd: 店铺存放2.psd") across multiple <a:t> nodes.
  const lines = [];
  const paraPattern = /<a:p\b[^>]*?>([\s\S]*?)<\/a:p>/g;
  for (const paraMatch of xml.matchAll(paraPattern)) {
    const paraXml = paraMatch[1] || "";
    const parts = [];
    const tokenPattern = /<a:t>([\s\S]*?)<\/a:t>/g;
    for (const tokenMatch of paraXml.matchAll(tokenPattern)) {
      const token = xmlDecode(tokenMatch[1] || "");
      if (token) parts.push(token);
    }
    // Right-trim only: preserve leading whitespace because PSD layer names can
    // legitimately start with spaces (e.g. " 直播间到手价¥").
    const line = parts.join("").replace(/[\s\uFEFF\xA0]+$/, "");
    if (line.trim()) lines.push(line);
  }
  return lines;
}

function parseRelationshipTargets(xml) {
  const map = new Map();
  const pattern = /<Relationship\b[^>]*\bId="([^"]+)"[^>]*\bTarget="([^"]+)"[^>]*\/?>/g;
  for (const match of xml.matchAll(pattern)) {
    map.set(String(match[1] || ""), String(match[2] || ""));
  }
  return map;
}

function parseSlideImageTargets(slideXml, relMap) {
  const targets = [];
  const pattern = /<a:blip\b[^>]*\br:embed="([^"]+)"[^>]*\/?>/g;
  for (const match of slideXml.matchAll(pattern)) {
    const rid = String(match[1] || "");
    const target = relMap.get(rid);
    if (target) targets.push(target);
  }
  return targets;
}

function parseSourcePsdFromText(text) {
  if (!text) return "";
  const match = String(text).match(/([^\s，。,;；"'`]+?\.(?:psd|psb))/i);
  return match?.[1]?.trim() || "";
}

function parseBoolean(text, fallback = true) {
  const value = String(text || "")
    .trim()
    .toLowerCase();
  if (!value) return fallback;
  if (["true", "1", "yes", "y", "on"].includes(value)) return true;
  if (["false", "0", "no", "n", "off"].includes(value)) return false;
  return fallback;
}

function parseEditsFromLines(lines) {
  const edits = [];
  for (const line of lines) {
    // Strip only the bullet marker itself (-, *, N., N)) but keep any leading
    // whitespace that precedes the bullet — those spaces may be significant parts
    // of the PSD layer name (e.g. "  1) 直播间到手价¥" → "  直播间到手价¥").
    const raw = String(line || "").replace(/[\s\uFEFF\xA0]+$/, "");
    // \s* (not \s+) so "1)layerName" with no space after bullet is also stripped.
    const bulletMatch = raw.match(/^([\s]*)(?:[-*][ \t]+|\d+[.)]\s*)([\s\S]*)$/);
    const value = bulletMatch ? bulletMatch[1] + bulletMatch[2] : raw;
    if (!value.trim()) continue;
    const match = value.match(/^(.+?)\s*(?:=>|->|＝>|→)\s*(.+)$/);
    if (!match) continue;
    // Preserve leading whitespace in layerName; only right-trim.
    const layerName = String(match[1] || "").replace(/\s+$/, "");
    const rhs = String(match[2] || "").trim();
    if (!layerName || !rhs) continue;

    // place_image op: "place_image => /path/to/img.png"
    //             or  "place_image:LOGO => /path/to/img.png"
    //             or  "置入 => /path/to/img.png"
    const placeMatch = layerName.match(/^(?:place_image|置入)(?::(.*))?$/i);
    if (placeMatch) {
      edits.push({
        op: "place_image",
        imagePath: rhs,
        layerName: placeMatch[1] ? placeMatch[1].trim() : "",
        position: "top",
        visible: true,
        confidence: 0.96,
      });
      continue;
    }

    if (/^delete$/i.test(rhs)) {
      edits.push({
        op: "delete_text",
        layerName,
        newText: "",
        confidence: 0.96,
      });
    } else {
      edits.push({
        op: "replace_text",
        layerName,
        newText: rhs,
        confidence: 0.98,
      });
    }
  }
  return edits;
}

function parseEditsFromChinese(text) {
  const edits = [];
  const source = String(text || "");
  const replacePattern =
    /(?:把)?([^，,。]+?)改成([\s\S]+?)(?=(?:，|,)?(?:把)?[^，,。]+?改成|(?:，|,)?(?:删除|移除|去掉|并保存|并导出|保存成|保存到|放置在|然后|$))/g;
  for (const match of source.matchAll(replacePattern)) {
    const layerName = (match[1] || "").trim();
    const newText = (match[2] || "").trim().replace(/[，,。]\s*$/, "");
    if (!layerName || !newText) continue;
    edits.push({
      op: "replace_text",
      layerName,
      newText,
      confidence: 0.82,
    });
  }
  const deletePattern =
    /(?:删除|移除|去掉)(?:图层)?\s*["“]?([^"”。，,]+)["”]?(?:\s*(?:文字|文案|内容))?/g;
  for (const match of source.matchAll(deletePattern)) {
    const layerName = (match[1] || "").trim();
    if (!layerName) continue;
    edits.push({
      op: "delete_text",
      layerName,
      newText: "",
      confidence: 0.78,
    });
  }
  return edits;
}

// Map Chinese KV labels to canonical English keys.
const ZH_KEY_MAP = {
  "图层名": "layername",
  "内容修改成": "newtext",
  "文件名": "filename",
  "文件路径": "filepath",
  "画板名": "artboardname",
  "导出文件的储存位置": "outputdir",
  "优先级": "priority",
  "备注": "note",
};

function normalizeKvKey(raw) {
  const s = raw.trim();
  // Try Chinese mapping first.
  if (ZH_KEY_MAP[s]) return ZH_KEY_MAP[s];
  return s.toLowerCase().replace(/\s+/g, "");
}

// Parse step-based place_image operations like:
// "第1步操作:将波咯咯家装节logo.png置入天猫首焦.psd，置入前N首焦这个画板的上方"
// filePaths: map of filename → full path collected from 文件路径: lines
function parseStepOps(lines, filePaths) {
  const edits = [];
  for (const line of lines) {
    const stepMatch = line.match(/^第\s*\d+\s*步操作\s*[:：]\s*(.+)$/);
    if (!stepMatch) continue;
    const content = stepMatch[1].trim();

    // "将X置入Y，置入Z这个画板的上方" pattern
    const placeMatch = content.match(
      /将(.+?)置入.+?，置入(.+?)(?:这个)?画板的上方/,
    );
    if (placeMatch) {
      const imgFileName = placeMatch[1].trim();
      const targetArtboard = placeMatch[2].trim();
      // Look up full image path from 文件路径 lines.
      const imagePath = filePaths.get(imgFileName) || imgFileName;
      edits.push({
        op: "place_image",
        imagePath,
        layerName: "",
        position: "top",
        visible: true,
        targetArtboard,
        confidence: 0.95,
      });
    }
  }
  return edits;
}

function parseStructuredFields(lines) {
  // Full-width colon → ASCII colon, right-trim only.
  const normalized = lines
    .map((line) => String(line || "").trim())
    .filter(Boolean)
    .map((line) => line.replace(/[：]/g, ":"));
  const allText = normalized.join("\n");
  let pageId = "";
  let sourcePsd = "";
  let exactPath = "";
  let priority = "P1";
  let note = "";
  let outputSpecLine = "";
  let artboardName = "";
  // Map filename → full path for image assets declared in 文件路径: lines.
  const filePaths = new Map();
  // Collect Windows UNC paths that could not be resolved to a local /Volumes path.
  const uncPathErrors = [];

  // Extended KV regex supports Chinese characters in key.
  const KV_RE = /^([\w\u4e00-\u9fff][\w\u4e00-\u9fff ]*)\s*:\s*(.+)$/;

  for (const line of normalized) {
    const kv = line.match(KV_RE);
    if (!kv) continue;
    const rawKey = normalizeKvKey(kv[1]);
    const value = kv[2].trim();

    if (rawKey === "pageid" || rawKey === "page id") {
      pageId = value;
    } else if (rawKey === "sourcepsd" || rawKey === "source psd") {
      // Apply UNC conversion for sourcePsd declared directly as a full path.
      const unc = tryConvertWindowsUncPath(value);
      if (unc.isUnc && !unc.exists) {
        uncPathErrors.push({ field: "sourcePsd", original: value, converted: unc.macPath });
      } else {
        sourcePsd = unc.macPath;
      }
    } else if (rawKey === "priority" || rawKey === "优先级") {
      priority = value.toUpperCase();
    } else if (rawKey === "note" || rawKey === "备注") {
      note = value;
    } else if (rawKey === "outputspec" || rawKey === "output spec") {
      outputSpecLine = value;
    } else if (rawKey === "artboardname") {
      artboardName = value;
    } else if (rawKey === "filename") {
      // 文件名: 天猫首焦.psd → use as sourcePsd if .psd
      if (/\.psd$/i.test(value) && !sourcePsd) sourcePsd = value;
    } else if (rawKey === "filepath") {
      // 文件路径: /Volumes/.../天猫首焦.psd → store full paths.
      // If the value is a Windows UNC path, try to convert it to a /Volumes path first.
      const unc = tryConvertWindowsUncPath(value);
      if (unc.isUnc && !unc.exists) {
        uncPathErrors.push({ field: "filePath", original: value, converted: unc.macPath });
      } else {
        const resolvedValue = unc.macPath;
        const baseName = resolvedValue.split(/[\\/]/).pop() || "";
        filePaths.set(baseName, resolvedValue);
        if (/\.psd$/i.test(resolvedValue) && !exactPath) {
          exactPath = resolvedValue;
          if (!sourcePsd) sourcePsd = baseName;
        }
      }
    }
  }

  if (!sourcePsd) {
    const candidate = parseSourcePsdFromText(allText);
    if (candidate) {
      // Free-text extraction may also yield a Windows UNC path — convert and validate.
      const unc = tryConvertWindowsUncPath(candidate);
      if (unc.isUnc && !unc.exists) {
        uncPathErrors.push({ field: "sourcePsd (text)", original: candidate, converted: unc.macPath });
      } else {
        sourcePsd = unc.macPath;
      }
    }
  }
  if (!pageId) {
    const guess = allText.match(/\bP\d{3}\b/i);
    pageId = guess ? guess[0].toUpperCase() : "";
  }

  // --- Chinese KV edit blocks: pairs of 图层名/内容修改成 ---
  const zhEdits = [];
  {
    let pendingLayer = "";
    for (const line of normalized) {
      const kv = line.match(KV_RE);
      if (!kv) { pendingLayer = ""; continue; }
      const rawKey = normalizeKvKey(kv[1]);
      const val = kv[2].trim();
      if (rawKey === "layername") {
        pendingLayer = val;
      } else if (rawKey === "newtext" && pendingLayer) {
        zhEdits.push({
          op: "replace_text",
          layerName: pendingLayer,
          newText: val,
          confidence: 0.97,
        });
        pendingLayer = "";
      } else {
        // Any other key breaks the pair context.
        if (rawKey !== "layername") pendingLayer = "";
      }
    }
  }

  // --- KV-based place_image blocks (English op: place_image format) ---
  const kvPlaceEdits = [];
  {
    let pendingPlace = null;
    for (const line of normalized) {
      const kv = line.match(KV_RE);
      if (!kv) continue;
      const rawKey = normalizeKvKey(kv[1]);
      const val = kv[2].trim();
      if (rawKey === "op" && /^place_image$/i.test(val)) {
        pendingPlace = { op: "place_image", imagePath: "", layerName: "", position: "top", visible: true, targetArtboard: "", confidence: 0.96 };
      } else if (pendingPlace) {
        if (rawKey === "imagepath") {
          pendingPlace.imagePath = val;
        } else if (rawKey === "layername" || rawKey === "layerlabel") {
          pendingPlace.layerName = val;
        } else if (rawKey === "position") {
          pendingPlace.position = val;
        } else if (rawKey === "visible") {
          pendingPlace.visible = !/^false$/i.test(val);
        } else if (rawKey === "targetartboard" || rawKey === "artboardname") {
          pendingPlace.targetArtboard = val;
        } else if (rawKey === "op") {
          if (pendingPlace.imagePath) kvPlaceEdits.push(pendingPlace);
          pendingPlace = /^place_image$/i.test(val)
            ? { op: "place_image", imagePath: "", layerName: "", position: "top", visible: true, targetArtboard: "", confidence: 0.96 }
            : null;
        }
      }
    }
    if (pendingPlace && pendingPlace.imagePath) kvPlaceEdits.push(pendingPlace);
  }

  // --- Step-based place_image: 第N步操作: 将X置入Y画板 ---
  const stepEdits = parseStepOps(normalized, filePaths);

  // --- Line-based edits (existing => format) ---
  const rawLines = lines.map((l) => String(l || "").replace(/[\s\uFEFF\xA0]+$/, ""));
  const lineEdits = parseEditsFromLines(rawLines);

  // Merge all edit sources, deduplicating place_image by imagePath+targetArtboard.
  const seenPlaceKeys = new Set([
    ...kvPlaceEdits.map((e) => `${e.imagePath}|${e.targetArtboard}`),
    ...stepEdits.map((e) => `${e.imagePath}|${e.targetArtboard}`),
  ]);
  const textOnlyEdits = [...lineEdits, ...parseEditsFromChinese(allText)].filter(
    (e) => !(e.op === "place_image" && seenPlaceKeys.has(`${e.imagePath}|${e.targetArtboard}`)),
  );

  // Priority: zh KV edits > line edits > chinese sentence edits; place ops merged separately.
  const mergedTextEdits = zhEdits.length > 0 ? zhEdits : textOnlyEdits;
  const allEdits = [...kvPlaceEdits, ...stepEdits, ...mergedTextEdits];

  const outputText = outputSpecLine || allText;
  const outputSpec = {
    format: "png",
    mode: /mode\s*=\s*single/i.test(outputText) ? "single" : "layer_sets",
    bundleZip: parseBoolean((outputText.match(/bundleZip\s*=\s*([A-Za-z0-9]+)/i) || [])[1], true),
    artboardName: artboardName || "",
  };

  // Final safety net: any UNC path that slipped through earlier parsing paths
  // (e.g. set directly without going through the KV loop) is caught here.
  if (sourcePsd) {
    const unc = tryConvertWindowsUncPath(sourcePsd);
    if (unc.isUnc && !unc.exists) {
      uncPathErrors.push({ field: "sourcePsd (final)", original: sourcePsd, converted: unc.macPath });
      sourcePsd = "";
    } else if (unc.isUnc && unc.exists) {
      sourcePsd = unc.macPath;
    }
  }
  if (exactPath) {
    const unc = tryConvertWindowsUncPath(exactPath);
    if (unc.isUnc && !unc.exists) {
      uncPathErrors.push({ field: "exactPath (final)", original: exactPath, converted: unc.macPath });
      exactPath = "";
    } else if (unc.isUnc && unc.exists) {
      exactPath = unc.macPath;
    }
  }

  // Full-text UNC scan: catch Windows paths that appear in free text or non-standard
  // KV labels (e.g. "PSD文件：\\server\share\banner.psd") where the label prefix would
  // prevent startsWith("\\") detection on the extracted sourcePsd value.
  // Only runs if no UNC errors have been found yet (to avoid duplicate entries).
  if (uncPathErrors.length === 0) {
    // Match \\server\... or //server/... patterns followed eventually by .psd/.psb
    const uncScanPattern = /\\\\[^\s\\][^\s]*?\.(?:psd|psb)|\/\/[^\s/][^\s]*?\.(?:psd|psb)/gi;
    for (const m of allText.matchAll(uncScanPattern)) {
      const candidate = m[0];
      const unc = tryConvertWindowsUncPath(candidate);
      if (unc.isUnc && !unc.exists) {
        uncPathErrors.push({ field: "text (scan)", original: candidate, converted: unc.macPath });
      } else if (unc.isUnc && unc.exists && !sourcePsd) {
        sourcePsd = path.basename(unc.macPath);
        exactPath = unc.macPath;
      }
    }
  }

  const pri = ["P0", "P1", "P2"].includes(priority) ? priority : "P1";
  return {
    pageId: pageId || "",
    sourcePsd: sourcePsd || "",
    exactPath: exactPath || "",
    edits: allEdits.map((item) => ({
      ...item,
      confidence: toConfidence(item.confidence, 0.9),
    })),
    outputSpec,
    priority: pri,
    note,
    uncPathErrors,
  };
}

// Detect a global-config slide (e.g. Slide 1 that declares output dir, constraints).
// Returns { isConfig, outputDir, dateFolder, copyPsdLocal } or null.
function parseGlobalConfig(lines) {
  const normalized = lines
    .map((line) => String(line || "").trim())
    .filter(Boolean)
    .map((line) => line.replace(/[：]/g, ":"));
  const allText = normalized.join("\n");

  const isConfig =
    /全局声明|硬性要求/.test(allText) ||
    /导出文件的储存位置/.test(allText);
  if (!isConfig) return null;

  let outputDir = "";
  let dateFolder = false;
  let copyPsdLocal = false;

  const KV_RE = /^([\w\u4e00-\u9fff][\w\u4e00-\u9fff ]*)\s*:\s*(.+)$/;
  for (const line of normalized) {
    const kv = line.match(KV_RE);
    if (!kv) continue;
    const rawKey = normalizeKvKey(kv[1]);
    const val = kv[2].trim();
    if (rawKey === "outputdir") outputDir = val;
  }
  if (!outputDir) {
    const freeText = allText.match(
      /(?:导出文件的储存位置|导出文件存储位置|导出储存位置|导出存储位置|导出目录|输出目录)\s*(?:是|为|到|至|:)\s*([^\n]+)/,
    );
    const candidateRaw = freeText?.[1]?.trim() || "";
    if (candidateRaw) {
      const quoted = candidateRaw.match(/["']([^"']+)["']/);
      outputDir = (quoted?.[1] || candidateRaw).replace(/[，。；;、]+$/g, "").trim();
    }
  }
  // Heuristics from free text.
  if (/新建文件夹以当日的?日期命名/.test(allText)) dateFolder = true;
  if (/拷贝到本地|复制到本地|copy.*local|copy-psd-local/i.test(allText)) copyPsdLocal = true;

  return { isConfig: true, outputDir, dateFolder, copyPsdLocal };
}

function runTesseractOcr(imagePath) {
  const result = spawnSync("tesseract", [imagePath, "stdout", "-l", "chi_sim+eng", "--psm", "6"], {
    encoding: "utf8",
    timeout: 20_000,
  });
  if (result.status === 0) return (result.stdout || "").trim();
  const fallback = spawnSync("tesseract", [imagePath, "stdout", "-l", "eng", "--psm", "6"], {
    encoding: "utf8",
    timeout: 20_000,
  });
  if (fallback.status === 0) return (fallback.stdout || "").trim();
  return "";
}

function runVisionOcr(imagePath) {
  const script = `
import Foundation
import Vision
if CommandLine.arguments.count < 2 { exit(0) }
let imagePath = CommandLine.arguments[1]
let url = URL(fileURLWithPath: imagePath)
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = true
request.recognitionLanguages = ["zh-Hans", "en-US"]
let handler = VNImageRequestHandler(url: url, options: [:])
do {
  try handler.perform([request])
  let lines = (request.results ?? []).compactMap { $0.topCandidates(1).first?.string }
  print(lines.joined(separator: "\\n"))
} catch {
  exit(0)
}
`;
  const result = spawnSync("swift", ["-", imagePath], {
    encoding: "utf8",
    timeout: 120_000,
    input: script,
  });
  if (result.status === 0) return (result.stdout || "").trim();
  return "";
}

function runOcr(imagePath) {
  const t = runTesseractOcr(imagePath);
  return t || runVisionOcr(imagePath);
}

// Convert a Windows UNC path (\\server\share\rest) to a macOS /Volumes path.
// Returns { macPath, isUnc, exists } where:
//   isUnc=false  → not a UNC path, macPath equals the original value
//   isUnc=true, exists=true  → converted and the file exists on disk
//   isUnc=true, exists=false → converted but not found (share not mounted or server unreachable)
function tryConvertWindowsUncPath(value) {
  const raw = String(value || "").trim();
  // Match \\server\share\... or //server/share/... patterns.
  if (!raw.startsWith("\\\\") && !(raw.startsWith("//") && !raw.startsWith("///"))) {
    return { macPath: raw, isUnc: false };
  }
  // Normalise all separators to forward slash and strip the leading //.
  const normalised = raw.replace(/\\/g, "/").replace(/^\/\//, "");
  const parts = normalised.split("/").filter(Boolean);
  // Minimum valid UNC: server + share (2 parts).
  if (parts.length < 2) {
    return { macPath: raw, isUnc: true, exists: false };
  }
  // macOS mounts the share under /Volumes/<share_name>; server name is irrelevant.
  const share = parts[1];
  const rest = parts.slice(2).join("/");
  const macPath = rest ? `/Volumes/${share}/${rest}` : `/Volumes/${share}`;
  const exists = fs.existsSync(macPath);
  return { macPath, isUnc: true, original: raw, exists };
}

function normalizeTargetMediaPath(target) {
  const raw = String(target || "");
  if (!raw) return "";
  if (raw.startsWith("../")) return `ppt/${raw.slice(3)}`;
  if (raw.startsWith("/")) return raw.slice(1);
  return `ppt/slides/${raw}`.replace("/slides/../", "/");
}

export async function parsePptRequest(input = {}) {
  const pptPath = path.resolve(expandHome(input.pptPath || ""));
  if (!pptPath || !fs.existsSync(pptPath)) {
    return {
      ok: false,
      code: "E_TASK_INVALID",
      message: "pptPath is required and must exist.",
    };
  }
  const fallbackPolicy =
    input.fallbackPolicy === "structured_only" ? "structured_only" : "structured_first_with_ocr";

  const raw = fs.readFileSync(pptPath);
  const zip = await JSZip.loadAsync(raw);
  const names = Object.keys(zip.files);
  const slides = names
    .filter((name) => /^ppt\/slides\/slide\d+\.xml$/.test(name))
    .sort((a, b) => Number(a.match(/\d+/)?.[0] || 0) - Number(b.match(/\d+/)?.[0] || 0));
  if (slides.length === 0) {
    return { ok: false, code: "E_PARSE_FAILED", message: "No slides found in pptx." };
  }

  const mediaTempDir = path.join(
    os.tmpdir(),
    "openclaw-ppt-task-orchestrator",
    `${Date.now()}-${Math.random().toString(16).slice(2)}`,
  );
  fs.mkdirSync(mediaTempDir, { recursive: true });

  const pages = [];
  const diagnostics = [];
  let globalConfig = null;

  for (let i = 0; i < slides.length; i += 1) {
    const slideIndex = i + 1;
    const slidePath = slides[i];
    const slideXml = await zip.file(slidePath).async("string");
    const textLines = extractSlideTextLines(slideXml);
    const relPath = `ppt/slides/_rels/slide${slideIndex}.xml.rels`;
    const relXml = zip.file(relPath) ? await zip.file(relPath).async("string") : "";
    const relMap = parseRelationshipTargets(relXml);
    const imageTargets = parseSlideImageTargets(slideXml, relMap)
      .map(normalizeTargetMediaPath)
      .filter(Boolean);

    const localImages = [];
    for (const target of imageTargets) {
      const file = zip.file(target);
      if (!file) continue;
      const fileName = `${slideIndex}-${path.basename(target)}`;
      const filePath = path.join(mediaTempDir, fileName);
      fs.writeFileSync(filePath, await file.async("nodebuffer"));
      localImages.push(filePath);
    }
    const screenshotPath = localImages[0] || "";

    // Detect and extract global config slide (e.g. "本ppt全局声明").
    const maybeConfig = parseGlobalConfig(textLines);
    if (maybeConfig) {
      globalConfig = maybeConfig;
      diagnostics.push({
        slideIndex,
        pageId: `GLOBAL_CONFIG`,
        parseMode: "global_config",
        code: "OK",
        message: "Global config slide detected; skipping as task page.",
      });
      continue; // Not a task page.
    }

    const structured = parseStructuredFields(textLines);

    // Surface Windows UNC path errors immediately — no point continuing with an
    // unresolvable path.  The converted /Volumes path is included in the message
    // so users know exactly what macOS path to mount.
    if (structured.uncPathErrors && structured.uncPathErrors.length > 0) {
      for (const ue of structured.uncPathErrors) {
        const hint = `请在访达中连接服务器（smb://${ue.original.replace(/\\\\/g, "").replace(/\\/g, "/").split("/")[0]}），挂载后对应路径为 ${ue.converted}`;
        diagnostics.push({
          slideIndex,
          pageId: structured.pageId || `P${String(slideIndex).padStart(3, "0")}`,
          parseMode: "structured",
          code: "E_WINDOWS_UNC_PATH",
          message: `Windows 网络路径无法访问（${ue.field}）：${ue.original} → 转换后路径 ${ue.converted} 不存在。${hint}`,
        });
      }
      // Skip this page — cannot execute without a valid PSD path.
      continue;
    }

    let parseMode = "structured";
    let confidence = 0.97;
    let page = {
      slideIndex,
      pageId: structured.pageId || `P${String(slideIndex).padStart(3, "0")}`,
      sourcePsd: structured.sourcePsd,
      exactPath: structured.exactPath || (structured.sourcePsd?.startsWith("/") ? structured.sourcePsd : ""),
      edits: structured.edits,
      outputSpec: structured.outputSpec,
      priority: structured.priority,
      note: structured.note,
      parseMode,
      confidence,
      screenshotPath,
    };

    const missingStructured =
      !page.sourcePsd || !Array.isArray(page.edits) || page.edits.length === 0;
    if (missingStructured && fallbackPolicy === "structured_first_with_ocr" && screenshotPath) {
      const ocrText = runOcr(screenshotPath);
      const ocrLines = String(ocrText)
        .split(/\r?\n/)
        .map((line) => line.trim())
        .filter(Boolean);
      const ocrFields = parseStructuredFields(ocrLines);
      if ((ocrFields.sourcePsd || ocrFields.edits.length > 0) && ocrLines.length > 0) {
        parseMode = "ocr_fallback";
        confidence = 0.78;
        page = {
          ...page,
          sourcePsd: ocrFields.sourcePsd || page.sourcePsd,
          exactPath: ocrFields.exactPath || page.exactPath ||
            ((ocrFields.sourcePsd || page.sourcePsd || "").startsWith("/")
              ? ocrFields.sourcePsd || page.sourcePsd
              : ""),
          edits: ocrFields.edits.length > 0 ? ocrFields.edits : page.edits,
          outputSpec: ocrFields.outputSpec || page.outputSpec,
          priority: ocrFields.priority || page.priority,
          parseMode,
          confidence,
        };
      }
    }

    const valid = Boolean(page.sourcePsd) && Array.isArray(page.edits) && page.edits.length > 0;
    if (!valid) {
      diagnostics.push({
        slideIndex,
        pageId: page.pageId,
        parseMode: page.parseMode,
        code: "E_PARSE_FAILED",
        message: "Missing sourcePsd or edits.",
      });
    }

    pages.push(page);
  }

  if (pages.length === 0) {
    const hasUnc = diagnostics.some((d) => d.code === "E_WINDOWS_UNC_PATH");
    return {
      ok: false,
      code: hasUnc ? "E_WINDOWS_UNC_PATH" : "E_PARSE_FAILED",
      message: hasUnc
        ? "PPT 中包含 Windows 网络路径，无法在 macOS 上访问。请先在访达中挂载对应的共享盘。"
        : "No page task was parsed from pptx.",
      globalConfig,
      diagnostics,
    };
  }

  // Cross-slide PSD propagation: if a slide declares no sourcePsd/exactPath, carry
  // forward the last known PSD path from a preceding slide (common PPT pattern where
  // Slide 2 declares the asset paths and Slides 3-N just list edits for that same PSD).
  let lastKnownExactPath = "";
  let lastKnownSourcePsd = "";
  for (const page of pages) {
    if (page.exactPath || page.sourcePsd) {
      lastKnownExactPath = page.exactPath || lastKnownExactPath;
      lastKnownSourcePsd = page.sourcePsd || lastKnownSourcePsd;
    } else if (lastKnownSourcePsd || lastKnownExactPath) {
      page.exactPath = lastKnownExactPath;
      page.sourcePsd = lastKnownSourcePsd;
    }
  }

  return {
    ok: true,
    pptPath,
    pages,
    globalConfig,
    diagnostics,
    mediaTempDir,
  };
}

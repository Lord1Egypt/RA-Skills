#!/usr/bin/env node
/**
 * present.mjs — the mechanical half of the `present` skill.
 *
 * Everything here is the same on macOS, Linux and Windows because it is Node,
 * not shell: no curl quoting, no jq, no PowerShell/POSIX branch. Run it with
 * `node` (>=18, for global fetch) or `bun`.
 *
 *   node present.mjs doctor
 *   node present.mjs login   [--profile NAME]
 *   node present.mjs plan    --html index.html
 *   node present.mjs publish --html index.html --voice kokoro:af_heart
 *
 * `publish` implements the update loop the whole feature exists for:
 *
 *   1. POST /api/presentations/publish-narrated with NO audio. The response's
 *      `staleSlides` names exactly the narrated slides whose text changed;
 *      every other slide's audio carries forward untouched. (A first publish
 *      has nothing to carry, so the server answers 400 NO_AUDIO — that is not
 *      a failure, it means "all of them".)
 *   2. Synthesize ONLY those slides with `bisque-voice`.
 *   3. POST again with just that audio, PUT each MP3 to its returned upload
 *      URL, POST the returned `completeUrl` with the returned `files`.
 *
 * So editing one slide of a twelve-slide presentation costs one slide of
 * synthesis, not twelve.
 *
 * The narration extractor below mirrors Bisque's server-side HTML presentation
 * parser character for character (tags dropped without inserting a space,
 * entities decoded once, `<<marker>>` runs replaced with a word break only when
 * they split a word). It has to: the server rejects a publish whose word-timing
 * count differs from its own whitespace-token count of the same narration,
 * because cue markers index that array by position.
 */

import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const BASE = (process.env.BISQUE_BASE_URL || "https://bisque.cloud").replace(
  /\/+$/,
  "",
);

// ─── narration extraction (mirror of the server's HTML presentation parser) ─

const SENTINEL = "\u0000";

function findMatchingSectionEnd(region, start) {
  let depth = 0;
  let i = start;
  while (i < region.length) {
    if (region[i] === "<") {
      if (region.startsWith("<section", i)) {
        depth += 1;
        i += "<section".length;
        continue;
      }
      if (region.startsWith("</section>", i)) {
        depth -= 1;
        const after = i + "</section>".length;
        if (depth === 0) return after;
        i = after;
        continue;
      }
    }
    i += 1;
  }
  return region.length;
}

function extractSections(html) {
  const regionStart = html.indexOf('<div class="slides">');
  const region = regionStart === -1 ? html : html.slice(regionStart);
  const sections = [];
  let cursor = 0;
  while (cursor < region.length) {
    const openIdx = region.indexOf("<section", cursor);
    if (openIdx === -1) break;
    const endIdx = findMatchingSectionEnd(region, openIdx);
    sections.push(region.slice(openIdx, endIdx));
    cursor = endIdx;
  }
  return sections;
}

/** `<<…>>` → sentinel. Scanned BEFORE entity decode, so `&lt;&lt;x&gt;&gt;`
 *  is prose, exactly as the server sees it. */
function scanMarkers(raw) {
  let out = "";
  let i = 0;
  while (i < raw.length) {
    if (raw[i] === "<" && raw[i + 1] === "<") {
      const close = raw.indexOf(">>", i + 2);
      if (close !== -1) {
        out += SENTINEL;
        i = close + 2;
        continue;
      }
    }
    const cp = raw.codePointAt(i);
    if (cp === undefined) break;
    const ch = String.fromCodePoint(cp);
    out += ch;
    i += ch.length;
  }
  return out;
}

/** Tags that end a run of text, so `a<br>b` is two words rather than "ab".
 *  MUST stay identical to TEXT_BOUNDARY_TAGS in
 *  packages/presentation-format/src/html-build.ts: the server counts words the
 *  same way, and a disagreement gets the publish rejected. Inline tags are
 *  deliberately absent so `<em>word</em>s` stays one word. */
const TEXT_BOUNDARY_TAGS = new Set([
  "br",
  "hr",
  "p",
  "div",
  "section",
  "article",
  "aside",
  "header",
  "footer",
  "main",
  "nav",
  "figure",
  "figcaption",
  "blockquote",
  "pre",
  "h1",
  "h2",
  "h3",
  "h4",
  "h5",
  "h6",
  "ul",
  "ol",
  "li",
  "dl",
  "dt",
  "dd",
  "table",
  "thead",
  "tbody",
  "tfoot",
  "tr",
  "td",
  "th",
  "caption",
]);

function isTextBoundaryTag(tagBody) {
  const m = tagBody.match(/^\/?\s*([a-zA-Z][a-zA-Z0-9]*)/);
  return m !== null && TEXT_BOUNDARY_TAGS.has(m[1].toLowerCase());
}

function stripTags(input) {
  let out = "";
  let inTag = false;
  let tagBody = "";
  for (const ch of input) {
    if (ch === "<") {
      inTag = true;
      tagBody = "";
    } else if (ch === ">") {
      inTag = false;
      if (isTextBoundaryTag(tagBody)) out += " ";
    } else if (inTag) {
      tagBody += ch;
    } else {
      out += ch;
    }
  }
  return out;
}

/** Narration is authored inside indented HTML, so the raw text carries
 *  newlines and long indent runs, and a removed cue marker leaves its
 *  surrounding spaces behind. Speech engines read those as pauses, which is
 *  heard as halting narration. Collapsing cannot change the word count, so
 *  client and server stay in agreement. */
function collapseWhitespace(input) {
  return input.replace(/\s+/g, " ").trim();
}

function decodeEntities(s) {
  return s
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

/** A sentinel inside a word splits it; between words it contributes nothing. */
function dropSentinels(input) {
  let out = "";
  let inWord = false;
  for (const ch of input) {
    if (ch === SENTINEL) {
      if (inWord) {
        out += " ";
        inWord = false;
      }
      continue;
    }
    if (/\s/.test(ch)) {
      inWord = false;
      out += ch;
    } else {
      inWord = true;
      out += ch;
    }
  }
  return out;
}

/** The inside of a slide's `<aside class="notes">`, exactly as authored —
 *  tags, entities and cue markers all still in it. `null` when the slide has
 *  no notes. */
function rawNotesOf(section) {
  const open = '<aside class="notes">';
  const openIdx = section.indexOf(open);
  if (openIdx === -1) return null;
  const afterOpen = openIdx + open.length;
  const closeOffset = section.indexOf("</aside>", afterOpen);
  if (closeOffset === -1) return null;
  return section.slice(afterOpen, closeOffset);
}

function narrationOf(section) {
  const raw = rawNotesOf(section);
  if (raw === null) return "";
  const trimmed = decodeEntities(stripTags(scanMarkers(raw))).trim();
  if (trimmed === "") return "";
  return collapseWhitespace(dropSentinels(trimmed));
}

function slideKeyFor(i) {
  return `slide-${String(i).padStart(2, "0")}`;
}

/** Every narrated slide, in document order. A slide with no `<aside
 *  class="notes">` (or notes that are only cue markers) has no audio and is
 *  absent here — the same rule the server applies when it builds the plan. */
export function narrationPlan(html) {
  return extractSections(html)
    .map((section, i) => ({
      slideIndex: i,
      slideKey: slideKeyFor(i),
      text: narrationOf(section),
    }))
    .filter((s) => s.text !== "")
    .map((s) => ({
      ...s,
      // Count DISPLAY words. A pronunciation override is one word to a reader
      // and to the timings bisque-voice reports, but `[Qwen3](Qwen three)` is
      // two whitespace tokens raw — counting those rejects a valid publish
      // with a word-timing mismatch. Same rule as `stripPronunciation` in
      // packages/presentation-format; see docs/bisque-voice-pronunciation.md.
      wordCount: stripPronunciation(s.text).split(/\s+/).filter(Boolean).length,
    }));
}

/**
 * Replace every `[display](spoken)` override with the word a reader sees.
 *
 * Deliberately mirrors `parse_override` in apps/bisque-voice/src/pronounce.rs
 * and `parsePronunciation` in packages/presentation-format: anything that does
 * not parse cleanly stays literal, so prose holding a bracket is never eaten,
 * and a body of empty slashes is an unfinished override rather than a marker.
 */
function stripPronunciation(text) {
  let out = "";
  let at = 0;
  let i = 0;
  while (i < text.length) {
    const open = text.indexOf("[", i);
    if (open === -1) break;
    const close = text.indexOf("]", open + 1);
    if (close === -1) break;
    if (text[close + 1] !== "(") {
      i = open + 1;
      continue;
    }
    const end = text.indexOf(")", close + 2);
    if (end === -1) break;
    const display = text.slice(open + 1, close);
    const body = text.slice(close + 2, end);
    const isIpa =
      body.startsWith("/") && body.endsWith("/") && body.length >= 2;
    const inner = isIpa ? body.slice(1, -1) : body;
    if (
      display.trim() === "" ||
      inner.trim() === "" ||
      display.includes("[") ||
      display.includes("\n") ||
      body.includes("\n")
    ) {
      i = open + 1;
      continue;
    }
    out += text.slice(at, open) + display;
    at = end + 1;
    i = end + 1;
  }
  return out + text.slice(at);
}

/**
 * A cue marker whose `<<` or `>>` is HTML-escaped, anywhere in a slide's
 * notes.
 *
 * `scanMarkers` above matches the literal `<<…>>` form only, so an escaped
 * marker is neither stripped from the narration nor fired as a cue: the voice
 * reads "reveal target s2a" out loud and nothing on the slide moves. One
 * published presentation carried 13 of them and spent 20 seconds of its 88
 * saying them.
 *
 * The test is the marker grammar from the authoring spec — `<<command args>>`
 * with both delimiters literal — rather than a list of command names, so
 * `reveal`, `fire`, `set` and any command the spec adds later are all covered.
 * Only the notes are scanned: a slide that puts marker syntax on screen writes
 * it escaped on purpose, and that is correct.
 */
const CUE_MARKER_IN_NOTES =
  /(&lt;&lt;|<<)(\s*[a-zA-Z][\w-]*[\s\S]*?)(&gt;&gt;|>>)/g;

function escapedCueMarkers(rawNotes) {
  const found = [];
  for (const m of rawNotes.matchAll(CUE_MARKER_IN_NOTES)) {
    if (m[1] === "<<" && m[3] === ">>") continue;
    const body = m[2].length > 60 ? `${m[2].slice(0, 60)}…` : m[2];
    found.push({ escaped: `${m[1]}${body}${m[3]}`, fixed: `<<${body}>>` });
  }
  return found;
}

/**
 * Everything an author can see before spending a minute of synthesis: a
 * pronunciation marker that did not parse (its leftover `](` is spoken and
 * captioned), a `data-*-spec` whose JSON does not parse (the player renders it
 * as empty space), and an HTML-escaped cue marker (spoken aloud, and its
 * reveal never fires). The first two mirror `validatePronunciationMarkers` /
 * `validateSpecJson` in packages/presentation-format, which the server rejects
 * a publish on; the escaped marker is caught here only, because the server
 * accepts it as prose. `plan` prints these and `publish` refuses to start on
 * them.
 */
export function lintPresentation(html) {
  const problems = [];
  extractSections(html).forEach((section, i) => {
    const id = sectionAttr(section, "id") ?? slideKeyFor(i);
    const where = `slide ${i + 1} (#${id})`;

    for (const marker of escapedCueMarkers(rawNotesOf(section) ?? "")) {
      problems.push(
        `${where}: this cue marker is HTML-escaped — \`${marker.escaped}\`. ` +
          `Write it literally: \`${marker.fixed}\`. ` +
          "An escaped marker is read aloud by the voice and never fires.",
      );
    }

    const text = narrationOf(section);
    const shown = stripPronunciation(text);
    const at = shown.indexOf("](");
    if (at !== -1) {
      let start = at;
      while (start > 0 && !/\s/.test(shown[start - 1]) && at - start < 40)
        start--;
      let end = at + 2;
      while (end < shown.length && !/\s/.test(shown[end]) && end - at < 40)
        end++;
      problems.push(
        `${where}: pronunciation marker did not parse — \`${shown.slice(start, end)}\`. ` +
          "One marker per word, never nested: `[Changelog's](/…/)`.",
      );
    }

    const specs = /\sdata-([a-z]+(?:-[a-z]+)*-spec)=(["'])/g;
    for (;;) {
      const m = specs.exec(section);
      if (m === null) break;
      const quoteEnd = section.indexOf(m[2], m.index + m[0].length);
      if (quoteEnd === -1) break;
      const value = decodeEntities(
        section.slice(m.index + m[0].length, quoteEnd),
      );
      specs.lastIndex = quoteEnd + 1;
      try {
        JSON.parse(value);
      } catch (error) {
        const tail = value.length > 60 ? `…${value.slice(-60)}` : value;
        problems.push(
          `${where}: data-${m[1]} is not valid JSON — ${error.message} — ends \`${tail}\`.`,
        );
      }
    }
    const background = sectionAttr(section, "data-background")?.trim();
    if (background?.startsWith("dither:")) {
      const body = background.slice("dither:".length).trim();
      if (body.startsWith("{")) {
        try {
          JSON.parse(body);
        } catch (error) {
          problems.push(
            `${where}: data-background dither spec is not valid JSON — ${error.message}.`,
          );
        }
      }
    }
  });
  return problems;
}

function sectionAttr(section, name) {
  const openEnd = section.indexOf(">");
  if (openEnd === -1) return undefined;
  const tag = section.slice(0, openEnd);
  const pos = tag.indexOf(`${name}=`);
  if (pos === -1) return undefined;
  const after = tag.slice(pos + name.length + 1);
  if (after.startsWith('"')) return after.slice(1).split('"')[0];
  if (after.startsWith("'")) return after.slice(1).split("'")[0];
  const m = after.match(/\S+/);
  return m === null ? undefined : m[0];
}

// ─── bisque-voice ──────────────────────────────────────────────────────────

/**
 * Absolute paths only. `~/.bisque/bin` is usually NOT on PATH, so probing with
 * `command -v` / `where` reports "missing" on a machine where it is installed —
 * and a false "missing" here is the difference between narrating locally and
 * not narrating at all.
 */
export function findTts() {
  const override = process.env.BISQUE_VOICE_BIN;
  if (override) return fs.existsSync(override) ? override : null;
  const home = os.homedir();
  const p =
    process.platform === "win32"
      ? path.join(home, ".bisque", "bin", "bisque-voice.exe")
      : path.join(home, ".bisque", "bin", "bisque-voice");
  return fs.existsSync(p) ? p : null;
}

function requireTts() {
  const bin = findTts();
  if (bin) return bin;
  fail(
    "bisque-voice is not installed (looked for " +
      (process.platform === "win32"
        ? "%USERPROFILE%\\.bisque\\bin\\bisque-voice.exe"
        : "~/.bisque/bin/bisque-voice") +
      ").\n" +
      "Install it, then re-run:\n" +
      (process.platform === "win32"
        ? "  irm https://download.bisque.today/bisque-voice/install.ps1 | iex"
        : "  curl -fsSL https://download.bisque.today/bisque-voice/install.sh | sh"),
  );
}

function runTts(bin, args, { input } = {}) {
  const res = spawnSync(bin, args, {
    input,
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
    // stderr is progress + errors; let it stream so a model download is visible.
    stdio: ["pipe", "pipe", "inherit"],
  });
  if (res.error) fail(`could not run ${bin}: ${res.error.message}`);
  if (res.status !== 0) fail(`bisque-voice exited ${res.status}`);
  return res.stdout;
}

/** Like runTts, but a failure is a return value, not a process exit — the
 *  doctor smoke test reports problems instead of dying of them. stderr is
 *  captured (not streamed) so a clean doctor run stays clean. */
function runTtsTry(bin, args, { input, timeoutMs } = {}) {
  const res = spawnSync(bin, args, {
    input,
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
    stdio: ["pipe", "pipe", "pipe"],
    ...(timeoutMs ? { timeout: timeoutMs } : {}),
  });
  if (res.error) {
    const detail =
      res.error.code === "ETIMEDOUT"
        ? `timed out after ${Math.round((timeoutMs ?? 0) / 1000)}s`
        : res.error.message;
    return { ok: false, detail, stderr: res.stderr ?? "" };
  }
  if (res.status !== 0) {
    return {
      ok: false,
      detail: `bisque-voice exited ${res.status}`,
      stderr: res.stderr ?? "",
    };
  }
  return { ok: true, stdout: res.stdout, stderr: res.stderr ?? "" };
}

function ttsJson(bin, args) {
  return JSON.parse(runTts(bin, args));
}

function formatBytes(n) {
  if (!Number.isFinite(n) || n <= 0) return "size unknown";
  const gb = n / 2 ** 30;
  if (gb >= 1) return `${gb.toFixed(1)} GB`;
  return `${Math.max(1, Math.round(n / 2 ** 20))} MB`;
}

/** The engine a publish will synthesize with, when one is nameable: an
 *  explicit/settings `--engine`, else the `engine:` qualifier on the voice. */
function engineFor(flags) {
  if (typeof flags.engine === "string" && flags.engine) return flags.engine;
  if (typeof flags.voice === "string" && flags.voice.includes(":")) {
    return flags.voice.split(":")[0];
  }
  return null;
}

/** The two Studio engine families, asked about by predicate instead of by a
 *  regex retyped at each call site — the drift between two such copies is what
 *  let a named-Studio engine skip its own install. `qwen3-clone-*` narrates in
 *  a voice cloned on THIS machine; `qwen3-voices-*` narrates in one of the nine
 *  speakers shipped inside the pack. Both are large on-demand downloads and
 *  both want a forced aligner, so "is this Studio?" has exactly one answer. */
export function isCloneEngine(engineId) {
  return typeof engineId === "string" && /^qwen3-clone-/.test(engineId);
}
export function isNamedStudioEngine(engineId) {
  return typeof engineId === "string" && /^qwen3-voices-/.test(engineId);
}
export function isStudioEngine(engineId) {
  return isCloneEngine(engineId) || isNamedStudioEngine(engineId);
}

/**
 * The account's engine pick may name a Studio engine (qwen3-clone-* to clone
 * the account's own voice, qwen3-voices-* for one of the nine named speakers)
 * that this machine has never installed — the welcome flow saves the pick, the
 * terminal does the download. Say plainly what will be downloaded and how
 * large, then install it via bisque-voice, so synthesis below just works.
 * Non-Studio engines keep today's behavior (their absence still fails with
 * bisque-voice's own error), and an engine bisque-voice does not know is left
 * for synthesis to report.
 */
function ensureStudioEngineInstalled(bin, flags) {
  const engineId = engineFor(flags);
  if (!isStudioEngine(engineId)) return;
  let engines;
  try {
    engines = ttsJson(bin, ["engines", "--json"]);
  } catch {
    return; // engines list unavailable — let synthesis surface the real error
  }
  const spec = engines.find((s) => s.id === engineId);
  if (!spec) {
    say(
      `note: this bisque-voice does not list engine ${engineId} — it may be ` +
        `out of date. If synthesis fails, update bisque-voice first.`,
    );
    return;
  }
  if (spec.installed) return;
  say(
    `The voice engine set on this account (${engineId}) is not on this ` +
      `machine yet. Downloading it now — a one-time ` +
      `${formatBytes(spec.downloadBytes)} download:`,
  );
  say(`  bisque-voice install ${engineId}`);
  const res = spawnSync(bin, ["install", engineId], { stdio: "inherit" });
  if (res.error) {
    fail(`could not run bisque-voice install: ${res.error.message}`);
  }
  if (res.status !== 0) {
    fail(`bisque-voice install ${engineId} exited ${res.status}`);
  }
}

/**
 * COMPATIBILITY BRIDGE. From bisque-voice 0.1.10, `install <studio-engine>`
 * resolves the engine's companion aligner itself (`companionAligner` in
 * `engines --json`) — the aligner requirement is the engine's contract, not
 * this script's knowledge. This covers a machine whose Studio engine predates
 * that, which would otherwise never acquire the companion, since `install` is
 * not run again. Every failure path degrades to a warning rather than blocking
 * the publish: an older bisque-voice still narrates, with the sync caveat
 * stated rather than hidden.
 */
function ensureAlignerInstalled(bin, flags) {
  const engineId = engineFor(flags);
  if (!isStudioEngine(engineId)) return;
  if (flags.align === "none") return; // explicit opt-out
  let aligners;
  try {
    aligners = ttsJson(bin, ["aligners", "--json"]);
  } catch {
    say(
      "note: this bisque-voice has no aligner support — narration sync may " +
        "drift on Studio engines. Update it: " +
        "curl -fsSL https://download.bisque.today/bisque-voice/install.sh | sh",
    );
    return;
  }
  if (aligners.some((a) => a.installed)) return;
  const spec =
    aligners.find((a) => a.id === "qwen3-q4" && !a.unsupported) ??
    aligners.find((a) => !a.unsupported);
  if (!spec) return; // no aligner can run in this build (Intel mac) — engine timings it is
  say(
    `Studio narration needs a forced aligner to keep slides in sync with ` +
      `the voice. Downloading ${spec.id} — a one-time ` +
      `${formatBytes(spec.downloadBytes)} download:`,
  );
  say(`  bisque-voice install ${spec.id}`);
  const res = spawnSync(bin, ["install", spec.id], { stdio: "inherit" });
  if (res.error || res.status !== 0) {
    say(
      `note: aligner install failed — continuing with the engine's own ` +
        `timings, which can drift out of sync. Update bisque-voice and retry.`,
    );
  }
}

/**
 * LEGACY clone-provenance state, for bisque-voice older than 0.1.10 only.
 * Newer binaries store provenance in the voice manifest itself (`clone
 * --source-id`, surfaced by `list --json` as `sourceId`) — the manifest is
 * the single source of truth and this file is not written when the binary
 * supports that. Best-effort on both ends: an unreadable file means
 * "unknown", which re-clones — the safe direction.
 */
const CLONE_STATE_PATH = path.join(
  os.homedir(),
  ".bisque",
  "voice-clone-state.json",
);

function readCloneState() {
  try {
    return JSON.parse(fs.readFileSync(CLONE_STATE_PATH, "utf8"));
  } catch {
    return {};
  }
}

function writeCloneState(engineId, uploadedAt) {
  try {
    fs.writeFileSync(
      CLONE_STATE_PATH,
      JSON.stringify({ ...readCloneState(), [engineId]: uploadedAt }, null, 2),
    );
  } catch {
    /* unwritable — next publish just re-clones, which is harmless */
  }
}

/** Does this bisque-voice support `clone --source-id` (0.1.10+)? */
function cloneSupportsSourceId(bin) {
  const help = runTtsTry(bin, ["clone", "--help"], { timeoutMs: 15_000 });
  return help.ok && help.stdout.includes("--source-id");
}

/**
 * A `qwen3-clone-*` engine narrates in a voice cloned from the account's
 * reference recording (made in the browser on bisque.cloud/welcome). The
 * clone itself is local and one-time: if this machine already has a
 * CURRENT clone of that recording, use it; otherwise — first run, or the
 * account recording changed since (`/account` re-record) — fetch the
 * recording + its passage and run `bisque-voice clone` here. The
 * recording never needs to be made twice — a new machine, or the other
 * engine size, just re-clones from the same clip. Voice latents stay on
 * this machine.
 */
async function ensureCloneVoiceReady(bin, flags, auth, me) {
  const engineId = engineFor(flags);
  if (!isCloneEngine(engineId)) return;

  // An explicit engine-qualified --voice names its clone directly; a wrong
  // name gets bisque-voice's own error, which lists what exists.
  if (typeof flags.voice === "string" && flags.voice.includes(":")) return;

  const accountUploadedAt =
    typeof me?.settings?.voiceClone?.uploadedAt === "string"
      ? me.settings.voiceClone.uploadedAt
      : null;

  let existing = null;
  const listed = runTtsTry(bin, ["list", "--json"], { timeoutMs: 30_000 });
  if (listed.ok) {
    try {
      const clones = JSON.parse(listed.stdout).filter(
        (v) => v.engine === engineId,
      );
      // "me" is the clone this script manages from the account recording;
      // any other name was cloned by hand and is deliberate — respect it.
      existing = clones.find((v) => v.name === "me") ?? clones[0] ?? null;
    } catch {
      /* unparsable — treat as no clones and try the account */
    }
  }
  if (existing && existing.name !== "me") {
    flags.voice = `${engineId}:${existing.name}`;
    say(`voice: ${flags.voice} (cloned by hand on this machine)`);
    return;
  }
  if (existing) {
    // Provenance lives in the voice manifest when the binary supports it
    // (`sourceId` on `list --json`); the local state file is only the
    // fallback for older binaries and for voices cloned before 0.1.10.
    const clonedFrom =
      typeof existing.sourceId === "string"
        ? existing.sourceId
        : readCloneState()[engineId];
    const current =
      accountUploadedAt === null || clonedFrom === accountUploadedAt;
    if (current) {
      flags.voice = `${engineId}:me`;
      say(`voice: ${flags.voice} (cloned on this machine)`);
      return;
    }
    say(
      "Your account has a newer voice recording than the clone on this " +
        "machine — re-cloning from it…",
    );
  } else {
    say(
      `No ${engineId} voice is cloned on this machine yet — fetching the ` +
        `recording from your account…`,
    );
  }
  let ref;
  try {
    ref = await api("/api/voice-clone-reference", { method: "GET", auth });
  } catch (error) {
    if (error instanceof ApiError && error.code === "NO_VOICE_CLONE") {
      fail(
        "This account picked its own cloned voice, but has no reference " +
          "recording yet.\nRecord one at https://bisque.cloud/welcome " +
          "(Voice step → Clone my voice), then re-run this command.",
      );
    }
    throw error;
  }
  if (typeof ref?.wavBase64 !== "string" || typeof ref?.passage !== "string") {
    fail(
      "The account's voice-clone recording came back malformed — re-record it at https://bisque.cloud/welcome.",
    );
  }

  const sourceId =
    typeof ref.uploadedAt === "string" ? ref.uploadedAt : accountUploadedAt;
  const manifestProvenance = sourceId !== null && cloneSupportsSourceId(bin);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "bisque-clone-"));
  try {
    const wavPath = path.join(tmp, "reference.wav");
    const passagePath = path.join(tmp, "passage.txt");
    fs.writeFileSync(wavPath, Buffer.from(ref.wavBase64, "base64"));
    fs.writeFileSync(passagePath, ref.passage);
    say(`Cloning your voice into ${engineId} — one-time, a few seconds:`);
    say(`  bisque-voice clone --engine ${engineId} --name me`);
    const args = [
      "clone",
      "--engine",
      engineId,
      "--name",
      "me",
      "--reference",
      wavPath,
      "--transcript-file",
      passagePath,
    ];
    if (manifestProvenance) args.push("--source-id", sourceId);
    const res = spawnSync(bin, args, { stdio: "inherit" });
    if (res.error)
      fail(`could not run bisque-voice clone: ${res.error.message}`);
    if (res.status !== 0) fail(`bisque-voice clone exited ${res.status}`);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
  // Older binaries can't record provenance in the manifest — keep it here.
  if (!manifestProvenance && sourceId !== null) {
    writeCloneState(engineId, sourceId);
  }
  flags.voice = `${engineId}:me`;
  say(`voice: ${flags.voice} (cloned from your account's recording)`);
}

// ─── credentials ─────────────────────────────────────────────────────────

const CONFIG_PATH = path.join(os.homedir(), ".bisque", "config.json");

function readConfig() {
  try {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, "utf8"));
  } catch {
    return null;
  }
}

/**
 * Report whether `~/.bisque/config.json` is readable by anyone but its owner.
 * Windows ACLs are not POSIX bits and `mode` there says nothing useful, so
 * this checks only where the answer means something.
 */
function reportConfigPermissions() {
  if (process.platform === "win32") return;
  let mode;
  try {
    mode = fs.statSync(CONFIG_PATH).mode & 0o777;
  } catch {
    return; // no config file — nothing is exposed
  }
  if ((mode & 0o077) === 0) {
    say(`config     : ${CONFIG_PATH} (0${mode.toString(8)}, owner-only)`);
    return;
  }
  say(
    `config     : ${CONFIG_PATH} is 0${mode.toString(8)} — it holds an API key\n` +
      `             and every account on this machine can read it. Fix:\n` +
      `             chmod 600 ${CONFIG_PATH}`,
  );
}

/** `.bisque.json` — the committed, per-repo pin of which account this
 *  directory speaks for. Walked up from `from`, exactly as the `bisque` CLI
 *  does, so both tools agree about whose presentation this is. */
function pinnedProfile(from) {
  let dir = path.resolve(from);
  for (;;) {
    try {
      const pinned = JSON.parse(
        fs.readFileSync(path.join(dir, ".bisque.json"), "utf8"),
      );
      if (typeof pinned.profile === "string" && pinned.profile)
        return pinned.profile;
    } catch {
      /* absent or unreadable — keep walking */
    }
    const parent = path.dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}

/** `.bisque.json` may also pin the ORGANIZATION this directory publishes
 *  into (`{"org": "acme"}`): every publish from the repo then goes to the
 *  company's library on bisque.team instead of a personal channel. Same
 *  upward walk as the profile pin. `--org` overrides; `--org ""` clears. */
function pinnedOrg(from) {
  let dir = path.resolve(from);
  for (;;) {
    try {
      const pinned = JSON.parse(
        fs.readFileSync(path.join(dir, ".bisque.json"), "utf8"),
      );
      if (typeof pinned.org === "string" && pinned.org) return pinned.org;
    } catch {
      /* absent or unreadable — keep walking */
    }
    const parent = path.dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}

/**
 * env → `--profile` → `.bisque.json` → `present` → `default` → the only one.
 *
 * It refuses to guess between several accounts: publishing someone's briefing
 * to the wrong account is silent and not obviously undoable. Credentials come
 * from the environment and `~/.bisque/config.json` only; `login` below always
 * writes that file, so there is exactly one place to look when resolution
 * surprises someone.
 */
export function resolveAuth({ profile, cwd = process.cwd() } = {}) {
  const envKey = process.env.BISQUE_API_KEY;
  const envUser = process.env.BISQUE_USER_ID;
  if (envKey && envUser) {
    return { apiKey: envKey, userId: envUser, from: "environment" };
  }
  const profiles = readConfig()?.profiles ?? {};
  const usable = Object.entries(profiles)
    .filter(([, p]) => p?.apiKey && p?.userId)
    .map(([name]) => name);
  const asked = profile ?? process.env.BISQUE_PROFILE ?? pinnedProfile(cwd);
  const pick = (name, why) =>
    usable.includes(name)
      ? {
          apiKey: profiles[name].apiKey,
          userId: profiles[name].userId,
          from: why,
        }
      : null;

  if (asked) {
    const chosen = pick(asked, `profile ${asked}`);
    if (chosen) return chosen;
    return {
      error: `Profile ${JSON.stringify(asked)} has no stored credentials. Available: ${usable.join(", ") || "(none)"}.`,
    };
  }
  const fallback =
    pick("present", "profile present") ?? pick("default", "profile default");
  if (fallback) return fallback;
  if (usable.length === 1) return pick(usable[0], `profile ${usable[0]}`);
  if (usable.length > 1) {
    return {
      error:
        `Several Bisque accounts are configured (${usable.join(", ")}) and none is ` +
        `pinned. Pass --profile <name>, set BISQUE_PROFILE, or commit a ` +
        `.bisque.json with {"profile": "<name>"}.`,
    };
  }
  return null;
}

function requireAuth(flags = {}, cwd = process.cwd()) {
  const auth = resolveAuth({
    profile: typeof flags.profile === "string" ? flags.profile : undefined,
    cwd,
  });
  if (auth?.apiKey) {
    if (!auth.from.startsWith("environment")) say(`using ${auth.from}`);
    return auth;
  }
  if (auth?.error) fail(auth.error);
  fail(
    "No Bisque credentials. Run `node present.mjs login` (browser sign-in), or " +
      "set BISQUE_API_KEY and BISQUE_USER_ID.",
  );
}

function authHeaders(auth) {
  return {
    authorization: `Bearer ${auth.apiKey}`,
    "x-bisque-user-id": auth.userId,
  };
}

// ─── HTTP ────────────────────────────────────────────────────────────────

class ApiError extends Error {
  constructor(status, code, message) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

async function api(target, { method = "POST", body, auth } = {}) {
  const url = target.startsWith("http") ? target : BASE + target;
  const res = await fetch(url, {
    method,
    headers: {
      ...(auth ? authHeaders(auth) : {}),
      ...(body === undefined ? {} : { "content-type": "application/json" }),
    },
    ...(body === undefined ? {} : { body: JSON.stringify(body) }),
  });
  const text = await res.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    /* non-JSON body — surfaced raw below */
  }
  if (!res.ok) {
    throw new ApiError(
      res.status,
      json?.error?.code ?? "HTTP_ERROR",
      json?.error?.message ?? text.slice(0, 500),
    );
  }
  return json;
}

// ─── account preflight (/api/me) ─────────────────────────────────────────

/**
 * GET /api/me — the account snapshot behind both preflights. Best-effort:
 * an old server, a proxy, or a network blip must never break a publish that
 * would have succeeded before this call existed, so every failure degrades
 * to `null` (with a note) and the caller behaves exactly as it always did —
 * including the 412 USERNAME_REQUIRED recovery, which stays as the fallback.
 */
async function fetchMeSafe(auth) {
  try {
    return await api("/api/me", { method: "GET", auth });
  } catch (error) {
    const detail =
      error instanceof ApiError
        ? `${error.status} ${error.code}`
        : (error?.message ?? String(error));
    say(`note: /api/me preflight failed (${detail}) — continuing without it.`);
    return null;
  }
}

/**
 * The handle a publish will land under, for voice resolution: an explicit
 * `--handle`, else the account's default username. Absent when the account
 * has no username at all (a first publish stops on that anyway).
 */
function publishHandle(flags, me) {
  const explicit = typeof flags?.handle === "string" ? flags.handle.trim() : "";
  if (explicit) return explicit.toLowerCase();
  const username = me?.account?.username;
  return typeof username === "string" && username
    ? username.toLowerCase()
    : null;
}

/**
 * The `settings` object on /api/me — defaults set at bisque.cloud. Contract:
 * the object and every field in it are OPTIONAL; an absent field means "not
 * set", never an error. Fields this script understands: `voiceId` (e.g.
 * "kokoro:af_heart") and `engine` (a bisque-voice engine id). `model` is
 * server-side narration only, so it is read but unused here. Anything
 * non-string is ignored.
 *
 * A channel may carry its own voice (`channelVoices.<handle>`), and it wins
 * over the account's when this publish targets that channel — the same
 * precedence the server applies to narration it synthesizes itself. Both
 * fields are taken from the channel entry together, never mixed with the
 * account's, so a channel that sets only an engine can't inherit a voice id
 * saved for a different one. Pass the handle to get that; omit it and this
 * is the account voice, unchanged.
 */
function accountSettings(me, handle) {
  const s = me?.settings;
  if (!s || typeof s !== "object" || Array.isArray(s)) return {};
  const str = (v) => (typeof v === "string" && v !== "" ? v : undefined);

  const channel = handle ? s.channelVoices?.[handle] : undefined;
  const voice =
    channel && typeof channel === "object" && !Array.isArray(channel)
      ? channel
      : s;

  return {
    voiceId: str(voice.voiceId),
    engine: str(voice.engine),
    model: str(s.model),
    fromChannel: voice !== s ? handle : undefined,
  };
}

/** A settings voiceId that LOCAL synthesis can actually speak, resolved
 *  against the engine it was saved with — a bare voice id means nothing on its
 *  own, so the engine is part of the question. Engine-qualified ids
 *  ("kokoro:af_heart", "qwen3-clone-17b:narrator") pass through; a bare id under
 *  a named-Studio engine is one of that pack's nine speakers (ryan, uncle_fu,
 *  …) and gets that engine's prefix; a bare Kokoro voice gets "kokoro:"; an
 *  bare 10–40 alphanumeric id is a cloud voice — not speakable here → null.
 *  The speaker name is deliberately NOT checked against a list:
 *  bisque-voice validates it against the model's own speaker table and names
 *  the real alternatives, so a second copy of the nine ids here would only be
 *  one more thing to drift. Publish and doctor both resolve through this, so
 *  they cannot disagree about what the account's own voice is. */
export function localVoiceRef(voiceId, engineId) {
  if (!voiceId) return null;
  if (voiceId.includes(":")) return voiceId;
  if (isNamedStudioEngine(engineId)) return `${engineId}:${voiceId}`;
  if (/^[a-z]{2}_[a-z0-9]+$/i.test(voiceId)) return `kokoro:${voiceId}`;
  return null;
}

/** Fill flags the caller did not pass from the account's settings. Explicit
 *  flags always win; an engine setting that contradicts the voice's own
 *  `engine:` qualifier is dropped rather than handed to bisque-voice as a
 *  conflict. */
function applyAccountSettings(flags, me) {
  const settings = accountSettings(me, publishHandle(flags, me));
  const source = settings.fromChannel
    ? `@${settings.fromChannel} setting`
    : "account setting";
  if (!flags.voice && settings.voiceId) {
    // An explicit --engine outranks the account's, and inside this branch
    // flags.voice is unset — so engineFor() is exactly "the engine this publish
    // will run", which is the engine a bare voiceId must be read under.
    const local = localVoiceRef(
      settings.voiceId,
      engineFor(flags) ?? settings.engine,
    );
    if (local) {
      flags.voice = local;
      say(`voice: ${local} (${source})`);
    } else {
      say(
        `note: ${source} ${JSON.stringify(settings.voiceId)} is not ` +
          `a local voice; pass --voice, or change the setting on bisque.cloud.`,
      );
    }
  }
  const voiceEngine =
    typeof flags.voice === "string" && flags.voice.includes(":")
      ? flags.voice.split(":")[0]
      : null;
  if (!flags.engine && settings.engine) {
    if (settings.engine === "elevenlabs") {
      // A cloud voice, not a bisque-voice engine. Local synthesis cannot run
      // it, and handing it over produces an unknown-engine error that says
      // nothing about where the setting came from.
      say(
        `note: ${settings.fromChannel ? `@${settings.fromChannel} is` : "this account is"} ` +
          `set to a cloud voice, and narration here is local. Pass ` +
          `--voice <engine:voice>, or pick a local voice at ` +
          `bisque.cloud/welcome.`,
      );
    } else if (!voiceEngine || voiceEngine === settings.engine) {
      flags.engine = settings.engine;
      say(`engine: ${settings.engine} (${source})`);
    }
  }
}

// ─── doctor smoke synthesis ──────────────────────────────────────────────

const SMOKE_TEXT = "Bisque.";
const SMOKE_TIMEOUT_MS = 180_000;
/** Encoded audio is peak-normalized to 0.89 full scale, so real speech sits
 *  far above this, while output that is digitally silent (all-zero or NaN
 *  samples both quantize to 0) sits at ~0. */
const SMOKE_SILENCE_RMS = 0.005;

/** RMS of a 16-bit PCM WAV, as a fraction of full scale. Walks the chunk
 *  list to the `data` chunk rather than assuming a 44-byte header. */
function wavRms(buf) {
  let off = 12;
  while (off + 8 <= buf.length) {
    const id = buf.toString("ascii", off, off + 4);
    const size = buf.readUInt32LE(off + 4);
    if (id === "data") {
      const end = Math.min(off + 8 + size, buf.length);
      let sum = 0;
      let n = 0;
      for (let i = off + 8; i + 1 < end; i += 2) {
        const s = buf.readInt16LE(i) / 32768;
        sum += s * s;
        n += 1;
      }
      return n > 0 ? Math.sqrt(sum / n) : 0;
    }
    off += 8 + size + (size % 2);
  }
  return 0;
}

/** Voices excluded from every listing (they still synthesize when named
 *  explicitly via --voice): af_nicole is a whisper/ASMR-register voice,
 *  wrong for presentation narration. */
const UNLISTED_VOICES = new Set(["af_nicole"]);

/** Which voice the smoke test speaks with — the one a publish would
 *  actually use, so doctor proves the real path, not just "some engine
 *  makes sound": --voice wins, then the account's settings (engine +
 *  voice — a clone engine resolves to its cloned voice on this machine,
 *  a named-Studio engine to its speaker), then a voice found on disk
 *  (preferring one the engine marks `recommended`), then any cloned
 *  voice — each only when its engine is actually installed. Null when
 *  nothing usable exists (the smoke test is then skipped, with a
 *  message, not failed). */
function pickSmokeVoice({
  bin,
  flagVoice,
  settingsVoiceId,
  settingsEngine,
  onDiskVoices,
  installedEngines,
  recommendedVoices = [],
}) {
  const usable = (ref) => {
    if (!ref) return null;
    const engine = ref.includes(":") ? ref.split(":")[0] : null;
    if (engine && !installedEngines.includes(engine)) return null;
    return ref;
  };
  const listClones = () => {
    const cloned = runTtsTry(bin, ["list", "--json"], { timeoutMs: 30_000 });
    if (!cloned.ok) return [];
    try {
      return JSON.parse(cloned.stdout);
    } catch {
      return [];
    }
  };
  if (flagVoice) return flagVoice; // explicit — trust it, errors are informative

  // A clone engine's voice is not in settings at all — it is whatever this
  // machine cloned — so that is the only case needing a lookup here. Every
  // other account voice (named-Studio speaker, Kokoro) goes through the same
  // localVoiceRef the publish path uses, one line below.
  if (
    isCloneEngine(settingsEngine) &&
    installedEngines.includes(settingsEngine)
  ) {
    // Publish narrates in the clone managed from the account recording
    // ("me"), or a hand-made clone. No clone yet ⇒ fall through: publish
    // would create it, and the fallbacks below still prove audio works.
    const clones = listClones().filter((v) => v.engine === settingsEngine);
    const chosen = clones.find((v) => v.name === "me") ?? clones[0];
    if (chosen) return `${settingsEngine}:${chosen.name}`;
  }

  const fromSettings = usable(localVoiceRef(settingsVoiceId, settingsEngine));
  if (fromSettings) return fromSettings;
  if (onDiskVoices.length > 0) {
    // Quality is graded per voice; when the pick is automatic, prefer one
    // the engine recommends over whatever sorts first alphabetically.
    const recommended = onDiskVoices.find((v) => recommendedVoices.includes(v));
    return recommended ?? onDiskVoices[0];
  }
  for (const v of listClones()) {
    const ref = usable(`${v.engine}:${v.name}`);
    if (ref) return ref;
  }
  return null;
}

/** One word through the installed engine, end to end, at doctor time — so an
 *  engine that cannot synthesize (or synthesizes silence) is caught here,
 *  not one minute into a publish. Writes a WAV (loudness is measurable
 *  without an MP3 decoder) to a temp dir that is always removed. */
function smokeSynth(bin, voice, flags) {
  say(`smoke synthesis: ${JSON.stringify(SMOKE_TEXT)} with ${voice}…`);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "present-doctor-"));
  const wav = path.join(tmp, "smoke.wav");
  try {
    const args = ["--text", "-", "--out", wav, "--speed", "1.0"];
    args.push("--voice", voice);
    if (flags.device) args.push("--device", String(flags.device));
    const started = Date.now();
    const res = runTtsTry(bin, args, {
      input: SMOKE_TEXT,
      timeoutMs: SMOKE_TIMEOUT_MS,
    });
    if (!res.ok) {
      say(`smoke synthesis: FAILED — ${res.detail}`);
      const lines = res.stderr.split("\n").filter((l) => l.trim() !== "");
      for (const line of lines.slice(-3)) say(`    ${line}`);
      suggestCpuRetry(flags);
      return;
    }
    const seconds = ((Date.now() - started) / 1000).toFixed(1);
    let durationMs = null;
    try {
      durationMs = JSON.parse(res.stdout).durationMs ?? null;
    } catch {
      /* stdout not JSON — loudness below still decides */
    }
    const rms = fs.existsSync(wav) ? wavRms(fs.readFileSync(wav)) : 0;
    if (rms < SMOKE_SILENCE_RMS) {
      say(
        `smoke synthesis: SILENT — ${voice} produced ` +
          `${durationMs ?? "?"} ms of audio with no audible signal. ` +
          `Publishing now would ship silent narration.`,
      );
      suggestCpuRetry(flags);
      const engine = voice.includes(":") ? voice.split(":")[0] : null;
      if (engine) {
        say(
          `  → or reinstall the engine: bisque-voice uninstall ${engine} && ` +
            `bisque-voice install ${engine}`,
        );
      }
      return;
    }
    say(
      `smoke synthesis: ok — ${durationMs ?? "?"} ms of audible audio ` +
        `in ${seconds}s`,
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

function suggestCpuRetry(flags) {
  if (flags.device === "cpu") return;
  say(
    "  → " +
      (process.platform === "darwin"
        ? "on macOS this is usually the GPU path; retry on CPU:"
        : "retry on CPU:") +
      "\n      node present.mjs doctor --device cpu\n" +
      "    and if that fixes it, pass --device cpu to publish too.",
  );
}

// ─── commands ────────────────────────────────────────────────────────────

async function cmdDoctor(flags) {
  const bin = findTts();
  let installedEngines = [];
  const onDiskVoices = [];
  let recommendedVoices = [];
  if (bin) {
    say(`bisque-voice: ${bin}`);
    // `engines --json` / `aligners --json` flatten the spec into the status,
    // so ids and sizes are top-level fields.
    const engines = ttsJson(bin, ["engines", "--json"]);
    const aligners = ttsJson(bin, ["aligners", "--json"]);
    const ids = (list) =>
      list
        .filter((s) => s.installed)
        .map((s) => s.id)
        .join(", ") || "none";
    installedEngines = engines.filter((s) => s.installed).map((s) => s.id);
    // Engines publish per-voice quality metadata (`voices`, recommended
    // first with grades) in `engines --json`; older builds simply don't.
    recommendedVoices = engines
      .filter((s) => s.installed)
      .flatMap((s) =>
        (s.voices ?? [])
          .filter((v) => v.recommended)
          .map((v) => `${s.id}:${v.id}`),
      );
    say(`  engines installed : ${ids(engines)}`);
    say(
      `  aligners installed: ${ids(aligners)}` +
        (ids(aligners) === "none"
          ? "  (word timings come from the engine itself — approximate)"
          : ""),
    );
    for (const engine of engines.filter((s) => s.installed)) {
      // Kokoro-style packs keep one file per voice; other engines carry their
      // speakers inside the model, and name them in the error for a bad
      // --voice. Only report what is actually on disk — minus unlisted
      // voices, which appear in no listing — recommended first, with the
      // engine's quality grades attached where it publishes them.
      const voicesDir = path.join(engine.path, "voices");
      if (!fs.existsSync(voicesDir)) continue;
      const meta = new Map((engine.voices ?? []).map((v) => [v.id, v]));
      const ids = fs
        .readdirSync(voicesDir)
        .filter((f) => f.endsWith(".bin"))
        .map((f) => path.basename(f, ".bin"))
        .filter((id) => !UNLISTED_VOICES.has(id))
        .sort(
          (a, b) =>
            (meta.get(b)?.recommended ? 1 : 0) -
            (meta.get(a)?.recommended ? 1 : 0),
        );
      if (ids.length > 0) {
        const shown = ids.map((id) => {
          const m = meta.get(id);
          if (!m) return `${engine.id}:${id}`;
          return `${engine.id}:${id} (${m.grade}${m.recommended ? "" : " — not recommended"})`;
        });
        say(`  ${engine.id} voices: ${shown.join(", ")}`);
        onDiskVoices.push(...ids.map((id) => `${engine.id}:${id}`));
      }
    }
    if (ids(engines) === "none") {
      say("  → no engine installed; synthesis fails until you install one.");
      say("    `bisque-voice engines` lists them; nothing picks for you.");
    }
  } else {
    say(
      "bisque-voice: NOT INSTALLED (" +
        (process.platform === "win32"
          ? "%USERPROFILE%\\.bisque\\bin\\bisque-voice.exe"
          : "~/.bisque/bin/bisque-voice") +
        ")",
    );
    say(
      process.platform === "win32"
        ? "  install: irm https://download.bisque.today/bisque-voice/install.ps1 | iex"
        : "  install: curl -fsSL https://download.bisque.today/bisque-voice/install.sh | sh",
    );
  }
  const auth = resolveAuth({
    profile: typeof flags.profile === "string" ? flags.profile : undefined,
  });
  say(
    auth?.apiKey
      ? `credentials: ${auth.userId} (${auth.from})`
      : auth?.error
        ? `credentials: AMBIGUOUS — ${auth.error}`
        : "credentials: NONE — run `node present.mjs login`",
  );
  // The config file holds an API key in plain text. `login` writes it 0600,
  // but a file the `bisque` CLI created earlier can be 0644 and stays that way
  // until something notices — so notice here, where the user is already
  // reading a list of things to fix, and say exactly how to fix it.
  reportConfigPermissions();
  say(`api base   : ${BASE}`);

  // Account preflight: the same /api/me the publish path consults, so a
  // missing username is discovered here, not one minute into a publish.
  let settings = {};
  if (auth?.apiKey) {
    const me = await fetchMeSafe(auth);
    if (me) {
      const acct = me.account ?? {};
      say(
        `account    : ${acct.email ?? acct.userId ?? auth.userId}` +
          ` — tier ${me.tier ?? "?"}, credits ${me.credits?.balance ?? 0}`,
      );
      const handles = Array.isArray(acct.handles) ? acct.handles : [];
      if (acct.username) {
        say(
          `username   : ${acct.username}` +
            (handles.length > 0 ? ` (+ handles: ${handles.join(", ")})` : ""),
        );
      } else {
        say(
          "username   : NONE — the first publish needs one. Claim it now:\n" +
            "             node present.mjs claim-username <handle>",
        );
      }
      // Resolved for the handle a publish would target, so doctor reports
      // the voice that will actually speak rather than the account's.
      settings = accountSettings(me, publishHandle(flags, me));
      const parts = [
        settings.voiceId ? `voice ${settings.voiceId}` : null,
        settings.engine ? `engine ${settings.engine}` : null,
        settings.model ? `model ${settings.model}` : null,
      ].filter(Boolean);
      if (parts.length > 0) {
        say(
          `settings   : ${parts.join(", ")}` +
            (settings.fromChannel
              ? ` (voice set on @${settings.fromChannel})`
              : ""),
        );
      }
    }
  }

  // Smoke synthesis — only when there is an engine to exercise, and
  // skippable with --no-smoke.
  if (!bin || installedEngines.length === 0) return;
  if (flags["no-smoke"]) {
    say("smoke synthesis: skipped (--no-smoke)");
    return;
  }
  const voice = pickSmokeVoice({
    bin,
    flagVoice: typeof flags.voice === "string" ? flags.voice : undefined,
    settingsVoiceId: settings.voiceId,
    settingsEngine: settings.engine,
    onDiskVoices,
    installedEngines,
    recommendedVoices,
  });
  if (!voice) {
    say(
      "smoke synthesis: skipped — no voice to test with " +
        "(pass --voice <engine:voice> to exercise the engine).",
    );
    return;
  }
  smokeSynth(bin, voice, flags);
}

/**
 * Free bytes on the volume that holds HOME — where bisque-voice puts its
 * engines, so it is the number an engine-size recommendation needs. Node 18.15+
 * has fs.statfsSync everywhere; older Nodes fall back to `df -kP` (POSIX, so
 * no line wrapping) or PowerShell/wmic on Windows. Returns null when nothing
 * works — the field is then simply omitted.
 */
function freeDiskBytesForHome() {
  const home = os.homedir();
  try {
    if (typeof fs.statfsSync === "function") {
      const s = fs.statfsSync(home);
      const free = Number(s.bavail) * Number(s.bsize);
      if (Number.isFinite(free) && free >= 0) return free;
    }
  } catch {
    /* fall through to the command-line fallbacks */
  }
  try {
    if (process.platform === "win32") {
      const driveLetter = path.parse(home).root.replace(/[\\/:]+$/, "");
      const ps = spawnSync(
        "powershell",
        [
          "-NoProfile",
          "-Command",
          `(Get-PSDrive -Name ${driveLetter.replace(/:$/, "")}).Free`,
        ],
        { encoding: "utf8", timeout: 15_000 },
      );
      const fromPs = Number((ps.stdout ?? "").trim());
      if (ps.status === 0 && Number.isFinite(fromPs) && fromPs >= 0) {
        return fromPs;
      }
      const wmic = spawnSync(
        "wmic",
        [
          "logicaldisk",
          "where",
          `DeviceID='${driveLetter}'`,
          "get",
          "FreeSpace",
          "/value",
        ],
        { encoding: "utf8", timeout: 15_000 },
      );
      const match = /FreeSpace=(\d+)/.exec(wmic.stdout ?? "");
      if (wmic.status === 0 && match) return Number(match[1]);
    } else {
      const df = spawnSync("df", ["-kP", home], {
        encoding: "utf8",
        timeout: 15_000,
      });
      if (df.status === 0) {
        const lines = (df.stdout ?? "").trim().split("\n");
        const cols = lines[lines.length - 1]?.trim().split(/\s+/) ?? [];
        // POSIX format: Filesystem 1024-blocks Used Available Capacity Mounted
        const availableKb = Number(cols[3]);
        if (Number.isFinite(availableKb) && availableKb >= 0) {
          return availableKb * 1024;
        }
      }
    }
  } catch {
    /* unmeasurable — omit the field */
  }
  return null;
}

/**
 * What this machine is, so the welcome flow on bisque.cloud can recommend an
 * engine size for it. Best-effort by contract: login must NEVER fail over a
 * profile, so any error degrades to omitting fields (or the whole object).
 */
function gatherMachineProfile() {
  try {
    const profile = {
      platform: process.platform,
      arch: process.arch,
      memoryBytes: os.totalmem(),
    };
    const freeDiskBytes = freeDiskBytesForHome();
    // Whole gigabytes only — the size recommendation needs no more, and the
    // exact byte count never needs to leave this machine.
    if (freeDiskBytes !== null) {
      profile.freeDiskBytes = Math.round(freeDiskBytes / 1e9) * 1e9;
    }
    return profile;
  } catch {
    return undefined;
  }
}

async function cmdLogin(flags = {}) {
  // Sign-in writes to a named profile so a second account can be added without
  // displacing the first. Everything that READS credentials already honours
  // `--profile`; without it here, a multi-account machine could resolve a
  // profile it had no way to create.
  const profileName =
    typeof flags.profile === "string" && flags.profile
      ? flags.profile
      : "present";
  const machineProfile = gatherMachineProfile();
  const start = await api("/api/create-cli-session", {
    body: {
      name: `${os.hostname()} (/present)`,
      ...(machineProfile ? { machineProfile } : {}),
    },
  });
  say("Open this URL and approve the sign-in:");
  say(`  ${start.browserUrl}`);
  say(`Pairing code: ${start.pairingCode}`);
  const deadline = Date.now() + 5 * 60 * 1000;
  for (;;) {
    if (Date.now() > deadline)
      fail("Sign-in timed out (the session lasts 5 minutes).");
    await new Promise((r) => setTimeout(r, 2000));
    let poll;
    try {
      poll = await api(
        `/api/poll-cli-session?t=${encodeURIComponent(start.token)}`,
        { method: "GET" },
      );
    } catch (err) {
      // A transient 5xx or network blip on one poll must not kill the
      // sign-in — the session is still pending server-side and the next
      // poll answers. The 5-minute deadline above still bounds the loop.
      if (err instanceof ApiError && err.status < 500) throw err;
      continue;
    }
    if (poll.status === "pending") continue;
    if (poll.status !== "approved") fail(`Sign-in ${poll.status}.`);
    const config = readConfig() ?? {};
    config.profiles = config.profiles ?? {};
    // Its own profile: never overwrite whatever `bisque login` put in
    // `default`, which may belong to a different account.
    config.profiles[profileName] = {
      ...(config.profiles[profileName] ?? {}),
      userId: poll.userId,
      apiKey: poll.apiKey,
      ...(poll.email ? { email: poll.email } : {}),
    };
    fs.mkdirSync(path.dirname(CONFIG_PATH), { recursive: true, mode: 0o700 });
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2) + "\n", {
      mode: 0o600,
    });
    // `mode` above applies only when writeFileSync CREATES the file. The
    // `bisque` CLI usually creates this config first, at 0644, so on most
    // machines the file already exists and that mode is silently ignored —
    // which leaves an API key readable by every account on the box. chmod
    // unconditionally, on every login, so an already-loose file gets fixed
    // rather than inherited.
    fs.chmodSync(CONFIG_PATH, 0o600);
    say(
      `Signed in as ${poll.email ?? poll.userId}; saved to ${CONFIG_PATH} (profile "${profileName}").`,
    );
    return;
  }
}

function cmdPlan(flags) {
  const htmlPath = path.resolve(flags.html ?? "index.html");
  const html = fs.readFileSync(htmlPath, "utf8");
  const plan = narrationPlan(html);
  const problems = lintPresentation(html);
  process.stdout.write(
    JSON.stringify({ narrated: plan.length, problems, slides: plan }, null, 2) +
      "\n",
  );
  if (problems.length > 0) {
    fail(
      `${problems.length} problem(s) to fix before publishing:\n  ` +
        problems.join("\n  "),
    );
  }
}

/**
 * Per-word pronunciation facts for every narrated slide, straight from the
 * voice's own letters-to-sounds stage. Synthesizes nothing.
 *
 * Emits, per slide, bisque-voice's `pronunciation-report --json` envelope:
 * `inspectable`, and for each word its `phonemes`, `respelled`, `inLexicon`
 * and `readings`. Facts only — the caller judges the respellings against how
 * the words should sound. Markers already in the narration stay in the text
 * handed over, so a marked word reports the pinned pronunciation; that is
 * what makes this the verify step of the loop in SKILL.md as well as the
 * report step.
 */
function cmdPronunciationReport(flags) {
  const bin = requireTts();
  const voice = typeof flags.voice === "string" ? flags.voice : null;
  if (!voice) {
    fail(
      "--voice is required: the voice id chooses the lexicon the report " +
        "reads, e.g. --voice kokoro:af_heart.",
    );
  }
  const htmlPath = path.resolve(flags.html ?? "index.html");
  const plan = narrationPlan(fs.readFileSync(htmlPath, "utf8"));
  const slides = plan.map((slide) => {
    const args = [
      "pronunciation-report",
      "--voice",
      voice,
      "--text",
      "-",
      "--json",
    ];
    if (typeof flags.engine === "string" && flags.engine) {
      args.push("--engine", flags.engine);
    }
    const res = runTtsTry(bin, args, { input: slide.text });
    if (!res.ok) {
      if (/unrecognized subcommand|unexpected argument/i.test(res.stderr)) {
        fail(
          "this bisque-voice has no pronunciation-report subcommand — " +
            "update it first:\n" +
            (process.platform === "win32"
              ? "  irm https://download.bisque.today/bisque-voice/install.ps1 | iex"
              : "  curl -fsSL https://download.bisque.today/bisque-voice/install.sh | sh"),
        );
      }
      fail(
        `bisque-voice pronunciation-report failed on ${slide.slideKey} ` +
          `(${res.detail})\n${res.stderr}`,
      );
    }
    return {
      slideIndex: slide.slideIndex,
      slideKey: slide.slideKey,
      ...JSON.parse(res.stdout),
    };
  });
  process.stdout.write(JSON.stringify({ slides }, null, 2) + "\n");
}

/** The manifest's own audio path for a slide — mirrors `audio/<slideKey>.mp3`. */
function audioPathFor(slideKey) {
  return `audio/${slideKey}.mp3`;
}

/**
 * Every file under `<workDir>/assets/`, declared for upload.
 *
 * The format requires fonts and images to be self-hosted and referenced
 * relative to the bundle, so a presentation that renders locally is broken
 * once published unless these travel with it. Walked from disk rather than
 * parsed out of the HTML: a stylesheet's `url(...)`, a `data-lottie-spec`, an
 * `<img srcset>` and a cue's `src` all reference assets, and missing one would
 * publish a page with a hole in it.
 *
 * `contentType` is deliberately a placeholder — the server re-derives it from
 * the extension using the same map it applies to bundle uploads, so there is
 * no second lookup table here to fall out of date.
 */
function collectAssets(workDir) {
  const root = path.join(workDir, "assets");
  if (!fs.existsSync(root) || !fs.statSync(root).isDirectory()) return [];
  const out = [];
  const walk = (dir) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name.startsWith(".")) continue; // .DS_Store and friends
      const abs = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(abs);
        continue;
      }
      if (!entry.isFile()) continue; // never follow a symlink out of the tree
      out.push({
        path: path.relative(workDir, abs).split(path.sep).join("/"),
        contentType: "application/octet-stream",
        size: fs.statSync(abs).size,
        hash: sha256File(abs),
      });
    }
  };
  walk(root);
  return out.sort((a, b) => a.path.localeCompare(b.path));
}

function sha256File(file) {
  return (
    "sha256:" + createHash("sha256").update(fs.readFileSync(file)).digest("hex")
  );
}

/**
 * `voiceId` is recorded in the manifest; it is not used to generate anything.
 * The endpoint only accepts a Kokoro-shaped id or a cloud-voice id, so a voice
 * from another engine is omitted rather than rejected.
 */
function serverVoiceId(voice) {
  if (!voice) return undefined;
  const m = /^(?:kokoro|local):(.+)$/i.exec(voice);
  const bare = m ? m[1] : voice;
  if (/^[a-z]{2}_[a-z0-9]+$/i.test(bare)) return `kokoro:${bare}`;
  if (/^[A-Za-z0-9]{10,40}$/.test(bare)) return bare;
  return undefined;
}

async function cmdPublish(flags) {
  const htmlPath = path.resolve(flags.html ?? "index.html");
  const indexHtml = fs.readFileSync(htmlPath, "utf8");
  const workDir = path.dirname(htmlPath);
  // Resolved from the presentation's own directory, so a repo that pins an
  // account in `.bisque.json` publishes to that account.
  const auth = requireAuth(flags, workDir);
  const audioDir = path.resolve(workDir, flags["audio-dir"] ?? "audio");
  // A bare `--speed` (no value) parses as boolean true, and Number(true) === 1
  // would slip past the range check below and silently narrate at 1.0 — catch it.
  if (flags.speed === true) {
    fail("--speed needs a value between 0.7 and 1.2 (e.g. --speed 1.1)");
  }
  const speed = Number(flags.speed ?? 1.0);
  // The server clamps speechSpeed to 0.7–1.2. Synthesizing outside that range
  // would record a speed the server never stored, so every re-publish would
  // find every slide stale. Refuse instead of silently diverging.
  if (!Number.isFinite(speed) || speed < 0.7 || speed > 1.2) {
    fail("--speed must be a number between 0.7 and 1.2");
  }

  // ── 0. Account preflight. Two jobs, one /api/me call: (a) a fresh account
  // with no username would otherwise fail mid-flow with 412 USERNAME_REQUIRED
  // — catch it BEFORE any synthesis is spent; (b) account settings from
  // bisque.cloud fill in --voice/--engine when they were not passed. Both
  // degrade to today's behavior when /api/me is unavailable, and the 412
  // handler below remains as the fallback.
  const me = await fetchMeSafe(auth);
  if (me) {
    applyAccountSettings(flags, me);
    if (me.account && !me.account.username && !flags.handle) {
      const handles = Array.isArray(me.account.handles)
        ? me.account.handles
        : [];
      fail(
        "This account has no username yet, and a presentation is published under one.\n" +
          (handles.length > 0
            ? `You do own handle(s): ${handles.join(", ")} — pass --handle <one of them>, ` +
              `or claim a default username:\n`
            : "Claim one (3–30 chars, lowercase letters/digits/hyphens):\n") +
          "  node present.mjs claim-username <handle>",
      );
    }
  }

  const problems = lintPresentation(indexHtml);
  if (problems.length > 0) {
    fail(
      `${problems.length} problem(s) in the presentation — nothing was synthesized:\n  ` +
        problems.join("\n  "),
    );
  }
  const plan = narrationPlan(indexHtml);
  const voiceId = serverVoiceId(flags.voice);
  if (flags.voice && !voiceId) {
    say(
      `note: voiceId ${JSON.stringify(flags.voice)} is not a shape the publish ` +
        `endpoint accepts, so the manifest will record the server default. The ` +
        `audio is still yours — nothing is narrated server-side.`,
    );
  }

  const assets = collectAssets(workDir);
  if (assets.length > 0) {
    say(
      `assets: ${assets.length} file(s) under assets/ will publish with the ` +
        `presentation.`,
    );
  }

  // Company publish target: --org wins, else the .bisque.json pin. An org
  // publish has no personal handle, and its natural visibility is "org"
  // (members only) unless the caller says otherwise.
  const org = flags.org !== undefined ? flags.org || null : pinnedOrg(workDir);
  if (org && flags.handle) {
    fail(
      "--handle and --org are mutually exclusive — a company publish has no personal handle.",
    );
  }
  if (org) say(`org: publishing into ${org} on bisque.team`);

  const meta = {
    indexHtml,
    ...(assets.length > 0 ? { assets } : {}),
    ...(flags.title ? { title: flags.title } : {}),
    ...(flags.slug ? { slug: flags.slug } : {}),
    ...(flags["presentation-id"]
      ? { presentationId: flags["presentation-id"] }
      : {}),
    ...(flags.handle ? { handle: flags.handle } : {}),
    ...(org ? { org, ...(flags.group ? { group: flags.group } : {}) } : {}),
    visibility: flags.visibility ?? (org ? "org" : "unlisted"),
    ...(voiceId ? { voiceId } : {}),
    // ALWAYS explicit: speechSpeed is part of the audio cache key, so the value
    // recorded at publish time has to be the exact value synthesis used.
    // Leaving it to a default on either side makes every slide stale on every
    // re-publish.
    speechSpeed: speed,
    ...(flags.context
      ? {
          contextMd: readNamedFile(
            path.resolve(workDir, flags.context),
            "--context",
          ),
        }
      : {}),
    ...(flags.design
      ? {
          designMd: readNamedFile(
            path.resolve(workDir, flags.design),
            "--design",
          ),
        }
      : {}),
  };

  // ── 1. Ask what is stale before spending a minute of synthesis on it.
  let session = null;
  let stale;
  if (flags.all) {
    stale = plan.map((s) => s.slideKey);
    say(`--all: synthesizing every narrated slide (${stale.length}).`);
  } else {
    try {
      session = await api("/api/presentations/publish-narrated", {
        body: meta,
        auth,
      });
      stale = session.staleSlides;
      say(
        `carried forward: ${session.reused.length} slide(s); ` +
          `needs synthesis: ${stale.length}${stale.length ? ` (${stale.join(", ")})` : ""}`,
      );
    } catch (error) {
      if (error instanceof ApiError && error.code === "NO_AUDIO") {
        // First publish (or every slide changed): nothing to carry forward.
        stale = plan.map((s) => s.slideKey);
        say(
          `nothing to carry forward — synthesizing all ${stale.length} narrated slide(s).`,
        );
      } else if (
        error instanceof ApiError &&
        error.code === "USERNAME_REQUIRED"
      ) {
        fail(
          "This account has no username yet, and a presentation is published under one.\n" +
            "Claim one:  node present.mjs claim-username <handle>",
        );
      } else {
        throw error;
      }
    }
  }

  // ── 2. Synthesize exactly those slides.
  const supplied = [];
  if (stale.length > 0) {
    const bin = requireTts();
    ensureStudioEngineInstalled(bin, flags);
    ensureAlignerInstalled(bin, flags);
    await ensureCloneVoiceReady(bin, flags, auth, me);
    fs.mkdirSync(audioDir, { recursive: true });
    for (const slideKey of stale) {
      const slide = plan.find((s) => s.slideKey === slideKey);
      if (!slide) continue;
      const mp3 = path.join(audioDir, `${slideKey}.mp3`);
      const sidecar = path.join(audioDir, `${slideKey}.json`);
      const cached = readCached(sidecar, mp3, slide.text, flags, speed);
      if (cached) {
        say(`${slideKey}: reusing local audio`);
        supplied.push({ slideKey, ...cached.result });
        continue;
      }
      say(`${slideKey}: synthesizing ${slide.wordCount} words…`);
      const args = ["--text", "-", "--out", mp3, "--speed", String(speed)];
      if (flags.voice) args.push("--voice", flags.voice);
      if (flags.engine) args.push("--engine", flags.engine);
      if (flags.align) args.push("--align", flags.align);
      if (flags.device) args.push("--device", String(flags.device));
      if (flags["match-macos"]) args.push("--match-macos");
      const result = JSON.parse(runTts(bin, args, { input: slide.text }));
      if (result.words.length !== slide.wordCount) {
        fail(
          `${slideKey}: bisque-voice returned ${result.words.length} timings for ` +
            `${slide.wordCount} words. Publishing that would misplace every cue.`,
        );
      }
      // The digest we are about to declare must describe the bytes actually on
      // disk: re-hash the file rather than trust the reported value, so a
      // truncated or half-written MP3 is caught here, not at watch time.
      const actual = sha256File(mp3);
      if (actual !== result.hash) {
        fail(
          `${slideKey}: ${mp3} does not match the digest bisque-voice reported.`,
        );
      }
      fs.writeFileSync(
        sidecar,
        JSON.stringify(
          { text: slide.text, voice: flags.voice ?? null, speed, result },
          null,
          2,
        ) + "\n",
      );
      supplied.push({ slideKey, ...result });
    }
  }

  // ── 3. Publish for real (or complete the probe session when nothing changed).
  if (supplied.length > 0) {
    session = await api("/api/presentations/publish-narrated", {
      body: {
        ...meta,
        presentationId: session?.presentationId ?? meta.presentationId,
        audio: supplied.map((s) => ({
          slideKey: s.slideKey,
          words: s.words,
          durationMs: s.durationMs,
          size: s.size,
          hash: s.hash,
          exact: s.exact,
          contentType: s.contentType,
        })),
      },
      auth,
    });
  }
  if (!session) fail("No publish session — nothing to publish.");

  // ── 4. Upload each file straight to object storage, then close the session.
  for (const target of session.uploadUrls) {
    // Two kinds of upload come back from one session. An asset keeps its
    // bundle-relative path, so it resolves against the presentation directory;
    // audio is addressed by slide key and may live in a relocated --audio-dir.
    const local = target.path.startsWith("assets/")
      ? path.resolve(workDir, target.path)
      : path.join(audioDir, `${path.basename(target.path, ".mp3")}.mp3`);
    if (!fs.existsSync(local)) {
      fail(`publish asked for ${target.path} but ${local} does not exist.`);
    }
    say(`uploading ${target.path}…`);
    const res = await fetch(target.url, {
      method: target.method,
      headers: target.headers,
      body: fs.readFileSync(local),
    });
    if (!res.ok)
      fail(
        `upload of ${target.path} failed: ${res.status} ${await res.text()}`,
      );
  }

  const done = await api(session.completeUrl, {
    body: { publishId: session.publishId, files: session.files },
    auth,
  });

  for (const w of session.warnings ?? []) say(`warning: ${w}`);
  process.stdout.write(
    JSON.stringify(
      {
        webUrl: session.webUrl,
        presentationId: session.presentationId,
        synthesized: session.synthesized,
        reused: session.reused,
        staleSlides: session.staleSlides,
        complete: done?.status ?? "ok",
      },
      null,
      2,
    ) + "\n",
  );
}

function readCached(sidecar, mp3, text, flags, speed) {
  try {
    const cached = JSON.parse(fs.readFileSync(sidecar, "utf8"));
    if (cached.text !== text) return null;
    if ((cached.voice ?? null) !== (flags.voice ?? null)) return null;
    if (cached.speed !== speed) return null;
    if (!fs.existsSync(mp3)) return null;
    if (sha256File(mp3) !== cached.result.hash) return null;
    return cached;
  } catch {
    return null;
  }
}

/** A file the caller explicitly named. Missing is a mistake worth stopping for
 *  — publishing without the `context.md` someone asked for is silent. */
function readNamedFile(p, flag) {
  if (!fs.existsSync(p)) fail(`${flag} ${p} does not exist.`);
  return fs.readFileSync(p, "utf8");
}

async function cmdClaimUsername(rest, flags) {
  const username = rest[0];
  if (!username) fail("usage: claim-username <handle>");
  const auth = requireAuth(flags);
  const res = await api("/api/claim-username", { body: { username }, auth });
  say(`claimed: ${JSON.stringify(res)}`);
}

// ─── plumbing ────────────────────────────────────────────────────────────

function say(msg) {
  process.stderr.write(msg + "\n");
}

function fail(msg) {
  process.stderr.write("present: " + msg + "\n");
  process.exit(1);
}

function parseFlags(argv) {
  const flags = {};
  const rest = [];
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith("--")) {
      rest.push(arg);
      continue;
    }
    const eq = arg.indexOf("=");
    if (eq !== -1) {
      flags[arg.slice(2, eq)] = arg.slice(eq + 1);
      continue;
    }
    const name = arg.slice(2);
    const next = argv[i + 1];
    if (next === undefined || next.startsWith("--")) {
      flags[name] = true;
    } else {
      flags[name] = next;
      i += 1;
    }
  }
  return { flags, rest };
}

/**
 * `spec` — fetch the authoring spec, authenticated when credentials exist.
 *
 * The endpoint is public and takes no auth for the ordinary payload, so this
 * could be a bare `curl`, and it was one for a long time. It is a command now
 * because the spec can carry SOFT-LAUNCHED sections that only the calling
 * account is entitled to, and those only appear when a bearer token comes
 * along. Without this, a capability rolled out to an account would be
 * invisible to the very workflow that account authors with.
 *
 * Credentials are optional here on purpose: no profile, no `login`, an expired
 * key — all of them still get the correct public spec, which is the whole
 * point of the endpoint. Auth only ever ADDS.
 *
 * The default part is `core` — the format contract without the deep
 * capability modules. The core's own index names the modules (design,
 * charts, tables, dither, motion, code-walkthrough, cues-advanced); fetch
 * each one the presentation needs with `--part <name>`. `--part format` is the whole
 * spec with every module inlined.
 */
async function cmdSpec(flags) {
  const part = typeof flags.part === "string" ? flags.part : "core";
  const auth = resolveAuth({
    profile: typeof flags.profile === "string" ? flags.profile : undefined,
    cwd: process.cwd(),
  });
  const headers = { accept: "text/markdown" };
  if (auth?.apiKey) Object.assign(headers, authHeaders(auth));

  // Path form first (the canonical spelling; unknown names 404 loudly).
  // Fall back to the legacy ?part= query for servers that predate path
  // addressing — the query form answers an unknown part with the full
  // default payload, so the fallback degrades to "more spec than asked
  // for", never to a miss.
  const urls = [
    `${BASE}/api/presentations/spec/${encodeURIComponent(part)}.md`,
    `${BASE}/api/presentations/spec?part=${encodeURIComponent(part)}`,
  ];
  let response;
  for (const url of urls) {
    response = await fetch(url, { headers });
    if (response.ok) break;
  }
  if (!response.ok) {
    fail(`spec fetch failed: HTTP ${response.status}`);
  }
  const text = await response.text();

  const out = typeof flags.out === "string" ? flags.out : null;
  if (out) {
    fs.writeFileSync(out, text);
    say(
      `wrote ${out} (${text.length} chars)${auth?.apiKey ? ", authenticated" : ""}`,
    );
  } else {
    process.stdout.write(text);
  }
}

const USAGE = `usage:
  node present.mjs doctor  [--voice V] [--device auto|cpu|gpu] [--no-smoke]
  node present.mjs login   [--profile NAME]
  node present.mjs claim-username <handle> [--profile NAME]
  node present.mjs spec    [--part core|format|<module>|portable|macos|recipe] [--out spec.md]
  node present.mjs plan    [--html index.html]
  node present.mjs pronunciation-report [--html index.html] --voice <engine:voice>
                           [--engine E]
  node present.mjs publish [--html index.html] --voice <engine:voice>
                           [--title T] [--slug S] [--visibility unlisted|public|private]
                           [--presentation-id ID] [--handle H]
                           [--org SLUG] [--group ID]
                           [--context context.md] [--design design.md]
                           [--engine E] [--align A|none] [--speed 1.0] [--match-macos]
                           [--device auto|cpu|gpu] [--audio-dir audio] [--all]
                           [--profile NAME]

--voice/--engine fall back to the account's settings on bisque.cloud (via
/api/me) when omitted.

--org publishes into a company's library on bisque.team (members only by
default); a repo can pin it with {"org": "<slug>"} in .bisque.json.

Credentials: BISQUE_API_KEY + BISQUE_USER_ID, else --profile / BISQUE_PROFILE /
.bisque.json's "profile", else the single profile in ~/.bisque/config.json.`;

async function main() {
  if (typeof fetch !== "function") {
    fail("needs Node 18+ (global fetch) or bun.");
  }
  const [command, ...argv] = process.argv.slice(2);
  const { flags, rest } = parseFlags(argv);
  switch (command) {
    case "doctor":
      return cmdDoctor(flags);
    case "login":
      return cmdLogin(flags);
    case "claim-username":
      return cmdClaimUsername(rest, flags);
    case "spec":
      return cmdSpec(flags);
    case "plan":
      return cmdPlan(flags);
    case "pronunciation-report":
      return cmdPronunciationReport(flags);
    case "publish":
      return cmdPublish(flags);
    default:
      process.stderr.write(USAGE + "\n");
      process.exit(command ? 1 : 0);
  }
}

// Only run when invoked as a program, so the extractor can be imported by a
// test without publishing anything. argv[1] is realpath'd because
// import.meta.url is already resolved — invoking through a symlinked skill
// directory (~/.claude/skills/present → a repo checkout) must still
// count as direct invocation, not silently do nothing.
const invokedDirectly =
  process.argv[1] !== undefined &&
  (() => {
    try {
      return (
        import.meta.url === pathToFileURL(fs.realpathSync(process.argv[1])).href
      );
    } catch {
      return false;
    }
  })();

if (invokedDirectly) {
  main().catch((error) => {
    if (error instanceof ApiError) {
      fail(
        `${error.status} ${error.code}: ${error.message}` +
          (error.code === "USERNAME_REQUIRED"
            ? "\nClaim one:  node present.mjs claim-username <handle>"
            : ""),
      );
    }
    fail(error?.stack ?? String(error));
  });
}

// Series mode: one style guide for every engine, then a local palette check.
// The score is implemented in imgtool.py (Pillow only). It is 0.8 times the cosine
// of an 8-bin joint RGB histogram plus 0.2 times the cosine of a 4x4 luminance grid,
// both taken from a 64x64 resize. 1 is the same palette. There is no CLIP model and
// no network call.

import path from 'node:path';

export const STYLE_METHOD = "palette-histogram";
export const DEFAULT_STYLE_THRESHOLD = 0.72;
export const DEFAULT_STYLE_RETRIES = 2;

export function splitJobsDocument(doc) {
  if (Array.isArray(doc)) return { jobs: doc, series: null, root: null };
  if (doc && typeof doc === "object" && Array.isArray(doc.jobs)) {
    return { jobs: doc.jobs, series: doc.series === undefined ? null : doc.series, root: doc };
  }
  throw new Error("jobs file must be a JSON array, or an object with a jobs array");
}

// Informational only. Compare ordered lists, including duplicates, after path.resolve
// relative to the jobs file. Do not resolve symlinks, inspect images, or compare prompts.
export function shouldHintSeries({ flag, root, jobs, base }) {
  if (flag || (root && Object.hasOwn(root, 'series')) || jobs.length < 4) return false;
  let shared = null;
  for (const job of jobs) {
    if (!Array.isArray(job?.ref) || !job.ref.length) return false;
    if (!job.ref.every(ref => typeof ref === 'string' && ref.trim().length > 0)) return false;
    const refs = job.ref.map(ref => path.resolve(base, ref));
    if (shared === null) shared = refs;
    else if (refs.length !== shared.length || refs.some((ref, i) => ref !== shared[i])) return false;
  }
  return true;
}

function asList(value) {
  if (value == null || value === "") return [];
  const items = Array.isArray(value) ? value : [value];
  return items.map(item => String(item)).filter(item => item !== "");
}

function asEngines(value) {
  if (value == null || value === "") return null;
  const items = Array.isArray(value) ? value : String(value).split(",");
  const names = items.map(item => String(item).trim()).filter(Boolean);
  return names.length ? names : null;
}

function pickNumber(raw, label) {
  if (raw == null || raw === "") return null;
  const number = Number(raw);
  if (!Number.isFinite(number)) throw new Error(label + " is not a number: " + raw);
  return number;
}

// flag, a jobs-file series value, and the CLI fields. CLI wins when it is set.
export function resolveSeriesConfig({ flag, fileSeries, root, cli }) {
  const options = cli ?? {};
  const spec = fileSeries && typeof fileSeries === "object" ? fileSeries : null;
  const styleFromString = typeof fileSeries === "string" ? fileSeries : "";
  const enabled = Boolean(flag || fileSeries === true || spec || styleFromString);
  if (!enabled) {
    return {
      enabled: false, method: STYLE_METHOD, style: "", styleRefs: [],
      threshold: DEFAULT_STYLE_THRESHOLD, maxRetries: DEFAULT_STYLE_RETRIES,
      engines: null, prefer: "off",
    };
  }
  const source = spec ?? (fileSeries === true ? (root ?? {}) : {});
  const style = String(options.style ?? source.style ?? styleFromString ?? "").trim();
  if (!style) throw new Error("series mode needs a style guide (series.style, --style, or --style-file)");
  const threshold = pickNumber(options.threshold != null && options.threshold !== "" ? options.threshold : source.threshold, "series threshold");
  const maxRetries = pickNumber(options.maxRetries != null && options.maxRetries !== "" ? options.maxRetries : source.max_retries, "series max_retries");
  const chosenThreshold = threshold == null ? DEFAULT_STYLE_THRESHOLD : threshold;
  const chosenRetries = maxRetries == null ? DEFAULT_STYLE_RETRIES : maxRetries;
  if (!(chosenThreshold > 0) || chosenThreshold > 1) throw new Error("series threshold must be greater than 0 and at most 1");
  if (!Number.isInteger(chosenRetries) || chosenRetries < 0) throw new Error("series max_retries must be a non-negative integer");
  const prefer = String(options.prefer || source.prefer || "consistent");
  if (prefer !== "consistent" && prefer !== "off") throw new Error("series prefer must be consistent or off");
  const refs = options.refs && options.refs.length ? asList(options.refs) : asList(source.ref);
  const engines = options.engines != null ? asEngines(options.engines) : asEngines(source.engines);
  return {
    enabled: true, method: STYLE_METHOD, style, styleRefs: refs,
    threshold: chosenThreshold, maxRetries: chosenRetries, engines, prefer,
  };
}

// The same characters for every engine. The subject stays the job prompt.
export function stylePrompt(prompt, style) {
  return String(prompt).trim() + "\n\nSTYLE GUIDE (apply to every image in this series; do not change the subject):\n" + String(style).trim();
}

// Style references go in front of the job's own references, and never past the engine limit.
// A full slot, or a video job, keeps the job references and uses the style text only.
export function styleRefsForEngine({ maxRefs, jobRefs, styleRefs, video }) {
  const own = (jobRefs ?? []).slice();
  const style = styleRefs ?? [];
  if (!style.length) return { refs: own, attached: 0, textOnly: false, reason: null };
  if (video) {
    return { refs: own, attached: 0, textOnly: true, reason: "video uses the reference slot as the motion source" };
  }
  const limit = maxRefs == null ? own.length : maxRefs;
  const room = limit === Infinity ? Infinity : limit - own.length;
  if (!(room > 0)) {
    return { refs: own, attached: 0, textOnly: true, reason: "reference limit " + limit + " already used by the job" };
  }
  const take = room === Infinity ? style.length : Math.min(style.length, room);
  const attached = style.slice(0, take);
  const refs = attached.concat(own);
  if (attached.length < style.length) {
    return {
      refs, attached: attached.length, textOnly: false,
      reason: "attached " + attached.length + " of " + style.length + " style references (limit " + limit + ")",
    };
  }
  return { refs, attached: attached.length, textOnly: false, reason: null };
}

export function recordStyleScore(stats, engine, score) {
  const row = stats[engine] ?? { sum: 0, n: 0 };
  row.sum += score;
  row.n += 1;
  stats[engine] = row;
  return stats;
}

export function engineMean(stats, engine) {
  const row = stats?.[engine];
  if (!row || !row.n) return null;
  return row.sum / row.n;
}

export function styleMeans(stats) {
  const means = {};
  for (const [engine, row] of Object.entries(stats ?? {})) {
    if (!row?.n) continue;
    means[engine] = { n: row.n, mean: Math.round((row.sum / row.n) * 10000) / 10000 };
  }
  return means;
}

// Highest mean among candidates that already have a score. Ties stay together.
export function bestStyleEngines(stats, candidates) {
  let best = null;
  const names = [];
  for (const engine of candidates ?? []) {
    const mean = engineMean(stats, engine);
    if (mean == null) continue;
    if (best == null || mean > best + 1e-12) {
      best = mean;
      names.length = 0;
      names.push(engine);
    } else if (Math.abs(mean - best) <= 1e-12) names.push(engine);
  }
  return names;
}

// allowedEngines restricts the batch to those engines.
// prefer "consistent" leaves a job for the current best engine while that engine has a free lane.
export function styleRouteAllows({ enabled, video, engine, allowedEngines, prefer, scores, fitting, free }) {
  if (!enabled) return true;
  if (allowedEngines && !allowedEngines.includes(engine)) return false;
  if (video || prefer === "off") return true;
  const best = bestStyleEngines(scores, fitting);
  if (!best.length || best.includes(engine)) return true;
  const bestIsFree = best.some(name => free?.[name]);
  return !bestIsFree;
}

// redos is how many low scores this job already discarded. A pass does not add one.
export function styleDecision({ score, threshold, redos, maxRetries }) {
  const used = redos ?? 0;
  if (Number(score) + 1e-9 >= threshold) return { action: "keep", redos: used };
  const next = used + 1;
  if (next > maxRetries) return { action: "fail", redos: next };
  return { action: "redo", redos: next };
}

// One visual anchor for a text-only series: the first image is kept and later images
// are scored against that file. Reference images score every output, including the first.
export async function takeStyleScreen(series, job, scoreAgainst, sleep) {
  const redos = job.styleRedos ?? 0;
  if (series.styleRefs.length) {
    const score = await scoreAgainst(series.styleRefs);
    return { ...styleDecision({ score, threshold: series.threshold, redos, maxRetries: series.maxRetries }), score, claim: false };
  }
  const wait = sleep ?? (ms => new Promise(resolve => setTimeout(resolve, ms)));
  for (;;) {
    if (series.visualAnchor) {
      const score = await scoreAgainst([series.visualAnchor]);
      return { ...styleDecision({ score, threshold: series.threshold, redos, maxRetries: series.maxRetries }), score, claim: false };
    }
    if (!series.anchorJob || series.anchorJob === job.id) {
      series.anchorJob = job.id;
      return { action: "keep", score: null, claim: true, redos };
    }
    await wait(20);
  }
}

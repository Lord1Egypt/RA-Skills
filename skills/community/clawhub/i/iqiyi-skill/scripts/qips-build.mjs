/**
 * qips 拼接契约与 SKILL.md、references/qips/vtype-recipes.md、references/qips/channel-table.md 对齐。
 * value 一律 encodeURIComponent；分号分隔；末尾保留分号。
 */

/** @typedef {{ key: string, value: string | number | boolean }} QipsEntry */

const SAFE_KEY = /^[A-Za-z0-9_]+$/;
const UNSAFE_VALUE_PROTOCOL = /^(?:javascript|data|file|vbscript|applescript|osascript|shell|qips|qisu|iqiyi):/i;
const SAFE_PLAYBACK_TARGETS = new Set([101, 102, 103, 104, 105, 106]);

function decodeOnce(value) {
  try {
    return decodeURIComponent(value);
  } catch {
    return value;
  }
}

function assertSafeEntry({ key, value }) {
  if (!SAFE_KEY.test(key)) {
    throw new Error(`Unsafe qips key: ${key}`);
  }

  const text = String(value).trim();
  const decoded = decodeOnce(text).trim();
  if (key === "third_play_url" && UNSAFE_VALUE_PROTOCOL.test(decoded)) {
    throw new Error(`Unsafe third_play_url protocol: ${value}`);
  }
}

function assertChannelId(channelid) {
  const id = Number(channelid);
  if (!Number.isInteger(id) || id <= 0) {
    throw new Error(`channelid must be a positive integer: ${channelid}`);
  }
}

function assertRequiredText(name, value) {
  if (typeof value !== "string" || value.trim() === "") {
    throw new Error(`${name} is required`);
  }
}

/**
 * @param {QipsEntry[]} entries 键值顺序即输出顺序（稳定 golden）
 * @returns {string}
 */
export function buildQips(entries) {
  entries.forEach(assertSafeEntry);
  const body = entries
    .map(({ key, value }) => `${key}=${encodeURIComponent(String(value))}`)
    .join(";");
  return `qips://${body};`;
}

/**
 * vtype=6 + target=2 跳频道（可选 third_play_url：已编码前的原始字符串 / JSON 字符串）
 * @param {{ channelid: number | string, third_play_url?: string }} p
 */
export function navigateChannel6(p) {
  assertChannelId(p.channelid);
  /** @type {QipsEntry[]} */
  const entries = [
    { key: "vtype", value: 6 },
    { key: "target", value: 2 },
    { key: "channelid", value: p.channelid },
  ];
  if (p.third_play_url !== undefined && p.third_play_url !== "") {
    entries.push({ key: "third_play_url", value: p.third_play_url });
  }
  return buildQips(entries);
}

/**
 * @param {Record<string, string | number>} queryObj query 段为未 URL 编码的 k=v（整段后再 encode 一次）
 * @param {number | string} channelId
 */
export function buildV7ChannelThirdPlayUrl(queryObj, channelId) {
  const qs = Object.entries(queryObj)
    .map(([k, v]) => `${k}=${v}`)
    .join("&");
  return `?${qs}#/channel/${channelId}/`;
}

/**
 * vtype=7：URL-hash（third_play_url = ?query#/channel/id/），如播单
 * @param {{ query: Record<string, string | number>, channelId: number | string }} p
 */
export function navigateChannel7(p) {
  assertChannelId(p.channelId);
  const raw = buildV7ChannelThirdPlayUrl(p.query, p.channelId);
  return buildQips([
    { key: "vtype", value: 7 },
    { key: "third_play_url", value: raw },
  ]);
}

/**
 * @param {{ target: number }} p 101..106
 */
export function playbackControl6(p) {
  const target = Number(p.target);
  if (!SAFE_PLAYBACK_TARGETS.has(target)) {
    throw new Error(`Unsupported playback target: ${p.target}`);
  }
  return buildQips([
    { key: "vtype", value: 6 },
    { key: "target", value: target },
  ]);
}

/**
 * @param {{ title: string, season?: number | string, year?: string, episode?: number | string }} p
 */
export function playByTitle6(p) {
  assertRequiredText("title", p.title);
  /** @type {QipsEntry[]} */
  const entries = [
    { key: "vtype", value: 6 },
    { key: "action", value: "play" },
    { key: "title", value: p.title },
  ];
  if (p.season !== undefined) {
    entries.push({ key: "season", value: p.season });
  }
  if (p.year !== undefined) {
    entries.push({ key: "year", value: p.year });
  }
  if (p.episode !== undefined) {
    entries.push({ key: "episode", value: p.episode });
  }
  return buildQips(entries);
}

/**
 * JSON 形态 third_play_url（H5 ChannelInfo 等）
 * @param {Record<string, unknown>} obj
 */
export function thirdPlayUrlFromJson(obj) {
  return JSON.stringify(obj);
}

/**
 * @param {{ tvid: string | number, albumid?: string | number, start_pos?: string | number, playrecord?: string | boolean, ischarge?: string | boolean, s2?: string, s3?: string, s4?: string }} p
 */
export function vodPlay0(p) {
  /** @type {QipsEntry[]} */
  const entries = [{ key: "vtype", value: 0 }, { key: "tvid", value: p.tvid }];
  if (p.albumid !== undefined) entries.push({ key: "albumid", value: p.albumid });
  if (p.start_pos !== undefined) entries.push({ key: "start_pos", value: p.start_pos });
  if (p.playrecord !== undefined) entries.push({ key: "playrecord", value: p.playrecord });
  if (p.ischarge !== undefined) entries.push({ key: "ischarge", value: p.ischarge });
  if (p.s2 !== undefined) entries.push({ key: "s2", value: p.s2 });
  if (p.s3 !== undefined) entries.push({ key: "s3", value: p.s3 });
  if (p.s4 !== undefined) entries.push({ key: "s4", value: p.s4 });
  return buildQips(entries);
}

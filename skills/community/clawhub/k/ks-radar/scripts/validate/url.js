const PROFILE_PREFIX = "https://www.kuaishou.com/profile/";
const VIDEO_PREFIX = "https://www.kuaishou.com/short-video/";
const SHORT_PREFIX = "https://v.kuaishou.com/";
const ID_RE = /^[A-Za-z0-9_-]+$/;
const VIDEO_ID_RE = /^3x[A-Za-z0-9_-]+$/;
// 链接本体不含中文引号/书名号；粘贴污染时截断并剥尾
const INLINE_CUT = /[「」『』“”‘’《》〈〉]/;
const TRAILING_PUNCT =
  /[\/.,;:!?"'，。！？；：、）】》「」『』“”‘’《》〈〉［］〔〕〖〗…—～·]+$/;

const PROFILE_MESSAGE =
  "无法识别博主主页。支持 https://www.kuaishou.com/profile/{id}，或纯数字 user_id。裸的 3x 视频 id 请交给评论命令";
const VIDEO_MESSAGE =
  "无法识别视频链接。支持 https://www.kuaishou.com/short-video/{id}、https://v.kuaishou.com/*，或 3x 开头的视频 id。博主主页和纯数字 user_id 请交给作品命令";

function codePointLength(value) {
  return Array.from(value).length;
}

/**
 * 去掉首尾空白和句尾标点，把 http 升级为 https，只小写协议和主机名。
 * 不带 www 的 kuaishou.com 会补上 www。query 和 hash 会去掉。id 保持原样。
 * 无法识别时返回空字符串。
 * @param {string} raw
 * @returns {string}
 */
function scrubUrlDecorators(raw) {
  let text = String(raw).trim();
  const cut = text.search(INLINE_CUT);
  if (cut >= 0) text = text.slice(0, cut);
  return text.replace(TRAILING_PUNCT, "").trim();
}

function normalizeUrl(raw) {
  if (typeof raw !== "string") return "";
  let url = scrubUrlDecorators(raw);
  if (!url || /\s/.test(url)) return "";
  if (/^\d+$/.test(url)) return url;
  if (VIDEO_ID_RE.test(url)) return url;

  url = url.replace(/^https?:\/\//i, "https://");
  url = url.replace(
    /^https:\/\/([^/?#]+)/i,
    (_, host) => "https://" + host.toLowerCase(),
  );
  url = url.replace(
    /^https:\/\/kuaishou\.com\//,
    "https://www.kuaishou.com/",
  );
  url = url.replace(
    /^https:\/\/www\.kuaishou\.com\/(profile|short-video)(?=\/)/i,
    (_, pathPrefix) => "https://www.kuaishou.com/" + pathPrefix.toLowerCase(),
  );
  url = url.split("#")[0].split("?")[0].replace(/\/+$/, "");
  if (!url.startsWith("https://")) return "";
  return url;
}

function idAfter(url, prefix) {
  if (!url.startsWith(prefix)) return "";
  return url.slice(prefix.length).split(/[/?#]/)[0];
}

function isProfileUrl(raw) {
  const url = normalizeUrl(raw);
  if (!url) return false;
  if (/^\d+$/.test(url)) return codePointLength(url) <= 255;
  const id = idAfter(url, PROFILE_PREFIX);
  return ID_RE.test(id) && codePointLength(url) <= 255;
}

function isVideoUrl(raw) {
  const url = normalizeUrl(raw);
  if (!url || codePointLength(url) > 255) return false;
  if (VIDEO_ID_RE.test(url)) return true;
  if (ID_RE.test(idAfter(url, VIDEO_PREFIX))) return true;
  if (url.startsWith(SHORT_PREFIX)) {
    const rest = url.slice(SHORT_PREFIX.length);
    return /^[A-Za-z0-9_-]+(?:\/[A-Za-z0-9_-]+)*$/.test(rest);
  }
  return false;
}

function rejectLength(url, label) {
  if (codePointLength(url) > 255) {
    const error = new Error(`${label}长度不能超过 255 个字符`);
    error.code = "INVALID_URL";
    throw error;
  }
}

function resolveProfileUrl(raw) {
  const url = normalizeUrl(raw);
  if (!isProfileUrl(raw)) {
    const error = new Error(PROFILE_MESSAGE);
    error.code = "INVALID_URL";
    throw error;
  }
  rejectLength(url, "博主主页链接或 user_id");
  if (/^\d+$/.test(url)) return url;
  return PROFILE_PREFIX + idAfter(url, PROFILE_PREFIX);
}

function resolveVideoUrl(raw) {
  const url = normalizeUrl(raw);
  if (!isVideoUrl(raw)) {
    const error = new Error(VIDEO_MESSAGE);
    error.code = "INVALID_URL";
    throw error;
  }
  rejectLength(url, "视频链接或视频 id");
  if (VIDEO_ID_RE.test(url)) return url;
  const videoId = idAfter(url, VIDEO_PREFIX);
  if (videoId) return VIDEO_PREFIX + videoId;
  return url;
}

function url2Name(url) {
  if (typeof url !== "string" || url === "") return "unknown";
  const clean = url.trim().split("?")[0].split("#")[0];
  const name = clean
    .replace(/^https?:\/\//, "")
    .replace(/www\.kuaishou\.com\/short-video\//, "video_")
    .replace(/www\.kuaishou\.com\/profile\//, "profile_")
    .replace(/v\.kuaishou\.com\//, "short_")
    .replace(/[\/?=&-]/g, "_");
  return name || "unknown";
}

module.exports = {
  normalizeUrl,
  isProfileUrl,
  isVideoUrl,
  resolveProfileUrl,
  resolveVideoUrl,
  url2Name,
  PROFILE_MESSAGE,
  VIDEO_MESSAGE,
};

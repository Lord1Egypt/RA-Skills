function normalizeUrl(url) {
  if (typeof url !== "string" || url.trim() === "") return false;
  url = url.trim();
  url = url.replace(/^http:\/\//, "https://");
  if (url.indexOf(" ") !== -1) return false;
  if (/^\d+$/.test(url)) return url;
  if (url.startsWith("3x")) return url;
  if (!url.startsWith("https://")) return false;
  return url;
}

function isVideoUrl(url) {
  url = normalizeUrl(url);
  if (!url) return false;
  if (url.startsWith("https://www.kuaishou.com/short-video/")) {
    return true;
  } else if (url.startsWith("https://v.kuaishou.com/")) {
    return true;
  } else if (url.startsWith("3x")) {
    return true;
  } else {
    return false;
  }
}

function isProfileUrl(url) {
  url = normalizeUrl(url);
  if (!url) return false;
  if (url.startsWith("https://www.kuaishou.com/profile/")) {
    return true;
  } else if (isFinite(url) && url > 10) {
    return true;
  } else {
    return false;
  }
}

function url2Name(url) {
  if (typeof url !== "string" || url === "") return "unknown";
  const clean = url.trim();
  const qIndex = clean.indexOf("?");
  const base = qIndex >= 0 ? clean.slice(0, qIndex) : clean;
  const name = base
    .replace(/^https?:\/\//, "")
    .replace(/www\.kuaishou\.com\/short-video\//, "video_")
    .replace(/www\.kuaishou\.com\/profile\//, "profile_")
    .replace(/v\.kuaishou\.com\//, "short_")
    .replace(/[\/?=&-]/g, "_");
  return name || "unknown";
}

module.exports = {
  normalizeUrl,
  isVideoUrl,
  isProfileUrl,
  url2Name,
};

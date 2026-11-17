/** Shared validation and file utilities. No browser/dependency side effects on import. */
import {
  realpathSync,
  existsSync,
  renameSync,
  rmSync,
  readFileSync,
} from "node:fs";
import { dirname, resolve, basename, join } from "node:path";
import { randomBytes } from "node:crypto";

// One version everywhere: package.json is the source, and the CLIs print it.
// A hardcoded copy drifts the moment the skill is bumped, and the drift only
// shows up in a --version output nobody compares against the manifest.
export function skillVersion(dir) {
  try {
    const pkg = JSON.parse(readFileSync(join(dir, "package.json"), "utf8"));
    if (typeof pkg.version === "string" && pkg.version) return pkg.version;
  } catch {}
  return "unknown";
}

export function svgRootInfo(source) {
  // Ignore comments, XML declarations and doctypes before looking for the actual root.
  const src = source
    .replace(/<!--[\s\S]*?-->/g, "")
    .replace(/<\?[\s\S]*?\?>/g, "")
    .replace(/<!DOCTYPE(?:[^>"'\[]|"[^"]*"|'[^']*'|\[[\s\S]*?\])*>/gi, "");
  const tag = src.match(/<svg\b(?:[^>"']|"[^"]*"|'[^']*')*>/i)?.[0];
  if (!tag) throw new Error("no <svg> root found");
  const attrs = new Map();
  for (const m of tag.matchAll(/\s+([\w:.-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')/g))
    if (!attrs.has(m[1].toLowerCase()))
      attrs.set(m[1].toLowerCase(), m[2] ?? m[3]);
  const px = (v) => {
    if (
      !v ||
      !/^\s*\+?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?(?:px)?\s*$/i.test(v)
    )
      return null;
    const n = Number(v.trim().replace(/px$/i, ""));
    return Number.isFinite(n) && n > 0 ? n : null;
  };
  const vb = attrs
    .get("viewbox")
    ?.trim()
    .split(/[\s,]+/)
    .map(Number);
  const hasViewBox =
    vb?.length === 4 && vb.every(Number.isFinite) && vb[2] > 0 && vb[3] > 0;
  let w = px(attrs.get("width")),
    h = px(attrs.get("height"));
  if (hasViewBox) {
    if (w && !h) h = (w * vb[3]) / vb[2];
    else if (h && !w) w = (h * vb[2]) / vb[3];
    else if (!w && !h) {
      w = vb[2];
      h = vb[3];
    }
  }
  return {
    source: src,
    tag,
    size: w && h ? { w, h } : null,
    hasViewBox: !!hasViewBox,
    hasViewBoxAttr: attrs.has("viewbox"),
  };
}

export function sameFile(a, b) {
  const canon = (p) => (existsSync(p) ? realpathSync(p) : resolve(p));
  const fold = (p) => (process.platform === "win32" ? p.toLowerCase() : p);
  return fold(canon(a)) === fold(canon(b));
}

export function safeUrl(value) {
  try {
    const u = new URL(value);
    u.username = "";
    u.password = "";
    u.search = "";
    u.hash = "";
    return u.href;
  } catch {
    return value;
  }
}

export function assertBudget(w, h, density, maxPixels, label = "image") {
  const rw = Math.ceil(w * density),
    rh = Math.ceil(h * density);
  if (![w, h, density, rw, rh].every(Number.isFinite) || w <= 0 || h <= 0)
    throw new Error(`${label} has invalid dimensions: ${w}×${h}`);
  if (rw > 32767 || rh > 32767 || rw * rh > maxPixels)
    throw new Error(
      `${label} ${rw}×${rh} exceeds the safety budget (${maxPixels} pixels; 32767 per axis). Reduce dimensions/--scale/--dpr, or raise --max-pixels deliberately.`,
    );
}

// Chromium refuses page and WebSocket URLs on its restricted ports (1723/PPTP,
// 6000/X11, 10080/Amanda, …); the highest is 10080. listen(0) is not enough —
// some hosts keep handing out restricted or low ports — so pick a random port
// above 10080, retrying when the OS has reserved it (EACCES) or it is already
// in use (EADDRINUSE).
const SAFE_PORT_MIN = 13200;
const SAFE_PORT_MAX = 14999;
export function listenOnSafePort(server, host = "127.0.0.1") {
  return new Promise((resolve, reject) => {
    let attempts = 80;
    const attempt = () => {
      const port =
        SAFE_PORT_MIN +
        Math.floor(Math.random() * (SAFE_PORT_MAX - SAFE_PORT_MIN + 1));
      const onError = (error) => {
        server.removeListener("error", onError);
        if (
          (error.code === "EADDRINUSE" || error.code === "EACCES") &&
          --attempts > 0
        )
          attempt();
        else reject(error);
      };
      server.once("error", onError);
      server.listen(port, host, () => {
        server.removeListener("error", onError);
        resolve();
      });
    };
    attempt();
  });
}

export function tempOutput(output) {
  return join(
    dirname(resolve(output)),
    `.${basename(output)}.html-shot-${randomBytes(8).toString("hex")}.tmp`,
  );
}

export async function atomicImage(pipe, output) {
  const tmp = tempOutput(output);
  try {
    const info = await pipe.toFile(tmp);
    renameSync(tmp, resolve(output));
    return info;
  } finally {
    rmSync(tmp, { force: true });
  }
}

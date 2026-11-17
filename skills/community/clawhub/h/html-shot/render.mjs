#!/usr/bin/env node
/** Render trusted HTML/SVG/HTTP(S) into PNG/JPEG/WebP. See references/cli.md. */
import { createServer } from "node:http";
import {
  createReadStream,
  existsSync,
  statSync,
  realpathSync,
  readFileSync,
} from "node:fs";
import { randomBytes } from "node:crypto";
import { dirname, resolve, extname, basename, sep, relative } from "node:path";
import { fileURLToPath } from "node:url";
import {
  svgRootInfo,
  sameFile,
  safeUrl,
  assertBudget,
  atomicImage,
  listenOnSafePort,
  skillVersion,
} from "./lib.mjs";

// The per-run server token is a 32-hex hostname. main() redacts it with the real
// token; this shape-based fallback covers the top-level catch, where that binding
// is out of scope.
export const redactToken = (value) => String(value).replace(/\b[a-f0-9]{32}\.localhost\b/gi, "<token>.localhost");
const HELP = `html-shot — render trusted HTML/SVG or HTTP(S) to an image
Usage: node render.mjs <input> <output.png|jpg|webp> [options]
  --width N --height N   CSS viewport/capture dimensions (auto from body by default)
  --selector CSS | --full   Element or full-page capture
  --dpr N --scale N      Output density (1); render supersampling (2)
  --format png|jpeg|webp --quality 1..100 --palette --colors 2|4|16|256
  --transparent --scheme light|dark --style CSS --base DIR --wait MS
  --channel chrome|msedge (also -beta/-dev) | --executable PATH
  --timeout MS          Total browser/render deadline (60000)
  --max-pixels N        Raster pixel budget (64000000; also 32767 per axis)
  --wait-for CSS        Wait for a visible readiness marker
  --offline             Local inputs only; block non-local network requests
  --allow-missing       Keep warnings but exit 0 for failed subresources
  --help | --version
Details: references/cli.md. HTML executes JavaScript; this is not a security sandbox.`;
const SKILL_DIR = dirname(fileURLToPath(import.meta.url));

/**
 * Render one input to one image file.
 *
 * This is the engine behind both entry points: render.mjs calls it from the CLI
 * below, and icons.mjs calls it in-process to build an icon master. Callers pass
 * their own argv so neither has to spawn the other, and `log` lets the CLI keep
 * its result line on stdout while a library caller stays quiet.
 */
export async function renderImage(argv, { log = console.log } = {}) {
  const PW_CLI = resolve(SKILL_DIR, "node_modules/playwright/cli.js");
  const INSTALL_HINT = `cd "${SKILL_DIR}" && npm ci && node "${PW_CLI}" install chromium`;

  const [nodeMajor, nodeMinor] = process.versions.node.split(".").map(Number);
  if (nodeMajor < 20 || (nodeMajor === 20 && nodeMinor < 9)) {
    console.error(
      `html-shot: needs Node >= 20.9 (sharp's floor; playwright asks for 20); this is ${process.versions.node}.`,
    );
    throw new Error("see diagnostic above");
  }

  let chromium, sharp;
  try {
    ({ chromium } = await import("playwright"));
    ({ default: sharp } = await import("sharp"));
  } catch (e) {
    console.error(
      `html-shot: dependencies are not installed (${e.code || e.message}).`,
    );
    console.error(`Run once:\n  ${INSTALL_HINT}`);
    throw new Error("see diagnostic above");
  }

  function fail(msg) {
    throw new Error(msg);
  }
  const warn = (msg) => console.error(`html-shot: note — ${msg}`);

  const [inputArg, output, ...rest] = argv;
  if (!inputArg || !output) fail("missing <input> or <output>; use --help");

  const VALUE_FLAGS = new Set([
    "width",
    "height",
    "dpr",
    "scale",
    "format",
    "quality",
    "scheme",
    "base",
    "wait",
    "selector",
    "colors",
    "channel",
    "style",
    "executable",
    "timeout",
    "max-pixels",
    "wait-for",
  ]);
  const BOOL_FLAGS = new Set([
    "transparent",
    "full",
    "palette",
    "offline",
    "allow-missing",
  ]);
  const opts = {};
  for (let i = 0; i < rest.length; i++) {
    if (!rest[i].startsWith("--")) fail(`unexpected argument "${rest[i]}"`);
    const name = rest[i].slice(2);
    if (BOOL_FLAGS.has(name)) opts[name] = true;
    else if (VALUE_FLAGS.has(name)) {
      opts[name] = rest[++i];
      if (opts[name] === undefined || opts[name].startsWith("--"))
        fail(`--${name} needs a value`);
    } else fail(`unknown option --${name}`);
  }
  const int = (name, def, min = 1) => {
    if (opts[name] === undefined) return def;
    const n = Number(opts[name]);
    if (!Number.isSafeInteger(n) || n < min)
      fail(`--${name} needs a whole number >= ${min}, got "${opts[name]}"`);
    return n;
  };
  const ratio = (name, def, min, max) => {
    if (opts[name] === undefined) return def;
    const n = Number(opts[name]);
    if (!Number.isFinite(n) || n < min || n > max)
      fail(
        `--${name} needs a number between ${min} and ${max}, got "${opts[name]}"`,
      );
    return n;
  };

  let width = int("width", null);
  let height = int("height", null);
  const dpr = ratio("dpr", 1, 0.05, 10);
  const scale = ratio("scale", 2, 0.1, 10);
  const quality = int("quality", 90);
  const wait = int("wait", 150, 0);
  const timeout = int("timeout", 60_000);
  const maxPixels = int("max-pixels", 64_000_000);
  if (timeout > 3_600_000) fail("--timeout must be <= 3600000 ms");
  const scheme = opts.scheme ?? null;
  if (scheme && !["dark", "light"].includes(scheme))
    fail(`--scheme accepts dark | light, got "${scheme}"`);
  const transparent = !!opts.transparent;
  const selector = opts.selector ?? null;
  const full = !!opts.full;

  const PALETTE_STEPS = [2, 4, 16, 256];
  const colors = int("colors", null, 2);
  if (colors !== null && !PALETTE_STEPS.includes(colors))
    fail(
      `--colors accepts ${PALETTE_STEPS.join(" | ")} — supported 1/2/4/8-bit CLI presets; got "${opts.colors}"`,
    );
  const palette = !!opts.palette || colors !== null;

  const style = opts.style ?? null;

  const CHANNELS = [
    "chrome",
    "chrome-beta",
    "chrome-dev",
    "msedge",
    "msedge-beta",
    "msedge-dev",
  ];
  const channel = opts.channel ?? null;
  if (channel && opts.executable)
    fail("--channel and --executable are mutually exclusive");
  if (
    opts.executable &&
    (!existsSync(resolve(opts.executable)) ||
      !statSync(resolve(opts.executable)).isFile())
  )
    fail("--executable must name an existing browser executable");
  if (channel && !CHANNELS.includes(channel))
    fail(`--channel accepts ${CHANNELS.join(" | ")}, got "${channel}"`);

  let input = inputArg;
  const isUrl = /^https?:\/\//i.test(input);
  if (opts.offline && isUrl) fail("--offline only accepts local input");
  if (isUrl) {
    try {
      new URL(input);
    } catch {
      fail("invalid HTTP(S) input URL");
    }
  }
  if (/^file:\/\//i.test(input)) {
    try {
      input = fileURLToPath(input);
    } catch (e) {
      fail(`could not read the file:// URL: ${e.message}`);
    }
  }
  if (!isUrl) {
    if (!existsSync(resolve(input))) fail(`input file not found: ${input}`);
    if (statSync(resolve(input)).isDirectory())
      fail(`input is a directory, expected an HTML file: ${input}`);
    const RASTER_IN = [
      ".png",
      ".jpg",
      ".jpeg",
      ".webp",
      ".gif",
      ".avif",
      ".tif",
      ".tiff",
      ".bmp",
      ".ico",
    ];
    const ext = extname(resolve(input)).toLowerCase();
    if (RASTER_IN.includes(ext))
      fail(
        `${basename(input)} is already a raster image — this renders HTML/SVG, and a ${ext.slice(1)} handed to it would be served as HTML and come out as mojibake. Convert it first (sharp reads png/jpeg/webp/gif/avif/tiff — not bmp or ico), or reference it from an HTML file and shoot that.`,
      );
  }
  if (opts.base && !isUrl) {
    const b = resolve(opts.base);
    if (!existsSync(b)) fail(`--base directory not found: ${opts.base}`);
    if (!statSync(b).isDirectory())
      fail(`--base is not a directory: ${opts.base}`);
  }
  if (!isUrl && sameFile(input, output))
    fail("output would overwrite the input file");
  const outDir = dirname(resolve(output));
  if (!existsSync(outDir) || !statSync(outDir).isDirectory())
    fail(`output directory does not exist: ${outDir}`);
  if (existsSync(output) && !statSync(output).isFile())
    fail("output must be a file");

  let svgBody = null;
  if (!isUrl && extname(resolve(input)).toLowerCase() === ".svg") {
    let src;
    try {
      src = readFileSync(resolve(input), "utf8");
    } catch (e) {
      fail(`could not read ${input}: ${e.message.split("\n")[0]}`);
    }
    const info = svgRootInfo(src);
    const { tag, size, hasViewBox, hasViewBoxAttr } = info;
    src = info.source;

    let markup = src;
    if (!hasViewBox) {
      if (size) {
        let withVB;
        if (hasViewBoxAttr) {
          withVB = tag.replace(
            /((?:^|[\s"'])viewBox\s*=\s*)["'][^"']*["']/i,
            `$1"0 0 ${size.w} ${size.h}"`,
          );
          warn(
            `${basename(input)} has a viewBox that cannot be read; using "0 0 ${size.w} ${size.h}" from its width/height instead. Fix the viewBox on the <svg> root.`,
          );
        } else {
          const closed = /\/>$/.test(tag);
          withVB = tag.replace(
            /\s*\/?>$/,
            ` viewBox="0 0 ${size.w} ${size.h}"${closed ? "/>" : ">"}`,
          );
        }
        markup = src.replace(tag, () => withVB);
      } else {
        warn(
          `${basename(input)} has ${hasViewBoxAttr ? "no usable viewBox" : "no viewBox"}, so its artwork cannot scale to the frame — it will sit at its authored size in the top-left corner. Add viewBox="0 0 W H" to the <svg> root.`,
        );
      }
    }

    svgBody =
      '<!doctype html><html><head><meta charset="utf-8"><style>' +
      "html,body{margin:0;padding:0;width:100%;height:100%;overflow:hidden}" +
      "body>svg{display:block;width:100%;height:100%}</style></head><body>" +
      markup +
      "</body></html>";

    if (!size) {
      if (!(width && height))
        warn(
          `${basename(input)} declares neither width/height nor a usable viewBox, so its size is unknown; ${
            width || height
              ? `the axis you did not give falls back to the default (${width ? "height 630" : "width 1200"}) — pass both --width and --height`
              : "shooting the default 1200×630 viewport — pass --width/--height"
          }`,
        );
    } else if (!width && !height) {
      width = Math.max(1, Math.round(size.w));
      height = Math.max(1, Math.round(size.h));
    } else if (width && !height)
      height = Math.max(1, Math.round((width * size.h) / size.w));
    else if (height && !width)
      width = Math.max(1, Math.round((height * size.w) / size.h));
  }
  if (svgBody && selector === null && full)
    warn(
      "--full on an SVG input is the same as the default; the wrapper is exactly one viewport",
    );

  const renderScale = Math.max(scale, dpr);

  if (isUrl && opts.base)
    warn("--base only applies to local HTML; ignored for URL input");
  if (selector && full)
    warn("--selector and --full were both given; using --selector");

  const extOut = extname(output).toLowerCase().replace(".", "");
  let fmtIn = opts.format?.toLowerCase();
  if (fmtIn === "jpg") fmtIn = "jpeg";
  const byExt = { png: "png", jpg: "jpeg", jpeg: "jpeg", webp: "webp" }[extOut];
  const format = fmtIn ?? byExt;
  if (fmtIn && !["png", "jpeg", "webp"].includes(fmtIn))
    fail(`--format accepts png | jpeg | webp, got "${opts.format}"`);
  if (!format)
    fail(
      `cannot tell the output format from "${output}" — use a .png/.jpg/.webp extension, or pass --format`,
    );
  if (quality > 100)
    fail(`--quality is an integer 1-100, got "${opts.quality}"`);
  if (opts.quality !== undefined && format === "png")
    warn("--quality only applies to jpeg/webp; png ignores it");
  if (palette && format !== "png")
    warn(
      `--palette/--colors only apply to png; ${format} ignores them (use --quality)`,
    );

  const MIME = {
    ".html": "text/html; charset=utf-8",
    ".htm": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".mjs": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".woff2": "font/woff2",
    ".woff": "font/woff",
    ".ttf": "font/ttf",
    ".otf": "font/otf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml; charset=utf-8",
    ".webp": "image/webp",
    ".avif": "image/avif",
    ".ico": "image/x-icon",
  };

  const fold = process.platform === "win32" ? (p) => p.toLowerCase() : (p) => p;

  const canonical = (p) => {
    try {
      return realpathSync.native(p);
    } catch {
      return realpathSync(p);
    }
  };

  function findPublic(startDir) {
    let d = startDir;
    for (let i = 0; i < 6; i++) {
      const cand = resolve(d, "public");
      if (existsSync(cand)) {
        try {
          const real = canonical(cand);
          if (basename(real) === "public" && statSync(real).isDirectory())
            return real;
        } catch {
          /* unreadable; keep walking */
        }
      }
      if (
        existsSync(resolve(d, "package.json")) ||
        existsSync(resolve(d, ".git"))
      )
        break;
      const up = dirname(d);
      if (up === d) break;
      d = up;
    }
    return startDir;
  }

  // --offline: the context routes every request except the local server through this
  // proxy, which refuses them all. Unlike Playwright request interception, a proxy also
  // covers workers, popups, iframes and WebSockets, and it does not make Playwright abort
  // every URL ending in /favicon.ico (its interception treats those as favicon requests).
  function blackholeProxy() {
    const proxy = createServer((_req, res) => res.destroy());
    proxy.on("connect", (_req, socket) => socket.destroy());
    proxy.on("upgrade", (_req, socket) => socket.destroy());
    const started = listenOnSafePort(proxy).then(
      () => `http://127.0.0.1:${proxy.address().port}`,
    );
    return { server: proxy, started };
  }

  function serveRoots(roots, indexFile, token, indexBody = null) {
    // One problem set for the whole render: the local server and the browser
    // context report into the same set, so a failed resource is counted once.
    const server = createServer((req, res) => {
      let urlPath;
      try {
        urlPath = decodeURIComponent(
          new URL(req.url, "http://127.0.0.1").pathname,
        );
      } catch {
        res.writeHead(400).end();
        return;
      }
      // The per-run token is the hostname (<token>.localhost), so every request from
      // this render carries it whatever its credentials mode or frame sandboxing.
      if (
        (req.headers.host || "").toLowerCase() !==
        `${token}.localhost:${server.address().port}`
      ) {
        problem(
          "403:" + urlPath,
          `${urlPath} was refused: the request did not come from this render (wrong host)`,
        );
        res.writeHead(403).end();
        return;
      }
      if (
        urlPath.split("/").some((p) => p.startsWith(".") && p !== ".well-known")
      ) {
        problem(
          "hidden:" + urlPath,
          `${urlPath} was refused: hidden files are not served`,
        );
        res.writeHead(403).end();
        return;
      }
      let file = null;
      let type = null;
      if (urlPath === "/") {
        if (indexBody !== null) {
          res
            .writeHead(200, {
              "content-type": MIME[".html"],
              "referrer-policy": "same-origin",
            })
            .end(indexBody);
          return;
        }
        file = indexFile;
        type = MIME[".html"]; // the input is HTML whatever its extension (.htm, none, ...)
      } else {
        for (const root of roots) {
          const prefix = fold(root.endsWith(sep) ? root : root + sep);
          let real;
          try {
            real = canonical(resolve(root, "." + urlPath));
          } catch {
            continue; // does not exist under this root
          }
          if (!fold(real + sep).startsWith(prefix)) continue;
          if (
            relative(root, real)
              .split(sep)
              .some((part) => part.startsWith(".") && part !== ".well-known")
          )
            continue; // escapes via /../ or a symlink
          try {
            if (!statSync(real).isFile()) continue;
          } catch {
            continue;
          }
          const onDisk = "/" + relative(root, real).split(sep).join("/");
          if (
            onDisk !== urlPath &&
            onDisk.toLowerCase() === urlPath.toLowerCase()
          )
            warn(
              `${urlPath} is spelled ${onDisk} on disk — it resolves here but will 404 on a case-sensitive filesystem (Linux/CI)`,
            );
          file = real;
          type =
            MIME[extname(real).toLowerCase()] || "application/octet-stream";
          break;
        }
      }
      if (!file) {
        if (urlPath !== "/favicon.ico")
          problem(
            "404:" + urlPath,
            `${urlPath} was requested but not found under the input's directory or --base`,
          );
        res.writeHead(404).end();
        return;
      }
      // Keep the token hostname out of Referer headers sent to other origins.
      res.writeHead(200, {
        "content-type": type,
        "referrer-policy": "same-origin",
      });
      createReadStream(file)
        .on("error", () => res.destroy())
        .pipe(res);
    });
    const started = listenOnSafePort(server).then(
      () => `http://${token}.localhost:${server.address().port}/`,
    );
    return { server, started };
  }

  const settleAnimations = (page) =>
    page
      .evaluate(() => {
        for (const a of document.getAnimations()) {
          try {
            const end = a.effect?.getComputedTiming?.().endTime;
            if (typeof end === "number" && Number.isFinite(end)) a.finish();
            else a.cancel();
          } catch {
            /* an animation that refuses to settle is left alone */
          }
        }
      })
      .catch(() => {});

  assertBudget(
    width || 1200,
    height || 630,
    renderScale,
    maxPixels,
    "viewport",
  );
  // Per-run secret for the local server, carried as the hostname <token>.localhost.
  const token = isUrl ? null : randomBytes(16).toString("hex");
  const browserStarted = Date.now();
  let browser;
  try {
    browser = await chromium.launch({
      ...(channel ? { channel } : {}),
      ...(opts.executable ? { executablePath: resolve(opts.executable) } : {}),
      // Pin *.localhost to the IPv4 listener (it would otherwise try ::1 first; a refused
      // IPv6 connect can add a delay on Windows). The rule names no token on purpose:
      // browser arguments are visible to other local users in the process list.
      ...(token
        ? { args: ["--host-resolver-rules=MAP *.localhost 127.0.0.1"] }
        : {}),
      timeout,
    });
  } catch (e) {
    if (
      /Executable doesn't exist|distribution .* is not found/i.test(e.message)
    )
      fail(
        `browser not installed; use --executable PATH / --channel chrome, or run: node "${PW_CLI}" install chromium`,
      );
    fail(`could not launch browser: ${e.message.split("\n")[0]}`);
  }
  let site = null;
  let blackhole = null;
  let shot;
  let expired = false;
  const deadline = setTimeout(
    () => {
      expired = true;
      void browser.close().catch(() => {});
    },
    Math.max(1, timeout - (Date.now() - browserStarted)),
  );
  const problems = new Set();
  // URLs that failed to load. The image check below reports images that could
  // not be decoded; an image whose request failed was already reported when it
  // failed, so it must not be counted twice.
  const failedUrls = new Set();
  const problem = (key, message) => {
    if (!problems.has(key)) {
      problems.add(key);
      warn(message);
    }
  };
  // The per-run token in the hostname is the local server's access guard, and
  // it is live for the whole render. It must not reach stderr: CI logs are
  // public, and a printed token is a printed key.
  const redact = (value) => {
    const cleaned = safeUrl(typeof value === "string" ? value : String(value));
    return token ? cleaned.split(token).join("<token>") : cleaned;
  };
  try {
    const initialViewport = { width: width || 1200, height: height || 630 };
    let target = input;
    if (!isUrl) {
      const file = resolve(input);
      const inputDir = dirname(file);
      const baseDir = opts.base ? resolve(opts.base) : findPublic(inputDir);
      const roots = (
        baseDir === inputDir ? [inputDir] : [inputDir, baseDir]
      ).map((r) => {
        try {
          return canonical(r);
        } catch {
          return r;
        }
      });
      site = serveRoots(roots, file, token, svgBody);
      target = await site.started.catch((e) =>
        fail(`could not start the local server: ${e.message}`),
      );
    }
    const local = new URL(target);
    let proxyServer = null;
    if (opts.offline) {
      blackhole = blackholeProxy();
      proxyServer = await blackhole.started.catch((e) =>
        fail(`could not start the offline proxy: ${e.message}`),
      );
    }
    // No request interception: Playwright aborts any intercepted URL ending in
    // /favicon.ico, which would break <img src="/favicon.ico">. The token is carried by
    // the hostname instead, and --offline uses a refusing proxy.
    const context = await browser.newContext({
      viewport: initialViewport,
      deviceScaleFactor: renderScale,
      ...(proxyServer
        ? { proxy: { server: proxyServer, bypass: local.host } }
        : {}),
    });
    // Same effect as Playwright's serviceWorkers: "block", whose init script reads
    // navigator.serviceWorker and so throws a page error in every sandboxed iframe.
    await context.addInitScript(() => {
      try {
        if (typeof ServiceWorkerContainer !== "undefined")
          ServiceWorkerContainer.prototype.register = async () => {
            console.warn("Service Worker registration blocked by html-shot");
          };
      } catch {
        /* nothing to block in this realm */
      }
    });
    const external = (url) => {
      if (/^(data|blob|about):/i.test(url)) return false;
      try {
        return new URL(url).origin !== local.origin;
      } catch {
        return true;
      }
    };
    context.on("response", (response) => {
      const url = response.url();
      if (response.status() < 400) return;
      if (new URL(url).pathname === "/favicon.ico") return;
      failedUrls.add(url);
      // The local server already reports its own 403/404 (with the path and the
      // reason). Reporting them again here printed the same failure twice and
      // counted it twice. Only the local server can report: with a URL input
      // `local` is the remote target, and its own failures must be reported.
      if (
        token &&
        url.startsWith(local.origin) &&
        (response.status() === 404 || response.status() === 403)
      )
        return;
      problem(url, `HTTP ${response.status()} loading ${redact(url)}`);
    });
    context.on("requestfailed", (request) => {
      if (new URL(request.url()).pathname === "/favicon.ico") return;
      failedUrls.add(request.url());
      if (opts.offline && external(request.url()))
        problem(
          request.url(),
          `offline mode blocked ${redact(request.url())}`,
        );
      else
        problem(
          request.url(),
          `request failed: ${redact(request.url())} (${request.failure()?.errorText})`,
        );
    });
    const watchSockets = (p) =>
      p.on("websocket", (socket) => {
        if (opts.offline && external(socket.url()))
          problem(
            socket.url(),
            `offline mode blocked WebSocket ${redact(socket.url())}`,
          );
      });
    context.on("page", watchSockets);
    const page = await context.newPage();
    page.setDefaultTimeout(Math.min(timeout, 30_000));
    page.setDefaultNavigationTimeout(Math.min(timeout, 30_000));
    page.on("pageerror", (error) =>
      problem(
        "script:" + error.message,
        `page JavaScript error: ${redact(error.message).split("\n")[0]}`,
      ),
    );
    await page.emulateMedia({
      reducedMotion: "reduce",
      ...(scheme ? { colorScheme: scheme } : {}),
    });

    const response = await page.goto(target, { waitUntil: "load" });
    if (response && response.status() >= 400)
      fail(
        `main document returned HTTP ${response.status()}: ${redact(target)}`,
      );
    if (style)
      await page
        .addStyleTag({ content: style })
        .catch((e) =>
          fail(`could not inject --style: ${e.message.split("\n")[0]}`),
        );
    await page
      .waitForLoadState("networkidle", { timeout: 10_000 })
      .catch(() =>
        warn("network did not go idle within 10s; capturing the page as-is"),
      );
    await page.evaluate(() => document.fonts?.ready).catch(() => {});
    if (opts["wait-for"])
      await page.locator(opts["wait-for"]).waitFor({ state: "visible" });
    if (wait) await page.waitForTimeout(wait); // let content settle before measuring
    await settleAnimations(page);

    let clip = null;
    if (!selector && !full) {
      const measure = async () => {
        await settleAnimations(page); // a viewport change can start new animations
        return page
          .evaluate(() => {
            const r = document.body.getBoundingClientRect();
            return { x: r.x, y: r.y, w: r.width, h: r.height };
          })
          .catch(() => ({ x: 0, y: 0, w: 0, h: 0 }));
      };
      const clipOf = (b) => {
        const x = width ? 0 : Math.max(0, Math.round(b.x));
        const y = height ? 0 : Math.max(0, Math.round(b.y));
        return {
          x,
          y,
          width: Math.round(width || b.w) || 1200,
          height: Math.round(height || b.h) || 630,
        };
      };

      clip = clipOf(await measure());
      let settled = false;
      for (let i = 0; i < 4; i++) {
        const vp = page.viewportSize();
        const need = {
          width: Math.max(vp.width, clip.x + clip.width),
          height: Math.max(vp.height, clip.y + clip.height),
        };
        if (need.width === vp.width && need.height === vp.height) {
          settled = true;
          break;
        }
        assertBudget(
          need.width,
          need.height,
          renderScale,
          maxPixels,
          "auto-sized viewport",
        );
        await page.setViewportSize(need);
        await page.evaluate(() => document.fonts?.ready).catch(() => {});
        clip = clipOf(await measure());
      }
      if (!settled) {
        await page.setViewportSize(initialViewport);
        await page.evaluate(() => document.fonts?.ready).catch(() => {});
        clip = {
          x: 0,
          y: 0,
          width: initialViewport.width,
          height: initialViewport.height,
        };
        warn(
          `this layout's size follows the viewport (vh/vw units or auto margins), so the automatic size cannot settle; shooting the ${initialViewport.width}×${initialViewport.height} viewport instead. Pass --width/--height for a predictable size.`,
        );
      }
      const vp = page.viewportSize();
      const x = Math.max(0, Math.min(clip.x, vp.width));
      const y = Math.max(0, Math.min(clip.y, vp.height));
      const w = Math.min(clip.width, vp.width - x);
      const h = Math.min(clip.height, vp.height - y);
      if (w < 1 || h < 1)
        fail(
          `body's box (${clip.width}×${clip.height} at ${clip.x},${clip.y}) falls outside the ${vp.width}×${vp.height} viewport, so there is nothing to capture — the layout positions it off-screen. Pass --width/--height, or use --full.`,
        );
      clip = { x, y, width: w, height: h };
      width = w;
      height = h;
    }

    if (selector) {
      const element = page.locator(selector);
      await element.waitFor({ state: "visible" });
      const box = await element.boundingBox();
      if (!box) fail(`no visible element matches --selector "${selector}"`);
      assertBudget(box.width, box.height, renderScale, maxPixels, "element");
      shot = await element.screenshot({
        omitBackground: transparent,
        animations: "disabled",
      });
    } else if (full) {
      const box = await page.evaluate(() => ({
        w: Math.max(
          innerWidth,
          document.documentElement.scrollWidth,
          document.body?.scrollWidth || 0,
        ),
        h: Math.max(
          innerHeight,
          document.documentElement.scrollHeight,
          document.body?.scrollHeight || 0,
        ),
      }));
      assertBudget(box.w, box.h, renderScale, maxPixels, "full page");
      shot = await page.screenshot({
        fullPage: true,
        omitBackground: transparent,
        animations: "disabled",
      });
    } else {
      assertBudget(clip.width, clip.height, renderScale, maxPixels, "capture");
      shot = await page.screenshot({
        clip,
        omitBackground: transparent,
        animations: "disabled",
      });
    }
    const brokenImages = await page.evaluate(() =>
      Array.from(document.images)
        .filter(
          (img) => img.currentSrc && img.complete && img.naturalWidth === 0,
        )
        .map((img) => img.currentSrc),
    );
    for (const url of brokenImages) {
      // An image that failed to load was already reported when it failed; only
      // an image that loaded and could not be decoded is new information.
      if (failedUrls.has(url)) continue;
      problem(url, `image could not decode: ${redact(url)}`);
    }
  } catch (e) {
    if (expired) fail(`render exceeded --timeout ${timeout} ms`);
    throw e;
  } finally {
    clearTimeout(deadline);
    await browser.close().catch(() => {});
    for (const server of [site?.server, blackhole?.server]) {
      if (!server) continue;
      server.closeAllConnections();
      await new Promise((ok) => server.close(ok));
    }
  }

  let pipe = sharp(shot);
  const meta = await sharp(shot).metadata();
  const target =
    !selector && !full
      ? { w: Math.round(width * dpr), h: Math.round(height * dpr) }
      : {
          w: Math.round((meta.width * dpr) / renderScale),
          h: Math.round((meta.height * dpr) / renderScale),
        };
  if (target.w < 1 || target.h < 1)
    fail(
      `--dpr ${dpr} shrinks the image below one pixel (${target.w}×${target.h}); raise it`,
    );
  if (target.w !== meta.width || target.h !== meta.height)
    pipe = pipe.resize(target.w, target.h);
  if (format === "jpeg")
    pipe = pipe.flatten({ background: "#ffffff" }).jpeg({ quality }); // jpeg has no alpha
  else if (format === "webp") pipe = pipe.webp({ quality });
  else
    pipe = pipe.png(
      palette
        ? {
            palette: true,
            colours: colors ?? 256,
            dither: 0,
            compressionLevel: 9,
          }
        : { compressionLevel: 9 },
    );
  assertBudget(target.w, target.h, 1, maxPixels, "output");
  const info = await atomicImage(pipe, output).catch((e) =>
    fail(`could not write ${output}: ${e.message.split("\n")[0]}`),
  );

  const problemCount = problems.size;
  if (problemCount) {
    log(
      `⚠ ${output}  ${info.width}×${info.height}  ${format} — written, but ${problemCount} resource/runtime issue(s) did not load (notes above)`,
    );
  } else {
    log(`✔ ${output}  ${info.width}×${info.height}  ${format}`);
  }
  return { problems: problemCount, failed: problemCount > 0 && !opts["allow-missing"] };
}

// CLI entry point. The engine above is also called in-process by icons.mjs, so
// everything that belongs to "running as a command" lives here.
async function main() {
  const args = process.argv.slice(2);
  if (args.length === 1 && ["--help", "-h"].includes(args[0])) {
    console.log(HELP);
    return;
  }
  if (args.length === 1 && args[0] === "--version") {
    console.log(skillVersion(SKILL_DIR));
    return;
  }
  const { failed } = await renderImage(args);
  if (failed) process.exitCode = 1;
}

// Only run the CLI when this file is the program that was invoked. icons.mjs
// imports renderImage from here, and importing a module must not start a render.
// realpath keeps a symlinked skill directory working; the case fold covers
// Windows drive-letter and file-name casing.
function invokedDirectly() {
  const entry = process.argv[1];
  if (!entry) return false;
  try {
    const a = realpathSync(entry);
    const b = realpathSync(fileURLToPath(import.meta.url));
    return process.platform === "win32"
      ? a.toLowerCase() === b.toLowerCase()
      : a === b;
  } catch {
    return false;
  }
}
if (invokedDirectly()) {
  main().catch((error) => {
    const message = redactToken(
      error?.message?.split("\n")[0] || String(error),
    ).replace(/https?:\/\/[^\s"'<>]+/gi, safeUrl);
    console.error(`html-shot: ${message}`);
    process.exitCode = 1;
  });
}

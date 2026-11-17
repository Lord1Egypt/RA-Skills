/** Deterministic local-only integration tests. HTML_SHOT_EXECUTABLE is optional. */
import test from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { createServer } from "node:http";
import {
  mkdtempSync,
  writeFileSync,
  readFileSync,
  mkdirSync,
  readdirSync,
  symlinkSync,
  existsSync,
  rmSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import sharp from "sharp";
import { listenOnSafePort } from "../lib.mjs";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const dir =
  process.env.HTML_SHOT_TEST_DIR ||
  mkdtempSync(join(tmpdir(), "html-shot-test-"));
mkdirSync(dir, { recursive: true });
const browser = process.env.HTML_SHOT_EXECUTABLE
  ? ["--executable", process.env.HTML_SHOT_EXECUTABLE]
  : [];
const html = (body, css = "") =>
  `<!doctype html><html lang="zh-CN"><meta charset="utf-8"><style>html,body{margin:0}body{width:160px;height:80px;background:white}${css}</style><body>${body}</body></html>`;
const fixture = (name, content) => {
  const p = join(dir, name);
  writeFileSync(p, content);
  return p;
};
const output = (name) => join(dir, name);
function run(script, args, render = true) {
  return new Promise((ok, no) => {
    const c = spawn(
      process.execPath,
      [join(ROOT, script), ...args, ...(render ? browser : [])],
      { cwd: ROOT, stdio: ["ignore", "pipe", "pipe"] },
    );
    let stdout = "",
      stderr = "";
    c.stdout.on("data", (d) => (stdout += d));
    c.stderr.on("data", (d) => (stderr += d));
    const timer = setTimeout(() => {
      c.kill("SIGKILL");
      no(new Error("CLI test exceeded 90s"));
    }, 90_000);
    c.on("error", (e) => {
      clearTimeout(timer);
      no(e);
    });
    c.on("close", (code, signal) => {
      clearTimeout(timer);
      ok({ code, signal, stdout, stderr });
    });
  });
}
const shot = (src, name, extra = []) =>
  run("render.mjs", [src, output(name), "--wait", "0", ...extra]);
const dims = async (path, w, h, format = "png") => {
  const m = await sharp(path).metadata();
  assert.deepEqual([m.width, m.height, m.format], [w, h, format]);
  return m;
};
// A refused resource still leaves an image behind for inspection, so "the render
// failed" alone does not prove the resource was blocked — sample a pixel.
const pixelAt = async (path, x, y) => {
  const buf = await sharp(path)
    .extract({ left: x, top: y, width: 1, height: 1 })
    .raw()
    .toBuffer();
  return [buf[0], buf[1], buf[2]];
};
const good = (r) => assert.equal(r.code, 0, r.stderr);
const bad = (r) => {
  assert.notEqual(r.code, 0);
  assert.doesNotMatch(r.stderr, /\n\s+at .+:\d/);
};
const outdir = (name) => {
  const p = output(name);
  mkdirSync(p, { recursive: true });
  return p;
};
// Windows creates symlinks only with Developer Mode or elevation. Those cases are
// skipped rather than failed, so the suite still means something on a stock Windows box.
function symlinkAllowed(target, link) {
  try {
    symlinkSync(target, link);
    return true;
  } catch (error) {
    if (error.code === "EPERM" || error.code === "EACCES") return false;
    throw error;
  }
}

// A directory junction needs no elevation on Windows, and Node treats the type as a
// plain symlink everywhere else — so link escapes can be exercised everywhere.
function linkDir(target, link) {
  symlinkSync(target, link, "junction");
}
const card = fixture(
  "card.html",
  html(
    '<div id="mark">中文测试 ✨</div>',
    "#mark{width:40px;height:30px;background:red}",
  ),
);
const svg = fixture(
  "mark.svg",
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="10" y="10" width="80" height="80" rx="18" fill="#2783de"/></svg>',
);

// All browser tests are local. The fixture server is never exposed beyond loopback.
let server, origin;
async function withServer(fn) {
  server = createServer((req, res) => {
    if (req.url === "/missing") {
      res.writeHead(404, { "content-type": "text/html" }).end("missing");
      return;
    }
    if (req.url === "/bad.png") {
      res.writeHead(404).end();
      return;
    }
    if (req.url === "/broken") {
      res
        .writeHead(200, { "content-type": "text/html" })
        .end(html('<img src="/bad.png">'));
      return;
    }
    if (req.url === "/hang") {
      res
        .writeHead(200, { "content-type": "text/html" })
        .write("<body>never finishes");
      return;
    }
    res
      .writeHead(200, { "content-type": "text/html; charset=utf-8" })
      .end(html("remote fixture"));
  });
  await listenOnSafePort(server);
  origin = `http://127.0.0.1:${server.address().port}`;
  try {
    await fn();
  } finally {
    server.closeAllConnections();
    await new Promise((ok) => server.close(ok));
  }
}

test("CLI help/version works without opening a browser", async () => {
  // The repository validator checks Skill metadata and lockfile consistency.
  // Installed-package tests check the public CLI output against package.json.
  const { version } = JSON.parse(
    readFileSync(join(ROOT, "package.json"), "utf8"),
  );
  for (const cli of ["render.mjs", "icons.mjs"]) {
    good(await run(cli, ["--help"], false));
    assert.equal((await run(cli, ["--version"], false)).stdout.trim(), version);
  }
});
test("HTML automatic CSS dimensions and file URLs", async () => {
  good(await shot(card, "auto.png"));
  await dims(output("auto.png"), 160, 80);
  good(await shot(pathToFileURL(card).href, "file-url.png"));
  await dims(output("file-url.png"), 160, 80);
});
test("dpr changes output; supersampling does not change dimensions", async () => {
  good(await shot(card, "retina.png", ["--dpr", "2", "--scale", "1"]));
  await dims(output("retina.png"), 320, 160);
  good(await shot(card, "sample.png", ["--scale", "3"]));
  await dims(output("sample.png"), 160, 80);
});
test("JPEG and WebP formats; JPEG transparency is white", async () => {
  const src = fixture(
    "alpha.html",
    html("", "html,body{background:transparent}"),
  );
  good(await shot(src, "white.jpg", ["--transparent"]));
  await dims(output("white.jpg"), 160, 80, "jpeg");
  const { data } = await sharp(output("white.jpg"))
    .raw()
    .toBuffer({ resolveWithObject: true });
  assert.ok(data[0] > 245 && data[1] > 245 && data[2] > 245);
  good(await shot(src, "alpha.webp", ["--transparent"]));
  assert.equal(
    (await dims(output("alpha.webp"), 160, 80, "webp")).hasAlpha,
    true,
  );
});
test("palette presets produce indexed PNG; reject unsupported count", async () => {
  good(await shot(card, "palette.png", ["--colors", "16"]));
  assert.equal(readFileSync(output("palette.png"))[25], 3);
  bad(await shot(card, "bad-palette.png", ["--colors", "64"]));
});
test("selector, injected style, and viewport-independent output", async () => {
  good(
    await shot(card, "selector.png", [
      "--selector",
      "#mark",
      "--style",
      "#mark{width:45px!important}",
      "--dpr",
      "2",
    ]),
  );
  await dims(output("selector.png"), 90, 60);
});
test("full-page output retains scroll content", async () => {
  const src = fixture(
    "long.html",
    html(
      '<div style="height:1400px;background:red"></div>',
      "body{height:auto}",
    ),
  );
  good(
    await shot(src, "full.png", [
      "--full",
      "--width",
      "200",
      "--height",
      "100",
      "--scale",
      "1",
    ]),
  );
  await dims(output("full.png"), 200, 1400);
});
test("invalid/multiple/missing selector fails cleanly and boundedly", async () => {
  bad(await shot(card, "multi.png", ["--selector", "div,body"]));
  bad(
    await shot(card, "none.png", ["--selector", "#absent", "--timeout", "900"]),
  );
});
test("SVG aspect ratio, missing viewBox repair, and invalid viewBox replacement", async () => {
  const src = fixture(
    "wide.svg",
    '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50"><rect width="100" height="50" fill="red"/></svg>',
  );
  good(await shot(src, "wide.png", ["--width", "200"]));
  await dims(output("wide.png"), 200, 100);
  const broken = fixture(
    "invalid-viewbox.svg",
    '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox=""><rect width="40" height="40" fill="red"/></svg>',
  );
  good(await shot(broken, "fixed.png", ["--width", "80"]));
  await dims(output("fixed.png"), 80, 80);
});
test("SVG ignores fake comment root and accepts sub-unit viewBox", async () => {
  const src = fixture(
    "fraction.svg",
    '<!-- <svg width="999" height="888"> --><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 .5 .5"><rect width=".5" height=".5" fill="lime"/></svg>',
  );
  good(await shot(src, "fraction.png", ["--width", "80"]));
  await dims(output("fraction.png"), 80, 80);
  const { data } = await sharp(output("fraction.png"))
    .removeAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });
  assert.ok(data[1] > 240);
});
test("nested SVG keeps authored width and height", async () => {
  const src = fixture(
    "nested.svg",
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="white"/><svg x="25" y="25" width="50" height="50" viewBox="0 0 10 10"><rect width="10" height="10" fill="red"/></svg></svg>',
  );
  good(await shot(src, "nested.png", ["--scale", "1"]));
  const { data, info } = await sharp(output("nested.png"))
    .removeAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });
  const pixel = (x, y) => [
    ...data.subarray((y * info.width + x) * 3, (y * info.width + x) * 3 + 3),
  ];
  assert.deepEqual(pixel(50, 50), [255, 0, 0]);
  assert.deepEqual(pixel(90, 90), [255, 255, 255]);
});
test("PNG transparency contains actual transparent pixels", async () => {
  good(await shot(svg, "transparent.png", ["--transparent"]));
  assert.equal(
    (await sharp(output("transparent.png")).stats()).isOpaque,
    false,
  );
});
test("missing local assets write inspectable image but fail by default", async () => {
  const src = fixture("missing.html", html('<img src="missing-asset.png">'));
  const r = await shot(src, "missing.png");
  bad(r);
  assert.equal(existsSync(output("missing.png")), true);
  // One missing asset is one problem: the local server and the browser context
  // used to report it twice, and the count said 2.
  assert.match(r.stdout, /1 resource\/runtime issue\(s\) did not load/);
  // The per-run server token is the local server's access guard; it must not
  // reach the log.
  assert.doesNotMatch(r.stderr, /https?:\/\/[a-f0-9]{16,}\.localhost/);
  good(await shot(src, "missing-allowed.png", ["--allow-missing"]));
});
test("CSS, JS modules, srcset and explicit base resolve locally", async () => {
  const base = outdir("base");
  writeFileSync(join(base, "style.css"), "body{background:rgb(1,2,3)}");
  const src = fixture(
    "base.html",
    html(
      '<link rel="stylesheet" href="/style.css"><script type="module" src="/module.mjs"></script><img srcset="/a.png 1x, /a.png 2x">',
    ),
  );
  writeFileSync(
    join(base, "module.mjs"),
    'document.body.dataset.loaded="true";',
  );
  await sharp({
    create: { width: 8, height: 8, channels: 3, background: "red" },
  })
    .png()
    .toFile(join(base, "a.png"));
  good(
    await shot(src, "base.png", [
      "--base",
      base,
      "--wait-for",
      'body[data-loaded="true"]',
    ]),
  );
});
test("root containment blocks hidden ancillary files", async () => {
  const inside = outdir("inside");
  writeFileSync(join(inside, ".env"), "secret");
  const src = join(inside, "index.html");
  writeFileSync(src, html('<img src="/.env">'));
  bad(await shot(src, "boundary.png"));
  assert.equal(existsSync(output("boundary.png")), true);
});
test("root containment blocks a directory alias escape", async () => {
  const outside = outdir("outside-dir"),
    inside = outdir("inside-dir");
  writeFileSync(join(outside, "secret.css"), "body{background:red}");
  // A junction resolves without elevation on Windows, so this escape case runs
  // everywhere instead of being skipped on a stock Windows box.
  linkDir(outside, join(inside, "escape"));
  const src = join(inside, "index.html");
  writeFileSync(src, html('<link rel="stylesheet" href="/escape/secret.css">'));
  bad(await shot(src, "escape-dir.png"));
  assert.equal(existsSync(output("escape-dir.png")), true);
  // The escaped stylesheet must not have applied — a plain 404 would fail the
  // render too, so sample the pixel the stylesheet would have painted.
  assert.notDeepEqual(
    await pixelAt(output("escape-dir.png"), 2, 2),
    [255, 0, 0],
  );
});
test("root containment blocks a file symlink escape", async (t) => {
  const outside = outdir("outside"),
    inside = outdir("inside");
  writeFileSync(join(outside, "secret.css"), "body{background:red}");
  if (!symlinkAllowed(join(outside, "secret.css"), join(inside, "escape.css")))
    return t.skip("symlink creation is not permitted on this platform");
  const src = join(inside, "index.html");
  writeFileSync(src, html('<link rel="stylesheet" href="/escape.css">'));
  bad(await shot(src, "escape.png"));
  assert.equal(existsSync(output("escape.png")), true);
  assert.notDeepEqual(await pixelAt(output("escape.png"), 2, 2), [255, 0, 0]);
});
test("HTTP main-document error is not a successful screenshot", async () =>
  withServer(async () => {
    bad(await shot(origin + "/missing", "http-404.png"));
    assert.equal(existsSync(output("http-404.png")), false);
  }));
test("HTTP failed subresources are checked, not only local files", async () =>
  withServer(async () => {
    bad(await shot(origin + "/broken", "remote-broken.png"));
    good(await shot(origin, "remote-good.png"));
  }));
test("offline blocks external origins even when they are loopback", async () =>
  withServer(async () => {
    const src = fixture(
      "offline.html",
      html(`<img src="${origin}/asset.png">`),
    );
    const r = await shot(src, "offline.png", ["--offline"]);
    bad(r);
    assert.match(r.stderr, /offline mode blocked/);
    bad(await shot(origin, "offline-url.png", ["--offline"]));
  }));
// The guarantee is that the request never leaves the browser, so this asserts on the
// server side: the loopback service must receive nothing at all. Asserting only on the
// printed note would also pass if the request went out and was blocked afterwards at the
// CORS layer. The hostnames matter: Chromium is the component most likely to exempt
// loopback destinations from the proxy, so "localhost" and "*.localhost" are probed
// alongside the 127.0.0.1 literal. The control render (no --offline) proves the probe
// can reach the service — without it a broken probe would read as a pass.
test("offline stops a page from reaching a loopback service under any hostname", async () => {
  const hits = [];
  const remote = createServer((req, res) => {
    hits.push(req.url);
    res.writeHead(200, { "content-type": "text/plain" }).end("SECRET");
  });
  await listenOnSafePort(remote);
  const port = remote.address().port;
  try {
    const src = fixture(
      "offline-hostnames.html",
      html(`<script>
        const urls = ${JSON.stringify([
          `http://127.0.0.1:${port}/hit-ip`,
          `http://localhost:${port}/hit-localhost`,
          `http://probe.localhost:${port}/hit-wildcard`,
        ])};
        Promise.allSettled(urls.map((u) => fetch(u, { mode: "no-cors" })))
          .then(() => { document.body.dataset.done = "1"; });
      </script>`),
    );
    const blocked = await shot(src, "offline-hostnames.png", [
      "--offline",
      "--wait-for",
      "body[data-done]",
    ]);
    bad(blocked);
    assert.match(blocked.stderr, /offline mode blocked/);
    assert.deepEqual(
      hits,
      [],
      "the loopback service received a request while --offline was on",
    );

    hits.length = 0;
    const control = await shot(src, "offline-hostnames-control.png", [
      "--wait-for",
      "body[data-done]",
    ]);
    good(control);
    assert.deepEqual(
      [...hits].sort(),
      ["/hit-ip", "/hit-localhost", "/hit-wildcard"],
      "the control render never reached the service — this probe proves nothing",
    );
  } finally {
    remote.closeAllConnections();
    await new Promise((ok) => remote.close(ok));
  }
});
test("total deadline terminates a stalled page load", async () =>
  withServer(async () => {
    const start = Date.now();
    const r = await shot(origin + "/hang", "hang.png", ["--timeout", "900"]);
    bad(r);
    // gstack-timing-ok: this bound proves the 900 ms --timeout terminates the process;
    // it is a liveness check, not a performance measurement.
    assert.ok(Date.now() - start < 10_000);
    assert.match(r.stderr, /timeout|Timeout/i);
  }));
test("wait-for marker and deterministic animation end state", async () => {
  const src = fixture(
    "ready.html",
    html(
      '<div id="ready" style="display:none">ready</div><script>setTimeout(()=>document.querySelector("#ready").style.display="block",120)</script>',
      "body{animation:grow 1s forwards}@keyframes grow{to{width:200px}}",
    ),
  );
  good(await shot(src, "ready.png", ["--wait-for", "#ready"]));
  await dims(output("ready.png"), 200, 80);
});
test("render limits reject oversize/invalid flags before image creation", async () => {
  for (const args of [
    ["--width", "40000"],
    ["--width", "20000", "--height", "20000"],
    ["--dpr", "NaN"],
    ["--height", "0"],
    ["--unknown"],
    ["--channel", "chrome", "--executable", process.execPath],
  ])
    bad(await shot(card, "limit.png", args));
  assert.equal(existsSync(output("limit.png")), false);
});
test("render never overwrites its input even with --format", async () => {
  const src = fixture("keep.html", html("keep"));
  const before = readFileSync(src);
  bad(await run("render.mjs", [src, src, "--format", "png"]));
  assert.deepEqual(readFileSync(src), before);
});

// Raster icon tests exercise the encoders without repeatedly launching a browser.
const raster = join(dir, "master.png"),
  tiny = join(dir, "tiny.png");
await sharp({
  create: { width: 1024, height: 1024, channels: 4, background: "#2783de80" },
})
  .png()
  .toFile(raster);
await sharp({
  create: { width: 32, height: 32, channels: 4, background: "#2783de80" },
})
  .png()
  .toFile(tiny);
const icons = (src, folder, args = []) =>
  run("icons.mjs", [src, folder, ...args], false);
function inspectIco(path) {
  const b = readFileSync(path);
  assert.equal(b.readUInt16LE(2), 1);
  const n = b.readUInt16LE(4);
  assert.ok(n > 1);
  const sizes = [];
  for (let i = 0; i < n; i++) {
    const p = 6 + 16 * i,
      w = b[p] || 256,
      h = b[p + 1] || 256,
      len = b.readUInt32LE(p + 8),
      offset = b.readUInt32LE(p + 12);
    assert.equal(w, h);
    assert.ok(offset + len <= b.length);
    sizes.push(w);
  }
  return sizes;
}
test("web preset creates ICO, SVG, opaque 180px apple icon and valid snippets", async () => {
  const folder = outdir("web");
  good(await run("icons.mjs", [svg, folder, "--wait", "0", ...browser], false));
  assert.ok(inspectIco(join(folder, "favicon.ico")).includes(256));
  assert.equal(
    readFileSync(join(folder, "favicon.svg"), "utf8"),
    readFileSync(svg, "utf8"),
  );
  const m = await dims(join(folder, "apple-touch-icon.png"), 180, 180);
  assert.equal(m.hasAlpha, false);
});
test("SVG-only passthrough accepts non-square artwork and needs no browser", async () => {
  const src = fixture(
    "wordmark.svg",
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100"/>',
  );
  good(await icons(src, outdir("svg-only"), ["--only", "svg"]));
  bad(
    await run(
      "icons.mjs",
      [src, outdir("wordmark-reject"), "--only", "ico", ...browser],
      false,
    ),
  );
});
test("raster web/PWA writes exact required sizes and purpose any", async () => {
  const folder = outdir("public/icons");
  const r = await icons(raster, folder, ["--pwa"]);
  good(r);
  await dims(join(folder, "icon-192.png"), 192, 192);
  await dims(join(folder, "icon-512.png"), 512, 512);
  assert.match(r.stdout, /\/icons\/favicon.ico/);
  assert.match(r.stdout, /"purpose":"any"/);
  assert.match(r.stdout, /"src":"\/icons\/icon-512.png"/);
});
test("Next raster fallback and SVG convention names; PWA is separate", async () => {
  const folder = outdir("next");
  good(
    await icons(raster, folder, ["--preset", "next", "--only", "svg,apple"]),
  );
  await dims(join(folder, "icon.png"), 512, 512);
  await dims(join(folder, "apple-icon.png"), 180, 180);
  bad(await icons(raster, folder, ["--preset", "next", "--pwa"]));
});
test("Electron ICO/ICNS/PNG containers and Tauri filenames", async () => {
  const folder = outdir("electron");
  good(await icons(raster, folder, ["--preset", "electron"]));
  inspectIco(join(folder, "icon.ico"));
  const b = readFileSync(join(folder, "icon.icns"));
  assert.equal(b.toString("ascii", 0, 4), "icns");
  assert.equal(b.readUInt32BE(4), b.length);
  await dims(join(folder, "icon.png"), 1024, 1024);
  const t = outdir("tauri");
  good(await icons(raster, t, ["--preset", "tauri", "--only", "png"]));
  await dims(join(t, "32x32.png"), 32, 32);
  await dims(join(t, "128x128.png"), 128, 128);
  await dims(join(t, "128x128@2x.png"), 256, 256);
});
test("undersized input fails without modifying existing output; opt-in upscales exactly", async () => {
  const folder = outdir("small-input");
  writeFileSync(join(folder, "favicon.ico"), "original");
  bad(await icons(tiny, folder, ["--pwa"]));
  assert.equal(readFileSync(join(folder, "favicon.ico"), "utf8"), "original");
  assert.equal(
    readdirSync(folder).some((n) => n.startsWith(".html-shot-")),
    false,
  );
  good(await icons(tiny, folder, ["--only", "pwa", "--allow-upscale"]));
  await dims(join(folder, "icon-512.png"), 512, 512);
});
test("simplified ICO uses alternate mark for 16/32 entries", async () => {
  const folder = outdir("small-mark");
  good(await icons(raster, folder, ["--only", "ico", "--small", tiny]));
  assert.deepEqual(
    inspectIco(join(folder, "favicon.ico")),
    [16, 32, 48, 64, 128, 256],
  );
});
test("invalid bg/options and impossible output selection fail cleanly", async () => {
  const folder = outdir("invalid-icons");
  for (const args of [
    ["--bg", "transparent"],
    ["--bg", "#fff0"],
    ["--bg", "wihte"],
    ["--preset", "electron", "--pwa"],
    ["--only", "svg"],
    ["--only", "bad"],
    ["--only", "apple", "--small", tiny],
    ["--url-prefix", "https://bad"],
  ])
    bad(await icons(raster, folder, args));
  assert.deepEqual(readdirSync(folder), []);
});
test("commit preflight leaves prior outputs intact if a target is a directory", async () => {
  const folder = outdir("transaction");
  writeFileSync(join(folder, "favicon.ico"), "keep");
  mkdirSync(join(folder, "apple-touch-icon.png"));
  bad(await icons(raster, folder));
  assert.equal(readFileSync(join(folder, "favicon.ico"), "utf8"), "keep");
  assert.equal(
    readdirSync(folder).some((n) => n.startsWith(".html-shot-")),
    false,
  );
});
test("custom URL prefix overrides filesystem convention and encodes spaces", async () => {
  const folder = outdir("url-prefix");
  const r = await icons(raster, folder, [
    "--only",
    "ico,pwa",
    "--url-prefix",
    "/my icons",
  ]);
  good(r);
  assert.match(r.stdout, /\/my%20icons\/favicon.ico/);
  assert.match(r.stdout, /\/my%20icons\/icon-192.png/);
});
test("paths with spaces and non-ASCII characters work", async () => {
  // Windows paths routinely carry both, and the local server has to survive them.
  const folder = outdir("中文 目录 with spaces");
  const src = join(folder, "卡片 页面.html");
  writeFileSync(src, html('<div id="box">中文与 emoji ✨</div>'));
  good(await shot(src, "space-path.png"));
  await dims(output("space-path.png"), 160, 80);
});

test("file URL raster source and source collision protection", async () => {
  good(
    await icons(pathToFileURL(raster).href, outdir("file-icons"), [
      "--only",
      "apple",
    ]),
  );
  const folder = outdir("collision"),
    src = join(folder, "icon.png");
  writeFileSync(src, readFileSync(raster));
  const before = readFileSync(src);
  bad(await icons(src, folder, ["--preset", "electron", "--only", "png"]));
  assert.deepEqual(readFileSync(src), before);
});

test("format override is honoured and single-image temp files are cleaned", async () => {
  good(await shot(card, "override.data", ["--format", "webp"]));
  await dims(output("override.data"), 160, 80, "webp");
  assert.equal(
    readdirSync(dir).some(
      (n) => n.includes(".html-shot-") && n.endsWith(".tmp"),
    ),
    false,
  );
});
test("page script and undecodable image errors cannot silently ship", async () => {
  const script = fixture(
    "script-error.html",
    html('<script>throw new Error("fixture-error")</script>'),
  );
  bad(await shot(script, "script-error.png"));
  const img = fixture("not-image.png", "this is not a PNG");
  const src = fixture("broken-decoder.html", html('<img src="not-image.png">'));
  const r = await shot(src, "broken-decoder.png");
  bad(r);
  assert.match(r.stderr, /could not decode/);
});
test("page errors do not print the per-run server token", async () => {
  const src = fixture(
    "token-error.html",
    html('<script>throw new Error(location.href)</script>'),
  );
  const r = await shot(src, "token-error.png");
  bad(r);
  assert.doesNotMatch(r.stderr, /https?:\/\/[a-f0-9]{32}\.localhost/);
  assert.match(r.stderr, /<token>\.localhost/);
});
test("offline closes WebSockets without connecting to the external server", async () => {
  let upgrades = 0;
  const wsServer = createServer();
  wsServer.on("upgrade", (_req, socket) => {
    upgrades++;
    socket.destroy();
  });
  await listenOnSafePort(wsServer);
  const port = wsServer.address().port;
  try {
    const src = fixture(
      "socket.html",
      html(
        `<script>const s=new WebSocket('ws://127.0.0.1:${port}/');s.onclose=()=>document.body.dataset.ready='yes';</script>`,
      ),
    );
    const r = await shot(src, "socket.png", [
      "--offline",
      "--wait-for",
      'body[data-ready="yes"]',
    ]);
    bad(r);
    assert.match(r.stderr, /blocked WebSocket/);
    assert.equal(upgrades, 0);
  } finally {
    wsServer.closeAllConnections();
    await new Promise((ok) => wsServer.close(ok));
  }
});
test("browser renders the bundled responsive icon example at exact master size", async () => {
  const name = "bundled-icon.png";
  good(
    await shot(join(ROOT, "icon.example.html"), name, [
      "--width",
      "1024",
      "--height",
      "1024",
      "--transparent",
    ]),
  );
  await dims(output(name), 1024, 1024);
  assert.equal((await sharp(output(name)).stats()).isOpaque, false);
});
test("image inspector reports actual opacity and rejects missing files", async () => {
  const fixturePath = output("inspector-alpha.png");
  await sharp({
    create: { width: 8, height: 8, channels: 4, background: "#00000000" },
  })
    .png()
    .toFile(fixturePath);
  const r = await run("inspect.mjs", [fixturePath], false);
  good(r);
  assert.equal(JSON.parse(r.stdout).opaque, false);
  bad(await run("inspect.mjs", [output("does-not-exist.png")], false));
});
test("icons reject invalid forwarded numeric options even for raster sources", async () => {
  const folder = outdir("invalid-numeric");
  for (const args of [
    ["--scale", "bad"],
    ["--wait", "-1"],
    ["--timeout", "0"],
    ["--max-pixels", "NaN"],
  ])
    bad(await icons(raster, folder, args));
  assert.deepEqual(readdirSync(folder), []);
});

test("offline context routing covers the first request of a popup", async () => {
  let hits = 0;
  const remote = createServer((_req, res) => {
    hits++;
    res.end("external");
  });
  await listenOnSafePort(remote);
  try {
    const src = fixture(
      "popup.html",
      html(
        `<script>window.open('http://127.0.0.1:${remote.address().port}/popup');</script>`,
      ),
    );
    const r = await shot(src, "popup.png", ["--offline"]);
    bad(r);
    assert.match(r.stderr, /offline mode blocked/);
    assert.equal(hits, 0);
  } finally {
    remote.closeAllConnections();
    await new Promise((ok) => remote.close(ok));
  }
});
test("oversized raster master is normalised for exact desktop outputs", async () => {
  const src = output("large-master.png");
  await sharp({
    create: { width: 1600, height: 1600, channels: 4, background: "red" },
  })
    .png()
    .toFile(src);
  const folder = outdir("large-icons");
  good(await icons(src, folder, ["--preset", "electron", "--only", "png"]));
  await dims(join(folder, "icon.png"), 1024, 1024);
});

test("hidden files cannot be served through a non-hidden symlink alias", async (t) => {
  const folder = outdir("hidden-alias");
  writeFileSync(join(folder, ".secret.css"), "body{background:red}");
  if (
    !symlinkAllowed(
      join(folder, ".secret.css"),
      join(folder, "public-name.css"),
    )
  )
    return t.skip("symlink creation is not permitted on this platform");
  const src = join(folder, "index.html");
  writeFileSync(src, html('<link rel="stylesheet" href="public-name.css">'));
  const r = await shot(src, "hidden-alias.png");
  bad(r);
  assert.match(r.stderr, /not found|HTTP 4/);
});
test.after(() => {
  if (!process.env.HTML_SHOT_TEST_DIR)
    rmSync(dir, { recursive: true, force: true });
});

// Playwright request interception aborts every URL ending in /favicon.ico. The renderer
// therefore must not intercept: such an image has to render, and a missing one has to fail.
test("an <img> named favicon.ico renders, at the root and in a subfolder", async () => {
  const folder = outdir("favicon-img");
  const red = await sharp({
    create: { width: 16, height: 16, channels: 4, background: "#ff0000" },
  })
    .png()
    .toBuffer();
  mkdirSync(join(folder, "assets"), { recursive: true });
  writeFileSync(join(folder, "favicon.ico"), red);
  writeFileSync(join(folder, "assets", "favicon.ico"), red);
  const src = join(folder, "index.html");
  writeFileSync(
    src,
    html(
      '<img src="/favicon.ico" style="position:absolute;left:0;top:0;width:40px;height:40px">' +
        '<img src="assets/favicon.ico" style="position:absolute;left:80px;top:0;width:40px;height:40px">',
    ),
  );
  good(await shot(src, "favicon-img.png"));
  assert.deepEqual(
    await pixelAt(output("favicon-img.png"), 20, 20),
    [255, 0, 0],
  );
  assert.deepEqual(
    await pixelAt(output("favicon-img.png"), 100, 20),
    [255, 0, 0],
  );
  good(await shot(src, "favicon-img-offline.png", ["--offline"]));
  assert.deepEqual(
    await pixelAt(output("favicon-img-offline.png"), 20, 20),
    [255, 0, 0],
  );
});
test("a missing <img> named favicon.ico is still reported", async () => {
  const folder = outdir("favicon-missing");
  const src = join(folder, "index.html");
  writeFileSync(
    src,
    html('<img src="assets/favicon.ico" width="20" height="20">'),
  );
  const r = await shot(src, "favicon-missing.png");
  bad(r);
  assert.match(r.stderr, /favicon\.ico/);
});
test("credential-less fetches and sandboxed iframes still reach local files", async () => {
  const folder = outdir("token-host");
  await sharp({
    create: { width: 8, height: 8, channels: 3, background: "#ff0000" },
  })
    .png()
    .toFile(join(folder, "red.png"));
  writeFileSync(
    join(folder, "frame.html"),
    '<!doctype html><body style="margin:0"><img src="red.png" style="width:40px;height:40px">',
  );
  const src = join(folder, "index.html");
  writeFileSync(
    src,
    html(
      `<iframe sandbox src="frame.html" style="border:0;width:40px;height:40px"></iframe><script>fetch('frame.html',{credentials:'omit'}).then(r=>document.body.dataset.status=r.status)</script>`,
    ),
  );
  const r = await shot(src, "token-host.png", [
    "--wait-for",
    'body[data-status="200"]',
  ]);
  good(r);
  assert.deepEqual(
    await pixelAt(output("token-host.png"), 20, 20),
    [255, 0, 0],
  );
});
test("the local server refuses requests that lack the per-run host", async () => {
  const src = fixture(
    "wrong-host.html",
    html(
      `<script>fetch('http://127.0.0.1:'+location.port+'/wrong-host.html',{mode:'no-cors'}).finally(()=>document.body.dataset.done='1')</script>`,
    ),
  );
  const r = await shot(src, "wrong-host.png", [
    "--wait-for",
    "body[data-done]",
  ]);
  bad(r);
  assert.match(r.stderr, /refused: the request did not come from this render/);
});
test("offline blocks requests from an iframe and a dedicated worker", async () => {
  let hits = 0;
  const remote = createServer((_req, res) => {
    hits++;
    res.end("external");
  });
  await listenOnSafePort(remote);
  try {
    const url = `http://127.0.0.1:${remote.address().port}`;
    const folder = outdir("offline-frames");
    writeFileSync(
      join(folder, "worker.js"),
      `fetch('${url}/from-worker').catch(()=>{}).finally(()=>postMessage('done'))`,
    );
    const src = join(folder, "index.html");
    writeFileSync(
      src,
      html(
        `<iframe src="${url}/frame"></iframe><script>const w=new Worker('worker.js');w.onmessage=()=>document.body.dataset.ready='yes'</script>`,
      ),
    );
    const r = await shot(src, "offline-frames.png", [
      "--offline",
      "--wait-for",
      'body[data-ready="yes"]',
    ]);
    bad(r);
    assert.match(r.stderr, /offline mode blocked/);
    assert.equal(hits, 0);
  } finally {
    remote.closeAllConnections();
    await new Promise((ok) => remote.close(ok));
  }
});
test("service workers stay blocked without breaking sandboxed iframes", async () => {
  const folder = outdir("service-worker");
  writeFileSync(join(folder, "sw.js"), "self.addEventListener('fetch',()=>{})");
  writeFileSync(join(folder, "frame.html"), "<!doctype html><p>framed</p>");
  const src = join(folder, "index.html");
  writeFileSync(
    src,
    html(
      `<iframe sandbox src="frame.html"></iframe><script>navigator.serviceWorker.register('sw.js').then(()=>navigator.serviceWorker.getRegistrations()).then(r=>document.body.dataset.registrations=r.length)</script>`,
    ),
  );
  const r = await shot(src, "service-worker.png", [
    "--wait-for",
    'body[data-registrations="0"]',
  ]);
  good(r);
  assert.doesNotMatch(r.stderr, /serviceWorker/);
});

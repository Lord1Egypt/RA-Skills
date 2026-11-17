#!/usr/bin/env node
/** Build platform-specific icon sets. See references/icons.md. */
import {
  existsSync,
  statSync,
  readFileSync,
  writeFileSync,
  mkdirSync,
  rmSync,
  copyFileSync,
  mkdtempSync,
  renameSync,
} from "node:fs";
import { dirname, resolve, extname, join, basename } from "node:path";
import { fileURLToPath } from "node:url";
import { svgRootInfo, sameFile, assertBudget, safeUrl, skillVersion } from "./lib.mjs";
import { renderImage, redactToken } from "./render.mjs";

const HELP = `html-shot icons — build a favicon/app icon set
Usage: node icons.mjs <source.svg|html|png|url> <existing-outdir> [options]
  --preset web|docusaurus|next|electron|tauri (default: web)
  --only ico,svg,apple,pwa  Web outputs; app outputs: ico,icns,png
  --pwa --bg COLOR --small SOURCE
  --allow-upscale         Explicitly allow undersized raster sources
  --url-prefix /PATH      Public URL directory for printed HTML/manifest snippets
  --scale N --wait MS --base DIR --style CSS --channel C --executable PATH
  --timeout MS --max-pixels N --wait-for CSS --offline  Forwarded to renderer
  --help | --version
Existing target files are replaced only after all generation succeeds.
See references/icons.md for size requirements and platform limitations.`;
const args = process.argv.slice(2);
if (args.length === 1 && ["--help", "-h"].includes(args[0])) {
  console.log(HELP);
  process.exit(0);
}
if (args.length === 1 && args[0] === "--version") {
  console.log(skillVersion(dirname(fileURLToPath(import.meta.url))));
  process.exit(0);
}
async function main() {
  const [major, minor] = process.versions.node.split(".").map(Number);
  if (major < 20 || (major === 20 && minor < 9))
    throw new Error("requires Node >=20.9");
  const SKILL_DIR = dirname(fileURLToPath(import.meta.url));

  let sharp, png2icons;
  function fail(msg) {
    throw new Error(msg);
  }
  const warn = (msg) => console.error(`html-shot/icons: note — ${msg}`);

  let [source, outDirArg, ...rest] = process.argv.slice(2);
  if (/^file:\/\//i.test(source || "")) source = fileURLToPath(source);
  if (!source || !outDirArg) fail("missing <source> or <outdir>; use --help");
  const isUrl = /^https?:\/\//i.test(source);
  const srcExt = isUrl ? "" : extname(resolve(source)).toLowerCase();

  const VALUE_FLAGS = new Set([
    "preset",
    "only",
    "bg",
    "small",
    "scale",
    "wait",
    "base",
    "style",
    "channel",
    "executable",
    "timeout",
    "max-pixels",
    "wait-for",
    "url-prefix",
  ]);
  const BOOL_FLAGS = new Set(["pwa", "allow-upscale", "offline"]);
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

  for (const name of ["wait", "timeout", "max-pixels"]) {
    if (opts[name] === undefined) continue;
    const n = Number(opts[name]);
    if (
      !Number.isSafeInteger(n) ||
      n < (name === "wait" ? 0 : 1) ||
      (name === "timeout" && n > 3_600_000)
    )
      fail(`invalid --${name}: ${opts[name]}`);
  }
  if (
    opts.scale !== undefined &&
    (!Number.isFinite(Number(opts.scale)) ||
      Number(opts.scale) < 0.1 ||
      Number(opts.scale) > 10)
  )
    fail("--scale must be between 0.1 and 10");
  if (opts.channel && opts.executable)
    fail("--channel and --executable are mutually exclusive");

  const PRESETS = {
    web: {
      kind: "web",
      ico: "favicon.ico",
      svg: "favicon.svg",
      apple: "apple-touch-icon.png",
    },
    docusaurus: {
      kind: "web",
      ico: "favicon.ico",
      svg: "favicon.svg",
      apple: "apple-touch-icon.png",
    },
    next: {
      kind: "web",
      ico: "favicon.ico",
      svg: "icon.svg",
      svgFallback: ["icon.png", 512],
      apple: "apple-icon.png",
    },
    electron: {
      kind: "app",
      ico: "icon.ico",
      icns: "icon.icns",
      png: [["icon.png", 1024]],
    },
    tauri: {
      kind: "app",
      ico: "icon.ico",
      icns: "icon.icns",
      png: [
        ["icon.png", 1024],
        ["32x32.png", 32],
        ["128x128.png", 128],
        ["128x128@2x.png", 256],
      ],
    },
  };
  const presetName = opts.preset ?? "web";
  const preset = PRESETS[presetName];
  if (!preset)
    fail(
      `--preset accepts ${Object.keys(PRESETS).join(" | ")}, got "${presetName}"`,
    );
  if (opts.pwa && preset.kind !== "web")
    fail(
      `--pwa applies to the web presets; --preset ${presetName} builds desktop app icons`,
    );

  const CAPS =
    preset.kind === "web"
      ? ["ico", "svg", "apple", "pwa"]
      : ["ico", "icns", "png"];
  let want;
  if (opts.only !== undefined) {
    want = new Set(
      opts.only
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean),
    );
    if (!want.size) fail("--only needs at least one of " + CAPS.join(","));
    for (const k of want)
      if (!CAPS.includes(k))
        fail(
          `--only accepts ${CAPS.join(",")} for --preset ${presetName}, got "${k}"`,
        );
  } else {
    want = new Set(CAPS.filter((k) => k !== "pwa")); // pwa is always opt-in
  }
  if (opts.pwa) want.add("pwa");

  if (want.has("pwa") && presetName === "next")
    fail(
      `the PWA pair cannot share an output directory with --preset next: these two files belong in public/, but the next preset writes App Router convention names into app/. Build them separately:\n  node icons.mjs ${source} public --only pwa`,
    );

  if (
    ["ico", "icns", "png", "apple", "pwa"].some((k) => want.has(k)) ||
    (want.has("svg") && preset.svgFallback && srcExt !== ".svg")
  ) {
    try {
      ({ default: sharp } = await import("sharp"));
    } catch (e) {
      fail(
        `sharp unavailable (${e.code || e.message}); run npm ci in the skill directory`,
      );
    }
  }
  if (want.has("ico") || want.has("icns")) {
    try {
      png2icons = await import("png2icons");
    } catch (e) {
      fail(
        `png2icons unavailable (${e.code || e.message}); run npm ci in the skill directory`,
      );
    }
  }
  if (
    opts["url-prefix"] !== undefined &&
    (!opts["url-prefix"].startsWith("/") ||
      opts["url-prefix"].startsWith("//") ||
      /[?#\\]/.test(opts["url-prefix"]))
  )
    fail(
      "--url-prefix must be an absolute site path such as / or /assets/icons (no query/hash)",
    );
  const bg = opts.bg ?? "#ffffff";
  if (opts.bg) {
    if (!preset.apple)
      fail(
        `--bg only affects the apple-touch icon, which --preset ${presetName} does not build`,
      );
    if (!want.has("apple"))
      fail(
        `--bg only affects the apple-touch icon, which --only ${opts.only} leaves out`,
      );
    if (
      !/^(#([0-9a-f]{3}|[0-9a-f]{4}|[0-9a-f]{6}|[0-9a-f]{8})|[a-z]+)$/i.test(bg)
    )
      fail(
        `--bg should be a CSS colour name or #rgb / #rgba / #rrggbb / #rrggbbaa, got "${bg}"`,
      );
    const bgAlpha = /^transparent$/i.test(bg)
      ? 0
      : /^#[0-9a-f]{4}$/i.test(bg)
        ? parseInt(bg[4] + bg[4], 16)
        : /^#[0-9a-f]{8}$/i.test(bg)
          ? parseInt(bg.slice(7), 16)
          : 255;
    if (bgAlpha < 255)
      fail(
        `--bg ${bg} is see-through, but the apple-touch icon has to be opaque — iOS composites alpha onto black, so this would ship a black icon. Pass an opaque colour.`,
      );
    try {
      await sharp({
        create: { width: 1, height: 1, channels: 4, background: bg },
      })
        .png()
        .toBuffer();
    } catch {
      fail(
        `--bg "${bg}" is not a colour sharp can parse — use a CSS colour name or a hex value`,
      );
    }
  }

  const outDir = resolve(outDirArg);
  if (!existsSync(outDir)) fail(`output directory does not exist: ${outDir}`);
  if (!statSync(outDir).isDirectory())
    fail(`output path is not a directory: ${outDir}`);

  if (!isUrl && !existsSync(resolve(source)))
    fail(`source not found: ${source}`);
  if (!isUrl && !statSync(resolve(source)).isFile())
    fail("source must be a file");
  if (opts.offline && isUrl) fail("--offline only accepts local input");
  if (srcExt === ".svg") svgRootInfo(readFileSync(resolve(source), "utf8"));
  if (opts.small) {
    if (/^file:\/\//i.test(opts.small)) opts.small = fileURLToPath(opts.small);
    if (
      !existsSync(resolve(opts.small)) ||
      !statSync(resolve(opts.small)).isFile()
    )
      fail(`--small source not found: ${opts.small}`);
    if (!preset.ico)
      fail(
        `--small only affects the .ico, which --preset ${presetName} does not build`,
      );
    if (!want.has("ico"))
      fail(
        `--small only affects the .ico, which --only ${opts.only} leaves out`,
      );
  }

  const MASTER = 1024;
  const tmp = mkdtempSync(join(outDir, ".html-shot-"));
  const stage = join(tmp, "stage");
  mkdirSync(stage);
  let preserveTmp = false;
  const cleanup = () => {
    if (preserveTmp) return;
    try {
      rmSync(tmp, { recursive: true, force: true });
    } catch {}
  };
  process.on("exit", cleanup);
  const written = [];
  const pwaWritten = [];

  const RASTER = new Set([
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".avif",
    ".tif",
    ".tiff",
  ]);

  const UNDECODABLE = new Set([".bmp", ".ico"]);

  async function makeMaster(src, outPath) {
    const ext = /^https?:\/\//i.test(src)
      ? ""
      : extname(resolve(src)).toLowerCase();
    if (UNDECODABLE.has(ext))
      fail(
        `${basename(src)} is a ${ext} file, which nothing in this pipeline can decode — export the artwork as SVG (best, it stays crisp at every size) or as a PNG at 1024×1024, and pass that`,
      );
    if (RASTER.has(ext)) {
      const m = await sharp(resolve(src)).metadata();
      // The flag loop above already bounds --max-pixels to a safe integer >= 1,
      // so there is nothing left to re-check here.
      const maxPixels = Number(opts["max-pixels"] ?? 64_000_000);
      assertBudget(m.width, m.height, 1, maxPixels, "raster source");
      if (m.width !== m.height)
        fail(
          `${basename(src)} is ${m.width}×${m.height}; an icon master must be square`,
        );
      if (m.width < MASTER)
        warn(
          `${basename(src)} is ${m.width}×${m.width}; ${MASTER}×${MASTER} or larger keeps the big icons sharp`,
        );
      await sharp(resolve(src))
        .rotate()
        .resize(MASTER, MASTER, { withoutEnlargement: true })
        .toColourspace("srgb")
        .png({ compressionLevel: 9 })
        .toFile(outPath);
    } else {
      if (ext === ".svg") {
        const a = svgRootInfo(readFileSync(resolve(src), "utf8")).size;
        if (!a)
          fail(
            `${basename(src)} declares no usable width/height and no viewBox, so it cannot be scaled to a square icon frame — add viewBox="0 0 W H" to the <svg> root`,
          );
        if (Math.abs(a.w - a.h) > Math.max(a.w, a.h) * 1e-6)
          fail(
            `${basename(src)} is ${a.w}×${a.h}; an icon master must be square — pad the artwork to a square viewBox`,
          );
      }
      const args = [
        src,
        outPath,
        "--width",
        String(MASTER),
        "--height",
        String(MASTER),
        "--transparent",
      ];
      for (const f of [
        "scale",
        "wait",
        "base",
        "style",
        "channel",
        "executable",
        "timeout",
        "max-pixels",
        "wait-for",
      ])
        if (opts[f] !== undefined) args.push(`--${f}`, opts[f]);
      if (opts.offline) args.push("--offline");
      // The same engine the render CLI runs, called in-process. Its result line
      // goes nowhere (the icon set prints its own summary) and its notes stay on
      // stderr, exactly as they did when this ran as a child process.
      //
      // The flag loop above bounds --timeout to [1, 3_600_000], so the budget
      // below is always inside the range and never needs a second check. The
      // engine's own deadline closes the browser at --timeout; this backstop
      // covers the encoding work that follows it.
      const budget = Number(opts.timeout ?? 60_000) + 15_000;
      let watchdog;
      const overran = new Promise((_, reject) => {
        watchdog = setTimeout(
          () => reject(new Error(`the render did not finish within ${budget} ms`)),
          budget,
        );
      });
      let result;
      try {
        result = await Promise.race([
          renderImage(args, { log: () => {} }),
          overran,
        ]);
      } catch (e) {
        // The render CLI redacts the per-run server token and URL credentials
        // before printing an error; do the same here, because this message is
        // printed by icons.mjs.
        const detail = redactToken(
          e?.message?.split("\n")[0] || String(e),
        ).replace(/https?:\/\/[^\s"'<>]+/gi, safeUrl);
        fail(`rendering ${basename(src)} failed: ${detail}`);
      } finally {
        clearTimeout(watchdog);
      }
      if (result.failed || !existsSync(outPath))
        fail(`rendering ${basename(src)} failed — see the notes above`);
    }
    return readFileSync(outPath);
  }

  function packIco(entries) {
    const header = Buffer.alloc(6);
    header.writeUInt16LE(0, 0); // reserved
    header.writeUInt16LE(1, 2); // type: icon
    header.writeUInt16LE(entries.length, 4);
    const dir = Buffer.alloc(16 * entries.length);
    let offset = 6 + 16 * entries.length;
    entries.forEach(({ size, buf }, i) => {
      const e = i * 16;
      dir.writeUInt8(size >= 256 ? 0 : size, e + 0); // 0 means 256
      dir.writeUInt8(size >= 256 ? 0 : size, e + 1);
      dir.writeUInt8(0, e + 2); // palette entries
      dir.writeUInt8(0, e + 3); // reserved
      dir.writeUInt16LE(1, e + 4); // colour planes
      dir.writeUInt16LE(32, e + 6); // bits per pixel
      dir.writeUInt32LE(buf.length, e + 8);
      dir.writeUInt32LE(offset, e + 12);
      offset += buf.length;
    });
    return Buffer.concat([header, dir, ...entries.map((e) => e.buf)]);
  }

  const needsMaster =
    want.has("ico") ||
    want.has("icns") ||
    want.has("png") ||
    want.has("apple") ||
    want.has("pwa") ||
    (want.has("svg") && srcExt !== ".svg" && !!preset.svgFallback);

  try {
    const masterBuf = needsMaster
      ? await makeMaster(source, join(tmp, "master.png"))
      : null;
    const smallBuf = opts.small
      ? await makeMaster(opts.small, join(tmp, "small.png"))
      : null;
    const masterMeta = masterBuf ? await sharp(masterBuf).metadata() : null;

    const out = (name) => join(stage, name);
    const requestedSize = Math.max(
      want.has("ico") ? 256 : 0,
      want.has("icns") ? 1024 : 0,
      want.has("apple") ? 180 : 0,
      want.has("pwa") ? 512 : 0,
      want.has("png") ? Math.max(...(preset.png || []).map((x) => x[1])) : 0,
      want.has("svg") && srcExt !== ".svg" && preset.svgFallback
        ? preset.svgFallback[1]
        : 0,
    );
    if (
      masterMeta &&
      masterMeta.width < requestedSize &&
      !opts["allow-upscale"]
    )
      fail(
        `source is ${masterMeta.width}×${masterMeta.height}; selected outputs require at least ${requestedSize}×${requestedSize}. Provide a larger source, choose fewer outputs, or explicitly use --allow-upscale`,
      );
    if (
      smallBuf &&
      (await sharp(smallBuf).metadata()).width < 32 &&
      !opts["allow-upscale"]
    )
      fail("--small requires at least 32×32 pixels, or --allow-upscale");
    if (masterMeta && masterMeta.width < requestedSize)
      warn(
        `--allow-upscale: interpolating ${masterMeta.width}px source for ${requestedSize}px outputs; this cannot restore detail`,
      );
    const note = (name, extra = "") =>
      written.push(`  ${name}${extra ? "  " + extra : ""}`);

    if (preset.ico && want.has("ico")) {
      let ico, how;
      if (smallBuf) {
        const png = (buf, size) =>
          sharp(buf).resize(size, size).png({ compressionLevel: 9 }).toBuffer();
        const entries = [
          { size: 16, buf: await png(smallBuf, 16) },
          { size: 32, buf: await png(smallBuf, 32) },
          { size: 48, buf: await png(masterBuf, 48) },
          { size: 64, buf: await png(masterBuf, 64) },
          { size: 128, buf: await png(masterBuf, 128) },
          { size: 256, buf: await png(masterBuf, 256) },
        ];
        ico = packIco(entries);
        how = `16/32 from ${basename(opts.small)}, 48+ from the main mark`;
        if (preset.kind === "app")
          warn(
            `--small packs the .ico with PNG entries; for an icon embedded in a Windows executable, the BMP entries the default path writes render more reliably on Windows before 10`,
          );
      } else {
        ico = png2icons.createICO(
          masterBuf,
          png2icons.BICUBIC2,
          0,
          false,
          true,
        );
        how = "";
      }
      if (!ico) fail("could not build the .ico");
      writeFileSync(out(preset.ico), ico);
      note(
        preset.ico,
        `${(ico.length / 1024).toFixed(1)} KB${how ? " — " + how : ""}`,
      );
    }

    if (preset.icns && want.has("icns")) {
      const icns = png2icons.createICNS(masterBuf, png2icons.BICUBIC2, 0);
      if (!icns) fail("png2icons could not build the .icns");
      writeFileSync(out(preset.icns), icns);
      note(preset.icns, `${(icns.length / 1024).toFixed(1)} KB`);
    }

    for (const [name, size] of want.has("png") ? (preset.png ?? []) : []) {
      const target = size;
      const buf =
        target === masterMeta.width
          ? masterBuf
          : await sharp(masterBuf)
              .resize(target, target)
              .png({ compressionLevel: 9 })
              .toBuffer();
      writeFileSync(out(name), buf);
      note(name, `${target}×${target}`);
    }

    if (preset.apple && want.has("apple")) {
      const target = 180;
      const buf = await sharp(masterBuf)
        .resize(target, target)
        .flatten({ background: bg })
        .removeAlpha()
        .png({ compressionLevel: 9 })
        .toBuffer();
      writeFileSync(out(preset.apple), buf);
      note(preset.apple, `${target}×${target} opaque on ${bg}`);
      if (!opts.bg && !(await sharp(masterBuf).stats()).isOpaque)
        warn(
          `${preset.apple} was flattened onto the default #ffffff — if the mark has rounded corners, pass --bg with its own fill so the corners disappear under iOS's mask`,
        );
    }

    if (preset.svg && want.has("svg")) {
      if (srcExt === ".svg") {
        copyFileSync(resolve(source), out(preset.svg));
        note(preset.svg, "passed through from the source");
      } else if (preset.svgFallback) {
        const [name, size] = preset.svgFallback;
        const target = size;
        writeFileSync(
          out(name),
          await sharp(masterBuf)
            .resize(target, target)
            .png({ compressionLevel: 9 })
            .toBuffer(),
        );
        note(
          name,
          `${target}×${target} — the source is not a vector, so this stands in for ${preset.svg}`,
        );
      } else {
        warn(
          `no ${preset.svg} written: the source is not an SVG, and wrapping a raster in one would be larger than the PNG and still not scale`,
        );
      }
    }

    if (want.has("pwa")) {
      for (const size of [192, 512]) {
        const name = `icon-${size}.png`;
        const target = size;
        writeFileSync(
          out(name),
          await sharp(masterBuf)
            .resize(target, target)
            .png({ compressionLevel: 9 })
            .toBuffer(),
        );
        note(name, `${target}×${target}`);
        pwaWritten.push({ name, target });
      }
    }
    const names = written.map((line) => line.trim().split(/\s+/)[0]);
    const committed = [],
      backups = [];
    try {
      for (const name of names) {
        const dest = join(outDir, name);
        for (const input of [isUrl ? null : source, opts.small].filter(
          Boolean,
        )) {
          if (existsSync(dest) && sameFile(input, dest)) {
            if (
              name === preset.svg &&
              srcExt === ".svg" &&
              readFileSync(dest).equals(readFileSync(out(name)))
            )
              continue;
            fail(`refusing to overwrite source file: ${dest}`);
          }
        }
        if (existsSync(dest) && !statSync(dest).isFile())
          fail(`output target is not a file: ${dest}`);
      }
      for (const name of names) {
        const dest = join(outDir, name),
          backup = join(tmp, `backup-${name}`);
        if (existsSync(dest)) {
          renameSync(dest, backup);
          backups.push({ dest, backup });
        }
        renameSync(out(name), dest);
        committed.push(dest);
      }
    } catch (error) {
      const rollbackErrors = [];
      for (const dest of committed.reverse()) {
        try {
          rmSync(dest, { force: true });
        } catch (e) {
          rollbackErrors.push(e);
        }
      }
      for (const { dest, backup } of backups.reverse()) {
        try {
          renameSync(backup, dest);
        } catch (e) {
          rollbackErrors.push(e);
        }
      }
      if (rollbackErrors.length) {
        preserveTmp = true;
        fail(
          `commit/rollback failed; recover originals from ${tmp}: ${error.message}`,
        );
      }
      throw error;
    }
  } catch (e) {
    fail(e?.message?.split("\n")[0] ?? String(e));
  } finally {
    cleanup();
    process.off("exit", cleanup);
  }

  if (!written.length) {
    console.error(
      `html-shot/icons: nothing was written to ${outDir} — the selected outputs produced no files for this source (see the notes above).`,
    );
    throw new Error("no selected outputs were produced");
  }

  console.log(`✔ ${presetName} icon set → ${outDir}`);
  console.log(written.join("\n"));

  const SERVED_ROOTS = new Set(["public", "static"]);
  const outParts = outDirArg.replace(/\\/g, "/").replace(/\/+$/, "").split("/");
  const rootIndex = outParts.findLastIndex((p) => SERVED_ROOTS.has(p));
  const inferredBase =
    rootIndex < 0
      ? null
      : "/" +
        outParts
          .slice(rootIndex + 1)
          .map(encodeURIComponent)
          .join("/");
  const urlBase =
    opts["url-prefix"] !== undefined
      ? "/" +
        opts["url-prefix"]
          .split("/")
          .filter(Boolean)
          .map(encodeURIComponent)
          .join("/")
      : inferredBase;
  const href = (f) =>
    (urlBase === null || urlBase === "/" ? "/" : urlBase + "/") + f;
  if (preset.kind === "web" && presetName !== "next") {
    const links = [];
    if (want.has("ico"))
      links.push(`  <link rel="icon" href="${href(preset.ico)}" sizes="any">`);
    if (want.has("svg") && srcExt === ".svg")
      links.push(
        `  <link rel="icon" href="${href(preset.svg)}" type="image/svg+xml">`,
      );
    if (want.has("apple"))
      links.push(
        `  <link rel="apple-touch-icon" href="${href(preset.apple)}">`,
      );
    if (links.length) {
      const ico = !want.has("ico")
        ? ""
        : urlBase === "/"
          ? ` (${preset.ico} is found at the site root on its own)`
          : ` (${preset.ico} is not at the served root, so nothing auto-discovers it — point the framework's favicon setting at it)`;
      console.log(`\nAdd to <head>${ico}:`);
      console.log(links.join("\n"));
    } else if (want.has("ico")) {
      console.log(
        urlBase === "/"
          ? `\nNothing to wire up: browsers fetch /${preset.ico} from the site root by themselves.`
          : `\nNo <head> line, but ${preset.ico} is not at the served root — point the framework's favicon setting at it.`,
      );
    }
    const shownDir = /^[.\\/]*$/.test(outDirArg)
      ? "the output directory"
      : outDirArg;
    if ((links.length || want.has("ico")) && urlBase === null)
      console.log(
        `\n(the hrefs above assume ${shownDir} is served at the site root; if it sits below one, prefix the path)`,
      );
  }
  if (presetName === "next")
    console.log(
      `\nNothing to wire up: Next's App Router picks these up by filename.`,
    );
  if (pwaWritten.length) {
    if (urlBase === null)
      console.log(
        "\nPWA src URLs assume the output directory is served at /; use --url-prefix for another public path.",
      );
    const entry = ({ name, target }) =>
      JSON.stringify({
        src: href(name),
        sizes: `${target}x${target}`,
        type: "image/png",
        purpose: "any",
      });
    console.log(
      `\nIn the web manifest (verify these URLs are publicly served; these are not maskable icons):`,
    );
    console.log(
      `  "icons": [` + pwaWritten.map(entry).join(",\n            ") + `]`,
    );
  }
}
main().catch((error) => {
  const message = (error?.message?.split("\n")[0] || String(error)).replace(
    /https?:\/\/[^\s"'<>]+/gi,
    safeUrl,
  );
  console.error(`html-shot/icons: ${message}`);
  process.exitCode = 1;
});

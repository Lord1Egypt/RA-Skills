#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";

function usage() {
  console.error("Usage: node generate-html-player.mjs --images <dir> --out <dir> --title <title>");
  process.exit(1);
}

const args = process.argv.slice(2);
const opts = {};
for (let i = 0; i < args.length; i += 2) {
  const key = args[i];
  const value = args[i + 1];
  if (!key || !key.startsWith("--") || !value) usage();
  opts[key.slice(2)] = value;
}

if (!opts.images || !opts.out) usage();

const title = opts.title || "PPT 图片播放";
const imageDir = path.resolve(opts.images);
const outDir = path.resolve(opts.out);
const assetsDir = path.join(outDir, "assets");

const entries = await fs.readdir(imageDir);
const images = entries
  .filter((name) => /\.(png|jpe?g|webp)$/i.test(name))
  .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));

if (images.length === 0) {
  throw new Error(`No slide images found in ${imageDir}`);
}

await fs.mkdir(assetsDir, { recursive: true });

const slideNames = [];
for (let i = 0; i < images.length; i += 1) {
  const ext = path.extname(images[i]).toLowerCase() || ".png";
  const slideName = `slide-${String(i + 1).padStart(2, "0")}${ext}`;
  await fs.copyFile(path.join(imageDir, images[i]), path.join(assetsDir, slideName));
  slideNames.push(`assets/${slideName}`);
}

const html = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escapeHtml(title)}</title>
  <style>
    :root {
      --bg: #0f1720;
      --panel: rgba(18, 59, 93, 0.82);
      --text: #f8fafc;
      --muted: #cbd5e1;
      --accent: #16a36a;
      --line: rgba(255, 255, 255, 0.16);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      overflow: hidden;
      background:
        radial-gradient(circle at 12% 18%, rgba(43, 179, 192, 0.18), transparent 28%),
        linear-gradient(135deg, #0b1118 0%, #132130 55%, #0f1720 100%);
      color: var(--text);
      font-family: "Microsoft YaHei", "PingFang SC", "Segoe UI", Arial, sans-serif;
    }

    .app {
      width: 100vw;
      height: 100vh;
      display: grid;
      grid-template-rows: 1fr auto;
      padding: 24px;
      gap: 16px;
    }

    .stage {
      min-height: 0;
      display: grid;
      place-items: center;
      position: relative;
    }

    .slide-frame {
      width: min(100%, calc((100vh - 116px) * 16 / 9));
      aspect-ratio: 16 / 9;
      border-radius: 8px;
      overflow: hidden;
      background: #fff;
      box-shadow: 0 28px 80px rgba(0, 0, 0, 0.42);
      border: 1px solid rgba(255, 255, 255, 0.22);
    }

    .slide-frame img {
      display: block;
      width: 100%;
      height: 100%;
      object-fit: contain;
      user-select: none;
      -webkit-user-drag: none;
      background: #fff;
    }

    .nav-hit {
      position: absolute;
      top: 0;
      bottom: 0;
      width: 28%;
      border: 0;
      background: transparent;
      cursor: pointer;
    }

    .nav-hit.prev { left: 0; }
    .nav-hit.next { right: 0; }

    .toolbar {
      min-height: 60px;
      display: grid;
      grid-template-columns: auto 1fr auto;
      align-items: center;
      gap: 16px;
      padding: 12px 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      backdrop-filter: blur(14px);
    }

    .controls {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    button {
      height: 36px;
      min-width: 36px;
      border: 1px solid rgba(255, 255, 255, 0.22);
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.1);
      color: var(--text);
      font-size: 15px;
      cursor: pointer;
    }

    button:hover { background: rgba(255, 255, 255, 0.18); }
    button:disabled { opacity: 0.4; cursor: not-allowed; }

    .title {
      min-width: 0;
      text-align: center;
      font-size: 15px;
      color: var(--muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .counter {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 10px;
      min-width: 148px;
      font-variant-numeric: tabular-nums;
      color: var(--muted);
      font-size: 14px;
    }

    .progress {
      width: 88px;
      height: 6px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.18);
      overflow: hidden;
    }

    .progress span {
      display: block;
      height: 100%;
      width: 0;
      border-radius: inherit;
      background: var(--accent);
      transition: width 160ms ease;
    }

    @media (max-width: 720px) {
      .app { padding: 10px; gap: 10px; }
      .toolbar { grid-template-columns: auto auto; gap: 10px; }
      .title { display: none; }
      .counter { min-width: auto; }
    }
  </style>
</head>
<body>
  <main class="app">
    <section class="stage" aria-label="幻灯片播放区">
      <div class="slide-frame">
        <img id="slide" src="${slideNames[0]}" alt="第 1 页幻灯片">
      </div>
      <button class="nav-hit prev" id="prevHit" aria-label="上一页"></button>
      <button class="nav-hit next" id="nextHit" aria-label="下一页"></button>
    </section>

    <footer class="toolbar">
      <div class="controls">
        <button id="prev" type="button" title="上一页">‹</button>
        <button id="next" type="button" title="下一页">›</button>
        <button id="fullscreen" type="button" title="全屏">⛶</button>
      </div>
      <div class="title">${escapeHtml(title)}</div>
      <div class="counter">
        <span id="pageText">1 / ${slideNames.length}</span>
        <div class="progress" aria-hidden="true"><span id="progressBar"></span></div>
      </div>
    </footer>
  </main>

  <script>
    const slides = ${JSON.stringify(slideNames, null, 6)};
    const slideEl = document.getElementById("slide");
    const pageText = document.getElementById("pageText");
    const progressBar = document.getElementById("progressBar");
    const prevBtn = document.getElementById("prev");
    const nextBtn = document.getElementById("next");
    const prevHit = document.getElementById("prevHit");
    const nextHit = document.getElementById("nextHit");
    const fullscreenBtn = document.getElementById("fullscreen");
    let index = 0;

    function render() {
      slideEl.src = slides[index];
      slideEl.alt = \`第 \${index + 1} 页幻灯片\`;
      pageText.textContent = \`\${index + 1} / \${slides.length}\`;
      progressBar.style.width = \`\${((index + 1) / slides.length) * 100}%\`;
      prevBtn.disabled = index === 0;
      nextBtn.disabled = index === slides.length - 1;
    }

    function go(delta) {
      index = Math.max(0, Math.min(slides.length - 1, index + delta));
      render();
    }

    prevBtn.addEventListener("click", () => go(-1));
    nextBtn.addEventListener("click", () => go(1));
    prevHit.addEventListener("click", () => go(-1));
    nextHit.addEventListener("click", () => go(1));
    fullscreenBtn.addEventListener("click", async () => {
      if (!document.fullscreenElement) {
        await document.documentElement.requestFullscreen();
      } else {
        await document.exitFullscreen();
      }
    });

    window.addEventListener("keydown", (event) => {
      if (event.key === "ArrowRight" || event.key === "PageDown" || event.key === " ") {
        event.preventDefault();
        go(1);
      }
      if (event.key === "ArrowLeft" || event.key === "PageUp") {
        event.preventDefault();
        go(-1);
      }
      if (event.key === "Home") {
        index = 0;
        render();
      }
      if (event.key === "End") {
        index = slides.length - 1;
        render();
      }
    });

    slides.slice(1).forEach((src) => {
      const img = new Image();
      img.src = src;
    });

    render();
  </script>
</body>
</html>
`;

await fs.mkdir(outDir, { recursive: true });
await fs.writeFile(path.join(outDir, "index.html"), html, "utf8");
console.log(`Generated ${path.join(outDir, "index.html")}`);

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

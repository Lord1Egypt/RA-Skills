const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");
const { pathToFileURL } = require("url");
const { buildPreviewHtml } = require("./render_preview");
const { computeTimeline, ensureDir, getMoviePath, readJson, writeText } = require("./common");
const { syncMovieTimings } = require("./timing");
const { validateMovie } = require("./validate_movie");

function requirePlaywright() {
  try {
    return require("playwright");
  } catch (error) {
    console.error('Missing dependency "playwright". Run `npm install` and `npx playwright install chromium` first.');
    process.exit(1);
  }
}

async function exportVideo(moviePath, outputPath) {
  const movie = syncMovieTimings(readJson(moviePath));
  const errors = validateMovie(movie, moviePath);
  if (errors.length > 0) {
    throw new Error(`Validation failed:\n${errors.map((item) => `- ${item}`).join("\n")}`);
  }

  const { chromium } = requirePlaywright();
  const fps = movie.meta.fps || 30;
  const timeline = computeTimeline(movie);
  const totalFrames = Math.max(1, Math.ceil((timeline.totalDurationMs / 1000) * fps));
  const exportRoot = fs.mkdtempSync(path.join(os.tmpdir(), "motion-video-export-"));
  const previewPath = path.join(exportRoot, "preview.html");
  const framesDir = path.join(exportRoot, "frames");

  ensureDir(framesDir);
  writeText(previewPath, buildPreviewHtml(movie, moviePath));

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 980 }, deviceScaleFactor: 1 });

  await page.goto(pathToFileURL(previewPath).href);
  await page.waitForFunction(() => window.__MOVIE_READY === true);

  const stage = page.locator("#stage");
  for (let frame = 0; frame < totalFrames; frame += 1) {
    const timeMs = Math.min(timeline.totalDurationMs, Math.round((frame * 1000) / fps));
    await page.evaluate((value) => window.__setMovieTime(value), timeMs);
    await stage.screenshot({
      path: path.join(framesDir, `frame-${String(frame).padStart(5, "0")}.png`)
    });
  }

  await browser.close();

  ensureDir(path.dirname(path.resolve(outputPath)));
  execFileSync("ffmpeg", [
    "-y",
    "-framerate",
    String(fps),
    "-i",
    path.join(framesDir, "frame-%05d.png"),
    "-c:v",
    "libx264",
    "-pix_fmt",
    "yuv420p",
    path.resolve(outputPath)
  ], { stdio: "inherit" });
}

if (require.main === module) {
  const source = process.argv[2];
  const output = process.argv[3];
  const confirmed = process.argv.includes("--confirm");

  if (!source || !output) {
    console.error("Usage: node scripts/export_video.js <movie.json | project-dir> <output.mp4> --confirm");
    process.exit(1);
  }

  if (!confirmed) {
    console.error("Refusing to export without explicit confirmation. Re-run with --confirm after the user approves.");
    process.exit(1);
  }

  exportVideo(getMoviePath(source), output)
    .then(() => {
      console.log(`Video written to ${path.resolve(output)}`);
    })
    .catch((error) => {
      console.error(error.message || String(error));
      process.exit(1);
    });
}

module.exports = {
  exportVideo
};

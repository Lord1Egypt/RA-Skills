const path = require("path");
const { execFileSync } = require("child_process");
const { getMoviePath, getProjectDir } = require("./common");

if (require.main === module) {
  const target = process.argv[2];
  const shouldExport = process.argv.includes("--export");
  const confirmExport = process.argv.includes("--confirm-export");

  if (!target) {
    console.error("Usage: node scripts/build_project.js <project-dir | movie.json> [--export --confirm-export]");
    process.exit(1);
  }

  if (shouldExport && !confirmExport) {
    console.error("Export blocked. Preview is ready, but video export requires explicit confirmation via --confirm-export.");
    process.exit(1);
  }

  const moviePath = getMoviePath(target);
  const projectDir = getProjectDir(target);
  const previewPath = path.join(projectDir, "preview.html");
  const outputVideoPath = path.join(projectDir, "output", `${path.basename(projectDir)}.mp4`);

  execFileSync("node", [path.join(__dirname, "sync_timings.js"), moviePath], { stdio: "inherit" });
  execFileSync("node", [path.join(__dirname, "validate_movie.js"), moviePath], { stdio: "inherit" });
  execFileSync("node", [path.join(__dirname, "render_preview.js"), moviePath, previewPath], { stdio: "inherit" });

  if (shouldExport) {
    execFileSync("node", [path.join(__dirname, "export_video.js"), moviePath, outputVideoPath, "--confirm"], { stdio: "inherit" });
  }

  console.log(`Build finished for ${projectDir}`);
}

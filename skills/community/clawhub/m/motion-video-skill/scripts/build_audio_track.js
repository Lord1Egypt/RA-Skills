const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");
const { getMoviePath, readJson } = require("./common");
const { ffprobeDurationMs } = require("./audio_common");

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function escapeConcatPath(filePath) {
  return filePath.replace(/'/g, "'\\''");
}

if (require.main === module) {
  const target = process.argv[2];
  const outputArg = process.argv[3];

  if (!target) {
    console.error("Usage: node scripts/build_audio_track.js <movie.json | project-dir> [output.wav]");
    process.exit(1);
  }

  const moviePath = getMoviePath(target);
  const projectDir = path.dirname(moviePath);
  const movie = readJson(moviePath);

  if (!movie.audio || !Array.isArray(movie.audio.tracks) || movie.audio.tracks.length === 0) {
    console.error("No synthesized audio tracks found. Run TTS synthesis first.");
    process.exit(1);
  }

  const trackMap = new Map(movie.audio.tracks.map((track) => [track.sceneId, track]));
  const workDir = fs.mkdtempSync(path.join(os.tmpdir(), "motion-video-audio-"));
  const segmentDir = path.join(workDir, "segments");
  ensureDir(segmentDir);

  const segmentFiles = [];

  for (let index = 0; index < movie.scenes.length; index += 1) {
    const scene = movie.scenes[index];
    const track = trackMap.get(scene.id);
    if (!track) {
      console.error(`Missing audio track for scene ${scene.id}`);
      process.exit(1);
    }

    const sourceFile = path.join(projectDir, track.file);
    const sourceDurationMs = Number.isFinite(track.durationMs) ? track.durationMs : ffprobeDurationMs(sourceFile);
    const targetDurationMs = Math.max(scene.durationMs, sourceDurationMs);
    const segmentFile = path.join(segmentDir, `segment-${String(index).padStart(2, "0")}.wav`);

    execFileSync(
      "ffmpeg",
      [
        "-y",
        "-i",
        sourceFile,
        "-af",
        `apad=whole_dur=${(targetDurationMs / 1000).toFixed(3)}`,
        "-t",
        (targetDurationMs / 1000).toFixed(3),
        "-ar",
        "48000",
        "-ac",
        "1",
        segmentFile
      ],
      { stdio: "inherit" }
    );

    segmentFiles.push(segmentFile);
  }

  const concatFile = path.join(workDir, "concat.txt");
  fs.writeFileSync(concatFile, segmentFiles.map((file) => `file '${escapeConcatPath(file)}'`).join("\n") + "\n", "utf8");

  const outputFile = path.resolve(outputArg || path.join(projectDir, movie.audio.outputDir || "audio", "narration-track.wav"));
  ensureDir(path.dirname(outputFile));

  execFileSync(
    "ffmpeg",
    [
      "-y",
      "-f",
      "concat",
      "-safe",
      "0",
      "-i",
      concatFile,
      "-c",
      "copy",
      outputFile
    ],
    { stdio: "inherit" }
  );

  console.log(`Built merged narration track: ${outputFile}`);
}

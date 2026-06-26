const path = require("path");
const { execFileSync } = require("child_process");
const { getMoviePath } = require("./common");

if (require.main === module) {
  const target = process.argv[2];
  const videoArg = process.argv[3];
  const audioArg = process.argv[4];
  const outputArg = process.argv[5];

  if (!target) {
    console.error("Usage: node scripts/mux_video_audio.js <movie.json | project-dir> [video.mp4] [audio.wav] [output.mp4]");
    process.exit(1);
  }

  const moviePath = getMoviePath(target);
  const projectDir = path.dirname(moviePath);
  const baseName = path.basename(projectDir);
  const videoFile = path.resolve(videoArg || path.join(projectDir, "output", `${baseName}.mp4`));
  const audioFile = path.resolve(audioArg || path.join(projectDir, "audio", "narration-track.wav"));
  const outputFile = path.resolve(outputArg || path.join(projectDir, "output", `${baseName}-voiced.mp4`));

  execFileSync(
    "ffmpeg",
    [
      "-y",
      "-i",
      videoFile,
      "-i",
      audioFile,
      "-c:v",
      "copy",
      "-c:a",
      "aac",
      "-b:a",
      "192k",
      "-shortest",
      outputFile
    ],
    { stdio: "inherit" }
  );

  console.log(`Muxed final voiced video: ${outputFile}`);
}

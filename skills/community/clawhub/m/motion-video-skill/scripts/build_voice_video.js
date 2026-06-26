const path = require("path");
const { execFileSync } = require("child_process");
const { getMoviePath, getProjectDir, readJson } = require("./common");

if (require.main === module) {
  const target = process.argv[2];
  const confirmExport = process.argv.includes("--confirm-export");

  if (!target) {
    console.error("Usage: node scripts/build_voice_video.js <movie.json | project-dir> --confirm-export");
    process.exit(1);
  }

  if (!confirmExport) {
    console.error("Refusing to build final voiced video without --confirm-export.");
    process.exit(1);
  }

  const moviePath = getMoviePath(target);
  const movie = readJson(moviePath);
  if (!movie.audio || movie.audio.confirmationStatus !== "confirmed" || !movie.audio.voice) {
    console.error("Voiced export is blocked until the user explicitly confirms provider, voice, language, speed, and fallback. Run `node scripts/configure_tts.js ...`, show voice options to the user, then run `node scripts/confirm_tts.js ... --voice <voice-id>`.");
    process.exit(1);
  }

  const projectDir = getProjectDir(target);
  const baseName = path.basename(projectDir);
  const outputVideo = path.join(projectDir, "output", `${baseName}.mp4`);
  const outputAudio = path.join(projectDir, "audio", "narration-track.wav");
  const finalVideo = path.join(projectDir, "output", `${baseName}-voiced.mp4`);

  execFileSync("node", [path.join(__dirname, "synthesize_voice.js"), moviePath], { stdio: "inherit" });
  execFileSync("node", [path.join(__dirname, "sync_audio_durations.js"), moviePath], { stdio: "inherit" });
  execFileSync("node", [path.join(__dirname, "build_project.js"), moviePath, "--export", "--confirm-export"], { stdio: "inherit" });
  execFileSync("node", [path.join(__dirname, "build_audio_track.js"), moviePath, outputAudio], { stdio: "inherit" });
  execFileSync("node", [path.join(__dirname, "mux_video_audio.js"), moviePath, outputVideo, outputAudio, finalVideo], { stdio: "inherit" });

  console.log(`Built final voiced video: ${finalVideo}`);
}

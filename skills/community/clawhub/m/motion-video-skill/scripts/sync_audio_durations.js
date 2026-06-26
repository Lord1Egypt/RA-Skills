const path = require("path");
const { getMoviePath, readJson, writeText } = require("./common");
const { ffprobeDurationMs } = require("./audio_common");

if (require.main === module) {
  const target = process.argv[2];
  if (!target) {
    console.error("Usage: node scripts/sync_audio_durations.js <movie.json | project-dir>");
    process.exit(1);
  }

  const moviePath = getMoviePath(target);
  const projectDir = path.dirname(moviePath);
  const movie = readJson(moviePath);

  if (!movie.audio || !Array.isArray(movie.audio.tracks)) {
    console.error("No audio tracks found in movie.json. Configure and synthesize TTS first.");
    process.exit(1);
  }

  movie.audio.tracks = movie.audio.tracks.map((track) => {
    const absoluteFile = path.join(projectDir, track.file);
    const durationMs = ffprobeDurationMs(absoluteFile);
    return {
      ...track,
      durationMs,
      status: "ready"
    };
  });

  writeText(moviePath, JSON.stringify(movie, null, 2) + "\n");
  console.log(`Synced audio durations into ${moviePath}`);
}

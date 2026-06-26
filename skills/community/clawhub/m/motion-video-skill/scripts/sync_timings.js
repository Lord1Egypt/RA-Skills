const { getMoviePath, readJson, writeText } = require("./common");
const { syncMovieTimings } = require("./timing");

if (require.main === module) {
  const target = process.argv[2];
  if (!target) {
    console.error("Usage: node scripts/sync_timings.js <movie.json | project-dir>");
    process.exit(1);
  }

  const moviePath = getMoviePath(target);
  const movie = readJson(moviePath);
  const syncedMovie = syncMovieTimings(movie);
  writeText(moviePath, JSON.stringify(syncedMovie, null, 2) + "\n");
  console.log(`Synced narration-based timings for ${moviePath}`);
}

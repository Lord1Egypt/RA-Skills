const path = require("path");
const {
  getMoviePath,
  parseFlag,
  readJson,
  resolveCatalogEntry,
  writeText
} = require("./common");

function defaultTrackExtension({ providerId, format }) {
  if (format) {
    return format;
  }

  if (providerId === "system") {
    return process.platform === "win32" ? "wav" : "aiff";
  }

  return "wav";
}

function buildTrackList(movie, outputDir, extension) {
  return (movie.scenes || []).map((scene) => ({
    sceneId: scene.id,
    text: scene.narration || "",
    file: path.posix.join(outputDir, `${scene.id}.${extension}`),
    status: "pending"
  }));
}

if (require.main === module) {
  const target = process.argv[2];
  if (!target) {
    console.error("Usage: node scripts/configure_tts.js <movie.json | project-dir> --provider openai [--language zh-CN] [--speed 1.0] [--fallback system]");
    process.exit(1);
  }

  const providerId = parseFlag(process.argv, "--provider");
  const language = parseFlag(process.argv, "--language", "zh-CN");
  const speedValue = parseFlag(process.argv, "--speed", "1");
  const fallbackProvider = parseFlag(process.argv, "--fallback", "system");
  const model = parseFlag(process.argv, "--model", providerId === "minimax" ? "speech-2.8-hd" : null);
  const format = parseFlag(process.argv, "--format", providerId === "minimax" ? "mp3" : null);
  const confirmed = process.argv.includes("--confirmed");

  if (!providerId) {
    console.error("Missing --provider. Use `node scripts/list_catalog.js` to inspect available TTS providers.");
    process.exit(1);
  }

  if (confirmed) {
    console.error("`configure_tts.js` no longer supports `--confirmed`. First save a pending provider config, then run `node scripts/confirm_tts.js ... --voice <voice-id>` after the user explicitly approves a voice.");
    process.exit(1);
  }

  const provider = resolveCatalogEntry("tts-providers", providerId);
  const fallback = fallbackProvider ? resolveCatalogEntry("tts-providers", fallbackProvider) : null;
  const moviePath = getMoviePath(target);
  const movie = readJson(moviePath);
  const speed = Number(speedValue);
  const extension = defaultTrackExtension({ providerId, format });

  if (!Number.isFinite(speed) || speed <= 0) {
    console.error("Invalid --speed. Expected a positive number.");
    process.exit(1);
  }

  movie.audio = {
    enabled: true,
    mode: "tts",
    confirmationRequired: true,
    confirmationStatus: "pending",
    provider: provider.id,
    voice: null,
    language,
    speed,
    fallbackProvider: fallback ? fallback.id : null,
    outputDir: "audio",
    providerConfig: {
      ...(model ? { model } : {}),
      ...(format ? { format } : {})
    },
    tracks: buildTrackList(movie, "audio", extension)
  };

  writeText(moviePath, JSON.stringify(movie, null, 2) + "\n");
  console.log(`Configured pending TTS provider for ${moviePath}: ${provider.id}. Voice remains unconfirmed until the user explicitly chooses one.`);
}

module.exports = {
  defaultTrackExtension,
  buildTrackList
};

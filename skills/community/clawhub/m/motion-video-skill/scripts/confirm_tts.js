const { getMoviePath, parseFlag, readJson, resolveCatalogEntry, writeText } = require("./common");
const { defaultTrackExtension, buildTrackList } = require("./configure_tts");

if (require.main === module) {
  const target = process.argv[2];
  if (!target) {
    console.error("Usage: node scripts/confirm_tts.js <movie.json | project-dir> --voice <voice-id> [--provider minimax] [--language zh-CN] [--speed 1.0] [--fallback system]");
    process.exit(1);
  }

  const voice = parseFlag(process.argv, "--voice");
  const moviePath = getMoviePath(target);
  const movie = readJson(moviePath);
  const existingAudio = movie.audio && typeof movie.audio === "object" ? movie.audio : {};
  const providerId = parseFlag(process.argv, "--provider", existingAudio.provider || null);
  const language = parseFlag(process.argv, "--language", existingAudio.language || "zh-CN");
  const speedValue = parseFlag(process.argv, "--speed", existingAudio.speed !== undefined ? String(existingAudio.speed) : "1");
  const fallbackProvider = parseFlag(process.argv, "--fallback", existingAudio.fallbackProvider || "system");
  const model = parseFlag(
    process.argv,
    "--model",
    existingAudio.providerConfig && existingAudio.providerConfig.model
      ? existingAudio.providerConfig.model
      : providerId === "minimax"
        ? "speech-2.8-hd"
        : null
  );
  const format = parseFlag(
    process.argv,
    "--format",
    existingAudio.providerConfig && existingAudio.providerConfig.format
      ? existingAudio.providerConfig.format
      : providerId === "minimax"
        ? "mp3"
        : null
  );
  const speed = Number(speedValue);

  if (!providerId) {
    console.error("Missing provider. Run `node scripts/configure_tts.js ... --provider <id>` first, or pass `--provider` here.");
    process.exit(1);
  }

  if (!voice || !voice.trim()) {
    console.error("Missing --voice. TTS confirmation is blocked until the user explicitly picks a voice.");
    process.exit(1);
  }

  if (!Number.isFinite(speed) || speed <= 0) {
    console.error("Invalid --speed. Expected a positive number.");
    process.exit(1);
  }

  const provider = resolveCatalogEntry("tts-providers", providerId);
  const fallback = fallbackProvider ? resolveCatalogEntry("tts-providers", fallbackProvider) : null;
  const extension = defaultTrackExtension({ providerId, format });

  movie.audio = {
    enabled: true,
    mode: "tts",
    confirmationRequired: true,
    confirmationStatus: "confirmed",
    provider: provider.id,
    voice: voice.trim(),
    language,
    speed,
    fallbackProvider: fallback ? fallback.id : null,
    outputDir: existingAudio.outputDir || "audio",
    providerConfig: {
      ...(model ? { model } : {}),
      ...(format ? { format } : {})
    },
    tracks: buildTrackList(movie, existingAudio.outputDir || "audio", extension)
  };

  writeText(moviePath, JSON.stringify(movie, null, 2) + "\n");
  console.log(`Confirmed TTS voice for ${moviePath}: ${provider.id} / ${voice.trim()}`);
}

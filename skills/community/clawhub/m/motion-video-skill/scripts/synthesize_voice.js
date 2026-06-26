const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");
const { getMoviePath, readJson, writeText } = require("./common");
const { getProviderSecret } = require("./secrets");

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function requireAudioConfig(movie) {
  if (!movie.audio || movie.audio.enabled !== true || movie.audio.mode !== "tts") {
    throw new Error("TTS is not enabled for this project. Configure it first with `node scripts/configure_tts.js ...`.");
  }

  if (movie.audio.confirmationStatus !== "confirmed") {
    throw new Error("TTS synthesis is blocked until the user confirms the TTS provider and voice settings.");
  }
}

function mapSayRate(speed = 1) {
  return Math.max(120, Math.min(260, Math.round(180 * speed)));
}

function mapWindowsRate(speed = 1) {
  return Math.max(-10, Math.min(10, Math.round((speed - 1) * 8)));
}

function systemOutputExtension() {
  return process.platform === "win32" ? "wav" : "aiff";
}

function replaceTrackExtension(trackFile, extension) {
  return String(trackFile).replace(/\.(aiff|wav|mp3)$/i, `.${extension}`);
}

function synthesizeWithMacSay(track, absoluteFile, sayRate, sayVoice) {
  const sayArgs = [];
  if (sayVoice) {
    sayArgs.push("-v", sayVoice);
  }
  sayArgs.push("-r", String(sayRate), "-o", absoluteFile, track.text);
  execFileSync("say", sayArgs, { stdio: "inherit" });
}

function synthesizeWithWindowsSpeech(track, absoluteFile, speed, voice) {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "motion-video-tts-"));
  const scriptPath = path.join(tempDir, "synthesize.ps1");
  const textPath = path.join(tempDir, "input.txt");
  const rate = mapWindowsRate(speed);

  fs.writeFileSync(textPath, track.text, "utf8");
  fs.writeFileSync(
    scriptPath,
    [
      "param(",
      "  [string]$TextPath,",
      "  [string]$OutputPath,",
      "  [int]$Rate,",
      "  [string]$VoiceName",
      ")",
      "Add-Type -AssemblyName System.Speech",
      "$text = Get-Content -Raw -Path $TextPath -Encoding UTF8",
      "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer",
      "if ($VoiceName) {",
      "  $synth.SelectVoice($VoiceName)",
      "}",
      "$synth.Rate = $Rate",
      "$synth.SetOutputToWaveFile($OutputPath)",
      "$synth.Speak($text)",
      "$synth.Dispose()"
    ].join("\n"),
    "utf8"
  );

  const psArgs = [
    "-NoProfile",
    "-ExecutionPolicy",
    "Bypass",
    "-File",
    scriptPath,
    "-TextPath",
    textPath,
    "-OutputPath",
    absoluteFile,
    "-Rate",
    String(rate)
  ];

  if (voice) {
    psArgs.push("-VoiceName", voice);
  }

  execFileSync("powershell.exe", psArgs, { stdio: "inherit" });
}

function synthesizeWithSystem(movie, moviePath, options = {}) {
  const projectDir = path.dirname(moviePath);
  const outputDir = path.join(projectDir, movie.audio.outputDir || "audio");
  ensureDir(outputDir);

  const sayRate = mapSayRate(movie.audio.speed);
  const sayVoice = options.useConfiguredVoice ? movie.audio.voice : null;
  const extension = systemOutputExtension();

  const nextTracks = (movie.audio.tracks || []).map((track) => {
    const nextFile = replaceTrackExtension(track.file, extension);
    const absoluteFile = path.join(projectDir, nextFile);
    ensureDir(path.dirname(absoluteFile));

    if (process.platform === "darwin") {
      synthesizeWithMacSay(track, absoluteFile, sayRate, sayVoice);
    } else if (process.platform === "win32") {
      synthesizeWithWindowsSpeech(track, absoluteFile, movie.audio.speed, sayVoice);
    } else {
      throw new Error(`System TTS fallback is currently supported on macOS and Windows only. Current platform: ${process.platform}`);
    }

    return {
      ...track,
      file: nextFile,
      status: "ready"
    };
  });

  movie.audio.tracks = nextTracks;
  movie.audio.confirmationStatus = "synthesized";
  writeText(moviePath, JSON.stringify(movie, null, 2) + "\n");
}

function languageBoost(language) {
  const normalized = String(language || "").toLowerCase();
  if (normalized.startsWith("zh")) {
    return "Chinese";
  }
  if (normalized.startsWith("en")) {
    return "English";
  }
  if (normalized.startsWith("ja")) {
    return "Japanese";
  }
  if (normalized.startsWith("ko")) {
    return "Korean";
  }
  return "auto";
}

async function synthesizeWithMiniMax(movie, moviePath) {
  const secret = getProviderSecret("minimax");
  if (!secret || !secret.apiKey) {
    throw new Error("MiniMax API key is not configured. Store it first with `node scripts/set_provider_secret.js minimax <api-key>` or set MINIMAX_API_KEY.");
  }

  const projectDir = path.dirname(moviePath);
  const outputDir = path.join(projectDir, movie.audio.outputDir || "audio");
  ensureDir(outputDir);

  const model = movie.audio.providerConfig && movie.audio.providerConfig.model ? movie.audio.providerConfig.model : "speech-2.8-hd";
  const format = movie.audio.providerConfig && movie.audio.providerConfig.format ? movie.audio.providerConfig.format : "mp3";
  const voiceId = movie.audio.voice;

  if (!voiceId) {
    throw new Error("MiniMax TTS requires a confirmed voice id before synthesis.");
  }

  const nextTracks = [];
  for (const track of movie.audio.tracks || []) {
    const response = await fetch("https://api.minimaxi.com/v1/t2a_v2", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${secret.apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model,
        text: track.text,
        stream: false,
        voice_setting: {
          voice_id: voiceId,
          speed: movie.audio.speed || 1,
          vol: 1,
          pitch: 0
        },
        audio_setting: {
          sample_rate: 32000,
          bitrate: 128000,
          format,
          channel: 1
        },
        language_boost: languageBoost(movie.audio.language),
        subtitle_enable: false,
        output_format: "hex"
      })
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`MiniMax TTS request failed (${response.status}): ${text}`);
    }

    const payload = await response.json();
    if (!payload || !payload.base_resp || payload.base_resp.status_code !== 0) {
      throw new Error(`MiniMax TTS returned an error: ${JSON.stringify(payload)}`);
    }
    const hexAudio = payload && payload.data && payload.data.audio;
    if (!hexAudio) {
      throw new Error(`MiniMax TTS response did not include audio: ${JSON.stringify(payload)}`);
    }

    const absoluteFile = path.join(projectDir, track.file.replace(/\.(aiff|wav|mp3)$/i, `.${format}`));
    ensureDir(path.dirname(absoluteFile));
    fs.writeFileSync(absoluteFile, Buffer.from(hexAudio, "hex"));
    nextTracks.push({
      ...track,
      file: path.relative(projectDir, absoluteFile),
      status: "ready"
    });
  }

  movie.audio.tracks = nextTracks;
  movie.audio.confirmationStatus = "synthesized";
  writeText(moviePath, JSON.stringify(movie, null, 2) + "\n");
}

if (require.main === module) {
  const target = process.argv[2];
  if (!target) {
    console.error("Usage: node scripts/synthesize_voice.js <movie.json | project-dir>");
    process.exit(1);
  }

  const moviePath = getMoviePath(target);
  const movie = readJson(moviePath);
  requireAudioConfig(movie);

  const provider = movie.audio.provider;
  const fallback = movie.audio.fallbackProvider;

  (async () => {
    if (provider === "system") {
      synthesizeWithSystem(movie, moviePath, { useConfiguredVoice: true });
      console.log(`Synthesized scene audio with system TTS for ${moviePath}`);
      return;
    }

    if (provider === "minimax") {
      try {
        await synthesizeWithMiniMax(movie, moviePath);
        console.log(`Synthesized scene audio with MiniMax TTS for ${moviePath}`);
        return;
      } catch (error) {
        if (fallback === "system") {
          console.warn(`${error.message} Falling back to system TTS.`);
          synthesizeWithSystem(movie, moviePath, { useConfiguredVoice: false });
          console.log(`Synthesized scene audio with system fallback for ${moviePath}`);
          return;
        }
        throw error;
      }
    }

    if (fallback === "system") {
      console.warn(`Provider "${provider}" is configured but no adapter is implemented yet. Falling back to system TTS.`);
      synthesizeWithSystem(movie, moviePath, { useConfiguredVoice: false });
      console.log(`Synthesized scene audio with system fallback for ${moviePath}`);
      return;
    }

    throw new Error(`Provider "${provider}" is configured, but its adapter is not implemented yet and no system fallback is enabled.`);
  })().catch((error) => {
    console.error(error.message || String(error));
    process.exit(1);
  });
}

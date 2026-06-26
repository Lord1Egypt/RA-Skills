const {
  VALID_EFFECTS,
  VALID_SCENE_TRANSITIONS,
  VALID_SUBTITLE_PRESETS,
  clamp
} = require("./common");

function cloneJson(value) {
  return JSON.parse(JSON.stringify(value));
}

function countMatches(text, pattern) {
  const matches = text.match(pattern);
  return matches ? matches.length : 0;
}

function normalizeNarrationText(text) {
  return String(text || "")
    .replace(/\s+/g, " ")
    .trim();
}

function estimateSpeechMs(text) {
  const normalized = normalizeNarrationText(text);
  if (!normalized) {
    return 1200;
  }

  const tokens = normalized.match(/[\u4e00-\u9fff]|[A-Za-z0-9%+/_:.-]+/g) || [];
  let totalMs = 0;

  for (const token of tokens) {
    if (/^[\u4e00-\u9fff]$/.test(token)) {
      totalMs += 180;
    } else {
      totalMs += clamp(Math.round(token.length * 52), 160, 420);
    }
  }

  totalMs += countMatches(normalized, /[，,、]/g) * 120;
  totalMs += countMatches(normalized, /[：:；;]/g) * 180;
  totalMs += countMatches(normalized, /[。！？!?]/g) * 280;
  return Math.max(1200, totalMs);
}

function splitNarrationIntoCueTexts(text) {
  const normalized = normalizeNarrationText(text);
  if (!normalized) {
    return [];
  }

  const majorChunks = normalized
    .split(/(?<=[。！？!?；;])/)
    .map((chunk) => chunk.trim())
    .filter(Boolean);

  const cues = [];
  for (const chunk of majorChunks.length > 0 ? majorChunks : [normalized]) {
    if (estimateSpeechMs(chunk) > 2500 && /[，,、：:]/.test(chunk)) {
      const subChunks = chunk
        .split(/(?<=[，,、：:])/)
        .map((item) => item.trim())
        .filter(Boolean);
      cues.push(...(subChunks.length > 0 ? subChunks : [chunk]));
    } else {
      cues.push(chunk);
    }
  }

  return cues.length > 0 ? cues : [normalized];
}

function buildSceneCues(sceneId, narrationText, speechDurationMs) {
  const cueTexts = splitNarrationIntoCueTexts(narrationText);
  if (cueTexts.length === 0) {
    return [];
  }

  const estimatedDurations = cueTexts.map((cueText) => estimateSpeechMs(cueText));
  const estimatedTotal = estimatedDurations.reduce((sum, value) => sum + value, 0) || 1;
  const leadInMs = 180;
  const resolvedSpeechDurationMs = Math.max(720, Math.round(speechDurationMs || estimatedTotal));
  const speechEndMs = leadInMs + resolvedSpeechDurationMs;

  let cursorMs = leadInMs;
  return cueTexts.map((cueText, index) => {
    const proportionalMs = Math.max(320, Math.round((estimatedDurations[index] / estimatedTotal) * resolvedSpeechDurationMs));
    const endMs = index === cueTexts.length - 1 ? speechEndMs : Math.min(speechEndMs, cursorMs + proportionalMs);
    const cue = {
      id: `${sceneId}-cue-${String(index + 1).padStart(2, "0")}`,
      text: cueText,
      startMs: cursorMs,
      endMs: Math.max(cursorMs + 240, endMs)
    };
    cursorMs = cue.endMs;
    return cue;
  });
}

function elementSpeechText(element) {
  if (!element || typeof element !== "object") {
    return "";
  }

  if (element.type === "bullet-list" && Array.isArray(element.items)) {
    return element.items.join("，");
  }

  if (element.type === "stat") {
    return [element.value, element.text].filter(Boolean).join("，");
  }

  if (typeof element.text === "string") {
    return element.text;
  }

  return "";
}

function deriveNarrationText(scene) {
  if (typeof scene.narration === "string" && scene.narration.trim()) {
    return scene.narration.trim();
  }

  return (scene.elements || [])
    .map((element) => elementSpeechText(element))
    .filter(Boolean)
    .join("。");
}

function defaultEffectForElement(element) {
  if (!element || typeof element !== "object") {
    return "fade";
  }

  if (element.type === "shape") {
    return "clip-up";
  }
  if (element.type === "chip") {
    return "fade";
  }
  if (element.type === "title") {
    return "fade-up";
  }
  if (element.type === "bullet-list") {
    return "reveal-down";
  }
  if (element.type === "quote") {
    return "blur-in";
  }
  if (element.type === "stat") {
    return "glow-pop";
  }
  if (element.type === "subtitle") {
    return "blur-in";
  }
  return "fade";
}

function effectForElement(element) {
  const requested = element && element.animation && typeof element.animation.effect === "string" ? element.animation.effect : "";
  return VALID_EFFECTS.has(requested) ? requested : defaultEffectForElement(element);
}

function elementPriority(element) {
  if (element.type === "shape") {
    return 0;
  }
  if (element.type === "chip") {
    return 1;
  }
  if (element.type === "title" || element.type === "stat") {
    return 2;
  }
  if (element.type === "subtitle") {
    return 3;
  }
  if (element.type === "bullet-list") {
    return 4;
  }
  if (element.type === "text" || element.type === "quote") {
    return 5;
  }
  return 6;
}

function elementSort(left, right) {
  return elementPriority(left) - elementPriority(right) || left.y - right.y || left.x - right.x;
}

function baseAnimationDuration(element, effect, textMs) {
  const typeBase = {
    shape: 620,
    chip: 360,
    title: 660,
    subtitle: 520,
    text: 520,
    "bullet-list": 560,
    quote: 600,
    stat: 660
  };
  const effectBonus = {
    fade: 0,
    "fade-up": 40,
    "slide-left": 60,
    "slide-right": 60,
    pop: 50,
    "clip-up": 80,
    "zoom-in": 70,
    "blur-in": 90,
    "glow-pop": 100,
    "swing-up": 80,
    "reveal-right": 90,
    "reveal-down": 90
  };

  const base = typeBase[element.type] || 500;
  const bonus = effectBonus[effect] || 0;
  return clamp(Math.round(base + bonus + textMs * 0.04), 320, 980);
}

function defaultSceneTransitionForType(sceneType) {
  const defaults = {
    hero: {
      enterEffect: "zoom-out",
      exitEffect: "fade",
      enterDurationMs: 360,
      exitDurationMs: 220
    },
    problem: {
      enterEffect: "blur-in",
      exitEffect: "slide-left",
      enterDurationMs: 320,
      exitDurationMs: 220
    },
    steps: {
      enterEffect: "lift-up",
      exitEffect: "fade",
      enterDurationMs: 300,
      exitDurationMs: 220
    },
    comparison: {
      enterEffect: "wipe-left",
      exitEffect: "slide-right",
      enterDurationMs: 320,
      exitDurationMs: 240
    },
    stat: {
      enterEffect: "zoom-in",
      exitEffect: "fade",
      enterDurationMs: 280,
      exitDurationMs: 220
    },
    quote: {
      enterEffect: "blur-in",
      exitEffect: "fade",
      enterDurationMs: 300,
      exitDurationMs: 220
    },
    closing: {
      enterEffect: "iris-in",
      exitEffect: "fade",
      enterDurationMs: 340,
      exitDurationMs: 260
    }
  };

  return defaults[sceneType] || defaults.hero;
}

function normalizeSceneTransition(scene) {
  const requested = scene && scene.transition && typeof scene.transition === "object" ? scene.transition : {};
  const defaults = defaultSceneTransitionForType(scene.type);

  const enterEffect = VALID_SCENE_TRANSITIONS.has(requested.enterEffect) ? requested.enterEffect : defaults.enterEffect;
  const exitEffect = VALID_SCENE_TRANSITIONS.has(requested.exitEffect) ? requested.exitEffect : defaults.exitEffect;
  const enterDurationMs = Number.isFinite(requested.enterDurationMs)
    ? clamp(Math.round(requested.enterDurationMs), 120, 900)
    : defaults.enterDurationMs;
  const exitDurationMs = Number.isFinite(requested.exitDurationMs)
    ? clamp(Math.round(requested.exitDurationMs), 120, 900)
    : defaults.exitDurationMs;

  return {
    enterEffect,
    exitEffect,
    enterDurationMs,
    exitDurationMs
  };
}

function cueForIndex(cues, cueIndex, fallbackStartMs, fallbackEndMs) {
  if (!Array.isArray(cues) || cues.length === 0) {
    return {
      id: null,
      text: "",
      startMs: fallbackStartMs,
      endMs: fallbackEndMs
    };
  }

  const cue = cues[Math.min(cueIndex, cues.length - 1)];
  return {
    id: cue.id,
    text: cue.text,
    startMs: cue.startMs,
    endMs: cue.endMs
  };
}

function syncSceneTimings(scene, options = {}) {
  const nextScene = cloneJson(scene);
  const narrationText = deriveNarrationText(nextScene);
  const narrationMs = estimateSpeechMs(narrationText);
  const speechDurationMs = Number.isFinite(options.trackDurationMs) ? options.trackDurationMs : narrationMs;

  if (nextScene.timingMode === "manual") {
    nextScene.narration = narrationText;
    nextScene.cues =
      Array.isArray(nextScene.cues) && nextScene.cues.length > 0 ? nextScene.cues : buildSceneCues(nextScene.id, narrationText, speechDurationMs);
    nextScene.transition = normalizeSceneTransition(nextScene);
    return nextScene;
  }

  const cues = buildSceneCues(nextScene.id, narrationText, speechDurationMs);
  const elements = [...(nextScene.elements || [])].sort(elementSort);

  let cursorMs = 120;
  let latestEndMs = 0;
  let cueCursor = 0;

  for (const element of elements) {
    const speechText = elementSpeechText(element);
    const speechMs = estimateSpeechMs(speechText);
    const effect = effectForElement(element);
    const durationMs = baseAnimationDuration(element, effect, speechMs);
    const nextAnimation = element.animation && typeof element.animation === "object" ? { ...element.animation } : {};

    if (element.type === "shape") {
      nextAnimation.effect = effect;
      nextAnimation.startMs = clamp(60 + Math.round((element.y || 0) * 0.08), 40, 380);
      nextAnimation.durationMs = durationMs;
      latestEndMs = Math.max(latestEndMs, nextAnimation.startMs + nextAnimation.durationMs);
      element.animation = nextAnimation;
      continue;
    }

    if (element.type === "chip") {
      nextAnimation.effect = effect;
      nextAnimation.startMs = clamp(40 + Math.round((element.x || 0) * 0.03), 20, 260);
      nextAnimation.durationMs = durationMs;
      latestEndMs = Math.max(latestEndMs, nextAnimation.startMs + nextAnimation.durationMs);
      element.animation = nextAnimation;
      continue;
    }

    const cue = cueForIndex(cues, cueCursor, cursorMs, cursorMs + speechMs);
    let anchorStartMs = cue.startMs;
    const anchorEndMs = cue.endMs;

    if (element.type === "title" || element.type === "stat") {
      anchorStartMs = Math.max(80, anchorStartMs - 50);
    }

    nextAnimation.effect = effect;
    nextAnimation.startMs = clamp(Math.max(cursorMs, anchorStartMs), 80, 10000);
    nextAnimation.durationMs = durationMs;

    if (element.type === "bullet-list") {
      const itemCount = Array.isArray(element.items) && element.items.length > 0 ? element.items.length : 1;
      const cueSlice = cues.slice(cueCursor, cueCursor + itemCount);

      if (cueSlice.length >= 2) {
        const staggerValues = cueSlice.slice(1).map((cueItem, index) => cueItem.startMs - cueSlice[index].startMs);
        const averageStagger = staggerValues.reduce((sum, value) => sum + value, 0) / staggerValues.length;
        nextAnimation.itemStaggerMs = clamp(Math.round(averageStagger), 160, 520);
      } else {
        nextAnimation.itemStaggerMs = clamp(Math.round((speechMs / itemCount) * 0.68), 160, 460);
      }

      const lastCueEndMs = cueSlice.length > 0 ? cueSlice[cueSlice.length - 1].endMs : anchorEndMs;
      const listEndMs = Math.max(
        nextAnimation.startMs + nextAnimation.durationMs + nextAnimation.itemStaggerMs * (itemCount - 1),
        lastCueEndMs
      );
      latestEndMs = Math.max(latestEndMs, listEndMs);
      cursorMs = Math.max(nextAnimation.startMs + 340, lastCueEndMs - 80);
      cueCursor += cueSlice.length > 0 ? cueSlice.length : 1;
    } else {
      latestEndMs = Math.max(latestEndMs, nextAnimation.startMs + nextAnimation.durationMs);
      const carryRatio = element.type === "title" || element.type === "stat" ? 0.48 : 0.42;
      cursorMs = Math.max(nextAnimation.startMs + Math.max(260, Math.round(speechMs * carryRatio)), anchorEndMs - 90);
      cueCursor += cues.length > 0 ? 1 : 0;
    }

    element.animation = nextAnimation;
  }

  nextScene.narration = narrationText;
  nextScene.timingMode = "auto";
  nextScene.cues = cues;
  nextScene.transition = normalizeSceneTransition(nextScene);
  nextScene.durationMs = Math.max(2200, Math.round(Math.max(speechDurationMs + 760, latestEndMs + 420)));
  return nextScene;
}

function normalizeSubtitles(movie) {
  const existing = movie.subtitles && typeof movie.subtitles === "object" ? movie.subtitles : {};
  const stylePreset = VALID_SUBTITLE_PRESETS.has(existing.stylePreset) ? existing.stylePreset : "bottom-band";
  const maxLines = Number.isFinite(existing.maxLines) ? clamp(Math.round(existing.maxLines), 1, 4) : 2;
  const enabled = existing.enabled !== false;

  const tracks = [];
  for (const scene of movie.scenes || []) {
    for (const cue of scene.cues || []) {
      tracks.push({
        id: `subtitle-${cue.id}`,
        sceneId: scene.id,
        cueId: cue.id,
        text: cue.text,
        startMs: cue.startMs,
        endMs: cue.endMs
      });
    }
  }

  return {
    enabled,
    source: "scene-cues",
    stylePreset,
    maxLines,
    tracks
  };
}

function syncMovieTimings(movie) {
  const nextMovie = cloneJson(movie);
  const trackDurationMap = new Map(
    (((nextMovie.audio && nextMovie.audio.tracks) || []).filter((track) => Number.isFinite(track.durationMs))).map((track) => [
      track.sceneId,
      track.durationMs
    ])
  );

  nextMovie.scenes = (nextMovie.scenes || []).map((scene) => {
    const trackDurationMs = trackDurationMap.get(scene.id);
    const syncedScene = syncSceneTimings(scene, { trackDurationMs });
    if (Number.isFinite(trackDurationMs)) {
      syncedScene.durationMs = Math.max(syncedScene.durationMs, Math.ceil(trackDurationMs + 420));
      syncedScene.cues = buildSceneCues(syncedScene.id, syncedScene.narration, trackDurationMs);
    }
    return syncedScene;
  });
  nextMovie.subtitles = normalizeSubtitles(nextMovie);
  return nextMovie;
}

module.exports = {
  buildSceneCues,
  deriveNarrationText,
  elementSpeechText,
  estimateSpeechMs,
  normalizeSceneTransition,
  splitNarrationIntoCueTexts,
  syncMovieTimings,
  syncSceneTimings
};

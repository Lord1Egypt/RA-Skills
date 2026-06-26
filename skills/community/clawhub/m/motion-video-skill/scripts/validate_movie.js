const fs = require("fs");
const path = require("path");
const {
  DEFAULT_TEMPLATE,
  PREVIEW_HEIGHT,
  PREVIEW_WIDTH,
  VALID_EFFECTS,
  VALID_ELEMENT_TYPES,
  VALID_SCENE_TRANSITIONS,
  VALID_SCENE_TYPES,
  VALID_SUBTITLE_PRESETS,
  getMoviePath,
  readJson,
  resolveTemplate,
  resolveTheme
} = require("./common");
const { syncMovieTimings } = require("./timing");

function pushError(errors, scope, message) {
  errors.push(`${scope}: ${message}`);
}

function validateElement(element, scope, errors) {
  if (!element || typeof element !== "object") {
    pushError(errors, scope, "element must be an object");
    return;
  }

  if (!element.id || typeof element.id !== "string") {
    pushError(errors, scope, "missing string id");
  }

  if (!VALID_ELEMENT_TYPES.has(element.type)) {
    pushError(errors, scope, `unsupported element type "${element.type}"`);
  }

  for (const key of ["x", "y", "w", "h"]) {
    if (!Number.isFinite(element[key])) {
      pushError(errors, scope, `field "${key}" must be a number`);
    }
  }

  if (element.type === "bullet-list" && !Array.isArray(element.items)) {
    pushError(errors, scope, 'bullet-list must contain "items" array');
  }

  if (element.type === "stat" && typeof element.value !== "string") {
    pushError(errors, scope, 'stat must contain string "value"');
  }

  if (["title", "subtitle", "text", "chip", "quote"].includes(element.type) && typeof element.text !== "string") {
    pushError(errors, scope, `type "${element.type}" must contain string "text"`);
  }

  if (element.animation !== undefined) {
    if (!element.animation || typeof element.animation !== "object") {
      pushError(errors, scope, '"animation" must be an object');
    } else {
      if (!VALID_EFFECTS.has(element.animation.effect)) {
        pushError(errors, scope, `unsupported animation effect "${element.animation.effect}"`);
      }
      if (!Number.isFinite(element.animation.startMs) || element.animation.startMs < 0) {
        pushError(errors, scope, '"animation.startMs" must be a non-negative number');
      }
      if (!Number.isFinite(element.animation.durationMs) || element.animation.durationMs <= 0) {
        pushError(errors, scope, '"animation.durationMs" must be a positive number');
      }
      if (
        element.animation.itemStaggerMs !== undefined &&
        (!Number.isFinite(element.animation.itemStaggerMs) || element.animation.itemStaggerMs < 0)
      ) {
        pushError(errors, scope, '"animation.itemStaggerMs" must be a non-negative number');
      }
    }
  }
}

function validateScene(scene, sceneIndex, errors) {
  const scope = `scene[${sceneIndex}]`;
  if (!scene || typeof scene !== "object") {
    pushError(errors, scope, "scene must be an object");
    return;
  }

  if (!scene.id || typeof scene.id !== "string") {
    pushError(errors, scope, "missing string id");
  }

  if (!VALID_SCENE_TYPES.has(scene.type)) {
    pushError(errors, scope, `unsupported scene type "${scene.type}"`);
  }

  if (!Number.isFinite(scene.durationMs) || scene.durationMs <= 0) {
    pushError(errors, scope, '"durationMs" must be a positive number');
  }

  if (!Array.isArray(scene.elements) || scene.elements.length === 0) {
    pushError(errors, scope, '"elements" must be a non-empty array');
    return;
  }

  if (scene.transition !== undefined) {
    if (!scene.transition || typeof scene.transition !== "object" || Array.isArray(scene.transition)) {
      pushError(errors, scope, '"transition" must be an object');
    } else {
      if (!VALID_SCENE_TRANSITIONS.has(scene.transition.enterEffect)) {
        pushError(errors, scope, `unsupported transition enterEffect "${scene.transition.enterEffect}"`);
      }
      if (!VALID_SCENE_TRANSITIONS.has(scene.transition.exitEffect)) {
        pushError(errors, scope, `unsupported transition exitEffect "${scene.transition.exitEffect}"`);
      }
      if (!Number.isFinite(scene.transition.enterDurationMs) || scene.transition.enterDurationMs <= 0) {
        pushError(errors, scope, '"transition.enterDurationMs" must be a positive number');
      }
      if (!Number.isFinite(scene.transition.exitDurationMs) || scene.transition.exitDurationMs <= 0) {
        pushError(errors, scope, '"transition.exitDurationMs" must be a positive number');
      }
    }
  }

  if (scene.cues !== undefined) {
    if (!Array.isArray(scene.cues)) {
      pushError(errors, scope, '"cues" must be an array');
    } else {
      scene.cues.forEach((cue, cueIndex) => {
        if (!cue || typeof cue !== "object") {
          pushError(errors, `${scope}.cues[${cueIndex}]`, "cue must be an object");
          return;
        }
        if (typeof cue.id !== "string" || !cue.id) {
          pushError(errors, `${scope}.cues[${cueIndex}]`, 'cue.id must be a non-empty string');
        }
        if (typeof cue.text !== "string" || !cue.text.trim()) {
          pushError(errors, `${scope}.cues[${cueIndex}]`, 'cue.text must be a non-empty string');
        }
        if (!Number.isFinite(cue.startMs) || cue.startMs < 0) {
          pushError(errors, `${scope}.cues[${cueIndex}]`, 'cue.startMs must be a non-negative number');
        }
        if (!Number.isFinite(cue.endMs) || cue.endMs <= cue.startMs) {
          pushError(errors, `${scope}.cues[${cueIndex}]`, "cue.endMs must be greater than cue.startMs");
        }
      });
    }
  }

  scene.elements.forEach((element, elementIndex) => validateElement(element, `${scope}.elements[${elementIndex}]`, errors));
}

function validateMovie(movie, moviePath) {
  const normalizedMovie = syncMovieTimings(movie);
  const errors = [];

  if (!normalizedMovie || typeof normalizedMovie !== "object") {
    errors.push("movie must be an object");
    return errors;
  }

  if (!normalizedMovie.meta || typeof normalizedMovie.meta !== "object") {
    errors.push("missing meta object");
  } else {
    if (typeof normalizedMovie.meta.title !== "string" || !normalizedMovie.meta.title.trim()) {
      errors.push("meta.title must be a non-empty string");
    }
    if (!Number.isFinite(normalizedMovie.meta.fps) || normalizedMovie.meta.fps <= 0) {
      errors.push("meta.fps must be a positive number");
    }
    if (normalizedMovie.meta.width !== PREVIEW_WIDTH) {
      errors.push(`meta.width must be ${PREVIEW_WIDTH}`);
    }
    if (normalizedMovie.meta.height !== PREVIEW_HEIGHT) {
      errors.push(`meta.height must be ${PREVIEW_HEIGHT}`);
    }
    try {
      resolveTemplate(normalizedMovie.meta.template || DEFAULT_TEMPLATE);
    } catch (error) {
      errors.push(error.message);
    }
    if (normalizedMovie.meta.theme) {
      try {
        resolveTheme(normalizedMovie.meta.theme);
      } catch (error) {
        errors.push(error.message);
      }
    }
  }

  if (normalizedMovie.audio !== undefined) {
    const audio = normalizedMovie.audio;
    if (!audio || typeof audio !== "object") {
      errors.push("audio must be an object");
    } else {
      const validStatuses = new Set(["pending", "confirmed", "synthesized"]);
      if (audio.enabled !== undefined && typeof audio.enabled !== "boolean") {
        errors.push("audio.enabled must be a boolean");
      }
      if (audio.mode !== undefined && !["tts"].includes(audio.mode)) {
        errors.push('audio.mode must be "tts" when present');
      }
      if (audio.confirmationRequired !== undefined && typeof audio.confirmationRequired !== "boolean") {
        errors.push("audio.confirmationRequired must be a boolean");
      }
      if (audio.confirmationStatus !== undefined && !validStatuses.has(audio.confirmationStatus)) {
        errors.push('audio.confirmationStatus must be one of "pending", "confirmed", "synthesized"');
      }
      if (audio.provider !== undefined && audio.provider !== null && typeof audio.provider !== "string") {
        errors.push("audio.provider must be a string or null");
      }
      if (audio.voice !== undefined && audio.voice !== null && typeof audio.voice !== "string") {
        errors.push("audio.voice must be a string or null");
      }
      if (audio.language !== undefined && typeof audio.language !== "string") {
        errors.push("audio.language must be a string");
      }
      if (audio.speed !== undefined && (!Number.isFinite(audio.speed) || audio.speed <= 0)) {
        errors.push("audio.speed must be a positive number");
      }
      if (audio.fallbackProvider !== undefined && audio.fallbackProvider !== null && typeof audio.fallbackProvider !== "string") {
        errors.push("audio.fallbackProvider must be a string or null");
      }
      if (audio.outputDir !== undefined && typeof audio.outputDir !== "string") {
        errors.push("audio.outputDir must be a string");
      }
      if (audio.providerConfig !== undefined && (!audio.providerConfig || typeof audio.providerConfig !== "object" || Array.isArray(audio.providerConfig))) {
        errors.push("audio.providerConfig must be an object");
      }
      if (["confirmed", "synthesized"].includes(audio.confirmationStatus) && (!audio.provider || typeof audio.provider !== "string")) {
        errors.push("audio.provider must be a non-empty string once TTS is confirmed");
      }
      if (["confirmed", "synthesized"].includes(audio.confirmationStatus) && (!audio.voice || typeof audio.voice !== "string")) {
        errors.push("audio.voice must be a non-empty string once TTS is confirmed");
      }
      if (audio.tracks !== undefined) {
        if (!Array.isArray(audio.tracks)) {
          errors.push("audio.tracks must be an array");
        } else {
          audio.tracks.forEach((track, index) => {
            if (!track || typeof track !== "object") {
              errors.push(`audio.tracks[${index}] must be an object`);
              return;
            }
            if (typeof track.sceneId !== "string" || !track.sceneId) {
              errors.push(`audio.tracks[${index}].sceneId must be a non-empty string`);
            }
            if (typeof track.text !== "string") {
              errors.push(`audio.tracks[${index}].text must be a string`);
            }
            if (typeof track.file !== "string" || !track.file) {
              errors.push(`audio.tracks[${index}].file must be a non-empty string`);
            }
            if (track.durationMs !== undefined && (!Number.isFinite(track.durationMs) || track.durationMs <= 0)) {
              errors.push(`audio.tracks[${index}].durationMs must be a positive number when present`);
            }
          });
        }
      }
    }
  }

  if (normalizedMovie.subtitles !== undefined) {
    const subtitles = normalizedMovie.subtitles;
    if (!subtitles || typeof subtitles !== "object" || Array.isArray(subtitles)) {
      errors.push("subtitles must be an object");
    } else {
      if (subtitles.enabled !== undefined && typeof subtitles.enabled !== "boolean") {
        errors.push("subtitles.enabled must be a boolean");
      }
      if (subtitles.source !== undefined && typeof subtitles.source !== "string") {
        errors.push("subtitles.source must be a string");
      }
      if (subtitles.stylePreset !== undefined && !VALID_SUBTITLE_PRESETS.has(subtitles.stylePreset)) {
        errors.push(`subtitles.stylePreset must be one of: ${Array.from(VALID_SUBTITLE_PRESETS).join(", ")}`);
      }
      if (subtitles.maxLines !== undefined && (!Number.isFinite(subtitles.maxLines) || subtitles.maxLines <= 0)) {
        errors.push("subtitles.maxLines must be a positive number");
      }
      if (subtitles.tracks !== undefined) {
        if (!Array.isArray(subtitles.tracks)) {
          errors.push("subtitles.tracks must be an array");
        } else {
          subtitles.tracks.forEach((track, index) => {
            if (!track || typeof track !== "object") {
              errors.push(`subtitles.tracks[${index}] must be an object`);
              return;
            }
            if (typeof track.id !== "string" || !track.id) {
              errors.push(`subtitles.tracks[${index}].id must be a non-empty string`);
            }
            if (typeof track.sceneId !== "string" || !track.sceneId) {
              errors.push(`subtitles.tracks[${index}].sceneId must be a non-empty string`);
            }
            if (typeof track.cueId !== "string" || !track.cueId) {
              errors.push(`subtitles.tracks[${index}].cueId must be a non-empty string`);
            }
            if (typeof track.text !== "string" || !track.text.trim()) {
              errors.push(`subtitles.tracks[${index}].text must be a non-empty string`);
            }
            if (!Number.isFinite(track.startMs) || track.startMs < 0) {
              errors.push(`subtitles.tracks[${index}].startMs must be a non-negative number`);
            }
            if (!Number.isFinite(track.endMs) || track.endMs <= track.startMs) {
              errors.push(`subtitles.tracks[${index}].endMs must be greater than startMs`);
            }
          });
        }
      }
    }
  }

  if (!Array.isArray(normalizedMovie.scenes) || normalizedMovie.scenes.length === 0) {
    errors.push("scenes must be a non-empty array");
  } else {
    normalizedMovie.scenes.forEach((scene, index) => validateScene(scene, index, errors));
  }

  if (!fs.existsSync(path.resolve(moviePath))) {
    errors.push(`file not found: ${moviePath}`);
  }

  return errors;
}

if (require.main === module) {
  const target = process.argv[2];
  if (!target) {
    console.error("Usage: node scripts/validate_movie.js <movie.json | project-dir>");
    process.exit(1);
  }

  const moviePath = getMoviePath(target);
  const movie = syncMovieTimings(readJson(moviePath));
  const errors = validateMovie(movie, moviePath);

  if (errors.length > 0) {
    console.error(`Validation failed for ${moviePath}`);
    for (const error of errors) {
      console.error(`- ${error}`);
    }
    process.exit(1);
  }

  console.log(`Validated ${moviePath} successfully.`);
}

module.exports = {
  validateMovie
};

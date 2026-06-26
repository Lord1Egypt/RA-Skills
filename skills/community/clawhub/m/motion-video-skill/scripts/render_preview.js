const path = require("path");
const { pathToFileURL } = require("url");
const {
  DEFAULT_TEMPLATE,
  PREVIEW_HEIGHT,
  PREVIEW_WIDTH,
  computeTimeline,
  escapeHtml,
  formatDuration,
  getMoviePath,
  loadBaseCss,
  readJson,
  resolveTemplate,
  resolveTheme,
  writeText
} = require("./common");
const { syncMovieTimings } = require("./timing");
const { validateMovie } = require("./validate_movie");

function buildPreviewHtml(movie) {
  const template = resolveTemplate(movie.meta.template || DEFAULT_TEMPLATE);
  const theme = resolveTheme(movie.meta.theme || template.theme || "signal-ink");
  const css = loadBaseCss();
  const timeline = computeTimeline(movie);
  const frameCount = Math.max(1, Math.ceil((timeline.totalDurationMs / 1000) * (movie.meta.fps || 30)));
  const subtitlePreset =
    movie.subtitles && typeof movie.subtitles.stylePreset === "string" ? movie.subtitles.stylePreset : "bottom-band";
  const subtitleTrackCount = movie.subtitles && Array.isArray(movie.subtitles.tracks) ? movie.subtitles.tracks.length : 0;
  const subtitleChip =
    movie.subtitles && movie.subtitles.enabled !== false
      ? `<span class="meta-chip">subtitles ${subtitleTrackCount}</span>`
      : "";

  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${escapeHtml(movie.meta.title)}</title>
  <style>${css}</style>
</head>
<body>
  <main class="page">
    <section class="preview-shell">
      <div class="stage-shell">
        <div
          id="stage"
          class="stage ${escapeHtml(template.stageClass || "")}"
          style="--movie-bg:${escapeHtml(theme.bg)};--movie-surface:${escapeHtml(theme.surface)};--movie-surfaceStrong:${escapeHtml(
            theme.surfaceStrong
          )};--movie-text-primary:${escapeHtml(theme.textPrimary)};--movie-text-secondary:${escapeHtml(
            theme.textSecondary
          )};--movie-accent:${escapeHtml(theme.accent)};--movie-accent-soft:${escapeHtml(
            theme.accentSoft
          )};--movie-accent-alt:${escapeHtml(theme.accentAlt)};--movie-outline:${escapeHtml(theme.outline)};--movie-shadow:${escapeHtml(
            theme.shadow
          )};--movie-font-display:${escapeHtml(theme.fontDisplay)};--movie-font-body:${escapeHtml(
            theme.fontBody
          )};--movie-panel-bg:${escapeHtml(template.panelBg || "rgba(10, 15, 28, 0.74)")};--movie-panel-outline:${escapeHtml(
            template.panelOutline || "rgba(148, 163, 184, 0.18)"
          )};--movie-stage-border:${escapeHtml(template.stageBorder || "rgba(255,255,255,0.06)")};--movie-stage-radius:${escapeHtml(
            String(template.stageRadius || 30) + "px"
          )};--movie-card-radius:${escapeHtml(String(template.cardRadius || 28) + "px")};--movie-chip-radius:${escapeHtml(
            String(template.chipRadius || 999) + "px"
          )};--movie-quote-font-style:${escapeHtml(template.quoteFontStyle || "normal")};"
        >
          <div id="subtitle-layer" class="subtitle-layer subtitle-preset-${escapeHtml(subtitlePreset)}" style="--subtitle-max-lines:${escapeHtml(
            String((movie.subtitles && movie.subtitles.maxLines) || 2)
          )};">
            <div id="subtitle-text" class="subtitle-text"></div>
          </div>
        </div>
      </div>
      <div class="controls">
        <div class="controls-top">
          <div class="meta">
            <span class="meta-chip">${escapeHtml(movie.meta.title)}</span>
            <span class="meta-chip">${escapeHtml(template.label)}</span>
            <span class="meta-chip">${timeline.scenes.length} scenes</span>
            ${subtitleChip}
            <span class="meta-chip">${formatDuration(timeline.totalDurationMs)}</span>
            <span class="meta-chip">${movie.meta.fps} fps</span>
            <span class="meta-chip">${frameCount} frames</span>
          </div>
          <button id="play-toggle" type="button">Play</button>
        </div>
        <div class="time-readout" id="time-readout">00:00 / ${formatDuration(timeline.totalDurationMs)}</div>
        <div class="timeline">
          <input id="timeline-range" type="range" min="0" max="${timeline.totalDurationMs}" value="0" step="1" />
        </div>
      </div>
    </section>
  </main>
  <script>
    const MOVIE = ${JSON.stringify(movie)};
    const TIMELINE = ${JSON.stringify(timeline)};
    const STAGE_WIDTH = ${PREVIEW_WIDTH};
    const STAGE_HEIGHT = ${PREVIEW_HEIGHT};
    const DEFAULT_FONT_DISPLAY = ${JSON.stringify(theme.fontDisplay)};
    const DEFAULT_FONT_BODY = ${JSON.stringify(theme.fontBody)};

    const stage = document.getElementById("stage");
    const playToggle = document.getElementById("play-toggle");
    const timelineRange = document.getElementById("timeline-range");
    const timeReadout = document.getElementById("time-readout");
    const subtitleLayer = document.getElementById("subtitle-layer");
    const subtitleText = document.getElementById("subtitle-text");

    let isPlaying = false;
    let currentTimeMs = 0;
    let rafId = null;
    let lastTick = null;
    const sceneViews = [];
    const sceneStartMap = new Map(TIMELINE.scenes.map((scene) => [scene.id, scene.startMs]));
    const subtitleTrack =
      MOVIE.subtitles && MOVIE.subtitles.enabled !== false && Array.isArray(MOVIE.subtitles.tracks)
        ? MOVIE.subtitles.tracks
            .map((track) => {
              const sceneStartMs = sceneStartMap.get(track.sceneId) || 0;
              return {
                ...track,
                globalStartMs: sceneStartMs + track.startMs,
                globalEndMs: sceneStartMs + track.endMs
              };
            })
            .sort((left, right) => left.globalStartMs - right.globalStartMs)
        : [];

    function clamp(value, min, max) {
      return Math.max(min, Math.min(max, value));
    }

    function formatDurationMs(ms) {
      const totalSeconds = Math.max(0, Math.floor(ms / 1000));
      const minutes = Math.floor(totalSeconds / 60);
      const seconds = totalSeconds % 60;
      return String(minutes).padStart(2, "0") + ":" + String(seconds).padStart(2, "0");
    }

    function easeOutCubic(value) {
      return 1 - Math.pow(1 - value, 3);
    }

    function applyRect(node, element) {
      node.style.left = element.x + "px";
      node.style.top = element.y + "px";
      node.style.width = element.w + "px";
      node.style.height = element.h + "px";
    }

    function applyStyle(node, style = {}, fallbackType) {
      node.style.color = style.color || "";
      node.style.background = style.background || "";
      node.style.fontSize = style.fontSize ? style.fontSize + "px" : "";
      node.style.fontWeight = style.fontWeight || "";
      node.style.textAlign = style.textAlign || "";
      node.style.lineHeight = style.lineHeight ? String(style.lineHeight) : "";
      node.style.letterSpacing = style.letterSpacing || "";
      node.style.borderRadius = style.borderRadius ? style.borderRadius + "px" : "";
      node.style.padding = style.padding ? style.padding + "px" : "";
      node.style.border = style.borderColor ? "1px solid " + style.borderColor : "";
      node.style.opacity = style.opacity !== undefined ? String(style.opacity) : "";
      node.style.fontFamily = fallbackType === "title" ? DEFAULT_FONT_DISPLAY : DEFAULT_FONT_BODY;
    }

    function createElementNode(element) {
      const node = document.createElement("div");
      node.className = "element " + element.type;
      node.dataset.elementType = element.type;
      applyRect(node, element);
      applyStyle(node, element.style || {}, element.type);

      if (element.type === "bullet-list") {
        const list = document.createElement("ul");
        const itemNodes = [];
        for (const item of element.items || []) {
          const li = document.createElement("li");
          li.textContent = item;
          list.appendChild(li);
          itemNodes.push(li);
        }
        node.appendChild(list);
        node.__items = itemNodes;
      } else if (element.type === "stat") {
        const value = document.createElement("div");
        value.className = "stat-value";
        value.textContent = element.value || "";
        const label = document.createElement("div");
        label.className = "stat-label";
        label.textContent = element.text || "";
        node.appendChild(value);
        node.appendChild(label);
      } else if (element.type === "shape") {
        node.setAttribute("aria-hidden", "true");
      } else {
        node.textContent = element.text || "";
      }

      return node;
    }

    function createSceneView(scene) {
      const sceneNode = document.createElement("section");
      sceneNode.className = "scene";
      const contentNode = document.createElement("div");
      contentNode.className = "scene-content";
      sceneNode.appendChild(contentNode);

      if (scene.background && scene.background.gradient) {
        sceneNode.style.background = scene.background.gradient;
      }

      const elementViews = [];
      for (const element of scene.elements || []) {
        const node = createElementNode(element);
        contentNode.appendChild(node);
        elementViews.push({ element, node });
      }

      stage.appendChild(sceneNode);
      return { scene, node: sceneNode, elementViews };
    }

    function animationConfig(element) {
      const animation = element.animation || {};
      return {
        effect: animation.effect || "fade",
        startMs: Number.isFinite(animation.startMs) ? animation.startMs : 0,
        durationMs: Number.isFinite(animation.durationMs) ? animation.durationMs : 500,
        itemStaggerMs: Number.isFinite(animation.itemStaggerMs) ? animation.itemStaggerMs : 0
      };
    }

    function transitionConfig(scene) {
      const transition = scene.transition || {};
      return {
        enterEffect: transition.enterEffect || "fade",
        exitEffect: transition.exitEffect || "fade",
        enterDurationMs: Number.isFinite(transition.enterDurationMs) ? transition.enterDurationMs : 280,
        exitDurationMs: Number.isFinite(transition.exitDurationMs) ? transition.exitDurationMs : 220
      };
    }

    function getEffectState(effect, progress) {
      const eased = easeOutCubic(progress);
      const visible = progress > 0.001;
      const hidden = 1 - eased;
      const state = {
        opacity: visible ? eased : 0,
        transform: "translate3d(0, 0, 0) scale(1)",
        clipPath: "inset(0 0 0 0 round 0px)",
        boxShadow: "",
        filter: ""
      };

      if (effect === "fade-up") {
        state.transform = "translate3d(0, " + Math.round(hidden * 32) + "px, 0)";
      } else if (effect === "slide-left") {
        state.transform = "translate3d(" + Math.round(hidden * 42) + "px, 0, 0)";
      } else if (effect === "slide-right") {
        state.transform = "translate3d(" + Math.round(-hidden * 42) + "px, 0, 0)";
      } else if (effect === "pop") {
        state.transform = "translate3d(0, 0, 0) scale(" + (0.84 + eased * 0.16).toFixed(3) + ")";
      } else if (effect === "clip-up") {
        state.opacity = visible ? 1 : 0;
        state.clipPath = "inset(" + Math.round(hidden * 100) + "% 0 0 0 round 0px)";
      } else if (effect === "zoom-in") {
        state.transform = "translate3d(0, 0, 0) scale(" + (1.12 - eased * 0.12).toFixed(3) + ")";
      } else if (effect === "blur-in") {
        state.transform = "translate3d(0, " + Math.round(hidden * 18) + "px, 0) scale(" + (0.97 + eased * 0.03).toFixed(3) + ")";
        state.filter = "blur(" + (hidden * 16).toFixed(1) + "px)";
      } else if (effect === "glow-pop") {
        state.opacity = visible ? 0.6 + eased * 0.4 : 0;
        state.transform = "translate3d(0, 0, 0) scale(" + (0.72 + eased * 0.28).toFixed(3) + ")";
        state.boxShadow = "0 0 " + Math.round(34 + eased * 16) + "px rgba(255, 255, 255, 0.16)";
      } else if (effect === "swing-up") {
        state.transform =
          "translate3d(0, " + Math.round(hidden * 30) + "px, 0) rotate(" + (-hidden * 6).toFixed(2) + "deg)";
      } else if (effect === "reveal-right") {
        state.opacity = visible ? 1 : 0;
        state.clipPath = "inset(0 " + Math.round(hidden * 100) + "% 0 0 round 0px)";
      } else if (effect === "reveal-down") {
        state.opacity = visible ? 1 : 0;
        state.clipPath = "inset(0 0 " + Math.round(hidden * 100) + "% 0 round 0px)";
      }

      return state;
    }

    function getSceneTransitionState(effect, progress, phase) {
      const eased = easeOutCubic(progress);
      const hidden = 1 - eased;
      const direction = phase === "exit" ? -1 : 1;
      const state = {
        opacity: eased,
        transform: "translate3d(0, 0, 0) scale(1)",
        clipPath: "inset(0 0 0 0 round 0px)",
        filter: ""
      };

      if (effect === "slide-left") {
        state.transform = "translate3d(" + Math.round(hidden * 74 * direction) + "px, 0, 0)";
      } else if (effect === "slide-right") {
        state.transform = "translate3d(" + Math.round(-hidden * 74 * direction) + "px, 0, 0)";
      } else if (effect === "lift-up") {
        state.transform = "translate3d(0, " + Math.round(hidden * 68) + "px, 0)";
      } else if (effect === "zoom-in") {
        state.transform = "translate3d(0, 0, 0) scale(" + (1.1 - eased * 0.1).toFixed(3) + ")";
      } else if (effect === "zoom-out") {
        state.transform = "translate3d(0, 0, 0) scale(" + (0.92 + eased * 0.08).toFixed(3) + ")";
      } else if (effect === "blur-in") {
        state.filter = "blur(" + (hidden * 18).toFixed(1) + "px)";
        state.transform = "translate3d(0, " + Math.round(hidden * 30) + "px, 0)";
      } else if (effect === "wipe-left") {
        state.opacity = 1;
        state.clipPath = "inset(0 " + Math.round(hidden * 100) + "% 0 0 round 0px)";
      } else if (effect === "wipe-up") {
        state.opacity = 1;
        state.clipPath = "inset(" + Math.round(hidden * 100) + "% 0 0 0 round 0px)";
      } else if (effect === "iris-in") {
        state.opacity = 1;
        state.clipPath = "circle(" + (20 + eased * 86).toFixed(2) + "% at 50% 50%)";
      }

      if (phase === "exit" && (effect === "fade" || effect === "blur-in")) {
        state.opacity = progress;
      }

      return state;
    }

    function getSceneFrameState(scene, localTime) {
      const transition = transitionConfig(scene);
      if (localTime <= transition.enterDurationMs) {
        const progress = clamp(localTime / transition.enterDurationMs, 0, 1);
        return getSceneTransitionState(transition.enterEffect, progress, "enter");
      }
      if (scene.durationMs - localTime <= transition.exitDurationMs) {
        const progress = clamp((scene.durationMs - localTime) / transition.exitDurationMs, 0, 1);
        return getSceneTransitionState(transition.exitEffect, progress, "exit");
      }

      return {
        opacity: 1,
        transform: "translate3d(0, 0, 0) scale(1)",
        clipPath: "inset(0 0 0 0 round 0px)",
        filter: ""
      };
    }

    function findActiveSubtitle(timeMs) {
      for (const track of subtitleTrack) {
        if (timeMs >= track.globalStartMs && timeMs <= track.globalEndMs) {
          return track;
        }
      }
      return null;
    }

    function renderSubtitle(timeMs) {
      if (!subtitleTrack.length) {
        subtitleLayer.dataset.visible = "false";
        subtitleText.textContent = "";
        subtitleLayer.style.opacity = "0";
        subtitleLayer.style.transform = "translate3d(-50%, 16px, 0) scale(0.98)";
        return;
      }

      const activeTrack = findActiveSubtitle(timeMs);
      if (!activeTrack) {
        subtitleLayer.dataset.visible = "false";
        subtitleText.textContent = "";
        subtitleLayer.style.opacity = "0";
        subtitleLayer.style.transform = "translate3d(-50%, 16px, 0) scale(0.98)";
        return;
      }

      const durationMs = Math.max(240, activeTrack.globalEndMs - activeTrack.globalStartMs);
      const fadeIn = clamp((timeMs - activeTrack.globalStartMs) / 140, 0, 1);
      const fadeOut = clamp((activeTrack.globalEndMs - timeMs) / 180, 0, 1);
      const visibility = Math.min(fadeIn, fadeOut);
      const progress = clamp((timeMs - activeTrack.globalStartMs) / durationMs, 0, 1);
      const eased = easeOutCubic(progress);

      subtitleLayer.dataset.visible = "true";
      subtitleText.textContent = activeTrack.text;
      subtitleLayer.style.opacity = String(visibility);
      subtitleLayer.style.transform =
        "translate3d(-50%, " + Math.round((1 - eased) * 10) + "px, 0) scale(" + (0.98 + eased * 0.02).toFixed(3) + ")";
    }

    function applyElementFrame(view, localTime) {
      const element = view.element;
      const node = view.node;
      const animation = animationConfig(element);
      const progress = clamp((localTime - animation.startMs) / animation.durationMs, 0, 1);
      const state = getEffectState(animation.effect, progress);

      node.style.opacity = String(state.opacity);
      node.style.transform = state.transform;
      node.style.clipPath = state.clipPath;
      node.style.boxShadow = state.boxShadow;
      node.style.filter = state.filter;

      if (element.type === "bullet-list" && Array.isArray(node.__items) && node.__items.length > 0) {
        node.__items.forEach((itemNode, itemIndex) => {
          const itemStart = animation.startMs + itemIndex * animation.itemStaggerMs;
          const itemProgress = clamp((localTime - itemStart) / animation.durationMs, 0, 1);
          const itemState = getEffectState(animation.effect, itemProgress);
          itemNode.style.opacity = String(itemState.opacity);
          itemNode.style.transform = itemState.transform;
          itemNode.style.clipPath = itemState.clipPath;
          itemNode.style.filter = itemState.filter;
        });
      }
    }

    function renderAt(timeMs) {
      currentTimeMs = clamp(timeMs, 0, TIMELINE.totalDurationMs);
      timelineRange.value = String(currentTimeMs);
      timeReadout.textContent = formatDurationMs(currentTimeMs) + " / " + formatDurationMs(TIMELINE.totalDurationMs);

      for (const view of sceneViews) {
        const localTime = currentTimeMs - view.scene.startMs;
        const isActive = localTime >= 0 && localTime <= view.scene.durationMs;
        if (!isActive) {
          view.node.style.opacity = "0";
          view.node.style.transform = "translate3d(0, 0, 0) scale(1)";
          view.node.style.clipPath = "inset(0 0 0 0 round 0px)";
          view.node.style.filter = "";
          continue;
        }

        const sceneState = getSceneFrameState(view.scene, localTime);
        view.node.style.opacity = String(sceneState.opacity);
        view.node.style.transform = sceneState.transform;
        view.node.style.clipPath = sceneState.clipPath;
        view.node.style.filter = sceneState.filter;

        for (const elementView of view.elementViews) {
          applyElementFrame(elementView, localTime);
        }
      }

      renderSubtitle(currentTimeMs);
    }

    function tick(timestamp) {
      if (!isPlaying) {
        return;
      }

      if (lastTick === null) {
        lastTick = timestamp;
      }

      const delta = timestamp - lastTick;
      lastTick = timestamp;
      const nextTime = currentTimeMs + delta;

      if (nextTime >= TIMELINE.totalDurationMs) {
        renderAt(TIMELINE.totalDurationMs);
        isPlaying = false;
        playToggle.textContent = "Play";
        lastTick = null;
        rafId = null;
        return;
      }

      renderAt(nextTime);
      rafId = window.requestAnimationFrame(tick);
    }

    function setPlaying(nextValue) {
      isPlaying = nextValue;
      playToggle.textContent = isPlaying ? "Pause" : "Play";
      if (isPlaying) {
        lastTick = null;
        rafId = window.requestAnimationFrame(tick);
      } else if (rafId !== null) {
        window.cancelAnimationFrame(rafId);
        rafId = null;
      }
    }

    function bootstrap() {
      for (const scene of TIMELINE.scenes) {
        sceneViews.push(createSceneView(scene));
      }

      playToggle.addEventListener("click", () => {
        if (currentTimeMs >= TIMELINE.totalDurationMs && !isPlaying) {
          renderAt(0);
        }
        setPlaying(!isPlaying);
      });

      timelineRange.addEventListener("input", () => {
        setPlaying(false);
        renderAt(Number(timelineRange.value));
      });

      renderAt(0);
      window.__setMovieTime = (ms) => {
        setPlaying(false);
        renderAt(ms);
      };
      window.__getMovieDuration = () => TIMELINE.totalDurationMs;
      window.__MOVIE_READY = true;
    }

    bootstrap();
  </script>
</body>
</html>`;
}

if (require.main === module) {
  const source = process.argv[2];
  const outputPath = process.argv[3];

  if (!source || !outputPath) {
    console.error("Usage: node scripts/render_preview.js <movie.json | project-dir> <output.html>");
    process.exit(1);
  }

  const moviePath = getMoviePath(source);
  const movie = syncMovieTimings(readJson(moviePath));
  const errors = validateMovie(movie, moviePath);
  if (errors.length > 0) {
    console.error(`Validation failed for ${moviePath}`);
    for (const error of errors) {
      console.error(`- ${error}`);
    }
    process.exit(1);
  }

  writeText(outputPath, buildPreviewHtml(movie));
  console.log(`Preview written to ${path.resolve(outputPath)}`);
  console.log(`Open in browser: ${pathToFileURL(path.resolve(outputPath)).href}`);
}

module.exports = {
  buildPreviewHtml
};

const path = require("path");
const { DEFAULT_TEMPLATE, PREVIEW_HEIGHT, PREVIEW_WIDTH, ensureDir, resolveTemplate, slugify, writeText } = require("./common");

function createStarterMovie({ title, theme, templateId }) {
  return {
    meta: {
      title,
      theme,
      template: templateId,
      ratio: "16:9",
      fps: 30,
      width: PREVIEW_WIDTH,
      height: PREVIEW_HEIGHT
    },
    audio: {
      enabled: false,
      mode: "tts",
      confirmationRequired: true,
      confirmationStatus: "pending",
      provider: null,
      voice: null,
      language: "zh-CN",
      speed: 1,
      fallbackProvider: "system",
      outputDir: "audio",
      tracks: []
    },
    subtitles: {
      enabled: true,
      source: "scene-cues",
      stylePreset: "bottom-band",
      maxLines: 2,
      tracks: []
    },
    scenes: [
      {
        id: "scene-01",
        label: "开场",
        type: "hero",
        transition: {
          enterEffect: "zoom-out",
          exitEffect: "fade",
          enterDurationMs: 360,
          exitDurationMs: 220
        },
        durationMs: 2800,
        narration: "先用一句话说清这个视频的主题。",
        elements: [
          {
            id: "scene-01-chip",
            type: "chip",
            text: "topic intro",
            x: 92,
            y: 90,
            w: 200,
            h: 42,
            animation: {
              effect: "fade",
              startMs: 0,
              durationMs: 360
            }
          },
          {
            id: "scene-01-title",
            type: "title",
            text: title,
            x: 92,
            y: 150,
            w: 760,
            h: 168,
            animation: {
              effect: "fade-up",
              startMs: 160,
              durationMs: 620
            }
          },
          {
            id: "scene-01-subtitle",
            type: "subtitle",
            text: "把原始文本拆成重点，再给重点安排合适的镜头和动效。",
            x: 94,
            y: 352,
            w: 640,
            h: 84,
            animation: {
              effect: "blur-in",
              startMs: 480,
              durationMs: 520
            }
          }
        ]
      },
      {
        id: "scene-02",
        label: "步骤",
        type: "steps",
        transition: {
          enterEffect: "lift-up",
          exitEffect: "fade",
          enterDurationMs: 300,
          exitDurationMs: 220
        },
        durationMs: 3200,
        narration: "把流程拆成三段逐步讲。",
        elements: [
          {
            id: "scene-02-title",
            type: "title",
            text: "先把内容拆成三步",
            x: 92,
            y: 108,
            w: 760,
            h: 96,
            style: {
              fontSize: 56
            },
            animation: {
              effect: "swing-up",
              startMs: 120,
              durationMs: 560
            }
          },
          {
            id: "scene-02-list",
            type: "bullet-list",
            items: ["提炼主结论", "拆成分镜", "安排动效节奏"],
            x: 98,
            y: 234,
            w: 560,
            h: 260,
            animation: {
              effect: "reveal-down",
              startMs: 420,
              durationMs: 520,
              itemStaggerMs: 180
            }
          }
        ]
      },
      {
        id: "scene-03",
        label: "结尾",
        type: "closing",
        transition: {
          enterEffect: "iris-in",
          exitEffect: "fade",
          enterDurationMs: 340,
          exitDurationMs: 240
        },
        durationMs: 2600,
        narration: "最后用一句总结收尾，预览确认后再导出视频。",
        elements: [
          {
            id: "scene-03-title",
            type: "title",
            text: "先预览确认，再导出视频",
            x: 96,
            y: 206,
            w: 860,
            h: 136,
            style: {
              fontSize: 58
            },
            animation: {
              effect: "fade-up",
              startMs: 120,
              durationMs: 620
            }
          },
          {
            id: "scene-03-chip",
            type: "chip",
            text: "export mp4",
            x: 102,
            y: 378,
            w: 178,
            h: 42,
            animation: {
              effect: "glow-pop",
              startMs: 620,
              durationMs: 420
            }
          }
        ]
      }
    ]
  };
}

if (require.main === module) {
  const slugArg = process.argv[2];
  const title = process.argv[3];
  const themeFlagIndex = process.argv.indexOf("--theme");
  const templateFlagIndex = process.argv.indexOf("--template");
  const templateId = templateFlagIndex >= 0 ? process.argv[templateFlagIndex + 1] : DEFAULT_TEMPLATE;

  if (!slugArg || !title) {
    console.error('Usage: node scripts/init_project.js <slug> "<title>" [--template signal-stage] [--theme signal-ink]');
    process.exit(1);
  }

  const template = resolveTemplate(templateId);
  const theme = themeFlagIndex >= 0 ? process.argv[themeFlagIndex + 1] : template.theme;

  const slug = slugify(slugArg);
  const projectDir = path.join(__dirname, "..", "projects", slug);
  const moviePath = path.join(projectDir, "movie.json");

  if (pathExists(moviePath)) {
    console.error(`Project already exists: ${projectDir}`);
    process.exit(1);
  }

  ensureDir(path.join(projectDir, "assets"));
  ensureDir(path.join(projectDir, "output"));
  writeText(moviePath, JSON.stringify(createStarterMovie({ title, theme, templateId: template.id }), null, 2) + "\n");
  console.log(`Created ${projectDir}`);
}

function pathExists(targetPath) {
  try {
    return require("fs").existsSync(targetPath);
  } catch (error) {
    return false;
  }
}

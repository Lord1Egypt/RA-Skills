#!/usr/bin/env node

import fs from "node:fs/promises";
import fsSync from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillRoot = path.resolve(__dirname, "..");

const allowedKinds = [
  { kind: "flowchart", pattern: /^(flowchart|graph)\s+(TD|TB|BT|RL|LR)\b/i },
  { kind: "sequence", pattern: /^sequenceDiagram(?:-v2)?\b/i },
  { kind: "class", pattern: /^classDiagram(?:-v2)?\b/i },
];

main().catch((error) => {
  console.error(`[handdraw-flowchart] ${error.message || error}`);
  process.exit(1);
});

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.input) {
    printUsage();
    process.exit(args.help ? 0 : 1);
  }

  const inputPath = path.resolve(args.input);
  const rawSource = await fs.readFile(inputPath, "utf8");
  const source = normalizeMermaidSource(rawSource);
  const kind = detectKind(source);

  const validateOnly = Boolean(args["validate-only"]);
  const name = sanitizeName(args.name || path.basename(inputPath, path.extname(inputPath)));
  const outDir = path.resolve(args["out-dir"] || path.dirname(inputPath));
  const background = args.background || "#ffffff";
  const scale = Number(args.scale || 2);

  if (!Number.isFinite(scale) || scale <= 0 || scale > 4) {
    throw new Error("--scale must be a number between 0 and 4.");
  }

  const { esbuild, chromium } = await loadDependencies();
  const bundle = await buildBrowserBundle(esbuild);
  const browser = await launchBrowser(chromium);

  try {
    const page = await browser.newPage();
    await page.setContent("<!doctype html><html><body></body></html>");
    await page.addScriptTag({ content: bundle });

    let result;
    try {
      result = await page.evaluate(
        async ({ mermaidSource, renderBackground, renderScale, onlyValidate }) =>
          window.__handdrawFlowchart.render({
            mermaidSource,
            renderBackground,
            renderScale,
            onlyValidate,
          }),
        {
          mermaidSource: source,
          renderBackground: background,
          renderScale: scale,
          onlyValidate: validateOnly,
        },
      );
    } catch (error) {
      throw new Error(cleanBrowserError(error));
    }

    if (validateOnly) {
      console.log(`[handdraw-flowchart] valid ${kind} Mermaid: ${inputPath}`);
      return;
    }

    await fs.mkdir(outDir, { recursive: true });

    const mmdPath = path.join(outDir, `${name}.mmd`);
    const scenePath = path.join(outDir, `${name}.excalidraw`);
    const pngPath = path.join(outDir, `${name}.png`);

    await fs.writeFile(mmdPath, `${source}\n`, "utf8");
    await fs.writeFile(scenePath, `${JSON.stringify(result.scene, null, 2)}\n`, "utf8");
    await fs.writeFile(pngPath, Buffer.from(result.pngBase64, "base64"));

    const mode = result.metadata.fileCount > 0 ? "image-fallback" : "native-elements";
    console.log(`[handdraw-flowchart] diagram kind: ${kind}`);
    console.log(`[handdraw-flowchart] conversion mode: ${mode}`);
    console.log(`[handdraw-flowchart] elements: ${result.metadata.elementCount}, files: ${result.metadata.fileCount}`);
    console.log(`[handdraw-flowchart] wrote ${mmdPath}`);
    console.log(`[handdraw-flowchart] wrote ${scenePath}`);
    console.log(`[handdraw-flowchart] wrote ${pngPath}`);
  } finally {
    await browser.close();
  }
}

function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      throw new Error(`Unexpected argument: ${token}`);
    }
    const key = token.slice(2);
    if (key === "help" || key === "validate-only") {
      args[key] = true;
      continue;
    }
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      throw new Error(`Missing value for --${key}.`);
    }
    args[key] = value;
    index += 1;
  }
  return args;
}

function printUsage() {
  console.log(`Usage:
  node scripts/render-mermaid-handdraw.mjs --input diagram.mmd --out-dir ./out --name diagram
  node scripts/render-mermaid-handdraw.mjs --input diagram.mmd --validate-only

Options:
  --input           Mermaid .mmd file. Required.
  --out-dir         Output directory. Defaults to the input file directory.
  --name            Output file basename. Defaults to input basename.
  --background      PNG background color. Defaults to #ffffff.
  --scale           Export scale from 1 to 4. Defaults to 2.
  --validate-only   Strictly validate Mermaid without writing output files.
`);
}

function normalizeMermaidSource(source) {
  const trimmed = source.trim();
  const fenced = trimmed.match(/^```(?:mermaid|mmd)?\s*\n([\s\S]*?)\n```\s*$/i);
  const normalized = (fenced ? fenced[1] : trimmed).trim();

  if (!normalized) {
    throw new Error("Mermaid source is empty.");
  }
  if (normalized.startsWith("---")) {
    throw new Error("YAML frontmatter is not allowed for this strict workflow.");
  }
  if (/@\{\s*shape\s*:/i.test(normalized)) {
    throw new Error("Experimental Mermaid shape declarations are not allowed; use classic flowchart node syntax.");
  }
  return normalized;
}

function detectKind(source) {
  const firstLine = source
    .split(/\r?\n/)
    .map((line) => line.trim())
    .find((line) => line && !line.startsWith("%%"));

  if (!firstLine) {
    throw new Error("Mermaid source has no diagram declaration.");
  }

  const matched = allowedKinds.find((entry) => entry.pattern.test(firstLine));
  if (!matched) {
    throw new Error(
      `Unsupported Mermaid diagram declaration "${firstLine}". Allowed: flowchart, sequenceDiagram, classDiagram.`,
    );
  }
  return matched.kind;
}

function sanitizeName(value) {
  const sanitized = value.toLowerCase().replace(/[^a-z0-9._-]+/g, "-").replace(/^-+|-+$/g, "");
  if (!sanitized) {
    throw new Error("Output name is empty after sanitization.");
  }
  return sanitized;
}

function cleanBrowserError(error) {
  const message = error.message || String(error);
  return message
    .split(/\n\s+at /)[0]
    .replace(/^page\.evaluate:\s*/, "")
    .replace(/^Error:\s*/, "")
    .trim();
}

async function loadDependencies() {
  try {
    const esbuild = await import("esbuild");
    const { chromium } = await import("playwright");
    return { esbuild, chromium };
  } catch (error) {
    throw new Error(
      `Missing renderer dependencies. Run "npm install" in ${skillRoot}. Original error: ${error.message}`,
    );
  }
}

async function buildBrowserBundle(esbuild) {
  const browserSource = `
    import mermaid from "mermaid";
    import { convertToExcalidrawElements, exportToBlob } from "@excalidraw/excalidraw";
    import { parseMermaidToExcalidraw } from "@excalidraw/mermaid-to-excalidraw";

    async function validateMermaid(mermaidSource) {
      mermaid.initialize({
        startOnLoad: false,
        securityLevel: "strict",
        deterministicIds: true,
        deterministicIDSeed: "handdraw-flowchart"
      });
      try {
        await mermaid.parse(mermaidSource, { suppressErrors: false });
      } catch (error) {
        throw new Error("Mermaid validation failed: " + (error.str || error.message || String(error)));
      }
    }

    async function blobToBase64(blob) {
      const buffer = await blob.arrayBuffer();
      const bytes = new Uint8Array(buffer);
      let binary = "";
      const chunkSize = 0x8000;
      for (let offset = 0; offset < bytes.length; offset += chunkSize) {
        const chunk = bytes.subarray(offset, offset + chunkSize);
        binary += String.fromCharCode.apply(null, chunk);
      }
      return btoa(binary);
    }

    window.__handdrawFlowchart = {
      async render({ mermaidSource, renderBackground, renderScale, onlyValidate }) {
        await validateMermaid(mermaidSource);
        if (onlyValidate) {
          return { ok: true };
        }

        let parsed;
        try {
          parsed = await parseMermaidToExcalidraw(mermaidSource, { fontSize: 20 });
        } catch (error) {
          throw new Error("Mermaid to Excalidraw conversion failed: " + (error.message || String(error)));
        }
        const files = parsed.files || {};
        const elements = convertToExcalidrawElements(parsed.elements);
        const appState = {
          exportBackground: true,
          exportWithDarkMode: false,
          gridSize: null,
          viewBackgroundColor: renderBackground
        };

        const blob = await exportToBlob({
          elements,
          appState,
          files,
          mimeType: "image/png",
          quality: 1,
          getDimensions: (width, height) => ({
            width: width * renderScale,
            height: height * renderScale,
            scale: renderScale
          })
        });

        return {
          scene: {
            type: "excalidraw",
            version: 2,
            source: "handdraw-flowchart",
            elements,
            appState,
            files
          },
          pngBase64: await blobToBase64(blob),
          metadata: {
            elementCount: elements.length,
            fileCount: Object.keys(files).length
          }
        };
      }
    };
  `;

  try {
    const result = await esbuild.build({
      stdin: {
        contents: browserSource,
        resolveDir: skillRoot,
        sourcefile: "handdraw-flowchart-renderer.js",
      },
      bundle: true,
      write: false,
      format: "iife",
      globalName: "HanddrawFlowchartRenderer",
      platform: "browser",
      define: {
        "process.env.NODE_ENV": '"production"',
      },
      loader: {
        ".css": "empty",
      },
    });
    return result.outputFiles[0].text;
  } catch (error) {
    throw new Error(`Failed to bundle the browser renderer: ${error.message}`);
  }
}

async function launchBrowser(chromium) {
  const candidates = [
    process.env.CHROME_PATH,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ].filter(Boolean);

  const errors = [];

  try {
    return await chromium.launch({ headless: true });
  } catch (error) {
    errors.push(`bundled Playwright browser: ${error.message}`);
  }

  for (const executablePath of candidates) {
    if (!fsSync.existsSync(executablePath)) {
      continue;
    }
    try {
      return await chromium.launch({ headless: true, executablePath });
    } catch (error) {
      errors.push(`${executablePath}: ${error.message}`);
    }
  }

  throw new Error(
    `Unable to launch Chromium. Install Playwright browsers with "npx playwright install chromium" or set CHROME_PATH. Attempts: ${errors.join(" | ")}`,
  );
}

#!/usr/bin/env node
import { access, mkdir, readFile, writeFile } from "node:fs/promises";
import { constants as fsConstants } from "node:fs";
import { basename, dirname, extname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const skillDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const runtimePath = resolve(skillDir, "assets/html-slide-mender-runtime.js");
const START_MARKER = "<!-- html-slide-mender-skill:start -->";
const END_MARKER = "<!-- html-slide-mender-skill:end -->";

main().catch((error) => {
  console.error(JSON.stringify({
    ok: false,
    error: error?.message || String(error)
  }, null, 2));
  process.exit(1);
});

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.input) {
    printUsage();
    process.exit(args.help ? 0 : 1);
  }

  const inputPath = resolve(args.input);
  await access(inputPath, fsConstants.R_OK);

  const outputPath = resolve(args.out || defaultOutputPath(inputPath));
  await mkdir(dirname(outputPath), { recursive: true });

  const sourceHtml = await readFile(inputPath, "utf8");
  const runtime = await readFile(runtimePath, "utf8");
  const cleanedHtml = stripPreviousInjection(sourceHtml);
  const options = {
    lang: args.lang || "zh-CN",
    exportMode: args.mode || "basic",
    autoStart: args.autoStart,
    enableDraft: false
  };
  const editableHtml = injectBeforeBodyEnd(
    cleanedHtml,
    buildBodyInjection(runtime, options, cleanedHtml)
  );

  await writeFile(outputPath, editableHtml, "utf8");

  console.log(JSON.stringify({
    ok: true,
    input: inputPath,
    output: outputPath,
    lang: args.lang || "zh-CN",
    exportMode: args.mode || "basic",
    autoStart: args.autoStart,
    cspMetaPreserved: true,
    cspMetaModified: false,
    note: "Open the output HTML in a browser, edit visually, then use the editor toolbar to download a clean HTML copy."
  }, null, 2));
}

function parseArgs(argv) {
  const args = {
    input: "",
    out: "",
    lang: "zh-CN",
    mode: "basic",
    autoStart: true,
    help: false
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--help" || arg === "-h") {
      args.help = true;
    } else if (arg === "--out") {
      args.out = requireValue(argv, index, arg);
      index += 1;
    } else if (arg === "--lang") {
      args.lang = normalizeLanguage(requireValue(argv, index, arg));
      index += 1;
    } else if (arg === "--mode") {
      args.mode = normalizeMode(requireValue(argv, index, arg));
      index += 1;
    } else if (arg === "--no-autostart") {
      args.autoStart = false;
    } else if (arg.startsWith("--")) {
      throw new Error(`Unknown option: ${arg}`);
    } else if (!args.input) {
      args.input = arg;
    } else {
      throw new Error(`Unexpected extra argument: ${arg}`);
    }
  }

  return args;
}

function requireValue(argv, index, flag) {
  const value = argv[index + 1];
  if (!value || value.startsWith("--")) {
    throw new Error(`Missing value for ${flag}`);
  }
  return value;
}

function normalizeLanguage(value) {
  return value === "en" ? "en" : "zh-CN";
}

function normalizeMode(value) {
  if (!value || value === "basic") {
    return "basic";
  }
  throw new Error(`Unsupported export mode for the skill runtime: ${value}. Use basic.`);
}

function defaultOutputPath(inputPath) {
  const dir = dirname(inputPath);
  const ext = extname(inputPath) || ".html";
  const stem = basename(inputPath, ext);
  return resolve(dir, `${stem}.editable${ext}`);
}

function stripPreviousInjection(html) {
  const source = String(html || "");
  const ranges = findInjectionRemovalRanges(source);
  if (!ranges.length) {
    return source;
  }
  return applyRemovalRanges(source, ranges);
}

function buildBodyInjection(runtime, options, sourceHtml) {
  const optionsJson = jsonForInlineScript(options);
  const sourceJson = jsonForInlineScript(String(sourceHtml || ""));
  return [
    START_MARKER,
    `<script data-hsm-editor="skill-runtime">\n(() => {\n  const skillSourceHtml = ${sourceJson};\n  const skillOptions = ${optionsJson};\n${indentRuntime(escapeScript(runtime))}\n})();\n</script>`,
    END_MARKER
  ].join("\n");
}

function escapeScript(source) {
  return String(source || "").replace(/<\/script/gi, "<\\/script");
}

function jsonForInlineScript(value) {
  return JSON.stringify(value)
    .replace(/</g, "\\u003c")
    .replace(/\u2028/g, "\\u2028")
    .replace(/\u2029/g, "\\u2029");
}

function indentRuntime(source) {
  return String(source || "").split("\n").map((line) => `  ${line}`).join("\n");
}

function injectBeforeBodyEnd(html, injection) {
  const source = String(html || "");
  const bodyEnd = findClosingTagOutsideRawText(source, "body");
  if (bodyEnd) {
    return `${source.slice(0, bodyEnd.start)}${injection}\n${source.slice(bodyEnd.start)}`;
  }
  const htmlEnd = findClosingTagOutsideRawText(source, "html");
  if (htmlEnd) {
    return `${source.slice(0, htmlEnd.start)}${injection}\n${source.slice(htmlEnd.start)}`;
  }
  return `${source}\n${injection}\n`;
}

function findInjectionRemovalRanges(source) {
  const ranges = [];
  walkHtmlTokens(source, {
    comment(token) {
      if (/html-slide-mender-skill:(?:start|end)/i.test(token.text)) {
        ranges.push({ start: token.start, end: token.end });
      }
    },
    startTag(token) {
      if (token.tag === "script" && /\bdata-hsm-editor\b/i.test(token.text)) {
        const close = findRawTextClose(source, "script", token.end);
        ranges.push({ start: token.start, end: close?.end || token.end });
      }
    }
  });
  return ranges;
}

function applyRemovalRanges(source, ranges) {
  let result = source;
  let nextStart = source.length + 1;
  const ordered = ranges
    .filter((range) => range.start >= 0 && range.end >= range.start && range.end <= source.length)
    .sort((a, b) => b.start - a.start);
  for (const range of ordered) {
    if (range.end > nextStart) {
      continue;
    }
    result = result.slice(0, range.start) + result.slice(range.end);
    nextStart = range.start;
  }
  return result;
}

function findClosingTagOutsideRawText(source, tagName) {
  let found = null;
  walkHtmlTokens(source, {
    endTag(token) {
      if (token.tag === tagName.toLowerCase()) {
        found = token;
      }
    }
  });
  return found;
}

function walkHtmlTokens(source, visitor = {}) {
  const html = String(source || "");
  let index = 0;
  while (index < html.length) {
    const start = html.indexOf("<", index);
    if (start < 0) {
      break;
    }

    if (html.startsWith("<!--", start)) {
      const close = html.indexOf("-->", start + 4);
      const end = close < 0 ? html.length : close + 3;
      visitor.comment?.({
        start,
        end,
        text: html.slice(start, end)
      });
      index = end;
      continue;
    }

    const tagEnd = findTagEnd(html, start);
    if (tagEnd < 0) {
      break;
    }
    const tagText = html.slice(start, tagEnd);
    const endMatch = tagText.match(/^<\s*\/\s*([a-zA-Z][^\s/>]*)/);
    if (endMatch) {
      visitor.endTag?.({
        start,
        end: tagEnd,
        tag: endMatch[1].toLowerCase(),
        text: tagText
      });
      index = tagEnd;
      continue;
    }

    const startMatch = tagText.match(/^<\s*([a-zA-Z][^\s/>]*)/);
    if (!startMatch) {
      index = tagEnd;
      continue;
    }

    const tag = startMatch[1].toLowerCase();
    visitor.startTag?.({
      start,
      end: tagEnd,
      tag,
      text: tagText
    });

    if (!/\/\s*>$/.test(tagText) && isRawTextTag(tag)) {
      const close = findRawTextClose(html, tag, tagEnd);
      index = close?.end || tagEnd;
      continue;
    }

    index = tagEnd;
  }
}

function findTagEnd(source, start) {
  let quote = "";
  for (let index = start + 1; index < source.length; index += 1) {
    const char = source[index];
    if (quote) {
      if (char === quote) {
        quote = "";
      }
      continue;
    }
    if (char === "\"" || char === "'") {
      quote = char;
      continue;
    }
    if (char === ">") {
      return index + 1;
    }
  }
  return -1;
}

function findRawTextClose(source, tag, fromIndex) {
  const pattern = new RegExp(`</\\s*${tag}\\s*>`, "i");
  const match = pattern.exec(source.slice(fromIndex));
  if (!match) {
    return null;
  }
  const start = fromIndex + match.index;
  return {
    start,
    end: start + match[0].length
  };
}

function isRawTextTag(tag) {
  return /^(script|style|textarea|title)$/i.test(tag);
}

function printUsage() {
  console.log(`Usage:
  node scripts/inject-html-editor.mjs <input.html> [--out output.html] [--lang zh-CN|en] [--mode basic]

Options:
  --out <path>       Output editable HTML path. Defaults to <input>.editable.html in the same folder.
  --lang <value>     Editor language: zh-CN or en. Defaults to zh-CN.
  --mode <value>     Export mode. Only basic is supported by the skill runtime.
  --no-autostart     Inject the runtime but do not start editing automatically.
`);
}

/**
 * Image downloader for LinkMind
 * Downloads images to the Obsidian vault's attachments directory.
 *
 * Usage:
 *   npx tsx download-images.ts \
 *     --urls "url1,url2,url3" \
 *     --output-dir "/path/to/vault/LinkMind/attachments/2026-03-22-slug" \
 *     [--referer "https://weibo.com"]
 *
 * Output: JSON mapping { "original_url": "local_filename", ... }
 */

import { fileURLToPath } from "node:url";
import { writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join, extname } from "node:path";
import { withRetry, isRetryableError } from "./retry.js";

const CONCURRENCY = 5;
const DOWNLOAD_TIMEOUT = 30_000;

const DEFAULT_UA =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " +
  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36";

const CONTENT_TYPE_EXT: Record<string, string> = {
  "image/jpeg": ".jpg",
  "image/png": ".png",
  "image/gif": ".gif",
  "image/webp": ".webp",
  "image/svg+xml": ".svg",
  "image/bmp": ".bmp",
  "image/avif": ".avif",
};

function guessExtension(url: string, contentType?: string | null): string {
  if (contentType) {
    const base = contentType.split(";")[0].trim().toLowerCase();
    if (CONTENT_TYPE_EXT[base]) return CONTENT_TYPE_EXT[base];
  }
  const pathPart = url.split("?")[0];
  const ext = extname(pathPart).toLowerCase();
  if (ext && [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".avif"].includes(ext)) {
    return ext === ".jpeg" ? ".jpg" : ext;
  }
  return ".jpg";
}

async function downloadOne(
  url: string,
  outputDir: string,
  index: number,
  referer?: string,
): Promise<{ url: string; filename: string | null }> {
  try {
    const headers: Record<string, string> = { "User-Agent": DEFAULT_UA };
    if (referer) headers["Referer"] = referer;

    const buffer = await withRetry(
      async () => {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), DOWNLOAD_TIMEOUT);
        try {
          const resp = await fetch(url, {
            headers,
            signal: controller.signal,
          });
          if (!resp.ok) {
            const err = new Error(`HTTP ${resp.status}`);
            (err as any).httpStatus = resp.status;
            throw err;
          }
          const ct = resp.headers.get("content-type");
          const ext = guessExtension(url, ct);
          const arrayBuf = await resp.arrayBuffer();
          return { data: Buffer.from(arrayBuf), ext };
        } finally {
          clearTimeout(timer);
        }
      },
      { maxAttempts: 2, shouldRetry: isRetryableError },
    );

    const filename = `img-${String(index + 1).padStart(3, "0")}${buffer.ext}`;
    writeFileSync(join(outputDir, filename), buffer.data);
    return { url, filename };
  } catch {
    return { url, filename: null };
  }
}

interface DownloadResult {
  [originalUrl: string]: string | null;
}

async function downloadAll(
  urls: string[],
  outputDir: string,
  referer?: string,
): Promise<DownloadResult> {
  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }

  const result: DownloadResult = {};
  const queue = urls.map((url, i) => ({ url, index: i }));
  const active: Promise<void>[] = [];

  for (const item of queue) {
    const p = downloadOne(item.url, outputDir, item.index, referer).then(
      (r) => {
        result[r.url] = r.filename;
      },
    );
    active.push(p);

    if (active.length >= CONCURRENCY) {
      await Promise.race(active);
      // Remove settled promises
      for (let i = active.length - 1; i >= 0; i--) {
        const settled = await Promise.race([
          active[i].then(() => true),
          Promise.resolve(false),
        ]);
        if (settled) active.splice(i, 1);
      }
    }
  }

  await Promise.all(active);
  return result;
}

function parseArgs(argv: string[]): {
  urls: string[];
  outputDir: string;
  referer?: string;
} {
  let urls: string[] = [];
  let outputDir = "";
  let referer: string | undefined;

  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === "--urls" && i + 1 < argv.length) {
      urls = argv[++i].split(",").filter(Boolean);
    } else if (argv[i] === "--output-dir" && i + 1 < argv.length) {
      outputDir = argv[++i];
    } else if (argv[i] === "--referer" && i + 1 < argv.length) {
      referer = argv[++i];
    }
  }

  if (!urls.length || !outputDir) {
    console.error(
      "Usage: download-images.ts --urls <url1,url2,...> --output-dir <path> [--referer <url>]",
    );
    process.exit(1);
  }

  return { urls, outputDir, referer };
}

async function main(): Promise<void> {
  const { urls, outputDir, referer } = parseArgs(process.argv);
  const result = await downloadAll(urls, outputDir, referer);
  console.log(JSON.stringify(result, null, 2));
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}

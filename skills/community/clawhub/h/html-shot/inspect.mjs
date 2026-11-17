#!/usr/bin/env node
/** Report actual image properties, including whether any transparent pixels exist. */
import { readFileSync } from "node:fs";
const files = process.argv.slice(2);
if (!files.length || (files.length === 1 && files[0] === "--help")) {
  console.log("Usage: node inspect.mjs <image.png|jpg|webp> [...]");
  process.exitCode = files.length ? 0 : 1;
} else {
  try {
    const { default: sharp } = await import("sharp");
    for (const file of files) {
      try {
        const buffer = readFileSync(file),
          image = sharp(buffer);
        const meta = await image.metadata(),
          stats = await image.stats();
        console.log(
          JSON.stringify({
            file,
            format: meta.format,
            width: meta.width,
            height: meta.height,
            hasAlpha: meta.hasAlpha,
            opaque: stats.isOpaque,
            bytes: buffer.length,
          }),
        );
      } catch (error) {
        console.error(
          `html-shot/inspect: ${file}: ${error.message.split("\n")[0]}`,
        );
        process.exitCode = 1;
      }
    }
  } catch (error) {
    console.error(
      `html-shot/inspect: sharp unavailable (${error.code || error.message}); run npm ci`,
    );
    process.exitCode = 1;
  }
}

import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { normalizeImageGenerationInputs } from "../src/image-input.js";

test("normalizeImageGenerationInputs maps one source image to imageDataUrl", async () => {
  const dir = await mkdtemp(join(tmpdir(), "nano-gpt-cli-"));
  const imagePath = join(dir, "source.png");
  await writeFile(
    imagePath,
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00]),
  );

  const requestFields = await normalizeImageGenerationInputs([imagePath]);
  assert.match(requestFields.imageDataUrl ?? "", /^data:image\/png;base64,/);
  assert.equal(requestFields.imageDataUrls, undefined);
});

test("normalizeImageGenerationInputs maps multiple source images to imageDataUrls", async () => {
  const dir = await mkdtemp(join(tmpdir(), "nano-gpt-cli-"));
  const firstImagePath = join(dir, "one.png");
  const secondImagePath = join(dir, "two.png");

  await writeFile(
    firstImagePath,
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00]),
  );
  await writeFile(
    secondImagePath,
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x01]),
  );

  const requestFields = await normalizeImageGenerationInputs([firstImagePath, secondImagePath]);
  assert.equal(requestFields.imageDataUrl, undefined);
  assert.equal(requestFields.imageDataUrls?.length, 2);
  assert.match(requestFields.imageDataUrls?.[0] ?? "", /^data:image\/png;base64,/);
  assert.match(requestFields.imageDataUrls?.[1] ?? "", /^data:image\/png;base64,/);
});

test("normalizeImageGenerationInputs converts remote image URLs to data URLs", async () => {
  let requestedUrl = "";
  const requestFields = await normalizeImageGenerationInputs(
    ["https://example.com/source.webp"],
    async (input) => {
      requestedUrl = String(input);
      return new Response(
        Buffer.from([
          0x52, 0x49, 0x46, 0x46, 0x01, 0x00, 0x00, 0x00, 0x57, 0x45, 0x42, 0x50,
        ]),
        {
          status: 200,
          headers: {
            "Content-Type": "image/webp",
          },
        },
      );
    },
  );

  assert.equal(requestedUrl, "https://example.com/source.webp");
  assert.match(requestFields.imageDataUrl ?? "", /^data:image\/webp;base64,/);
});

test("normalizeImageGenerationInputs rejects unsupported image-to-image formats", async () => {
  const dir = await mkdtemp(join(tmpdir(), "nano-gpt-cli-"));
  const imagePath = join(dir, "source.bmp");
  await writeFile(imagePath, Buffer.from([0x42, 0x4d, 0x00, 0x00]));

  await assert.rejects(
    () => normalizeImageGenerationInputs([imagePath]),
    /jpeg, png, webp, or gif/,
  );
});

import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

import {
  normalizeVideoGenerationImageInput,
  normalizeVideoGenerationVideoInput,
} from "../src/image-input.js";

test("normalizeVideoGenerationImageInput keeps remote image URLs as imageUrl", async () => {
  const media = await normalizeVideoGenerationImageInput("https://example.com/input.png");
  assert.deepEqual(media, {
    imageUrl: "https://example.com/input.png",
  });
});

test("normalizeVideoGenerationImageInput converts local images to imageDataUrl", async () => {
  const dir = await mkdtemp(join(tmpdir(), "nano-gpt-cli-"));
  const imagePath = join(dir, "input.png");
  await writeFile(
    imagePath,
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00]),
  );

  const media = await normalizeVideoGenerationImageInput(imagePath);
  assert.match(media.imageDataUrl ?? "", /^data:image\/png;base64,/);
  assert.equal(media.imageUrl, undefined);
});

test("normalizeVideoGenerationVideoInput converts local videos to videoDataUrl", async () => {
  const dir = await mkdtemp(join(tmpdir(), "nano-gpt-cli-"));
  const videoPath = join(dir, "input.mp4");
  await writeFile(
    videoPath,
    Buffer.from([
      0x00, 0x00, 0x00, 0x14,
      0x66, 0x74, 0x79, 0x70,
      0x69, 0x73, 0x6f, 0x6d,
      0x00, 0x00, 0x00, 0x00,
    ]),
  );

  const media = await normalizeVideoGenerationVideoInput(videoPath);
  assert.match(media.videoDataUrl ?? "", /^data:video\/mp4;base64,/);
  assert.equal(media.videoUrl, undefined);
});

test("normalizeVideoGenerationVideoInput keeps remote video URLs as videoUrl", async () => {
  const media = await normalizeVideoGenerationVideoInput("https://example.com/input.mp4");
  assert.deepEqual(media, {
    videoUrl: "https://example.com/input.mp4",
  });
});

test("normalizeVideoGenerationVideoInput rejects unsupported local video files", async () => {
  const dir = await mkdtemp(join(tmpdir(), "nano-gpt-cli-"));
  const videoPath = join(dir, "input.avi");
  await writeFile(videoPath, Buffer.from([0x00, 0x01, 0x02, 0x03]));

  await assert.rejects(
    () => normalizeVideoGenerationVideoInput(videoPath),
    /Unsupported local video file/,
  );
});

import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { buildMessageContent, extractTextContent } from "../src/messages.js";

test("buildMessageContent returns plain text when no images are attached", async () => {
  const content = await buildMessageContent("hello", []);
  assert.equal(content, "hello");
});

test("buildMessageContent converts local image paths to file URLs", async () => {
  const dir = await mkdtemp(join(tmpdir(), "nano-gpt-cli-"));
  const imagePath = join(dir, "image.png");
  await writeFile(imagePath, "fake-image");

  const content = await buildMessageContent("describe", [imagePath]);
  assert.ok(Array.isArray(content));
  assert.equal(content[0]?.type, "text");
  assert.equal(content[1]?.type, "image_url");
  assert.match(content[1]?.image_url.url ?? "", /^data:image\/png;base64,/);
});

test("buildMessageContent sniffs extensionless local image files", async () => {
  const dir = await mkdtemp(join(tmpdir(), "nano-gpt-cli-"));
  const imagePath = join(dir, "image.png");
  const linkPath = join(dir, "image-without-extension");
  await writeFile(
    imagePath,
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00]),
  );
  await symlink(imagePath, linkPath);

  const content = await buildMessageContent("describe", [linkPath]);
  assert.ok(Array.isArray(content));
  const imagePart = content[1];
  assert.equal(imagePart?.type, "image_url");
  assert.match(imagePart.image_url.url, /^data:image\/png;base64,/);
});

test("buildMessageContent rejects unsupported local files", async () => {
  const dir = await mkdtemp(join(tmpdir(), "nano-gpt-cli-"));
  const filePath = join(dir, "blob");
  await writeFile(filePath, "not-an-image");

  await assert.rejects(
    () => buildMessageContent("describe", [filePath]),
    /Unsupported local image file/,
  );
});

test("extractTextContent joins text parts", () => {
  const text = extractTextContent([
    { type: "text", text: "hello " },
    { type: "image_url", image_url: { url: "https://example.com/cat.png" } },
    { type: "text", text: "world" },
  ]);

  assert.equal(text, "hello world");
});

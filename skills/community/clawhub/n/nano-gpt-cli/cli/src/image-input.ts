import { access, readFile } from "node:fs/promises";
import { extname, resolve } from "node:path";

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_VIDEO_DATA_URL_BYTES = 4 * 1024 * 1024;
const IMAGE_TO_IMAGE_MIME_TYPES = new Set([
  "image/gif",
  "image/jpeg",
  "image/png",
  "image/webp",
]);
const VIDEO_MIME_TYPES = new Set([
  "video/mp4",
  "video/quicktime",
  "video/webm",
  "video/x-m4v",
]);

export async function normalizeChatImageInput(input: string): Promise<string> {
  if (isRemoteImageInput(input) || input.startsWith("data:")) {
    return input;
  }

  return readLocalImageAsDataUrl(input);
}

export async function normalizeImageGenerationInputs(
  inputs: string[],
  fetchImpl: typeof fetch = fetch,
): Promise<Pick<ImageGenerationImageInputs, "imageDataUrl" | "imageDataUrls">> {
  if (inputs.length === 0) {
    return {};
  }

  const imageDataUrls = await Promise.all(
    inputs.map((input) => normalizeImageGenerationInput(input, fetchImpl)),
  );

  if (imageDataUrls.length === 1) {
    return {
      imageDataUrl: imageDataUrls[0],
    };
  }

  return {
    imageDataUrls,
  };
}

export async function normalizeVideoGenerationImageInput(
  input: string | undefined,
): Promise<{
  imageUrl?: string;
  imageDataUrl?: string;
}> {
  if (!input) {
    return {};
  }

  if (input.startsWith("data:")) {
    assertImageToImageMimeType(extractDataUrlMimeType(input), input);
    return { imageDataUrl: input };
  }

  if (isRemoteImageInput(input)) {
    return { imageUrl: input };
  }

  const media = await readLocalMediaAsDataUrl(input, { kind: "image" });
  assertImageToImageMimeType(media.mimeType, media.source);
  assertMaxVideoDataUrlBytes(media.bytes.length, media.source);
  return {
    imageDataUrl: media.dataUrl,
  };
}

export async function normalizeVideoGenerationVideoInput(
  input: string | undefined,
): Promise<{
  videoUrl?: string;
  videoDataUrl?: string;
}> {
  if (!input) {
    return {};
  }

  if (input.startsWith("data:")) {
    assertSupportedVideoMimeType(extractDataUrlMimeType(input), input);
    return { videoDataUrl: input };
  }

  if (isRemoteImageInput(input)) {
    return { videoUrl: input };
  }

  const media = await readLocalMediaAsDataUrl(input, { kind: "video" });
  assertSupportedVideoMimeType(media.mimeType, media.source);
  assertMaxVideoDataUrlBytes(media.bytes.length, media.source);
  return {
    videoDataUrl: media.dataUrl,
  };
}

type ImageGenerationImageInputs = {
  imageDataUrl?: string;
  imageDataUrls?: string[];
};

async function normalizeImageGenerationInput(
  input: string,
  fetchImpl: typeof fetch,
): Promise<string> {
  if (input.startsWith("data:")) {
    assertImageToImageMimeType(extractDataUrlMimeType(input), input);
    return input;
  }

  if (isRemoteImageInput(input)) {
    return readRemoteImageAsDataUrl(input, fetchImpl);
  }

  return readLocalImageAsDataUrl(input, { imageToImage: true });
}

async function readRemoteImageAsDataUrl(
  input: string,
  fetchImpl: typeof fetch,
): Promise<string> {
  const response = await fetchImpl(input);
  if (!response.ok) {
    throw new Error(
      `Failed to download source image: ${input} (${response.status} ${response.statusText})`,
    );
  }

  const bytes = Buffer.from(await response.arrayBuffer());
  const mimeType = detectImageMimeType(input, bytes, response.headers.get("content-type"));
  assertImageToImageMimeType(mimeType, input);
  return toDataUrl(mimeType, bytes);
}

async function readLocalImageAsDataUrl(
  input: string,
  options?: { imageToImage?: boolean },
): Promise<string> {
  const media = await readLocalMediaAsDataUrl(input, { kind: "image" });
  if (options?.imageToImage) {
    assertImageToImageMimeType(media.mimeType, media.source);
  }

  return media.dataUrl;
}

async function readLocalMediaAsDataUrl(
  input: string,
  options: { kind: "image" | "video" },
): Promise<{
  bytes: Buffer;
  dataUrl: string;
  mimeType: string;
  source: string;
}> {
  const absolutePath = resolve(input);
  await access(absolutePath);
  const bytes = await readFile(absolutePath);
  const mimeType =
    options.kind === "image"
      ? detectImageMimeType(absolutePath, bytes)
      : detectVideoMimeType(absolutePath, bytes);

  return {
    bytes,
    dataUrl: toDataUrl(mimeType, bytes),
    mimeType,
    source: absolutePath,
  };
}

function toDataUrl(mimeType: string, bytes: Buffer): string {
  return `data:${mimeType};base64,${bytes.toString("base64")}`;
}

function isRemoteImageInput(input: string): boolean {
  return /^https?:\/\//i.test(input);
}

function extractDataUrlMimeType(input: string): string {
  const match = /^data:([^;,]+)[;,]/i.exec(input);
  if (!match?.[1]) {
    throw new Error(`Invalid image data URL: ${input.slice(0, 32)}...`);
  }

  const mimeType = normalizeMimeType(match[1]);
  if (!mimeType) {
    throw new Error(`Invalid image data URL: ${input.slice(0, 32)}...`);
  }

  return mimeType;
}

function detectImageMimeType(pathOrUrl: string, bytes: Buffer, contentType?: string | null): string {
  const normalizedContentType = normalizeMimeType(contentType);
  if (normalizedContentType?.startsWith("image/")) {
    return normalizedContentType;
  }

  if (bytes.length >= 8 && bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
    return "image/png";
  }

  if (bytes.length >= 3 && bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff) {
    return "image/jpeg";
  }

  if (bytes.length >= 6) {
    const header = bytes.subarray(0, 6).toString("ascii");
    if (header === "GIF87a" || header === "GIF89a") {
      return "image/gif";
    }
  }

  if (
    bytes.length >= 12 &&
    bytes.subarray(0, 4).toString("ascii") === "RIFF" &&
    bytes.subarray(8, 12).toString("ascii") === "WEBP"
  ) {
    return "image/webp";
  }

  if (bytes.length >= 2 && bytes.subarray(0, 2).toString("ascii") === "BM") {
    return "image/bmp";
  }

  const textPrefix = bytes.subarray(0, 512).toString("utf8").trimStart();
  if (textPrefix.startsWith("<svg") || textPrefix.startsWith("<?xml")) {
    return "image/svg+xml";
  }

  switch (extname(pathOrUrl).toLowerCase()) {
    case ".jpg":
    case ".jpeg":
      return "image/jpeg";
    case ".png":
      return "image/png";
    case ".webp":
      return "image/webp";
    case ".gif":
      return "image/gif";
    case ".bmp":
      return "image/bmp";
    case ".svg":
      return "image/svg+xml";
    default:
      throw new Error(
        `Unsupported local image file: ${pathOrUrl}. Use png, jpg, webp, gif, bmp, svg, or pass a remote URL/data URL.`,
      );
  }
}

function detectVideoMimeType(pathOrUrl: string, bytes: Buffer): string {
  if (
    bytes.length >= 12 &&
    bytes.subarray(4, 8).toString("ascii") === "ftyp"
  ) {
    const brand = bytes.subarray(8, 12).toString("ascii").toLowerCase();
    if (brand === "qt  ") {
      return "video/quicktime";
    }

    return "video/mp4";
  }

  if (
    bytes.length >= 4 &&
    bytes[0] === 0x1a &&
    bytes[1] === 0x45 &&
    bytes[2] === 0xdf &&
    bytes[3] === 0xa3
  ) {
    return "video/webm";
  }

  switch (extname(pathOrUrl).toLowerCase()) {
    case ".mp4":
      return "video/mp4";
    case ".mov":
      return "video/quicktime";
    case ".webm":
      return "video/webm";
    case ".m4v":
      return "video/x-m4v";
    default:
      throw new Error(
        `Unsupported local video file: ${pathOrUrl}. Use mp4, mov, webm, m4v, or pass a remote URL/data URL.`,
      );
  }
}

function normalizeMimeType(contentType?: string | null): string | undefined {
  if (!contentType) {
    return undefined;
  }

  const mimeType = contentType.split(";", 1)[0]?.trim().toLowerCase();
  if (!mimeType) {
    return undefined;
  }

  if (mimeType === "image/jpg") {
    return "image/jpeg";
  }

  return mimeType;
}

function assertImageToImageMimeType(mimeType: string, source: string): void {
  if (IMAGE_TO_IMAGE_MIME_TYPES.has(mimeType)) {
    return;
  }

  throw new Error(
    `Unsupported image-to-image source: ${source}. NanoGPT image inputs must be jpeg, png, webp, or gif data URLs.`,
  );
}

function assertSupportedVideoMimeType(mimeType: string, source: string): void {
  if (VIDEO_MIME_TYPES.has(mimeType)) {
    return;
  }

  throw new Error(
    `Unsupported video source: ${source}. NanoGPT video inputs must be mp4, mov, webm, or m4v data URLs.`,
  );
}

function assertMaxVideoDataUrlBytes(size: number, source: string): void {
  if (size <= MAX_VIDEO_DATA_URL_BYTES) {
    return;
  }

  throw new Error(
    `Local media source is too large for a video data URL: ${source}. NanoGPT limits inline video inputs to 4 MB, so use a remote URL instead.`,
  );
}

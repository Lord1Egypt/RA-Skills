import { H as resolveApiKeyForProvider } from "../../pi-embedded-BaSvmUpW.js";

const DEFAULT_OUTPUT_MIME = "image/png";
const DEFAULT_SIZE = "1024x1024";
const SUPPORTED_SIZES = [
  "1024x1024",
  "1024x1536",
  "1536x1024"
];
const SUPPORTED_ASPECT_RATIOS = [
  "1:1",
  "2:3",
  "3:2"
];
const ASPECT_RATIO_TO_SIZE = {
  "1:1": "1024x1024",
  "2:3": "1024x1536",
  "3:2": "1536x1024"
};

function resolveHnbcBaseUrl(cfg) {
  const direct = cfg?.models?.providers?.hnbc?.baseUrl?.trim() || "https://api.1415.xin/v1";
  return direct.replace(/\/+$/u, "");
}

function decodeBase64Payload(value) {
  if (!value || typeof value !== "string") return null;
  const trimmed = value.trim();
  if (!trimmed) return null;
  const match = /^data:([^;]+);base64,(.+)$/u.exec(trimmed);
  if (match) {
    return {
      buffer: Buffer.from(match[2], "base64"),
      mimeType: match[1] || DEFAULT_OUTPUT_MIME
    };
  }
  try {
    return {
      buffer: Buffer.from(trimmed, "base64"),
      mimeType: DEFAULT_OUTPUT_MIME
    };
  } catch {
    return null;
  }
}

function normalizeImageEntries(payload) {
  const data = payload?.data;
  if (!Array.isArray(data)) return [];
  const images = [];
  let idx = 0;
  for (const entry of data) {
    const decoded = decodeBase64Payload(entry?.b64_json || entry?.base64 || entry?.image_base64);
    if (!decoded) continue;
    idx += 1;
    images.push({
      buffer: decoded.buffer,
      mimeType: decoded.mimeType,
      fileName: `image-${idx}.png`,
      ...(entry?.revised_prompt ? { revisedPrompt: entry.revised_prompt } : {})
    });
  }
  return images;
}

function resolveRequestedSize(req) {
  const size = req.size?.trim();
  if (size) return size;
  const aspectRatio = req.aspectRatio?.trim();
  if (aspectRatio && ASPECT_RATIO_TO_SIZE[aspectRatio]) return ASPECT_RATIO_TO_SIZE[aspectRatio];
  return DEFAULT_SIZE;
}

function buildHnbcImageGenerationProvider() {
  return {
    id: "hnbc",
    label: "HNBC",
    defaultModel: "gpt-image-2",
    models: ["gpt-image-2"],
    capabilities: {
      generate: {
        maxCount: 4,
        supportsSize: true,
        supportsAspectRatio: true,
        supportsResolution: false
      },
      edit: {
        enabled: false,
        maxCount: 0,
        maxInputImages: 0,
        supportsSize: false,
        supportsAspectRatio: false,
        supportsResolution: false
      },
      geometry: {
        sizes: [...SUPPORTED_SIZES],
        aspectRatios: [...SUPPORTED_ASPECT_RATIOS]
      }
    },
    async generateImage(req) {
      if ((req.inputImages?.length ?? 0) > 0) {
        throw new Error("HNBC image provider v1 暂不支持参考图编辑");
      }
      const auth = await resolveApiKeyForProvider({
        provider: "hnbc",
        cfg: req.cfg,
        agentDir: req.agentDir,
        store: req.authStore
      });
      const apiKey = auth.apiKey || req.cfg?.models?.providers?.hnbc?.apiKey?.trim();
      if (!apiKey) throw new Error("HNBC API key missing");
      const response = await fetch(`${resolveHnbcBaseUrl(req.cfg)}/images/generations`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${apiKey}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: req.model || "gpt-image-2",
          prompt: req.prompt,
          n: req.count ?? 1,
          size: resolveRequestedSize(req)
        })
      });
      if (!response.ok) {
        const text = await response.text().catch(() => "");
        throw new Error(`HNBC image generation failed (${response.status}): ${text || response.statusText}`);
      }
      const payload = await response.json();
      const images = normalizeImageEntries(payload);
      if (images.length === 0) {
        throw new Error("HNBC image generation response missing image data");
      }
      return {
        images,
        model: req.model || "gpt-image-2",
        metadata: payload?.created ? { created: payload.created } : void 0
      };
    }
  };
}

export { buildHnbcImageGenerationProvider };

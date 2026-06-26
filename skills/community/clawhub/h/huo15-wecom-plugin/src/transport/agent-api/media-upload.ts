import type { ResolvedAgentAccount } from "../../types/index.js";
import { uploadMedia as uploadLegacyMedia } from "./core.js";

export async function uploadAgentApiMedia(params: {
  agent: ResolvedAgentAccount;
  type: "image" | "voice" | "video" | "file";
  buffer: Buffer;
  filename: string;
}): Promise<string> {
  return uploadLegacyMedia(params);
}

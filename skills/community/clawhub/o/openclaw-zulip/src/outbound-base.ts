import { sanitizeForPlainText } from "openclaw/plugin-sdk/outbound-runtime";

export const zulipOutboundBaseAdapter = {
  deliveryMode: "direct" as const,
  chunkerMode: "markdown" as const,
  textChunkLimit: 4000,
  sanitizeText: ({ text }: { text: string }) => sanitizeForPlainText(text),
};

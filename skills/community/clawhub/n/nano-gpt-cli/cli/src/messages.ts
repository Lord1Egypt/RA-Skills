import type { ChatMessage, MessageContent, MessageContentPart } from "./types.js";
import { normalizeChatImageInput } from "./image-input.js";

export async function buildUserMessage(
  prompt: string,
  imageInputs: string[],
): Promise<ChatMessage> {
  return {
    role: "user",
    content: await buildMessageContent(prompt, imageInputs),
  };
}

export async function buildMessageContent(
  prompt: string,
  imageInputs: string[],
): Promise<MessageContent> {
  if (imageInputs.length === 0) {
    return prompt;
  }

  const parts: MessageContentPart[] = [];
  if (prompt.trim()) {
    parts.push({
      type: "text",
      text: prompt,
    });
  }

  for (const input of imageInputs) {
    parts.push({
      type: "image_url",
      image_url: {
        url: await normalizeChatImageInput(input),
      },
    });
  }

  return parts;
}

export function extractTextContent(content?: MessageContent): string {
  if (!content) {
    return "";
  }

  if (typeof content === "string") {
    return content;
  }

  return content
    .filter((part) => part.type === "text")
    .map((part) => part.text)
    .join("");
}

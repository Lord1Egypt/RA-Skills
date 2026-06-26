import { describe, it, expect } from "vitest";
import { convertMessages, convertTools, type ContentPart } from "../src/gemini-api-runner.js";
import type { ChatMessage } from "../src/cli-runner.js";
import type { ToolDefinition } from "../src/tool-protocol.js";

describe("gemini-api-runner", () => {
  describe("convertMessages", () => {
    it("converts system messages to systemInstruction", () => {
      const messages: ChatMessage[] = [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "Hello" },
      ];
      const result = convertMessages(messages);
      expect(result.systemInstruction).toEqual({
        parts: [{ text: "You are a helpful assistant." }],
      });
      expect(result.contents).toHaveLength(1);
      expect(result.contents[0].role).toBe("user");
    });

    it("maps assistant role to model", () => {
      const messages: ChatMessage[] = [
        { role: "user", content: "Hi" },
        { role: "assistant", content: "Hello!" },
      ];
      const result = convertMessages(messages);
      expect(result.contents[0].role).toBe("user");
      expect(result.contents[1].role).toBe("model");
    });

    it("converts tool results to functionResponse", () => {
      const messages: ChatMessage[] = [
        { role: "tool", content: '{"result": "42"}', name: "calculator" } as ChatMessage & { name: string },
      ];
      const result = convertMessages(messages);
      expect(result.contents[0].role).toBe("user");
      const part = result.contents[0].parts[0] as { functionResponse: { name: string; response: Record<string, unknown> } };
      expect(part.functionResponse.name).toBe("calculator");
      expect(part.functionResponse.response).toEqual({ result: "42" });
    });

    it("converts assistant tool_calls to functionCall parts", () => {
      const messages = [
        {
          role: "assistant" as const,
          content: null,
          tool_calls: [
            { id: "call_1", type: "function" as const, function: { name: "search", arguments: '{"q":"test"}' } },
          ],
        },
      ] as unknown as ChatMessage[];
      const result = convertMessages(messages);
      expect(result.contents[0].role).toBe("model");
      const part = result.contents[0].parts[0] as { functionCall: { name: string; args: Record<string, unknown> } };
      expect(part.functionCall.name).toBe("search");
      expect(part.functionCall.args).toEqual({ q: "test" });
    });

    it("converts image_url content parts to inlineData", () => {
      const messages: ChatMessage[] = [
        {
          role: "user",
          content: [
            { type: "text", text: "What is this?" },
            { type: "image_url", image_url: { url: "data:image/png;base64,iVBOR" } },
          ] as unknown as string,
        },
      ];
      const result = convertMessages(messages);
      expect(result.contents[0].parts).toHaveLength(2);
      const imgPart = result.contents[0].parts[1] as { inlineData: { mimeType: string; data: string } };
      expect(imgPart.inlineData.mimeType).toBe("image/png");
      expect(imgPart.inlineData.data).toBe("iVBOR");
    });

    it("handles multiple system messages", () => {
      const messages: ChatMessage[] = [
        { role: "system", content: "Rule 1" },
        { role: "system", content: "Rule 2" },
        { role: "user", content: "Go" },
      ];
      const result = convertMessages(messages);
      expect(result.systemInstruction?.parts).toHaveLength(2);
      expect(result.contents).toHaveLength(1);
    });

    it("skips empty content messages", () => {
      const messages: ChatMessage[] = [
        { role: "user", content: "" },
        { role: "user", content: "Hello" },
      ];
      const result = convertMessages(messages);
      expect(result.contents).toHaveLength(1);
    });

    it("handles plain string tool result", () => {
      const messages: ChatMessage[] = [
        { role: "tool", content: "plain text result", name: "myTool" } as ChatMessage & { name: string },
      ];
      const result = convertMessages(messages);
      const part = result.contents[0].parts[0] as { functionResponse: { name: string; response: Record<string, unknown> } };
      expect(part.functionResponse.response).toEqual({ result: "plain text result" });
    });
  });

  describe("convertTools", () => {
    it("wraps tool definitions in functionDeclarations", () => {
      const tools: ToolDefinition[] = [
        {
          type: "function",
          function: {
            name: "search",
            description: "Search the web",
            parameters: { type: "object", properties: { q: { type: "string" } } },
          },
        },
      ];
      const result = convertTools(tools);
      expect(result).toHaveLength(1);
      expect(result[0].functionDeclarations).toHaveLength(1);
      expect(result[0].functionDeclarations[0].name).toBe("search");
      expect(result[0].functionDeclarations[0].description).toBe("Search the web");
    });

    it("handles multiple tools", () => {
      const tools: ToolDefinition[] = [
        { type: "function", function: { name: "a", description: "A", parameters: {} } },
        { type: "function", function: { name: "b", description: "B", parameters: {} } },
      ];
      const result = convertTools(tools);
      expect(result[0].functionDeclarations).toHaveLength(2);
    });
  });
});

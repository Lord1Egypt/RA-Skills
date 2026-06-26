/**
 * LLaVA Vision Skill (OpenClaw Compatible)
 * - calls local llama-server (OpenAI-like API)
 */

const LLAMA_SERVER_URL = "http://127.0.0.1:8081/v1/chat/completions";

/**
 * imageBase64: string (required)
 * prompt: string (optional)
 */
export const skills = {
  async vision_analyze({ imagePathOrUrl, prompt = "Describe this image in detail" }) {
    try {
      const fs = await import("node:fs");
      let imageBase64;
      if (imagePathOrUrl.startsWith("http://") || imagePathOrUrl.startsWith("https://")) {
        const res = await fetch(imagePathOrUrl);
        if (!res.ok) throw new Error(`Failed to fetch image: ${res.statusText}`);
        const buffer = await res.arrayBuffer();
        imageBase64 = Buffer.from(buffer).toString("base64");
      } else {
        const buffer = await fs.promises.readFile(imagePathOrUrl);
        imageBase64 = buffer.toString("base64");
      }
      const payload = {
        model: "llava",
        messages: [
          {
            role: "user",
            content: [
              {
                type: "text",
                text: prompt
              },
              {
                type: "image_url",
                image_url: {
                  url: `data:image/jpeg;base64,${imageBase64}`
                }
              }
            ]
          }
        ],
        temperature: 0.2
      };

      const res = await fetch(LLAMA_SERVER_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const err = await res.text();
        return {
          ok: false,
          error: "LLAMA_SERVER_ERROR",
          detail: err
        };
      }

      const data = await res.json();

      const text =
        data?.choices?.[0]?.message?.content ??
        "No response from model";

      return {
        ok: true,
        text
      };
    } catch (e) {
      return {
        ok: false,
        error: "SKILL_RUNTIME_ERROR",
        detail: String(e)
      };
    }
  }
};
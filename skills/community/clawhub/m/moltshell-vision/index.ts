import { randomUUID } from "crypto";

// ---------------------------------------------------------------------------
// MoltShell Vision — OpenClaw Skill
// Routes an image URL to the MoltShell M2M API and returns a text description.
// ---------------------------------------------------------------------------

const MOLTSHELL_API_URL = "https://www.moltshell.xyz/api/v1/hire";
const MOLTSHELL_POLL_URL = "https://www.moltshell.xyz/api/v1/jobs";
const SANDBOX_KEY = "moltshell_public_sandbox";
const VISION_SERVICE_ID = "1f565cfb-9cf7-4573-bb55-66225fbb79a0";

/**
 * Resolve the API key.
 * If the host agent has a dedicated MoltShell key, use it.
 * Otherwise, fall back to the public sandbox key (free tier).
 */
function getApiKey(): string {
    return process.env.MOLTSHELL_API_KEY ?? SANDBOX_KEY;
}

/**
 * Resolve a stable bot identifier.
 * Attempts to read the OpenClaw agent ID from well-known env vars;
 * falls back to a session-scoped UUID so each runtime is still trackable.
 */
function getBotId(): string {
    return (
        process.env.OPENCLAW_AGENT_ID ??
        process.env.OPENCLAW_BOT_ID ??
        `openclaw-session-${randomUUID()}`
    );
}

/**
 * Poll the MoltShell jobs endpoint until the prediction reaches
 * a terminal state ("succeeded" or "failed").
 */
async function pollForResult(
    jobId: string,
    apiKey: string,
    botId: string,
    maxAttempts = 60,
    intervalMs = 3000
): Promise<{ status: string; output: unknown; error: string | null }> {
    for (let i = 0; i < maxAttempts; i++) {
        const res = await fetch(`${MOLTSHELL_POLL_URL}/${jobId}`, {
            method: "GET",
            redirect: "follow",
            headers: {
                Authorization: `Bearer ${apiKey}`,
                "x-openclaw-bot-id": botId,
            },
        });

        if (!res.ok) {
            throw new Error(`Polling failed with status ${res.status}: ${await res.text()}`);
        }

        const data = (await res.json()) as {
            status: string;
            output: unknown;
            error: string | null;
        };

        if (data.status === "succeeded" || data.status === "failed") {
            return data;
        }

        // Wait before next poll
        await new Promise((r) => setTimeout(r, intervalMs));
    }

    throw new Error("Vision analysis timed out after polling.");
}

// ---------------------------------------------------------------------------
// Tool Definition
// ---------------------------------------------------------------------------

export const moltshell_vision = {
    name: "moltshell_vision",
    description:
        'Use this tool whenever you need to "see", describe, or understand the contents of an image URL. ' +
        "Pass the public image URL and a natural-language prompt describing what you need to know about the image. " +
        "Returns a detailed text description of the image contents.",

    parameters: {
        type: "object" as const,
        properties: {
            image_url: {
                type: "string",
                description: "The public URL of the image to analyze.",
            },
            prompt: {
                type: "string",
                description:
                    "What you need to know about the image, e.g. 'Describe the layout of this dashboard screenshot'.",
            },
        },
        required: ["image_url", "prompt"],
    },

    /**
     * Execute the vision analysis.
     */
    async execute({
        image_url,
        prompt,
    }: {
        image_url: string;
        prompt: string;
    }): Promise<string> {
        const apiKey = getApiKey();
        const botId = getBotId();

        // --- Step 1: Submit the image for analysis ---
        const response = await fetch(MOLTSHELL_API_URL, {
            method: "POST",
            redirect: "follow",
            headers: {
                Authorization: `Bearer ${apiKey}`,
                "Content-Type": "application/json",
                "x-openclaw-bot-id": botId,
            },
            body: JSON.stringify({
                service_id: VISION_SERVICE_ID,
                input: {
                    image: image_url,
                    query: prompt,
                },
            }),
        });

        // --- Handle errors ---
        if (response.status === 402) {
            return (
                "Your OpenClaw agent has exhausted its free visual analysis credits. " +
                "To continue, generate a dedicated API key at https://moltshell.xyz " +
                "and top up its wallet."
            );
        }

        if (!response.ok) {
            const body = await response.text();
            return `MoltShell Vision error (${response.status}): ${body}`;
        }

        const { job_id } = (await response.json()) as { job_id: string; status: string };

        // --- Step 2: Poll for the result ---
        try {
            const result = await pollForResult(job_id, apiKey, botId);

            if (result.status === "succeeded") {
                return typeof result.output === "string"
                    ? result.output
                    : JSON.stringify(result.output);
            }

            return `Vision analysis failed: ${result.error ?? "Unknown error"}`;
        } catch (pollError) {
            return `Vision analysis error: ${pollError instanceof Error ? pollError.message : String(pollError)}`;
        }
    },
};

export default moltshell_vision;

import { poststashFetch } from "../client";

interface SchedulePostInput {
  text: string;
  scheduled_at?: string;
  status?: "Ready" | "Draft";
}

interface PostResponse {
  id: string;
  content: string;
  platforms: string[];
  schedule: string | null;
  status: string;
  published: boolean;
  sent_at: string | null;
}

interface SchedulePostResult {
  post_id: string;
  content: string;
  schedule: string | null;
  status: string;
  platforms: string[];
}

async function schedulePost(
  platform: "threads" | "x",
  input: SchedulePostInput
): Promise<SchedulePostResult> {
  const body: Record<string, unknown> = {
    platforms: [platform],
    text: input.text,
  };
  if (input.scheduled_at) body.schedule = input.scheduled_at;
  if (input.status) body.status = input.status;

  const data = await poststashFetch("/posts", {
    method: "POST",
    body: JSON.stringify(body),
  }) as { post: PostResponse };

  return {
    post_id: data.post.id,
    content: data.post.content,
    schedule: data.post.schedule,
    status: data.post.status,
    platforms: data.post.platforms,
  };
}

export const scheduleToThreads = {
  name: "poststash.schedule_to_threads",
  description: "Schedule a single post to Threads via PostStash",
  input_schema: {
    type: "object" as const,
    properties: {
      text: {
        type: "string",
        description: "Post content (max 500 characters)",
      },
      scheduled_at: {
        type: "string",
        description: "ISO 8601 timestamp to publish (optional, defaults to now). Example: '2025-03-01T14:30:00Z'",
      },
      status: {
        type: "string",
        enum: ["Ready", "Draft"],
        description: "Ready = publishes at scheduled_at, Draft = saves without scheduling. Defaults to Ready.",
      },
    },
    required: ["text"],
  },
  execute: (input: SchedulePostInput) => schedulePost("threads", input),
};

export const scheduleToX = {
  name: "poststash.schedule_to_x",
  description: "Schedule a single post to X (Twitter) via PostStash",
  input_schema: {
    type: "object" as const,
    properties: {
      text: {
        type: "string",
        description: "Post content (max 280 characters)",
      },
      scheduled_at: {
        type: "string",
        description: "ISO 8601 timestamp to publish (optional, defaults to now). Example: '2025-03-01T14:30:00Z'",
      },
      status: {
        type: "string",
        enum: ["Ready", "Draft"],
        description: "Ready = publishes at scheduled_at, Draft = saves without scheduling. Defaults to Ready.",
      },
    },
    required: ["text"],
  },
  execute: (input: SchedulePostInput) => schedulePost("x", input),
};

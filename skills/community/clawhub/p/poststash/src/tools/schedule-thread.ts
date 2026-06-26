import { poststashFetch } from "../client";

interface ThreadPost {
  text: string;
}

interface ScheduleThreadInput {
  platform: "threads" | "x";
  posts: ThreadPost[];
  scheduled_at?: string;
  status?: "Ready" | "Draft";
}

interface ScheduledThreadPost {
  id: string;
  content: string;
  thread_position: number;
  schedule: string | null;
  status: string;
}

interface ScheduleThreadResult {
  thread_id: string;
  posts: ScheduledThreadPost[];
}

export const scheduleThread = {
  name: "poststash.schedule_thread",
  description: "Schedule a thread (2–20 posts) to Threads or X via PostStash",
  input_schema: {
    type: "object" as const,
    properties: {
      platform: {
        type: "string",
        enum: ["threads", "x"],
        description: "Target platform",
      },
      posts: {
        type: "array",
        description: "Array of posts in the thread (2–20 items)",
        items: {
          type: "object",
          properties: {
            text: {
              type: "string",
              description: "Text content of this post in the thread",
            },
          },
          required: ["text"],
        },
        minItems: 2,
        maxItems: 20,
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
    required: ["platform", "posts"],
  },
  execute: async (input: ScheduleThreadInput): Promise<ScheduleThreadResult> => {
    const body: Record<string, unknown> = {
      platforms: [input.platform],
      posts: input.posts,
    };
    if (input.scheduled_at) body.schedule = input.scheduled_at;
    if (input.status) body.status = input.status;

    const data = await poststashFetch("/posts", {
      method: "POST",
      body: JSON.stringify(body),
    }) as { thread_id: string; posts: ScheduledThreadPost[] };

    return {
      thread_id: data.thread_id,
      posts: data.posts.map((p) => ({
        id: p.id,
        content: p.content,
        thread_position: p.thread_position,
        schedule: p.schedule,
        status: p.status,
      })),
    };
  },
};

import { poststashFetch } from "../client";

interface ListPostsInput {
  status?: "Draft" | "Ready" | "Published" | "Failed";
  published?: boolean;
  limit?: number;
  offset?: number;
}

interface PostSummary {
  id: string;
  content: string;
  platforms: string[];
  schedule: string | null;
  published: boolean;
  status: string;
  created_by_source: string;
  created_by_api_key_name: string | null;
  created_at: string;
  updated_at: string;
}

interface ListPostsResult {
  posts: PostSummary[];
  total: number;
  limit: number;
  offset: number;
}

export const listPosts = {
  name: "poststash.list_posts",
  description: "List posts for your account (scoped to the context of your API key)",
  input_schema: {
    type: "object" as const,
    properties: {
      status: {
        type: "string",
        enum: ["Draft", "Ready", "Published", "Failed"],
        description: "Filter by post status (optional)",
      },
      published: {
        type: "boolean",
        description: "Filter by published state: true (already posted) or false (pending)",
      },
      limit: {
        type: "number",
        description: "Results per page (default: 20, max: 100)",
      },
      offset: {
        type: "number",
        description: "Pagination offset (default: 0)",
      },
    },
  },
  execute: async (input: ListPostsInput = {}): Promise<ListPostsResult> => {
    const params = new URLSearchParams();
    if (input.status) params.set("status", input.status);
    if (input.published !== undefined) params.set("published", String(input.published));
    params.set("limit", String(input.limit ?? 20));
    params.set("offset", String(input.offset ?? 0));

    const query = params.toString();
    const data = await poststashFetch(`/posts?${query}`) as {
      posts: PostSummary[];
      pagination: { total: number; limit: number; offset: number };
    };

    return {
      posts: data.posts,
      total: data.pagination.total,
      limit: data.pagination.limit,
      offset: data.pagination.offset,
    };
  },
};

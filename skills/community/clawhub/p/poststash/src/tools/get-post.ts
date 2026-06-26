import { poststashFetch } from "../client";

interface GetPostInput {
  post_id: string;
}

interface PostMetrics {
  views: number;
  likes: number;
  replies: number;
  reposts: number;
  quotes: number;
}

interface PostAnalytics {
  platform: string;
  metrics: PostMetrics;
  last_fetched_at: string;
}

interface PostObject {
  id: string;
  content: string;
  platforms: string[];
  schedule: string | null;
  published: boolean;
  status: string;
  sent_at: string | null;
  context_id: string | null;
  created_by_source: string;
  created_by_api_key_name: string | null;
  created_at: string;
  updated_at: string;
}

interface GetPostResult {
  post: PostObject;
  analytics: PostAnalytics[];
}

export const getPost = {
  name: "poststash.get_post",
  description: "Fetch a scheduled or published post along with its analytics",
  input_schema: {
    type: "object" as const,
    properties: {
      post_id: {
        type: "string",
        description: "Post UUID from a schedule response",
      },
    },
    required: ["post_id"],
  },
  execute: async (input: GetPostInput): Promise<GetPostResult> => {
    const data = await poststashFetch(`/posts/${input.post_id}`) as {
      post: PostObject;
      analytics: PostAnalytics[];
    };

    return {
      post: data.post,
      analytics: data.analytics,
    };
  },
};

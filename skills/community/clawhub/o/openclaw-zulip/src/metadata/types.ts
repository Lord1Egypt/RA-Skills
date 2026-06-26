export type TopicStatus = "open" | "wip" | "blocked" | "done" | "archived";
export type TopicPriority = "p0" | "p1" | "p2" | "p3";

export interface TopicMetadata {
  id: number;
  stream_id: number;
  topic_name: string;
  status: TopicStatus;
  priority: TopicPriority | null;
  assignee: string | null;
  labels: string[];
  due_date: string | null;
  context: string | null;
  created_at: string;
  updated_at: string;
}

export interface TopicMetadataUpdate {
  stream_id?: number;
  topic_name?: string;
  status?: TopicStatus;
  priority?: TopicPriority | null;
  assignee?: string | null;
  labels?: string[];
  due_date?: string | null;
  context?: string | null;
  updated_at?: string;
}

export interface TopicRenameEntry {
  id: number;
  stream_id: number;
  old_name: string;
  new_name: string;
  renamed_at: string;
}

export interface MetadataFilter {
  status?: TopicStatus;
  assignee?: string;
  label?: string;
}

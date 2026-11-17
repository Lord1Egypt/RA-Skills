export interface ImportClient {
  skill_version: string;
  host_agent: string;
  host_agent_version: string;
  os: string;
  collected_at: string;
}

export interface ImportRedaction {
  enabled: boolean;
  rules_version: string;
  redacted_count: number;
  email_redacted?: boolean;
}

export interface MemoryItem {
  relative_path: string;
  type: 'markdown_index' | 'markdown_memory' | 'scheduled_task' | string;
  size_bytes: number;
  mtime: string;
  content?: string;
  frontmatter?: Record<string, string>;
  cron?: string;
  prompt?: string;
  durable?: boolean;
  recurring?: boolean;
  created_at?: string;
}

export interface CollectorResult {
  name: string;
  source_root: string;
  items: MemoryItem[];
}

export interface ImportPayload {
  schema_version: '1.0';
  client: ImportClient;
  redaction: ImportRedaction;
  collectors: CollectorResult[];
}

import { ConnectorConfig, NormalizedInboundMessage, nowIso, uid } from '../types';

const safeString = (value: unknown, fallback = '') => (typeof value === 'string' && value.trim() ? value.trim() : fallback);

export interface ConnectorAdapter {
  source_type: string;
  normalize(payload: Record<string, unknown>): NormalizedInboundMessage;
  defaultConfig(identityKey?: string): ConnectorConfig;
}

export const buildNormalizedInbound = (params: {
  source_type: string;
  source_thread_key: string;
  content: string;
  source_message_id?: string | null;
  source_author_id?: string | null;
  source_author_name?: string | null;
  target_session_id?: string | null;
  message_type?: string;
  attachments?: Array<Record<string, unknown>>;
  timestamp?: string;
  metadata?: Record<string, unknown>;
  request_id?: string;
  external_trigger_id?: string;
}) => ({
  request_id: params.request_id || uid('req'),
  external_trigger_id: params.external_trigger_id || uid('evt'),
  source_type: params.source_type,
  source_thread_key: params.source_thread_key,
  source_message_id: params.source_message_id || null,
  source_author_id: params.source_author_id || null,
  source_author_name: params.source_author_name || null,
  target_session_id: params.target_session_id || null,
  message_type: params.message_type || 'user_message',
  content: params.content,
  attachments: params.attachments || [],
  timestamp: params.timestamp || nowIso(),
  metadata: params.metadata || {},
});

export const connectorConfig = (connector: string, identityKey: string, mode: ConnectorConfig['mode'], endpointHint?: string) => ({
  connector,
  mode,
  identity_key: identityKey,
  endpoint_hint: endpointHint,
});

export { safeString };

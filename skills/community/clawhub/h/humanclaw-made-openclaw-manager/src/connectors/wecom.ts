import { ConnectorAdapter } from './base';
import { buildNormalizedInbound, connectorConfig, safeString } from './base';

export const wecomConnector: ConnectorAdapter = {
  source_type: 'wecom',
  normalize(payload) {
    const message = (payload.message as Record<string, unknown>) || payload;
    const threadKey =
      safeString(payload.source_thread_key) ||
      safeString(message.conversation_id) ||
      safeString(message.external_userid) ||
      'wecom-unknown';

    return buildNormalizedInbound({
      source_type: 'wecom',
      source_thread_key: `wecom:${threadKey}`,
      source_message_id: safeString(message.msgid || payload.message_id) || null,
      source_author_id: safeString(message.sender || message.from_userid || payload.source_author_id) || null,
      source_author_name: safeString(message.sender_name || message.from_name || payload.source_author_name) || null,
      content:
        safeString(message.content) ||
        safeString(message.text) ||
        safeString(payload.content) ||
        '[wecom message]',
      attachments: Array.isArray(message.attachments) ? (message.attachments as Array<Record<string, unknown>>) : [],
      timestamp: safeString(message.create_time || payload.timestamp) || undefined,
      metadata: {
        conversation_id: safeString(message.conversation_id),
        msg_type: safeString(message.msgtype),
        transport: 'wecom',
      },
      request_id: safeString(payload.request_id) || undefined,
      external_trigger_id: safeString(message.msgid || payload.external_trigger_id) || undefined,
    });
  },
  defaultConfig(identityKey = 'wecom-default') {
    return connectorConfig('wecom', identityKey, 'webhook', '/connectors/wecom/ingest');
  },
};

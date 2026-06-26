import { ConnectorAdapter } from './base';
import { buildNormalizedInbound, connectorConfig, safeString } from './base';

export const emailConnector: ConnectorAdapter = {
  source_type: 'email',
  normalize(payload) {
    const message = (payload.message as Record<string, unknown>) || payload;
    const threadKey =
      safeString(payload.source_thread_key) ||
      safeString(message.thread_id) ||
      safeString(message.in_reply_to) ||
      safeString(message.subject) ||
      'email-unknown';

    return buildNormalizedInbound({
      source_type: 'email',
      source_thread_key: `email:${threadKey}`,
      source_message_id: safeString(message.message_id || payload.message_id) || null,
      source_author_id: safeString(message.from_address || payload.source_author_id) || null,
      source_author_name: safeString(message.from_name || message.from_address || payload.source_author_name) || null,
      content:
        safeString(message.text_body) ||
        safeString(message.html_body) ||
        safeString(payload.content) ||
        '[email message]',
      attachments: Array.isArray(message.attachments) ? (message.attachments as Array<Record<string, unknown>>) : [],
      timestamp: safeString(message.received_at || payload.timestamp) || undefined,
      metadata: {
        subject: safeString(message.subject),
        thread_id: safeString(message.thread_id),
        transport: 'email',
      },
      request_id: safeString(payload.request_id) || undefined,
      external_trigger_id: safeString(message.message_id || payload.external_trigger_id) || undefined,
    });
  },
  defaultConfig(identityKey = 'email-default') {
    return connectorConfig('email', identityKey, 'polling', '/connectors/email/poll');
  },
};

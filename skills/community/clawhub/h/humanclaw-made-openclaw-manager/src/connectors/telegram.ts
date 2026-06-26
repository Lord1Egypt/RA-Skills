import { ConnectorAdapter } from './base';
import { buildNormalizedInbound, connectorConfig, safeString } from './base';

export const telegramConnector: ConnectorAdapter = {
  source_type: 'telegram',
  normalize(payload) {
    const message = (payload.message as Record<string, unknown>) || payload;
    const chat = (message.chat as Record<string, unknown>) || {};
    const from = (message.from as Record<string, unknown>) || {};
    const chatId = String(chat.id || payload.source_thread_key || payload.chat_id || 'telegram-unknown');
    const threadKey = safeString(payload.source_thread_key, `telegram:${chatId}`);
    const content =
      safeString(message.text) ||
      safeString(message.caption) ||
      safeString(payload.content) ||
      safeString(payload.body, '[telegram message]');

    return buildNormalizedInbound({
      source_type: 'telegram',
      source_thread_key: threadKey,
      source_message_id: safeString(message.message_id || payload.message_id) || null,
      source_author_id: safeString(from.id) || null,
      source_author_name: safeString(from.username || from.first_name || from.last_name) || null,
      content,
      attachments: Array.isArray(payload.attachments) ? (payload.attachments as Array<Record<string, unknown>>) : [],
      timestamp: safeString(message.date ? new Date(Number(message.date) * 1000).toISOString() : payload.timestamp, ''),
      metadata: {
        chat_id: chatId,
        chat_title: safeString(chat.title),
        transport: 'telegram',
      },
      request_id: safeString(payload.request_id) || undefined,
      external_trigger_id: safeString(payload.update_id || payload.external_trigger_id) || undefined,
    });
  },
  defaultConfig(identityKey = 'telegram-default') {
    return connectorConfig('telegram', identityKey, 'webhook', '/connectors/telegram/ingest');
  },
};

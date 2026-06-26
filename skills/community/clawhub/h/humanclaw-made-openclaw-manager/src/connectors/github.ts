import { ConnectorAdapter } from './base';
import { buildNormalizedInbound, connectorConfig, safeString } from './base';

export const githubConnector: ConnectorAdapter = {
  source_type: 'github',
  normalize(payload) {
    const repository = (payload.repository as Record<string, unknown>) || {};
    const issue = (payload.issue as Record<string, unknown>) || (payload.pull_request as Record<string, unknown>) || {};
    const comment = (payload.comment as Record<string, unknown>) || {};
    const sender = (payload.sender as Record<string, unknown>) || {};
    const repoFullName = safeString(repository.full_name, safeString(payload.repository_full_name, 'github-unknown'));
    const number = safeString(issue.number || payload.issue_number, '0');
    const threadKey = safeString(payload.source_thread_key, `github:${repoFullName}#${number}`);
    const body =
      safeString(comment.body) ||
      safeString(issue.body) ||
      safeString(payload.content) ||
      safeString(payload.action, '[github event]');

    return buildNormalizedInbound({
      source_type: 'github',
      source_thread_key: threadKey,
      source_message_id: safeString(comment.id || issue.id || payload.message_id) || null,
      source_author_id: safeString(sender.login || payload.source_author_id) || null,
      source_author_name: safeString(sender.login || payload.source_author_name) || null,
      content: body,
      attachments: Array.isArray(payload.attachments) ? (payload.attachments as Array<Record<string, unknown>>) : [],
      timestamp: safeString(comment.updated_at || issue.updated_at || payload.timestamp) || undefined,
      metadata: {
        repository: repoFullName,
        action: safeString(payload.action),
        issue_number: number,
        transport: 'github',
      },
      request_id: safeString(payload.request_id) || undefined,
      external_trigger_id: safeString(payload.delivery_id || payload.external_trigger_id) || undefined,
    });
  },
  defaultConfig(identityKey = 'github-default') {
    return connectorConfig('github', identityKey, 'webhook', '/connectors/github/ingest');
  },
};

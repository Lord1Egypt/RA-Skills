import path from 'node:path';
import { BindingRecord, ConnectorConfig, nowIso, uid } from '../types';
import { FsStore } from '../storage/fs-store';

export class BindingService {
  constructor(private readonly store: FsStore) {}

  private bindingsFile() {
    return path.join(this.store.connectorsDir, 'bindings.json');
  }

  async list(): Promise<BindingRecord[]> {
    return this.store.readJson<BindingRecord[]>(this.bindingsFile(), []);
  }

  async listConnectorConfigs(): Promise<ConnectorConfig[]> {
    return this.store.readJson<ConnectorConfig[]>(this.store.connectorConfigsFile, []);
  }

  async resolve(channel: string, externalThreadKey: string) {
    const bindings = await this.list();
    return (
      bindings.find(
        (binding) => binding.channel === channel && binding.external_thread_key === externalThreadKey
      ) || null
    );
  }

  async add(input: { channel: string; external_thread_key: string; session_id: string }) {
    const channel = String(input.channel || '').trim();
    const externalThreadKey = String(input.external_thread_key || '').trim();
    const sessionId = String(input.session_id || '').trim();
    if (!channel || !externalThreadKey || !sessionId) {
      throw new Error('channel, external_thread_key, and session_id are required.');
    }

    const bindings = await this.list();
    const existing = bindings.find(
      (binding) => binding.channel === channel && binding.external_thread_key === externalThreadKey
    );
    const next: BindingRecord = existing || {
      binding_id: uid('bind'),
      channel,
      external_thread_key: externalThreadKey,
      session_id: sessionId,
      created_at: nowIso(),
    };
    next.session_id = sessionId;

    const filtered = bindings.filter((binding) => binding.binding_id !== next.binding_id);
    await this.store.writeJson(this.bindingsFile(), [...filtered, next]);
    return next;
  }

  async upsertConnectorConfig(config: ConnectorConfig) {
    const configs = await this.listConnectorConfigs();
    const filtered = configs.filter((item) => !(item.connector === config.connector && item.identity_key === config.identity_key));
    const next = [...filtered, config];
    await this.store.writeJson(this.store.connectorConfigsFile, next);
    return config;
  }
}

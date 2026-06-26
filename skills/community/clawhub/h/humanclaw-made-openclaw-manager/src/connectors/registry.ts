import { ConnectorAdapter } from './base';
import { emailConnector } from './email';
import { githubConnector } from './github';
import { telegramConnector } from './telegram';
import { wecomConnector } from './wecom';

const CONNECTORS: Record<string, ConnectorAdapter> = {
  telegram: telegramConnector,
  wecom: wecomConnector,
  email: emailConnector,
  github: githubConnector,
};

export const getConnectorAdapter = (name: string) => CONNECTORS[name] || null;

export const listConnectorAdapters = () => Object.values(CONNECTORS);

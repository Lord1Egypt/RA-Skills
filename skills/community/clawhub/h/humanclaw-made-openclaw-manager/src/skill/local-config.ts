import { FsStore } from '../storage/fs-store';
import { ManagerSettings, nowIso } from '../types';

export const DEFAULT_SIDECAR_HOST = '127.0.0.1';
export const DEFAULT_SIDECAR_PORT = 4318;

const LOOPBACK_HOSTS = new Set(['127.0.0.1', 'localhost', '::1']);

const normalizeHost = (host: string) => host.replace(/^\[(.*)\]$/, '$1').trim().toLowerCase();

export const isLoopbackHost = (host: string) => LOOPBACK_HOSTS.has(normalizeHost(host));

export const resolvePort = () => Number(process.env.PORT || DEFAULT_SIDECAR_PORT);

export const resolveBindHost = () => {
  const configured = (process.env.OPENCLAW_MANAGER_BIND_HOST || DEFAULT_SIDECAR_HOST).trim();
  const normalized = normalizeHost(configured);

  if (isLoopbackHost(normalized)) {
    return normalized === 'localhost' ? DEFAULT_SIDECAR_HOST : normalized;
  }

  if (normalized === '0.0.0.0' || normalized === '::') {
    return normalized;
  }

  throw new Error(
    'OPENCLAW_MANAGER_BIND_HOST must be loopback by default. Use 0.0.0.0 or :: only when you explicitly intend to expose the sidecar.'
  );
};

export const defaultSidecarBaseUrl = () => `http://${DEFAULT_SIDECAR_HOST}:${resolvePort()}`;

export const isRemoteSidecarAllowed = () => process.env.OPENCLAW_MANAGER_ALLOW_REMOTE_SIDECAR === '1';

export const resolveSidecarBaseUrl = () => {
  const configured = process.env.OPENCLAW_MANAGER_SIDECAR_URL || defaultSidecarBaseUrl();
  const url = new URL(configured);

  if (!isRemoteSidecarAllowed() && !isLoopbackHost(url.hostname)) {
    throw new Error(
      'OPENCLAW_MANAGER_SIDECAR_URL must point to a loopback address. Set OPENCLAW_MANAGER_ALLOW_REMOTE_SIDECAR=1 only if you explicitly trust a remote sidecar.'
    );
  }

  return url.toString().replace(/\/$/, '');
};

export const isServerProcess = () => process.env.OPENCLAW_MANAGER_SERVER_PROCESS === '1';

export const isAutostartDisabled = () => process.env.OPENCLAW_MANAGER_NO_AUTOSTART === '1';

export const defaultManagerSettings = (): ManagerSettings => ({
  sidecar_autostart_consent: false,
  consent_recorded_at: null,
  consent_source: 'default',
});

export const readManagerSettings = async (store: FsStore) =>
  store.readJson<ManagerSettings>(store.settingsFile, defaultManagerSettings());

export const writeManagerSettings = async (store: FsStore, settings: ManagerSettings) => {
  await store.writeJson(store.settingsFile, settings);
  return settings;
};

export const setSidecarAutostartConsent = async (
  store: FsStore,
  consent: boolean,
  source: ManagerSettings['consent_source']
) => {
  const next = {
    sidecar_autostart_consent: consent,
    consent_recorded_at: consent ? nowIso() : null,
    consent_source: source,
  } satisfies ManagerSettings;

  return writeManagerSettings(store, next);
};

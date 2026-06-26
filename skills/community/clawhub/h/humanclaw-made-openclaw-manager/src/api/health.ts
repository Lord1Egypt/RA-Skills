import { Request, Response } from 'express';
import { FsStore } from '../storage/fs-store';
import { readManagerSettings, resolveBindHost, resolvePort } from '../skill/local-config';

export const healthHandler =
  (store: FsStore) =>
  async (_req: Request, res: Response) => {
    await store.ensureLayout();
    const settings = await readManagerSettings(store);
    res.json({
      status: 'ok',
      product: 'openclaw-manager',
      state_root: store.rootDir,
      mode: 'filesystem-first',
      bind_host: resolveBindHost(),
      port: resolvePort(),
      autostart_consent: settings.sidecar_autostart_consent,
    });
  };

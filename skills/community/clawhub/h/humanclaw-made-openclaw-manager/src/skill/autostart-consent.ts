import { FsStore } from '../storage/fs-store';
import { readManagerSettings, setSidecarAutostartConsent } from './local-config';

const parseAction = (args: string[]) => {
  if (args.includes('--allow')) {
    return 'allow';
  }
  if (args.includes('--deny')) {
    return 'deny';
  }
  throw new Error('Pass either --allow or --deny.');
};

export const updateAutostartConsent = async (
  action: 'allow' | 'deny',
  source: 'install_script' | 'manual_command' | 'bootstrap_flag'
) => {
  const store = new FsStore();
  await store.ensureLayout();
  const settings = await setSidecarAutostartConsent(store, action === 'allow', source);
  return {
    state_root: store.rootDir,
    settings,
  };
};

if (require.main === module) {
  (async () => {
    const action = parseAction(process.argv.slice(2));
    const source = process.argv.includes('--source=install_script') ? 'install_script' : 'manual_command';
    const result = await updateAutostartConsent(action, source);
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  })().catch((error) => {
    console.error(error);
    process.exit(1);
  });
}

export const readAutostartConsent = async () => {
  const store = new FsStore();
  await store.ensureLayout();
  return readManagerSettings(store);
};

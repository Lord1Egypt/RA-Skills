const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');

const stateRoot = path.join(os.tmpdir(), `openclaw-manager-security-${Date.now()}`);
process.env.OPENCLAW_MANAGER_STATE_ROOT = stateRoot;
process.env.PORT = '45218';
process.env.OPENCLAW_MANAGER_BIND_HOST = '127.0.0.1';
delete process.env.OPENCLAW_MANAGER_NO_AUTOSTART;
delete process.env.OPENCLAW_MANAGER_SERVER_PROCESS;
delete process.env.OPENCLAW_MANAGER_ALLOW_REMOTE_SIDECAR;
delete process.env.OPENCLAW_MANAGER_SIDECAR_URL;

const { FsStore } = require('../dist/storage/fs-store.js');
const { ensureSidecarRunning } = require('../dist/skill/bootstrap.js');
const {
  readManagerSettings,
  resolveBindHost,
  resolveSidecarBaseUrl,
  setSidecarAutostartConsent,
} = require('../dist/skill/local-config.js');
const { resolveServerCommand } = require('../dist/skill/sidecar-launcher.js');

const assert = (condition, message) => {
  if (!condition) {
    throw new Error(message);
  }
};

(async () => {
  await fs.rm(stateRoot, { recursive: true, force: true });

  const store = new FsStore(stateRoot);
  await store.ensureLayout();

  const settings = await readManagerSettings(store);
  assert(settings.sidecar_autostart_consent === false, 'Autostart consent should default to false.');
  assert(resolveBindHost() === '127.0.0.1', 'Bind host should default to loopback.');
  assert(resolveSidecarBaseUrl() === 'http://127.0.0.1:45218', 'Default sidecar URL should stay loopback-only.');

  process.env.OPENCLAW_MANAGER_SIDECAR_URL = 'http://example.com:4318';
  let rejectedRemote = false;
  try {
    resolveSidecarBaseUrl();
  } catch {
    rejectedRemote = true;
  }
  assert(rejectedRemote, 'Non-loopback sidecar URLs must be rejected by default.');
  delete process.env.OPENCLAW_MANAGER_SIDECAR_URL;

  const bootstrapResult = await ensureSidecarRunning();
  assert(bootstrapResult.status === 'consent_required', 'Bootstrap should require consent before autostart.');
  assert(bootstrapResult.launched === false, 'Bootstrap must not launch before consent.');
  assert(bootstrapResult.consent_required === true, 'Bootstrap should mark consent_required.');
  assert(
    bootstrapResult.next_steps.some((step) => step.includes('npm run consent:autostart')),
    'Bootstrap should explain how to authorize autostart.'
  );

  const updated = await setSidecarAutostartConsent(store, true, 'manual_command');
  assert(updated.sidecar_autostart_consent === true, 'Consent writer should persist allowed autostart.');

  const [command, args] = await resolveServerCommand();
  assert(command === process.execPath, 'Launcher must invoke the local Node.js executable.');
  assert(
    args.some((arg) => /(?:dist[\\/]+api[\\/]+server\.js|src[\\/]+api[\\/]+server\.ts)$/.test(arg)),
    'Launcher must only target the local sidecar server entrypoint.'
  );

  const lockfile = await fs.readFile(path.resolve(process.cwd(), 'package-lock.json'), 'utf8');
  assert(!lockfile.includes('registry.npmmirror.com'), 'Lockfile must not reference registry.npmmirror.com.');

  process.stdout.write(
    `${JSON.stringify(
      {
        status: 'ok',
        state_root: stateRoot,
        bind_host: resolveBindHost(),
        bootstrap_status: bootstrapResult.status,
      },
      null,
      2
    )}\n`
  );
})().catch((error) => {
  console.error(error);
  process.exit(1);
});

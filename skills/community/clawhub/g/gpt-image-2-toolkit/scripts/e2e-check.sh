#!/usr/bin/env bash
set -euo pipefail

WORKDIR="${1:-/root/.openclaw/workspace}"
export WORKDIR

echo '=== HNBC E2E CHECK START ==='
echo "WORKDIR=$WORKDIR"
echo

echo '[1/4] Installed plugin files'
"$(cd "$(dirname "$0")" && pwd)/self-check.sh"
echo

echo '[2/4] Gateway status'
openclaw gateway status || true
echo

echo '[3/4] Local runtime registry view'
node - <<'NODE'
(async () => {
  const envmod = await import('file:///usr/lib/node_modules/openclaw/dist/env-D1ktUnAV.js');
  const pimod = await import('file:///usr/lib/node_modules/openclaw/dist/pi-embedded-BaSvmUpW.js');
  const cfg = envmod.O();
  const reg = pimod.gt({ config: cfg, workspaceDir: process.env.WORKDIR, cache: false, env: process.env, throwOnLoadError: false });
  const plugin = (reg.plugins || []).find(p => p.id === 'hnbc');
  const providers = (reg.imageGenerationProviders || []).map(x => x.provider?.id).filter(Boolean);
  console.log('ACTIVE_PLUGIN=' + (plugin ? plugin.status : 'missing'));
  console.log('ACTIVE_IMAGE_PROVIDERS=' + providers.join(','));
})();
NODE
echo

echo '[4/4] Tool-side verification reminder'
echo 'Run tool call: image_generate(action="list")'
echo 'Expected: hnbc (default gpt-image-2)'
echo 'Bundled hnbc is valid; missing ~/.openclaw/extensions/hnbc alone does not prove failure.'
echo 'If local runtime sees hnbc but tool-side list does not, restart the running gateway with user approval.'
echo 'Do not pass resolution when generating with hnbc/gpt-image-2.'
echo '=== HNBC E2E CHECK END ==='

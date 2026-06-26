#!/usr/bin/env bash
set -euo pipefail

WORKDIR="${1:-/root/.openclaw/workspace}"
export WORKDIR
CONFIG_DIR="${OPENCLAW_CONFIG_DIR:-$HOME/.openclaw}"
USER_PLUGIN_DIR="$CONFIG_DIR/extensions/hnbc"
BUNDLED_PLUGIN_DIR="/usr/lib/node_modules/openclaw/dist/extensions/hnbc"

echo '=== HNBC DIAGNOSE START ==='
echo "WORKDIR=$WORKDIR"
echo "CONFIG_DIR=$CONFIG_DIR"
echo

echo '--- plugin files ---'
echo "USER_PLUGIN_DIR=$USER_PLUGIN_DIR"
if [ -d "$USER_PLUGIN_DIR" ]; then
  find "$USER_PLUGIN_DIR" -maxdepth 1 -type f | sort
else
  echo "USER_PLUGIN_DIR_MISSING=$USER_PLUGIN_DIR"
fi
echo
echo "BUNDLED_PLUGIN_DIR=$BUNDLED_PLUGIN_DIR"
if [ -d "$BUNDLED_PLUGIN_DIR" ]; then
  find "$BUNDLED_PLUGIN_DIR" -maxdepth 1 -type f | sort
else
  echo "BUNDLED_PLUGIN_DIR_MISSING=$BUNDLED_PLUGIN_DIR"
fi
echo

echo '--- gateway status ---'
openclaw gateway status || true
echo

echo '--- tool-side providers ---'
# This script only prints guidance. Agents should use image_generate(action=list) directly.
echo 'Use tool call: image_generate(action="list")'
echo

echo '--- local runtime registry ---'
node - <<'NODE'
(async () => {
  const envmod = await import('file:///usr/lib/node_modules/openclaw/dist/env-D1ktUnAV.js');
  const pimod = await import('file:///usr/lib/node_modules/openclaw/dist/pi-embedded-BaSvmUpW.js');
  const cfg = envmod.O();
  const discovery = envmod.Lt({ workspaceDir: process.env.WORKDIR, extraPaths: cfg?.plugins?.loadPaths, cache: false, env: process.env });
  const dc = discovery.candidates.filter(c => String(c.rootDir || '').includes('/hnbc') || String(c.source || '').includes('/hnbc') || String(c.idHint || '').includes('hnbc'));
  console.log('DISCOVERY_HNBC_COUNT=' + dc.length);
  console.log(JSON.stringify(dc, null, 2));
  const manifest = envmod.kt({ config: cfg, workspaceDir: process.env.WORKDIR, cache: false, env: process.env, candidates: discovery.candidates, diagnostics: discovery.diagnostics });
  const mp = manifest.plugins.filter(p => p.id === 'hnbc');
  console.log('MANIFEST_HNBC_COUNT=' + mp.length);
  console.log(JSON.stringify(mp, null, 2));
  const reg = pimod.gt({ config: cfg, workspaceDir: process.env.WORKDIR, cache: false, env: process.env, throwOnLoadError: false });
  const ap = reg.plugins.filter(p => p.id === 'hnbc');
  console.log('ACTIVE_HNBC_COUNT=' + ap.length);
  console.log(JSON.stringify(ap, null, 2));
  console.log('ACTIVE_IMAGE_GEN_PROVIDER_IDS=' + JSON.stringify((reg.imageGenerationProviders || []).map(x => x.provider?.id)));
})();
NODE
echo

echo '--- hints ---'
echo 'Bundled hnbc under /usr/lib/node_modules/openclaw/dist/extensions/hnbc is a valid install source; missing ~/.openclaw/extensions/hnbc alone does not prove the provider is absent.'
echo 'If local runtime sees hnbc but image_generate(action=list) does not, the running gateway likely still holds an old provider registry and needs restart.'
echo 'If generation fails with resolution override error, remove resolution and keep only size/aspectRatio.'
echo '=== HNBC DIAGNOSE END ==='

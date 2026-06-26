import { apiRequestForm } from 'file:///D:/tool/nodejs/node_global/node_modules/clawhub/dist/http.js';
import { listTextFiles } from 'file:///D:/tool/nodejs/node_global/node_modules/clawhub/dist/skills.js';
import { requireAuthToken } from 'file:///D:/tool/nodejs/node_global/node_modules/clawhub/dist/cli/authToken.js';
import { getRegistry } from 'file:///D:/tool/nodejs/node_global/node_modules/clawhub/dist/cli/registry.js';

const folder = 'C:/Users/zhanh/.openclaw/workspace/publish/ningyao-voice-launcher';
const filesOnDisk = await listTextFiles(folder);
const token = await requireAuthToken();
const registry = await getRegistry({ registry: '', registrySource: 'default', site: 'https://clawhub.ai' }, { cache: true });
const form = new FormData();
form.set('payload', JSON.stringify({
  slug: 'ningyao-voice-launcher',
  displayName: 'Ningyao Voice Launcher',
  version: '0.1.0',
  changelog: 'Initial public release',
  tags: ['latest'],
  acceptLicenseTerms: true
}));
for (const file of filesOnDisk) {
  const blob = new Blob([Buffer.from(file.bytes)], { type: file.contentType ?? 'text/plain' });
  form.append('files', blob, file.relPath);
}
try {
  const result = await apiRequestForm(registry, { method: 'POST', path: '/api/v1/skills', token, form });
  console.log(JSON.stringify(result));
} catch (error) {
  console.error('PUBLISH_ERROR:', error?.message || error);
  process.exit(1);
}

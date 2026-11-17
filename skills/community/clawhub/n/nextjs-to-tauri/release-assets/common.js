import fs from 'node:fs';
import { createHash } from 'node:crypto';
export const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
export const safeName = name => typeof name === 'string' && name !== '.' && name !== '..' && /^[A-Za-z0-9._-]+$/.test(name);
export const requireValue = (condition, message) => { if (!condition) throw new Error(message); };
export const platformForTarget = target => {
  const [cpu, , os] = target.split('-');
  requireValue(['x86_64', 'aarch64'].includes(cpu) && ['windows', 'darwin', 'linux'].includes(os), 'Unsupported build target');
  return ("" + (os) + "-" + (cpu));
};
export async function hashFile(file) {
  const hash = createHash('sha256');
  for await (const chunk of fs.createReadStream(file)) hash.update(chunk);
  return hash.digest('hex');
}

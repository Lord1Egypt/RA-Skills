import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';

export async function previewDemand(file) {
  const input = JSON.parse(await readFile(file, 'utf8'));
  const allowed = ['email', 'request', 'locale'];
  if (!input || Array.isArray(input) || Object.keys(input).some(key => !allowed.includes(key))) throw new Error('Demand files accept only email, request and locale. Remove all other context.');
  if (typeof input.email !== 'string' || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.email) || input.email.length > 254) throw new Error('Provide a user-approved contact email. Do not infer one from credentials or files.');
  if (typeof input.request !== 'string' || input.request.trim().length < 5 || input.request.length > 2000) throw new Error('Provide a concise image request of 5–2000 characters.');
  if (!['en','zh'].includes(input.locale)) throw new Error('Set locale to en or zh.');
  const payload = { email:input.email, request:input.request.trim(), locale:input.locale };
  const confirmation = createHash('sha256').update(JSON.stringify(payload)).digest('hex');
  return { destination:'https://imagen.chat/api/v1/gallery/demand-requests', payload, confirmation, notice:'Preview only. Nothing has been sent. Show all fields to the user and obtain explicit consent before submitting. This is a catalog suggestion, not an immediate generation order.' };
}
export async function submitDemand(client, file, confirmation) {
  const preview = await previewDemand(file);
  if (typeof confirmation !== 'string' || confirmation !== preview.confirmation) throw new Error('Preview and obtain explicit user consent for this exact payload first. Confirmation is missing or the payload changed.');
  const receipt = await client.request('/gallery/demand-requests',{ method:'POST',body:preview.payload });
  return { submitted:preview.payload, receipt, notice:'Submitted as a catalog suggestion. No immediate generation or delivery is promised.' };
}

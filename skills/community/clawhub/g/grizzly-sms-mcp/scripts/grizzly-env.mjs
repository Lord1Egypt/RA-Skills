/**
 * Grizzly SMS — API key from environment only (no network).
 * Used by grizzly-cli.mjs; egress is limited to api.grizzlysms.com there.
 */

export function readGrizzlySmsApiKey() {
  const k = process.env.GRIZZLY_SMS_API_KEY;
  if (!k || String(k).trim() === '') {
    console.error(JSON.stringify({ error: 'GRIZZLY_SMS_API_KEY required' }));
    process.exit(1);
  }
  return k;
}

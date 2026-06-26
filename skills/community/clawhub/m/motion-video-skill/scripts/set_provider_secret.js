const { resolveCatalogEntry } = require("./common");
const { SECRETS_PATH, maskSecret, setProviderSecret } = require("./secrets");

if (require.main === module) {
  const providerId = process.argv[2];
  const apiKey = process.argv[3];

  if (!providerId || !apiKey) {
    console.error("Usage: node scripts/set_provider_secret.js <provider-id> <api-key>");
    process.exit(1);
  }

  resolveCatalogEntry("tts-providers", providerId);
  setProviderSecret(providerId, { apiKey });
  console.log(`Stored secret for ${providerId} at ${SECRETS_PATH} (${maskSecret(apiKey)})`);
}

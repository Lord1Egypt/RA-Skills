const fs = require("fs");
const os = require("os");
const path = require("path");

const SECRETS_DIR = path.join(os.homedir(), ".codex", "motion-video-skill");
const SECRETS_PATH = path.join(SECRETS_DIR, "secrets.json");

function ensureSecretsDir() {
  fs.mkdirSync(SECRETS_DIR, { recursive: true });
}

function readSecrets() {
  if (!fs.existsSync(SECRETS_PATH)) {
    return { providers: {} };
  }

  try {
    return JSON.parse(fs.readFileSync(SECRETS_PATH, "utf8"));
  } catch (error) {
    return { providers: {} };
  }
}

function writeSecrets(secrets) {
  ensureSecretsDir();
  fs.writeFileSync(SECRETS_PATH, JSON.stringify(secrets, null, 2) + "\n", { mode: 0o600 });
  try {
    fs.chmodSync(SECRETS_PATH, 0o600);
  } catch (error) {
    // Best-effort permission hardening.
  }
}

function setProviderSecret(providerId, payload) {
  const secrets = readSecrets();
  secrets.providers = secrets.providers || {};
  secrets.providers[providerId] = {
    ...(secrets.providers[providerId] || {}),
    ...payload,
    updatedAt: new Date().toISOString()
  };
  writeSecrets(secrets);
}

function getProviderSecret(providerId) {
  const envMap = {
    minimax: process.env.MINIMAX_API_KEY,
    openai: process.env.OPENAI_API_KEY,
    "microsoft-azure": process.env.AZURE_SPEECH_KEY,
    doubao: process.env.DOUBAO_API_KEY
  };

  if (envMap[providerId]) {
    return { apiKey: envMap[providerId], source: "env" };
  }

  const secrets = readSecrets();
  const provider = secrets.providers && secrets.providers[providerId];
  if (!provider || !provider.apiKey) {
    return null;
  }

  return { ...provider, source: "file" };
}

function maskSecret(value) {
  if (!value || value.length < 8) {
    return "********";
  }
  return `${value.slice(0, 4)}...${value.slice(-4)}`;
}

module.exports = {
  SECRETS_PATH,
  getProviderSecret,
  maskSecret,
  readSecrets,
  setProviderSecret
};

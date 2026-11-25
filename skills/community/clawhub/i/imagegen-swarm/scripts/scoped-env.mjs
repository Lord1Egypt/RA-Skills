// Child processes get these named variables only, never a copy of the full
// environment. The names are documented in SKILL.md. Callers may pass extra
// keys for one invocation (a test override, or the three Lovart keys just read).

export const NAMED_ENV_KEYS = [
  "PATH", "PATHEXT", "SystemRoot", "WINDIR", "COMSPEC",
  "HOME", "USERPROFILE", "HOMEDRIVE", "HOMEPATH", "USER", "USERNAME", "LOGNAME",
  "LANG", "LC_ALL", "LC_MESSAGES", "LC_CTYPE",
  "TMPDIR", "TMP", "TEMP",
  "SHELL",
  "PYTHON", "PYTHONPATH", "PYTHONHOME", "PYTHONUTF8", "PYTHONIOENCODING",
  "VIRTUAL_ENV",
  "CODEX_BIN", "CODEX_HOME",
  "AGY_BIN",
  "DREAMINA_INSTALL_DIR",
  "LOVART_ACCESS_KEY", "LOVART_SECRET_KEY", "LOVART_ENV", "LOVART_BASE_URL", "LOVART_LV", "LOVART_AGENT_SKILL",
  "OPENAI_API_KEY", "GEMINI_API_KEY",
  "IMAGE_GEN_API_CONFIG", "IMAGE_GEN_API_LEDGER", "IMAGE_GEN_ENGINE_OFF", "IMAGE_GEN_MEMORY_GB", "IMAGE_GEN_MUSE_PROFILE",
  "IMAGE_GEN_MUSE_REMOTE_DIR", "IMAGE_GEN_MUSE_APPROVAL", "IMAGE_GEN_GROK_MODE", "IMAGE_GEN_CLIP_ALLOW_UNVERIFIED", "IMAGE_GEN_CLIP_MODEL",
  "IMAGE_GEN_RUN_ID", "IMAGE_GEN_SANDBOX_ESCALATE", "IMAGE_GEN_TEST_NO_KEY",
  "HTTPS_PROXY", "HTTP_PROXY", "https_proxy", "http_proxy", "NO_PROXY", "no_proxy", "ALL_PROXY", "all_proxy",
  "SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE", "NODE_EXTRA_CA_CERTS",
  "PLAYWRIGHT_BROWSERS_PATH",
  "XDG_CONFIG_HOME", "XDG_CACHE_HOME", "XDG_DATA_HOME", "XDG_RUNTIME_DIR",
  "CI", "TERM", "APPDATA", "LOCALAPPDATA",
];

function namedValue(source, key) {
  const value = source[key];
  return value === undefined ? undefined : value;
}

export function childEnv(extra, source = process.env) {
  const env = {};
  for (const key of NAMED_ENV_KEYS) {
    const value = namedValue(source, key);
    if (value !== undefined) env[key] = value;
  }
  if (extra) {
    for (const [key, value] of Object.entries(extra)) {
      if (value === undefined) continue;
      env[key] = value;
    }
  }
  return env;
}

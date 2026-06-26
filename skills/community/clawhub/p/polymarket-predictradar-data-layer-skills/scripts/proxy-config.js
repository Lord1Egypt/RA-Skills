"use strict";

const { execFileSync } = require("child_process");

function detectProxy() {
  const fromEnv =
    process.env.HTTPS_PROXY ||
    process.env.https_proxy ||
    process.env.HTTP_PROXY ||
    process.env.http_proxy;
  if (fromEnv) return fromEnv;

  try {
    const out = execFileSync("scutil", ["--proxy"], {
      encoding: "utf-8",
      timeout: 3000,
    });
    const httpsEnabled = out.match(/HTTPSEnable\s*:\s*(\d)/);
    const httpsHost = out.match(/HTTPSProxy\s*:\s*(\S+)/);
    const httpsPort = out.match(/HTTPSPort\s*:\s*(\d+)/);
    if (httpsEnabled?.[1] === "1" && httpsHost && httpsPort) {
      return `http://${httpsHost[1]}:${httpsPort[1]}`;
    }

    const httpEnabled = out.match(/HTTPEnable\s*:\s*(\d)/);
    const httpHost = out.match(/HTTPProxy\s*:\s*(\S+)/);
    const httpPort = out.match(/HTTPPort\s*:\s*(\d+)/);
    if (httpEnabled?.[1] === "1" && httpHost && httpPort) {
      return `http://${httpHost[1]}:${httpPort[1]}`;
    }
  } catch (_) {}

  try {
    const result = execFileSync(
      "python3",
      [
        "-c",
        "import urllib.request; p=urllib.request.getproxies(); print(p.get('https') or p.get('http') or '')",
      ],
      { encoding: "utf-8", timeout: 3000 },
    ).trim();
    if (result) return result;
  } catch (_) {}

  return null;
}

const PROXY = detectProxy();

module.exports = {
  detectProxy,
  PROXY,
};

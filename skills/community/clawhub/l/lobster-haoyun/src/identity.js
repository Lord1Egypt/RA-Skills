/**
 * OB Identity bootstrap — SDK FileKeyStore with 0o600 permissions.
 *
 * SDK v0.14.2 FileKeyStore handles persistence at ~/.lucky-lobster/ob-credentials.json
 * with mode 0o600 (owner read/write only). Identity is auto-restored on subsequent starts.
 */
import os from "node:os";
import path from "node:path";

const DATA_DIR = path.join(os.homedir(), ".lucky-lobster");
const CRED_FILE = path.join(DATA_DIR, "ob-credentials.json");

export async function loadOrCreateIdentity(createOceanBus) {
  const ob = await createOceanBus({
    keyStore: { type: "file", filePath: CRED_FILE },
  });

  let openid;
  let created = false;

  try {
    // Try restoring from persisted file keystore first.
    // ob.getAddress() is the current SDK API (replaces deprecated getOpenId).
    openid = await ob.getAddress();
  } catch (_) {
    // First run — no saved identity. Register to create one.
    // SDK auto-saves to FileKeyStore (0o600) after register().
    await ob.register();
    openid = await ob.getAddress();
    created = true;
  }

  return { ob, openid, agentId: ob.identity.getAgentId(), created };
}

export function getDataDir() {
  return DATA_DIR;
}

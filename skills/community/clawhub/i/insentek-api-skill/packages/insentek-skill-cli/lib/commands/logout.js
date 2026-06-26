import { clearCredentials, CREDENTIALS_FILE, getCredentialStatus } from '../core/credentials.js';
import { formatPath, printInfo, printSuccess } from '../utils.js';

export async function runLogout({ json = false } = {}) {
  const cleared = await clearCredentials();

  if (json) {
    return {
      ok: true,
      command: 'logout',
      cleared,
      connected: false,
      config_path: CREDENTIALS_FILE,
    };
  }

  if (cleared) {
    printSuccess(`Credentials removed from ${formatPath(CREDENTIALS_FILE)}`);
  } else {
    printInfo('No saved credentials to remove.');
  }

  return { ok: true, cleared, ...(await getCredentialStatus()) };
}

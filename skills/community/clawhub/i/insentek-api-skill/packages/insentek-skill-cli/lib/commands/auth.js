import { getCredentialStatus } from '../core/credentials.js';
import { formatPath, printInfo } from '../utils.js';

export async function runAuthStatus({ json = false } = {}) {
  const status = await getCredentialStatus();

  if (json) {
    return {
      ok: true,
      command: 'auth',
      subcommand: 'status',
      ...status,
    };
  }

  if (!status.connected) {
    printInfo('尚未连接 Insentek API。');
    console.log(`\n${status.message}\n`);
    return status;
  }

  console.log('\nCredential status:\n');
  console.log(`  App ID: ${status.appid}`);
  console.log(`  Secret: ${status.secret}`);
  console.log(`  Token:  ${status.token}`);
  if (status.token_updated_at) {
    console.log(`  Token updated: ${status.token_updated_at}`);
  }
  console.log(`  Encrypted: ${status.encrypted ? 'yes' : 'no'}`);
  console.log(`  Path: ${formatPath(status.config_path)}\n`);

  return status;
}

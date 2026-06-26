import { confirm, input, password } from '@inquirer/prompts';
import {
  CREDENTIALS_FILE,
  getCredentialStatus,
  getLoginHelpText,
  hasCredentials,
  loginWithCredentials,
} from '../core/credentials.js';
import { formatPath, printInfo, printSuccess, printWarn } from '../utils.js';

export async function runLogin({ yes = false, appid = null, secret = null, json = false } = {}) {
  const existing = await hasCredentials();

  if (existing && !yes && !appid && !secret) {
    const overwrite = await confirm({
      message: 'Credentials already configured. Update them?',
      default: false,
    });
    if (!overwrite) {
      if (json) {
        return { ok: true, command: 'login', skipped: true, ...(await getCredentialStatus()) };
      }
      printInfo('Login cancelled. Existing credentials kept.');
      return { ok: true, skipped: true };
    }
  }

  const resolvedAppId = appid?.trim() || await input({
    message: 'Insentek App ID',
    validate: (value) => (value.trim() ? true : 'App ID is required'),
  });

  const resolvedSecret = secret?.trim() || await password({
    message: 'Insentek App Secret',
    mask: '*',
    validate: (value) => (value.trim() ? true : 'App Secret is required'),
  });

  const result = await loginWithCredentials({
    appid: resolvedAppId,
    secret: resolvedSecret,
  });

  if (json) {
    return {
      ok: true,
      command: 'login',
      connected: true,
      ...result,
    };
  }

  printSuccess('Insentek API connected.');
  printInfo(`App ID: ${result.appid}`);
  printInfo(`Secret: ${result.secret}`);
  printInfo(`Token: ${result.token}`);
  printInfo(`Saved to ${formatPath(CREDENTIALS_FILE)}`);
  console.log('\nYou can now use the skill in your agent.\n');

  return { ok: true, connected: true, ...result };
}

export async function ensureCredentialsForInstall({ yes = false, silent = false } = {}) {
  if (await hasCredentials()) {
    return { connected: true, prompted: false };
  }

  if (silent || yes) {
    if (!silent) {
      printWarn('No Insentek API credentials found.');
      console.log(`\n${getLoginHelpText()}\n`);
    }
    return { connected: false, prompted: false };
  }

  printWarn('No Insentek API credentials found.');
  const shouldLogin = await confirm({
    message: 'Configure Insentek API credentials now?',
    default: true,
  });

  if (!shouldLogin) {
    console.log(`\n${getLoginHelpText()}\n`);
    return { connected: false, prompted: true };
  }

  await runLogin();
  return { connected: await hasCredentials(), prompted: true };
}

/**
 * Login to PowPow and store a JWT session in the user's state directory
 * (POWPOW_STATE_DIR, default ~/.powpow/session.json).
 * Password is NEVER persisted - it is only used to obtain the token.
 *
 * Usage:
 *   node login.js <username>                       (password via POWPOW_PASSWORD env)
 *   echo <password> | node login.js <username>     (stdin pipe, avoids shell history)
 *   node login.js <username> <password>            (works, but the password lands in
 *                                                   shell history / process list - avoid)
 */
const { login, ApiError } = require('./lib/api-client');

async function main() {
  const [, , usernameArg, passwordArg] = process.argv;

  if (!usernameArg) {
    console.error('Usage: node login.js <username>');
    console.error('       Password via POWPOW_PASSWORD env or stdin pipe (recommended),');
    console.error('       or as a positional argument (lands in shell history - avoid).');
    process.exit(1);
  }

  let password = passwordArg || process.env.POWPOW_PASSWORD || null;
  if (!password) {
    password = await new Promise((resolve) => {
      let data = '';
      process.stdin.setEncoding('utf-8');
      process.stdin.on('data', (chunk) => { data += chunk; });
      process.stdin.on('end', () => resolve(data.trim()));
      process.stdin.on('error', () => resolve(''));
      // If stdin is a TTY (interactive terminal), read a hidden line instead.
      if (process.stdin.isTTY) {
        process.stdout.write(`Password for ${usernameArg} (input hidden): `);
        process.stdin.setRawMode(true);
        process.stdin.removeAllListeners('data');
        let line = '';
        const onData = (ch) => {
          if (ch === '\r' || ch === '\n') {
            process.stdin.setRawMode(false);
            process.stdin.removeListener('data', onData);
            process.stdin.destroy();
            process.stdout.write('\n');
            resolve(line);
          } else if (ch === '\u0003') {
            process.exit(1);
          } else {
            line += ch;
          }
        };
        process.stdin.on('data', onData);
      }
    });
  }

  if (!password) {
    console.error('Error: password is required');
    process.exit(1);
  }

  try {
    const session = await login(usernameArg, password);
    console.log('✅ Login successful');
    console.log(`  Account: ${session.nickname ? `${session.nickname} (` : ''}${session.username}${session.nickname ? ')' : ''}`);
    console.log(`  User ID: ${session.userId}`);
    console.log(`  Token saved to ${require('./lib/api-client').SESSION_PATH} (server-side expiry ~7 days; this skill asks for re-login after 6 - sessionMaxAgeDays)`);
    console.log('  Note: your password was NOT stored anywhere');
    // Wipe reference so it does not linger in closure longer than needed.
    password = null;
  } catch (err) {
    if (err instanceof ApiError) {
      console.error(`❌ Login failed (${err.status}): ${typeof err.body === 'object' && err.body.error ? err.body.error : err.message}`);
    } else {
      console.error(`❌ Login failed: ${err.message}`);
    }
    process.exitCode = 1;
  }
}

main();

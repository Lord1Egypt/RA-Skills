import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';

const skillRoot = resolve(import.meta.dirname, '..');
const installer = join(skillRoot, 'scripts', 'install-analyticscli-cli.sh');

test('installer falls back to user-local prefix, updates profiles, and verifies a fresh shell', () => {
  const home = mkdtempSync(join(tmpdir(), 'analyticscli-home-'));
  const fakeBin = join(home, 'fake-bin');
  const fakeNpm = join(fakeBin, 'npm');

  mkdirSync(fakeBin, { recursive: true });
  writeFileSync(
    fakeNpm,
    `#!/usr/bin/env bash
set -euo pipefail

if [[ "$*" == "install -g @analyticscli/cli" ]]; then
  echo "EACCES: permission denied, mkdir '/usr/local/lib/node_modules'" >&2
  exit 243
fi

prefix=""
args=("$@")
for ((i = 0; i < \${#args[@]}; i++)); do
  if [[ "\${args[$i]}" == "--prefix" ]]; then
    prefix="\${args[$((i + 1))]}"
  fi
done

if [[ -z "$prefix" ]]; then
  echo "missing --prefix" >&2
  exit 1
fi

mkdir -p "$prefix/bin"
cat >"$prefix/bin/analyticscli" <<'EOF'
#!/usr/bin/env bash
if [[ "\${1:-}" == "--help" ]]; then
  echo "analyticscli help"
  exit 0
fi
echo "analyticscli fake"
EOF
chmod +x "$prefix/bin/analyticscli"
`,
    { mode: 0o755 },
  );

  const result = spawnSync('bash', [installer], {
    env: {
      ...process.env,
      HOME: home,
      PATH: `${fakeBin}:${process.env.PATH || ''}`,
    },
    encoding: 'utf8',
  });

  try {
    assert.equal(result.status, 0, `${result.stderr}\n${result.stdout}`);
    assert.match(result.stderr, /Fresh shell verification passed/);

    const expectedLine =
      'export PATH="$HOME/.local/bin:$HOME/.local/analyticscli-npm/bin:$PATH"';
    for (const profileName of ['.profile', '.bashrc', '.bash_profile', '.zshrc', '.zprofile']) {
      const profile = readFileSync(join(home, profileName), 'utf8');
      assert.match(profile, /AnalyticsCLI CLI user-local npm bin/);
      assert.ok(profile.includes(expectedLine), `${profileName} did not contain ${expectedLine}`);
    }

    const freshShell = spawnSync(
      'bash',
      [
        '-lc',
        'source "$HOME/.bashrc" 2>/dev/null || true; source "$HOME/.profile" 2>/dev/null || true; command -v analyticscli && analyticscli --help >/dev/null',
      ],
      {
        env: {
          HOME: home,
          PATH: '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
        },
        encoding: 'utf8',
      },
    );
    assert.equal(freshShell.status, 0, `${freshShell.stderr}\n${freshShell.stdout}`);
    assert.equal(freshShell.stdout.trim(), join(home, '.local', 'bin', 'analyticscli'));
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

#!/usr/bin/env python3
"""Register/resume, inspect readiness, and meet Welcome without exposing credentials."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

ORIGIN = 'https://lobstermatch.com'
USER_AGENT_TEMPLATE = 'LobsterMatch-Skill/{version} (+https://lobstermatch.com/connect.md)'

def package_version():
    skill = Path(__file__).resolve().parents[1] / 'SKILL.md'
    try:
        match = re.search(r'(?m)^version:\s*v?(\d+\.\d+\.\d+)\s*$', skill.read_text())
    except OSError:
        match = None
    return match.group(1) if match else '1.0.39'

def skill_user_agent(version=None):
    return USER_AGENT_TEMPLATE.format(version=version or package_version())

class FlowStop(Exception):
    def __init__(self, stage, action, **details):
        self.output = {'ok': False, 'stage': stage, 'nextAction': action, **details}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None

def load(path):
    try:
        data = json.loads(Path(path).expanduser().read_text())
        if not isinstance(data, dict):
            raise ValueError()
        return data
    except (OSError, ValueError):
        raise FlowStop('invalid_local_file', 'Provide a readable JSON object; do not paste credentials into chat.')

def save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.auth-')
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(data, stream, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        os.chmod(path, 0o600)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

def token(config):
    return config.get('agentSessionToken') or config.get('agentSessionAuth', {}).get('agentSessionToken') or ''

class Connect:
    def __init__(self, args):
        self.args = args
        self.base = args.base_url.rstrip('/')
        parsed = urllib.parse.urlsplit(self.base)
        local = parsed.hostname in ('localhost', '127.0.0.1') and args.allow_local_test
        if self.base != ORIGIN and not local:
            raise FlowStop('invalid_origin', 'Credentials may only be sent to https://lobstermatch.com.')
        self.root = Path(os.environ.get('LOBSTERMATCH_AUTH_ROOT', str(Path.home() / '.openclaw/workspace/.lobstermatch'))).expanduser()
        self.opener = urllib.request.build_opener(NoRedirect())
        self.config = {}
        self.config_path = None
        self.profile = load(args.profile) if args.profile else {}
        self.value = load(args.value_exchange) if args.value_exchange else self.profile

    def api(self, method, path, body=None, candidate=False, authenticated=True):
        if not path.startswith('/api/') or '?' in path or '#' in path or '..' in path:
            raise FlowStop('invalid_endpoint', 'Use the published LobsterMatch API contract.')
        headers = {'Content-Type': 'application/json', 'User-Agent': skill_user_agent()}
        if authenticated:
            if not token(self.config):
                raise FlowStop('recover_identity', 'Recover your existing identity with recover-agent-auth.sh or bootstrap-agent-auth.sh. Do not register again.', agentId=self.config.get('agentId'))
            headers['x-agent-id'] = self.config['agentId']
            headers['x-candidate-session-token' if candidate else 'x-agent-session-token'] = token(self.config)
        request = urllib.request.Request(self.base + path, data=json.dumps(body).encode() if body is not None else None, headers=headers, method=method)
        try:
            with self.opener.open(request, timeout=30) as response:
                data = json.loads(response.read(262144))
                if not isinstance(data, dict):
                    raise ValueError()
                return data
        except urllib.error.HTTPError as error:
            try:
                raw = error.read(8192)
            except (OSError, AttributeError):
                raw = b''
            text = raw.decode('utf-8', 'replace') if isinstance(raw, (bytes, bytearray)) else str(raw or '')
            # Cloudflare error 1010 is a user-agent block, not an auth failure. Do not print the body.
            if error.code == 403 and '1010' in text:
                raise FlowStop('request_failed', 'Cloudflare returned 403 error 1010. Send a non-default User-Agent such as LobsterMatch-Skill/<version> (+https://lobstermatch.com/connect.md). The default Python-urllib agent is blocked.', httpStatus=403, error='cloudflare-error-1010')
            try:
                reason = json.loads(text or '{}').get('error', 'request-rejected')
            except (ValueError, AttributeError):
                reason = 'request-rejected'
            if error.code in (401, 403):
                raise FlowStop('recover_identity', 'Recover or refresh same-agent auth, then rerun connect.sh. Your identity is preserved.', httpStatus=error.code)
            raise FlowStop('request_failed', 'Retry connect.sh after resolving the reported API error. Saved identity is preserved.', httpStatus=error.code, error=re.sub('[^a-zA-Z0-9_-]', '', str(reason))[:100])
        except (urllib.error.URLError, TimeoutError, ValueError):
            raise FlowStop('retry_later', 'Request did not complete. Rerun the same command; it resumes saved identity and reuses the welcome message ID.')

    def choose_identity(self):
        explicit = os.environ.get('LOBSTERMATCH_AGENT_AUTH_PATH') or os.environ.get('LOBSTERMATCH_AGENT_CONFIG')
        if explicit:
            paths = [Path(explicit).expanduser()]
        else:
            paths = list((self.root / 'agents').glob('*/agent-auth.json'))
            legacy = Path(__file__).resolve().parent.parent / '.lobstermatch-agent.json'
            if not paths and legacy.exists():
                paths = [legacy]
        choices = {}
        for path in paths:
            data = load(path)
            if str(data.get('type', '')).startswith('lobstermatch-agent-auth-pointer'):
                target = data.get('statePath') or data.get('persistentAuthPath') or data.get('configPath') or data.get('authPath')
                if not target:
                    raise FlowStop('recover_identity', 'Run recover-agent-auth.sh to restore the saved identity.')
                target_path = Path(target).expanduser()
                path = target_path if target_path.is_absolute() else path.parent / target_path
                data = load(path)
            if data.get('agentId'):
                choices[data['agentId']] = (path, data)
        if self.args.agent_id:
            choices = {key: value for key, value in choices.items() if key == self.args.agent_id}
            if not choices:
                raise FlowStop('recover_identity', 'No saved auth for that agent. Recover its existing identity; do not register a duplicate.')
        elif self.profile and choices and not explicit:
            handle = self.profile.get('publicHandle')
            source = self.profile.get('sourceAgentId')
            matching = {key: item for key, item in choices.items() if (handle and item[1].get('publicHandle') == handle) or (source and item[1].get('sourceAgentId') == source)}
            if matching:
                choices = matching
            elif not self.args.new:
                raise FlowStop('choose_identity', 'Existing local identities were found. Use --agent-id to resume one, or --new only if connecting a different agent.', agentIds=list(choices))
            else:
                choices = {}
        if len(choices) > 1:
            raise FlowStop('choose_identity', 'Use --agent-id to choose the existing identity to connect.', agentIds=list(choices))
        if choices:
            self.config_path, self.config = next(iter(choices.values()))
            if self.config.get('baseUrl', ORIGIN).rstrip('/') != self.base:
                raise FlowStop('origin_mismatch', 'Saved auth belongs to a different server. Use the correct identity.')
        elif self.args.agent_id or explicit:
            raise FlowStop('recover_identity', 'Recover the existing auth before continuing.')

    def persist_response(self, data):
        auth = data.get('agentSessionAuth') or data.get('candidateSessionAuth', {}).get('agentSessionAuth') or {}
        secret = auth.get('agentSessionToken') or data.get('candidateSessionAuth', {}).get('candidateSessionToken')
        agent_id = data.get('agentId') or auth.get('agentId') or self.config.get('agentId')
        if not re.fullmatch(r'agent-[a-zA-Z0-9-]+', str(agent_id or '')):
            raise FlowStop('invalid_registration_response', 'Registration did not return a valid agent ID. Inspect the registration status before retrying.')
        self.config.update({'agentId': agent_id, 'baseUrl': self.base})
        for key in ['registrationStatus', 'runtimeStatus']:
            if data.get(key):
                self.config[key] = data[key]
        if secret:
            self.config['agentSessionToken'] = secret
            self.config['agentSessionAuth'] = {key: value for key, value in auth.items() if key != 'agentSessionToken'}
        for key in ['publicHandle', 'sourceAgentId', 'sourcePlatform']:
            if self.profile.get(key):
                self.config[key] = self.profile[key]
        self.config_path = self.root / 'agents' / agent_id / 'agent-auth.json'
        save(self.config_path, self.config)

    def run(self):
        self.choose_identity()
        if self.args.dry_run:
            return {'ok': True, 'stage': 'preview', 'willRegister': not bool(self.config), 'profileProvided': bool(self.profile), 'nextAction': 'Review truthful profile fields, then rerun without --dry-run. No requests were sent.'}
        if not self.config:
            if not self.profile or not str(self.profile.get('name') or self.profile.get('agentName') or '').strip() or not str(self.profile.get('profile') or self.profile.get('shortDescription') or '').strip():
                raise FlowStop('needs_profile', 'Prepare a truthful agent-registration.json and run bash scripts/connect.sh --profile agent-registration.json. The agent should fill it from its own capabilities; ask its owner only for genuinely missing facts.')
            identity = self.profile.get('sourceAgentId') or self.profile.get('publicHandle')
            if not identity or 'replace-' in str(identity):
                raise FlowStop('needs_identity', 'Set your real stable sourceAgentId or a unique publicHandle in the profile.')
            payload = {**self.profile, 'idempotencyKey': 'connect-' + hashlib.sha256((str(self.profile.get('sourcePlatform', '')) + ':' + str(identity)).encode()).hexdigest()[:40]}
            registered = self.api('POST', '/api/agent-onboarding/install-register', payload, authenticated=False)
            self.persist_response(registered)
        agent_id = self.config['agentId']
        prefix = '/api/agents/' + agent_id
        requirements = self.api('GET', prefix + '/upgrade-requirements', authenticated=False)
        if requirements.get('canSelfUpgrade'):
            allowed = requirements.get('requiredValueExchangeFields', [])
            values = {key: self.value[key] for key in allowed if key in self.value}
            if requirements.get('missingRequirements') and values:
                self.api('POST', prefix + '/value-exchange', values, candidate=True)
                requirements = self.api('GET', prefix + '/upgrade-requirements', authenticated=False)
            if requirements.get('missingRequirements'):
                return {'ok': False, 'stage': 'needs_details', 'agentId': agent_id, 'missingRequirements': requirements['missingRequirements'], 'nextAction': 'Add these truthful fields to the profile (or --value-exchange file) and rerun connect.sh. Your existing candidate will be reused.'}
            checked = self.api('POST', prefix + '/registration-gate/recheck', {}, candidate=True)
            self.persist_response(checked)
        funnel = self.api('GET', prefix + '/onboarding-funnel', authenticated=False)
        if not funnel.get('matchingReady'):
            return {'ok': False, 'stage': 'awaiting_approval', 'agentId': agent_id, 'missingRequirements': funnel.get('blockers', []), 'nextAction': funnel.get('nextAction') or 'Registration is saved. Check again later; approval is not automatic.'}
        # Runtime authorization is enforced by the welcome endpoint, not inferred from a public status.
        welcome_path = '/api/welcome/' + self.config['agentId']
        conversation = self.api('GET', welcome_path)
        if self.args.message_file:
            message = Path(self.args.message_file).read_text().strip()
            message_id = 'intro-' + hashlib.sha256(message.encode()).hexdigest()[:40]
        else:
            message = 'Hello! I have connected to LobsterMatch and would like to meet the welcome assistant.' if self.args.language == 'en' else 'Привет! Я подключился к LobsterMatch и хочу познакомиться с приветственным помощником.'
            message_id = 'first-welcome-v1'
        if len(message) > 2000 or not message:
            raise FlowStop('invalid_message', 'Use a non-empty introduction of at most 2000 characters.')
        # A rerun reads an existing reply rather than sending another introduction.
        if not any(item.get('replyTo') == message_id for item in conversation.get('messages', [])):
            if not any(item.get('id') == message_id for item in conversation.get('messages', [])):
                conversation = self.api('POST', welcome_path, {'messageId': message_id, 'message': message, 'language': self.args.language})
            deadline = time.monotonic() + min(max(self.args.wait_seconds, 0), 90)
            while not any(item.get('replyTo') == message_id for item in conversation.get('messages', [])) and time.monotonic() < deadline:
                time.sleep(min(5, max(0, deadline - time.monotonic())))
                conversation = self.api('GET', welcome_path)
        reply = next((item for item in conversation.get('messages', []) if item.get('replyTo') == message_id), None)
        return {'ok': bool(reply), 'stage': 'welcomed' if reply else 'awaiting_welcome_reply', 'agentId': agent_id, 'profileUrl': funnel.get('canonicalUrl'), 'welcomeReply': reply.get('text') if reply else None, 'lastInboxCheckAt': conversation.get('lastInboxCheckAt'), 'nextAction': 'Introduce your capabilities and first task using --message-file introduction.txt, or explore https://lobstermatch.com/agents.' if reply else 'The message is saved. Rerun this command to read the reply; it will not duplicate the message.', 'reputationChanged': False}

def exec_watch(args):
    script = Path(__file__).resolve().parent / 'agent-watch.sh'
    interval = args.interval if isinstance(args.interval, int) and args.interval > 0 else 5
    command = ['bash', str(script), '--interval', str(interval)]
    if args.loop:
        command.append('--loop')
    try:
        os.execvp('bash', command)
    except OSError:
        print(json.dumps({
            'ok': False,
            'stage': 'missing_runtime',
            'error': 'bash-required',
            'nextAction': 'Run bash scripts/install-watch-cron.sh --trigger-cmd with a command that starts one agent turn. A flag-only cron does not wake the agent. Do not run --watch inside an agent turn.',
        }, indent=2))
        return 1

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile'); parser.add_argument('--value-exchange'); parser.add_argument('--agent-id')
    parser.add_argument('--message-file'); parser.add_argument('--language', choices=['en', 'ru'], default='en')
    parser.add_argument('--new', action='store_true'); parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--watch', action='store_true', help='Run scripts/agent-watch.sh. Does not start an agent turn.')
    parser.add_argument('--loop', action='store_true', help='With --watch, poll until stopped. Prefer a single cron run.')
    parser.add_argument('--interval', type=int, default=5, help='With --watch --loop, minutes between polls.')
    parser.add_argument('--wait-seconds', type=int, default=45)
    parser.add_argument('--base-url', default=ORIGIN); parser.add_argument('--allow-local-test', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.watch:
        return exec_watch(args)
    try:
        flow = Connect(args)
        flow.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        with open(flow.root / '.connect.lock', 'a') as lock:
            try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError: raise FlowStop('already_running', 'A connection attempt is already running. Wait for its result.')
            result = flow.run()
    except FlowStop as error:
        result = error.output
    except (OSError, ValueError, KeyError, TypeError):
        result = {'ok': False, 'stage': 'local_error', 'nextAction': 'Check local JSON files and permissions, then rerun. Do not share credentials.'}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get('ok') or result.get('stage') in ['needs_details', 'awaiting_approval', 'awaiting_welcome_reply'] else 1

if __name__ == '__main__':
    raise SystemExit(main())

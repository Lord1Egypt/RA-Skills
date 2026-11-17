"""Explicit destinations and durable receipts; no secrets are persisted."""
import hashlib
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit
import omni_core as c
from omni_document import validate_key

MODES = {
    'html': ('local', 'host'), 'pdf': ('local', 'host'), 'markdown': ('local', 'host'), 'docx': ('local', 'host'),
    'obsidian': ('local',), 'notion': ('api', 'cli', 'host', 'import'),
    'feishu': ('api', 'cli', 'host', 'import'), 'tencent': ('api', 'mcp', 'host', 'import'),
    'dingtalk': ('cli', 'host', 'import'), 'generic': ('host', 'import'),
}
DESTINATIONS = {'parent_page_id', 'vault_path', 'subdir', 'folder_token', 'folder_id',
                'workspace_id', 'name'}
CREDENTIALS = {'token', 'app_id', 'app_secret', 'client_id', 'open_id'}
HOSTS = {'notion': ('notion.so', 'notion.site', 'app.notion.com'), 'feishu': ('feishu.cn', 'larksuite.com'),
         'tencent': ('docs.qq.com',), 'dingtalk': ('dingtalk.com',)}


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def validate_delivery(target):
    if not isinstance(target, dict) or set(target) - {'platform', 'mode', 'destination', 'credential_env', 'account_id', 'cli_profile', 'auth_profile'}:
        raise ValueError('Delivery accepts only platform, mode, destination and credential_env; keep secrets outside config.')
    platform = target.get('platform'); mode = target.get('mode')
    if not isinstance(platform,str) or not isinstance(mode,str) or platform not in MODES or mode not in MODES[platform]:
        raise ValueError('Unsupported delivery platform/mode; choose a documented route.')
    for key in ('account_id', 'cli_profile', 'auth_profile'):
        value = target.get(key)
        if value is not None and (not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_.:@-]{1,128}', value)):
            raise ValueError('Invalid non-secret connection identity/profile.')
    destination = target.get('destination', {}); credentials = target.get('credential_env', {})
    if not isinstance(destination, dict) or set(destination) - DESTINATIONS:
        raise ValueError('Unsupported destination field; do not put credentials in destination.')
    if any(not isinstance(v, str) or not v.strip() for v in destination.values()):
        raise ValueError('Destination values must be nonempty strings.')
    if not isinstance(credentials, dict) or set(credentials) - CREDENTIALS:
        raise ValueError('Use documented credential roles and environment-variable references.')
    if any(not isinstance(v, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]{0,127}', v) for v in credentials.values()):
        raise ValueError('credential_env values must be environment-variable names, never tokens.')
    if 'subdir' in destination:
        p = Path(destination['subdir'])
        if p.is_absolute() or '..' in p.parts or '\\' in destination['subdir']:
            raise ValueError('Vault subdir must be a safe relative directory.')


def preflight(target, environ=None):
    if target is None:
        return {'ready': False, 'missing': ['delivery.platform'], 'note': 'Ask the learner for a destination.'}
    validate_delivery(target)
    environ = os.environ if environ is None else environ
    platform = target['platform']; mode = target['mode']
    dest = target.get('destination', {}); refs = target.get('credential_env', {})
    missing = []
    required = {'notion': ('parent_page_id',), 'feishu': ('folder_token',),
                'tencent': ('folder_id',), 'obsidian': ('vault_path', 'subdir')}
    if mode not in ('import',) and platform in required:
        missing.extend('destination.' + k for k in required[platform] if not dest.get(k))
    if platform == 'dingtalk' and mode != 'import' and not (dest.get('folder_id') or dest.get('workspace_id')):
        missing.append('destination.folder_id or destination.workspace_id')
    if mode=='mcp':
        for k in ('account_id','auth_profile'):
            if not target.get(k):missing.append(k+' (run connect)')
    if mode == 'api':
        roles = {'notion': ('token',), 'tencent': ('client_id', 'open_id', 'token')}
        needed = roles.get(platform, ())
        if platform == 'feishu':
            needed = ('token',) if refs.get('token') else ('app_id', 'app_secret')
        for role in needed:
            if not refs.get(role):
                missing.append('credential_env.' + role)
            elif not environ.get(refs[role]):
                missing.append('environment.' + refs[role])
    if platform == 'obsidian' and dest.get('vault_path'):
        if not Path(dest['vault_path']).expanduser().is_dir():
            missing.append('existing writable Obsidian Vault')
    if mode == 'cli':
        binary = {'notion': 'ntn', 'feishu': 'lark-cli', 'dingtalk': 'dws'}[platform]
        if not shutil.which(binary): missing.append('installed and authorized ' + binary + ' CLI')
        if platform in ('notion', 'feishu') and not target.get('account_id'): missing.append('account_id (run connect)')
    return {'ready': not missing, 'platform': platform, 'mode': mode, 'missing': missing,
            'note': 'Host/import routes need actual host tools and content readback before recording delivery.' if mode in ('host', 'import') else 'Configuration check only; publish validates remote permissions and content.'}


def default_formats(config):
    target = config.get('delivery')
    if not target:
        return ['pdf']
    platform = target['platform']
    if platform in ('pdf', 'markdown', 'docx', 'html'):
        return [platform]
    if platform=='tencent' and target.get('mode')=='mcp':return ['docx','markdown']
    if platform == 'notion' and target.get('mode') == 'import':
        return ['docx', 'markdown']
    return ['markdown'] if platform in ('obsidian', 'notion') else ['docx', 'markdown']


def receipt_path(root, key):
    validate_key(key)
    path = root / 'receipts' / (key + '.json')
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Receipt path escapes project.')
    return path


def binding(root, key, manifest, target):
    manifest_hash = c.digest(root / 'manifests' / (key + '.json'))
    target_hash = fingerprint(target)
    return {'key': key, 'manifest_hash': manifest_hash, 'target_hash': target_hash,
            'delivery_id': fingerprint([manifest_hash, target_hash, key])}


def check_binding(root, key, receipt, manifest=None):
    manifest = manifest or c.reviewed(root, key)
    target = c.read(root / 'config.json').get('delivery')
    if not target:
        raise ValueError('Receipt needs an explicit configured delivery target.')
    expected = binding(root, key, manifest, target)
    if any(receipt.get(k) != v for k, v in expected.items()):
        raise ValueError('Receipt does not match the reviewed document and configured destination.')


def status(root, key):
    root = Path(root).resolve(); path = receipt_path(root, key)
    if not path.exists():
        return {'key': key, 'status': 'not_published'}
    receipt = c.read(path); check_binding(root, key, receipt)
    return receipt


def require_verified(root, key):
    receipt = status(root, key)
    if receipt.get('status') != 'verified':
        raise ValueError('Primary destination is not verified; publish/reconcile the existing document first.')
    return receipt


def verify_url(platform, url):
    parsed = urlsplit(url)
    host = parsed.hostname or ''
    if parsed.scheme != 'https' or parsed.username or parsed.password or not host:
        raise ValueError('Remote receipt needs an HTTPS document URL without credentials.')
    if any(s in parsed.query.lower() for s in ('token', 'secret', 'key=', 'auth=')):
        raise ValueError('Do not store credential-bearing URLs in receipts.')
    if platform in HOSTS and not any(host == h or host.endswith('.' + h) for h in HOSTS[platform]):
        raise ValueError('Receipt URL does not belong to the selected provider.')


def record_receipt(root, key, supplied):
    root = Path(root).resolve(); validate_key(key)
    with c.lock(root):
        target = c.read(root / 'config.json').get('delivery', {})
        if target.get('mode') not in ('host', 'import'):
            raise ValueError('External attestations are only for configured host/import routes.')
        if key != 'plan':
            c.check_approval(root, c.read(root / 'state.json'))
        check_binding(root, key, supplied)
        if supplied.get('status') != 'verified' or not supplied.get('remote_id'):
            raise ValueError('Host receipt must identify a verified remote document.')
        evidence = supplied.get('evidence', {})
        if not all(evidence.get(k) is True for k in ('content_checked', 'image_checked', 'links_checked')) or not evidence.get('note', '').strip():
            raise ValueError('Read back document content, image and source links; record actual evidence.')
        verify_url(target['platform'], supplied.get('url', ''))
        path = receipt_path(root, key)
        if path.exists() and c.read(path).get('status') == 'verified':
            old = c.read(path)
            if old.get('remote_id') != supplied['remote_id']:
                raise ValueError('Verified receipt is immutable; preserve the original delivery.')
            return old
        receipt = dict(binding(root, key, c.reviewed(root, key), target), status='verified',
                       platform=target['platform'], mode=target['mode'], remote_id=str(supplied['remote_id']),
                       url=supplied['url'], evidence={k: evidence[k] for k in ('content_checked', 'image_checked', 'links_checked', 'note')},
                       verified_at=c.today(root))
        c.save(path, receipt)
        return receipt


def publish(root, key, adapter=None):
    root = Path(root).resolve(); validate_key(key)
    with c.lock(root):
        config = c.read(root / 'config.json'); target = config.get('delivery')
        if not target:
            raise ValueError('Legacy PDF delivery uses the host; configure a new course for explicit destinations.')
        validate_delivery(target)
        manifest = c.reviewed(root, key)
        if key != 'plan':
            state = c.read(root / 'state.json'); c.check_approval(root, state)
            if str(int(key[3:])) not in state['lessons']:
                action = c.next_action(root)
                if action.get('day') != int(key[3:]) or action['action'] != 'deliver_existing':
                    raise ValueError('Publish only the next reviewed lesson in an active course.')
        path = receipt_path(root, key)
        if path.exists():
            receipt = c.read(path); check_binding(root, key, receipt, manifest)
            if receipt['status'] == 'verified':
                return receipt
            if receipt['status'] in ('creating', 'needs_reconciliation') and not (receipt.get('remote_id') or receipt.get('task_id')):
                raise ValueError('Write outcome is uncertain. Reconcile the existing remote document before retrying.')
        else:
            receipt = dict(binding(root, key, manifest, target), status='prepared',
                           platform=target['platform'], mode=target['mode'])
        def checkpoint(**changes):
            candidate=dict(receipt,**changes)
            if candidate.get('status')=='pending' and target['mode'] in ('api','cli','mcp'):
                from omni_http import segment
                segment(candidate.get('remote_id') or candidate.get('task_id'))
            receipt.update(changes); c.save(path, receipt)
        formats = manifest.get('artifacts', {'pdf': manifest.get('pdf')})
        needed = default_formats(config)[0]
        # Keep previously reviewed Markdown-only Notion imports resumable.
        if target['platform'] == 'notion' and target['mode'] == 'import' and not formats.get(needed) and formats.get('markdown'):
            needed = 'markdown'
        if not formats.get(needed):
            raise ValueError('Required destination export missing: ' + needed)
        artifact = root / formats[needed]
        if target['mode'] in ('host', 'import'):
            checkpoint(status='awaiting_import' if target['mode'] == 'import' else 'prepared',
                       artifact=str(artifact.relative_to(root)))
            return receipt
        ready = preflight(target)
        if not ready['ready']:
            raise ValueError('Missing delivery information: ' + ', '.join(ready['missing']))
        if target['platform'] in ('pdf', 'markdown', 'docx', 'html'):
            checkpoint(status='verified', artifact=str(artifact.relative_to(root)),
                       content_hash=c.digest(artifact), verified_at=c.today(root))
            return receipt
        checkpoint(status=receipt.get('status', 'prepared'))
        if adapter is None:
            from omni_providers import publish_document
            adapter = publish_document
        try:
            result = adapter(root, manifest, target, receipt, checkpoint)
            if result.get('status') == 'verified' and target['platform'] != 'obsidian':
                if not result.get('remote_id') or not result.get('url'):
                    raise ValueError('Provider did not identify its verified document.')
                verify_url(target['platform'], result['url'])
                evidence = result.get('evidence', {})
                if not all(evidence.get(k) is True for k in ('content_checked', 'image_checked', 'links_checked')):
                    raise ValueError('Provider did not verify content, image and links.')
            if result.get('status') == 'verified': receipt.pop('error', None)
            checkpoint(**result)
        except Exception:
            # Never persist raw provider exceptions: they can contain tokens/headers.
            checkpoint(status='needs_reconciliation' if receipt['status'] == 'creating' else receipt['status'],
                       error='Provider operation failed. Check authorization/task status and retry only after reconciliation.')
            raise RuntimeError(receipt['error']) from None
        return receipt


def reconcile(root, key, remote_id=None, url=None, task_id=None):
    """Identify an observed existing object; only a later provider readback can verify it."""
    root = Path(root).resolve(); validate_key(key)
    with c.lock(root):
        path = receipt_path(root, key)
        receipt = c.read(path); check_binding(root, key, receipt)
        target = c.read(root / 'config.json')['delivery']
        if target['mode'] not in ('api', 'cli', 'mcp') or receipt['status'] == 'verified':
            raise ValueError('Reconcile only an unfinished API/CLI delivery.')
        if bool(remote_id) == bool(task_id):
            raise ValueError('Supply exactly one observed document ID or import task ID.')
        from omni_http import segment
        segment(remote_id or task_id)
        if remote_id:
            verify_url(target['platform'], url or '')
            receipt.update(remote_id=remote_id, url=url, status='pending')
        else:
            receipt.update(task_id=task_id, status='pending')
        receipt.pop('error', None)
        c.save(path, receipt)
        return receipt

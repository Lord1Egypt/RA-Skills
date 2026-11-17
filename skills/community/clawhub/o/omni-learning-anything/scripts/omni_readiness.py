"""Local dependencies plus fresh, course-scoped host attestations. No remote calls."""
import importlib.util
import shutil
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
import omni_core as c

CAPABILITIES = {
    'execution': 'Verify command execution and course-file access in this host.',
    'research': 'Open an authoritative source with the actual host research tool.',
    'images': 'Verify access to the agreed image-generation or licensed-source-image workflow.',
    'inspection': 'Inspect a real artifact in the selected format with an available viewer.',
    'notification': 'Verify the agreed user-facing delivery/notification mechanism.',
    'scheduler': 'Verify a real native job in this execution context after plan approval.',
    'credentials': 'Check the pinned account/destination with official tools in this execution context; do not export credentials.',
}


def tex_binary():
    found = shutil.which('xelatex')
    if found:
        return found
    for folder in (Path.home()/'Library/TinyTeX/bin', Path.home()/'.TinyTeX/bin', Path('/Library/TeX/texbin')):
        for path in sorted(folder.glob('*/xelatex')) + [folder/'xelatex']:
            if path.is_file():
                import os
                if os.access(path, os.X_OK):
                    return str(path)
    return None


def host_evidence(root, config_path, report, background, now, host):
    result = {key: {'status': 'unknown', 'evidence_present': False, 'next_action': action} for key, action in CAPABILITIES.items()}
    reasons = []
    if report is None:
        return result, ['Host capability evidence has not been supplied.']
    if not isinstance(report, dict):
        raise ValueError('Host report must be a JSON object.')
    try:
        checked = datetime.fromisoformat(report.get('checked_at', '').replace('Z', '+00:00'))
        if checked.tzinfo is None or not -timedelta(minutes=5) <= now-checked <= timedelta(hours=24):
            reasons.append('Host evidence is stale, future-dated or lacks a timezone.')
    except (ValueError, TypeError, AttributeError):
        reasons.append('Host evidence needs an actual timezone-aware checked_at.')
    if not report.get('host') or report.get('context') not in ('foreground', 'background'):
        reasons.append('Host evidence needs host and foreground/background context.')
    if not isinstance(host, str) or not host.strip() or report.get('host') != host:
        reasons.append('Supply the expected execution host with --host; the evidence must match it.')
    project = report.get('project')
    same_project = isinstance(project, str) and bool(project) and Path(project).is_absolute() and Path(project).resolve() == root
    if not same_project or not config_path.is_file() or report.get('config_hash') != c.digest(config_path):
        reasons.append('Host evidence does not match this course path and current config hash.')
    if report.get('context') != ('background' if background else 'foreground'):
        reasons.append('Host evidence belongs to a different execution context; foreground and background checks are separate.')
    if background:
        try:
            state = c.read(root/'state.json'); config = c.read(root/'config.json')
            c.check_approval(root, state)
            schedule = state.get('schedule')
            if config_path.resolve() != (root/'config.json').resolve() or state.get('status') != 'active' or config.get('sample_mode'):
                raise ValueError('Not an active scheduled course.')
            if not isinstance(schedule, dict) or schedule.get('host') != host or not schedule.get('job_id') or report.get('job_id') != schedule['job_id']:
                raise ValueError('Schedule scope changed.')
        except (ValueError, OSError, KeyError, TypeError):
            reasons.append('Background evidence needs an active approved non-sample course and its matching registered host/job; recheck after a handoff or job change.')
    if reasons:
        return result, reasons
    capabilities = report.get('capabilities', {})
    if not isinstance(capabilities, dict):
        raise ValueError('Host capabilities must be a JSON object.')
    for key, item in capabilities.items():
        if key not in result or not isinstance(item, dict):
            continue
        status = item.get('status'); evidence = item.get('evidence')
        present = isinstance(evidence, str) and bool(evidence.strip())
        if status == 'unavailable' or status == 'verified' and present:
            result[key].update(status=status, evidence_present=present)
    # Do not echo supplied evidence strings: they may contain sensitive tool output.
    return result, []


def diagnose(root, report=None, *, background=False, now=None, config_path=None, host=None):
    from omni_delivery import default_formats, preflight
    root = Path(root).resolve(); now = now or datetime.now(timezone.utc)
    config_path = Path(config_path).resolve() if config_path else root/'config.json'
    config = c.read(config_path) if config_path.is_file() else None
    formats = default_formats(config) if config is not None else []
    writable = False
    if root.is_dir():
        try:
            with tempfile.TemporaryFile(dir=root):
                writable = True
        except OSError:
            pass
    checks = []

    def add(key, ready, action):
        checks.append({'id': key, 'status': 'verified' if ready else 'unavailable', 'next_action': '' if ready else action})

    add('runtime.python', sys.version_info >= (3, 10), 'Use Python 3.10 or later.')
    add('archive.writable', writable, 'Create or make the agreed course archive writable, then retry.')
    modules = {}
    if 'docx' in formats:
        modules.update(docx='python-docx', PIL='Pillow')
    if 'pdf' in formats:
        modules.update(pypdf='pypdf', pypdfium2='pypdfium2')
    target = (config or {}).get('delivery')
    if target and target['mode'] in ('api', 'mcp'):
        modules['requests'] = 'requests'
        if target['platform'] == 'tencent' and target['mode'] == 'api': modules['qcloud_cos'] = 'cos-python-sdk-v5'
    if target and target['platform'] == 'tencent' and target['mode'] == 'mcp':
        modules['keyring'] = 'keyring'
    for module, package in modules.items():
        try:
            available = importlib.util.find_spec(module) is not None
        except (ImportError, ValueError):
            available = False
        add('module.'+module, available, 'Install '+package+' in the selected interpreter; see references/setup.md.')
    xelatex = tex_binary()
    if 'pdf' in formats:
        add('tool.xelatex', bool(xelatex), 'Install/configure XeLaTeX; actual compilation must still check packages and fonts.')
    delivery = preflight(target)
    if config is not None and target is None:
        delivery = {'ready': True, 'platform': 'pdf', 'mode': 'legacy', 'missing': [],
                    'note': 'Legacy PDF configuration only; host delivery and rendering still require verification.'}
    host_checks, reasons = host_evidence(root, config_path, report, background, now, host)
    required = ['execution', 'research', 'images', 'inspection', 'notification']
    if background:
        required.append('scheduler')
        if target and target['platform'] in ('notion', 'feishu', 'dingtalk', 'tencent', 'generic'):
            required.append('credentials')
    local_ready = all(x['status'] == 'verified' for x in checks)
    host_ready = all(host_checks[key]['status'] == 'verified' for key in required)
    ready = local_ready and delivery['ready'] and host_ready
    return {'python': sys.version.split()[0], 'xelatex': xelatex, 'output_writable': writable,
            'formats': formats, 'delivery': delivery, 'checks': checks, 'host': host_checks,
            'host_evidence_issues': reasons, 'required_host_capabilities': required,
            'context': 'background' if background else 'foreground',
            'config_hash': c.digest(config_path) if config_path.is_file() else None,
            'local_ready': local_ready, 'ready_to_generate': ready,
            'unattended_ready': bool(background and ready),
            'note': 'Local checks and host attestations only; no remote access/write, successful publication or learner approval is established.'}

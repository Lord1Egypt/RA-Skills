"""Manage only this adapter's user service, never OpenClaw's service."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
from .core import Problem

UNIT='openclaw-gmail-connect.service'
SCRIPT=Path(__file__).resolve().parents[1]/'gmail_connect.py'

def run(args):
    try:
        result=subprocess.run(args, capture_output=True,text=True,timeout=15,check=False)
    except (OSError,subprocess.TimeoutExpired):
        raise Problem('User service manager is unavailable. Run the wizard in an Ubuntu desktop login session.') from None
    if result.returncode:
        raise Problem('User service command failed. Check: systemctl --user status '+UNIT)
    return result.stdout.strip()

def quote(value, exec_arg=False):
    # systemd has its own quoting/specifier rules; this is not a shell command.
    value=str(value).replace('\\','\\\\').replace('"','\\"').replace('%','%%').replace('\n','\\n').replace('\r','\\r')
    return '"'+(value.replace('$','$$') if exec_arg else value)+'"'

def enabled_state():
    try:
        result=subprocess.run(['systemctl','--user','is-enabled',UNIT],capture_output=True,text=True,timeout=5)
        return result.stdout.strip()
    except (OSError,subprocess.TimeoutExpired):
        raise Problem('Cannot inspect the existing user-service state.') from None

def status():
    if not shutil.which('systemctl'):return {'available':False,'active':False}
    try:
        r=subprocess.run(['systemctl','--user','is-active',UNIT],capture_output=True,text=True,timeout=5)
        return {'available':True,'active':r.returncode==0}
    except (OSError,subprocess.TimeoutExpired):return {'available':False,'active':False}

def install(store):
    if os.geteuid()==0:raise Problem('Run as your ordinary Ubuntu user, not root.')
    dest=Path.home()/'.config/systemd/user'/UNIT
    dest.parent.mkdir(parents=True,exist_ok=True)
    unit='''# Managed by gmail-connect; independent of OpenClaw Gateway.
[Unit]
Description=Gmail Connect mailbox monitor
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart={python} {script} monitor
Environment={state}
Restart=on-failure
RestartSec=30
TimeoutStopSec=10
UMask=0077
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths={root}

[Install]
WantedBy=default.target
'''.format(python=quote(sys.executable,True),script=quote(SCRIPT,True),root=quote(store.root),state=quote('GMAIL_CONNECT_HOME='+str(store.root)))
    if dest.exists() and not dest.read_text().startswith('# Managed by gmail-connect;'):
        raise Problem('A service with this name already exists and is not owned by this skill.')
    previous=dest.read_bytes() if dest.exists() else None
    was_active=status()['active']
    was_enabled=enabled_state()
    if previous is None and (was_active or was_enabled in ('enabled','enabled-runtime')):
        raise Problem('A service with this name is already loaded from another location. Resolve it before installing.')
    dest.write_text(unit)
    try:
        run(['systemctl','--user','daemon-reload'])
        run(['systemctl','--user','enable','--now',UNIT])
        if not status()['active']:raise Problem('Monitor did not become active; inspect its service status.')
    except Problem as original:
        cleanup=[]
        for operation in ('stop','disable'):
            try:run(['systemctl','--user',operation,UNIT])
            except Problem:cleanup.append(operation)
        if previous is None:dest.unlink(missing_ok=True)
        else:dest.write_bytes(previous)
        try:
            run(['systemctl','--user','daemon-reload'])
            if was_enabled in ('enabled','enabled-runtime'):
                run(['systemctl','--user','enable']+(['--runtime'] if was_enabled=='enabled-runtime' else [])+[UNIT])
            if was_active:run(['systemctl','--user','start',UNIT])
        except Problem:cleanup.append('restore prior state')
        if cleanup:raise Problem('Monitor installation failed; rollback was incomplete ('+', '.join(cleanup)+'). Inspect '+UNIT+'. OpenClaw Gateway was not changed.') from None
        raise original
    return {'installed':True,'note':'Runs while your user manager runs. For unattended cold boots, enable lingering using the command shown in the wizard.'}

def stop():
    dest=Path.home()/'.config/systemd/user'/UNIT
    if dest.exists() and not dest.read_text().startswith('# Managed by gmail-connect;'):
        raise Problem('This service is not owned by Gmail Connect.')
    if dest.exists():run(['systemctl','--user','disable','--now',UNIT])
    return {'stopped':True}

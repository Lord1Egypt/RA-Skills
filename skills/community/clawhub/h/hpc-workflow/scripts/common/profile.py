"""Render a reviewed Slurm site profile into a standalone deployment bundle."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex

ROOT = Path(__file__).resolve().parents[1]


def validate(profile):
    if profile.get('version') != 1:
        raise ValueError('Profile version must be 1')
    name = profile['name']
    if not re.fullmatch(r'[a-z][a-z0-9-]{0,30}', name):
        raise ValueError('Invalid site namespace')
    adapter = profile['adapter']
    if adapter not in ('direct-ssh', 'psc-bridge'):
        raise ValueError('Choose direct-ssh or psc-bridge after probing compute access')
    verified = profile['verified']
    if verified.get('scheduler') != 'slurm' or not verified.get('local_disk') or not verified.get('persistent_archive'):
        raise ValueError('Scheduler, disk-backed local storage and archive persistence must be established')
    if adapter == 'direct-ssh' and verified.get('compute_ssh') is not True:
        raise ValueError('Direct adapter requires verified login-to-compute SSH access')
    storage = profile['storage']
    for key in ('local_template', 'local_prefix', 'archive', 'results'):
        value = storage[key]
        if not isinstance(value, str) or not value or '\n' in value or '<' in value or '..' in value.split('/'):
            raise ValueError('Invalid or unfilled storage path: ' + key)
        if not value.startswith(('/', '$HOME', '${HOME}', '$SLURM_TMPDIR', '${SLURM_TMPDIR}')):
            raise ValueError('Storage path must be absolute or use a documented runtime variable: ' + key)
    if not storage['local_prefix'].endswith('/') or storage['local_prefix'] == '/':
        raise ValueError('Local prefix must name a constrained directory ending in /')
    if not any(token in storage['local_template'] for token in ('$SLURM_JOB_ID', '${SLURM_JOB_ID}', '$SLURM_TMPDIR', '${SLURM_TMPDIR}')):
        raise ValueError('Local template must isolate each job')
    for key in ('archive', 'results'):
        if 'SLURM_' in storage[key] or storage[key].startswith(storage['local_prefix']):
            raise ValueError(key + ' must live on persistent storage, outside job-local disk')
    allocation = profile['allocation']
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', allocation['account']):
        raise ValueError('An actual account is required')
    if not isinstance(allocation['cpus'], int) or allocation['cpus'] < 1 or not re.fullmatch(r'[1-9][0-9]*[MG]?', allocation['memory']):
        raise ValueError('CPU and memory requests must be explicit')
    if not re.fullmatch(r'[0-9]+:[0-5][0-9]:[0-5][0-9]', allocation['walltime']):
        raise ValueError('Invalid walltime')
    catalog = allocation['gpus']
    if allocation['default_gpu'] not in catalog or not catalog:
        raise ValueError('Default GPU must exist in the catalog')
    for gpu, data in catalog.items():
        if not re.fullmatch(r'[a-z][a-z0-9-]*', gpu):
            raise ValueError('Invalid GPU key')
        if adapter == 'psc-bridge' and gpu not in ('h100', 'a100', 'v100', 'l40s'):
            raise ValueError('The PSC bridge adapter requires adaptation for this GPU key')
        partitions = data['partition'].split(',')
        if (not re.fullmatch(r'[A-Za-z0-9_-]+', data['gres']) or
                not partitions or len(partitions) != len(set(partitions)) or
                any(not re.fullmatch(r'[A-Za-z0-9_-]+', partition) for partition in partitions)):
            raise ValueError('Invalid GRES or partition')
        if not isinstance(data['max_count'], int) or data['max_count'] < 1:
            raise ValueError('GPU capacity must be established')
        qos = data.get('qos', '')
        if qos:
            if qos not in verified['project_qos'] or any(qos not in verified['partition_qos'].get(partition, []) for partition in partitions):
                raise ValueError('QoS is not permitted by both project and partition: ' + qos)
        elif not verified.get('default_qos_allowed'):
            raise ValueError('A permitted explicit QoS or verified default QoS is required')
    transport = profile['transport']['exec_argv']
    if not isinstance(transport, list) or not transport or not all(isinstance(x, str) and x and '\n' not in x and '<' not in x for x in transport):
        raise ValueError('A supported authenticated exec argv is required')
    limits = dict(interval=1, compact_seconds=1, end_margin=1, generations_keep=2,
                  full_families_keep=2, max_incremental_ratio=0, home_budget_gb=1)
    for key, value in profile.get('snapshot', {}).items():
        if key not in limits or type(value) is not int or value < limits[key]:
            raise ValueError('Invalid snapshot policy: ' + key)
    return profile


def replace_tokens(body, name, adapter):
    return body.replace('@SITE@', name).replace('@PREFIX@', name.upper().replace('-', '_')).replace('@ADAPTER@', adapter)


def render(profile):
    validate(profile)
    name = profile['name']; prefix = name.upper().replace('-', '_')
    flavor = 'psc' if profile['adapter'] == 'psc-bridge' else 'msi'
    files = {}
    for source, suffix in [('local-snapshot.sh', 'local-snapshot'), ('task-runner.sh', 'gpu-inner-run'),
                           ('agent-state.py', 'agent-state'), ('allocation.py', 'allocation'), ('health.py', 'health')]:
        body = (ROOT / 'common' / source).read_text(encoding='utf-8')
        if source == 'local-snapshot.sh':
            body = body.replace('@GENERATION_ENGINE@', (ROOT / 'common/snapshot-generation.sh').read_text(encoding='utf-8'))
        files['bin/' + name + '-' + suffix] = replace_tokens(body, name, flavor)
    if flavor == 'msi':
        gpu = (ROOT / 'common/slurm-gpu.sh').read_text(encoding='utf-8')
        boot = (ROOT / 'common/slurm-boot.sh').read_text(encoding='utf-8')
    else:
        gpu = (ROOT / 'psc-remote-install/psc-gpu.sh').read_text(encoding='utf-8')
        default = profile['allocation']['default_gpu']
        gpu = gpu.replace('local gpu_type=h100 gpu_gres=h100-80 gpu_partition=GPU-shared gpu_pattern=H100 gpu_qos=""',
                          'local gpu_type=' + shlex.quote(default) + ' gpu_gres="" gpu_partition="" gpu_pattern="" gpu_qos="" max_gpu=1')
        start = gpu.index('    case "$gpu_type" in'); end = gpu.index('    export PSC_GPU_EXPECTED_GPU_NAME_PATTERN', start)
        cases = ['    case "$gpu_type" in']
        for key, data in profile['allocation']['gpus'].items():
            cases.append('        %s) gpu_gres=%s; gpu_partition=%s; gpu_qos=%s; gpu_pattern=%s; max_gpu=%s ;;' %
                (key, shlex.quote(data['gres']), shlex.quote(data['partition']), shlex.quote(data.get('qos', '')),
                 shlex.quote(data.get('name_pattern', key.upper())), data['max_count']))
        cases += ['        *) die "GPU type absent from verified profile" ;;', '    esac', '    [[ "${1:-1}" -le "$max_gpu" ]] || die "GPU count exceeds site profile"']
        gpu = gpu[:start] + '\n'.join(cases) + '\n' + gpu[end:]
        gpu = gpu.replace('local gpu_count="${1:-2}"', 'local gpu_count="${1:-1}"')
        gpu = gpu.replace('[[ "$gpu_type" != a100 || "$gpu_count" == 1 ]] || die "GPU-dev A100 requires one GPU"', ': # Partition-specific count limits come from the verified profile.')
        gpu = gpu.replace('local walltime="${2:-08:00:00}"', 'local walltime="${2:-' + profile['allocation']['walltime'] + '}"')
        boot = (ROOT / 'common/sites/psc-boot.sh').read_text(encoding='utf-8')
        for old, new in (('$HOME/.psc-local-env.sh', '$HOME/.config/psc-gpu/local-env.sh'),
                         ('$HOME/.tmux.inner.conf', '$HOME/.config/psc-gpu/tmux.compute.conf')):
            boot = boot.replace(old, new)
        gpu = gpu.replace('$HOME/.tmux.conf', '$HOME/.config/psc-gpu/tmux.login.conf')
        gpu = re.sub(r'\bpsc\b', name, gpu).replace('PSC', prefix)
        boot = re.sub(r'\bpsc\b', name, boot).replace('PSC', prefix)
    files['bin/' + name + '-gpu'] = replace_tokens(gpu, name, flavor)
    boot = boot.replace('@BOOT_GUARD@', (ROOT / 'common/boot-guard.sh').read_text(encoding='utf-8'))
    files['bin/' + name + '-gpu-boot'] = replace_tokens(boot, name, flavor)
    values = {'HPC_PROFILE_HASH': hashlib.sha256(json.dumps(profile, sort_keys=True).encode()).hexdigest(),
        'HPC_ACCOUNT': profile['allocation']['account'], 'HPC_CPUS': str(profile['allocation']['cpus']),
        'HPC_MEMORY': profile['allocation']['memory'], 'HPC_WALLTIME': profile['allocation']['walltime'],
        'HPC_DEFAULT_GPU': profile['allocation']['default_gpu'],
        'HPC_LOCAL_TEMPLATE': profile['storage']['local_template'], 'HPC_LOCAL_PREFIX': profile['storage']['local_prefix'],
        'HPC_ARCHIVE': profile['storage']['archive'], 'HPC_RESULTS': profile['storage']['results'],
        'HPC_LOCAL_SCRATCH_REQUEST': profile['allocation'].get('local_scratch', ''),
        'HPC_OUTER_SOCKET': name + '-login', 'HPC_OUTER_SESSION': name + '-login',
        prefix + '_GPU_AUTOSAVE_INTERVAL': '300'}
    policy = profile.get('snapshot', {})
    for key, suffix in dict(interval='GPU_AUTOSAVE_INTERVAL', compact_seconds='LOCAL_SNAPSHOT_COMPACT_SECONDS',
                            end_margin='LOCAL_SNAPSHOT_END_MARGIN', generations_keep='LOCAL_SNAPSHOT_GENERATIONS_KEEP',
                            full_families_keep='LOCAL_SNAPSHOT_FULL_FAMILIES_KEEP',
                            max_incremental_ratio='LOCAL_SNAPSHOT_MAX_INCREMENTAL_RATIO',
                            home_budget_gb='LOCAL_SNAPSHOT_HOME_BUDGET_GB').items():
        if key in policy: values[prefix + '_' + suffix] = str(policy[key])
    if flavor == 'psc':
        values.update({prefix + '_ACCOUNT': profile['allocation']['account'], prefix + '_CPUS_PER_TASK': str(profile['allocation']['cpus']),
                       prefix + '_MEMORY': profile['allocation']['memory'], prefix + '_TOOLCHAIN_DISABLED': '1',
                       prefix + '_BOOT_DOCTOR_DISABLED': '1', prefix + '_GPU_MIRROR_DISABLED': '1'})
        files['config/local-env.sh'] = '''# Generated cache and local-storage setup; no HOME symlink mutation.
expand_path() { python3 -c 'import os,sys; p=os.path.expandvars(sys.argv[1]); assert "$" not in p and os.path.isabs(p); print(p)' "$1"; }
export LOCAL="$(expand_path "$HPC_LOCAL_TEMPLATE")"
export HPC_ALLOWED_LOCAL_PREFIX="$(expand_path "$HPC_LOCAL_PREFIX")"
export ''' + prefix + '''_LOCAL_SNAPSHOT_ARCHIVE="$(expand_path "$HPC_ARCHIVE")"
mkdir -p "$LOCAL/work/$USER" "$LOCAL/cache/$USER/uv" "$LOCAL/tmp/$USER"
export UV_CACHE_DIR="$LOCAL/cache/$USER/uv" TMPDIR="$LOCAL/tmp/$USER" UV_LINK_MODE=hardlink
'''
    config = ['# Generated from a reviewed profile. No passwords or tokens belong here.']
    config += [key + '=' + shlex.quote(value) for key, value in sorted(values.items())]
    for field, array in [('gres', 'HPC_GPU_GRES'), ('partition', 'HPC_GPU_PARTITION'), ('qos', 'HPC_GPU_QOS'), ('max_count', 'HPC_GPU_MAX_COUNT')]:
        config.append('declare -A ' + array + '=(' + ' '.join('[' + key + ']=' + shlex.quote(str(data.get(field, ''))) for key, data in profile['allocation']['gpus'].items()) + ')')
    files['config/gpu.env'] = '\n'.join(config) + '\n'
    files['config/tmux.compute.conf'] = 'set -g prefix C-a\nunbind C-b\nbind C-a send-prefix\nset -g history-limit 50000\n'
    files['config/tmux.login.conf'] = 'set -g prefix C-b\nset -g history-limit 50000\n'
    files['profile.json'] = json.dumps(profile, indent=2, sort_keys=True) + '\n'
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('profile'); parser.add_argument('--output', required=True)
    args = parser.parse_args()
    profile = json.loads(Path(args.profile).read_text(encoding='utf-8-sig'))
    files = render(profile)
    root = Path(args.output)
    if root.exists() and any(root.iterdir()):
        parser.error('Output must be a new or empty staging directory')
    for relative, body in files.items():
        path = root / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(body, encoding='utf-8', newline='\n')
    manifest = dict(schema_version=1, core_version='0.4.0', site=profile['name'],
                    files={key: hashlib.sha256(body.encode()).hexdigest() for key, body in files.items()})
    (root / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps(dict(site=profile['name'], bundle=str(root.resolve()), file_count=len(files))))


if __name__ == '__main__':
    main()

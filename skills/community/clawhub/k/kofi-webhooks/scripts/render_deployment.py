"""Render Linux deployment files locally; does not install or contact a server."""
import argparse
import json
from pathlib import Path, PurePosixPath
import re


def render(output, name='kofi-webhooks', port=8787, app_dir=None,
           config_dir=None, python='/usr/bin/python3'):
    if not re.fullmatch(r'[a-z][a-z0-9-]{0,62}', name):
        raise ValueError('Service name must be lowercase letters, digits, and hyphens')
    if not 1 <= port <= 65535:
        raise ValueError('Port must be between 1 and 65535')
    values = {'SERVICE_NAME': name, 'PORT': str(port),
              'APP_DIR': app_dir or '/opt/' + name,
              'CONFIG_DIR': config_dir or '/etc/' + name,
              'STATE_DIR': '/var/lib/' + name, 'PYTHON': python}
    for key in ('APP_DIR', 'CONFIG_DIR', 'PYTHON'):
        value = values[key]
        if (not re.fullmatch(r'/[A-Za-z0-9_./-]+', value)
                or '..' in PurePosixPath(value).parts
                or str(PurePosixPath(value)) != value or value == '/'):
            raise ValueError(key + ' must be a normalized absolute Linux path without spaces or specifiers')
    assets = Path(__file__).resolve().parent.parent / 'assets'
    files = {}
    for template, filename in (
        ('kofi-webhooks.service.tmpl', name + '.service'),
        ('testing.conf.tmpl', 'testing.conf'),
        ('nginx-location.conf.tmpl', 'nginx-location.conf'),
    ):
        source = (assets / template).read_text(encoding='utf-8')
        source = re.sub(r'@@([A-Z_]+)@@', lambda match: values[match[1]], source)
        if '@@' in source:
            raise ValueError('Unresolved template parameter')
        files[filename] = source
    config = {'service': name + '.service', 'port': port,
              'app_dir': values['APP_DIR'], 'config_dir': values['CONFIG_DIR'],
              'state_dir': values['STATE_DIR'], 'python': python}
    files['deployment.json'] = json.dumps(config, indent=2) + '\n'
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    for filename, content in files.items():
        (output / filename).write_text(content, encoding='utf-8', newline='\n')
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='New directory; existing paths are never overwritten')
    parser.add_argument('--name', default='kofi-webhooks')
    parser.add_argument('--port', type=int, default=8787)
    parser.add_argument('--app-dir')
    parser.add_argument('--config-dir')
    parser.add_argument('--python', default='/usr/bin/python3')
    args = parser.parse_args()
    try:
        config = render(args.output, args.name, args.port, args.app_dir, args.config_dir, args.python)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, 'Rendering failed: ' + str(exc) + '\n')
    print(json.dumps(config, indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from revision_utils import base_state, load_state, save_state


def parse_value(raw):
    low = raw.lower()
    if low == 'true':
        return True
    if low == 'false':
        return False
    if low == 'null':
        return None
    return raw


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('project')
    parser.add_argument('field')
    parser.add_argument('value')
    parser.add_argument('--json', action='store_true', dest='json_mode')
    return parser.parse_args()


def main():
    args = parse_args()
    project = Path(args.project).expanduser()
    state_file = project / '.novel-state.json'
    field = args.field
    value = json.loads(args.value) if args.json_mode else parse_value(args.value)

    data = load_state(project) if state_file.exists() else base_state(project)

    if '.' not in field:
        print('Field must be section.key format')
        sys.exit(2)

    section, key = field.split('.', 1)
    if section not in data:
        data[section] = {}

    if isinstance(data[section], dict):
        data[section][key] = value
    else:
        print(f'Section {section} is not a dict')
        sys.exit(2)

    save_state(project, data)
    print(json.dumps(load_state(project), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

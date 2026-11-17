"""PopNow media API commands. Standard library only; no file downloads or telemetry."""
import argparse
import json
import os
import sys
from client import PopNowClient, PopNowError


def parser():
    result = argparse.ArgumentParser(description='PopNow media API with exact USD quote approval')
    commands = result.add_subparsers(dest='operation', required=True)
    models = commands.add_parser('models', help='Find models and their exact input schemas')
    models.add_argument('--search')
    models.add_argument('--modality')
    commands.add_parser('balance', help='Read API USD balance; website credits are separate')
    for name in ('quote', 'create'):
        command = commands.add_parser(name, help='Quote without spending' if name == 'quote' else 'Create one explicitly approved task')
        command.add_argument('--model', required=True)
        command.add_argument('--input-json', required=True, help='JSON object matching the chosen model schema')
        if name == 'create':
            command.add_argument('--quote-id', required=True)
            command.add_argument('--approved-max-usd', required=True, help='Approved maxChargeUsd as an exact decimal string')
            command.add_argument('--idempotency-key', required=True, help='Stable key for this approved task; reuse on retries')
    status = commands.add_parser('status', help='Read an existing task and output URLs')
    status.add_argument('--task-id', required=True)
    return result


def main(argv=None):
    args = vars(parser().parse_args(argv))
    operation = args.pop('operation')
    try:
        data = PopNowClient(os.environ.get('POPNOW_API_KEY')).invoke(operation, args)
        print(json.dumps({'data': data}, ensure_ascii=False, allow_nan=False))
        return 0
    except PopNowError as error:
        print(json.dumps({'error': str(error)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

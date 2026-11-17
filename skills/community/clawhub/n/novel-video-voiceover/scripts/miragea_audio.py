#!/usr/bin/env python3
"""Miragea audio task client; Python 3.9+, standard library only."""
import argparse
import json
import mimetypes
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

SKILL_VERSION = '1.1.0'


class ClientError(Exception):
    def __init__(self, payload):
        self.payload = payload


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Client:
    def __init__(self, timeout=30):
        self.base = os.environ.get('MIRAGEA_BASE_URL', 'https://miragea.ai/v1').rstrip('/')
        self.key = os.environ.get('MIRAGEA_API_KEY', '')
        if not self.key:
            raise ClientError({'error': {'code': 'missing_api_key', 'message': 'Set MIRAGEA_API_KEY.'}})
        parsed = urllib.parse.urlsplit(self.base)
        if parsed.scheme not in ('http', 'https') or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ClientError({'error': {'code': 'invalid_base_url', 'message': 'Use an HTTP(S) API root without credentials, query or fragment.'}})
        self.timeout = timeout
        self.opener = urllib.request.build_opener(NoRedirect())

    def request(self, method, path, payload=None, content_type=None, key=None, timeout=None):
        headers = {'Authorization': 'Bearer ' + self.key, 'Accept': 'application/json'}
        if content_type:
            headers['Content-Type'] = content_type
        if key:
            headers['Idempotency-Key'] = key
        request = urllib.request.Request(self.base + path, data=payload, headers=headers, method=method)
        try:
            with self.opener.open(request, timeout=timeout or self.timeout) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            try:
                result = json.load(exc)
            except (ValueError, UnicodeError):
                result = {'error': {'code': 'http_error', 'message': 'API returned HTTP ' + str(exc.code)}}
            raise ClientError({'http_status': exc.code, **result}) from None
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            raise ClientError({'error': {'code': 'request_failed', 'message': 'API request failed; submission outcome may be unknown. Reuse the same idempotency key for the same payload.'}}) from None

    def task(self, task_id, timeout=None):
        return self.request('GET', '/tasks/' + urllib.parse.quote(task_id, safe=''), timeout=timeout)

    def capabilities(self):
        result = self.request('GET', '/capabilities')
        latest = result.get('skill_version')
        if isinstance(latest, str):
            try:
                newer = tuple(map(int, latest.split('.'))) > tuple(map(int, SKILL_VERSION.split('.')))
            except ValueError:
                newer = False
            if newer:
                print(json.dumps({
                    'skill_update_available': {'installed': SKILL_VERSION, 'latest': latest,
                                               'package_url': result.get('skill_url')},
                }), file=sys.stderr)
        return result

    def wait(self, task_id, deadline_seconds):
        deadline = time.monotonic() + deadline_seconds
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ClientError({'task_id': task_id, 'error': {'code': 'wait_timeout', 'message': 'Task is still pending. Resume with task or wait; do not submit a new task.'}})
            try:
                task = self.task(task_id, timeout=min(self.timeout, remaining))
            except ClientError as exc:
                if time.monotonic() >= deadline:
                    raise ClientError({'task_id': task_id, 'error': {'code': 'wait_timeout', 'message': 'Polling deadline reached. Resume with task or wait; do not submit a new task.'}}) from None
                exc.payload['task_id'] = task_id
                raise
            if task.get('status') in ('succeeded', 'failed'):
                return task
            pause = task.get('poll_after_seconds', 3)
            pause = pause if isinstance(pause, (int, float)) and pause > 0 else 3
            time.sleep(min(pause, max(0, deadline - time.monotonic())))


def multipart(file_path, expected_rate):
    boundary = 'miragea-' + uuid.uuid4().hex
    filename = file_path.name.replace('"', '_').replace('\r', '_').replace('\n', '_')
    mime = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    prefix = (f'--{boundary}\r\nContent-Disposition: form-data; name="expected_rate"\r\n\r\n{expected_rate}\r\n'
              f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\n'
              f'Content-Type: {mime}\r\n\r\n').encode('utf-8')
    return prefix + file_path.read_bytes() + f'\r\n--{boundary}--\r\n'.encode(), 'multipart/form-data; boundary=' + boundary


def save_result(task, output, subtitle_format):
    if task.get('status') != 'succeeded':
        raise ClientError({'task_id': task.get('task_id'), 'error': {'code': 'result_not_ready', 'message': 'Output requires a succeeded task; use --wait.'}})
    result = task.get('result') or {}
    path = Path(output).expanduser()
    # Exclusive creation protects existing user files. Remove partial downloads on failure.
    created = False
    try:
        with path.open('xb') as target:
            created = True
            if task.get('kind') == 'audio_generation':
                url = result.get('audio_url', '')
                if urllib.parse.urlsplit(url).scheme not in ('https', 'http'):
                    raise ValueError('Invalid audio download URL.')
                with urllib.request.urlopen(url, timeout=60) as source:
                    while True:
                        chunk = source.read(1024 * 1024)
                        if not chunk:
                            break
                        target.write(chunk)
            else:
                value = result if subtitle_format == 'json' else result.get(subtitle_format, '')
                text = json.dumps(value, ensure_ascii=False, indent=2) if subtitle_format == 'json' else value
                target.write(text.encode('utf-8'))
    except Exception:
        if created:
            path.unlink(missing_ok=True)
        raise
    task['saved_to'] = str(path)


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--version', action='version', version=SKILL_VERSION)
    p.add_argument('--timeout', type=float, default=30, help='HTTP timeout in seconds')
    commands = p.add_subparsers(dest='command', required=True)
    commands.add_parser('capabilities')
    actors = commands.add_parser('actors')
    actors.add_argument('--limit', type=int, default=20)
    actors.add_argument('--offset', type=int, default=0)
    generate = commands.add_parser('generate')
    source = generate.add_mutually_exclusive_group(required=True)
    source.add_argument('--text')
    source.add_argument('--text-file', type=Path, help='UTF-8 text file')
    voice = generate.add_mutually_exclusive_group(required=True)
    voice.add_argument('--reference-audio-url')
    voice.add_argument('--actor-id')
    generate.add_argument('--reference-text')
    generate.add_argument('--model', choices=('expressive', 'standard'), help='Generation mode; omit to use the current default')
    generate.add_argument('--format', choices=('mp3', 'wav', 'flac', 'opus', 'aac', 'pcm'))
    generate.add_argument('--speed', type=float)
    generate.add_argument('--tag', action='append', dest='tags')
    generate.add_argument('--language')
    recognize = commands.add_parser('recognize')
    recognize.add_argument('--file', type=Path, required=True)
    recognize.add_argument('--expected-rate', type=float, help='Accepted points/second; omit to fetch current capabilities rate')
    task = commands.add_parser('task')
    task.add_argument('task_id')
    wait = commands.add_parser('wait')
    wait.add_argument('task_id')
    for command in (generate, recognize):
        command.add_argument('--idempotency-key', help='Reuse with identical input after uncertain submission')
        command.add_argument('--wait', action='store_true')
    for command in (generate, recognize, wait):
        command.add_argument('--wait-timeout', type=float, default=600)
    for command in (generate, recognize, task, wait):
        command.add_argument('--output', help='Save result to a new file; never overwrite')
        command.add_argument('--subtitle-format', choices=('srt', 'txt', 'json'), default='srt')
    return p


def main():
    args = parser().parse_args()
    try:
        if args.timeout <= 0 or getattr(args, 'wait_timeout', 1) <= 0:
            raise ValueError('Timeouts must be positive.')
        client = Client(args.timeout)
        submission_key = None
        if args.command == 'capabilities':
            result = client.capabilities()
        elif args.command == 'actors':
            if not 1 <= args.limit <= 100 or args.offset < 0:
                raise ValueError('Use a limit between 1 and 100 and a nonnegative offset.')
            query = urllib.parse.urlencode({'limit': args.limit, 'offset': args.offset})
            result = client.request('GET', '/actors?' + query)
        elif args.command in ('task', 'wait'):
            result = client.wait(args.task_id, args.wait_timeout) if args.command == 'wait' else client.task(args.task_id)
        else:
            submission_key = args.idempotency_key or str(uuid.uuid4())
            # Persist this line in the caller's tool transcript before a possibly uncertain POST.
            print(json.dumps({'idempotency_key': submission_key}, ensure_ascii=False), file=sys.stderr, flush=True)
            if args.command == 'generate':
                if args.actor_id is not None and args.reference_text is not None:
                    raise ValueError('--reference-text requires --reference-audio-url.')
                payload = {'text': args.text if args.text is not None else args.text_file.read_text(encoding='utf-8')}
                for field in ('actor_id', 'reference_audio_url', 'reference_text', 'model', 'format', 'speed', 'tags', 'language'):
                    value = getattr(args, field)
                    if value is not None:
                        payload[field] = value
                result = client.request('POST', '/audio/generations', json.dumps(payload).encode(), 'application/json', submission_key)
            else:
                capabilities = client.capabilities()
                rate = args.expected_rate if args.expected_rate is not None else capabilities['subtitles']['points_per_second']
                if args.file.stat().st_size > capabilities['subtitles']['max_upload_mb'] * 1024 * 1024:
                    raise ValueError('File exceeds capabilities.subtitles.max_upload_mb.')
                body, content_type = multipart(args.file, rate)
                result = client.request('POST', '/subtitles/recognitions', body, content_type, submission_key)
            if args.wait and result.get('status') not in ('succeeded', 'failed'):
                result = client.wait(result['task_id'], args.wait_timeout)
            result['idempotency_key'] = submission_key
        if getattr(args, 'output', None) and result.get('status') != 'failed':
            save_result(result, args.output, args.subtitle_format)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get('status') == 'failed' else 0
    except ClientError as exc:
        if locals().get('submission_key'):
            exc.payload['idempotency_key'] = submission_key
        print(json.dumps(exc.payload, ensure_ascii=False, indent=2))
        return 2
    except (OSError, ValueError, KeyError, TypeError) as exc:
        payload = {'error': {'code': 'client_error', 'message': str(exc)}}
        if locals().get('result', {}).get('task_id'):
            payload['task_id'] = result['task_id']
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""贵数 Images API：生成、参考图编辑，以及不重复生成的结果恢复。"""
import argparse
import base64
import binascii
import contextlib
import datetime as dt
import hashlib
import html
import http.client
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import uuid


VERSION = '1.1.0'
DEFAULT_ENDPOINT = 'https://api.llm-token.cn/v1/images/generations'
DEFAULT_MODEL = 'gpt-image-2'
KEY_ENV_NAMES = ('LLM_TOKEN_API_KEY', 'GUI_SHU_TOKEN_KEY')
GUI_SHU_HOSTS = {'api.llm-token.cn', 'gpt-agent.cc', 'hk.gpt-agent.cc', 'eu.gpt-agent.cc', 'img.llm-token.cn'}
EXTENDED_MODELS = {'gpt-image-2.5-flare', 'gpt-image-2.5-sunburst'}
MAX_IMAGE_BYTES = 50 * 1024 * 1024
MAX_INPUT_BYTES = 200 * 1024 * 1024
MAX_RESPONSE_BYTES = 256 * 1024 * 1024


class SkillError(Exception):
    def __init__(self, message, request_id=None):
        super().__init__(message)
        self.request_id = request_id


def safe_id(value, secret=''):
    if isinstance(value, str) and secret and secret in value:
        return None
    if isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_.:-]{1,128}', value) and not value.startswith('sk-'):
        return value
    return None


def https_url(value):
    if not isinstance(value, str):
        raise SkillError('URL 必须是字符串')
    try:
        parsed = urllib.parse.urlsplit(value)
        port = parsed.port
    except ValueError:
        raise SkillError('URL 格式无效') from None
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username is not None
            or parsed.password is not None or parsed.fragment or any(c.isspace() for c in value)):
        raise SkillError('只接受不含用户名、密码、片段或空白的 HTTPS URL')
    return parsed, port


def public_image_url(value):
    parsed, port = https_url(value)
    try:
        addresses = socket.getaddrinfo(parsed.hostname, port or 443, type=socket.SOCK_STREAM)
        if not addresses or any(not ipaddress.ip_address(item[4][0]).is_global for item in addresses):
            raise SkillError('图片 URL 必须指向公开网络地址')
    except (OSError, ValueError):
        raise SkillError('无法解析图片下载地址；可稍后仅恢复下载') from None
    return value


class NoPostRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # 凭据和非幂等 POST 不跨重定向传递。
        return None


class ImageRedirect(urllib.request.HTTPRedirectHandler):
    max_redirections = 5

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        public_image_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def bounded_read(response, limit):
    chunks = []
    size = 0
    length = getattr(response, 'headers', {}).get('Content-Length')
    if length is not None and (not length.isdigit() or int(length) > limit):
        raise SkillError('响应长度无效或超过本地安全大小限制')
    while True:
        chunk = response.read(min(1024 * 1024, limit + 1 - size))
        if not chunk:
            if length is not None and size != int(length):
                raise SkillError('响应内容未接收完整；已停止保存')
            return b''.join(chunks)
        chunks.append(chunk)
        size += len(chunk)
        if size > limit:
            raise SkillError('响应超过本地安全大小限制，已停止读取')


def image_format(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) >= 33 and data[12:16] == b'IHDR':
        return 'png'
    if data.startswith(b'\xff\xd8\xff'):
        return 'jpeg'
    if len(data) >= 12 and data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return 'webp'
    raise SkillError('文件不是支持的 PNG、JPEG 或 WebP 图片，未保存为图片')


def read_input(path):
    path = Path(path).expanduser()
    if not path.is_file() or path.stat().st_size > MAX_IMAGE_BYTES:
        raise SkillError('输入图片必须是存在且不超过 50 MiB 的本地文件')
    with path.open('rb') as stream:
        data = bounded_read(stream, MAX_IMAGE_BYTES)
    return data, image_format(data)


def read_prompts(args):
    prompts = [args.prompt.strip()] if args.prompt and args.prompt.strip() else []
    if args.prompt_file:
        path = Path(args.prompt_file).expanduser()
        if path.stat().st_size > 1024 * 1024:
            raise SkillError('提示词文件不能超过 1 MiB')
        prompts.extend(line.strip() for line in path.read_text(encoding='utf-8-sig').splitlines()
                       if line.strip() and not line.lstrip().startswith('#'))
    if not prompts:
        raise SkillError('必须提供非空 --prompt 或 --prompt-file；不会自动生成测试图片')
    if len(prompts) > 1000:
        raise SkillError('一次最多处理 1000 条提示词，请拆分批次')
    return prompts


def resolve_api_key(args):
    if args.api_key:
        key = args.api_key.strip()
    elif args.key_env:
        key = os.environ.get(args.key_env, '').strip()
    else:
        key = next((os.environ[name].strip() for name in KEY_ENV_NAMES if os.environ.get(name, '').strip()), '')
    if not key:
        raise SkillError('缺少 API Key：设置 LLM_TOKEN_API_KEY；使用其他变量须显式指定 --key-env')
    if any(c.isspace() for c in key):
        raise SkillError('API Key 不能包含空白字符')
    parsed, port = https_url(args.endpoint)
    if (parsed.hostname not in GUI_SHU_HOSTS or port not in (None, 443)) and not (args.key_env or args.api_key):
        raise SkillError('自定义服务地址必须显式指定 --key-env，避免将贵数密钥发送给其他服务')
    return key


def prepare(args):
    prompts = read_prompts(args)
    if not 1 <= args.n <= 10:
        raise SkillError('--n 必须在 1–10 之间')
    if not args.model.strip() or any(c.isspace() for c in args.model):
        raise SkillError('--model 必须是完整且不含空白的模型 ID')
    if args.size != 'auto':
        match = re.fullmatch(r'(\d{1,4})[xX×](\d{1,4})', args.size)
        if not match or any(not 64 <= int(value) <= 4096 for value in match.groups()):
            raise SkillError('--size 使用 auto 或 宽x高，每边 64–4096；具体支持范围由模型决定')
        args.size = 'x'.join(str(int(value)) for value in match.groups())
    if args.quality in ('xhigh', 'max') and args.model not in EXTENDED_MODELS:
        raise SkillError('xhigh/max 仅用于明确的 gpt-image-2.5-flare 或 gpt-image-2.5-sunburst')
    if args.background == 'transparent' and args.output_format == 'jpeg':
        raise SkillError('透明背景不能使用 JPEG；请选 PNG 或 WebP')
    if args.output_compression is not None:
        if not 0 <= args.output_compression <= 100 or args.output_format not in ('jpeg', 'webp'):
            raise SkillError('--output-compression 仅用于 JPEG/WebP，范围 0–100')
    if args.mask and not args.image:
        raise SkillError('--mask 必须同时提供 --image')
    if len(args.image) > 16:
        raise SkillError('本脚本一次最多接受 16 张参考图')
    images = [read_input(path) for path in args.image]
    mask = read_input(args.mask) if args.mask else None
    if mask:
        if mask[1] != 'png' or images[0][1] != 'png':
            raise SkillError('带蒙版编辑需要 PNG 主图和 PNG 蒙版，请先转换文件')
        if mask[0][16:24] != images[0][0][16:24]:
            raise SkillError('蒙版尺寸必须与第一张参考图一致')
        if mask[0][25] not in (4, 6):
            raise SkillError('蒙版必须是带 Alpha 通道的 PNG；透明区域表示需要修改的位置')
    if sum(len(item[0]) for item in images) + (len(mask[0]) if mask else 0) > MAX_INPUT_BYTES:
        raise SkillError('本脚本输入图片总量不能超过 200 MiB')
    endpoint = args.endpoint or DEFAULT_ENDPOINT
    parsed, _ = https_url(endpoint)
    if parsed.query:
        raise SkillError('API endpoint 不应包含查询参数；密钥通过 Authorization 发送')
    if images and endpoint.endswith('/images/generations'):
        endpoint = endpoint[:-len('generations')] + 'edits'
    if endpoint.endswith('/images/edits') and not images:
        raise SkillError('编辑接口必须提供 --image')
    args.endpoint = endpoint
    body = {'model': args.model, 'size': args.size, 'n': args.n, 'response_format': args.response_format}
    # 贵数现有 2.5 路由通过省略 quality 表示 auto，而不是发送字面量 auto。
    if not (args.model in EXTENDED_MODELS and args.quality == 'auto' and parsed.hostname in GUI_SHU_HOSTS):
        body['quality'] = args.quality
    for field in ('background', 'output_format', 'output_compression'):
        value = getattr(args, field)
        if value is not None and value != '':
            body[field] = value
    return prompts, body, images, mask


def request_bytes(body, images, mask, image_field):
    if not images:
        return json.dumps(body, ensure_ascii=False).encode('utf-8'), 'application/json'
    boundary = 'guishu-' + uuid.uuid4().hex
    parts = []
    for key, value in body.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode('utf-8'))
    files = [(image_field, data, fmt, f'input-{idx}.{fmt}') for idx, (data, fmt) in enumerate(images, 1)]
    if mask:
        files.append(('mask', mask[0], 'png', 'mask.png'))
    for field, data, fmt, name in files:
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{field}"; filename="{name}"\r\nContent-Type: image/{fmt}\r\n\r\n'.encode('ascii'))
        parts.extend((data, b'\r\n'))
    parts.append(f'--{boundary}--\r\n'.encode('ascii'))
    return b''.join(parts), f'multipart/form-data; boundary={boundary}'


def post_image(args, key, body, images, mask):
    data, content_type = request_bytes(body, images, mask, args.image_field)
    request = urllib.request.Request(args.endpoint, data=data, method='POST', headers={
        'Authorization': f'Bearer {key}', 'Content-Type': content_type, 'Accept': 'application/json',
    })
    request_id = None
    try:
        with urllib.request.build_opener(NoPostRedirect()).open(request, timeout=args.timeout) as response:
            request_id = safe_id(response.headers.get('x-request-id') or response.headers.get('request-id'), key)
            result = json.loads(bounded_read(response, MAX_RESPONSE_BYTES))
        if not isinstance(result, dict):
            raise SkillError('生成响应不是 JSON 对象；不要自动重发', request_id)
        return result, request_id
    except urllib.error.HTTPError as exc:
        request_id = safe_id(exc.headers.get('x-request-id') or exc.headers.get('request-id'), key)
        exc.close()
        hints = {400: '检查模型和参数', 401: '检查贵数 Key', 403: '检查账号权限或服务限制',
                 429: '额度或速率限制，请核对用量', 502: '上游异常', 504: '等待上游超时'}
        raise SkillError(f'HTTP {exc.code}：{hints.get(exc.code, "服务未返回成功结果")}；未自动重试', request_id) from None
    except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException):
        raise SkillError('请求连接中断或超时，生成结果未知；请先核对用量，不要自动重发', request_id) from None
    except (ValueError, UnicodeError, RecursionError):
        raise SkillError('响应不是有效 JSON，生成结果未知；不要自动重发', request_id) from None
    except SkillError as exc:
        exc.request_id = request_id
        raise


def minimal_response(result, save_prompts):
    data = result.get('data') if isinstance(result, dict) else None
    if not isinstance(data, list) or not data or len(data) > 10:
        raise SkillError('响应没有同步图片结果或数量异常；本脚本不猜测异步任务接口，请核对用量')
    items = []
    for item in data:
        if not isinstance(item, dict):
            items.append({'invalid_result': True})
            continue
        clean = {key: item[key] for key in ('b64_json', 'url') if isinstance(item.get(key), str) and item[key]}
        if not clean:
            items.append({'invalid_result': True})
            continue
        if save_prompts and isinstance(item.get('revised_prompt'), str):
            clean['revised_prompt'] = item['revised_prompt']
        items.append(clean)
    return {'data': items}


def download_item(item, timeout):
    if item.get('b64_json'):
        try:
            if len(item['b64_json']) > (MAX_IMAGE_BYTES + 2) // 3 * 4:
                raise SkillError('图片超过 50 MiB 本地限制')
            data = base64.b64decode(item['b64_json'], validate=True)
            if len(data) > MAX_IMAGE_BYTES:
                raise SkillError('图片超过 50 MiB 本地限制')
        except (binascii.Error, ValueError):
            raise SkillError('图片 Base64 无效；已保留响应，未重新生成') from None
    else:
        url = public_image_url(item.get('url', ''))
        try:
            # 下载不带 API Key，也不继承生成请求的 Authorization。
            with urllib.request.build_opener(ImageRedirect()).open(url, timeout=timeout) as response:
                data = bounded_read(response, MAX_IMAGE_BYTES)
        except urllib.error.HTTPError as exc:
            exc.close()
            raise SkillError(f'原图下载返回 HTTP {exc.code}；可仅恢复下载，不要重新生成') from None
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException):
            raise SkillError('原图下载连接中断或超时；可仅恢复下载，不要重新生成') from None
    fmt = image_format(data)
    if ((fmt == 'png' and not data.endswith(b'\x00\x00\x00\x00IEND\xaeB`\x82'))
            or (fmt == 'jpeg' and not data.endswith(b'\xff\xd9'))
            or (fmt == 'webp' and int.from_bytes(data[4:8], 'little') + 8 != len(data))):
        raise SkillError('图片文件不完整；已保留原响应，请只恢复下载')
    return data, fmt


def atomic_write(path, data):
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.writing-', delete=False) as stream:
        temp = Path(stream.name)
        try:
            os.chmod(temp, 0o600)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
            stream.close()
            os.replace(temp, path)
        finally:
            temp.unlink(missing_ok=True)


def write_json(path, value):
    atomic_write(path, json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8'))


def write_gallery(out_dir, state):
    figures = []
    for job in state['jobs']:
        for item in job['files']:
            filename = html.escape(item['file'], quote=True)
            caption = html.escape(job.get('prompt', item['file']), quote=True)
            figures.append(f'<figure><a href="{filename}"><img src="{filename}" loading="lazy"></a><figcaption>{caption}</figcaption></figure>')
    document = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' data:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>贵数图片结果</title><style>
body{margin:24px;font:16px/1.6 system-ui;background:#f7f8fa;color:#18212f}
main{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}
figure{margin:0;padding:16px;background:white;border-radius:12px}img{width:100%;height:auto}
figcaption{overflow-wrap:anywhere;margin-top:8px}</style><h1>贵数图片结果</h1>
<p>已保存到本地的图片；每项处理状态见 state.json。</p><main>'''
    atomic_write(out_dir / 'index.html', (document + '\n'.join(figures) + '</main></html>').encode('utf-8'))


def checkpoint(out_dir, state, gallery=True):
    write_json(out_dir / 'state.json', state)
    write_json(out_dir / 'request.json', [{'request': job['request'], 'status': job['status'],
                                         'request_id': job.get('request_id'), 'images': len(job['files'])}
                                        for job in state['jobs']])
    if state['save_prompts']:
        write_json(out_dir / 'prompts.json', [{'prompt': job['prompt'], 'file': item['file']}
                                            for job in state['jobs'] for item in job['files']])
    if gallery:
        write_gallery(out_dir, state)


@contextlib.contextmanager
def directory_lock(out_dir):
    path = out_dir / '.lock'
    if path.is_symlink():
        raise SkillError('输出目录锁不能是符号链接')
    with path.open('a+b') as stream:
        try:
            if os.name == 'nt':
                import msvcrt
                stream.seek(0, os.SEEK_END)
                if stream.tell() == 0:
                    stream.write(b'0')
                    stream.flush()
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise SkillError('此输出目录正被另一进程使用；请等待原进程完成') from None
        yield


def saved_json(path, limit):
    if path.is_symlink() or not path.is_file():
        raise SkillError('缺少可恢复的本地记录，或记录是符号链接')
    try:
        with path.open('rb') as stream:
            return json.loads(bounded_read(stream, limit))
    except (ValueError, UnicodeError):
        raise SkillError('本地记录不是有效 JSON；不会重新生成') from None


def load_state(out_dir):
    state = saved_json(out_dir / 'state.json', 8 * 1024 * 1024)
    if not isinstance(state, dict) or state.get('schema_version') != 1 or not isinstance(state.get('jobs'), list):
        raise SkillError('不支持的恢复记录格式')
    if not 1 <= len(state['jobs']) <= 1000 or not isinstance(state.get('save_prompts'), bool):
        raise SkillError('恢复记录无效')
    for idx, job in enumerate(state['jobs'], 1):
        if (not isinstance(job, dict) or job.get('index') != idx or not isinstance(job.get('request'), dict)
                or not isinstance(job.get('files'), list) or not isinstance(job.get('status'), str)
                or (state['save_prompts'] and not isinstance(job.get('prompt'), str))):
            raise SkillError('恢复记录中的任务结构无效')
        for item in job['files']:
            if (not isinstance(item, dict) or not isinstance(item.get('file'), str)
                    or not re.fullmatch(rf'{idx:03d}-\d{{2}}\.(png|jpeg|webp)', item['file'])
                    or not isinstance(item.get('sha256'), str)):
                raise SkillError('恢复记录包含不安全的文件名或校验值')
    return state


def file_matches(out_dir, item):
    path = out_dir / item['file']
    return (path.is_file() and not path.is_symlink() and path.stat().st_size <= MAX_IMAGE_BYTES
            and hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'])


def recover_job(out_dir, state, job, args):
    response_path = out_dir / f'response-{job["index"]:03d}.json'
    if not response_path.exists():
        if job['status'] == 'completed' and (not job['files'] or not all(file_matches(out_dir, item) for item in job['files'])):
            job['status'] = 'missing_response'
            job['error'] = '图片缺失或已变更，且没有可恢复的响应；不会重新生成'
            checkpoint(out_dir, state, not args.no_gallery)
        # submitting/unknown/pending 均不能在恢复时变成新的计费 POST。
        return job['status'] == 'completed'
    response = minimal_response(saved_json(response_path, MAX_RESPONSE_BYTES), state['save_prompts'])
    job['files'] = [item for item in job['files'] if file_matches(out_dir, item)]
    existing = {item['file']: item for item in job['files']}
    errors = []
    for idx, item in enumerate(response['data'], 1):
        prefix = f'{job["index"]:03d}-{idx:02d}.'
        previous = next((entry for name, entry in existing.items() if name.startswith(prefix)), None)
        if previous and file_matches(out_dir, previous):
            continue
        try:
            if item.get('invalid_result'):
                raise SkillError('此项响应缺少图片数据；其他已返回图片仍会保存')
            data, fmt = download_item(item, args.download_timeout)
            name = prefix + fmt
            atomic_write(out_dir / name, data)
            job['files'].append({'file': name, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
            checkpoint(out_dir, state, not args.no_gallery)
        except (SkillError, OSError) as exc:
            errors.append({'image_index': idx, 'error': str(exc) if isinstance(exc, SkillError) else '本地图片文件写入失败'})
    job['image_errors'] = errors
    if errors:
        job['status'] = 'download_failed'
        job['error'] = f'{len(errors)} 张图片未保存；其他结果已保留，详情见 state.json 的 image_errors'
        checkpoint(out_dir, state, not args.no_gallery)
        return False
    job['status'] = 'completed' if len(response['data']) == job['request'].get('n') else 'partial'
    job.pop('error', None)
    checkpoint(out_dir, state, not args.no_gallery)
    return job['status'] == 'completed'


def summary(out_dir, state):
    return {'output_dir': str(out_dir.resolve()), 'completed': sum(job['status'] == 'completed' for job in state['jobs']),
            'total': len(state['jobs']), 'files': [str((out_dir / item['file']).resolve()) for job in state['jobs'] for item in job['files']],
            'jobs': [{'index': job['index'], 'status': job['status'], 'request_id': job.get('request_id'),
                      'error': job.get('error'), 'image_errors': job.get('image_errors', [])} for job in state['jobs']]}


def run(args):
    if args.timeout <= 0 or args.download_timeout <= 0:
        raise SkillError('生成和下载超时必须大于 0 秒')
    if args.resume:
        if any((args.prompt, args.prompt_file, args.image, args.mask, args.endpoint, args.api_key, args.key_env,
                args.out_dir, args.save_prompts, args.dry_run, args.background, args.output_format,
                args.output_compression is not None, args.model != DEFAULT_MODEL, args.n != 1,
                args.size != '1024x1024', args.quality != 'high', args.response_format != 'b64_json')):
            raise SkillError('--resume 只恢复已有结果，不能同时指定生成输入、密钥或新输出目录')
        out_dir = Path(args.resume).expanduser()
        if not out_dir.is_dir():
            raise SkillError('恢复目录不存在')
        with directory_lock(out_dir):
            state = load_state(out_dir)
            for job in state['jobs']:
                try:
                    recover_job(out_dir, state, job, args)
                except (SkillError, OSError) as exc:
                    job['status'] = 'download_failed'
                    job['error'] = str(exc) if isinstance(exc, SkillError) else '本地文件读写失败'
                    checkpoint(out_dir, state, not args.no_gallery)
            return summary(out_dir, state)
    prompts, body, images, mask = prepare(args)
    if args.dry_run:
        return {'dry_run': True, 'endpoint': args.endpoint, 'request': body, 'prompt_count': len(prompts),
                'image_count': len(prompts) * args.n, 'reference_images': len(images), 'mask': bool(mask),
                'notice': '未联网、未写文件、未读取密钥；正式运行会产生模型调用费用'}
    key = resolve_api_key(args)
    out_dir = Path(args.out_dir).expanduser() if args.out_dir else Path('outputs') / ('guishu-image-' + dt.datetime.now().strftime('%Y%m%d-%H%M%S-') + uuid.uuid4().hex[:8])
    if out_dir.is_dir() and any(path.name != '.lock' for path in out_dir.iterdir()):
        raise SkillError('输出目录非空；请选择新目录，或用 --resume 仅恢复下载')
    out_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    with directory_lock(out_dir):
        if any(path.name != '.lock' for path in out_dir.iterdir()):
            raise SkillError('输出目录非空；请选择新目录，或用 --resume 仅恢复下载')
        state = {'schema_version': 1, 'skill_version': VERSION, 'endpoint': args.endpoint,
                 'save_prompts': args.save_prompts, 'created_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'jobs': []}
        for idx, prompt in enumerate(prompts, 1):
            job = {'index': idx, 'status': 'pending', 'files': [], 'request': dict(body),
                   'prompt_sha256': hashlib.sha256(prompt.encode('utf-8')).hexdigest()}
            if args.save_prompts:
                job['prompt'] = prompt
                job['request']['prompt'] = prompt
            state['jobs'].append(job)
        checkpoint(out_dir, state, not args.no_gallery)
        for prompt, job in zip(prompts, state['jobs']):
            job['status'] = 'submitting'
            checkpoint(out_dir, state, not args.no_gallery)
            print(f'[{job["index"]}/{len(prompts)}] 提交一次请求；不会自动重试', file=sys.stderr)
            try:
                result, request_id = post_image(args, key, dict(body, prompt=prompt), images, mask)
                job['request_id'] = request_id
                job['upstream_task_id'] = safe_id(result.get('task_id') or result.get('id'), key)
                clean = minimal_response(result, args.save_prompts)
                write_json(out_dir / f'response-{job["index"]:03d}.json', clean)
                job['status'] = 'response_saved'
                checkpoint(out_dir, state, not args.no_gallery)
                if not recover_job(out_dir, state, job, args):
                    break
            except (SkillError, OSError) as exc:
                job['status'] = 'download_failed' if (out_dir / f'response-{job["index"]:03d}.json').exists() else 'generation_unknown'
                job['error'] = str(exc) if isinstance(exc, SkillError) else '本地文件读写失败；请检查目录和剩余空间'
                if isinstance(exc, SkillError) and exc.request_id:
                    job['request_id'] = exc.request_id
                checkpoint(out_dir, state, not args.no_gallery)
                break
        return summary(out_dir, state)


def parser():
    p = argparse.ArgumentParser(description='贵数图片生成/编辑；--resume 只取已有结果，不重新生成')
    p.add_argument('--version', action='version', version=VERSION)
    p.add_argument('--prompt', default='')
    p.add_argument('--prompt-file', default='', help='UTF-8 文本，每行一条提示词；# 开头为注释')
    p.add_argument('--image', action='append', default=[], help='本地参考图路径，可重复指定')
    p.add_argument('--mask', default='', help='与第一张 PNG 参考图同尺寸的 Alpha PNG 蒙版')
    p.add_argument('--image-field', choices=['image', 'image[]'], default='image', help='默认与贵数网页版一致')
    p.add_argument('--endpoint', default='', help='完整 HTTPS 接口；带参考图时将 /images/generations 切换为 /images/edits')
    p.add_argument('--model', default=DEFAULT_MODEL)
    p.add_argument('--key-env', default='', help='显式指定凭据环境变量，不再读取其他变量')
    p.add_argument('--api-key', default='', help='旧版兼容参数；建议改用环境变量，避免 shell 历史泄露')
    p.add_argument('--size', default='1024x1024')
    p.add_argument('--quality', choices=['auto', 'low', 'medium', 'high', 'xhigh', 'max'], default='high')
    p.add_argument('--n', type=int, default=1)
    p.add_argument('--response-format', choices=['b64_json', 'url'], default='b64_json')
    p.add_argument('--background', choices=['auto', 'opaque', 'transparent'], default='')
    p.add_argument('--output-format', choices=['png', 'jpeg', 'webp'], default='')
    p.add_argument('--output-compression', type=int, default=None)
    p.add_argument('--timeout', type=int, default=1200, help='生成请求 socket 等待秒数，不保证上游在此期限内完成')
    p.add_argument('--download-timeout', type=int, default=120, help='单次下载 socket 等待秒数')
    p.add_argument('--out-dir', default='', help='新任务目录，必须为空')
    p.add_argument('--resume', default='', metavar='DIRECTORY', help='恢复已有目录中的图片下载；绝不发送生成请求')
    p.add_argument('--save-prompts', action='store_true', help='显式保存提示词和 revised_prompt；默认不保存')
    p.add_argument('--no-gallery', action='store_true', help='不创建或更新 HTML 预览页')
    p.add_argument('--dry-run', action='store_true', help='验证本地输入并显示不含提示词的计划，不联网、不写文件')
    p.add_argument('--json', action='store_true', help='stdout 输出结构化结果，进度写 stderr')
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        result = run(args)
    except (SkillError, OSError, UnicodeError) as exc:
        message = str(exc) if isinstance(exc, SkillError) else '本地文件读取或写入失败，请检查路径、编码与权限'
        if args.json:
            print(json.dumps({'error': message}, ensure_ascii=False))
        else:
            print(message, file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print('已中断；请求可能已受理。先检查原输出目录和用量，不要直接重发。', file=sys.stderr)
        return 130
    if args.json or args.dry_run:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f'已完成 {result["completed"]}/{result["total"]} 项；保存 {len(result["files"])} 张图片：{result["output_dir"]}')
        for job in result['jobs']:
            if job['status'] != 'completed':
                print(f'第 {job["index"]} 项：{job["status"]}；{job["error"] or "未取得完整结果，未自动重发"}', file=sys.stderr)
        if result['completed'] != result['total']:
            print('只恢复已有结果：python3 scripts/generate.py --resume "' + result['output_dir'] + '"', file=sys.stderr)
    return 0 if result.get('dry_run') or result['completed'] == result['total'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

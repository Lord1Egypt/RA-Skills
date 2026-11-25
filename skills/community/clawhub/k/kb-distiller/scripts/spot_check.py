#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""spot_check.py — kb 来源 URL 抽查（探活）脚本。

结构校验（validate_skill.py）之上的事实抽查第一步（见 kb-distiller/prompts/validate.md「事实抽查」）。
从 kb/SKILL.md 提取全部 http(s) URL，抽样探活，输出 OK / BLOCKED / EXEMPT / BROKEN 四态：

  OK       2xx / 3xx（可达，含重定向）
  BLOCKED  401 / 403 / 405 / 429 / 503 / 超时（可达但拒绝机器人/限流/网络不确定——人工复核，不计失败）
  EXEMPT   命中 EXEMPT_URLS 豁免表（POST-only/需凭证 API 端点等，GET 探活无意义——不探活）
  BROKEN   404 / 410 / 其余 4xx / 5xx / DNS 失败 / 连接失败（必须修复、登记 URL 迁移或豁免）

用法:
  python spot_check.py <产物目录> [--sample N] [--seed S] [--timeout T] [--all]
                        [--retries N] [--retry-delay D] [--host-delay D]

  --sample N      抽样 URL 数（默认 30；--all 则全量）
  --seed S        随机种子（默认 42，可复现）
  --timeout T     单请求超时秒数（默认 12）
  --all           全量检查（忽略 --sample）
  --retries N     BLOCKED 结果重试次数（默认 1；重试转 OK 判定为瞬时限流）
  --retry-delay D 重试前等待秒数（默认 5）
  --host-delay D  同域连续请求间隔秒数（默认 1；0 禁用——防并发限流误报，w3.org 403 实证）

退出码: 0 = 无 BROKEN；1 = 存在 BROKEN；2 = 用法/目录错误。
"""

import argparse
import random
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

URL_RE = re.compile(r'https?://[\x21-\x7e]+')  # 仅可见 ASCII（防中文误入 URL）
TRAIL_PUNCT = '.,;:!?)`*\'\"_'  # 剥离行内代码/加粗/引号尾随符

EXCLUDED_HOSTS = (
    'localhost', '127.0.0.1', 'example.com', 'example.org',
    'your-api.com', 'yourdomain.com', 'test.local',
)

EXEMPT_URLS = {
    'https://observe-api.nestjs.com/mcp':
        'NestJS Observe MCP 端点（POST + OAuth/omcp_ token，GET 401 属预期，非文档 URL）',
}

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0 Safari/537.36')


def extract_urls(root: Path):
    """提取 root 下全部 .md 文件中的 URL，返回 [(url, relative_file, line_no)]。"""
    found = []
    for md in sorted(root.rglob('*.md')):
        try:
            text = md.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for m in URL_RE.finditer(line):
                url = m.group(0).rstrip(TRAIL_PUNCT)
                if '<' in url or '>' in url:
                    continue  # 模板占位文字（如 <topic>.md）非真实 URL——真实 URL 不含尖括号
                host = urllib.request.urlparse(url).hostname or ''
                if any(h in host for h in EXCLUDED_HOSTS):
                    continue
                found.append((url, md.relative_to(root).as_posix(), i))
    # 去重（同 URL 保留首个出处）
    seen = {}
    for url, rel, ln in found:
        if url not in seen:
            seen[url] = (rel, ln)
    return [(u, v[0], v[1]) for u, v in seen.items()]


def probe(url: str, timeout: float) -> str:
    """探活单 URL，返回 'OK' | 'BLOCKED' | 'BROKEN: <原因>'。"""
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = resp.status
            return 'OK' if code < 400 else f'BROKEN: HTTP {code}'
    except urllib.error.HTTPError as e:
        if e.code in (401, 403, 405, 429, 503):
            return f'BLOCKED: HTTP {e.code}'
        return f'BROKEN: HTTP {e.code}'
    except urllib.error.URLError as e:
        reason = getattr(e, 'reason', e)
        if isinstance(reason, TimeoutError):
            return 'BLOCKED: timeout（网络不确定，人工复核）'
        return f'BROKEN: {reason}'
    except TimeoutError:
        return 'BLOCKED: timeout（网络不确定，人工复核）'
    except (ConnectionError, OSError, UnicodeError) as e:
        return f'BROKEN: {type(e).__name__}: {e}'


def probe_with_retry(url: str, timeout: float, retries: int, retry_delay: float) -> str:
    """探活并在 BLOCKED 时延迟重试：重试转 OK 判定为瞬时限流（采纳 OK）。"""
    status = probe(url, timeout)
    attempt = 0
    while status.startswith('BLOCKED') and attempt < retries:
        attempt += 1
        time.sleep(retry_delay)
        retried = probe(url, timeout)
        if retried.startswith('OK'):
            return f'OK（重试 {attempt} 次后，原 {status.split(":")[0].strip()} 为瞬时限流）'
        status = retried
    return status


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description='kb 来源 URL 抽查（探活）')
    ap.add_argument('target', help='产物目录（如 output/full-react-expert）')
    ap.add_argument('--sample', type=int, default=30, help='抽样数（默认 30）')
    ap.add_argument('--seed', type=int, default=42, help='随机种子（默认 42）')
    ap.add_argument('--timeout', type=float, default=12, help='单请求超时秒（默认 12）')
    ap.add_argument('--all', action='store_true', help='全量检查')
    ap.add_argument('--retries', type=int, default=1, help='BLOCKED 重试次数（默认 1）')
    ap.add_argument('--retry-delay', type=float, default=5, help='重试前等待秒（默认 5）')
    ap.add_argument('--host-delay', type=float, default=1, help='同域连续请求间隔秒（默认 1；0 禁用）')
    args = ap.parse_args()

    root = Path(args.target)
    if not root.is_dir():
        print(f'[ERROR] 目录不存在: {root}')
        sys.exit(2)

    urls = extract_urls(root)
    if not urls:
        print('[ERROR] 未提取到任何 URL')
        sys.exit(2)

    picked = urls if args.all else random.Random(args.seed).sample(
        urls, min(args.sample, len(urls)))
    # 按域聚类 + 同域间隔：降低单站并发限流误报（w3.org 403 实证）
    picked = sorted(picked, key=lambda t: (urllib.request.urlparse(t[0]).hostname or '', t[0]))

    print(f'== URL 抽查: {root} | 候选 {len(urls)} | 抽查 {len(picked)} | '
          f'seed {args.seed} | timeout {args.timeout}s | '
          f'retries {args.retries} | host-delay {args.host_delay}s ==\n')
    ok = blocked = broken = exempt = 0
    last_host, last_probe_at = None, 0.0
    for url, rel, ln in picked:
        if url in EXEMPT_URLS:
            exempt += 1
            print(f'[EXEMPT           ] {rel}:{ln}  {url}  -- {EXEMPT_URLS[url]}')
            continue
        host = urllib.request.urlparse(url).hostname or ''
        if args.host_delay > 0 and host == last_host:
            wait = args.host_delay - (time.monotonic() - last_probe_at)
            if wait > 0:
                time.sleep(wait)
        last_host, last_probe_at = host, time.monotonic()
        status = probe_with_retry(url, args.timeout, args.retries, args.retry_delay)
        if status.startswith('OK'):
            ok += 1
        elif status.startswith('BLOCKED'):
            blocked += 1
        else:
            broken += 1
        print(f'[{status:<18}] {rel}:{ln}  {url}')

    print(f'\n== 汇总: OK {ok} / BLOCKED {blocked} / EXEMPT {exempt} / BROKEN {broken} ==')
    if blocked:
        print('提示: BLOCKED 为可达但拒绝机器人/限流——人工或换抓取工具复核，不计失败。')
    if broken:
        print('失败: BROKEN 必须「修复来源 URL 或在冲突消解/对账记录登记 URL 迁移或豁免」。')
        sys.exit(1)
    print('结果: 无 BROKEN。')
    sys.exit(0)


if __name__ == '__main__':
    main()

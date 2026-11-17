#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
video_batch.py — 批量把「本地目录里的视频」封装成单文件 HTML 并上传到知识库

流程（一条命令）：遍历目录里的视频 → 逐个生成内嵌 HTML → 上传到目标文件夹

用法：
  python3 video_batch.py --dir ./videos --path "库名/文件夹名"
  python3 video_batch.py --dir ./videos --path "库名/文件夹名" --skip-upload   # 只生成，不上传
  python3 video_batch.py --dir ./videos --path "库名/文件夹名" --ext mp4,mov
  python3 video_batch.py --dir ./videos --path "库名/文件夹名" --title-map ./titles.json

规则：
  - 只处理 --dir 下的视频文件（默认 mp4,m4v,mov,webm,avi,mkv）
  - HTML 文件名 = 视频文件名（原样：不加序号、不加后缀；清洗掉 URL 危险字符）
  - **HTML 超过 10MB 自动跳过、不上传**，并在汇总里单独列出
  - 目标文件夹重名时不重复入库（可用 --allow-dup 放开）
  - 幂等：HTML 已存在且未加 --force 时跳过生成

依赖：python3、node（上传）、ffprobe（可选，取时长）
"""
import argparse
import json
import os
import subprocess
import sys
import time

sys.dont_write_bytecode = True  # 保持 skill 包干净：不生成 __pycache__

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
UPLOAD_CJS = os.path.join(SKILL_ROOT, 'knowledge-base', 'scripts', 'upload_to_kb.cjs')
GEN_PY = os.path.join(HERE, 'video_to_html.py')

sys.path.insert(0, HERE)
from video_to_html import safe_filename as safe_title  # noqa: E402  命名规则与单文件版保持一致

DEFAULT_EXT = ['mp4', 'm4v', 'mov', 'webm', 'avi', 'mkv']
HTML_LIMIT_MB = 10


def collect(dirpath, exts):
    out = []
    for name in sorted(os.listdir(dirpath)):
        full = os.path.join(dirpath, name)
        if not os.path.isfile(full):
            continue
        if os.path.splitext(name)[1].lstrip('.').lower() in exts:
            out.append(full)
    return out


def gen_html(mp4, title, out_dir, template=None):
    """返回 (ok, html_path, size_mb, warn)"""
    cmd = [sys.executable, GEN_PY, '--mp4', mp4, '--title', title, '--out-dir', out_dir]
    if template:
        cmd += ['--template', template]
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = r.stdout.decode('utf-8', 'ignore').strip().splitlines()
    try:
        d = json.loads(lines[-1])
    except Exception:
        return False, '', 0, (lines[-1] if lines else 'generate failed')
    return bool(d.get('ok')), d.get('out', ''), d.get('size_mb', 0), d.get('warn', '') or d.get('error', '')


def upload(html, kb_path, cancel_dup=True):
    cmd = ['node', UPLOAD_CJS, '--path', kb_path, '--file', html]
    if cancel_dup:
        cmd.append('--cancel-if-dup')
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = r.stdout.decode('utf-8', 'ignore')
    if '已成功入库' in out:
        return 'OK', ''
    if ('取消' in out) or ('重名' in out) or ('重复' in out):
        return 'SKIP', '目标文件夹已有同名条目'
    return 'FAIL', (out.strip().splitlines()[-1] if out.strip() else 'unknown error')


def main():
    ap = argparse.ArgumentParser(description='本地视频目录 → 内嵌 HTML → 上传知识库')
    ap.add_argument('--dir', required=True, help='视频所在目录')
    ap.add_argument('--path', required=True, help='目标知识库路径，如 "库名/文件夹名"')
    ap.add_argument('--ext', default=','.join(DEFAULT_EXT), help='视频扩展名，逗号分隔')
    ap.add_argument('--out-dir', help='HTML 输出目录（默认 <dir>/kb_html）')
    ap.add_argument('--template', help='自定义 HTML 模板')
    ap.add_argument('--title-map', help='JSON 文件：{"文件名":"标题"}（可选）')
    ap.add_argument('--skip-upload', action='store_true', help='只生成 HTML，不上传')
    ap.add_argument('--allow-dup', action='store_true', help='允许重名重复入库')
    ap.add_argument('--force', action='store_true', help='覆盖已存在的 HTML')
    ap.add_argument('--max', type=int, default=0, help='只处理前 N 个（调试用）')
    a = ap.parse_args()

    if not os.path.isdir(a.dir):
        print('[error] --dir 不是目录：%s' % a.dir)
        return 2

    exts = {e.strip().lower() for e in a.ext.split(',') if e.strip()}
    files = collect(a.dir, exts)
    if a.max:
        files = files[:a.max]
    if not files:
        print('[error] %s 下没有找到视频文件（扩展名：%s）' % (a.dir, ','.join(sorted(exts))))
        return 2

    out_dir = a.out_dir or os.path.join(a.dir, 'kb_html')
    os.makedirs(out_dir, exist_ok=True)

    title_map = {}
    if a.title_map and os.path.isfile(a.title_map):
        try:
            title_map = json.load(open(a.title_map, encoding='utf-8'))
        except Exception as e:
            print('[warn] title-map 读取失败：%s' % e)

    report, oversize = [], []
    print('共 %d 个视频 | 输出：%s | 目标：%s' % (len(files), out_dir, a.path))
    for i, mp4 in enumerate(files, 1):
        base = os.path.basename(mp4)
        stem = os.path.splitext(base)[0]
        title = title_map.get(base) or title_map.get(stem) or stem
        tag = '[%d/%d] %s' % (i, len(files), stem)

        export = os.path.join(out_dir, safe_title(title) + '.html')
        if os.path.isfile(export) and not a.force:
            ok, html_file, size_mb, warn = True, export, os.path.getsize(export) / 1048576.0, ''
        else:
            ok, html_file, size_mb, warn = gen_html(mp4, title, out_dir, a.template)

        if not ok:
            if '10MB' in warn:
                print('%s ⛔ 超限跳过：%s' % (tag, warn))
                oversize.append((stem, size_mb, warn))
                report.append((stem, 'TOO_BIG', size_mb))
            else:
                print('%s ❌ 生成失败：%s' % (tag, warn))
                report.append((stem, 'GEN_FAIL', size_mb))
            continue

        if a.skip_upload:
            print('%s ✅ 已生成 %.2fMB（未上传）' % (tag, size_mb))
            report.append((stem, 'GEN', size_mb))
            continue

        status, msg = upload(html_file, a.path, cancel_dup=not a.allow_dup)
        icon = {'OK': '✅ 已入库', 'SKIP': '⏭ 跳过', 'FAIL': '❌ 上传失败'}[status]
        print('%s %s %.2fMB %s' % (tag, icon, size_mb, msg))
        report.append((stem, status, size_mb))
        time.sleep(0.6)

    ok = sum(1 for r in report if r[1] == 'OK')
    gen = sum(1 for r in report if r[1] == 'GEN')
    skip = sum(1 for r in report if r[1] == 'SKIP')
    fail = [r for r in report if r[1] == 'FAIL']
    genfail = [r for r in report if r[1] == 'GEN_FAIL']
    print('\n===== 汇总 =====')
    print('入库成功 %d | 已生成 %d | 跳过 %d | 上传失败 %d | 生成失败 %d | 超 10MB 未上传 %d'
          % (ok, gen, skip, len(fail), len(genfail), len(oversize)))
    for s, mb, w in oversize:
        print('  超限：%s（%.2fMB）%s' % (s, mb, w))
    for s, _, _ in genfail:
        print('  生成失败：%s' % s)
    for s, _, _ in fail:
        print('  上传失败：%s' % s)
    print('（超过 10MB 的视频不会上传，请先压缩或截短后重跑）')
    return 0 if not fail and not genfail else 1


if __name__ == '__main__':
    sys.exit(main())

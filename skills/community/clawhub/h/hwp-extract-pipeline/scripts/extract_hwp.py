#!/usr/bin/env python3
"""
HWP extraction pipeline with HWPX support.
Usage: extract_hwp.py --input /path/to/file --id PBLN_xxx [--venv /path/to/venv]

Priority: hwp-reader -> pyhwp -> hwpx(zip) -> ocr(not implemented) -> strings
When --venv is provided (or default ~/.openclaw/venv exists), pyhwp will be
executed with that Python interpreter so it can use the venv-installed packages.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import shutil
import tempfile
import zipfile
import xml.etree.ElementTree as ET


def run_cmd(cmd, timeout=30, env=None):
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, env=env)
        return p.returncode, p.stdout.decode('utf-8', errors='replace'), p.stderr.decode('utf-8', errors='replace')
    except subprocess.TimeoutExpired:
        return -1, '', 'timeout'


def find_hwp_reader():
    # Check in PATH, workspace skills, and venv bin
    candidates = []
    # PATH
    candidates.append(('path', shutil.which('hwp-reader')))
    # workspace skill
    ws_candidate = os.path.join(os.getcwd(), 'skills', 'hwp-reader', 'hwp-reader')
    if os.path.exists(ws_candidate):
        candidates.append(('workspace', ws_candidate))
    ws_candidate2 = os.path.join(os.getcwd(), 'skills', 'hwp-reader', 'scripts', 'hwp-reader')
    if os.path.exists(ws_candidate2):
        candidates.append(('workspace-scripts', ws_candidate2))
    # venv default
    venv_bin = os.path.join(os.path.expanduser('~'), '.openclaw', 'venv', 'bin', 'hwp-reader')
    if os.path.exists(venv_bin):
        candidates.append(('venv', venv_bin))
    for src, path in candidates:
        if path and os.path.exists(path):
            return path
    return None


def try_hwp_reader(path):
    hwp_bin = find_hwp_reader()
    if not hwp_bin:
        return None, 'hwp-reader not found'
    rc, out, err = run_cmd([hwp_bin, path], timeout=30)
    if rc == 0 and out.strip():
        return out, None
    return None, err or f'exitcode={rc}'


def try_pyhwp(path, venv_python=None):
    # If venv_python provided, use it to run a small temporary extractor script
    try:
        tf = tempfile.NamedTemporaryFile(mode='w', suffix='_pyhwp_extract.py', delete=False)
        tf.write('#!/usr/bin/env python3\n')
        tf.write('import sys\n')
        tf.write('try:\n')
        tf.write('    import pyhwp\n')
        tf.write('except Exception as e:\n')
        tf.write("    sys.stderr.write('pyhwp-import-error:%s' % str(e))\n")
        tf.write('    sys.exit(2)\n')
        tf.write('try:\n')
        tf.write('    f = pyhwp.HWPFile(open(sys.argv[1], \"rb\"))\n')
        tf.write('    text = []\n')
        tf.write('    for p in f.body_text():\n')
        tf.write('        text.append(p)\n')
        tf.write('    print("\\n".join(text))\n')
        tf.write('except Exception as e:\n')
        tf.write('    import traceback; traceback.print_exc(file=sys.stderr); sys.exit(3)\n')
        tf.flush()
        tf.close()
        os.chmod(tf.name, 0o700)
        python_exec = venv_python or sys.executable
        rc, out, err = run_cmd([python_exec, tf.name, path], timeout=40)
        try:
            os.unlink(tf.name)
        except Exception:
            pass
        if rc == 0 and out.strip():
            return out, None
        return None, err or f'exit={rc}'
    except Exception as e:
        return None, f'pyhwp-wrapper-exc:{e}'


def extract_hwpx(path):
    """Extract text from HWPX (zip) files by reading Preview/PrvText.txt and
    Contents/section*.xml elements."""
    try:
        if not zipfile.is_zipfile(path):
            return None, 'not-zip'
        z = zipfile.ZipFile(path, 'r')
        namelist = z.namelist()
        texts = []
        # Prefer Preview/PrvText.txt if available
        if 'Preview/PrvText.txt' in namelist:
            try:
                data = z.read('Preview/PrvText.txt')
                texts.append(data.decode('utf-8', errors='replace'))
            except Exception as e:
                # continue to section xmls
                pass
        # Read Contents/section*.xml
        section_names = [n for n in namelist if n.startswith('Contents/section') and n.endswith('.xml')]
        section_names.sort()
        for name in section_names:
            try:
                data = z.read(name)
                # parse xml and extract text nodes
                try:
                    root = ET.fromstring(data)
                    for elem in root.iter():
                        if elem.text and elem.text.strip():
                            texts.append(elem.text.strip())
                except Exception:
                    # fallback: treat as raw text
                    texts.append(data.decode('utf-8', errors='replace'))
            except Exception:
                continue
        if texts:
            return '\n\n'.join(texts), None
        return None, 'no-text-found'
    except Exception as e:
        return None, f'hwpx-exc:{e}'


def try_strings(path):
    if not shutil.which('strings'):
        return None, 'strings not found'
    cmd = ['strings', path]
    rc, out, err = run_cmd(cmd, timeout=10)
    if rc == 0 and out.strip():
        return out, None
    return None, err or 'no-strings'


def detect_default_venv():
    venv_path = os.path.join(os.path.expanduser('~'), '.openclaw', 'venv', 'bin', 'python')
    if os.path.exists(venv_path):
        return venv_path
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--id', required=True)
    parser.add_argument('--venv', required=False, help='Path to venv python (bin/python) to run pyhwp from')
    args = parser.parse_args()

    path = args.input
    rec_id = args.id
    venv_python = args.venv or detect_default_venv()
    start = time.time()

    result = {
        'id': rec_id,
        'path': path,
        'text': None,
        'method': None,
        'mime': None,
        'notes': [],
        'elapsed': None,
    }

    # 1: hwp-reader
    try:
        out, err = try_hwp_reader(path)
        if out:
            result.update({'text': out, 'method': 'hwp-reader'})
            result['elapsed'] = time.time() - start
            print(json.dumps(result, ensure_ascii=False))
            with open(f"{rec_id}_extracted.json","w",encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False))
            return
        else:
            result['notes'].append('hwp-reader: %s' % (err or 'no-output'))
    except Exception as e:
        result['notes'].append('hwp-reader-exc: %s' % str(e))

    # 2: pyhwp via venv or current python
    try:
        out, err = try_pyhwp(path, venv_python)
        if out:
            result.update({'text': out, 'method': 'pyhwp'})
            result['elapsed'] = time.time() - start
            print(json.dumps(result, ensure_ascii=False))
            with open(f"{rec_id}_extracted.json","w",encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False))
            return
        else:
            result['notes'].append('pyhwp: %s' % (err or 'no-output'))
    except Exception as e:
        result['notes'].append('pyhwp-exc: %s' % str(e))

    # 3: HWPX (zip) direct extraction
    try:
        out, err = extract_hwpx(path)
        if out:
            result.update({'text': out, 'method': 'hwpx'})
            result['elapsed'] = time.time() - start
            print(json.dumps(result, ensure_ascii=False))
            with open(f"{rec_id}_extracted.json","w",encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False))
            return
        else:
            result['notes'].append('hwpx: %s' % (err or 'no-output'))
    except Exception as e:
        result['notes'].append('hwpx-exc: %s' % str(e))

    # 4: strings fallback
    try:
        out, err = try_strings(path)
        if out:
            result.update({'text': out, 'method': 'strings'})
            result['elapsed'] = time.time() - start
            print(json.dumps(result, ensure_ascii=False))
            with open(f"{rec_id}_extracted.json","w",encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False))
            return
        else:
            result['notes'].append('strings: %s' % (err or 'no-output'))
    except Exception as e:
        result['notes'].append('strings-exc: %s' % str(e))

    result['elapsed'] = time.time() - start
    print(json.dumps(result, ensure_ascii=False))
    with open(f"{rec_id}_extracted.json","w",encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()

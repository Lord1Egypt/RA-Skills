from __future__ import annotations

import argparse
import json
import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import os
import re

import requests


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


class StatusWindow:
    def __init__(self, title: str = 'OCR Progress', enabled: bool = True):
        self.enabled = enabled
        self._q: queue.Queue[str] = queue.Queue()
        self._thread = None
        if not enabled:
            return
        try:
            import tkinter as tk
            from tkinter.scrolledtext import ScrolledText
        except Exception:
            self.enabled = False
            return

        def _run():
            root = tk.Tk()
            root.title(title)
            root.geometry('760x420')
            text = ScrolledText(root, wrap='word')
            text.pack(fill='both', expand=True)

            def poll():
                while True:
                    try:
                        msg = self._q.get_nowait()
                    except queue.Empty:
                        break
                    if msg == '__CLOSE__':
                        root.destroy()
                        return
                    text.insert('end', msg + '\n')
                    text.see('end')
                root.after(200, poll)

            poll()
            root.mainloop()

        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()

    def log(self, msg: str) -> None:
        # 进度日志走 stderr，避免污染 stdout 的 JSON 行管道
        print(msg, file=__import__('sys').stderr)
        if self.enabled:
            self._q.put(msg)

    def close(self) -> None:
        if self.enabled:
            self._q.put('__CLOSE__')


def resolve_secret(value: str) -> str:
    v = (value or '').strip()
    if v.startswith('${') and v.endswith('}'):
        return (os.getenv(v[2:-1]) or '').strip()
    return v


def redact(text: str) -> str:
    if not text:
        return ''
    out = text
    out = re.sub(r'(?i)(authorization\s*:\s*bearer\s+)[^\s"\']+', r'\1***', out)
    out = re.sub(r'(?i)(api[_-]?key\s*[=:]\s*)[^\s,;"\']+', r'\1***', out)
    out = re.sub(r'(?i)(token\s*[=:]\s*)[^\s,;"\']+', r'\1***', out)
    return out


def submit_job(pdf_path: Path, job_url: str, api_key: str, model: str, optional_payload: dict) -> str:
    headers = {'Authorization': f'bearer {api_key}'}
    data = {'model': model, 'optionalPayload': json.dumps(optional_payload, ensure_ascii=False)}
    last_err = ''
    for i in range(3):
        with pdf_path.open('rb') as f:
            resp = requests.post(job_url, headers=headers, data=data, files={'file': f}, timeout=120)
        if resp.status_code == 200:
            return resp.json()['data']['jobId']
        # 仅保留简短且脱敏后的错误预览，避免敏感信息泄露
        preview = redact((resp.text or '').replace('\n', ' '))[:160]
        last_err = f'{resp.status_code} {preview}'
        time.sleep(2 * (i + 1))
    raise RuntimeError(f'OCR提交失败: {last_err}')


def poll_job(job_id: str, job_url: str, api_key: str, poll_seconds: float, timeout_seconds: float, ui: StatusWindow) -> str:
    headers = {'Authorization': f'bearer {api_key}'}
    start = time.time()
    while True:
        resp = requests.get(f'{job_url}/{job_id}', headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json().get('data', {})
        state = data.get('state')
        if state == 'done':
            return (data.get('resultUrl') or {}).get('jsonUrl', '')
        if state == 'failed':
            raise RuntimeError(f"OCR任务失败: {data.get('errorMsg', 'unknown')}")
        if state == 'running':
            prog = data.get('extractProgress', {})
            ui.log(f"[OCR] job={job_id} running pages={prog.get('extractedPages','?')}/{prog.get('totalPages','?')}")
        if timeout_seconds > 0 and (time.time() - start) >= timeout_seconds:
            raise TimeoutError(f'OCR超时: {job_id}')
        time.sleep(max(0.2, poll_seconds))


def fetch_markdown(jsonl_url: str) -> str:
    resp = requests.get(jsonl_url, timeout=180)
    resp.raise_for_status()
    chunks: list[str] = []
    for line in [x.strip() for x in resp.text.splitlines() if x.strip()]:
        payload = json.loads(line)
        for item in payload.get('result', {}).get('layoutParsingResults', []):
            txt = (((item or {}).get('markdown') or {}).get('text') or '').strip()
            if txt:
                chunks.append(txt)
    merged = '\n\n'.join(chunks).strip()
    if not merged:
        raise ValueError('OCR无可用文本')
    return merged


def process_one(pdf: Path, config: dict, ui: StatusWindow) -> dict:
    pconf = config['paddleocr']
    api_key = resolve_secret((pconf.get('api_key') or '').strip())
    if not api_key:
        raise ValueError('config.json 缺少 paddleocr.api_key（可用 ${ENV_VAR} 引用环境变量）')

    ui.log(f'[OCR] 提交任务: {pdf}')
    job_id = submit_job(pdf, pconf['job_url'], api_key, pconf['model'], pconf.get('optional_payload', {}))
    ui.log(f'[OCR] 提交成功: {pdf.name} jobId={job_id}')
    jsonl_url = poll_job(job_id, pconf['job_url'], api_key, pconf.get('poll_seconds', 5), pconf.get('timeout_seconds', 1800), ui)
    markdown = fetch_markdown(jsonl_url)
    ui.log(f'[OCR] 完成: {pdf.name}, chars={len(markdown)}')
    return {'pdf_path': str(pdf), 'text': markdown}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default='config.json')
    ap.add_argument('--pdf', action='append', default=[])
    args = ap.parse_args()

    config = read_json(Path(args.config))
    pdfs = [Path(p) for p in args.pdf]
    if not pdfs:
        raise SystemExit('缺少 --pdf')

    pconf = config.get('paddleocr', {})
    threads = max(1, int(pconf.get('threads', 1)))
    show_window = bool(pconf.get('show_window', True))
    ui = StatusWindow(title='PaddleOCR 可见窗口', enabled=show_window)

    try:
        with ThreadPoolExecutor(max_workers=threads) as ex:
            futs = [ex.submit(process_one, pdf, config, ui) for pdf in pdfs]
            for f in as_completed(futs):
                print(json.dumps(f.result(), ensure_ascii=True))
    finally:
        ui.log('[OCR] 处理结束')
        time.sleep(0.5)
        ui.close()

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

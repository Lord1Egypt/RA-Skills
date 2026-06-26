from __future__ import annotations

import argparse
import json
import os
import queue
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from openai import OpenAI


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


class StatusWindow:
    def __init__(self, title: str = 'Summarize Progress', enabled: bool = True):
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
        print(msg)
        if self.enabled:
            self._q.put(msg)

    def close(self) -> None:
        if self.enabled:
            self._q.put('__CLOSE__')


def slugify(name: str) -> str:
    stem = re.sub(r"\s+", " ", name).strip()
    stem = re.sub(r"[\\/:*?\"<>|]", "_", stem)
    return stem[:80] or "未命名论文"


def load_prompt(prompt_path: Path, topic: str, direction: str, pdf_path: str, output_path: str) -> str:
    text = prompt_path.read_text(encoding='utf-8')
    text = text.replace('{{RESEARCH_TOPIC}}', topic)
    text = text.replace('{{RESEARCH_DIRECTION}}', direction)
    text = text.replace('{{PDF_PATH}}', pdf_path)
    text = text.replace('{{OUTPUT_PATH}}', output_path)
    return text


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


def resolve_provider_config(config: dict) -> tuple[str, str, str]:
    sconf = config['summarizer']
    provider = sconf.get('provider', 'openai-compatible')
    providers = sconf.get('providers', {})
    if provider not in providers:
        raise ValueError(f'config.json summarizer.provider 无效: {provider}')
    p = providers[provider]
    base_url = (p.get('base_url') or '').strip()
    api_key = resolve_secret((p.get('api_key') or '').strip())
    model = (p.get('model') or '').strip()
    if not base_url or not api_key or not model:
        raise ValueError(f'config.json summarizer.providers.{provider} 缺少 base_url/api_key/model（api_key 支持 ${'{'}ENV_VAR{'}'}）')
    return base_url, api_key, model


def sanitize_report(content: str) -> str:
    c = content.replace('</think>', '').strip()
    markers = ['# 论文标题（中文）', '# 标题', '## 论文标题（中文）', '### 论文题目（中英）', '# Part A. 宏观综述']
    idxs = [c.find(m) for m in markers if c.find(m) >= 0]
    if idxs:
        c = c[min(idxs):]
    return c.strip()


def summarize_one(base_url: str, api_key: str, model: str, prompt_template: str, row: dict, output_dir_override: str, max_chars: int, ui: StatusWindow) -> Path:
    pdf_path = str(row['pdf_path'])
    text = str(row['text'])
    if max_chars > 0 and len(text) > max_chars:
        text = text[:max_chars]

    merged_prompt = prompt_template.replace('{以下是待总结文本}', text)
    ui.log(f'[SUM] 开始: {pdf_path}')

    client = OpenAI(base_url=base_url, api_key=api_key)
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': merged_prompt}],
        )
    except Exception as e:
        # 避免直接透传可能包含敏感响应体/密钥的原始异常文本
        em = redact(str(e)).replace('\n', ' ')[:220]
        raise RuntimeError(f'LLM 调用失败: {e.__class__.__name__}: {em}')
    content = sanitize_report((resp.choices[0].message.content or '').strip())
    if not content:
        raise ValueError(f'模型返回空内容: {pdf_path}')

    out_dir = Path(output_dir_override) if output_dir_override else (Path(pdf_path).parent / '总结')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slugify(Path(pdf_path).stem)}_研读报告.md"
    out_path.write_text(content, encoding='utf-8')
    ui.log(f'[SUM] 完成: {out_path}')
    return out_path


def parse_inputs_stdin() -> list[dict]:
    raw = sys.stdin.read().strip()
    if not raw:
        raise ValueError('stdin 缺少抽取文本输入')
    rows: list[dict] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default='config.json')
    ap.add_argument('--prompt', default='prompt.md')
    ap.add_argument('--topic', default='（请填写）')
    ap.add_argument('--direction', default='（请填写）')
    ap.add_argument('--pdf-path', required=True)
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--input-from-stdin', action='store_true')
    args = ap.parse_args()

    config = read_json(Path(args.config))
    base_url, api_key, model = resolve_provider_config(config)

    prompt_template = load_prompt(
        Path(args.prompt),
        args.topic,
        args.direction,
        args.pdf_path,
        args.output_dir,
    )

    sconf = config.get('summarizer', {})
    max_chars = int(sconf.get('max_input_chars', 0))
    threads = max(1, int(sconf.get('threads', 1)))
    show_window = bool(sconf.get('show_window', True))
    ui = StatusWindow(title='Summarize 可见窗口', enabled=show_window)

    if not args.input_from_stdin:
        raise SystemExit('请使用 --input-from-stdin 传入抽取文本')

    rows = parse_inputs_stdin()

    try:
        with ThreadPoolExecutor(max_workers=threads) as ex:
            futs = [
                ex.submit(summarize_one, base_url, api_key, model, prompt_template, row, args.output_dir, max_chars, ui)
                for row in rows
            ]
            for f in as_completed(futs):
                out = f.result()
                print(out)
                time.sleep(max(0, float(sconf.get('sleep_seconds', 1))))
    finally:
        ui.log('[SUM] 处理结束')
        time.sleep(0.5)
        ui.close()

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

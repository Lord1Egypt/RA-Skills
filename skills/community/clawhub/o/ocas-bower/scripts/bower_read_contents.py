#!/usr/bin/env python3
"""
Read and summarize file contents for Bower's deep scan.
Reads: Google Docs/Sheets/Slides (export), native text/code/markdown files.
Summarizes in ~150 words — enough to write a Drive description.
"""
import json
import sys
import re
import time
from pathlib import Path
from datetime import datetime, timezone

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 bower_read_contents.py [no flags]")
    sys.exit(0)

# Auth
import sys as _sys
_sys.path.insert(0, str(Path.home() / '.hermes' / 'scripts'))
from google_auth import get_drive_service

def get_drive():
    return get_drive_service()
READABLE_MIME = {
    'text/plain', 'text/html', 'text/csv', 'text/x-python',
    'text/x-sh', 'text/x-script.python', 'text/markdown',
    'text/x-csharp', 'text/x-c++src', 'text/x-chdr',
    'text/x-log', 'text/x-bibtex', 'text/javascript',
    'text/x-java', 'text/x-ruby', 'text/x-perl',
    'text/x-tex', 'text/x-ts', 'text/x-c',
    'application/json', 'application/xml', 'application/yaml',
    'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
}

# Google Workspace native types
GOOGLE_DOC = {
    'application/vnd.google-apps.document',
    'application/vnd.google-apps.spreadsheet',
    'application/vnd.google-apps.presentation',
    'application/vnd.google-apps.drawing',
}

# Export mime mapping
EXPORT_MIME = {
    'application/vnd.google-apps.document': 'text/plain',
    'application/vnd.google-apps.spreadsheet': 'text/csv',
    'application/vnd.google-apps.presentation': 'text/plain',
    'application/vnd.google-apps.drawing': 'image/png',
}


def read_content(drive, file_rec):
    """Read file content. Returns (text_content, error_or_none)."""
    mime = file_rec.get('mimeType', '')
    fid = file_rec.get('id')
    name = file_rec.get('name', '')
    size = int(file_rec.get('size', 0) or 0)

    if not fid:
        return None, 'no file id'

    # Google Workspace files — export via Drive API
    if mime in EXPORT_MIME:
        export_mime = EXPORT_MIME[mime]
        try:
            content = drive.files().export_media(
                fileId=fid, mimeType=export_mime
            ).execute()
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='replace')
            return content[:8000], None  # cap at 8K chars for summary
        except Exception as e:
            return None, f'export failed: {e}'

    # Regular readable files
    if mime not in READABLE_MIME:
        return None, f'not readable mime: {mime}'

    if size > 5 * 1024 * 1024:
        return None, 'file too large'

    try:
        content = drive.files().get_media(fileId=fid).execute()
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='replace')
        return content[:8000], None
    except Exception as e:
        return None, f'media read failed: {e}'


def summarize_text(content, name=''):
    """Simple extractive summary — grab the first meaningful paragraphs.
    For LLM summarization, pass to an LLM. This is the fallback.
    """
    if not content:
        return ''

    # Strip binary noise
    content = re.sub(r'[\x00-\x08\x0e-\x1f\x7f-\x9f]', '', content)

    # For code: return first 40 lines
    code_indicators = ['def ', 'class ', 'import ', 'package ', 'function', 'const ', 'let ', 'var ', '#include', 'fn ', 'impl ']
    first_200 = content[:200]
    is_code = any(content.startswith(p) for p in ['#!/', '<?php', '<!DOCTYPE', '<html']) or any(p in first_200 for p in code_indicators)
    if is_code:
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('//')]
        return '\n'.join(lines[:30])

    # For prose: first 3 paragraphs
    paragraphs = re.split(r'\n\n+', content)
    meaningful = [p.strip() for p in paragraphs if len(p.strip()) > 50 and not p.strip().startswith('#')]
    if meaningful:
        return '\n\n'.join(meaningful[:3])

    # Fallback: first 300 chars
    return content[:300].strip()


def summarize_llm(content, name, mime):
    """Use LLM to summarize content in ~150 words. Returns summary string."""
    # Detect type
    if 'google-apps' in mime:
        doc_type = 'Google Doc'
    elif mime.startswith('text/x-') or mime == 'text/plain':
        doc_type = 'code'
    elif mime == 'text/markdown':
        doc_type = 'markdown'
    elif mime == 'application/json':
        doc_type = 'data/JSON'
    elif mime == 'text/csv':
        doc_type = 'spreadsheet/CSV'
    else:
        doc_type = 'document'

    prompt = f"""Summarize this {doc_type} file called "{name}" in 3-5 sentences. Focus on: what is this document about, what data/ideas does it contain, and any notable structure or scope. Be specific, not generic.

{content[:6000]}

Summary:"""

    return prompt  # Return the prompt to be processed by caller


def main():
    import glob

    SCANS_DIR = Path.home() / ".hermes" / "commons" / "data" / "ocas-bower" / "scans"
    PROGRESS_FILE = Path.home() / ".hermes" / "commons" / "data" / "ocas-bower" / "content_progress.json"
    RESULTS_FILE = Path.home() / ".hermes" / "commons" / "data" / "ocas-bower" / "content_summaries.jsonl"
    MAX_FILES = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    OFFSET = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    drive = get_drive()
    if not drive:
        print('No Drive access. Check tokens.', file=sys.stderr)
        sys.exit(1)

    # Load existing progress
    progress = {}
    if PROGRESS_FILE.exists():
        progress = json.loads(PROGRESS_FILE.read_text())

    # Load existing results
    results = []
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE) as f:
            for line in f:
                try:
                    results.append(json.loads(line))
                except:
                    pass

    done_ids = {r['id'] for r in results}

    # Collect all readable files from scan files
    scan_files = glob.glob(str(SCANS_DIR / "*.json"))
    print(f'Found {len(scan_files)} scan files')

    all_files = []
    for sf in scan_files:
        try:
            data = json.load(open(sf))
            for f in data.get('files', []):
                mt = f.get('mimeType', '')
                if mt == 'application/vnd.google-apps.folder':
                    continue
                size = int(f.get('size', 0) or 0)
                if size > 5 * 1024 * 1024:
                    continue
                all_files.append(f)
        except Exception as e:
            print(f'Scan file error {sf}: {e}', file=sys.stderr)

    print(f'Total readable files: {len(all_files)}')

    # Filter to Google Docs + code + markdown + PDF (most valuable)
    priority_types = {
        'application/vnd.google-apps.document',
        'application/vnd.google-apps.spreadsheet',
        'application/vnd.google-apps.presentation',
        'text/markdown',
        'text/plain',
        'application/pdf',
        'application/json',
    }
    priority = [f for f in all_files if f.get('mimeType') in priority_types]
    others = [f for f in all_files if f.get('mimeType') not in priority_types]
    work_list = priority + others
    work_list = [f for f in work_list if f['id'] not in done_ids]
    work_list = work_list[OFFSET:OFFSET + MAX_FILES]

    print(f'Processing {len(work_list)} files (offset={OFFSET})')

    new_results = 0
    errors = 0

    for i, f in enumerate(work_list):
        fid = f['id']
        name = f.get('name', '')
        mime = f.get('mimeType', '')
        folder = f.get('folder_path', '')

        content, err = read_content(drive, f)
        if err:
            errors += 1
            if i < 10 or errors < 5:
                print(f'  SKIP {name}: {err}')
            continue

        summary = summarize_text(content, name)
        prompt_for_llm = summarize_llm(content, name, mime)

        result = {
            'id': fid,
            'name': name,
            'mimeType': mime,
            'folder_path': folder,
            'size': f.get('size'),
            'summary_text': summary,  # extracted text (not LLM summary)
            'llm_prompt': prompt_for_llm,  # ready to send to LLM
            'read_at': datetime.now(timezone.utc).isoformat(),
        }

        with open(RESULTS_FILE, 'a') as out:
            out.write(json.dumps(result, ensure_ascii=False) + '\n')

        results.append(result)
        new_results += 1

        if (i + 1) % 50 == 0:
            print(f'  [{i+1}/{len(work_list)}] done, {new_results} results, {errors} errors')

        time.sleep(0.05)  # gentle rate limit

    print(f'\nDone. {new_results} new files read, {errors} errors')
    print(f'Total results: {len(results)}')


if __name__ == '__main__':
    main()

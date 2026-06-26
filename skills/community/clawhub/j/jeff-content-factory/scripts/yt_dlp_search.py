#!/usr/bin/env python3
"""
Search YouTube via yt-dlp and output JSON results.

Usage:
  python3 scripts/yt_dlp_search.py "your query" --max 10 --out results.jsonl
"""
import argparse
import json
import shutil
import subprocess
import sys


def get_ytdlp_cmd():
  if shutil.which('yt-dlp'):
    return ['yt-dlp']
  return [sys.executable, '-m', 'yt_dlp']


def run_search(query, max_results):
  search_term = f'ytsearch{max_results}:{query}'
  cmd = get_ytdlp_cmd() + ['--dump-json', '--skip-download', search_term]
  proc = subprocess.run(cmd, capture_output=True, text=True)
  if proc.returncode != 0:
    sys.stderr.write(proc.stderr)
    raise SystemExit(proc.returncode)
  results = []
  for line in proc.stdout.splitlines():
    line = line.strip()
    if not line:
      continue
    try:
      data = json.loads(line)
    except json.JSONDecodeError:
      continue
    results.append({
      'id': data.get('id'),
      'title': data.get('title'),
      'channel': data.get('channel') or data.get('uploader'),
      'channel_id': data.get('channel_id') or data.get('uploader_id'),
      'view_count': data.get('view_count'),
      'upload_date': data.get('upload_date'),
      'duration': data.get('duration'),
      'webpage_url': data.get('webpage_url'),
      'description': data.get('description'),
    })
  return results


def main():
  parser = argparse.ArgumentParser(
    description='Search YouTube via yt-dlp and output JSON results.'
  )
  parser.add_argument('query', help='Search query')
  parser.add_argument('--max', type=int, default=10, help='Max results')
  parser.add_argument('--out', help='Output JSONL file path')
  args = parser.parse_args()

  results = run_search(args.query, args.max)
  if args.out:
    with open(args.out, 'w', encoding='utf-8') as handle:
      for item in results:
        handle.write(json.dumps(item, ensure_ascii=True) + '\n')
  else:
    print(json.dumps(results, ensure_ascii=True, indent=2))


if __name__ == '__main__':
  main()

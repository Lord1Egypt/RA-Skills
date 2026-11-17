# -*- coding: utf-8 -*-
"""
recover_l1.py — L1 精读结果回收 + 失败自动重投（通用版，路径全参数化）。

扫描 OUTBOX 下 result-<id>([-fN]).json：
  - status == done  → 把 content 落盘 OUTDIR/<name>_摘要.md
  - 否则（failed / 超时 abort） → 按 names.json 重投（id 加 -fN 后缀，最多 3 次）
全部回收完成退出 0；限时内未完成退出 2。

用法：
  python recover_l1.py --inbox <INBOX> --outbox <OUTBOX> --outdir <OUTDIR> \
                       --hub <HUB> --names names.json [--interval 60] [--max-minutes 45]

names.json 格式：
  {"L1-11": {"name": "GMP质量体系与验证枢纽", "file": "GMP质量体系与验证枢纽.md"}, ...}
"""
import argparse, json, os, re, sys, time, datetime


def load_names(p):
    if not p:
        return {}
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def now():
    return datetime.datetime.now().strftime('%H:%M:%S')


def recover_one(outbox, tid):
    """从 outbox 回收单个任务。返回 content(str) | False(失败) | None(无回执)"""
    pat = re.compile(r'result-' + re.escape(tid) + r'(?:-f\d+)?\.json$')
    cands = sorted(fn for fn in os.listdir(outbox) if pat.match(fn))
    if not cands:
        return None
    with open(os.path.join(outbox, cands[-1]), encoding='utf-8') as f:
        d = json.load(f)
    if d.get('status') != 'done':
        return False
    content = d.get('result') or d.get('output') or d.get('content') or ''
    if isinstance(content, str) and content.strip().startswith('{'):
        try:
            content = json.loads(content).get('text', content)
        except Exception:
            pass
    if not content or 'aborted' in content.lower():
        return False
    return content


TASK_TMPL = ('你是 MedXpert 知识库精读员，任务：L1 全库精读第 {idx} 份（自动重试 {n}）。请精读文件：\n'
             '{path}\n\n'
             '产出一份「理解摘要 + 疑点清单」，Markdown 格式，结构严格如下：\n'
             '## 核心内容（3 条）\n1. ...\n2. ...\n3. ...\n'
             '## 数据表格要点\n（列出文中关键表格的数据要点，无表格则写"本文无表格"）\n'
             '## 疑点清单（1-3 条）\n1. 疑点：...（说明为什么存疑）\n\n'
             '要求：忠实原文，不编造；数据引用原文数值；疑点必须是真实的困惑（如版本过时、'
             '链接失效、条款存疑），无疑点就写"暂无"。')


def retry(tid, attempt, names, inbox, hub):
    meta = names.get(tid)
    if not meta:
        print(f'[{now()}] [!] {tid} 无 names 映射，跳过重投', flush=True)
        return
    fpath = os.path.join(hub, meta.get('file', '')).replace('\\', '/')
    new_id = f'{tid}-f{attempt}'
    task = {
        'id': new_id, 'from': 'AI 助手平台', 'to': 'dsh', 'kind': 'execute',
        'title': f'L1精读-{meta.get("name", tid)}（自动重试 {attempt}）',
        'prompt': TASK_TMPL.format(idx=tid, n=attempt, path=fpath),
        'model': 'qwen3-local', 'status': 'pending',
        'createdAt': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H-%M-%S-000Z'),
        'retryOf': tid,
    }
    fn = f'task-{task["createdAt"]}-{new_id}.json'
    with open(os.path.join(inbox, fn), 'w', encoding='utf-8') as f:
        json.dump(task, f, ensure_ascii=False, indent=2)
    print(f'[{now()}] 重投 {tid} → {new_id}', flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--inbox', required=True)
    ap.add_argument('--outbox', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--hub', required=True)
    ap.add_argument('--names', required=True)
    ap.add_argument('--interval', type=int, default=60)
    ap.add_argument('--max-minutes', type=int, default=45)
    args = ap.parse_args()

    names = load_names(args.names)
    ensure_dir(args.outdir)
    deadline = time.time() + args.max_minutes * 60
    retry_count = {}
    target_ids = list(names.keys())

    if not target_ids:
        print('[!] names.json 为空，无任务可回收', flush=True)
        return 2

    while time.time() < deadline:
        done_ids, failed_ids = [], []
        for tid in target_ids:
            st = recover_one(args.outbox, tid)
            if st is None:
                continue
            elif st is False:
                failed_ids.append(tid)
            else:
                name = names[tid].get('name', tid)
                # 防路径穿越：name 来自外部 names.json，可能含 ../ 或绝对路径分隔符
                safe = re.sub(r'[\\/:*?"<>|\x00-\x1f]', '_', str(name)).replace('..', '_').strip(' .')
                if not safe:
                    safe = str(tid)
                target = os.path.join(args.outdir, f'{safe}_摘要.md')
                # 二次确认：解析后必须仍在 outdir 内（跨盘符时 commonpath 会抛 ValueError，按越界处理）
                try:
                    inside = os.path.commonpath([os.path.abspath(target), os.path.abspath(args.outdir)]) == os.path.abspath(args.outdir)
                except (ValueError, OSError):
                    inside = False
                if not inside:
                    print(f'[skip] 任务 {tid} 的输出名越出 outdir，已跳过：{name!r}', flush=True)
                    continue
                header = f'# {name} · L1 精读摘要\n\n> 生成：本地 qwen3-local · 任务 {tid}（状态 done）\n\n'
                with open(target, 'w', encoding='utf-8') as f:
                    f.write(header + (st if not st.startswith('#') else st))
                done_ids.append(tid)

        remaining = [t for t in target_ids if t not in done_ids]
        print(f'[{now()}] 进度: done={len(done_ids)}/{len(target_ids)} '
              f'剩余={len(remaining)} 失败={len(failed_ids)}', flush=True)
        if not remaining:
            print('ALL_DONE 全部回收完成', flush=True)
            return 0
        for tid in failed_ids:
            rc = retry_count.get(tid, 0)
            if rc < 3:
                retry_count[tid] = rc + 1
                retry(tid, rc + 1, names, args.inbox, args.hub)
            else:
                print(f'[{now()}] [!] {tid} 重试 3 次仍失败，留给人工', flush=True)
        time.sleep(args.interval)

    left = [t for t in target_ids if t not in done_ids]
    print('TIMEOUT 未在限时内完成，剩余:', left, flush=True)
    return 2


if __name__ == '__main__':
    sys.exit(main())

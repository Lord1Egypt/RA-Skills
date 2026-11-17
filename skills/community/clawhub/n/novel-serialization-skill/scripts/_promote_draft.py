# -*- coding: utf-8 -*-
"""
草稿 → 定稿（release）同步工具（CONTRIBUTING §9.1 第 5 步）

用法（在子项目根目录下执行，或显式给 --root）：
  python "../GitHub Novel Serialization Skill/scripts/_promote_draft.py" 031 047 036
  python "../GitHub Novel Serialization Skill/scripts/_promote_draft.py" 031 --dry-run   # 只看差异，不落盘
  python "../GitHub Novel Serialization Skill/scripts/_promote_draft.py" 031 --report .workbuddy/reports/xxx.md
  python "../GitHub Novel Serialization Skill/scripts/_promote_draft.py" 031 --root "C:/Users/Admin/-1928"
  python "../GitHub Novel Serialization Skill/scripts/_promote_draft.py" 031 --no-check  # 跳过 humanizer 自检（不推荐）
  python "../GitHub Novel Serialization Skill/scripts/_promote_draft.py" 031 --force     # humanizer 非 PASS 也强制同步

前提：草稿改动已通过审核（§9.1 第 1—4 步）。未过审的改动不得进定稿。

说明：脚本存放于技能仓库 scripts/（多子项目共用），项目根默认取当前工作目录，
      须为含 chapters/ 与 notes-personal/ 的子项目根目录。
"""
import re, sys, os, glob, subprocess, argparse, datetime, shutil

sys.stdout.reconfigure(encoding='utf-8')

# 脚本自身目录（技能仓库 scripts/）——humanizer 与本脚本同目录，随仓库一起分发
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HUMANIZER = os.path.join(SCRIPT_DIR, 'humanizer_check.py')

DRAFT_DEFAULT = 'notes-personal/正文草稿.md'


def cn(t):
    return len(re.findall(r'[\u4e00-\u9fff]',
        '\n'.join(l for l in t.split('\n') if not l.startswith('>') and not l.startswith('##'))))


def chapter_index():
    idx = {}
    for p in glob.glob('chapters/**/*.md', recursive=True):
        m = re.search(r'第(\d+)章', os.path.basename(p))
        if m:
            idx[str(int(m.group(1)))] = p
    return idx


def blocks(draft_text):
    """返回 {章号: (标题, 正文块文本)}"""
    lines = draft_text.split('\n')
    heads = [(i, l) for i, l in enumerate(lines) if re.match(r'^## 第\d+章', l)]
    out = {}
    for k, (i, l) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        m = re.match(r'^## 第(\d+)章 (.+)$', l)
        out[str(int(m.group(1)))] = (l, '\n'.join(lines[i:end]).strip('\n'))
    return out


def humanizer_pass(path):
    r = subprocess.run([sys.executable, HUMANIZER, path],
                       capture_output=True, text=True, encoding='utf-8')
    out = r.stdout or ''
    m = re.search(re.escape(os.path.basename(path)) + r'.*?\*\*(PASS|WARN|FAIL)\*\*', out, re.S)
    return (m.group(1) if m else 'UNKNOWN'), out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('nums', nargs='*', help='章号，如 031 047；不给则同步全部有差异的章')
    ap.add_argument('--draft', default=DRAFT_DEFAULT)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--report', default='', help='审核报告路径（记入同步日志）')
    ap.add_argument('--no-check', action='store_true')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--root', default='', help='子项目根目录（默认当前工作目录，须含 chapters/ 与 notes-personal/）')
    a = ap.parse_args()

    root = os.path.abspath(a.root) if a.root else os.getcwd()
    if not os.path.isdir(os.path.join(root, 'chapters')):
        print('根目录异常（未找到 chapters/）：%s' % root)
        print('请在子项目根目录执行，或用 --root 指定（如 --root "C:/Users/Admin/-1928"）。')
        return 1
    os.chdir(root)
    print('项目根：', root)

    if not os.path.exists(a.draft):
        print('草稿不存在：', a.draft); return 1
    dtext = open(a.draft, encoding='utf-8').read()
    dblocks = blocks(dtext)
    idx = chapter_index()

    nums = [str(int(n)) for n in a.nums] if a.nums else sorted(dblocks, key=lambda x: int(x))

    # 自检
    if not a.no_check:
        verdict, _ = humanizer_pass(a.draft)
        print('humanizer 自检（草稿）:', verdict)
        if verdict == 'FAIL' and not a.force:
            print('草稿未通过自检，拒绝同步定稿。改完再跑，或用 --force（不推荐）。'); return 2

    today = datetime.date.today().isoformat()
    snap_dir = os.path.join('_trash', '定稿同步前_%s' % today)
    todo = []
    for n in nums:
        if n not in dblocks:
            print('草稿中无 第%s章' % n); continue
        if n not in idx:
            print('chapters/ 中无 第%s章' % n); continue
        cur = open(idx[n], encoding='utf-8').read()
        new = dblocks[n][1] + '\n'
        if cur.strip('\n') == new.strip('\n'):
            print('第%s章 无差异，跳过' % n); continue
        todo.append((n, idx[n], cur, new))

    if not todo:
        print('没有需要同步的章节。'); return 0

    for n, p, cur, new in todo:
        print('第%s章 %s：%d -> %d 字' % (n, os.path.basename(p), cn(cur), cn(new)))

    if a.dry_run:
        print('--dry-run：未写入'); return 0

    os.makedirs(snap_dir, exist_ok=True)
    log = []
    for n, p, cur, new in todo:
        shutil.copy2(p, os.path.join(snap_dir, os.path.basename(p)))
        open(p, 'w', encoding='utf-8').write(new)
        log.append('- 第%s章：%d → %d 字（快照 %s）' % (n, cn(cur), cn(new), snap_dir))
        print('已同步 第%s章' % n)

    # 校验标题零差异
    dtitles = {k: v[0] for k, v in dblocks.items()}
    ctitles = {}
    for k, p in idx.items():
        m = re.search(r'^## 第(\d+)章 (.+)$', open(p, encoding='utf-8').read(), re.M)
        if m: ctitles[str(int(m.group(1)))] = '## 第%s章 %s' % (int(m.group(1)), m.group(2))
    diff = [k for k in dtitles if k in ctitles and dtitles[k] != ctitles[k]]
    print('章标题差异：', diff or '0（一致）')

    logpath = os.path.join(snap_dir, '_同步日志.md')
    with open(logpath, 'a', encoding='utf-8') as f:
        f.write('\n## %s 草稿→定稿同步（%s）\n' % (today, datetime.datetime.now().strftime('%H:%M')))
        f.write('- 草稿：%s\n- 审核报告：%s\n' % (a.draft, a.report or '（未填写）'))
        f.write('\n'.join(log) + '\n')
    print('同步日志：', logpath)
    return 0


if __name__ == '__main__':
    sys.exit(main())

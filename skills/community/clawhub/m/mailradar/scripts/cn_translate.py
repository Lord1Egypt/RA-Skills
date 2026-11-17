# -*- coding: utf-8 -*-
"""中文翻译层辅助脚本：把「待译邮件清单」交给 LLM，再把译文写回 workboard2_cn.json。

用法：
  python cn_translate.py                 # 导出 cn_inbox.json 待译清单（精简、供 LLM 翻译）
  python cn_translate.py --full          # 导出 cn_inbox_full.json 全量清单（含其他待办/西葡）
  python cn_translate.py --apply 译文.json  # 校验并合并 LLM 译文 → workboard2_cn.json
  python cn_translate.py --show          # 打印当前 workboard2_cn.json 概况

数据流（由 daily_mail_board.py 自动跑前两步）：
  prep_cn.py          → cn_inbox_full.json   （全量线程 + 清洗正文）
  build_cn_inbox.py   → cn_inbox.json        （每店筛选「含 DDL 或近 14 天活跃」，上限 6）
  LLM 翻译            → workboard2_cn.json   （本脚本 --apply 写入）
"""
import json, os, sys

WS = os.path.dirname(os.path.abspath(__file__))

def load(name, default=None):
    p = os.path.join(WS, name)
    if not os.path.exists(p):
        return default
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def dump_items(items, stream):
    """把一批条目打成紧凑、便于 LLM 阅读的结构（thread_id + 主题 + 正文摘要 + 待办）。"""
    for t in items:
        stream.write('---\n')
        stream.write('thread_id: %s\n' % (t.get('thread_id') or t.get('id') or ''))
        stream.write('subject: %s\n' % (t.get('subject') or ''))
        if t.get('responsible'):
            stream.write('responsible: %s\n' % t.get('responsible'))
        if t.get('ddl'):
            stream.write('ddl: %s\n' % (json.dumps(t.get('ddl'), ensure_ascii=False)))
        if t.get('todos'):
            stream.write('todos(原): %s\n' % (json.dumps(t.get('todos'), ensure_ascii=False)))
        if t.get('fresh'):
            stream.write('正文片段: %s\n' % t.get('fresh'))
    stream.write('\n')


def cmd_dump(full=False):
    src = 'cn_inbox_full.json' if full else 'cn_inbox.json'
    data = load(src)
    if not data:
        print('未找到 %s —— 请先运行 prep_cn.py 与 build_cn_inbox.py' % src)
        sys.exit(1)
    print('=== 待译邮件清单（%s）===' % src)
    print('规则：每线程输出 3 字段 —— summary(邮件沟通事项中文归纳) / todos(待办列表) / risk(风险)。')
    print('删问候/落款；仅展示发件人+收件人(抄送不显示)；方向语义 A→B 说「我要休假」=A 休假。')
    print('')
    stores = data.get('stores', {})
    for sk, sv in stores.items():
        items = sv.get('items', []) if isinstance(sv, dict) else []
        if not items:
            continue
        print('### 门店 %s（%s）%d 条' % (sk, sv.get('label', ''), len(items)))
        dump_items(items, sys.stdout)
    if full:
        ot = data.get('other_todos', [])
        if ot:
            print('### 其他待办 %d 条' % len(ot))
            dump_items(ot, sys.stdout)
        ib = data.get('iberia', {})
        ib_items = ib.get('items', []) if isinstance(ib, dict) else []
        if ib_items:
            print('### 西葡非建店 %d 条' % len(ib_items))
            dump_items(ib_items, sys.stdout)


def validate_entry(e, path):
    if not isinstance(e, dict):
        raise ValueError('%s 不是对象' % path)
    if 'summary' in e and not isinstance(e.get('summary'), str):
        raise ValueError('%s.summary 应为字符串' % path)
    if 'todos' in e and not isinstance(e.get('todos'), list):
        raise ValueError('%s.todos 应为数组' % path)
    if 'risk' in e and not isinstance(e.get('risk'), str):
        raise ValueError('%s.risk 应为字符串' % path)


def cmd_apply(translated_path):
    if not os.path.exists(translated_path):
        print('译文文件不存在：%s' % translated_path)
        sys.exit(1)
    tr = json.load(open(translated_path, encoding='utf-8'))
    if not isinstance(tr, dict):
        print('译文根节点应为对象（含 stores 键）')
        sys.exit(1)
    # 校验 stores
    stores = tr.get('stores', {})
    if not isinstance(stores, dict):
        print('译文缺少合法的 stores 对象')
        sys.exit(1)
    n = 0
    for sk, threads in stores.items():
        if not isinstance(threads, dict):
            raise ValueError('stores.%s 应为 {thread_id: {summary,todos,risk}}' % sk)
        for tid, e in threads.items():
            validate_entry(e, 'stores.%s.%s' % (sk, tid))
            n += 1
    # 其他模块（可选）
    for key in ('other_todos', 'iberia'):
        if key in tr and tr[key] is not None:
            if not isinstance(tr[key], dict):
                raise ValueError('%s 应为对象' % key)
            for tid, e in tr[key].items():
                validate_entry(e, '%s.%s' % (key, tid))
    # 合并进 workboard2_cn.json（保留已有译文，避免重复劳动）
    existing = load('workboard2_cn.json', {'stores': {}, 'other_todos': {}, 'iberia': {}})
    merged = {
        'stores': existing.get('stores', {}),
        'other_todos': existing.get('other_todos', {}),
        'iberia': existing.get('iberia', {}),
    }
    for key in merged:
        if isinstance(tr.get(key), dict):
            merged[key].update(tr[key])
    out = os.path.join(WS, 'workboard2_cn.json')
    json.dump(merged, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('已写入 %s：本次新增/更新 %d 条译文，合计 stores=%d' % (
        out, n, len(merged['stores'])))


def cmd_show():
    cn = load('workboard2_cn.json')
    if not cn:
        print('尚无 workboard2_cn.json（未翻译）')
        return
    stores = cn.get('stores', {})
    print('workboard2_cn.json 概况：')
    for sk, threads in stores.items():
        print('  %s: %d 条' % (sk, len(threads) if isinstance(threads, dict) else 0))
    print('  other_todos: %d | iberia: %d' % (
        len(cn.get('other_todos', {}) or {}), len(cn.get('iberia', {}) or {})))


def main():
    args = sys.argv[1:]
    if '--apply' in args:
        i = args.index('--apply')
        cmd_apply(args[i + 1] if i + 1 < len(args) else 'translated.json')
    elif '--show' in args:
        cmd_show()
    else:
        cmd_dump(full='--full' in args)


if __name__ == '__main__':
    main()

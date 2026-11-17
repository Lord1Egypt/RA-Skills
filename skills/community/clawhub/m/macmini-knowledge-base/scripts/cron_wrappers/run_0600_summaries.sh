#!/bin/bash
# 06:00 文档摘要 —— 确定性推送（command 型，不占模型配额）
#
# 设计要点（2026-11-06 重写）：
#  1. **按预算截断**：飞书单条消息上限约 30KB → 硬预算 24KB，超出即停。
#  2. **只归档真正进入本次摘要的文件**：未进入的留在 summaries/ 下轮次继续。
#     旧版把全部文件都 move 到 archives/，一旦超限推送失败 → 内容静默丢失。
#  3. **研报给正文摘录，其余按「源文档一级目录」汇总** —— 114 份工程表单
#     逐条列标题是噪音，汇总成几行才有信息量。
#  4. **分组键必须来自源文档，不能来自摘要文件名** —— 摘要全部平铺在
#     summaries/ 根目录，按摘要文件名分组会退化成逐份列举。
#     回退顺序：summary_index → 摘要正文 source_path/路径： → 其他
#  5. **字符级安全截断** —— `cut -c` 按字节切会切断中文。
#  6. macOS 自带 bash 3.2 → 无 mapfile / readarray / 关联数组。
#
# 环境变量：
#   DRY_RUN=1      只渲染不移动
#   BUDGET_BYTES   覆盖单条消息字节预算（默认 24000）
set -uo pipefail
WS=/Users/home/.openclaw/workspace
S="$WS/knowledge/.analysis/summaries"
A="$S/archives"
DRY="${DRY_RUN:-0}"
BUDGET="${BUDGET_BYTES:-24000}"

MANIFEST="$(mktemp)"; DIGEST="$(mktemp)"
trap 'rm -f "$MANIFEST" "$DIGEST"' EXIT

python3 - "$S" "$BUDGET" "$DIGEST" "$MANIFEST" "$WS/knowledge/.analysis/summary_index.json" <<'PYEOF'
import os, sys, re, json, collections, datetime
S, budget, digest_p, manifest_p, index_p = sys.argv[1:6]
budget = int(budget)
# 研报判定（三重，任一命中即算「研报」→ 给正文摘录而非仅计数）：
#   ① 文件名含券商/研报关键词
#   ② 源目录是 Macro Financials（AGENTS.md 声明的投行研报目录）
#   ③ 摘要正文含研报/政策研究特征
# 2026-11-06 修：原先只按文件名匹配 → 「20261102-扩大内需的七个认知困境.pdf」
#   （政策建议季度报告 第69期，正文 24K 字）文件名无关键词 → 被降级成一行计数，正文永远送不到
RESEARCH_NAME = re.compile(r'(高盛|Goldman|摩根士丹利|Morgan|野村|Nomura|摩根大通|JPMorgan|J\.P\.|花旗|CITI|Citi|巴克莱|Barclays|UBS|瑞银|BofA|美银|Jefferies|伯恩斯坦|Bernstein|汇丰|HSBC|德意志|Deutsche|宏观|研报|证券)')
RESEARCH_DIRS = ('Macro Financials',)
RESEARCH_BODY = re.compile(r'(政策建议季度报告|证券研究报告|证券研究|研究团队|投资评级|目标价|行业研究|宏观研究|专题报告)')
TS = re.compile(r'^\d{8}_\d{6}_')
HASH = re.compile(r'^[0-9a-f]{8}_')

def display(fn):
    b = os.path.basename(fn)[:-len('.summary.txt')]
    return HASH.sub('', TS.sub('', b))

def source_dir(fn):
    """推断源文档所在的一级目录（分组键）。

    顺序：summary_index（权威）→ 摘要正文 source_path/路径：→ None
    """
    bn = os.path.basename(fn)
    try:
        idx = json.load(open(index_p, encoding='utf-8'))
    except Exception:
        idx = {}
    rel = idx.get(bn)
    if not rel:
        try:
            with open(os.path.join(S, fn), encoding='utf-8', errors='replace') as fh:
                head = fh.read(2000)
            m = re.search(r'source_path:\s*"([^"]+)"', head) or re.search(r'路径：\s*(\S.*)', head)
            if m:
                rel = m.group(1).strip().strip('"')
        except OSError:
            rel = None
    if not rel:
        return None
    rel = rel.replace('\\', '/').lstrip('/')
    parts = [p for p in rel.split('/') if p]
    return parts[0] if len(parts) > 1 else None

def is_research(disp, src_dir, head):
    """三重判定：文件名关键词 / 源目录 / 正文特征。任一命中即算研报。"""
    if RESEARCH_NAME.search(disp):
        return True
    if src_dir in RESEARCH_DIRS:
        return True
    return bool(RESEARCH_BODY.search(head))


def head_text(fn, nchars=4000):
    path = fn if os.path.isabs(fn) else os.path.join(S, fn)
    try:
        with open(path, encoding='utf-8', errors='replace') as fh:
            return fh.read(nchars)
    except OSError:
        return ''


def body(fn, n=12):
    path = fn if os.path.isabs(fn) else os.path.join(S, fn)
    try:
        with open(path, encoding='utf-8', errors='replace') as fh:
            lines = [l for l in fh.read().split('\n') if l.strip()]
    except OSError:
        return ''
    skip = re.compile(r'^\s*$|@[a-z]+\.com|Securities \(Asia|Broking \(Hong')
    return '\n'.join([l for l in lines if not skip.match(l)][:n])

files = sorted(f for f in os.listdir(S) if f.endswith('.summary.txt'))
if not files:
    open(digest_p, 'w', encoding='utf-8').write('今天没有新文档')
    open(manifest_p, 'w', encoding='utf-8').close()
    sys.exit(0)

research, bulk = [], []
for f in files:
    disp = display(f)
    src = source_dir(f)
    h = head_text(f)
    if is_research(disp, src, h):
        research.append((f, disp))
    else:
        bulk.append((f, src))

out = []
used = 0
def add(block):
    global used
    b = block.encode('utf-8')
    if used + len(b) > budget:
        return False
    out.append(block); used += len(b)
    return True

head = (f"📄 文档摘要 · {datetime.datetime.now().strftime('%Y-%m-%d')}\n"
        f"共 {len(files)} 份待推送\n\n")
used = len(head.encode('utf-8'))
out.append(head)

included = []
for f, disp in research:
    nm = disp
    if len(nm) > 90:
        nm = nm[:88] + '…'
    if not add(f"── {nm}\n{body(f)}\n\n"):
        break
    included.append(f)

cnt = collections.Counter()
for f, src in bulk:
    cnt[src or '其他'] += 1
if cnt:
    blk = "以下文档已生成摘要（按源目录汇总，完整内容见 archives/）：\n"
    for k, v in sorted(cnt.items(), key=lambda x: (-x[1], x[0])):
        blk += f"· {k}：{v} 份\n"
    blk += "\n"
    if add(blk):
        included.extend(bulk)

open(digest_p, 'w', encoding='utf-8').write(''.join(out))
with open(manifest_p, 'w', encoding='utf-8') as fh:
    for f in included:
        fh.write(os.path.join(S, f) + '\n')
PYEOF
rc=$?
if [ $rc -ne 0 ]; then
  echo "摘要渲染失败（exit=$rc）"
  exit 1
fi

cat "$DIGEST"

if [ "$DRY" != "1" ]; then
  mkdir -p "$A"
  n=0
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    mv "$f" "$A/" 2>/dev/null && n=$((n+1))
  done < "$MANIFEST"
  LEFT=$(find "$S" -maxdepth 1 -name '*.summary.txt' 2>/dev/null | wc -l | tr -d ' ')
  printf '\n已推送并归档 %s 份 → archives/；剩余 %s 份留待下次\n' "$n" "$LEFT"
fi

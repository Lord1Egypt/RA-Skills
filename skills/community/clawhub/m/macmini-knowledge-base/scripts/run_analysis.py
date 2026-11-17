#!/usr/bin/env python3
"""
知识库文档分析脚本 - v2.0（kreuzberg 统一提取层 + antiword .doc 极速提取）
BATCH_SIZE=100，每批超时280秒，增量断点续传
"""
import os
import re
import json
import glob
import sys
import time
import hashlib
from datetime import datetime
from knowledge_policy import scan_files, scan_roots
from utils import (
    load_state, save_state,
    rel_key, STATE_SCHEMA_VERSION,
    load_summary_index, save_summary_index,
    extract_pdf_text, extract_doc_text, extract_docx_text,
    extract_xlsx_text, extract_pptx_text, extract_via_kreuzberg,
    convert_old_office, is_gibberish,
    clean_noise, MAX_EXTRACT_LEN
)

# macOS NAME_MAX = 255 bytes；Linux NAME_MAX 通常 255 bytes
# 保留 200 bytes 限额给 summary 文件名（实测 ASCII < 200 bytes 安全）
SUMMARY_NAME_MAX = 200

def sanitize_filename(name, max_length=SUMMARY_NAME_MAX):
    """防止 OSError [Errno 63] File name too long
    
    策略：
      1. 保留扩展名
      2. 超长文件名截断 + 加 8 位 MD5 hash 防冲突
      3. 处理 UTF-8 编码（不切碎字符）
    
    Args:
        name: 原始文件名
        max_length: 字节长度上限（默认 200）
    
    Returns:
        截断后的安全文件名
    """
    if not name:
        return name
    
    name_bytes = name.encode('utf-8')
    if len(name_bytes) <= max_length:
        return name
    
    # 分离扩展名（基于原始字符串）
    base, ext = os.path.splitext(name)
    ext_bytes = ext.encode('utf-8')
    base_bytes = base.encode('utf-8')
    
    # 加 8 位 hash 标识
    import hashlib
    h = hashlib.md5(name_bytes).hexdigest()[:8]
    
    # 截断 base_bytes，留出 ext + "_" + 8 hash 的空间
    reserve = len(ext_bytes) + 1 + 8  # "_" + hash + ext
    available = max_length - reserve
    
    if available > 0 and len(base_bytes) > available:
        # 安全截断（按 bytes 截断后 decode，errors='ignore' 切碎字符也无所谓）
        truncated = base_bytes[:available].decode('utf-8', errors='ignore')
        return f"{truncated}_{h}{ext}"
    
    # 兜底：极端情况（扩展名本身就超长）
    return name[:max_length]

KNOWLEDGE_DIR = os.path.expanduser("~/.openclaw/workspace/knowledge")
STATE_FILE = os.path.join(KNOWLEDGE_DIR, ".analysis/analysis_state.json")
SUMMARY_DIR = os.path.join(KNOWLEDGE_DIR, ".analysis/summaries")
BATCH_SIZE = 100
BATCH_TIMEOUT = 280

os.makedirs(SUMMARY_DIR, exist_ok=True)

def get_all_files():
    """扫描知识库中**允许进入分析**的文件。

    扫描范围在 glob 层按目录白名单限定（见 knowledge_policy.py）：
    白名单 = AGENTS.md 声明的 knowledge/ 合法结构 8 个目录。
    白名单之外的目录（包括未来新增的任何文件夹）根本不会被遍历，
    因此新增文件夹**不会**污染分析队列 —— 这是结构性保证，不靠事后过滤。
    """
    return scan_files(KNOWLEDGE_DIR)


def scan_policy_report():
    """报告扫描范围：白名单目录命中数 + 未纳入白名单的目录（用于诊断误入）。"""
    report = {"scanned": {}, "excluded_dirs": {}}
    for root in scan_roots(KNOWLEDGE_DIR):
        n = 0
        for dp, dn, fn in os.walk(root):
            n += len(fn)
        report["scanned"][os.path.basename(root)] = n
    for d in sorted(os.listdir(KNOWLEDGE_DIR)):
        p = os.path.join(KNOWLEDGE_DIR, d)
        if os.path.isdir(p) and d not in report["scanned"]:
            n = sum(len(fn) for _, _, fn in os.walk(p))
            report["excluded_dirs"][d] = n
    return report



def retry_with_backoff(func, *args, max_retries=2, initial_delay=1.0, **kwargs):
    """简单重试：max_retries=2，总共 3 次尝试
    
    退避策略：1s, 2s（指数）
    """
    last_err = None
    for attempt in range(max_retries + 1):
        try:
            result = func(*args, **kwargs)
            if result and not (isinstance(result, str) and result.startswith("【")):
                return result
            last_err = f"返回空或错误标记: {result[:100] if result else 'None'}"
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
        if attempt < max_retries:
            delay = initial_delay * (2 ** attempt)
            print(f"  ↻ 重试 {attempt+1}/{max_retries} ({delay}s) ...")
            time.sleep(delay)
    return f"【重试{max_retries+1}次仍失败】{last_err}"

def analyze_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == ".pdf":
            return retry_with_backoff(extract_pdf_text, filepath, max_retries=2)
        elif ext == ".doc":
            return extract_doc_text(filepath)
        elif ext == ".docx":
            return extract_docx_text(filepath)
        elif ext == ".xls":
            success, converted = convert_old_office(filepath, ext)
            if success:
                try:
                    return extract_xlsx_text(converted)
                finally:
                    try:
                        os.remove(converted)
                    except OSError as e:
                        # 临时文件清理失败：记录以便排查残留（不再静默吞掉）
                        print(f"[临时文件清理失败] {converted}: {e}", file=sys.stderr)
            return "【XLS转换失败】"
        elif ext == ".xlsx":
            return extract_xlsx_text(filepath)
        elif ext == ".ppt":
            success, converted = convert_old_office(filepath, ext)
            if success:
                try:
                    return extract_pptx_text(converted)
                finally:
                    try:
                        os.remove(converted)
                    except OSError as e:
                        # 临时文件清理失败：记录以便排查残留（不再静默吞掉）
                        print(f"[临时文件清理失败] {converted}: {e}", file=sys.stderr)
            return "【PPT转换失败】"
        elif ext == ".pptx":
            return extract_pptx_text(filepath)
        elif ext == ".md":
            text = extract_via_kreuzberg(filepath)
            if not text:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()[:MAX_EXTRACT_LEN]
            return clean_noise(text)
        else:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()[:MAX_EXTRACT_LEN]
    except Exception as e:
        return f"【分析失败】{str(e)}"

# ── P0 修复（2026-11-05）────────────────────────────────────────────
# 原缺陷：analyze_file() 失败时返回带【...失败】标记的字符串，主循环
#   不做校验，照样写摘要文件 + analyzed_files.append() → 单文件失败被
#   永久记为"已分析"，下游自动化把错误文本当成完成的摘要（持续遗漏）。
# 现在：失败 → 不写摘要、不入 analyzed_files、留在可重试队列；
#       连续失败达 MAX_RETRIES 次 → 隔离，停止自动重试（防无限重试）。
MAX_RETRIES = 3

# 提取失败的判定：任何以【...失败...】开头的文本即视为真失败
FAILURE_RE = re.compile(r'^\u3010[^\u3011]*\u5931\u8d25[^\u3011]*\u3011')
# 空内容标记属于"合法但无信息"，仍算完成（避免队列被空文件反复占用）
EMPTY_MARKERS = ("\u3010Word\u6587\u6863\u65e0\u6587\u5b57\u5185\u5bb9\u3011",
                 "\u3010Excel\u65e0\u5185\u5bb9\u3011",
                 "\u3010PPT\u65e0\u6587\u5b57\u5185\u5bb9\u3011")


def classify_result(content):
    """把提取结果分类为 (ok, reason)。

    ok=False → 真失败（异常 / 提取失败）：不写摘要、不入 analyzed_files、
               保留在重试队列，下一轮再试。
    ok=True  → 正常完成（空内容标记也算完成，但会记警告）。
    """
    if content is None:
        return False, "提取结果为 None"
    text = str(content).strip()
    if FAILURE_RE.match(text):
        return False, text[:200]
    if text and text in EMPTY_MARKERS:
        return True, "空内容标记（合法但无信息）"
    return True, ""


# ── 状态 schema 迁移（v1 basename → v2 相对路径）────────────────────
def _archives_dir():
    return os.path.join(KNOWLEDGE_DIR, ".analysis/summaries/archives")


def _summary_source_hints(basename):
    """从 archives 摘要里找出该 basename 的源路径线索。

    摘要正文两种格式都带源路径：
      旧格式  路径：房产效能专家/03.00管理培训课      （仅前两级目录）
      新格式  source_path: "完整相对路径"            （可精确到文件）
    返回线索集合（可能为空）。
    """
    hints = set()
    d = _archives_dir()
    if not os.path.isdir(d):
        return hints
    for fn in os.listdir(d):
        if not fn.endswith(".summary.txt"):
            continue
        base = re.sub(r"^\d{8}_\d{6}_", "", fn)
        base = re.sub(r"^[0-9a-f]{8}_", "", base)      # 新格式的路径哈希
        base = base[:-len(".summary.txt")]
        if base != basename:
            continue
        try:
            with open(os.path.join(d, fn), encoding="utf-8", errors="replace") as fh:
                head = fh.read(2000)
        except OSError:
            continue
        m = re.search(r"source_path:\s*\"([^\"]+)\"", head)
        if not m:
            m = re.search(r"路径：\s*(\S.*)", head)
        if m:
            hints.add(m.group(1).strip().strip('"'))
    return hints


def _tail_match_candidates(hint, cands, tail=3):
    """用路径尾部匹配定位候选。

    历史摘要里的源路径可能带**旧目录结构**（如 03房地产开发/ → 现 房产效能专家/），
    也可能是绝对路径 → 精确前缀匹配会全部落空。
    改为比较路径最后 N 段：目录改名只影响前缀，尾部仍然稳定。
    """
    h = hint.strip().strip('"')
    # 去掉 KNOWLEDGE 前缀（历史路径可能是绝对路径）
    kd = KNOWLEDGE_DIR.rstrip(os.sep)
    if h.startswith(kd):
        h = h[len(kd):]
    h = h.lstrip(os.sep)
    h_parts = [p for p in h.split(os.sep) if p]
    if not h_parts:
        return []
    ht = os.sep.join(h_parts[-tail:])
    hits = []
    for c in cands:
        rp = rel_key(c).split(os.sep)
        if len(rp) >= tail and os.sep.join(rp[-tail:]) == ht:
            hits.append(c)
    return hits


def migrate_state_schema(state, all_files):
    """把 v1（basename 键）迁移到 v2（相对路径键）。幂等。

    消歧规则：
      1 个候选            → 直接映射
      多个候选 + 摘要能唯一确定源 → 映射到真正产出过摘要的那一份
      多个候选 + 消歧不出 → **一个都不标记** → 该组全部重新分析
        （宁可多跑一次，也不让文档永久缺摘要）
    """
    by_basename = {}
    for f in all_files:
        by_basename.setdefault(os.path.basename(f), []).append(f)

    old_analyzed = list(state.get("analyzed_files", []))
    new_analyzed = []
    direct = ambiguous_resolved = ambiguous_unresolved = 0
    lost = 0
    report = []

    for bn in old_analyzed:
        cands = by_basename.get(bn, [])
        if not cands:
            lost += 1
            continue
        if len(cands) == 1:
            new_analyzed.append(rel_key(cands[0]))
            direct += 1
            continue
        # 多候选 → 用摘要源路径线索消歧
        hints = _summary_source_hints(bn)
        picked = None
        for h in hints:
            # 精确匹配优先
            hits = [c for c in cands
                    if rel_key(c) == h or rel_key(c).startswith(h + os.sep)]
            if len(hits) == 1:
                picked = hits[0]
                break
            # 退回尾部匹配（应对旧目录结构 / 绝对路径）
            for t in (4, 3, 2):
                hits = _tail_match_candidates(h, cands, tail=t)
                if len(hits) == 1:
                    picked = hits[0]
                    break
                if len(hits) > 1:
                    break
            if picked:
                break
        if picked:
            new_analyzed.append(rel_key(picked))
            ambiguous_resolved += 1
        else:
            # 消歧不出 → 该组全部不标记（会重新分析）
            ambiguous_unresolved += 1
            report.append(bn)

    # pending / failed / quarantined 同步迁移（当前多为空，但代码要正确）
    def remap(names):
        out = []
        for n in names:
            cands = by_basename.get(n, [])
            if len(cands) == 1:
                out.append(rel_key(cands[0]))
            elif cands:
                out.extend(rel_key(c) for c in cands)
        return out

    state["pending_files"] = remap(state.get("pending_files", []))
    state["quarantined_files"] = remap(state.get("quarantined_files", []))
    failed_map = {}
    for bn, rec in (state.get("failed_files") or {}).items():
        for k in remap([bn]):
            failed_map[k] = rec
    state["failed_files"] = failed_map

    # summaries 里的 filename 也改成相对路径
    for sm in state.get("summaries", []) or []:
        if sm.get("filepath"):
            sm["filename"] = rel_key(sm["filepath"])

    state["analyzed_files"] = new_analyzed
    state["schema_version"] = STATE_SCHEMA_VERSION

    print(f"[MIGRATE] schema v1 → v2（basename → 相对路径）")
    print(f"  唯一映射        : {direct}")
    print(f"  摘要消歧成功    : {ambiguous_resolved}")
    print(f"  消歧不出→重新分析: {ambiguous_unresolved} 组")
    print(f"  原件已不存在    : {lost}")
    if report:
        print(f"  待重新分析的同名组: {', '.join(report[:8])}"
              + (" ..." if len(report) > 8 else ""))
    return state


def main():
    state = load_state()
    all_files = get_all_files()
    summary_index = load_summary_index()

    # ── schema 迁移（幂等）────────────────────────────────────────
    # v1 用 basename 做键 → 同名文件互相顶替，一份被永久静默跳过。
    # 读到旧版自动迁移，避免恢复旧备份后全量重跑。
    if int(state.get("schema_version", 1)) < STATE_SCHEMA_VERSION:
        state = migrate_state_schema(state, all_files)
        save_state(state)

    analyzed_set = set(state.get("analyzed_files", []))
    failed_map = state.setdefault("failed_files", {})
    quarantined = set(state.get("quarantined_files", []))

    # ── 队列重建 ────────────────────────────────────────────────────
    # 原缺陷：队列只在 state["pending_files"] 为空时才重建，此后一直靠
    #   pending[:100] 消费 / pending[100:] 递减 → 磁盘上新到的文件
    #   永远进不了队列（实测 5 份新研报因此永远不会被处理）。
    # 现在：每次运行都按全量扫描重建，并与旧队列中仍未处理的部分合并
    #       （旧队列在前 → 保持处理连续性；新文件追加在后）。
    # 队列键 = 相对 knowledge/ 的路径（唯一标识每个文件）
    on_disk = []
    seen = set()
    for f in all_files:
        k = rel_key(f)
        if k not in seen:
            seen.add(k)
            on_disk.append(k)

    old_pending = [n for n in state.get("pending_files", [])
                   if n not in analyzed_set and n not in quarantined and n in seen]
    fresh_pending = [n for n in on_disk
                     if n not in analyzed_set and n not in quarantined]
    pending_names = list(dict.fromkeys(old_pending + fresh_pending))

    if not pending_names:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 没有新文件需要分析")
        # 仍输出 [STATS]：队列为空是正常状态，不是异常。
        # 23:00 cron 的 wrapper 依赖这一行判断健康度，缺失会被误报为「脚本崩溃」。
        print(f"[STATS] success=0 failure=0 queue=0")
        return

    state["pending_files"] = pending_names
    save_state(state)

    batch_names = pending_names[:BATCH_SIZE]
    remaining_names = pending_names[BATCH_SIZE:]

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 待处理队列：{len(pending_names)} 个文件")
    print(f"本批处理：{len(batch_names)} 个，剩余：{len(remaining_names)} 个")

    batch_start = time.time()
    summaries = []
    failed_this_batch = []
    handled = set()
    ok_count = 0
    fail_count = 0

    for filename in batch_names:
        file_start = time.time()
        # filename 现在是相对路径 → 精确还原绝对路径，无需"猜"第一个候选
        filepath = os.path.join(KNOWLEDGE_DIR, filename)
        if not os.path.isfile(filepath):
            print(f"  ⚠️  文件不存在，跳过：{filename}")
            handled.add(filename)
            continue

        print(f"  分析中: {filename}")
        content = analyze_file(filepath)
        ok, reason = classify_result(content)

        if not ok:
            # ── 失败：不写摘要、不入 analyzed_files、留队列重试 ──
            fail_count += 1
            handled.add(filename)
            rec = failed_map.get(filename) or {}
            rec["count"] = int(rec.get("count", 0)) + 1
            rec["last_error"] = reason
            rec["last_at"] = datetime.now().isoformat()
            failed_map[filename] = rec
            failed_this_batch.append(filename)
            print(f"    ❌ 提取失败（累计 {rec['count']}/{MAX_RETRIES}）：{reason[:100]}")
            print(f"    ⚠️  不写入 analyzed_files，保留在重试队列", file=sys.stderr)

            if rec["count"] >= MAX_RETRIES:
                quarantined.add(filename)
                if filename not in state.setdefault("quarantined_files", []):
                    state["quarantined_files"].append(filename)
                print(f"    🔒 连续失败达 {MAX_RETRIES} 次 → 隔离，停止自动重试")
        else:
            # ── 成功：写摘要 + 记入 analyzed_files ──
            ok_count += 1
            handled.add(filename)
            failed_map.pop(filename, None)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # 路径哈希：同名文档可能在同一秒被处理 → 仅靠时间戳会互相覆盖
            path_hash = hashlib.md5(filename.encode('utf-8')).hexdigest()[:8]
            safe_filename = sanitize_filename(os.path.basename(filename))
            summary_file = os.path.join(
                SUMMARY_DIR,
                f"{timestamp}_{path_hash}_{safe_filename}.summary.txt"
            )
            try:
                with open(summary_file, 'w', encoding='utf-8') as f:
                    f.write(content)
            except OSError as e:
                if e.errno == 63:  # ENAMETOOLONG（File name too long）
                    short_name = sanitize_filename(os.path.basename(filename), max_length=180)
                    summary_file = os.path.join(
                        SUMMARY_DIR,
                        f"{timestamp}_{path_hash}_{short_name}.summary.txt"
                    )
                    with open(summary_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"    ⚠️  文件名过长已截断: {short_name[:60]}...")
                else:
                    raise

            summaries.append({
                "filename": filename,
                "filepath": filepath,
                "summary_file": summary_file,
                "analyzed_at": datetime.now().isoformat()
            })
            # 持久化索引：摘要文件名 → 源文件相对路径。
            # 只存文件名不存全路径 → 摘要被移到 archives/ 后索引依然有效。
            summary_index[os.path.basename(summary_file)] = filename

            state["analyzed_files"].append(rel_key(filepath))

            file_elapsed = time.time() - file_start
            batch_elapsed = time.time() - batch_start
            print(f"    耗时: {file_elapsed:.1f}秒")

        if time.time() - batch_start > BATCH_TIMEOUT:
            print(f"  ⚠️  本批耗时已达 {time.time() - batch_start:.0f}秒，超过{BATCH_TIMEOUT}秒限制，立即保存退出")
            break

    # ── 队列收尾：失败文件回队首重试；超时未处理的批次尾部也保留 ──
    leftover = [n for n in batch_names if n not in handled]
    next_queue = [n for n in (failed_this_batch + leftover + remaining_names)
                  if n not in quarantined]

    state["schema_version"] = STATE_SCHEMA_VERSION
    state["pending_files"] = next_queue
    state["failed_files"] = failed_map
    state["quarantined_files"] = sorted(quarantined)
    state["errors"] = fail_count
    state["last_run"] = datetime.now().isoformat()
    state["last_batch_at"] = datetime.now().isoformat()
    state["summaries"] = summaries
    save_state(state)
    save_summary_index(summary_index)

    done = len(state["analyzed_files"])
    print(f"✅ 本批完成：成功 {ok_count} / 失败 {fail_count} | 累计已完成 {done} | 队列剩余 {len(next_queue)}")
    print(f"[STATS] success={ok_count} failure={fail_count} queue={len(next_queue)}")
    if failed_this_batch:
        print(f"⚠️  {len(failed_this_batch)} 个文件将在下一轮重试（达 {MAX_RETRIES} 次后隔离）")
    if leftover:
        print(f"⚠️  {len(leftover)} 个文件因超时未处理，已保留在队列")


if __name__ == "__main__":
    main()

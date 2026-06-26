#!/usr/bin/env python3
"""
TTS 语音播报守护进程
- 追尾读取 agent_events.jsonl（文件偏移量追踪，零事件丢失）
- 每一次新事件都触发播报（不再依赖 agent_state.json 快照）
- result/info/error 类型：直接播报 agent 上报的 text 全文（含纯文本回复的流式分段内容）
- 其他类型（task/think/tool/exec 等）：播报 "模板 + 实际内容" 组合文案
- 防抖：用 state:content 做 key，同状态不同内容不会被误跳过
- 队列上限（最多 5 个待播放 .npy 文件，增大以覆盖完整流程）

v9.1 优化：数据源从轮询 agent_state.json（覆写快照，快速连续 emit 会丢失中间事件）
改为追尾读取 agent_events.jsonl（追加日志，逐条消费零丢失）。
"""
import json
import os
import signal
import sys
import time
import tempfile
import numpy as np
from pathlib import Path

try:
    from platform_utils import (
        get_work_dir, register_signal_handlers, get_rotating_logger
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from platform_utils import (
        get_work_dir, register_signal_handlers, get_rotating_logger
    )

try:
    from tts_client import synthesize, load_tts_config
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from tts_client import synthesize, load_tts_config

# ── 配置 ────────────────────────────────────────────────────
WORK_DIR = get_work_dir()
WORK_DIR.mkdir(parents=True, exist_ok=True)
BUS_FILE = WORK_DIR / "agent_events.jsonl"   # 追尾读取的事件日志（追加写入，零丢失）
AUDIO_QUEUE_DIR = WORK_DIR / "audio_queue"
PID_FILE = str(WORK_DIR / "tts_worker.pid")
LOG_FILE = str(WORK_DIR / "tts_worker.log")

# 自适应退避轮询参数：
#   有事件 → 间隔缩短到 POLL_MIN（快速响应连续事件）
#   连续空轮询 → 间隔逐步 ×POLL_BACKOFF_FACTOR，直到 POLL_MAX（省资源）
POLL_MIN = 0.1        # 活跃期最小轮询间隔（秒）— 100ms 响应速度
POLL_MAX = 1.0        # 空闲期最大轮询间隔（秒）— 降低延迟（原 3.0s 太慢）
POLL_BACKOFF_FACTOR = 2.0  # 退避倍率：每次空轮询间隔翻倍

DEBOUNCE_SEC = 2.0    # 同一状态防抖时间（秒）— 降低以减少重复事件等待（原 5.0s 太保守）
MAX_QUEUE_SIZE = 15    # 队列最大待播放文件数（需足够大以覆盖故事等长文本的多段播报）

# 全文播报类型：这些状态直接播报 agent_bus 上报的 text 全文，而非固定模板
# result — Agent 返回的最终结果（任务完成摘要）
# info   — 系统通知 / 纯文本回复内容（笑话、故事、诗歌等，流式分段输出）
# error  — 错误详情
FULLTEXT_KINDS = {'result', 'info', 'error'}

# ── 状态 → 播报文案映射 ─────────────────────────────────────
# 所有类型都支持拼接实际内容：
#   - FULLTEXT_KINDS: 直接播报 text 全文（不使用模板前缀）
#   - 其他类型: 播报 "模板，{实际内容}" 组合文案
ANNOUNCE_MAP = {
    "idle":    "主人，小龙虾待命中，随时听候吩咐哦",
    "think":   "",
    "task":    "",
    "tool":    "小龙虾正在调用工具",
    "exec":    "小龙虾正在执行中",
    "search":  "小龙虾正在搜索",
    "fetch":   "小龙虾正在抓取数据",
    "write":   "小龙虾正在写入文件",
    "info":    "",   # 空模板 → 走 FULLTEXT_KINDS 分支直接播报全文（纯文本回复/通用信息）
    "result":  "报告主人，任务完成啦",
    "error":   "哎呀，小龙虾遇到错误了",
    "stream":  "推流一切正常哦",
}

# 模板类型内容拼接的最大长度（超过此长度截断，防止 TTS 请求过大）
TEMPLATE_CONTENT_MAX = 60

# 腾讯云 TTS API 单次请求字符上限
TTS_MAX_CHARS = 280  # API 限制 300，留 20 字符余量


# ── 长文本分段（替代粗暴截断）────────────────────────────────
import re

# 清洗 emoji 和不可朗读的 Unicode 特殊字符（TTS API 遇到 emoji 可能乱读或报错）
_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F9FF"  # 各类 emoji
    "\U00002702-\U000027B0"  # Dingbats
    "\U0000FE00-\U0000FE0F"  # Variation Selectors
    "\U0000200D"             # Zero Width Joiner
    "\U00002600-\U000026FF"  # Misc Symbols
    "\U0001FA00-\U0001FAFF"  # Symbols Extended-A
    "\U00010000-\U0001FFFF"  # 补充平面中其余字符
    "]+",
    flags=re.UNICODE
)

def _clean_tts_text(text: str) -> str:
    """清洗文本：移除 emoji 和不可朗读字符，避免 TTS 合成异常"""
    if not text:
        return text
    return _EMOJI_RE.sub("", text).strip()

def split_long_text(text: str, max_chars: int = TTS_MAX_CHARS) -> list[str]:
    """将长文本按标点/换行分段，每段不超过 max_chars 字符。

    分段策略（优先级从高到低）：
    1. 按换行符分割
    2. 在句号/问号/感叹号/分号处断句
    3. 在逗号/顿号处断句
    4. 硬截断（超长无标点的情况）

    返回：分段列表，每段都是非空字符串
    """
    if len(text) <= max_chars:
        return [text]

    segments = []
    # 先按换行分成段落
    paragraphs = text.split('\n')

    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # 如果当前段落本身就不超限，尝试合并
        if len(current) + len(para) + 1 <= max_chars:
            current = f"{current}，{para}" if current else para
            continue

        # 当前累积的先入队
        if current:
            segments.append(current)
            current = ""

        # 段落本身超限，需要按标点断句
        if len(para) > max_chars:
            # 按句末标点分割
            sentences = re.split(r'(?<=[。！？；\.\!\?\;])', para)
            for sent in sentences:
                sent = sent.strip()
                if not sent:
                    continue
                if len(current) + len(sent) + 1 <= max_chars:
                    current = f"{current}{sent}" if current else sent
                else:
                    if current:
                        segments.append(current)
                    # 单句还是超限，按逗号断
                    if len(sent) > max_chars:
                        sub_parts = re.split(r'(?<=[，、\,])', sent)
                        current = ""
                        for sp in sub_parts:
                            sp = sp.strip()
                            if not sp:
                                continue
                            if len(current) + len(sp) + 1 <= max_chars:
                                current = f"{current}{sp}" if current else sp
                            else:
                                if current:
                                    segments.append(current)
                                # 硬截断兜底
                                while len(sp) > max_chars:
                                    segments.append(sp[:max_chars])
                                    sp = sp[max_chars:]
                                current = sp
                    else:
                        current = sent
        else:
            current = para

    if current:
        segments.append(current)

    return [s for s in segments if s.strip()]

# ── 日志 ────────────────────────────────────────────────────
_logger = get_rotating_logger("tts_worker", LOG_FILE,
                              max_bytes=2 * 1024 * 1024, backup_count=2)

def log(msg, level="INFO"):
    if level == "ERROR":
        _logger.error(msg)
    elif level == "WARN":
        _logger.warning(msg)
    else:
        _logger.info(msg)

# ── 信号处理 ────────────────────────────────────────────────
_running = True

def _sig_handler(signum, frame):
    global _running
    log(f"Received signal {signum}, shutting down...", "WARN")
    _running = False

# 忽略 SIGTERM（抗 OpenClaw 容器定期清理非自管进程）
import signal as _signal
_signal.signal(_signal.SIGTERM, _signal.SIG_IGN)
_signal.signal(_signal.SIGINT, _sig_handler)

# ── 写 PID ──────────────────────────────────────────────────
with open(PID_FILE, 'w') as f:
    f.write(str(os.getpid()))
log(f"TTS worker started. PID={os.getpid()}")


# ── 追尾读取 agent_events.jsonl ──────────────────────────────

def read_new_events(file_pos: int) -> tuple[list[dict], int]:
    """从 file_pos 偏移量处读取 agent_events.jsonl 中新增的事件行。

    追尾机制（类似 tail -f）：
    - 记住上次读到的字节偏移量，每次只读新增部分
    - 如果文件被 _trim() 原子替换导致缩小，自动重置到文件头
    - 跳过 JSON 解析失败的残缺行（防止并发写入竞争）

    Args:
        file_pos: 上次读取的文件字节偏移量

    Returns:
        (events, new_file_pos): 新事件列表 + 更新后的偏移量
    """
    try:
        if not BUS_FILE.exists():
            return [], 0

        current_size = BUS_FILE.stat().st_size

        # 文件缩小了（被 _trim() 原子替换），重置偏移量到文件末尾
        # 原因：_trim() 只保留最近 N 条旧事件，这些旧事件 tts_worker 已经处理过了，
        # 如果重置到文件头（0）会导致旧事件被误重播。重置到末尾 = 只处理 trim 之后的新事件。
        if current_size < file_pos:
            log(f"BUS_FILE shrunk ({file_pos} → {current_size}), resetting to EOF (skip old events)")
            file_pos = current_size

        # 没有新数据
        if current_size <= file_pos:
            return [], file_pos

        # 读取新增部分
        with open(BUS_FILE, "r", encoding="utf-8") as f:
            f.seek(file_pos)
            new_lines = f.readlines()
            new_file_pos = f.tell()

        events = []
        for line in new_lines:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # 跳过残缺行（并发写入竞争导致）

        return events, new_file_pos

    except Exception as e:
        log(f"read_new_events error: {e}", "WARN")
        return [], file_pos


# ── 队列管理 ──────────────────────────────────────────────────

def get_queue_size() -> int:
    """获取 audio_queue 目录中待播放 .npy 文件数。
    优化：os.scandir 替代 glob，减少系统调用开销。
    """
    qdir = str(AUDIO_QUEUE_DIR)
    if not os.path.isdir(qdir):
        return 0
    count = 0
    try:
        with os.scandir(qdir) as entries:
            for entry in entries:
                if entry.name.endswith('.npy') and entry.is_file():
                    count += 1
    except OSError:
        pass
    return count


def enqueue_audio(audio: np.ndarray) -> bool:
    """将音频 numpy 数组原子写入 audio_queue/ 目录"""
    AUDIO_QUEUE_DIR.mkdir(parents=True, exist_ok=True)

    # 队列满了，跳过
    if get_queue_size() >= MAX_QUEUE_SIZE:
        log(f"Queue full ({MAX_QUEUE_SIZE}), dropping audio", "WARN")
        return False

    # 原子写入：先写临时文件，再 rename
    timestamp_ms = int(time.time() * 1000)
    final_name = AUDIO_QUEUE_DIR / f"{timestamp_ms}.npy"
    try:
        fd, tmp_path = tempfile.mkstemp(dir=str(AUDIO_QUEUE_DIR), suffix=".tmp")
        os.close(fd)
        np.save(tmp_path, audio)
        os.replace(tmp_path, str(final_name))
        log(f"Enqueued audio: {final_name.name} ({len(audio)} samples)")
        return True
    except Exception as e:
        log(f"Failed to enqueue audio: {e}", "ERROR")
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        return False


# ── 主循环 ──────────────────────────────────────────────────

def main_loop():
    tts_cfg = load_tts_config()
    if not tts_cfg:
        log("TTS config not found (tts_secret_id/tts_secret_key in config.json). "
            "TTS worker will poll until config is available.", "WARN")

    last_announce_time = {}
    retry_config_time = 0
    poll_interval = POLL_MIN           # 自适应轮询间隔

    file_pos = 0
    if BUS_FILE.exists():
        file_pos = BUS_FILE.stat().st_size
        log(f"Tailing {BUS_FILE.name} from offset {file_pos}")

    log(f"Adaptive polling: min={POLL_MIN}s max={POLL_MAX}s backoff=×{POLL_BACKOFF_FACTOR}")

    while _running:
        time.sleep(poll_interval)

        # 配置未加载时用最大间隔等待
        if not tts_cfg:
            poll_interval = POLL_MAX
            now = time.time()
            if now - retry_config_time > 10:
                tts_cfg = load_tts_config()
                retry_config_time = now
                if tts_cfg:
                    log("TTS config loaded successfully")
                    poll_interval = POLL_MIN
            continue

        new_events, file_pos = read_new_events(file_pos)

        if not new_events:
            # 空轮询 → 退避：间隔翻倍，直到上限
            prev = poll_interval
            poll_interval = min(poll_interval * POLL_BACKOFF_FACTOR, POLL_MAX)
            if poll_interval != prev:
                log(f"Backoff: poll interval {prev:.2f}s → {poll_interval:.2f}s")
            continue

        # 有事件 → 立刻切回最快速度
        if poll_interval > POLL_MIN:
            log(f"Events arrived: poll interval {poll_interval:.2f}s → {POLL_MIN}s")
            poll_interval = POLL_MIN

        for event in new_events:
            current_state = event.get("kind", "")
            current_content = event.get("text", "")

            # 过滤直播系统通道激活相关事件（不需要播报）
            if any(kw in current_content for kw in ("启动直播", "直播已在运行", "直播已运行",
                                                     "检查直播系统状态", "直播系统正在运行")):
                log(f"Skip TTS for channel-activate event: {current_content[:60]}")
                continue

            template = ANNOUNCE_MAP.get(current_state)
            if template is None:
                continue

            if current_content:
                debounce_key = f"{current_state}:{current_content[:50]}"
            else:
                debounce_key = current_state

            # result 类型额外增加 kind 级别去重：短时间内只播报一次 result（防止 Agent 连发两条 result）
            result_kind_key = f"__kind__:{current_state}" if current_state == "result" else None

            now = time.time()
            if debounce_key in last_announce_time:
                elapsed = now - last_announce_time[debounce_key]
                if elapsed < DEBOUNCE_SEC:
                    log(f"Debounce: skip '{debounce_key[:60]}' ({elapsed:.1f}s < {DEBOUNCE_SEC}s)")
                    continue
            if result_kind_key and result_kind_key in last_announce_time:
                elapsed = now - last_announce_time[result_kind_key]
                if elapsed < DEBOUNCE_SEC:
                    log(f"Debounce(kind): skip result (another result was announced {elapsed:.1f}s ago)")
                    continue

            if current_state in FULLTEXT_KINDS and current_content:
                # 长文本分段播报（按标点断句，每段不超过 API 限制）
                clean_content = _clean_tts_text(current_content)
                if not clean_content:
                    continue
                text_segments = split_long_text(clean_content)
                if not text_segments:
                    continue
                # 如果只有一段，直接播报
                announce_texts = text_segments
            elif current_content:
                clean_content = _clean_tts_text(current_content)
                content_part = clean_content[:TEMPLATE_CONTENT_MAX]
                if len(clean_content) > TEMPLATE_CONTENT_MAX:
                    content_part += "..."
                announce_texts = [f"{template}，{content_part}"]
            else:
                announce_texts = [template] if template else []

            # 防御：文案列表为空时跳过
            if not announce_texts:
                continue

            log(f"New event [{current_state}]: {len(announce_texts)} segment(s), first: {announce_texts[0][:80]}...")

            for seg_idx, announce_text in enumerate(announce_texts):
                # 防御：空段跳过
                if not announce_text.strip():
                    continue
                # 队列满了就停止后续分段（避免无限堆积）
                if get_queue_size() >= MAX_QUEUE_SIZE:
                    log(f"Queue full, dropping remaining {len(announce_texts) - seg_idx} segment(s)", "WARN")
                    break
                try:
                    audio = synthesize(
                        announce_text,
                        tts_cfg["secret_id"],
                        tts_cfg["secret_key"],
                        tts_cfg["sdkappid"]
                    )
                    if audio is not None and len(audio) > 0:
                        enqueue_audio(audio)
                        last_announce_time[debounce_key] = now
                        if result_kind_key:
                            last_announce_time[result_kind_key] = now
                    else:
                        log(f"TTS returned empty audio for segment {seg_idx}: {announce_text[:80]}", "WARN")
                except Exception as e:
                    log(f"TTS synthesis error (segment {seg_idx}): {e}", "ERROR")

    log("TTS worker exiting.")
    try:
        os.remove(PID_FILE)
    except OSError:
        pass


# ── 入口 ─────────────────────────────────────────────────────

if __name__ == "__main__":
    main_loop()

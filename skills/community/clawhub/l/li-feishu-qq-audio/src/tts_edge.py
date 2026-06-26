"""
Edge TTS 模块
功能：使用 Microsoft Edge TTS 合成语音

特点：
- 支持多种中文语音
- 自动处理文本分块（长文本分割）
- 信号处理确保临时文件清理
- 系统资源检查
"""

import os
import sys
import asyncio
import logging
import signal
import tempfile
import shutil
import subprocess
import time
from typing import Optional, Tuple, Callable, List
from pathlib import Path
from contextlib import contextmanager

# 尝试导入 edge-tts
try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False
    edge_tts = None

# 尝试导入 psutil
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    psutil = None

# 配置日志
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

if not _logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    _logger.addHandler(handler)


# 配置常量
DEFAULT_TIMEOUT = 120  # TTS 超时（秒）
MIN_FREE_MEMORY_MB = 256  # 最小可用内存（MB）
MAX_TEXT_LENGTH = 3000  # 最大文本长度
DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"  # 默认语音

# 支持的中文语音
SUPPORTED_VOICES = [
    "zh-CN-XiaoxiaoNeural",    # 晓晓 - 女声
    "zh-CN-YunyangNeural",     # 云扬 - 男声
    "zh-CN-YunxiNeural",       # 云希 - 男声
    "zh-CN-YunjianNeural",     # 云健 - 男声
    "zh-CN-XiaoyiNeural",      # 晓伊 - 女声
    "zh-CN-XiaochenNeural",    # 晓晨 - 女声
    "zh-CN-XiaohanNeural",     # 晓涵 - 女声
]

# 全局状态管理
_cleanup_handlers: List[Callable] = []
_is_shutting_down = False


def register_cleanup_handler(handler: Callable):
    """注册清理处理器"""
    _cleanup_handlers.append(handler)


def signal_handler(signum, frame):
    """信号处理 - 确保清理临时文件"""
    global _is_shutting_down
    _is_shutting_down = True
    _logger.info(f"收到信号 {signum}，执行清理...")
    
    for handler in _cleanup_handlers:
        try:
            handler()
        except Exception as e:
            _logger.error(f"清理处理器异常: {e}")
    
    sys.exit(0)


# 注册信号处理
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


def check_system_resources() -> Tuple[bool, str]:
    """
    检查系统资源是否充足
    
    Returns:
        (是否可用, 错误信息)
    """
    try:
        # 检查内存
        if HAS_PSUTIL:
            mem = psutil.virtual_memory()
            free_mb = mem.available / (1024 * 1024)
            
            if free_mb < MIN_FREE_MEMORY_MB:
                return False, f"可用内存不足: {free_mb:.1f}MB (需要至少 {MIN_FREE_MEMORY_MB}MB)"
        else:
            # 降级方案：检查 /proc/meminfo
            try:
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.read()
                    for line in meminfo.split('\n'):
                        if line.startswith('MemAvailable:'):
                            available_kb = int(line.split()[1])
                            free_mb = available_kb / 1024
                            if free_mb < MIN_FREE_MEMORY_MB:
                                return False, f"可用内存不足: {free_mb:.1f}MB (需要至少 {MIN_FREE_MEMORY_MB}MB)"
                            break
            except Exception:
                _logger.warning("无法读取内存信息，跳过内存检查")
        
        # 检查磁盘空间
        try:
            tmp_stat = shutil.disk_usage("/tmp")
            free_gb = tmp_stat.free / (1024 * 1024 * 1024)
            
            if free_gb < 0.5:  # 至少需要500MB
                return False, f"磁盘空间不足: {free_gb:.2f}GB"
        except Exception as e:
            _logger.warning(f"无法检查磁盘空间: {e}")
        
        return True, ""
        
    except Exception as e:
        return False, f"系统资源检查失败: {e}"


def split_text(text: str, max_length: int = 500) -> List[str]:
    """
    将长文本分割成适合 TTS 处理的短段落
    
    Args:
        text: 输入文本
        max_length: 每段最大长度
    
    Returns:
        文本段落列表
    """
    if len(text) <= max_length:
        return [text]
    
    segments = []
    current = ""
    
    # 按句子分割
    sentences = text.replace('。', '.|').replace('！', '!|').replace('？', '?|').split('|')
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        if len(current) + len(sentence) + 1 <= max_length:
            current += sentence + "。" if not sentence.endswith(('.', '!', '?')) else sentence
        else:
            if current:
                segments.append(current)
            current = sentence
    
    if current:
        segments.append(current)
    
    # 如果还是太长，按字符强制分割
    final_segments = []
    for seg in segments:
        while len(seg) > max_length:
            final_segments.append(seg[:max_length])
            seg = seg[max_length:]
        if seg:
            final_segments.append(seg)
    
    return final_segments if final_segments else [text[:max_length]]


def generate_unique_filename(prefix: str, suffix: str) -> str:
    """生成唯一的临时文件名"""
    timestamp = int(time.time() * 1000)
    pid = os.getpid()
    random_suffix = hash(f"{timestamp}{pid}{prefix}") % 10000
    return f"{prefix}_{pid}_{timestamp}_{random_suffix}{suffix}"


async def synthesize_segment(
    text: str,
    output_path: str,
    voice: str = DEFAULT_VOICE,
    rate: str = "+0%",
    volume: str = "+0%",
    timeout: int = DEFAULT_TIMEOUT
) -> Tuple[bool, str]:
    """
    合成单个文本段落
    
    Args:
        text: 要合成的文本
        output_path: 输出音频文件路径
        voice: 语音角色
        rate: 语速（如 "+0%", "+10%", "-10%"）
        volume: 音量
        timeout: 超时时间（秒）
    
    Returns:
        (是否成功, 错误信息)
    """
    if not HAS_EDGE_TTS:
        return False, "edge-tts 未安装，请运行: pip install edge-tts"
    
    if _is_shutting_down:
        return False, "系统正在关闭"
    
    # 检查系统资源
    resources_ok, resources_error = check_system_resources()
    if not resources_ok:
        return False, resources_error
    
    try:
        _logger.info(f"TTS 合成: {text[:50]}...")
        
        # 使用 edge-tts
        communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume)
        
        # 设置超时
        start_time = time.monotonic()
        
        await asyncio.wait_for(
            communicate.save(output_path),
            timeout=timeout
        )
        
        elapsed = time.monotonic() - start_time
        _logger.debug(f"TTS 合成耗时: {elapsed:.2f}秒")
        
        # 验证输出文件
        if not os.path.exists(output_path):
            return False, "输出文件未生成"
        
        if os.path.getsize(output_path) == 0:
            return False, "输出文件为空"
        
        # 验证音频格式
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_format", output_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return False, f"输出文件格式无效: {result.stderr}"
        
        _logger.info(f"TTS 合成成功: {output_path}")
        return True, ""
        
    except asyncio.TimeoutError:
        _logger.error("TTS 合成超时")
        if os.path.exists(output_path):
            try:
                os.unlink(output_path)
            except:
                pass
        return False, f"TTS 合成超时（超过{timeout}秒）"
        
    except Exception as e:
        _logger.error(f"TTS 合成异常: {e}")
        if os.path.exists(output_path):
            try:
                os.unlink(output_path)
            except:
                pass
        return False, str(e)


async def merge_audio_files(input_files: List[str], output_path: str) -> Tuple[bool, str]:
    """
    合并多个音频文件
    
    Args:
        input_files: 输入音频文件列表
        output_path: 输出音频文件路径
    
    Returns:
        (是否成功, 错误信息)
    """
    if len(input_files) == 1:
        # 只有一个文件，直接复制
        try:
            shutil.copy(input_files[0], output_path)
            return True, ""
        except Exception as e:
            return False, f"复制文件失败: {e}"
    
    # 创建 ffmpeg 输入列表文件
    list_file = generate_unique_filename("/tmp/audio_list", ".txt")
    
    try:
        # 写入文件列表
        with open(list_file, 'w', encoding='utf-8') as f:
            for audio_file in input_files:
                f.write(f"file '{audio_file}'\n")
        
        # 使用 ffmpeg 合并
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-acodec", "libmp3lame",
            "-q:a", "2",
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # 注册清理处理器
        def kill_process():
            try:
                process.kill()
            except:
                pass
        
        register_cleanup_handler(kill_process)
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=60
            )
        finally:
            if kill_process in _cleanup_handlers:
                _cleanup_handlers.remove(kill_process)
        
        if process.returncode != 0:
            error_msg = stderr.decode('utf-8', errors='ignore')[:500]
            return False, f"合并失败: {error_msg}"
        
        return True, ""
        
    except asyncio.TimeoutError:
        return False, "合并音频超时"
    except Exception as e:
        return False, f"合并异常: {e}"
    finally:
        if os.path.exists(list_file):
            try:
                os.unlink(list_file)
            except:
                pass


async def text_to_speech(
    text: str,
    output_path: Optional[str] = None,
    voice: str = DEFAULT_VOICE,
    rate: str = "+0%",
    volume: str = "+0%",
    timeout: int = DEFAULT_TIMEOUT
) -> Tuple[Optional[str], str]:
    """
    文本转语音（主函数）
    
    Args:
        text: 要合成的文本
        output_path: 输出音频文件路径（可选）
        voice: 语音角色
        rate: 语速
        volume: 音量
        timeout: 超时时间（秒）
    
    Returns:
        (输出文件路径, 错误信息)
    """
    if not text or not text.strip():
        return None, "文本为空"
    
    if len(text) > MAX_TEXT_LENGTH:
        _logger.warning(f"文本过长，截断到 {MAX_TEXT_LENGTH} 字符")
        text = text[:MAX_TEXT_LENGTH]
    
    # 生成输出文件名
    if not output_path:
        output_path = generate_unique_filename("/tmp/tts_output", ".mp3")
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    temp_files: List[str] = []
    
    try:
        # 分割长文本
        segments = split_text(text)
        _logger.info(f"文本分割为 {len(segments)} 个段落")
        
        # 合成每个段落
        for i, segment in enumerate(segments):
            if _is_shutting_down:
                return None, "系统正在关闭"
            
            segment_path = generate_unique_filename(f"/tmp/tts_segment_{i}", ".mp3")
            temp_files.append(segment_path)
            
            success, error = await synthesize_segment(
                segment,
                segment_path,
                voice=voice,
                rate=rate,
                volume=volume,
                timeout=timeout
            )
            
            if not success:
                return None, error
        
        # 合并音频文件
        _logger.info("合并音频文件...")
        success, error = await merge_audio_files(temp_files, output_path)
        
        if not success:
            return None, error
        
        _logger.info(f"TTS 完成: {output_path}")
        return output_path, ""
        
    except Exception as e:
        _logger.error(f"TTS 异常: {e}")
        return None, str(e)
    finally:
        # 清理临时文件
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                    _logger.debug(f"清理临时文件: {temp_file}")
                except Exception as e:
                    _logger.warning(f"无法清理临时文件 {temp_file}: {e}")


# 注册全局清理
register_cleanup_handler(lambda: _logger.info("TTS 模块清理完成"))


# CLI 接口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Edge TTS 工具")
    parser.add_argument("text", help="要合成的文本")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("-v", "--voice", default=DEFAULT_VOICE, help="语音角色")
    parser.add_argument("-r", "--rate", default="+0%", help="语速（如 +10%, -10%）")
    parser.add_argument("--list-voices", action="store_true", help="列出支持的语音")
    
    args = parser.parse_args()
    
    if args.list_voices:
        print("支持的中文语音:")
        for voice in SUPPORTED_VOICES:
            print(f"  - {voice}")
        sys.exit(0)
    
    if not HAS_EDGE_TTS:
        print("错误: edge-tts 未安装，请运行: pip install edge-tts")
        sys.exit(1)
    
    # 运行 TTS
    result_path, error = asyncio.run(text_to_speech(
        args.text,
        output_path=args.output,
        voice=args.voice,
        rate=args.rate
    ))
    
    if result_path:
        print(f"生成成功: {result_path}")
    else:
        print(f"生成失败: {error}")
        sys.exit(1)

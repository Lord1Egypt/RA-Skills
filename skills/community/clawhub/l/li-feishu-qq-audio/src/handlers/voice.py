"""
语音消息处理模块
功能：处理飞书语音消息，支持语音识别(STT)和语音合成(TTS)

工作流程：
1. 接收飞书语音消息
2. 下载语音文件（OPUS格式）
3. 转换为 WAV 格式
4. 使用 faster-whisper 识别语音内容
5. 将识别结果传递给 AI 处理
6. AI 生成回复后，使用 Edge TTS 合成语音
7. 将语音文件转换为 OPUS 格式（飞书要求）
8. 发送语音回复
"""

import os
import sys
import json
import asyncio
import logging
import subprocess
import tempfile
import shutil
import signal
import time
from typing import Optional, Dict, Any, Tuple, Callable, List
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager
from functools import wraps

# 尝试导入 psutil，如果不可用则提供降级方案
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
DEFAULT_TIMEOUT_STT = 180  # 语音识别超时（秒）
DEFAULT_TIMEOUT_TTS = 120  # 语音合成超时（秒）
DEFAULT_TIMEOUT_CONVERT = 60  # 音频转换超时（秒）
TEMP_FILE_RETENTION_HOURS = 24  # 临时文件保留时间
MIN_FREE_MEMORY_MB = 512  # 最小可用内存（MB）
MAX_AUDIO_FILE_SIZE_MB = 50  # 最大音频文件大小（MB）

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


@contextmanager
def temp_file_context(prefix: str, suffix: str, delete: bool = True):
    """临时文件上下文管理器 - 确保文件被清理"""
    tmp_path = generate_unique_filename(prefix, suffix)
    try:
        yield tmp_path
    finally:
        if delete and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
                _logger.debug(f"清理临时文件: {tmp_path}")
            except Exception as e:
                _logger.warning(f"无法清理临时文件 {tmp_path}: {e}")


def generate_unique_filename(prefix: str, suffix: str) -> str:
    """生成唯一的临时文件名"""
    timestamp = int(time.time() * 1000)
    pid = os.getpid()
    random_suffix = hash(f"{timestamp}{pid}{prefix}") % 10000
    return f"{prefix}_{pid}_{timestamp}_{random_suffix}{suffix}"


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
            
            if free_gb < 1:  # 至少需要1GB
                return False, f"磁盘空间不足: {free_gb:.2f}GB"
        except Exception as e:
            _logger.warning(f"无法检查磁盘空间: {e}")
        
        # 检查 ffmpeg
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode != 0:
            return False, "ffmpeg 不可用"
        
        return True, ""
        
    except Exception as e:
        return False, f"系统资源检查失败: {e}"


def validate_audio_file(file_path: str, max_size_mb: int = MAX_AUDIO_FILE_SIZE_MB) -> Tuple[bool, str]:
    """
    验证音频文件是否有效
    
    Args:
        file_path: 文件路径
        max_size_mb: 最大文件大小（MB）
    
    Returns:
        (是否有效, 错误信息)
    """
    try:
        # 检查文件存在性
        if not os.path.exists(file_path):
            return False, f"文件不存在: {file_path}"
        
        # 检查文件大小
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > max_size_mb:
            return False, f"文件过大: {size_mb:.2f}MB (最大允许 {max_size_mb}MB)"
        
        if os.path.getsize(file_path) == 0:
            return False, "文件为空"
        
        # 检查文件格式
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_format", "-show_streams", file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return False, f"文件格式无效: {result.stderr}"
        
        # 检查文件是否损坏（尝试读取前几秒）
        probe_result = subprocess.run(
            ["ffmpeg", "-y", "-i", file_path, "-t", "1", "-f", "null", "-"],
            capture_output=True,
            timeout=10
        )
        
        if probe_result.returncode != 0:
            return False, "文件可能已损坏"
        
        return True, ""
        
    except subprocess.TimeoutExpired:
        return False, "文件验证超时"
    except Exception as e:
        return False, f"文件验证失败: {e}"


def get_scripts_dir(env: dict) -> str:
    """获取脚本目录路径"""
    scripts_dir = env.get("SCRIPTS_DIR")
    if scripts_dir:
        return scripts_dir
    
    skill_dir = env.get("SKILL_DIR")
    if skill_dir:
        return os.path.join(skill_dir, "scripts")
    
    current_dir = Path(__file__).parent.parent.parent
    return os.path.join(str(current_dir), "scripts")


def load_env_config(env: dict) -> dict:
    """加载环境配置"""
    scripts_dir = get_scripts_dir(env)
    env_file = os.path.join(scripts_dir, ".env")
    
    config = {}
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        except Exception as e:
            _logger.warning(f"加载 .env 文件失败: {e}")
    
    return config


def ensure_script_executable(script_path: str) -> bool:
    """确保脚本可执行"""
    if not os.path.exists(script_path):
        _logger.error(f"脚本不存在: {script_path}")
        return False
    
    if not os.access(script_path, os.X_OK):
        try:
            os.chmod(script_path, os.stat(script_path).st_mode | 0o755)
            _logger.debug(f"已设置脚本权限: {script_path}")
        except Exception as e:
            _logger.warning(f"无法设置脚本权限: {e}")
            return False
    
    return True


async def convert_audio_format(
    input_path: str,
    output_path: str,
    output_codec: str = "pcm_s16le",
    sample_rate: int = 16000,
    channels: int = 1,
    extra_args: Optional[List[str]] = None,
    timeout: int = DEFAULT_TIMEOUT_CONVERT
) -> Tuple[bool, str]:
    """
    通用音频格式转换函数
    
    Args:
        input_path: 输入音频文件路径
        output_path: 输出音频文件路径
        output_codec: 输出编码器
        sample_rate: 采样率
        channels: 声道数
        extra_args: 额外 ffmpeg 参数
        timeout: 超时时间（秒）
    
    Returns:
        (转换是否成功, 错误信息)
    """
    try:
        _logger.info(f"音频转换: {input_path} -> {output_path}")
        
        # 验证输入文件
        is_valid, error_msg = validate_audio_file(input_path)
        if not is_valid:
            return False, f"输入文件无效: {error_msg}"
        
        # 检查系统资源
        resources_ok, resources_error = check_system_resources()
        if not resources_ok:
            return False, resources_error
        
        # 构建命令
        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-ar", str(sample_rate),
            "-ac", str(channels),
            "-c:a", output_codec,
        ]
        
        if extra_args:
            cmd.extend(extra_args)
        
        cmd.append(output_path)
        
        # 执行转换
        start_time = time.monotonic()
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
                timeout=timeout
            )
        except asyncio.TimeoutError:
            _logger.error("音频转换超时")
            try:
                process.kill()
                await process.wait()
            except:
                pass
            return False, "音频转换超时"
        finally:
            # 移除清理处理器
            if kill_process in _cleanup_handlers:
                _cleanup_handlers.remove(kill_process)
        
        elapsed = time.monotonic() - start_time
        _logger.debug(f"音频转换耗时: {elapsed:.2f}秒")
        
        if process.returncode != 0:
            error_msg = stderr.decode('utf-8', errors='ignore')[:500]
            _logger.error(f"音频转换失败: {error_msg}")
            return False, f"转换失败: {error_msg}"
        
        # 验证输出文件
        is_valid, error_msg = validate_audio_file(output_path)
        if not is_valid:
            return False, f"输出文件无效: {error_msg}"
        
        _logger.info(f"音频转换成功: {output_path}")
        return True, ""
        
    except Exception as e:
        _logger.error(f"音频转换异常: {e}")
        return False, str(e)


async def convert_opus_to_wav(opus_path: str, wav_path: str) -> Tuple[bool, str]:
    """将 OPUS 音频转换为 WAV 格式（用于语音识别）"""
    return await convert_audio_format(
        input_path=opus_path,
        output_path=wav_path,
        output_codec="pcm_s16le",
        sample_rate=16000,
        channels=1
    )


async def convert_mp3_to_opus(mp3_path: str, opus_path: str) -> Tuple[bool, str]:
    """将 MP3 音频转换为 OPUS 格式（飞书要求）"""
    return await convert_audio_format(
        input_path=mp3_path,
        output_path=opus_path,
        output_codec="libopus",
        sample_rate=48000,
        channels=1,
        extra_args=["-b:a", "24k"]
    )


async def transcribe_audio(audio_file: str, env: dict) -> str:
    """
    语音识别（STT）
    
    Args:
        audio_file: 音频文件路径（WAV 格式）
        env: 环境变量
    
    Returns:
        识别出的文本
    """
    _logger.info(f"开始语音识别: {audio_file}")
    
    # 验证音频文件
    is_valid, error_msg = validate_audio_file(audio_file)
    if not is_valid:
        raise ValueError(f"音频文件无效: {error_msg}")
    
    # 检查系统资源
    resources_ok, resources_error = check_system_resources()
    if not resources_ok:
        raise RuntimeError(resources_error)
    
    scripts_dir = get_scripts_dir(env)
    script_path = os.path.join(scripts_dir, "fast-whisper-fast.sh")
    
    if not ensure_script_executable(script_path):
        raise FileNotFoundError(f"语音识别脚本不存在或不可执行: {script_path}")
    
    process = None
    try:
        process = await asyncio.create_subprocess_exec(
            "bash",
            script_path,
            audio_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # 注册清理处理器
        def kill_process():
            if process:
                try:
                    process.kill()
                except:
                    pass
        
        register_cleanup_handler(kill_process)
        
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=DEFAULT_TIMEOUT_STT
        )
        
        # 移除清理处理器
        if kill_process in _cleanup_handlers:
            _cleanup_handlers.remove(kill_process)
        
        if process.returncode != 0:
            stderr_text = stderr.decode('utf-8', errors='ignore') if stderr else "未知错误"
            _logger.error(f"语音识别脚本执行失败: {stderr_text}")
            raise RuntimeError(f"语音识别失败: {stderr_text}")
        
        result = stdout.decode('utf-8', errors='ignore').strip()
        
        if not result:
            _logger.warning("语音识别结果为空")
            return ""
        
        _logger.info(f"语音识别完成，结果长度: {len(result)}")
        return result
        
    except asyncio.TimeoutError:
        _logger.error("语音识别超时")
        if process:
            try:
                process.kill()
                await process.wait()
            except:
                pass
        raise RuntimeError("语音识别超时（超过3分钟）")
        
    except Exception as e:
        _logger.error(f"语音识别异常: {e}")
        raise


async def generate_tts(text: str, env: dict) -> str:
    """
    语音合成（TTS）
    
    Args:
        text: 要合成的文本
        env: 环境变量
    
    Returns:
        生成的 MP3 文件路径
    """
    _logger.info(f"开始语音合成，文本长度: {len(text)}")
    
    # 检查系统资源
    resources_ok, resources_error = check_system_resources()
    if not resources_ok:
"""
TTS Controller Module
火山引擎 TTS 2.0 WebSocket V3 API 调用，支持 section_id 上下文模式
"""

import os
import json
import struct
import io
from pathlib import Path
from typing import Optional, Dict, List, Tuple, TYPE_CHECKING
import shutil
import websocket
import time

from .schema import ScriptVersion, DialogueLine

if TYPE_CHECKING:
    from pydub import AudioSegment

# 检查 ffmpeg 是否可用
def _check_ffmpeg():
    """检查系统是否安装了 ffmpeg"""
    # 检查环境变量
    ffmpeg_path = os.environ.get("FFMPEG_PATH")
    if ffmpeg_path and os.path.isfile(ffmpeg_path):
        return True

    # 检查 PATH
    if shutil.which("ffmpeg") is not None:
        return True

    # 检查常见安装路径 (Windows)
    common_paths = [
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
    ]
    for path in common_paths:
        if os.path.isfile(path):
            # 设置环境变量供 pydub 使用
            os.environ["FFMPEG_PATH"] = path
            return True

    return False

_HAS_FFMPEG = _check_ffmpeg()
AudioSegment = None

if _HAS_FFMPEG:
    try:
        from pydub import AudioSegment as _AS
        AudioSegment = _AS
        print(f"ffmpeg detected, stereo audio merging enabled")
    except ImportError:
        print("Warning: pydub not installed, audio merging will use raw MP3 concatenation")
else:
    print("Warning: ffmpeg not found, audio merging will use raw MP3 concatenation (mono)")


class VoiceConfig:
    """音色配置管理器"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        初始化音色配置

        Args:
            config_path: 配置文件路径，默认使用 config/tts_voices.json
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "tts_voices.json"

        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self) -> dict:
        """加载配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Voice config not found: {self.config_path}")

        with open(self.config_path, encoding='utf-8') as f:
            return json.load(f)

    def get_voice_info(self, voice_id: str) -> Optional[dict]:
        """获取音色信息"""
        return self._config.get("voices", {}).get(voice_id)

    def get_resource_id(self, voice_id: str) -> str:
        """
        根据音色ID获取资源ID

        Returns:
            资源ID: seed-tts-2.0 (uranus) 或 volc.megatts.default (saturn)
        """
        voice_info = self.get_voice_info(voice_id)
        if voice_info:
            voice_type = voice_info.get("type", "uranus")
            resource_mapping = self._config.get("_meta", {}).get("resource_mapping", {})
            return resource_mapping.get(voice_type, "seed-tts-2.0")
        return "seed-tts-2.0"  # 默认使用 seed-tts-2.0

    def get_recommended_pair(self, pair_name: str = "default") -> Optional[dict]:
        """获取推荐的音色配对"""
        return self._config.get("recommended_pairs", {}).get(pair_name)

    def list_voices(self, gender: Optional[str] = None, scene: Optional[str] = None) -> List[dict]:
        """
        列出符合条件的音色

        Args:
            gender: 性别过滤 (male/female)
            scene: 场景过滤
        """
        voices = []
        for voice_id, info in self._config.get("voices", {}).items():
            if gender and info.get("gender") != gender:
                continue
            if scene and info.get("scene") != scene:
                continue
            voices.append({"voice_id": voice_id, **info})
        return voices

    def get_default_voices(self) -> Tuple[str, str]:
        """获取默认男女音色"""
        default_pair = self.get_recommended_pair("default")
        if default_pair:
            return default_pair.get("host_a"), default_pair.get("host_b")
        # 回退到硬编码默认值
        return "zh_male_shaonianzixin_uranus_bigtts", "zh_female_vv_uranus_bigtts"


class VolcanoTTSController:
    """
    火山引擎 TTS 2.0 WebSocket 控制器
    支持 section_id 上下文模式，实现逐句合成
    优化特性：
    - WebSocket链接复用（降低时延约70ms/次）
    - 引用上文支持（TTS 2.0特有，增强情感连贯性）
    - 智能重试机制（指数退避）
    - 成本统计与监控
    """

    # WebSocket V3 单向流式接口
    WS_URL = "wss://openspeech.bytedance.com/api/v3/tts/unidirectional/stream"

    # 重试配置
    MAX_RETRIES = 3
    RETRY_DELAY_BASE = 1.0  # 基础延迟（秒）

    def __init__(
        self,
        app_id: Optional[str] = None,
        access_token: Optional[str] = None,
        secret_key: Optional[str] = None,
        host_a_voice: Optional[str] = None,
        host_b_voice: Optional[str] = None,
        voice_config_path: Optional[Path] = None,
        enable_context: bool = True,  # 是否启用引用上文功能
        cost_tracker: Optional[Dict] = None,  # 成本统计器
    ):
        """
        初始化TTS控制器

        Args:
            app_id: 应用ID
            access_token: 访问令牌
            secret_key: 密钥（可选）
            host_a_voice: 说话人A的音色ID，None则使用配置默认
            host_b_voice: 说话人B的音色ID，None则使用配置默认
            voice_config_path: 音色配置文件路径
            enable_context: 是否启用引用上文功能（仅TTS 2.0有效）
            cost_tracker: 成本统计字典（传入外部dict以追踪成本）
        """
        self.app_id = app_id or os.getenv("VOLCANO_TTS_APP_ID", "")
        self.access_token = access_token or os.getenv("VOLCANO_TTS_ACCESS_TOKEN", "")
        self.secret_key = secret_key or os.getenv("VOLCANO_TTS_SECRET_KEY", "")

        # 初始化音色配置
        self.voice_config = VoiceConfig(voice_config_path)

        # 获取音色ID（使用配置或传入的值）
        default_a, default_b = self.voice_config.get_default_voices()
        self.host_a_voice = host_a_voice or default_a
        self.host_b_voice = host_b_voice or default_b

        # 根据音色自动获取资源ID
        self.resource_id = self.voice_config.get_resource_id(self.host_a_voice)

        # 判断是否使用TTS 2.0（用于决定可用功能）
        self._is_tts_v2 = self._check_tts_v2()

        # 是否启用引用上文
        self.enable_context = enable_context and self._is_tts_v2

        # 验证 TTS 配置
        if not self.app_id:
            raise ValueError(
                "Volcano TTS App ID not configured. "
                "Set VOLCANO_TTS_APP_ID environment variable."
            )
        if not self.access_token:
            raise ValueError(
                "Volcano TTS Access Token not configured. "
                "Set VOLCANO_TTS_ACCESS_TOKEN environment variable."
            )

        # 上下文链管理：每个说话人的 session_id 链
        self._session_chains: Dict[str, List[str]] = {
            "A": [],
            "B": [],
        }

        # WebSocket连接复用池：按说话人保存连接
        self._connection_pools: Dict[str, websocket.WebSocket] = {}

        # Sequence计数器：每个连接需要递增的sequence号
        self._sequence_counters: Dict[str, int] = {}

        # 成本统计（使用传入的字典或创建新字典）
        if cost_tracker is None:
            self.cost_tracker = {
                "total_requests": 0,
                "total_chars": 0,
                "total_audio_seconds": 0,
                "failed_requests": 0,
                "retry_count": 0,
                "connection_reuses": 0,
                "connection_creates": 0,
            }
        else:
            # 使用传入的字典，初始化缺失的键
            self.cost_tracker = cost_tracker
            for key, val in {
                "total_requests": 0,
                "total_chars": 0,
                "total_audio_seconds": 0,
                "failed_requests": 0,
                "retry_count": 0,
                "connection_reuses": 0,
                "connection_creates": 0,
            }.items():
                if key not in self.cost_tracker:
                    self.cost_tracker[key] = val

        # 引用上文缓存（保存最近几句作为上下文）
        self._context_cache: Dict[str, List[str]] = {
            "A": [],
            "B": [],
        }
        self._max_context_lines = 2  # 最多引用前2句

    def _check_tts_v2(self) -> bool:
        """检查是否使用TTS 2.0（用于判断可用功能）"""
        voice_info = self.voice_config.get_voice_info(self.host_a_voice)
        if voice_info:
            # TTS 2.0 的 type 通常是 uranus 或特定的 2.0 标识
            voice_type = voice_info.get("type", "").lower()
            return voice_type == "uranus" or "2.0" in voice_info.get("name", "")
        return False

    def _get_recommended_voices(self) -> str:
        """获取推荐的音色列表（用于错误提示）"""
        try:
            # 从配置中获取推荐音色对
            pairs = self.voice_config._config.get("recommended_pairs", {})
            voices = self.voice_config._config.get("voices", {})

            lines = []
            # 显示推荐配置
            for pair_name, pair_config in pairs.items():
                host_a = pair_config.get("host_a", "")
                host_b = pair_config.get("host_b", "")
                desc = pair_config.get("description", "")

                # 获取音色名称
                a_name = voices.get(host_a, {}).get("name", host_a)
                b_name = voices.get(host_b, {}).get("name", host_b)

                lines.append(f"  [{pair_name}] {desc}")
                lines.append(f"    A: {host_a} ({a_name})")
                lines.append(f"    B: {host_b} ({b_name})")

            return "\n".join(lines) if lines else "  (无法读取音色配置)"
        except Exception as e:
            return f"  (读取配置失败: {e})"

    def _get_connection_for_speaker(self, speaker: str) -> websocket.WebSocket:
        """
        获取或创建说话人的WebSocket连接（链接复用）

        Args:
            speaker: 说话人标识 ("A" 或 "B")

        Returns:
            可用的WebSocket连接
        """
        # 检查现有连接是否可用
        if speaker in self._connection_pools:
            ws = self._connection_pools[speaker]
            try:
                # 简单检查连接状态（发送ping）
                ws.ping()
                self.cost_tracker["connection_reuses"] += 1
                # 递增sequence计数器
                self._sequence_counters[speaker] = self._sequence_counters.get(speaker, 1) + 1
                return ws
            except:
                # 连接已失效，关闭并移除
                try:
                    ws.close()
                except:
                    pass
                del self._connection_pools[speaker]
                self._sequence_counters[speaker] = 1  # 重置sequence

        # 创建新连接
        ws = self._create_connection()
        self._connection_pools[speaker] = ws
        self._sequence_counters[speaker] = 1  # 初始化sequence
        self.cost_tracker["connection_creates"] += 1
        return ws

    def _create_connection(self) -> websocket.WebSocket:
        """创建新的WebSocket连接"""
        import time

        timestamp = str(int(time.time()))
        signature = self._generate_signature(timestamp)

        ws_header = {
            "X-Api-App-Key": self.app_id,
            "X-Api-Access-Key": self.access_token,
            "X-Api-Resource-Id": self.resource_id,
        }

        if signature:
            ws_header["X-Api-Signature"] = signature
            ws_header["X-Api-Timestamp"] = timestamp

        return websocket.create_connection(
            self.WS_URL,
            header=ws_header,
            timeout=30,
        )

    def _close_all_connections(self):
        """关闭所有WebSocket连接（清理资源）"""
        for speaker, ws in list(self._connection_pools.items()):
            try:
                ws.close()
            except:
                pass
        self._connection_pools.clear()
        self._sequence_counters.clear()

    def _update_context_cache(self, speaker: str, text: str):
        """更新引用上文缓存"""
        cache = self._context_cache.get(speaker, [])
        cache.append(text)
        # 只保留最近几句
        if len(cache) > self._max_context_lines:
            cache = cache[-self._max_context_lines:]
        self._context_cache[speaker] = cache

    def _get_context_text(self, speaker: str) -> Optional[str]:
        """
        获取引用上文内容

        Returns:
            上文内容（多句用换行连接），如果没有则返回None
        """
        if not self.enable_context:
            return None

        cache = self._context_cache.get(speaker, [])
        if not cache:
            return None

        # 将缓存的上文用换行连接
        return "\n".join(cache)

    def _synthesize_with_retry(
        self,
        text: str,
        voice_id: str,
        speaker: str,
        section_id: Optional[str] = None,
    ) -> Tuple[bytes, str]:
        """
        带重试机制的合成调用

        Returns:
            (音频数据, session_id)
        """
        last_exception = None

        for attempt in range(self.MAX_RETRIES):
            try:
                result = self._synthesize_line(
                    text=text,
                    voice_id=voice_id,
                    speaker=speaker,
                    section_id=section_id,
                )
                return result
            except Exception as e:
                last_exception = e
                self.cost_tracker["retry_count"] += 1

                # 判断是否可重试
                error_msg = str(e).lower()
                is_retryable = any([
                    "timeout" in error_msg,
                    "connection" in error_msg,
                    "websocket" in error_msg,
                    "network" in error_msg,
                    "eof" in error_msg,
                ])

                if not is_retryable:
                    break  # 不可重试的错误直接抛出

                if attempt < self.MAX_RETRIES - 1:
                    # 指数退避延迟
                    delay = self.RETRY_DELAY_BASE * (2 ** attempt)
                    print(f"  [TTS Retry] 第{attempt + 1}次重试，等待{delay}s...")
                    time.sleep(delay)

                    # 重试前清理连接，强制重建
                    if speaker in self._connection_pools:
                        try:
                            self._connection_pools[speaker].close()
                        except:
                            pass
                        del self._connection_pools[speaker]

        self.cost_tracker["failed_requests"] += 1

        # 改进错误提示：针对 resource mismatch 提供有用信息
        error_str = str(last_exception).lower()
        if "resource" in error_str and "mismatch" in error_str:
            # 获取推荐音色列表
            recommended_voices = self._get_recommended_voices()
            helpful_msg = (
                f"\n[TTS Error] 音色ID '{voice_id}' 无效或不可用。\n"
                f"\n推荐使用的音色ID格式（从 config/tts_voices.json）：\n"
                f"{recommended_voices}\n"
                f"\n注意：\n"
                f"- 不要直接使用 BV001/BV005 等旧版标识\n"
                f"- 应使用完整的 voice_type，如 'zh_male_sophie_uranus_bigtts'\n"
                f"- 查看 api/TTS-voice-list.json 获取完整列表"
            )
            print(helpful_msg)
            raise RuntimeError(helpful_msg) from last_exception

        raise RuntimeError(f"TTS合成失败（已重试{self.MAX_RETRIES}次）: {last_exception}")

    def _generate_signature(self, timestamp: str) -> str:
        """生成请求签名 (HMAC-SHA256)"""
        import hmac
        import hashlib

        if not self.secret_key:
            return ""

        # 签名格式：HMAC-SHA256(AppId + Timestamp, SecretKey)
        sign_str = f"{self.app_id}{timestamp}"
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def generate_dual_audio(
        self,
        script: ScriptVersion,
        output_path: Path,
        persona_config: Optional[Dict] = None,
        progress_callback: Optional[callable] = None,
    ) -> Path:
        """
        生成双声道音频，使用 section_id 上下文模式逐句合成
        优化：链接复用、重试机制、引用上文、成本统计

        Args:
            script: 播客脚本
            output_path: 输出文件路径
            persona_config: Persona 配置（用于选择音色）
            progress_callback: 进度回调函数 (current, total)

        Returns:
            生成的音频文件路径
        """
        import time

        if not self.access_token:
            raise ValueError(
                "Volcano TTS access token not configured. "
                "Set VOLCANO_TTS_ACCESS_TOKEN environment variable."
            )

        # 根据 persona 选择音色
        if persona_config:
            self._select_voices_from_persona(persona_config)
            # 重新检查TTS版本
            self._is_tts_v2 = self._check_tts_v2()
            self.enable_context = self.enable_context and self._is_tts_v2

        total_lines = len(script.lines)
        start_time = time.time()

        # 逐句合成，保持对话顺序
        audio_segments: List[Tuple[AudioSegment, str]] = []
        raw_audio_chunks: List[bytes] = []  # 备选：原始MP3数据

        print(f"[TTS] 开始生成 {total_lines} 句音频，上下文功能: {'开启' if self.enable_context else '关闭'}")

        failed_lines = []
        try:
            for idx, line in enumerate(script.lines):
                speaker = line.speaker
                voice_id = self.host_a_voice if speaker == "A" else self.host_b_voice

                # 进度回调
                if progress_callback:
                    progress_callback(idx + 1, total_lines)
                elif (idx + 1) % 10 == 0 or idx == 0:
                    print(f"  [TTS] 进度: {idx + 1}/{total_lines} ({(idx + 1) * 100 // total_lines}%)")

                # 获取上下文 session_id
                section_id = self._get_last_session_id(speaker)

                # 更新成本统计
                self.cost_tracker["total_requests"] += 1
                self.cost_tracker["total_chars"] += len(line.text)

                # 合成单句（带重试）
                try:
                    audio_data, session_id = self._synthesize_with_retry(
                        text=line.text,
                        voice_id=voice_id,
                        speaker=speaker,
                        section_id=section_id,
                    )
                except Exception as e:
                    print(f"  [TTS Error] 第{idx + 1}句合成失败: {e}")
                    failed_lines.append(idx + 1)
                    if _HAS_FFMPEG:
                        # 插入3秒静音占位，保持时间线对齐
                        silent = AudioSegment.silent(duration=3000, frame_rate=24000)
                        audio_segments.append((silent, speaker))
                    continue

                # 更新上下文链
                self._update_session_chain(speaker, session_id)

                # 更新引用上文缓存（用于TTS 2.0的引用上文功能）
                self._update_context_cache(speaker, line.text)

                # 保存原始数据（备选方案）
                raw_audio_chunks.append(audio_data)

                # 尝试加载音频（需要ffmpeg）
                if _HAS_FFMPEG:
                    try:
                        audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_data))
                        audio_segments.append((audio_segment, speaker))
                    except Exception as e:
                        print(f"Warning: Could not decode audio for line {idx + 1}: {e}")

        finally:
            # 确保清理所有连接
            self._close_all_connections()

        # 计算总耗时和预估音频时长
        elapsed = time.time() - start_time
        estimated_duration = len(audio_segments) * 3 if audio_segments else 0  # 假设每句3秒
        self.cost_tracker["total_audio_seconds"] = estimated_duration

        # 保存输出
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if failed_lines:
            print(f"  [TTS Warning] 共 {len(failed_lines)} 句合成失败: {failed_lines}")

        print(f"[TTS] 合成完成: {total_lines}句, 耗时{elapsed:.1f}s, 连接创建{self.cost_tracker['connection_creates']}次, 复用{self.cost_tracker['connection_reuses']}次")

        if audio_segments and _HAS_FFMPEG:
            # 使用 pydub 合并为双声道立体声
            merged_audio = self._merge_to_stereo_sequential(audio_segments)
            merged_audio.export(str(output_path), format="mp3")
        elif raw_audio_chunks:
            # 备选：直接连接MP3数据（单声道，按顺序拼接）
            print("Warning: ffmpeg not available, using sequential MP3 concatenation (mono)")
            with open(output_path, 'wb') as f:
                for chunk in raw_audio_chunks:
                    f.write(chunk)
        else:
            raise RuntimeError("No audio data to save")

        return output_path

    def _select_voices_from_persona(self, persona_config: Dict):
        """
        根据 persona 选择音色
        从 expression.voice_id 直接读取，不再进行关键词匹配
        """
        host_a_voice_id = None
        host_b_voice_id = None

        # 解析 host_a 的 voice_id
        if "host_a" in persona_config:
            host_a = persona_config["host_a"]
            if "expression" in host_a:
                host_a_voice_id = host_a["expression"].get("voice_id")
            # 兼容旧字段
            if not host_a_voice_id:
                host_a_voice_id = host_a.get("voice_id")

        # 解析 host_b 的 voice_id
        if "host_b" in persona_config:
            host_b = persona_config["host_b"]
            if "expression" in host_b:
                host_b_voice_id = host_b["expression"].get("voice_id")
            # 兼容旧字段
            if not host_b_voice_id:
                host_b_voice_id = host_b.get("voice_id")

        # 应用 voice_id（如果存在且有效）
        if host_a_voice_id and self.voice_config.get_voice_info(host_a_voice_id):
            self.host_a_voice = host_a_voice_id

        if host_b_voice_id and self.voice_config.get_voice_info(host_b_voice_id):
            self.host_b_voice = host_b_voice_id

        # 更新资源ID
        self.resource_id = self.voice_config.get_resource_id(self.host_a_voice)

    def _match_voice_by_style(self, expression_style: str, gender: str) -> str:
        """
        根据 expression_style 关键词匹配音色

        Args:
            expression_style: 表达风格描述
            gender: 性别 (male/female)

        Returns:
            匹配的音色ID
        """
        style_lower = expression_style.lower()

        # 获取对应性别的所有音色
        voices = self.voice_config.list_voices(gender=gender)
        if not voices:
            # 回退到默认
            default_a, default_b = self.voice_config.get_default_voices()
            return default_a if gender == "male" else default_b

        # 关键词匹配映射
        keyword_mapping = {
            "专业": ["professional", "知性", "沉稳", "理性"],
            "活泼": ["活泼", "开朗", "轻松", "俏皮"],
            "温柔": ["温柔", "甜美", "亲和", "温暖"],
            "沉稳": ["沉稳", "成熟", "专业", "知性"],
            "幽默": ["幽默", "风趣", "搞笑", "搞怪"],
            "年轻": ["年轻", "少年", "活力", "青春"],
        }

        # 尝试匹配
        for category, keywords in keyword_mapping.items():
            if any(kw in style_lower for kw in keywords):
                # 找到该类别下的第一个匹配音色
                for voice in voices:
                    desc = voice.get("description", "")
                    if category in desc or any(kw in desc for kw in keywords):
                        return voice["voice_id"]

        # 无匹配时返回默认
        default_a, default_b = self.voice_config.get_default_voices()
        return default_a if gender == "male" else default_b

    def _get_last_session_id(self, speaker: str) -> Optional[str]:
        """获取说话人最后一个 session_id"""
        chain = self._session_chains.get(speaker, [])
        return chain[-1] if chain else None

    def _update_session_chain(self, speaker: str, session_id: str):
        """更新说话人的 session_id 链"""
        if speaker not in self._session_chains:
            self._session_chains[speaker] = []
        self._session_chains[speaker].append(session_id)

    def _synthesize_line(
        self,
        text: str,
        voice_id: str,
        speaker: str,
        section_id: Optional[str] = None,
    ) -> Tuple[bytes, str]:
        """
        合成单句音频（优化版）
        - 使用链接复用
        - 支持引用上文（TTS 2.0）
        - 改进的超时处理

        Args:
            text: 要合成的文本
            voice_id: 音色 ID
            speaker: 说话人标识
            section_id: 上下文 session_id（可选）

        Returns:
            (音频数据, 本次 session_id)
        """
        # 构建请求参数
        request_params = {
            "text": text,
            "speaker": voice_id,
            "audio_params": {
                "format": "mp3",
                "sample_rate": 24000,
            },
        }

        # 构建additions（section_id + context）
        additions = {}
        if section_id:
            additions["section_id"] = section_id

        # TTS 2.0 特有：引用上文功能
        if self.enable_context:
            context_text = self._get_context_text(speaker)
            if context_text:
                additions["context"] = context_text

        if additions:
            request_params["additions"] = json.dumps(additions)

        # WebSocket 二进制帧协议 (V3)
        header = bytes([
            0x11,  # Version 1, Header size 4
            0x11,  # Message type 1, Flags 1
            0x00,  # JSON serialization (0), no compression
            0x00,  # Reserved
        ])

        # 构建完整请求
        request_data = {
            "user": {"uid": f"user_{speaker}"},
            "req_params": request_params,
        }

        payload = json.dumps(request_data, ensure_ascii=False).encode("utf-8")
        payload_size = len(payload)

        # 使用链接复用获取连接（会递增sequence计数器）
        ws = self._get_connection_for_speaker(speaker)
        sequence = self._sequence_counters.get(speaker, 1)

        # 完整帧：Header (4) + Sequence (4) + Payload size (4) + Payload
        frame = header + struct.pack(">I", sequence) + struct.pack(">I", payload_size) + payload

        # WebSocket 通信
        audio_chunks = []
        session_id = None

        try:
            # 发送请求帧
            ws.send_binary(frame)

            # 接收响应 - 优化超时策略
            # 根据文本长度动态调整超时
            text_len = len(text)
            base_timeout = 5
            # 长文本需要更长的处理时间
            dynamic_timeout = min(base_timeout + text_len // 50, 15)  # 最多15秒
            ws.settimeout(dynamic_timeout)

            consecutive_timeouts = 0
            max_timeouts = 3  # 增加容错次数
            response_count = 0
            last_audio_time = time.time()

            while True:
                try:
                    # 接收二进制帧
                    response = ws.recv()
                    response_count += 1
                    consecutive_timeouts = 0
                    last_audio_time = time.time()

                    if isinstance(response, bytes):
                        # 解析响应帧
                        audio_data, event_type, sid = self._parse_response_frame(response)

                        # 检查错误
                        if sid and sid.startswith("ERROR:"):
                            raise RuntimeError(f"TTS error: {sid[6:]}")

                        if sid and not session_id:
                            session_id = sid

                        if audio_data:
                            audio_chunks.append(audio_data)

                        # SessionFinished 事件表示合成完成 (event=152)
                        if event_type == 152:
                            break

                        # 检测空JSON结束信号：已收到音频数据后，收到带session_id但无event/audio的帧
                        if audio_chunks and sid and event_type is None and audio_data is None:
                            break

                    elif isinstance(response, str):
                        # 文本消息（可能是错误）
                        msg_data = json.loads(response)
                        if msg_data.get("code") != 20000000:
                            raise RuntimeError(f"TTS error: {msg_data}")

                except websocket.WebSocketTimeoutException:
                    consecutive_timeouts += 1
                    # 如果已经收到音频数据，可能是正常结束
                    if audio_chunks and (time.time() - last_audio_time) > dynamic_timeout:
                        break
                    if consecutive_timeouts >= max_timeouts:
                        # 连接可能已失效，标记为需要重建
                        if speaker in self._connection_pools:
                            del self._connection_pools[speaker]
                        break

        except Exception as e:
            # 发生错误时，标记连接为失效
            if speaker in self._connection_pools:
                try:
                    self._connection_pools[speaker].close()
                except:
                    pass
                del self._connection_pools[speaker]
            raise

        if not audio_chunks:
            raise RuntimeError("No audio data received from TTS")

        # 合并音频数据
        full_audio = b"".join(audio_chunks)

        return full_audio, session_id or ""

    def _parse_response_frame(self, frame: bytes) -> Tuple[Optional[bytes], Optional[int], Optional[str]]:
        """
        解析 WebSocket 响应帧

        Returns:
            (音频数据, 事件类型, session_id)
        """
        if len(frame) < 12:
            return None, None, None

        # 解析 Header (4) + Sequence (4) + Size (4)
        # 注意: payload_size 字段有时只包含 UUID 长度，忽略它，直接使用 frame[12:]
        payload = frame[12:]

        # 尝试解析为JSON
        try:
            data = json.loads(payload.decode("utf-8"))

            # 检查错误
            if "error" in data:
                return None, None, f"ERROR:{data['error']}"

            # 提取事件类型
            event_type = data.get("event")
            if event_type is not None:
                event_type = int(event_type)

            # 提取session_id
            session_id = data.get("session_id")

            return None, event_type, session_id

        except (json.JSONDecodeError, UnicodeDecodeError):
            # 检查是否以UUID开头 (所有响应都有的session_id前缀)
            if len(payload) >= 36 and payload[8] == ord('-') and payload[13] == ord('-'):
                potential_uuid = payload[:36].decode("utf-8", errors="ignore")
                if potential_uuid.count('-') == 4:
                    session_id = potential_uuid
                    remaining = payload[36:]

                    # 如果只有UUID，返回session_id
                    if len(remaining) == 0:
                        return None, None, session_id

                    # 跳过可能的填充字节，寻找JSON开始
                    found_json = False
                    for offset in range(0, min(20, len(remaining))):
                        if remaining[offset:offset+1] == b'{':
                            try:
                                data = json.loads(remaining[offset:].decode("utf-8"))
                                event_type = data.get("event")
                                if event_type is not None:
                                    event_type = int(event_type)
                                if data.get("session_id"):
                                    session_id = data["session_id"]
                                return None, event_type, session_id
                            except:
                                pass
                            found_json = True
                            break

                    # 如果能提取UUID但后面不是JSON，剩余部分是音频数据
                    if not found_json:
                        # 清理音频数据：去除前面可能的零字节或填充
                        audio_data = self._clean_audio_data(remaining)
                        return audio_data, None, session_id

            # 纯音频数据 (不以UUID开头) - 同样需要清理
            audio_data = self._clean_audio_data(payload)
            return audio_data, None, None

    def _clean_audio_data(self, data: bytes) -> bytes:
        """
        清理音频数据，去除非MP3格式的填充字节
        MP3 帧头以 0xFF 0xFB 或 0xFF 0xF3 或 0xFF 0xF2 开头
        """
        if len(data) < 4:
            return data

        # MP3 帧同步字节的几种模式
        mp3_sync_patterns = [b'\xff\xfb', b'\xff\xf3', b'\xff\xf2', b'\xff\xfa']

        # 查找第一个MP3帧头位置
        for i in range(min(100, len(data) - 2)):  # 最多检查前100字节
            if data[i:i+2] in mp3_sync_patterns:
                if i > 0:
                    return data[i:]
                break

        return data

    def _merge_to_stereo_sequential(
        self,
        audio_segments: List[Tuple[AudioSegment, str]],
    ) -> AudioSegment:
        """
        按时间线合并音频为立体声

        Args:
            audio_segments: [(音频片段, 说话人), ...]

        Returns:
            合并后的立体声音频
        """
        # 创建空白立体声音频
        total_duration = sum(len(seg) for seg, _ in audio_segments)
        stereo_audio = AudioSegment.silent(duration=total_duration, frame_rate=24000)
        stereo_audio = stereo_audio.set_channels(2)

        current_pos = 0

        for segment, speaker in audio_segments:
            # 转换为单声道
            segment = segment.set_channels(1)

            # 根据说话人分配到左/右声道
            if speaker == "A":
                # A 在左声道
                stereo_segment = AudioSegment.from_mono_audiosegments(segment, AudioSegment.silent(duration=len(segment)))
            else:
                # B 在右声道
                stereo_segment = AudioSegment.from_mono_audiosegments(AudioSegment.silent(duration=len(segment)), segment)

            # 叠加到总音频
            stereo_audio = stereo_audio.overlay(stereo_segment, position=current_pos)
            current_pos += len(segment)

        return stereo_audio


def generate_dual_audio(
    script: ScriptVersion,
    output_path: str,
    persona_config: Optional[Dict] = None,
) -> str:
    """
    便捷函数：生成双声道音频

    Args:
        script: 播客脚本
        output_path: 输出文件路径
        persona_config: Persona 配置（用于选择音色）

    Returns:
        生成的音频文件路径
    """
    controller = VolcanoTTSController()
    result_path = controller.generate_dual_audio(
        script, Path(output_path), persona_config
    )
    return str(result_path)

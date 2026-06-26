"""
Qwen3-TTS Provider

使用qwen-tts包加载和使用Qwen3-TTS模型进行语音合成。
"""

import os
import torch
import numpy as np
from typing import List, Optional
from pathlib import Path
from .tts_base import (
    TTSProvider, Voice, AudioData, Emotion, Gender,
    TTSError, TTSNotAvailableError, TTSSynthesisError
)
from utils.logger import logger
from .tts_factory import register_provider


@register_provider
class Qwen3TTSProvider(TTSProvider):
    """
    Qwen3-TTS Provider
    
    使用qwen-tts包加载和使用Qwen3-TTS模型进行语音合成。
    支持从HuggingFace或ModelScope下载模型。
    """
    
    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
        model_dir: Optional[str] = None,
        device: str = "auto",
        use_gpu: bool = True
    ):
        """
        初始化Qwen3-TTS Provider
        
        Args:
            model_name: 模型名称（HuggingFace格式）
            model_dir: 模型本地目录（如果已下载）
            device: 设备类型（auto/cuda/cpu）
            use_gpu: 是否使用GPU
        """
        self.model_name = model_name
        
        # 如果提供了model_dir，使用提供的；否则自动检测本地模型
        if model_dir:
            self.model_dir = Path(model_dir)
        else:
            # 自动检测本地模型目录
            self.model_dir = self._detect_local_model(model_name)
        
        self.device = self._get_device(device, use_gpu)
        self.model = None
        self._voices_cache: Optional[List[Voice]] = None
    
    def _detect_local_model(self, model_name: str) -> Optional[Path]:
        """
        自动检测本地CustomVoice模型
        
        只检测CustomVoice模型，不检测Base模型。
        
        Args:
            model_name: 模型名称
            
        Returns:
            Optional[Path]: 本地模型路径，如果未找到返回None
        """
        # 提取模型基础名称（去掉组织前缀）
        model_base = model_name.split('/')[-1]
        
        # 获取技能根目录（当前文件的上两级目录）
        skill_root = Path(__file__).parent.parent.resolve()
        
        # 只检测CustomVoice模型路径（扩展检测范围）
        possible_paths = [
            # 标准路径（基于传入的 model_name）
            Path(f"./models/{model_base}"),
            Path(f"./{model_base}"),
            Path.home() / ".cache" / "huggingface" / "hub" / f"models--{model_name.replace('/', '--')}",
            
            # 技能根目录下的模型路径
            skill_root / "models" / model_base,
            skill_root / model_base,
            
            # 技能根目录下的CustomVoice版本
            skill_root / "models" / "Qwen3-TTS-12Hz-0.6B-CustomVoice",
            skill_root / "models" / "Qwen3-TTS-12Hz-1.7B-CustomVoice",
            skill_root / "Qwen3-TTS-12Hz-0.6B-CustomVoice",
            skill_root / "Qwen3-TTS-12Hz-1.7B-CustomVoice",
            
            # 当前工作目录下的模型路径
            Path("./models/Qwen3-TTS-12Hz-0.6B-CustomVoice"),
            Path("./models/Qwen3-TTS-12Hz-1.7B-CustomVoice"),
            Path("./Qwen3-TTS-12Hz-0.6B-CustomVoice"),
            Path("./Qwen3-TTS-12Hz-1.7B-CustomVoice"),
            
            # 上级目录的模型路径
            Path("../models/Qwen3-TTS-12Hz-0.6B-CustomVoice"),
            Path("../models/Qwen3-TTS-12Hz-1.7B-CustomVoice"),
            Path("../Qwen3-TTS-12Hz-0.6B-CustomVoice"),
            Path("../Qwen3-TTS-12Hz-1.7B-CustomVoice"),
            
            # 上两级目录的模型路径
            Path("../../models/Qwen3-TTS-12Hz-0.6B-CustomVoice"),
            Path("../../models/Qwen3-TTS-12Hz-1.7B-CustomVoice"),
            Path("../../Qwen3-TTS-12Hz-0.6B-CustomVoice"),
            Path("../../Qwen3-TTS-12Hz-1.7B-CustomVoice"),
            
            # 用户主目录下的常见模型路径
            Path.home() / "models" / "Qwen3-TTS-12Hz-0.6B-CustomVoice",
            Path.home() / "models" / "Qwen3-TTS-12Hz-1.7B-CustomVoice",
            Path.home() / ".models" / "Qwen3-TTS-12Hz-0.6B-CustomVoice",
            Path.home() / ".models" / "Qwen3-TTS-12Hz-1.7B-CustomVoice",
            
            # HuggingFace缓存路径（CustomVoice版本）
            Path.home() / ".cache" / "huggingface" / "hub" / "models--Qwen--Qwen3-TTS-12Hz-0.6B-CustomVoice",
            Path.home() / ".cache" / "huggingface" / "hub" / "models--Qwen--Qwen3-TTS-12Hz-1.7B-CustomVoice",
        ]
        
        for path in possible_paths:
            if path.exists() and (path / "config.json").exists():
                logger.info(f"发现本地模型: {path}")
                return path
        
        return None
    
    def _get_device(self, device: str, use_gpu: bool) -> str:
        """获取设备类型"""
        if device == "auto":
            if use_gpu:
                if torch.cuda.is_available():
                    return "cuda"
            return "cpu"
        return device
    
    @property
    def name(self) -> str:
        """提供商名称"""
        return "Qwen3-TTS"
    
    @property
    def supported_languages(self) -> List[str]:
        """支持的语言列表"""
        return ["zh-CN", "en-US", "ja-JP", "ko-KR", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "ru-RU"]
    
    async def load_model(self):
        """加载模型"""
        if self.model is not None:
            return
        
        try:
            from qwen_tts import Qwen3TTSModel
            
            if self.model_dir and self.model_dir.exists():
                model_path = str(self.model_dir)
            else:
                model_path = self.model_name
            
            logger.info(f"正在加载模型: {model_path}")
            logger.info(f"使用设备: {self.device}")
            
            # 确定dtype
            if self.device == "cuda":
                dtype = torch.bfloat16
            else:
                dtype = torch.float32
            
            self.model = Qwen3TTSModel.from_pretrained(
                model_path,
                device_map=self.device,
                dtype=dtype,
            )
            
            logger.info("模型加载完成")
            
        except Exception as e:
            raise TTSError(f"模型加载失败: {str(e)}") from e
    
    def _is_customvoice_model(self, model_path: Path) -> bool:
        """
        检查指定路径是否是CustomVoice版本模型
        
        Args:
            model_path: 模型路径
            
        Returns:
            bool: 如果是CustomVoice版本返回True
        """
        if not model_path or not model_path.exists():
            return False
        
        path_str = str(model_path).lower()
        # 检查路径名是否包含CustomVoice
        if "customvoice" in path_str:
            return True
        
        # 检查config.json中的模型类型
        config_file = model_path / "config.json"
        if config_file.exists():
            try:
                import json
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    model_type = config.get("model_type", "")
                    # 检查模型配置中是否有CustomVoice特征
                    if "custom" in model_type.lower():
                        return True
            except:
                pass
        
        return False
    
    async def check_availability(self) -> bool:
        """
        检查模型是否可用
        
        优先检查本地CustomVoice模型，如果本地没有则检查是否可以在线下载。
        
        Returns:
            bool: 如果CustomVoice模型已下载或可以下载返回True
        """
        try:
            # 尝试导入qwen_tts
            from qwen_tts import Qwen3TTSModel
            
            # 1. 优先检查本地模型（必须是CustomVoice版本）
            if self.model_dir and self.model_dir.exists():
                # 验证是否是CustomVoice版本
                if self._is_customvoice_model(self.model_dir):
                    # 检查必要的模型文件是否存在
                    config_file = self.model_dir / "config.json"
                    if config_file.exists():
                        logger.info(f"本地CustomVoice模型已就绪: {self.model_dir}")
                        return True
                else:
                    logger.warning(f"检测到非CustomVoice模型: {self.model_dir}")
                    logger.warning("需要CustomVoice版本才能使用全部功能")
            
            # 2. 重新检测本地CustomVoice模型（可能在初始化后下载的）
            local_model = self._detect_local_model(self.model_name)
            if local_model:
                self.model_dir = local_model
                return True
            
            # 3. 检查是否可以在线下载
            from transformers import AutoConfig
            try:
                AutoConfig.from_pretrained(self.model_name)
                logger.info(f"本地CustomVoice模型未找到，可以在线下载: {self.model_name}")
                return False  # 返回False，让调用者决定是否下载
            except:
                logger.error(f"模型不可用: {self.model_name}")
                return False
                
        except ImportError:
            logger.warning("qwen-tts包未安装，请运行: pip install qwen-tts")
            return False
        except Exception as e:
            logger.error(f"检查模型可用性失败: {e}")
            return False
    
    async def get_voices(self) -> List[Voice]:
        """
        获取可用音色列表
        
        Returns:
            List[Voice]: 音色列表
        """
        if self._voices_cache is not None:
            return self._voices_cache
        
        # Qwen3-TTS-12Hz-0.6B-CustomVoice模型支持9种预设音色
        voices = [
            Voice(
                id="xiaoxiao",
                name="Vivian (晓晓)",
                gender=Gender.FEMALE,
                language="zh-CN",
                description="明亮、略带锋芒的年轻女声，适合新闻播报"
            ),
            Voice(
                id="serena",
                name="Serena (晓辰)",
                gender=Gender.FEMALE,
                language="zh-CN",
                description="温暖、温柔的年轻女声，适合娱乐新闻"
            ),
            Voice(
                id="uncle_fu",
                name="Uncle Fu (云健)",
                gender=Gender.MALE,
                language="zh-CN",
                description="经验丰富的男声，低沉醇厚，适合财经资讯"
            ),
            Voice(
                id="dylan",
                name="Dylan (晓宇)",
                gender=Gender.MALE,
                language="zh-CN",
                description="年轻的北京男声，清晰自然，适合科技资讯"
            ),
            Voice(
                id="eric",
                name="Eric",
                gender=Gender.MALE,
                language="zh-CN",
                description="活泼的成都男声，略带沙哑的明亮感，适合轻松话题"
            ),
            Voice(
                id="ryan",
                name="Ryan",
                gender=Gender.MALE,
                language="en-US",
                description="富有节奏感的男声，适合英文播报"
            ),
            Voice(
                id="aiden",
                name="Aiden",
                gender=Gender.MALE,
                language="en-US",
                description="阳光美式男声，中音清晰，适合英文内容"
            ),
            Voice(
                id="ono_anna",
                name="Ono Anna (晓雅)",
                gender=Gender.FEMALE,
                language="ja-JP",
                description="俏皮的日语女声，轻快灵动，适合日语内容"
            ),
            Voice(
                id="sohee",
                name="Sohee",
                gender=Gender.FEMALE,
                language="ko-KR",
                description="温暖的韩语女声，情感丰富，适合韩语内容"
            )
        ]
        
        self._voices_cache = voices
        return voices
    
    def _get_speaker_name(self, voice_id: str) -> str:
        """
        将voice_id映射到模型支持的speaker名称
        
        Args:
            voice_id: 音色ID
            
        Returns:
            str: 模型speaker名称
        """
        # Qwen3-TTS-12Hz-0.6B-CustomVoice支持的9种音色
        speaker_map = {
            "xiaoxiao": "Vivian",      # 女声，温柔
            "yunjian": "Uncle_Fu",     # 男声，沉稳
            "xiaochen": "Serena",      # 女声，活泼
            "xiaoyu": "Dylan",         # 男声，年轻
            "xiaoya": "Ono_Anna",      # 女声，知性
            "vivian": "Vivian",
            "serena": "Serena",
            "uncle_fu": "Uncle_Fu",
            "dylan": "Dylan",
            "eric": "Eric",
            "ryan": "Ryan",
            "aiden": "Aiden",
            "ono_anna": "Ono_Anna",
            "sohee": "Sohee",
        }
        return speaker_map.get(voice_id, "Vivian")  # 默认使用Vivian
    
    async def synthesize(
        self,
        text: str,
        voice_id: str = "xiaoxiao",
        emotion: str = "neutral",
        speed: float = 1.0,
        pitch: float = 1.0,
        **kwargs
    ) -> AudioData:
        """
        合成语音
        
        Args:
            text: 要合成的文本
            voice_id: 音色ID
            emotion: 情感类型
            speed: 语速（0.5-2.0）
            pitch: 音调（0.5-2.0）
            **kwargs: 额外参数
            
        Returns:
            AudioData: 音频数据
        """
        if not self.model:
            await self.load_model()
        
        try:
            # 获取speaker名称
            speaker = self._get_speaker_name(voice_id)
            
            # 确定语言
            language = "Chinese" if any('\u4e00' <= c <= '\u9fff' for c in text) else "English"
            
            # 构建instruct（情感控制）
            instruct = ""
            if emotion == "happy":
                instruct = "用开心的语气说"
            elif emotion == "sad":
                instruct = "用悲伤的语气说"
            elif emotion == "excited":
                instruct = "用兴奋的语气说"
            elif emotion == "calm":
                instruct = "用平静的语气说"
            
            logger.info(f"使用音色: {speaker}, 语言: {language}")
            if instruct:
                logger.info(f"情感指令: {instruct}")
            
            logger.info("正在合成中...")
            
            # 使用generate_custom_voice进行合成（CustomVoice模型）
            wavs, sr = self.model.generate_custom_voice(
                text=text,
                language=language,
                speaker=speaker,
                instruct=instruct if instruct else None,
            )
            
            # 转换为AudioData格式
            import soundfile as sf
            import io
            
            # 将numpy数组保存为wav字节
            buffer = io.BytesIO()
            sf.write(buffer, wavs[0], sr, format='WAV')
            buffer.seek(0)
            audio_bytes = buffer.read()
            
            audio_data = AudioData(
                data=audio_bytes,
                sample_rate=sr,
                format="wav",
                duration=len(wavs[0]) / sr
            )
            
            logger.info("合成完成!")
            
            return audio_data
            
        except Exception as e:
            raise TTSSynthesisError(f"语音合成失败: {str(e)}")
    
    async def download_model(self) -> bool:
        """
        下载模型（优先从国内源下载）
        
        尝试顺序：
        1. ModelScope（国内推荐，速度更快）
        2. HuggingFace（国际源）
        
        Returns:
            bool: 下载成功返回True
        """
        model_base = self.model_name.split('/')[-1]
        
        logger.info(f"正在下载模型: {self.model_name}")
        logger.info("将优先从国内源下载...")
        
        try:
            from modelscope import snapshot_download
            
            logger.info("尝试从 ModelScope 下载...")
            local_path = snapshot_download(
                'qwen/' + model_base.replace('-CustomVoice', ''),
                cache_dir='./models'
            )
            
            model_dir = Path(local_path)
            if not model_dir.exists():
                model_dir = Path('./models') / model_base
            
            if model_dir.exists():
                logger.info(f"模型下载完成: {model_dir}")
                self.model_dir = model_dir
                return True
                
        except Exception as e:
            logger.warning(f"ModelScope 下载失败: {e}")
        
        try:
            from huggingface_hub import snapshot_download
            
            logger.info("尝试从 HuggingFace 下载...")
            local_path = snapshot_download(
                repo_id=self.model_name,
                local_dir=f"./models/{model_base}",
                local_dir_use_symlinks=False
            )
            
            logger.info(f"模型下载完成: {local_path}")
            self.model_dir = Path(local_path)
            return True
            
        except Exception as e:
            logger.error(f"模型下载失败: {e}")
            logger.error("请尝试手动下载模型:")
            logger.error(f"# ModelScope（国内推荐）")
            logger.error(f"pip install modelscope")
            logger.error(f"python -c \"from modelscope import snapshot_download; snapshot_download('qwen/{model_base.replace('-CustomVoice', '')}', cache_dir='./models')\"")
            return False

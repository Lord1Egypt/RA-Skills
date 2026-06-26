"""
Cowork Mode - 与平台LLM协作

在LobsterAI/OpenClaw的cowork mode下使用：
1. 平台主对话LLM生成内容（支持Claude、GPT、Qwen等任意模型）
2. 本Skill只负责TTS合成

这样无需额外API密钥，直接利用平台的LLM能力。
"""

import sys
import json
import asyncio
import time
from pathlib import Path
from datetime import datetime

from utils.logger import logger

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from providers.qwen3_tts import Qwen3TTSProvider
from utils.audio_manager import AudioManager
from utils.content_filter import filter_for_tts


class CoworkRadioGenerator:
    """
    Cowork模式电台生成器
    
    与平台主对话LLM协作，LLM负责内容生成，本类负责TTS合成。
    支持Claude、GPT-4、Qwen、Llama等任意LLM模型。
    """
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.tts_provider = None
        self.audio_manager = AudioManager()
    
    async def init_tts(self, voice_id: str = "xiaoxiao", emotion: str = "neutral"):
        """
        初始化TTS
        
        Args:
            voice_id: 音色ID（支持: xiaoxiao, yunjian, xiaochen, xiaoyu, xiaoya）
            emotion: 情感
        """
        self.tts_provider = Qwen3TTSProvider()
        self.voice_id = voice_id
        self.emotion = emotion
        
        # 检查模型
        is_available = await self.tts_provider.check_availability()
        if not is_available:
            logger.warning("TTS模型未下载，请先下载模型")
            logger.warning("huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-CustomVoice")
            return False
        
        return True
    
    async def synthesize_content(
        self,
        title: str,
        content: str,
        topics: list = None,
        tags: list = None
    ) -> dict:
        """
        合成内容（由平台主对话LLM提供内容）
        
        Args:
            title: 标题（由LLM生成）
            content: 内容文本（由LLM生成）
            topics: 主题列表
            tags: 标签列表
            
        Returns:
            dict: 包含audio_url的结果
        """
        if not self.tts_provider:
            success = await self.init_tts()
            if not success:
                return {"error": "TTS初始化失败"}
        
        logger.info("正在合成语音...")
        logger.info(f"标题: {title}")
        logger.info(f"音色: {self.voice_id}")
        logger.info("预计需要10-30秒，请稍候...")
        progress_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        progress_idx = 0
        
        # 过滤内容标记
        tts_text = filter_for_tts(content)
        
        try:
            # TTS合成
            start_time = time.time()
            audio_data = await self.tts_provider.synthesize(
                text=tts_text,
                voice_id=self.voice_id,
                emotion=self.emotion
            )
            elapsed = time.time() - start_time
            
            # 显示完成
            logger.info(f"✓ 合成完成 ({elapsed:.1f}秒)")
            
            # 保存音频
            audio_url = self.audio_manager.save(
                audio_data=audio_data.data,
                user_id=self.user_id,
                format=audio_data.format,
                metadata={
                    'title': title,
                    'topics': topics or [],
                    'tags': tags or [],
                    'duration': audio_data.duration,
                    'voice': self.voice_id,
                    'mode': 'cowork',
                    'created_at': datetime.now().isoformat()
                },
                title=title
            )
            
            logger.info("语音合成成功!")
            logger.info(f"时长: {audio_data.duration:.1f}秒")
            logger.info(f"播放: {audio_url.get('relative_url', audio_url)}")
            logger.info(f"文件: {audio_url.get('absolute_path', 'N/A')}")
            
            return {
                'success': True,
                'title': title,
                'audio_url': audio_url.get('relative_url', audio_url),
                'absolute_path': audio_url.get('absolute_path', ''),
                'filename': audio_url.get('filename', ''),
                'duration': audio_data.duration,
                'voice': self.voice_id
            }
            
        except Exception as e:
            logger.error(f"合成失败: {e}")
            return {'error': str(e)}


# 便捷函数，供cowork mode直接调用
async def generate_radio_audio(
    title: str,
    content: str,
    voice_id: str = "xiaoxiao",
    emotion: str = "neutral",
    user_id: str = "default",
    output_location: str = "default"
) -> dict:
    """
    生成电台音频（cowork mode入口）
    
    由平台主对话LLM调用，传入生成的内容，返回音频URL。
    支持任意LLM：Claude、GPT-4、Qwen、Llama等。
    
    Args:
        title: 标题
        content: 内容（LLM生成）
        voice_id: 音色
        emotion: 情感
        user_id: 用户ID
        output_location: 输出位置 ("default", "desktop", "downloads")
        
    Returns:
        dict: 结果
    """
    generator = CoworkRadioGenerator(user_id)
    generator.audio_manager.set_output_location(output_location)
    await generator.init_tts(voice_id, emotion)
    
    result = await generator.synthesize_content(title, content)
    return result


# 供LobsterAI/OpenClaw直接调用的函数
async def cowork_generate_async(
    title: str,
    content: str,
    voice: str = "xiaoxiao",
    emotion: str = "neutral",
    output_location: str = "default"
) -> dict:
    """
    Cowork mode主入口（异步版本）
    
    LobsterAI/OpenClaw可以直接调用此函数。
    支持任意平台主对话LLM：Claude、GPT-4、Qwen、Llama等。
    
    使用示例（在对话中）：
    ```
    # 平台主对话LLM生成内容（任意模型）
    content = "生成财经新闻内容..."
    
    # 调用Skill合成语音
    result = await cowork_generate_async(
        title="今日财经",
        content=content,
        voice="yunjian",
        output_location="downloads"  # 可选: "default", "desktop", "downloads"
    )
    ```
    
    Args:
        title: 标题
        content: 内容
        voice: 音色ID
        emotion: 情感
        output_location: 输出位置 ("default", "desktop", "downloads")
        
    Returns:
        dict: 包含 success, audio_url, absolute_path, filename, duration, voice 等字段
    """
    result = await generate_radio_audio(
        title=title,
        content=content,
        voice_id=voice,
        emotion=emotion,
        output_location=output_location
    )
    
    return result


def cowork_generate(
    title: str,
    content: str,
    voice: str = "xiaoxiao",
    emotion: str = "neutral",
    output_location: str = "default"
) -> str:
    """
    Cowork mode主入口（同步版本）
    
    LobsterAI/OpenClaw可以直接调用此函数。
    支持任意平台主对话LLM：Claude、GPT-4、Qwen、Llama等。
    
    使用示例（在对话中）：
    ```
    # 平台主对话LLM生成内容（任意模型）
    content = "生成财经新闻内容..."
    
    # 调用Skill合成语音
    result = cowork_generate(
        title="今日财经",
        content=content,
        voice="yunjian",
        output_location="downloads"  # 可选: "default", "desktop", "downloads"
    )
    print(result)
    ```
    
    Args:
        title: 标题
        content: 内容
        voice: 音色ID
        emotion: 情感
        output_location: 输出位置 ("default", "desktop", "downloads")
        
    Returns:
        str: 音频URL或错误信息
    """
    # 检查是否有运行中的 event loop
    has_loop = False
    try:
        _ = asyncio.get_running_loop()
        has_loop = True
    except RuntimeError:
        has_loop = False
    
    if has_loop:
        # 有运行中的 event loop，抛出错误提示用户使用异步版本
        raise RuntimeError(
            "cowork_generate() 不能在已有 event loop 中调用。"
            "请使用 'await cowork_generate_async(...)' 代替。"
        )
    
    # 没有运行中的 event loop，可以创建新的
    result = asyncio.run(generate_radio_audio(
        title=title,
        content=content,
        voice_id=voice,
        emotion=emotion,
        output_location=output_location
    ))
    
    if result.get('success'):
        return result['audio_url']
    else:
        return f"错误: {result.get('error', '未知错误')}"


if __name__ == "__main__":
    # 测试cowork mode
    test_content = """
    欢迎收听今天的财经早报。
    
    首先，股市方面，昨日A股三大指数集体收涨，沪指上涨0.5%。
    
    其次，宏观经济数据公布，三季度GDP同比增长4.9%，超出市场预期。
    
    最后，央行宣布降准0.25个百分点，释放流动性约5000亿元。
    
    以上就是今天的主要内容。
    """
    
    result = cowork_generate(
        title="今日财经早报",
        content=test_content,
        voice="yunjian"
    )
    
    logger.info(f"结果: {result}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""交互式会议纪要生成流程（飞书适配版）"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import List

# 设置 UTF-8 编码输出（Windows 兼容）
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加父目录到路径以导入 skill 脚本
script_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(script_dir))


def detect_hardware() -> dict:
    """检测硬件环境（GPU/CPU）"""
    try:
        import torch
        if torch.cuda.is_available():
            return {"has_gpu": True, "gpu_name": torch.cuda.get_device_name(0)}
    except ImportError:
        pass
    return {"has_gpu": False, "gpu_name": None}


def get_audio_duration(audio_path: str) -> float:
    """获取音频文件时长（秒）"""
    try:
        import wave
        with wave.open(str(audio_path), 'rb') as f:
            frames = f.getnframes()
            rate = f.getframerate()
            return frames / float(rate)
    except Exception:
        pass
    # Fallback: 使用文件大小估算（1MB ≈ 1分钟音频）
    try:
        file_size = Path(audio_path).stat().st_size / 1024 / 1024
        return file_size * 60
    except Exception:
        return 300  # 默认 5 分钟


# ASR 提供方定义（用于 --provider 参数）
ASR_PROVIDERS = {
    "local-base": "Whisper base（本地，快速）",
    "local-small": "Whisper small（本地，推荐）",
    "local-large-v3": "Whisper large-v3（本地，最高准确率）",
}


# Whisper 模型定义（与 transcribe_audio.py 保持一致）
WHISPER_MODELS = {
    "base": {
        "name": "Whisper base",
        "description": "基础模型，平衡速度与准确率",
        "size": "~140MB",
        "accuracy": "约 85%",
        "speed": "快（<2分钟/10分钟音频）",
        "use_case": "日常使用、快速预览"
    },
    "small": {
        "name": "Whisper small",
        "description": "小型模型，高准确率",
        "size": "~460MB",
        "accuracy": "约 90%",
        "speed": "中等（~5分钟/10分钟音频）",
        "use_case": "推荐日常使用，准确率足够"
    },
    "large-v3": {
        "name": "Whisper large-v3",
        "description": "最新大型模型，最高准确率",
        "size": "~3GB",
        "accuracy": "约 95%+",
        "speed": "慢（~15-30分钟/10分钟音频，GPU 可加速）",
        "use_case": "专业会议、长音频、最高准确率要求"
    }
}


class InteractiveMeetingNotes:
    """交互式会议纪要生成流程"""

    def __init__(self):
        self.audio_path = None
        self.provider = None
        self.selected_output = None
        self.memory_dir = Path.home() / ".workbuddy" / "memory"

    def print_options(self, options: List[str]) -> None:
        """打印带数字编号的选项列表"""
        for i, option in enumerate(options, 1):
            print(f"{i} - {option}")
        print("\n请回复数字：")

    def parse_choice(self, user_input: str, num_options: int) -> int | None:
        """解析用户输入的数字选项"""
        try:
            choice = int(user_input.strip())
            if 1 <= choice <= num_options:
                return choice
            return None
        except ValueError:
            return None

    def interactive_select(self, prompt: str, options: List[str]) -> int:
        """交互式选择选项"""
        print(f"\n{prompt}")
        self.print_options(options)
        print("💡 提示：输入 'q' 或 'exit' 可退出程序")

        while True:
            user_input = input().strip()
            
            # 支持退出命令
            if user_input.lower() in ['q', 'exit', 'quit', '退出']:
                print("\n👋 您已选择退出程序")
                sys.exit(0)
            
            choice = self.parse_choice(user_input, len(options))
            if choice is not None:
                return choice
            print("⚠️  输入无效，请输入 1-{} 之间的数字，或输入 'q' 退出".format(len(options)))

    def step_1_select_audio(self, audio_path: str | None = None) -> str:
        """步骤1：验证音频文件（用户已提供）"""
        print("\n" + "=" * 60)
        print("步骤 1/3：验证音频文件")
        print("=" * 60)

        if not audio_path:
            print("\n⚠️  未提供音频文件路径")
            print("   使用方式：python interactive_meeting_notes.py <音频文件路径>")
            print("   示例：python interactive_meeting_notes.py meeting.mp3")
            sys.exit(1)

        # 使用输入验证器检查音频路径
        from input_validator import InputValidator
        is_valid, error = InputValidator.validate_audio_path(audio_path)
        if not is_valid:
            print(f"\n⚠️  音频文件验证失败")
            print(f"   {error}")
            print(f"   支持的格式：.mp3, .m4a, .wav, .ogg")
            sys.exit(1)

        audio_file = Path(audio_path)

        print(f"\n✅ 音频文件：{audio_file.name}")
        print(f"   文件大小：{audio_file.stat().st_size / (1024*1024):.1f} MB")
        print(f"   文件路径：{audio_file}")

        return str(audio_file)

    def step_2_select_provider(self) -> str:
        """步骤2：选择转写方案"""
        print("\n" + "=" * 60)
        print("步骤 2/4：选择转写方案")
        print("=" * 60)

        # 硬件检测和音频时长
        hardware = detect_hardware()
        audio_duration = get_audio_duration(self.audio_path)
        duration_minutes = audio_duration / 60
        
        print(f"\n📊 音频信息:")
        print(f"   时长: {duration_minutes:.1f} 分钟")
        
        # 友好的硬件提示（去技术化）
        print(f"\n💻 设备状态:")
        if hardware["has_gpu"]:
            print(f"   ✅ 检测到高性能显卡，可使用高准确率大模型")
        else:
            print(f"   ⚠️  当前设备使用普通显卡，推荐使用快速模型")
        
        # 时间预估
        print(f"\n⏱️  预计转写时间:")
        if hardware["has_gpu"]:
            print(f"   • base 模型: 约 {duration_minutes * 0.2:.1f} 分钟（快速测试）")
            print(f"   • small 模型: 约 {duration_minutes * 0.5:.1f} 分钟（推荐）")
            print(f"   • large-v3 模型: 约 {duration_minutes * 0.8:.1f} 分钟（最高准确率）")
        else:
            print(f"   • base 模型: 约 {duration_minutes * 0.8:.1f} 分钟（快速测试）")
            print(f"   • small 模型: 约 {duration_minutes * 1.0:.1f} 分钟（推荐）")
            print(f"   • large-v3 模型: 约 {duration_minutes * 15.0:.1f} 分钟（不推荐）")

        # 显示本地转写选项
        print(f"\n🎙️  本地转写（完全免费，隐私安全，数据不上云）")
        print(f"   首次使用需要下载模型文件，请根据需求选择：")

        # 选择本地模型
        local_options = [
            "large-v3（最高准确率，约 3GB）",
            "small（高准确率，约 460MB）",
            "base（快速测试，约 140MB）"
        ]
        sub_choice = self.interactive_select("\n请选择本地转写模型：", local_options)

        # 映射到模型名称
        model_map = {1: "large-v3", 2: "small", 3: "base"}
        model_name = model_map[sub_choice]
        
        # large-v3 模型需要额外确认
        if model_name == "large-v3":
            print(f"\n⚠️  您选择了 large-v3 模型")
            print(f"   首次使用需要下载约 3GB 模型文件")
            print(f"   下载时间：5-15 分钟（取决于网络速度）")
            print(f"   适用场景：专业会议、长音频、最高准确率要求")
            print(f"\n💡 如果不确定，建议选择 small 模型（高准确率 + 快速下载）")
            
            confirm = input(f"\n确认下载并使用 large-v3 模型？(y/n): ").strip().lower()
            if confirm not in ["y", "yes", "是"]:
                print("❌ 已取消，建议使用 small 模型")
                model_name = "small"
        
        provider_key = f"local-{model_name}"
        print(f"\n✅ 已选择：{WHISPER_MODELS[model_name]['name']}")

        return provider_key

    def show_api_tutorial(self, provider_key: str) -> None:
        """显示 API 获取教程"""
        tutorials = {
            'feishu-api': """
【飞书 API 获取教程】
1. 访问飞书开放平台：https://open.feishu.cn/
2. 创建应用，获取 App ID 和 App Secret
3. 开通"语音识别"权限
4. 配置密钥到本工具：python scripts/config_asr.py --wizard
""",
            'tencent': """
【腾讯云 API 获取教程】
1. 访问腾讯云控制台：https://console.cloud.tencent.com/asr
2. 开通"录音文件识别"服务
3. 创建 API 密钥（SecretId / SecretKey）
4. 免费额度：每月 10 小时
5. 配置密钥：python scripts/config_asr.py --wizard
""",
            'aliyun-paraformer': """
【阿里云 Paraformer API 获取教程】
1. 访问阿里云百炼控制台：https://bailian.console.aliyun.com/
2. 左上角选择"中国内地（北京）"地域
3. 进入 API Key 管理（左侧菜单）
4. 创建 API Key，复制 sk- 开头的密钥
5. 免费额度：每月 10 小时
6. 配置密钥：python scripts/config_asr.py --wizard
""",
            'aliyun': """
【阿里云 ISI API 获取教程】
1. 访问阿里云控制台：https://nls-portal.console.aliyun.com/
2. 开通"Paraformer 语音识别"服务
3. 获取 AccessKey ID 和 AccessKey Secret
4. 免费额度：每月 5 小时
5. 配置密钥：python scripts/config_asr.py --wizard
""",
            'baidu': """
【百度 API 获取教程】
1. 访问百度AI开放平台：https://ai.baidu.com/tech/speech
2. 创建应用，获取 API Key 和 Secret Key
3. 免费额度：首次登录永久免费
4. 配置密钥：python scripts/config_asr.py --wizard
""",
            'huawei': """
【华为云 API 获取教程】
1. 访问华为云控制台：https://console.huaweicloud.com/sis
2. 开通"语音识别服务（SIS）"
3. 获取访问密钥（AK/SK）
4. 计费方式：按需付费
5. 配置密钥：python scripts/config_asr.py --wizard
""",
            'volcengine': """
【火山引擎 API 获取教程】
1. 访问火山引擎控制台：https://console.volcengine.com/speech
2. 开通"语音识别"服务
3. 获取 AccessKey 和 SecretKey
4. 计费方式：按需付费
5. 配置密钥：python scripts/config_asr.py --wizard
""",
            'iflytek': """
【科大讯飞 API 获取教程】
1. 访问讯飞开放平台：https://www.xfyun.cn/services/lfasr
2. 创建应用，获取 APPID 和 API Key
3. 免费额度：新用户 5 小时
4. 配置密钥：python scripts/config_asr.py --wizard
"""
        }

        if provider_key in tutorials:
            print(f"\n{tutorials[provider_key]}")

    def step_3_select_output(self) -> int:
        """步骤3：选择输出内容"""
        print("\n" + "=" * 60)
        print("步骤 3/4：选择输出内容")
        print("=" * 60)

        options = [
            "会议纪要 Word 文档（推荐）",
            "转写文本 Word 文档",
            "转写文本和会议纪要（两个 Word）",
            "仅查看转写文本（不生成文档）"
        ]

        choice = self.interactive_select("转写完成！请选择要生成的内容：", options)

        output_names = ["notes", "transcript", "both", "view_only"]
        self.selected_output = output_names[choice - 1]

        print(f"\n✅ 已选择：{options[choice - 1]}")

        return choice

    def step_4_final_action(self, output_files: List[str]) -> None:
        """步骤4：最终操作（预览/下载/分享/结束）"""
        print("\n" + "=" * 60)
        print("✅ 全部处理完成！")
        print("=" * 60)

        # 显示生成的文件信息
        print(f"\n📊 处理结果：")
        print(f"   音频时长: {get_audio_duration(self.audio_path) / 60:.1f} 分钟")
        # 从 provider_key 提取模型名称
        model_name = self.provider.replace("local-", "")
        if model_name in WHISPER_MODELS:
            print(f"   转写方案: {WHISPER_MODELS[model_name]['name']}")
        print(f"\n📁 已生成文件：")
        
        # 显示文件大小和类型
        for file in output_files:
            file_path = Path(file)
            file_size = file_path.stat().st_size / 1024  # KB
            file_type = "会议纪要" if "纪要" in file_path.name else "转写文本"
            print(f"   • {file_path.name}")
            print(f"     类型: {file_type} | 大小: {file_size:.1f} KB")

        # 引导用户下一步操作
        print(f"\n💡 接下来您可以：")
        options = [
            "预览文档内容（查看摘要/议题/待办）",
            "下载文档文件（保存到本地）",
            "分享文档（复制文件路径，发送给他人）",
            "重新处理（选择其他转写方案或输出内容）",
            "结束程序"
        ]

        choice = self.interactive_select("请选择下一步操作：", options)

        if choice == 1:
            # 预览 - 显示结构化信息
            self._preview_documents(output_files)
        elif choice == 2:
            # 下载 - 显示文件路径和说明
            self._download_documents(output_files)
        elif choice == 3:
            # 分享 - 复制文件路径
            self._share_documents(output_files)
        elif choice == 4:
            # 重新处理
            print(f"\n🔄 重新处理中...")
            self.run(audio_path=self.audio_path, provider_override=None)
        elif choice == 5:
            # 结束
            self._exit_program(with_cleanup_prompt=True)

    def _preview_documents(self, output_files: List[str]):
        """预览文档内容"""
        print("\n" + "=" * 60)
        print("📄 文档预览")
        print("=" * 60)
        
        for file in output_files:
            if file.endswith('.json'):
                # 预览 JSON 结构化数据
                self._preview_json(file)
            elif file.endswith('.txt'):
                # 预览转写文本
                self._preview_transcript(file)
            elif file.endswith('.docx'):
                # Word 文档提示
                print(f"\n【{Path(file).name}】")
                print("   Word 文档无法在终端预览，请使用下载功能查看")
        
        print("\n" + "=" * 60)
        print("💡 提示：使用下载功能获取完整文档")
        print("=" * 60)
    
    def _preview_json(self, json_file: str):
        """预览 JSON 会议纪要"""
        try:
            import json
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"\n📋 会议信息：")
            if 'meeting_info' in data:
                info = data['meeting_info']
                if 'title' in info:
                    print(f"   标题: {info['title']}")
                if 'participants' in info:
                    print(f"   参会人: {', '.join(info['participants'])}")
            
            print(f"\n🎯 议题概览：")
            if 'topics' in data and data['topics']:
                for i, topic in enumerate(data['topics'][:5], 1):
                    print(f"   {i}. {topic.get('title', '未命名')}")
                    if topic.get('summary'):
                        print(f"      {topic['summary'][:60]}...")
            if len(data['topics']) > 5:
                print(f"   ...还有 {len(data['topics']) - 5} 个议题")
            
            print(f"\n✅ 待办事项：")
            if 'todos' in data and data['todos']:
                for i, todo in enumerate(data['todos'][:5], 1):
                    print(f"   {i}. {todo.get('content', '未命名')}")
                    if todo.get('assignee'):
                        print(f"      责任人: {todo['assignee']}")
            if len(data['todos']) > 5:
                print(f"   ...还有 {len(data['todos']) - 5} 项待办")
            
            print(f"\n🔑 关键词：")
            if 'keywords' in data and data['keywords']:
                print(f"   {', '.join(data['keywords'][:10])}")
            
        except Exception as e:
            print(f"\n⚠️  预览失败：{e}")
    
    def _preview_transcript(self, txt_file: str):
        """预览转写文本"""
        content = Path(txt_file).read_text(encoding='utf-8')
        print(f"\n【{Path(txt_file).name}】")
        print(f"   总字数: {len(content)} 字符")
        print(f"\n   前 300 字符：")
        print(f"   {content[:300]}")
        if len(content) > 300:
            print(f"\n   ...（还有 {len(content)-300} 字符，使用下载功能查看完整内容）")
    
    def _download_documents(self, output_files: List[str]):
        """下载文档"""
        print("\n" + "=" * 60)
        print("💾 文档下载")
        print("=" * 60)
        
        print(f"\n📂 文档保存位置：")
        print(f"   {self.memory_dir}")
        
        print(f"\n📁 文件列表：")
        for file in output_files:
            file_path = Path(file)
            file_size = file_path.stat().st_size / 1024  # KB
            print(f"   • {file_path.name} ({file_size:.1f} KB)")
        
        print(f"\n💡 使用方法：")
        print(f"   1. 打开上述文件夹路径")
        print(f"   2. 找到对应的文档文件")
        print(f"   3. 双击打开或复制到其他位置")
        
        print(f"\n✅ 文档已保存，请从上述位置下载")
    
    def _share_documents(self, output_files: List[str]):
        """分享文档"""
        print("\n" + "=" * 60)
        print("🔗 文档分享")
        print("=" * 60)
        
        print(f"\n📂 分享路径：")
        print(f"   {self.memory_dir}")
        
        print(f"\n📁 分享文件：")
        for file in output_files:
            print(f"   • {Path(file).name}")
        
        print(f"\n💡 分享方法：")
        print(f"   1. 复制上述文件夹路径")
        print(f"   2. 通过微信、邮件等发送给他人")
        print(f"   3. 接收方打开路径即可访问文件")
        
        print(f"\n✅ 已复制文件夹路径到剪贴板")
        
        # 尝试复制到剪贴板（仅支持 Windows）
        try:
            import subprocess
            subprocess.run(['clip'], input=str(self.memory_dir), text=True, check=True)
        except:
            pass  # 跨平台兼容
    
    def _exit_program(self, with_cleanup_prompt: bool = False):
        """退出程序
        
        Args:
            with_cleanup_prompt: 是否提示用户清理数据
        """
        # 询问是否清理敏感数据
        if with_cleanup_prompt:
            print("\n" + "=" * 60)
            print("🔒 数据隐私保护")
            print("=" * 60)
            
            print(f"\n⚠️  您的转写数据保存在本地：")
            print(f"   {self.memory_dir}")
            
            print(f"\n🤔 为保护隐私，您可以选择删除这些数据：")
            print(f"   • 转写文本（音频文件已转写的内容）")
            print(f"   • 会议纪要（生成的结构化数据）")
            print(f"   • 中间文件（临时处理文件）")
            
            options = [
                "删除所有数据（保留 Word 文档）",
                "删除转写文本（保留纪要和 Word 文档）",
                "保留所有数据（不删除）"
            ]
            
            choice = self.interactive_select("请选择：", options)
            
            if choice == 1:
                self._cleanup_all_data(keep_word=True)
            elif choice == 2:
                self._cleanup_transcripts()
            else:
                print(f"\n✅ 所有数据已保留")
        
        print("\n" + "=" * 60)
        print("👋 感谢使用 Meeting Notes Assistant！")
        print("=" * 60)
        
        print(f"\n💡 下次使用提示：")
        print(f"   命令: python interactive_meeting_notes.py <音频文件>")
        print(f"   示例: python interactive_meeting_notes.py meeting.m4a")
        
        print(f"\n📚 更多帮助：")
        print(f"   • 用户手册: USER_GUIDE.md")
        print(f"   • 常见问题: SKILL.md")
        
        sys.exit(0)
    
    def _cleanup_all_data(self, keep_word: bool = False):
        """清理所有数据
        
        Args:
            keep_word: 是否保留 Word 文档
        """
        print(f"\n🗑️  正在清理数据...")
        
        deleted_files = []
        kept_files = []
        
        # 遍历 memory 目录
        if self.memory_dir.exists():
            for file in self.memory_dir.iterdir():
                if file.is_file():
                    should_delete = True
                    if keep_word and file.suffix == '.docx':
                        should_delete = False
                    
                    if should_delete:
                        try:
                            file.unlink()
                            deleted_files.append(file.name)
                        except Exception as e:
                            print(f"   ⚠️  删除失败 {file.name}: {e}")
                    else:
                        kept_files.append(file.name)
        
        # 显示结果
        if deleted_files:
            print(f"\n✅ 已删除 {len(deleted_files)} 个文件：")
            for name in deleted_files[:5]:
                print(f"   • {name}")
            if len(deleted_files) > 5:
                print(f"   ...还有 {len(deleted_files) - 5} 个文件")
        
        if kept_files:
            print(f"\n✅ 已保留 {len(kept_files)} 个文件：")
            for name in kept_files:
                print(f"   • {name}")
        
        print(f"\n🔒 数据清理完成，您的隐私已得到保护")
    
    def _cleanup_transcripts(self):
        """仅清理转写文本"""
        print(f"\n🗑️  正在清理转写文本...")
        
        deleted_files = []
        kept_files = []
        
        # 遍历 memory 目录
        if self.memory_dir.exists():
            for file in self.memory_dir.iterdir():
                if file.is_file():
                    if file.name.startswith('transcript') or file.suffix == '.txt':
                        try:
                            file.unlink()
                            deleted_files.append(file.name)
                        except Exception as e:
                            print(f"   ⚠️  删除失败 {file.name}: {e}")
                    else:
                        kept_files.append(file.name)
        
        # 显示结果
        if deleted_files:
            print(f"\n✅ 已删除 {len(deleted_files)} 个转写文件：")
            for name in deleted_files:
                print(f"   • {name}")
        
        if kept_files:
            print(f"\n✅ 已保留 {len(kept_files)} 个文件：")
            for name in kept_files:
                print(f"   • {name}")
        
        print(f"\n🔒 转写文本已清理，您的隐私已得到保护")

    def run(self, audio_path: str | None = None, provider_override: str | None = None) -> None:
        """运行完整流程"""
        try:
            # 步骤1：验证音频
            self.audio_path = self.step_1_select_audio(audio_path)

            # 步骤2：选择转写方案
            if provider_override:
                self.provider = provider_override
                model_name = self.provider.replace("local-", "")
                if model_name in WHISPER_MODELS:
                    print(f"\n✅ 使用指定方案：{WHISPER_MODELS[model_name]['name']}")
            else:
                self.provider = self.step_2_select_provider()

            # 执行转写
            print("\n" + "=" * 60)
            print("⏳ 开始转写...")
            print("=" * 60)
            print(f"   音频文件: {Path(self.audio_path).name}")
            
            # 从 provider_key 提取模型名称
            model_name = self.provider.replace("local-", "")
            if model_name in WHISPER_MODELS:
                print(f"   转写方案: {WHISPER_MODELS[model_name]['name']}")
            
            # 硬件检测和音频时长
            hardware = detect_hardware()
            audio_duration = get_audio_duration(self.audio_path)
            
            if hardware["has_gpu"]:
                print(f"   预计时间: {audio_duration / 60:.1f} 分钟 × 0.5 ≈ {audio_duration / 60 * 0.5:.1f} 分钟")
            else:
                print(f"   预计时间: {audio_duration / 60:.1f} 分钟 × 1.0 ≈ {audio_duration / 60:.1f} 分钟")
            print()
            
            # 调用转写脚本（实时捕获输出）
            import subprocess
            
            transcript_file = self.memory_dir / "transcripts"
            # 提取模型名称
            model_name = self.provider.replace("local-", "")
            cmd = [
                sys.executable,
                str(script_dir / "transcribe_audio.py"),
                self.audio_path,
                "--model", model_name,
                "--output", str(transcript_file)
            ]

            # 使用 subprocess 实时捕获输出
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                bufsize=1,  # 行缓冲
                universal_newlines=True
            )
            
            # 实时显示进度
            last_progress = 0
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    # 解析进度信息（Whisper 输出格式）
                    output = output.strip()
                    if output:
                        # Whisper 输出格式: " 10%|████ | 12.3s/it"
                        if '%' in output and '|' in output:
                            try:
                                # 提取进度百分比
                                progress_str = output.split('%')[0].strip()
                                if progress_str:
                                    progress = int(float(progress_str))
                                    # 显示简化的进度
                                    if progress - last_progress >= 10 or progress == 100:
                                        elapsed = (time.time() - start_time) / 60 if 'start_time' in locals() else 0
                                        if 'start_time' not in locals():
                                            start_time = time.time()
                                        
                                        # 计算预计剩余时间
                                        if progress > 0:
                                            rate = progress / elapsed if elapsed > 0 else 0
                                            remaining = (100 - progress) / rate if rate > 0 else 0
                                            print(f"\r   进度: {progress}% （预计剩余 {remaining:.1f} 分钟）", end='', flush=True)
                                            last_progress = progress
                            except (ValueError, IndexError):
                                pass
                        else:
                            # 显示其他信息（转写文本片段等）
                            if not any(x in output for x in ['Language mode', 'Model:', 'Device:', 'ffmpeg:', 'Task:', '开始转写']):
                                # 只显示有意义的输出
                                if output and not output.startswith(('Processing', 'Detecting', 'Loading')):
                                    print(f"\r   {output}", end='', flush=True)
            
            print()  # 换行
            
            result = process.returncode

            if result != 0:
                print(f"\n⚠️  转写过程中遇到问题")
                print(f"   请检查音频文件格式是否支持（支持 .mp3/.m4a/.wav/.ogg）")
                print(f"   退出码：{result}")
                sys.exit(1)

            print("\n✅ 转写完成！")

            # 步骤3：选择输出
            self.step_3_select_output()

            output_files = []

            # 根据选择生成输出
            if self.selected_output in ["notes", "both", "view_only"]:
                # 生成会议纪要
                notes_json = self.memory_dir / "notes-output.json"
                notes_word = self.memory_dir / f"{Path(self.audio_path).stem}-会议纪要.docx"

                cmd = [
                    sys.executable,
                    str(script_dir / "generate_notes.py"),
                    str(transcript_file),
                    "--output", str(notes_json)
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
                print(result.stdout)

                if result.returncode == 0:
                    cmd = [
                        sys.executable,
                        str(script_dir / "export_word.py"),
                        str(notes_json),
                        "--output", str(notes_word)
                    ]

                    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
                    print(result.stdout)

                    if result.returncode == 0:
                        output_files.append(str(notes_word))

            if self.selected_output in ["transcript", "both", "view_only"]:
                # 转写文本 Word
                transcript_word = self.memory_dir / f"{Path(self.audio_path).stem}-转写文本.docx"
                if transcript_word.exists():
                    output_files.append(str(transcript_word))

            if self.selected_output != "view_only":
                # 步骤4：最终操作
                self.step_4_final_action(output_files)
            else:
                # 仅查看转写文本
                content = transcript_file.read_text(encoding='utf-8')
                print("\n" + "=" * 60)
                print("📄 转写文本：")
                print("=" * 60)
                print(content)

        except KeyboardInterrupt:
            print("\n\n👋 您已中断操作，程序将退出")
            sys.exit(0)
        except Exception as e:
            print(f"\n⚠️  运行过程中遇到错误：{e}")
            print("   请截图此错误信息，联系技术支持")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="交互式会议纪要生成（飞书适配版）")
    parser.add_argument("audio_path", nargs="?", help="音频文件路径（必需）")
    parser.add_argument("--provider", choices=list(ASR_PROVIDERS.keys()),
                       help="跳过选择，直接使用指定转写方案")
    args = parser.parse_args()

    app = InteractiveMeetingNotes()
    app.run(audio_path=args.audio_path, provider_override=args.provider)


if __name__ == "__main__":
    main()

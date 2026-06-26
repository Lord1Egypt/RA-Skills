#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主脚本：表情自动发送与头像管理
- 自动触发：情绪切换时发送对应表情
- 主动索取：检测用户无头像 → 请求发送
- 等待确认：接收头像后询问是否生成
- 进度提示：生成过程中告知用户
- 发送表情：通过 OpenClaw channel 发送（使用 MEDIA 指令）
"""

import sys
import os
import json
import time
import re
from pathlib import Path
from typing import Optional, Dict, List, Tuple

# 添加项目路径
SKILL_ROOT = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from manage_emojis import EmojiManager
from generate_emojis import EmojiGenerator
from emotion_mapper import EmotionAnalyzer

class LocalAutoEmoji:
    """local-auto-emoji 主控制器"""

    def __init__(self):
        self.manager = EmojiManager()
        self.generator = EmojiGenerator()
        self.analyzer = EmotionAnalyzer()
        self.userid = None
        self.last_emotion = None
        self.emoji_send_count = 0
        self.send_timestamps = []  # 用于限流
        self.marker_map = self._build_marker_map()
        self.agentname = None  # 存储清洗后的 agent 名称

    def _extract_agentname(self, channel_info: Optional[Dict]) -> str:
        """从 channel_info 提取并清洗 agentname"""
        if not channel_info:
            return "unknown_agent"
        label = channel_info.get('label', 'unknown')
        # 清洗：只保留字母、数字、下划线，其他替换为下划线
        cleaned = re.sub(r'[^a-zA-Z0-9_]', '_', label)
        # 移除连续下划线
        cleaned = re.sub(r'_+', '_', cleaned)
        # 移除首尾下划线
        cleaned = cleaned.strip('_')
        return cleaned if cleaned else "unknown_agent"

    def _get_userid_for_agent(self, agentname: str) -> str:
        """生成 userid：优先使用已有目录，否则新建"""
        # 兼容旧数据：检测是否有 {agentname}_emoji_main（手动合并的）
        legacy_dir = SKILL_ROOT / "assets" / "public" / f"{agentname}_emoji_main"
        if legacy_dir.exists():
            # 直接复用，不重命名（保留凯哥的手工整理）
            userid = f"{agentname}_emoji_main"
            print(f"[LocalAutoEmoji] 复用手动合并目录: {userid}")
            return userid
        
        # 新生成：查找该 agent 的最大版本号
        pattern = f"{agentname}_emoji_*"
        existing = list((SKILL_ROOT / "assets" / "public").glob(pattern))
        versions = []
        for d in existing:
            try:
                ver = int(d.name.split('_')[-1])
                versions.append(ver)
            except:
                pass
        next_version = max(versions) + 1 if versions else 1
        userid = f"{agentname}_emoji_{next_version}"
        print(f"[LocalAutoEmoji] 新建目录: {userid}")
        return userid

    def ensure_user(self, userid: Optional[str] = None, agentname: Optional[str] = None) -> str:
        """确保用户存在，返回 userid"""
        # 如果未指定 userid，根据 agentname 生成
        if userid is None:
            if agentname is None:
                raise ValueError("必须指定 agentname 或 userid")
            userid = self._get_userid_for_agent(agentname)

        if userid not in self.manager.index["users"]:
            # 新用户，初始化（使用默认头像）
            default_avatar = str(SKILL_ROOT / "assets" / "local" / "default.jpg")
            self.manager.create_version(default_avatar, userid)
            print(f"[LocalAutoEmoji] 新用户: {userid}")
        else:
            print(f"[LocalAutoEmoji] 现有用户: {userid}")

        self.userid = userid
        return userid

    def has_avatar(self) -> bool:
        """检查用户是否有头像"""
        latest = self.manager.get_latest_version(self.userid)
        if not latest:
            return False
        avatar = latest / "avatar.jpg"
        return avatar.exists()

    def request_avatar(self) -> str:
        """主动索取头像消息"""
        return "阿狸想要有自己的专属表情包呢～请发送一张你的头像图片给我，我就可以生成专属表情啦！[眨眼]"

    def confirm_generate(self) -> str:
        """确认生成消息（收到头像后）"""
        return "收到头像啦！现在开始生成 8 种表情包，大约需要 2 分钟，请稍等哦～[可爱]"

    def progress_callback(self, current: int, total: int):
        """生成进度回调"""
        percent = int(current / total * 100)
        print(f"[LocalAutoEmoji] 生成进度: {current}/{total} ({percent}%)")

    def generate_user_emojis(self, avatar_path: Optional[str] = None, only_styles: Optional[List[str]] = None) -> Tuple[bool, List[str], str]:
        """
        为用户生成表情
        only_styles: 如果指定，只生成这些情感；否则生成全部
        返回：(success, emoji_paths, error_msg)
        """
        try:
            # 获取头像路径
            if avatar_path is None:
                latest = self.manager.get_latest_version(self.userid)
                if not latest:
                    return False, [], "用户无头像"
                avatar_path = str(latest / "avatar.jpg")

            # 确保用户版本目录存在（如果用户有头像但无版本目录，需创建）
            latest = self.manager.get_latest_version(self.userid)
            if not latest:
                # 创建新版本（使用现有头像）
                _, latest = self.manager.create_version(avatar_path, self.userid)

            # 如果指定了 only_styles，只生成这些情感
            if only_styles:
                success, output_paths, error = self.generator.generate_all(
                    avatar_path,
                    latest,
                    progress_callback=self.progress_callback,
                    styles=only_styles
                )
            else:
                # 生成全部表情
                success, output_paths, error = self.generator.generate_all(
                    avatar_path,
                    latest,
                    progress_callback=self.progress_callback
                )

            if not success:
                return False, [], error

            # output_paths 已经是 Path 对象列表，转换为字符串
            emoji_paths = [str(p) for p in output_paths]
            return True, emoji_paths, ""

        except Exception as e:
            import traceback
            return False, [], f"{str(e)}\n{traceback.format_exc()}"

    def _build_marker_map(self) -> Dict[str, str]:
        """构建表情标记到情感ID的映射"""
        marker_map = {}
        # 从 EMOTION_KEYWORDS 反向构建：关键词 -> emotion_id
        for emotion_id, keywords in self.analyzer.EMOTION_KEYWORDS.items():
            for kw in keywords:
                marker_map[kw] = emotion_id
        # 添加一些直接的中文标记（用户可能用情感名作为标记）
        direct_markers = {
            "开心": "happy", "高兴": "happy", "愉快": "happy", "棒": "happy", "太好了": "happy", "耶": "happy",
            "生气": "angry", "愤怒": "angry", "讨厌": "angry", "烦": "angry",
            "难过": "sad", "伤心": "sad", "哭": "sad", "泪": "sad", "委屈": "sad",
            "害羞": "shy", "脸红": "shy", "腼腆": "shy", "不好意思": "shy",
            "工作": "work", "加班": "work", "项目": "work", "deadline": "work", "会议": "work", "需求": "work", "开发": "work", "bug": "work",
            "搞笑": "meme", "笑死": "meme", "梗": "meme", "太逗了": "meme", "lol": "meme", "haha": "meme", "233": "meme", "滑稽": "meme",
            "惊讶": "surprised", "震惊": "surprised", "哇": "surprised", "卧槽": "surprised", "什么": "surprised", "竟然": "surprised",
            "酷": "cool", "帅": "cool", "厉害": "cool", "牛逼": "cool", "强": "cool", "大佬": "cool",
            "飞吻": "flying_kiss", "么么哒": "flying_kiss", "mua": "flying_kiss", "亲亲": "flying_kiss", "爱心发射": "flying_kiss", "比心": "flying_kiss",
            "抱抱": "hug", "拥抱": "hug", "要抱抱": "hug", "求抱抱": "hug", "蹭蹭": "hug",
            "可爱": "cute", "卡哇伊": "cute", "萌": "cute", "好可爱": "cute", "萌萌哒": "cute", "cute": "cute", "adorable": "cute", "卖萌": "cute",
            "眨眼": "blink", "wink": "blink", "放电": "blink", "挑逗": "blink", "你懂的": "blink"
        }
        marker_map.update(direct_markers)
        return marker_map

    def replace_emoji_markers(self, text: str) -> List[str]:
        """替换文本中的表情标记（如[可爱]），返回消息列表（文本 + 最多一个表情）"""
        import re
        pattern = r'\[([^\]]+)\]'  # 匹配 [xxx]
        
        # 查找所有标记
        markers = re.findall(pattern, text)
        if not markers:
            return [text]
        
        # 移除标记得到纯文本
        pure_text = re.sub(pattern, '', text).strip()
        
        messages = [pure_text] if pure_text else []
        
        # 只取第一个有效标记
        for marker in markers:
            emotion_id = self.marker_map.get(marker)
            if not emotion_id:
                continue  # 未知标记跳过
            
            # 获取表情路径
            emoji_path = self.get_emoji_for_emotion(emotion_id)
            if not emoji_path or not emoji_path.exists():
                emoji_path = self.fallback_to_local(emotion_id)
            
            if emoji_path:
                messages.append(f"MEDIA: {emoji_path}")
                break  # 只附加第一个表情
        
        return messages
        """
        判断是否应该发送表情（限流）
        规则：情绪切换必须发送；每5-10轮至少一次；每小时最多10次
        """
        current_emotion = self.analyzer.analyze(user_message)

        # 规则1：情绪切换必须发送
        if current_emotion != self.last_emotion:
            self.last_emotion = current_emotion
            return True

        # 规则2：每小时最多10次
        now = time.time()
        one_hour_ago = now - 3600
        self.send_timestamps = [t for t in self.send_timestamps if t > one_hour_ago]
        if len(self.send_timestamps) >= 10:
            return False

        # 规则3：每5-10轮至少一次（这里简化为每次都有一定概率）
        import random
        if random.random() < 0.5:  # 50% 概率
            return True

        return False

    def get_emoji_for_emotion(self, emotion: str) -> Optional[Path]:
        """获取指定情感的emoji路径"""
        return self.manager.get_emoji_path(self.userid, emotion)

    def fallback_to_local(self, emotion: str) -> Optional[Path]:
        """降级：使用本地静态表情"""
        local_dir = SKILL_ROOT / "assets" / "local" / emotion
        if local_dir.exists():
            files = list(local_dir.glob("*.jpg")) + list(local_dir.glob("*.png"))
            if files:
                return files[0]
        return None

    def send_emoji_via_media(self, emoji_path: Path) -> str:
        """
        通过 MEDIA 指令发送表情
        返回：OpenClaw 消息格式
        """
        # 在 OpenClaw 中，直接通过 print MEDIA 指令即可
        return f"MEDIA: {emoji_path}"

    def _is_kaige_channel(self, channel_info: Optional[Dict]) -> bool:
        """判断是否为凯哥的专属 channel"""
        if not channel_info:
            return False
        label = channel_info.get('label', '')
        # 凯哥的 channel: main 或 wecom:direct:wangdongkai
        return label in ['main', 'wecom:direct:wangdongkai']

    def _is_kaige_channel(self, channel_info: Optional[Dict]) -> bool:
        """判断是否为凯哥的专属 channel"""
        if not channel_info:
            return False
        label = channel_info.get('label', '')
        # 凯哥的 channel: main 或 wecom:direct:wangdongkai
        return label in ['main', 'wecom:direct:wangdongkai']

    def process_message(self, user_message: str, has_avatar: bool = False, avatar_file: Optional[str] = None, channel_info: Optional[Dict] = None) -> List[str]:
        """
        处理用户消息（核心流程）
        返回：需要发送的消息列表（包含可能的 MEDIA 指令）

        channel_info: OpenClaw 传递的通道信息，用于识别 agent
        """
        messages = []

        # 1. 身份检查：仅凯哥可用
        if not self._is_kaige_channel(channel_info):
            return ["阿狸目前只服务凯哥哦～[害羞]"]

        # 2. 提取 agentname（用于目录生成）
        agentname = self._extract_agentname(channel_info)
        self.agentname = agentname

        # 3. 初始化 userid（基于 agentname，兼容旧数据）
        if not self.userid:
            self.ensure_user(agentname=agentname)

        # 3. 首次使用：主动索取头像
        if not has_avatar and not self.has_avatar():
            messages.append(self.request_avatar())
            return messages

        # 4. 用户发送了头像
        if avatar_file and not self.has_avatar():
            self.manager.create_version(avatar_file, self.userid)
            messages.append(self.confirm_generate())

            # 异步生成表情（这里简化处理，直接生成并等待）
            success, emoji_paths, error = self.generate_user_emojis(avatar_file)
            if success:
                messages.append("搞定！我已经生成了 8 种专属表情，以后就可以用表情跟你对话啦～[胜利]")
                # 发送第一张示例（happy）
                happy_path = self.get_emoji_for_emotion("happy")
                if happy_path:
                    messages.append(f"MEDIA: {happy_path}")
            else:
                messages.append(f"生成过程中出错了: {error[:100]}，我会用默认表情跟你聊天～")
            return messages

        # 5. 自动触发：判断是否发送表情
        if self.should_send_emoji(user_message):
            current_emotion = self.analyzer.get_current_emotion()
            emoji_path = self.get_emoji_for_emotion(current_emotion)

            if emoji_path and emoji_path.exists():
                messages.append(self.send_emoji_via_media(emoji_path))
                self.send_timestamps.append(time.time())
                self.emoji_send_count += 1
            else:
                # 降级到本地静态表情
                fallback = self.fallback_to_local(current_emotion)
                if fallback:
                    messages.append(self.send_emoji_via_media(fallback))
                    self.send_timestamps.append(time.time())

        # 处理消息中的表情标记（如 [可爱] → 纯文本 + MEDIA 指令）
        final_messages = []
        for msg in messages:
            if msg.startswith("MEDIA:"):
                final_messages.append(msg)
            else:
                expanded = self.replace_emoji_markers(msg)
                final_messages.extend(expanded)
        return final_messages


def main():
    """命令行入口（用于测试）"""
    import argparse

    parser = argparse.ArgumentParser(description="local-auto-emoji 主脚本")
    parser.add_argument("--userid", help="用户ID（可选）")
    parser.add_argument("--avatar", help="头像路径（用于测试生成）")
    parser.add_argument("--test-emotion", help="测试情绪发送（emotion ID）")
    args = parser.parse_args()

    bot = LocalAutoEmoji()
    userid = bot.ensure_user(args.userid)

    print(f"[Main] 用户ID: {userid}")
    print(f"[Main] 是否有头像: {bot.has_avatar()}")

    if args.avatar:
        print(f"[Main] 测试生成头像: {args.avatar}")
        success, paths, error = bot.generate_user_emojis(args.avatar)
        if success:
            print(f"[Main] ✅ 生成成功: {paths}")
        else:
            print(f"[Main] ❌ 生成失败: {error}")

    if args.test_emotion:
        print(f"[Main] 测试发送表情: {args.test_emotion}")
        path = bot.get_emoji_for_emotion(args.test_emotion)
        if path:
            print(f"[Main] MEDIA: {path}")
        else:
            print(f"[Main] 未找到表情，尝试降级...")
            fallback = bot.fallback_to_local(args.test_emotion)
            if fallback:
                print(f"[Main] MEDIA: {fallback}")
            else:
                print(f"[Main] ❌ 无可用表情")


if __name__ == "__main__":
    main()

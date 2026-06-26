#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
头像和表情管理模块
- 用户版本管理（创建、查询、清理）
- 表情文件路径解析
- 用户设置读写
"""

import json
import os
import time
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple

# 技能根目录
SKILL_ROOT = Path(__file__).parent.parent.absolute()

class EmojiManager:
    """表情管理器"""

    def __init__(self, userid: Optional[str] = None):
        self.userid = userid
        self.assets_public = SKILL_ROOT / "assets" / "public"
        self.config_dir = SKILL_ROOT / "config"
        self.user_settings_file = self.config_dir / "user_settings.json"
        self.index_file = self.assets_public / "index.json"

        # 加载配置
        self._load_config()

    def _load_config(self):
        """加载用户设置和索引"""
        # 用户设置
        if self.user_settings_file.exists():
            with open(self.user_settings_file, 'r', encoding='utf-8') as f:
                self.user_settings = json.load(f)
        else:
            self.user_settings = {"users": {}, "defaults": {}}

        # 索引文件
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
        else:
            self.index = {"users": {}}

    def _save_config(self):
        """保存配置"""
        with open(self.user_settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_settings, f, indent=2, ensure_ascii=False)

        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def generate_userid(self) -> str:
        """生成用户ID：YYMMDD + 6位随机数"""
        date_part = time.strftime("%y%m%d")
        random_part = f"{int(time.time() * 1000) % 1000000:06d}"
        return f"{date_part}{random_part}"

    def create_version(self, avatar_path: str, userid: Optional[str] = None) -> Tuple[str, str]:
        """
        创建新版本（保存头像）
        返回：(userid, version_path)
        """
        if userid is None:
            userid = self.generate_userid()

        # 创建版本文件夹：<userid>_<timestamp>_<seq>
        timestamp = int(time.time())
        # 查找该 userid 的最大 seq
        existing_versions = []
        for item in self.assets_public.iterdir():
            if item.is_dir() and item.name.startswith(f"{userid}_"):
                parts = item.name.split('_')
                if len(parts) >= 3:
                    seq = int(parts[-1])
                    existing_versions.append((seq, item))

        seq = 1
        if existing_versions:
            seq = max(seq, *[v[0] for v in existing_versions]) + 1

        version_dir = self.assets_public / f"{userid}_{timestamp}_{seq}"
        version_dir.mkdir(parents=True, exist_ok=True)

        # 保存头像
        avatar_dest = version_dir / "avatar.jpg"
        shutil.copy2(avatar_path, avatar_dest)

        # 更新索引
        self.index["users"][userid] = {
            "latest_version": version_dir.name,
            "versions": [v[1].name for v in sorted(existing_versions, key=lambda x: x[0])] + [version_dir.name],
            "avatar_path": str(avatar_dest)
        }

        # 更新用户设置
        self.user_settings["users"][userid] = {
            "created_at": timestamp,
            "last_updated": timestamp,
            "total_versions": len(self.index["users"][userid]["versions"])
        }

        self._save_config()
        self.cleanup_old_versions(userid)

        return userid, str(version_dir)

    def get_latest_version(self, userid: str) -> Optional[Path]:
        """获取最新版本路径"""
        if userid not in self.index["users"]:
            return None
        version_name = self.index["users"][userid]["latest_version"]
        return self.assets_public / version_name

    def cleanup_old_versions(self, userid: str, max_versions: int = 2):
        """清理旧版本，保留最多 max_versions 个"""
        if userid not in self.index["users"]:
            return

        versions = self.index["users"][userid]["versions"]
        if len(versions) <= max_versions:
            return

        # 按版本号排序（假设格式为 userid_timestamp_seq）
        sorted_versions = sorted(
            versions,
            key=lambda v: int(v.split('_')[-1])
        )

        to_delete = sorted_versions[:-max_versions]
        for v in to_delete:
            v_path = self.assets_public / v
            if v_path.exists():
                shutil.rmtree(v_path)
                print(f"[EmojiManager] 清理旧版本: {v}")

        # 更新索引
        self.index["users"][userid]["versions"] = sorted_versions[-max_versions:]
        self._save_config()

    def get_emoji_path(self, userid: str, emotion: str, version: Optional[int] = None) -> Optional[Path]:
        """
        获取指定情感的表情文件路径
        emotion: 情感ID（happy, angry, ...）
        version: 版本号（1-based），None 表示最新版本
        """
        if userid not in self.index["users"]:
            return None

        if version is None:
            version_dir_name = self.index["users"][userid]["latest_version"]
        else:
            versions = self.index["users"][userid]["versions"]
            # 找到对应版本
            version_dir = None
            for v in versions:
                if v.endswith(f"_{version}"):
                    version_dir = v
                    break
            if not version_dir:
                return None
            version_dir_name = version_dir

        version_dir = self.assets_public / version_dir_name
        emoji_file = version_dir / f"{emotion}.jpg"

        if emoji_file.exists():
            return emoji_file

        # 尝试 png
        emoji_file = version_dir / f"{emotion}.png"
        if emoji_file.exists():
            return emoji_file

        return None

    def update_user_avatar(self, userid: str, new_avatar_path: str):
        """更新用户头像（创建新版本）"""
        return self.create_version(new_avatar_path, userid)

    def list_user_versions(self, userid: str) -> List[Dict]:
        """列出用户所有版本信息"""
        if userid not in self.index["users"]:
            return []
        return [
            {"version": v.split('_')[-1], "path": v}
            for v in self.index["users"][userid]["versions"]
        ]


if __name__ == "__main__":
    # 测试
    manager = EmojiManager()
    print(f"[Test] 生成 userid: {manager.generate_userid()}")
    print(f"[Test] assets_public: {manager.assets_public}")

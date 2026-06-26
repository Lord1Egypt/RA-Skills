#!/usr/bin/env python3
"""
密码管理器 - 核心功能模块

功能：
- 添加、编辑、删除密码
- 搜索和查找密码
- 分类管理
- 数据导入导出
- 备份管理
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class PasswordManager:
    """密码管理器主类"""

    def __init__(self, data_path: Optional[str] = None):
        """初始化密码管理器

        Args:
            data_path: 数据文件路径，默认为 ~/.workbuddy/data/passwords.json
        """
        if data_path is None:
            home = Path.home()
            data_dir = home / ".workbuddy" / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            self.data_path = data_dir / "passwords.json"
        else:
            self.data_path = Path(data_path)

        self.backup_dir = self.data_path.parent / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """加载数据文件"""
        if not self.data_path.exists():
            return self._create_empty_data()

        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载数据文件失败: {e}")
            return self._create_empty_data()

    def _create_empty_data(self) -> Dict[str, Any]:
        """创建空数据结构"""
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "categories": [
                "社交媒体",
                "邮箱",
                "电商购物",
                "金融银行",
                "工作相关",
                "娱乐",
                "其他"
            ],
            "passwords": [],
            "settings": {
                "auto_backup": True,
                "backup_interval": "daily",
                "password_length": 16,
                "password_complexity": "high"
            }
        }

    def _save_data(self) -> bool:
        """保存数据文件"""
        try:
            self.data["last_updated"] = datetime.now().isoformat()

            # 自动备份
            if self.data.get("settings", {}).get("auto_backup", True):
                self._create_backup()

            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存数据文件失败: {e}")
            return False

    def _create_backup(self) -> bool:
        """创建备份文件"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"passwords_backup_{timestamp}.json"

            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"创建备份失败: {e}")
            return False

    def add_password(
        self,
        name: str,
        username: str,
        password: str,
        category: str = "其他",
        notes: str = ""
    ) -> Optional[Dict[str, Any]]:
        """添加密码记录

        Args:
            name: 网站/应用名称
            username: 用户名/邮箱
            password: 密码
            category: 分类
            notes: 备注

        Returns:
            添加的密码记录，失败返回 None
        """
        try:
            # 评估密码强度
            strength = self._evaluate_strength(password)

            # 检查分类是否存在
            if category not in self.data["categories"]:
                self.data["categories"].append(category)

            password_entry = {
                "id": str(uuid.uuid4()),
                "name": name,
                "username": username,
                "password": password,
                "category": category,
                "notes": notes,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "strength": strength
            }

            self.data["passwords"].append(password_entry)

            if self._save_data():
                return password_entry
            return None

        except Exception as e:
            print(f"添加密码失败: {e}")
            return None

    def get_password(self, password_id: str) -> Optional[Dict[str, Any]]:
        """获取密码记录

        Args:
            password_id: 密码记录 ID

        Returns:
            密码记录，不存在返回 None
        """
        for pwd in self.data["passwords"]:
            if pwd["id"] == password_id:
                return pwd
        return None

    def update_password(
        self,
        password_id: str,
        **kwargs
    ) -> bool:
        """更新密码记录

        Args:
            password_id: 密码记录 ID
            **kwargs: 要更新的字段（name, username, password, category, notes）

        Returns:
            是否成功
        """
        try:
            password_entry = self.get_password(password_id)
            if password_entry is None:
                return False

            # 更新字段
            for key, value in kwargs.items():
                if key in password_entry and value is not None:
                    if key == "password":
                        password_entry["strength"] = self._evaluate_strength(value)
                    password_entry[key] = value

            password_entry["updated_at"] = datetime.now().isoformat()

            return self._save_data()

        except Exception as e:
            print(f"更新密码失败: {e}")
            return False

    def delete_password(self, password_id: str) -> bool:
        """删除密码记录

        Args:
            password_id: 密码记录 ID

        Returns:
            是否成功
        """
        try:
            self.data["passwords"] = [
                pwd for pwd in self.data["passwords"]
                if pwd["id"] != password_id
            ]
            return self._save_data()
        except Exception as e:
            print(f"删除密码失败: {e}")
            return False

    def search_passwords(
        self,
        keyword: str,
        search_field: str = "all"
    ) -> List[Dict[str, Any]]:
        """搜索密码记录

        Args:
            keyword: 搜索关键词
            search_field: 搜索字段（all, name, username, category, notes）

        Returns:
            匹配的密码记录列表
        """
        results = []

        for pwd in self.data["passwords"]:
            if search_field == "all":
                # 全局搜索
                search_text = f"{pwd['name']} {pwd['username']} {pwd['category']} {pwd.get('notes', '')}"
                if keyword.lower() in search_text.lower():
                    results.append(pwd)
            else:
                # 按字段搜索
                if search_field in pwd and keyword.lower() in str(pwd[search_field]).lower():
                    results.append(pwd)

        return results

    def get_passwords_by_category(self, category: str) -> List[Dict[str, Any]]:
        """按分类获取密码记录

        Args:
            category: 分类名称

        Returns:
            该分类下的密码记录列表
        """
        return [
            pwd for pwd in self.data["passwords"]
            if pwd["category"] == category
        ]

    def get_all_categories(self) -> List[str]:
        """获取所有分类"""
        return self.data["categories"]

    def add_category(self, category: str) -> bool:
        """添加分类

        Args:
            category: 分类名称

        Returns:
            是否成功
        """
        if category not in self.data["categories"]:
            self.data["categories"].append(category)
            return self._save_data()
        return True

    def delete_category(self, category: str) -> bool:
        """删除分类

        Args:
            category: 分类名称

        Returns:
            是否成功
        """
        try:
            # 将该分类下的密码移动到"其他"分类
            for pwd in self.data["passwords"]:
                if pwd["category"] == category:
                    pwd["category"] = "其他"

            # 删除分类
            self.data["categories"].remove(category)

            return self._save_data()

        except Exception as e:
            print(f"删除分类失败: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息

        Returns:
            统计信息字典
        """
        total_passwords = len(self.data["passwords"])
        category_counts = {}
        strength_counts = {"强": 0, "中": 0, "弱": 0}

        for pwd in self.data["passwords"]:
            # 分类统计
            category = pwd["category"]
            category_counts[category] = category_counts.get(category, 0) + 1

            # 强度统计
            strength = pwd.get("strength", "未知")
            if strength in strength_counts:
                strength_counts[strength] += 1

        return {
            "total_passwords": total_passwords,
            "total_categories": len(self.data["categories"]),
            "category_counts": category_counts,
            "strength_counts": strength_counts,
            "last_updated": self.data["last_updated"]
        }

    def _evaluate_strength(self, password: str) -> str:
        """评估密码强度

        Args:
            password: 密码

        Returns:
            强度（强/中/弱）
        """
        score = 0

        # 长度
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1

        # 字符类型
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        if has_lower:
            score += 1
        if has_upper:
            score += 1
        if has_digit:
            score += 1
        if has_special:
            score += 1

        # 常见弱密码
        weak_passwords = ["123456", "password", "12345678", "abc123", "111111"]
        if password.lower() in weak_passwords:
            return "弱"

        # 评估
        if score >= 5:
            return "强"
        elif score >= 3:
            return "中"
        else:
            return "弱"

    def export_to_json(self, export_path: str) -> bool:
        """导出为 JSON

        Args:
            export_path: 导出文件路径

        Returns:
            是否成功
        """
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False

    def export_to_csv(self, export_path: str) -> bool:
        """导出为 CSV

        Args:
            export_path: 导出文件路径

        Returns:
            是否成功
        """
        try:
            import csv

            with open(export_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                # 写入表头
                writer.writerow([
                    "名称",
                    "用户名",
                    "密码",
                    "分类",
                    "备注",
                    "密码强度",
                    "创建时间",
                    "更新时间"
                ])

                # 写入数据
                for pwd in self.data["passwords"]:
                    writer.writerow([
                        pwd["name"],
                        pwd["username"],
                        pwd["password"],
                        pwd["category"],
                        pwd.get("notes", ""),
                        pwd.get("strength", ""),
                        pwd["created_at"],
                        pwd["updated_at"]
                    ])

            return True

        except Exception as e:
            print(f"导出CSV失败: {e}")
            return False

    def import_from_json(self, import_path: str) -> bool:
        """从 JSON 导入

        Args:
            import_path: 导入文件路径

        Returns:
            是否成功
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)

            # 验证数据格式
            if "passwords" not in imported_data:
                print("数据格式错误：缺少 passwords 字段")
                return False

            # 合并数据
            for pwd in imported_data["passwords"]:
                if "id" not in pwd:
                    pwd["id"] = str(uuid.uuid4())

            self.data["passwords"].extend(imported_data["passwords"])

            # 合并分类
            for category in imported_data.get("categories", []):
                if category not in self.data["categories"]:
                    self.data["categories"].append(category)

            return self._save_data()

        except Exception as e:
            print(f"导入失败: {e}")
            return False

    def check_security(self) -> Dict[str, Any]:
        """检查密码安全

        Returns:
            安全检查结果
        """
        weak_passwords = []
        duplicate_passwords = {}
        old_passwords = []

        # 检查弱密码
        for pwd in self.data["passwords"]:
            if pwd.get("strength") == "弱":
                weak_passwords.append(pwd)

        # 检查重复密码
        password_map = {}
        for pwd in self.data["passwords"]:
            password = pwd["password"]
            if password not in password_map:
                password_map[password] = []
            password_map[password].append(pwd["name"])

        for password, names in password_map.items():
            if len(names) > 1:
                duplicate_passwords[password] = names

        # 检查长期未更改（超过90天）
        now = datetime.now()
        for pwd in self.data["passwords"]:
            try:
                updated_at = datetime.fromisoformat(pwd["updated_at"])
                days_old = (now - updated_at).days
                if days_old > 90:
                    old_passwords.append({
                        "name": pwd["name"],
                        "days_old": days_old
                    })
            except:
                pass

        return {
            "weak_passwords": weak_passwords,
            "duplicate_passwords": duplicate_passwords,
            "old_passwords": old_passwords,
            "score": self._calculate_security_score(
                len(weak_passwords),
                len(duplicate_passwords),
                len(old_passwords)
            )
        }

    def _calculate_security_score(
        self,
        weak_count: int,
        duplicate_count: int,
        old_count: int
    ) -> int:
        """计算安全评分（0-100）

        Args:
            weak_count: 弱密码数量
            duplicate_count: 重复密码组数
            old_count: 长期未更改密码数量

        Returns:
            安全评分
        """
        total = len(self.data["passwords"])
        if total == 0:
            return 100

        penalty = 0
        penalty += weak_count * 20  # 每个弱密码扣20分
        penalty += duplicate_count * 15  # 每组重复密码扣15分
        penalty += old_count * 10  # 每个长期未更改密码扣10分

        score = 100 - penalty
        return max(0, score)


def main():
    """主函数 - 用于测试"""
    # 创建密码管理器实例
    pm = PasswordManager()

    # 示例：添加密码
    # pm.add_password(
    #     name="Gmail",
    #     username="user@gmail.com",
    #     password="MyStrongP@ssw0rd123",
    #     category="邮箱",
    #     notes="主要工作邮箱"
    # )

    # 示例：获取统计信息
    stats = pm.get_statistics()
    print("统计信息：")
    print(f"  总密码数：{stats['total_passwords']}")
    print(f"  分类数：{stats['total_categories']}")
    print(f"  分类统计：{stats['category_counts']}")
    print(f"  强度统计：{stats['strength_counts']}")


if __name__ == "__main__":
    main()

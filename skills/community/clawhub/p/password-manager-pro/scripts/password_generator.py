#!/usr/bin/env python3
"""
密码生成器模块

功能：
- 生成随机强密码
- 自定义密码长度
- 自定义字符集
- 避免易混淆字符
"""

import random
import string
from typing import List


class PasswordGenerator:
    """密码生成器类"""

    def __init__(self):
        """初始化密码生成器"""
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"

        # 易混淆字符
        self.confusing_chars = "0O1lI"

    def generate_password(
        self,
        length: int = 16,
        use_lowercase: bool = True,
        use_uppercase: bool = True,
        use_digits: bool = True,
        use_special: bool = True,
        avoid_confusing: bool = True
    ) -> str:
        """生成随机密码

        Args:
            length: 密码长度（8-32）
            use_lowercase: 是否包含小写字母
            use_uppercase: 是否包含大写字母
            use_digits: 是否包含数字
            use_special: 是否包含特殊字符
            avoid_confusing: 是否避免易混淆字符

        Returns:
            生成的密码
        """
        # 验证长度
        if length < 8:
            length = 8
        elif length > 32:
            length = 32

        # 构建字符集
        charset = ""

        if use_lowercase:
            chars = self.lowercase
            if avoid_confusing:
                chars = chars.translate(str.maketrans('', '', 'lo'))
            charset += chars

        if use_uppercase:
            chars = self.uppercase
            if avoid_confusing:
                chars = chars.translate(str.maketrans('', '', 'IO'))
            charset += chars

        if use_digits:
            chars = self.digits
            if avoid_confusing:
                chars = chars.translate(str.maketrans('', '', '01'))
            charset += chars

        if use_special:
            charset += self.special

        # 如果字符集为空，使用默认设置
        if not charset:
            charset = self.lowercase + self.digits

        # 生成密码
        password = ''.join(random.choice(charset) for _ in range(length))

        return password

    def generate_memorable_password(
        self,
        word_count: int = 4,
        separator: str = "-"
    ) -> str:
        """生成易记密码（单词组合）

        Args:
            word_count: 单词数量（3-6）
            separator: 分隔符

        Returns:
            生成的密码
        """
        # 验证单词数量
        if word_count < 3:
            word_count = 3
        elif word_count > 6:
            word_count = 6

        # 常用单词列表
        common_words = [
            "apple", "brave", "cloud", "dream", "eagle", "flame",
            "green", "happy", "ice", "jump", "kite", "lion",
            "moon", "night", "ocean", "power", "queen", "rain",
            "star", "tiger", "unity", "victory", "wave", "xray",
            "yellow", "zebra", "bold", "calm", "dark", "fast"
        ]

        # 随机选择单词
        words = random.sample(common_words, word_count)

        # 组合密码
        password = separator.join(word.capitalize() for word in words)

        return password

    def generate_pin(self, length: int = 6) -> str:
        """生成 PIN 码

        Args:
            length: PIN 码长度（4-8）

        Returns:
            生成的 PIN 码
        """
        if length < 4:
            length = 4
        elif length > 8:
            length = 8

        return ''.join(random.choice(self.digits) for _ in range(length))

    def generate_passphrase(
        self,
        word_count: int = 5,
        use_numbers: bool = True
    ) -> str:
        """生成密码短语（更安全的单词组合）

        Args:
            word_count: 单词数量（4-8）
            use_numbers: 是否添加数字

        Returns:
            生成的密码短语
        """
        # 更长的单词列表
        words = [
            "correct", "horse", "battery", "staple", "genuine",
            "purple", "orange", "monkey", "banana", "galaxy",
            "planet", "cosmic", "energy", "future", "history",
            "moment", "nature", "ocean", "people", "quiet",
            "reason", "system", "travel", "unique", "vision",
            "weather", "yellow", "zebra", "active", "brave",
            "crystal", "diamond", "emerald", "forest", "golden"
        ]

        if word_count < 4:
            word_count = 4
        elif word_count > 8:
            word_count = 8

        selected_words = random.sample(words, word_count)

        passphrase = ' '.join(word.capitalize() for word in selected_words)

        if use_numbers:
            passphrase += str(random.randint(10, 99))

        return passphrase


def main():
    """主函数 - 用于测试"""
    generator = PasswordGenerator()

    # 测试生成密码
    print("1. 生成随机密码（16位）：")
    print(f"   {generator.generate_password(length=16)}")
    print()

    print("2. 生成易记密码（4个单词）：")
    print(f"   {generator.generate_memorable_password(word_count=4)}")
    print()

    print("3. 生成 PIN 码（6位）：")
    print(f"   {generator.generate_pin(length=6)}")
    print()

    print("4. 生成密码短语（5个单词+数字）：")
    print(f"   {generator.generate_passphrase(word_count=5, use_numbers=True)}")


if __name__ == "__main__":
    main()

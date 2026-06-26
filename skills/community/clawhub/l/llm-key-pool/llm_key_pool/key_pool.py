"""
分层API Key池管理器
实现分层轮询、跨层切换、故障转移和配额管理
"""

import threading
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


class TieredKeyPool:
    """分层API Key池管理器"""

    # 层级定义
    TIER_ORDER = ['primary', 'daily', 'fallback']  # primary -> daily -> fallback
    TIER_NAMES = {
        'primary': '主力层（高额度）',
        'daily': '每日回血层（稳定）',
        'fallback': '兜底层（开源/聚合）'
    }

    def __init__(self, provider_name: str, tier: str, api_keys: List[str], model: str, config: Dict):
        """
        初始化Key池

        Args:
            provider_name: 平台名称
            tier: 层级（primary/daily/fallback）
            api_keys: API Key列表
            model: 模型名称
            config: 全局配置
        """
        self.provider_name = provider_name
        self.tier = tier
        self.model = model
        self.api_keys = api_keys
        self.config = config

        # Key状态
        self.key_states = [
            {
                'index': i,
                'key': key,
                'error_count': 0,
                'last_error_time': None,
                'last_success_time': None,
                'quota_remaining': None,
                'is_disabled': False,
                'is_cooling': False  # 冷却状态标记
            }
            for i, key in enumerate(api_keys)
        ]

        # 轮询索引
        self.current_index = 0

        # 线程锁
        self.lock = threading.Lock()

        # 配置参数
        self.error_threshold = config.get('error_threshold', 5)
        self.cooldown_seconds = config.get('cooldown_seconds', 300)
        self.quota_check_enabled = config.get('quota_check_enabled', True)
        self.quota_min_remaining = config.get('quota_min_remaining', 1000)  # 剩余少于这个值就自动切换

    def get_next_key(self) -> Tuple[str, int]:
        """
        获取下一个可用的API Key（轮询策略）

        Returns:
            (api_key, key_index)

        Raises:
            Exception: 所有Key都不可用
        """
        with self.lock:
            # 尝试找到可用的Key
            for _ in range(len(self.api_keys)):
                index = self.current_index
                key_state = self.key_states[index]

                # 检查Key是否可用
                if self._is_key_available(key_state):
                    self.current_index = (self.current_index + 1) % len(self.api_keys)
                    return key_state['key'], index

                # 移动到下一个Key
                self.current_index = (self.current_index + 1) % len(self.api_keys)

            # 所有Key都不可用
            tier_name = self.TIER_NAMES.get(self.tier, self.tier)
            raise Exception(f"平台 {self.provider_name} ({tier_name}) 的所有API Key都不可用")

    def _is_key_available(self, key_state: Dict) -> bool:
        """
        检查Key是否可用

        Args:
            key_state: Key状态

        Returns:
            是否可用
        """
        # 如果被永久禁用，直接返回False
        if key_state['is_disabled']:
            return False

        # 检查是否在冷却中
        if key_state['is_cooling']:
            if key_state['last_error_time']:
                cooldown_end = key_state['last_error_time'] + timedelta(seconds=self.cooldown_seconds)
                if datetime.now() < cooldown_end:
                    return False
                else:
                    # 冷却结束，恢复可用
                    key_state['is_cooling'] = False
                    key_state['error_count'] = 0

        # 检查配额是否耗尽（剩余少于阈值也标记为不可用）
        if self.quota_check_enabled and key_state['quota_remaining'] is not None:
            if key_state['quota_remaining'] <= self.quota_min_remaining:
                print(f"[QUOTA] 平台 {self.provider_name} Key[{key_state['index']}] 剩余Token不足 ({key_state['quota_remaining']} < {self.quota_min_remaining})，自动跳过")
                return False

        # 检查错误次数是否超过阈值
        if key_state['error_count'] >= self.error_threshold:
            return False

        return True

    def mark_key_success(self, key_index: int, headers: Optional[Dict] = None):
        """
        标记Key使用成功

        Args:
            key_index: Key索引
            headers: HTTP响应头（用于提取配额信息）
        """
        with self.lock:
            if 0 <= key_index < len(self.key_states):
                key_state = self.key_states[key_index]
                key_state['error_count'] = max(0, key_state['error_count'] - 1)
                key_state['last_success_time'] = datetime.now()
                key_state['is_cooling'] = False

                # 更新配额信息
                if headers:
                    self._update_quota_info(key_state, headers)

    def mark_key_error(self, key_index: int, error_type: str, error_msg: str = ""):
        """
        标记Key使用失败

        Args:
            key_index: Key索引
            error_type: 错误类型（401, 429, 500等）
            error_msg: 错误消息
        """
        with self.lock:
            if 0 <= key_index < len(self.key_states):
                key_state = self.key_states[key_index]

                # 429错误：立即进入冷却状态
                if error_type == '429':
                    key_state['is_cooling'] = True
                    key_state['last_error_time'] = datetime.now()
                    tier_name = self.TIER_NAMES.get(self.tier, self.tier)
                    print(f"[COOLING] 平台 {self.provider_name} ({tier_name}) 的Key[{key_index}] 因429错误进入冷却 ({self.cooldown_seconds}秒)")
                    return

                # 401错误：永久禁用该Key
                if error_type == '401':
                    key_state['is_disabled'] = True
                    tier_name = self.TIER_NAMES.get(self.tier, self.tier)
                    print(f"[DISABLED] 平台 {self.provider_name} ({tier_name}) 的Key[{key_index}] 已被永久禁用（401 Unauthorized）")
                    return

                # 其他错误：增加错误计数
                key_state['error_count'] += 1
                key_state['last_error_time'] = datetime.now()

                # 如果错误次数超过阈值，进入冷却期
                if key_state['error_count'] >= self.error_threshold:
                    key_state['is_cooling'] = True
                    tier_name = self.TIER_NAMES.get(self.tier, self.tier)
                    print(
                        f"[COOLING] 平台 {self.provider_name} ({tier_name}) 的Key[{key_index}] 错误次数达到阈值，"
                        f"进入{self.cooldown_seconds}秒冷却期"
                    )

    def _update_quota_info(self, key_state: Dict, headers: Dict):
        """
        更新配额信息

        Args:
            key_state: Key状态
            headers: HTTP响应头
        """
        # OpenAI兼容接口的配额信息
        if 'x-ratelimit-remaining-tokens' in headers:
            key_state['quota_remaining'] = int(headers['x-ratelimit-remaining-tokens'])
            print(f"[INFO] Key[{key_state['index']}] 剩余Token: {key_state['quota_remaining']}")
            # 如果剩余不足，提示
            if key_state['quota_remaining'] <= self.quota_min_remaining:
                print(f"[WARNING] Key[{key_state['index']}] 剩余Token不足 {self.quota_min_remaining}，将自动切换")

        # 阿里云百炼可能使用的配额头
        if 'X-RateLimit-Remaining-Tokens' in headers:  # 首字母大写变体
            key_state['quota_remaining'] = int(headers['X-RateLimit-Remaining-Tokens'])
            print(f"[INFO] Key[{key_state['index']}] 剩余Token: {key_state['quota_remaining']}")
            if key_state['quota_remaining'] <= self.quota_min_remaining:
                print(f"[WARNING] Key[{key_state['index']}] 剩余Token不足 {self.quota_min_remaining}，将自动切换")

        if 'x-ratelimit-remaining' in headers:
            key_state['quota_remaining'] = int(headers['x-ratelimit-remaining'])
            print(f"[INFO] Key[{key_state['index']}] 剩余Token: {key_state['quota_remaining']}")
            if key_state['quota_remaining'] <= self.quota_min_remaining:
                print(f"[WARNING] Key[{key_state['index']}] 剩余Token不足 {self.quota_min_remaining}，将自动切换")

        # Anthropic配额信息
        if 'anthropic-ratelimit-tokens-remaining' in headers:
            key_state['quota_remaining'] = int(headers['anthropic-ratelimit-tokens-remaining'])
            print(f"[INFO] Key[{key_state['index']}] 剩余Token: {key_state['quota_remaining']}")
            if key_state['quota_remaining'] <= self.quota_min_remaining:
                print(f"[WARNING] Key[{key_state['index']}] 剩余Token不足 {self.quota_min_remaining}，将自动切换")

    def get_status(self) -> Dict:
        """
        获取Key池状态

        Returns:
            状态信息字典
        """
        with self.lock:
            tier_name = self.TIER_NAMES.get(self.tier, self.tier)
            status = {
                'provider': self.provider_name,
                'tier': self.tier,
                'tier_name': tier_name,
                'model': self.model,
                'total_keys': len(self.api_keys),
                'available_keys': sum(1 for ks in self.key_states if self._is_key_available(ks)),
                'keys': []
            }

            for ks in self.key_states:
                key_info = {
                    'index': ks['index'],
                    'key': ks['key'][:10] + '...' if len(ks['key']) > 10 else ks['key'],
                    'error_count': ks['error_count'],
                    'is_disabled': ks['is_disabled'],
                    'is_cooling': ks['is_cooling'],
                    'quota_remaining': ks['quota_remaining']
                }

                if ks['last_error_time']:
                    key_info['last_error_time'] = ks['last_error_time'].isoformat()

                if ks['last_success_time']:
                    key_info['last_success_time'] = ks['last_success_time'].isoformat()

                status['keys'].append(key_info)

            return status

    def has_available_key(self) -> bool:
        """
        检查是否有可用的Key

        Returns:
            是否有可用的Key
        """
        with self.lock:
            return any(self._is_key_available(ks) for ks in self.key_states)

    def reset_key_status(self, key_index: int):
        """
        重置指定Key的状态

        Args:
            key_index: Key索引
        """
        with self.lock:
            if 0 <= key_index < len(self.key_states):
                key_state = self.key_states[key_index]
                key_state['error_count'] = 0
                key_state['last_error_time'] = None
                key_state['is_disabled'] = False
                key_state['is_cooling'] = False
                print(f"[INFO] 已重置Key[{key_index}]的状态")

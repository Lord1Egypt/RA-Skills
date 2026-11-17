#!/usr/bin/env python3
"""
core/key_manager.py — Infoseek 归一化动态自适应 Key 管理（v1.0.1 PATCH）

把散落在 llm_router / pipeline / summarize_adapter / mcp_server 的
os.environ.get('*_API_KEY') 直接读取，归一化为统一入口 KeyManager。

设计（对齐《Key 管理机制设计评估》）：
- KeyRecord schema：provider / env_name / source / status / fail_count / circuit / quota
- 存储后端：Env（默认）→ Dotenv（.env 文件，标准库解析）→ 注册表追加（多 key 池）
- 生命周期状态机：CONFIGURED → ACTIVE → DEGRADED → CIRCUIT_OPEN → ROTATING → REVOKED
- 动态自适应：
    - 失败自适应：连续失败 N 次 → DEGRADED → CIRCUIT_OPEN（冷却后半开试探）
    - 多 key 池：同 provider 多个 key，least-used 选择（配额余量/失败次数最小）
    - 配额感知：quota.used/limit 计数，用尽自动降级
    - 用量统计：每次 get 计数，落盘 ~/.infoseek/key_usage.json
- 向后兼容：未显式 init 时，get() 直接退化为 os.environ.get()（与现状逐字节一致）

用法：
    from core.key_manager import KeyManager
    key = KeyManager.get('deepseek')           # 归一化读取（含熔断/轮换/配额）
    KeyManager.register('deepseek', 'sk-xxx')  # 会话内追加 key（多 key 池）
    KeyManager.report_failure('deepseek')      # 失败回注（触发熔断逻辑）
    KeyManager.report_success('deepseek')
    KeyManager.stats()                          # 用量/健康统计
"""

import os
import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional

try:
    from core.state_dir import state_path
except ImportError:
    def state_path(filename: str) -> Path:
        return Path(os.environ.get('INFOSEEK_DATA_DIR', Path.home() / '.infoseek')) / filename


def _dep_reg():
    """S7：外部依赖可用性统一经 dep_registry 事实层求值（懒加载，缺失回退）。"""
    try:
        import dep_registry as _dr
    except ImportError:
        from core import dep_registry as _dr  # type: ignore
    return _dr


class KeyManagementError(Exception):
    """Key 管理操作异常（加密缺失 / 密钥无效 / 解密失败等）。"""


# ═══════════════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════════════

# 内置 provider → env 变量名注册表（与 llm_router.ProviderConfig / pipeline._KEY_ENV 对齐）
BUILTIN_PROVIDERS: Dict[str, str] = {
    # LLM 路由（core/llm_router.py）
    'ollama-local': 'OLLAMA_HOST',
    'zhipu': 'ZHIPU_API_KEY',
    'openai': 'OPENAI_API_KEY',
    'anthropic': 'ANTHROPIC_API_KEY',
    'deepseek': 'DEEPSEEK_API_KEY',
    'kimi': 'KIMI_API_KEY',
    # 搜索链（scripts/infoseek_pipeline.py）
    'exa': 'EXA_API_KEY',
    'tavily': 'TAVILY_API_KEY',
    'tinyfish': 'TINYFISH_API_KEY',
    'metaso': 'METASO_API_KEY',
    # QVeris 能力路由（scripts/qveris_client.py）
    'qveris': 'QVERIS_API_KEY',
    # 摘要 / MCP 层
    'infoseek_llm': 'INFOSEEK_LLM_API_KEY',
    'auth': 'INFOSEEK_AUTH_TOKEN',
}

# 状态机
S_UNSET = 'UNSET'
S_CONFIGURED = 'CONFIGURED'
S_ACTIVE = 'ACTIVE'
S_DEGRADED = 'DEGRADED'
S_CIRCUIT_OPEN = 'CIRCUIT_OPEN'
S_ROTATING = 'ROTATING'
S_REVOKED = 'REVOKED'

# 默认阈值（可经 env 覆盖）
FAIL_THRESHOLD = int(os.environ.get('INFOSEEK_KEY_FAIL_THRESHOLD', '3'))   # 连败 N → DEGRADED
CIRCUIT_THRESHOLD = int(os.environ.get('INFOSEEK_KEY_CIRCUIT_THRESHOLD', '5'))  # 连败 M → 熔断
CIRCUIT_COOLDOWN = float(os.environ.get('INFOSEEK_KEY_CIRCUIT_COOLDOWN', '60'))  # 冷却秒数
AUTO_PERSIST_EVERY = int(os.environ.get('INFOSEEK_KEY_AUTO_PERSIST', '0'))  # 每 N 次 get 自动落盘用量（0=关闭，v1.0.1 PATCH）
DOTENV_FILE = os.environ.get('INFOSEEK_DOTENV', '.env')  # .env 路径（相对 CWD）


class KeyRecord:
    """单个 provider 的 key 状态记录"""

    __slots__ = ('provider', 'key', 'env_name', 'source', 'status',
                 'fail_count', 'circuit_open_until', 'quota_used', 'quota_limit',
                 'used_count', 'last_used', 'created_at')

    def __init__(self, provider: str, key: str, env_name: str = '',
                 source: str = 'env', quota_limit: Optional[int] = None):
        self.provider = provider
        self.key = key
        self.env_name = env_name
        self.source = source
        self.status = S_ACTIVE
        self.fail_count = 0
        self.circuit_open_until = 0.0
        self.quota_used = 0
        self.quota_limit = quota_limit
        self.used_count = 0
        self.last_used = ''
        self.created_at = time.strftime('%Y-%m-%dT%H:%M:%S')

    def to_dict(self) -> dict:
        return {
            'provider': self.provider,
            'source': self.source,
            'status': self.status,
            'fail_count': self.fail_count,
            'circuit_open_until': self.circuit_open_until,
            'quota_used': self.quota_used,
            'quota_limit': self.quota_limit,
            'used_count': self.used_count,
            'last_used': self.last_used,
            'created_at': self.created_at,
            'key_fingerprint': f'{self.key[:4]}***{self.key[-4:]}' if len(self.key) > 8 else '***',
        }


class KeyManager:
    """归一化 Key 管理单例（进程内）。"""

    _instance: Optional['KeyManager'] = None

    def __init__(self, dotenv: bool = True, dotenv_path: str = DOTENV_FILE):
        self._records: Dict[str, List[KeyRecord]] = {}
        self._lock = threading.Lock()
        self._dotenv_loaded = False
        self._dotenv_path = dotenv_path
        self._get_since_persist = 0  # v1.0.1 PATCH: 自动落盘计数
        self._token_usage: Dict[str, Dict[str, int]] = {}  # v1.0.1 B2: LLM token 用量累计
        if dotenv:
            self._load_dotenv()
        # 首次 get 前不预扫描 env —— 每次 get 兜底实时读 env（保证兼容）

    # ── 单例 ──
    @classmethod
    def instance(cls) -> 'KeyManager':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # ── .env 加载（标准库实现，无第三方依赖）──
    def _load_dotenv(self) -> bool:
        """加载 .env 文件到 os.environ（不覆盖已有 env 变量）。"""
        if self._dotenv_loaded:
            return True
        self._dotenv_loaded = True
        p = Path(self._dotenv_path)
        if not p.exists():
            return False
        try:
            for line in p.read_text(encoding='utf-8').splitlines():
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, _, v = line.partition('=')
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:  # 不覆盖已有 env
                    os.environ[k] = v
            return True
        except Exception:
            return False

    # ── 注册 / 追加 ──
    def register(self, provider: str, key: str,
                 env_name: str = '', source: str = 'session',
                 quota_limit: Optional[int] = None) -> None:
        """注册/追加一个 key 到 provider 池（多 key 池：同 provider 可多次调用）。"""
        if not key:
            return
        env_name = env_name or BUILTIN_PROVIDERS.get(provider, f'{provider.upper()}_API_KEY')
        rec = KeyRecord(provider, key, env_name=env_name, source=source,
                        quota_limit=quota_limit)
        with self._lock:
            self._records.setdefault(provider, []).append(rec)

    # ── 归一化读取 ──
    def get(self, provider: str, env_name: str = '') -> str:
        """返回 provider 的首选可用 key（str；无 key 返回 ''）。

        选择逻辑（动态自适应）：
        1. 优先进程内已注册记录（按 配额余量↑ 失败数↓ 排序）
        2. 无注册 → 实时读 env（兜底，与现状一致）
        3. 熔断中的记录跳过；全部熔断 → 回退 env
        """
        env_name = env_name or BUILTIN_PROVIDERS.get(provider, '')
        with self._lock:
            recs = self._records.get(provider, [])

        # 1) 注册池选择（least-used + 配额余量）
        if recs:
            now = time.time()
            candidates = []
            for r in recs:
                if r.status == S_REVOKED:
                    continue
                if r.status == S_CIRCUIT_OPEN and now < r.circuit_open_until:
                    continue  # 熔断冷却中
                if r.quota_limit is not None and r.quota_used >= r.quota_limit:
                    continue  # 配额用尽
                candidates.append(r)
            if candidates:
                # least-used：used_count 最小者优先；同 count 用 fail_count 最少
                best = min(candidates, key=lambda r: (r.used_count, r.fail_count))
                best.used_count += 1
                best.quota_used += 1
                best.last_used = time.strftime('%Y-%m-%dT%H:%M:%S')
                if best.status == S_CONFIGURED:
                    best.status = S_ACTIVE
                # v1.0.1 PATCH: 自动落盘（阈值批量，防频繁 IO；0=关闭）
                if AUTO_PERSIST_EVERY > 0:
                    self._get_since_persist += 1
                    if self._get_since_persist >= AUTO_PERSIST_EVERY:
                        self._get_since_persist = 0
                        try:
                            self.persist_usage()
                        except Exception:
                            pass
                return best.key

        # 2) 实时 env 兜底（无注册 / 全部熔断 / 全部配额用尽）
        env_key = os.environ.get(env_name, '') if env_name else ''
        if not env_key and provider == 'kimi':
            env_key = os.environ.get('MOONSHOT_API_KEY', '')  # kimi 别名兼容
        return env_key or ''

    # ── 健康回注（动态自适应）──
    def report_success(self, provider: str) -> None:
        """调用成功：重置失败计数，恢复 ACTIVE。"""
        with self._lock:
            for r in self._records.get(provider, []):
                r.fail_count = 0
                if r.status in (S_DEGRADED, S_CIRCUIT_OPEN):
                    r.status = S_ACTIVE
                    r.circuit_open_until = 0.0

    def report_failure(self, provider: str) -> None:
        """调用失败：累计 fail_count，触发 DEGRADED → CIRCUIT_OPEN 状态迁移。"""
        with self._lock:
            for r in self._records.get(provider, []):
                r.fail_count += 1
                if r.fail_count >= CIRCUIT_THRESHOLD:
                    r.status = S_CIRCUIT_OPEN
                    r.circuit_open_until = time.time() + CIRCUIT_COOLDOWN
                elif r.fail_count >= FAIL_THRESHOLD:
                    r.status = S_DEGRADED

    # ── 生命周期操作 ──
    def rotate(self, provider: str) -> bool:
        """轮换：将首个 ACTIVE 记录标记 ROTATING 并置后（验证新 key 后恢复）。

        实际 key 由宿主编排：本方法仅重排选择顺序（把最旧的放末尾）。
        返回是否发生轮换。
        """
        with self._lock:
            recs = self._records.get(provider, [])
            if len(recs) <= 1:
                return False
            # 取 used_count 最大的（最旧的）移到末尾
            oldest_idx = max(range(len(recs)), key=lambda i: recs[i].used_count)
            oldest = recs.pop(oldest_idx)
            oldest.status = S_ROTATING
            oldest.fail_count = 0
            recs.append(oldest)
            oldest.status = S_ACTIVE  # 完成轮换，恢复可选
            return True

    def revoke(self, provider: str, key_fingerprint: Optional[str] = None) -> int:
        """吊销：按指纹吊销指定 key（None=吊销全部）。返回吊销数。

        指纹匹配规则：key 的任意子串（兼容 list 显示的后 4 位指纹）。
        """
        revoked = 0
        with self._lock:
            recs = self._records.get(provider, [])
            targets = recs
            if key_fingerprint:
                fp = key_fingerprint.lower()
                targets = [r for r in recs
                           if fp in r.key.lower() or fp in r.key.lower()[-8:]]
            for r in targets:
                if r.status != S_REVOKED:
                    r.status = S_REVOKED
                    revoked += 1
        return revoked

    # ── 配额 ──
    def set_quota(self, provider: str, limit: int, key_index: int = -1) -> None:
        """设置配额上限（key_index=-1 表示池内全部）。"""
        with self._lock:
            recs = self._records.get(provider, [])
            if not recs:
                return
            targets = recs if key_index < 0 else [recs[key_index]]
            for r in targets:
                r.quota_limit = limit

    # ── 统计 / 可观测 ──
    def stats(self) -> dict:
        """输出全部 provider 的健康/用量统计（脱敏）。"""
        out = {}
        with self._lock:
            for provider, recs in self._records.items():
                out[provider] = [r.to_dict() for r in recs]
        # 补充 env 层（未注册但 env 有值）
        for provider, env_name in BUILTIN_PROVIDERS.items():
            if provider not in out:
                env_key = os.environ.get(env_name, '')
                if env_key:
                    out[provider] = [{
                        'source': 'env', 'status': S_ACTIVE, 'fail_count': 0,
                        'quota_used': 0, 'quota_limit': None, 'used_count': 0,
                        'last_used': '', 'created_at': '',
                        'key_fingerprint': f'{env_key[:4]}***{env_key[-4:]}' if len(env_key) > 8 else '***',
                    }]
        return out

    # ── v1.0.1 B2: LLM token 级用量统计 ──
    def record_usage(self, provider: str, input_tokens: int = 0,
                     output_tokens: int = 0) -> None:
        """累计 provider 的 LLM token 用量（llm_call 成功/失败路径调用）。"""
        if not provider:
            return
        with self._lock:
            t = self._token_usage.setdefault(provider, {'input_tokens': 0, 'output_tokens': 0})
            t['input_tokens'] += max(0, int(input_tokens or 0))
            t['output_tokens'] += max(0, int(output_tokens or 0))

    def token_usage(self) -> dict:
        """当前内存中 token 用量（provider → {input_tokens, output_tokens}）。"""
        with self._lock:
            return {p: dict(t) for p, t in self._token_usage.items()}

    def persist_usage(self, path: Optional[str] = None) -> Path:
        """用量统计落盘（默认 ~/.infoseek/key_usage.json，含 token 用量）。"""
        target = Path(path) if path else state_path('key_usage.json')
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = dict(self.stats())
        if self._token_usage:
            payload['_token_usage'] = {p: dict(t) for p, t in self._token_usage.items()}
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                          encoding='utf-8')
        return target

    # ── KeyringBackend（v1.0.1 A3/B1：系统级密钥环持久化）──
    @staticmethod
    def keyring_available() -> bool:
        """探测 keyring 库可用性（Windows Credential Locker / macOS Keychain / Linux SecretService）。

        S7：可用性经 dep_registry 事实层统一求值（返回值语义不变）。
        """
        return _dep_reg().is_available("keyring")

    def save_to_keyring(self, service: str = 'infoseek') -> int:
        """将当前注册池写入系统 keyring（service='infoseek'，username='{provider}:{idx}'）。

        仅持久化明文 key（session/env 均镜像）；keyring 不可用抛 KeyManagementError。
        返回写入数。
        """
        if not self.keyring_available():
            raise KeyManagementError("keyring 库未安装（pip install keyring），无法写入系统密钥环。")
        import keyring
        written = 0
        with self._lock:
            for provider, recs in self._records.items():
                for idx, r in enumerate(recs):
                    try:
                        keyring.set_password(service, f'{provider}:{idx}', r.key)
                        r.source = 'keyring'
                        written += 1
                    except Exception:
                        continue
        return written

    def load_from_keyring(self, service: str = 'infoseek', providers: Optional[list] = None) -> int:
        """从系统 keyring 读取并注册（username='{provider}:{idx}' pattern）。

        providers 默认取内置 provider 注册表键（不依赖已有 records，可直接恢复）。
        返回恢复数；keyring 不可用抛 KeyManagementError。
        """
        if not self.keyring_available():
            raise KeyManagementError("keyring 库未安装（pip install keyring），无法读取系统密钥环。")
        import keyring
        providers = providers or list(BUILTIN_PROVIDERS.keys())
        restored = 0
        for provider in providers:
            idx = 0
            while True:
                try:
                    val = keyring.get_password(service, f'{provider}:{idx}')
                except Exception:
                    val = None
                if not val:
                    break
                self.register(provider, val, source='keyring')
                restored += 1
                idx += 1
        return restored

    # ── FileBackend 加密持久化（v1.0.1 PATCH / P3）──
    def save_keys(self, path: Optional[str] = None, key_path: Optional[str] = None) -> Path:
        """加密持久化全部注册 key（Fernet AES-128-CBC）。

        - cryptography 可用 → 加密落盘，key 文件默认 <path>.key（权限 600）
        - cryptography 缺失 → 抛 KeyManagementError（**拒绝明文落盘**）

        返回: 数据文件路径
        """
        target = Path(path) if path else state_path('keys.enc.json')
        key_file = Path(key_path) if key_path else target.with_suffix('.key')

        try:
            if not _dep_reg().is_available("cryptography"):
                raise ImportError
            from cryptography.fernet import Fernet
        except ImportError:
            raise KeyManagementError(
                "cryptography 未安装，拒绝明文落盘。请 pip install cryptography "
                "或使用会话内注册（KeyManager.register）。")

        # 密钥：已存在则读取，否则生成（Fernet key 为 44 字符 base64）
        if key_file.exists():
            raw_key = key_file.read_bytes()
            try:
                fernet = Fernet(raw_key)
            except Exception:
                raise KeyManagementError(f"密钥文件无效: {key_file}")
        else:
            raw_key = Fernet.generate_key()
            fernet = Fernet(raw_key)
            key_file.parent.mkdir(parents=True, exist_ok=True)
            key_file.write_bytes(raw_key)

        payload = {}
        with self._lock:
            for provider, recs in self._records.items():
                payload[provider] = [
                    {'key': r.key, 'env_name': r.env_name, 'source': r.source,
                     'quota_limit': r.quota_limit} for r in recs if r.status != S_REVOKED
                ]

        target.parent.mkdir(parents=True, exist_ok=True)
        enc = fernet.encrypt(json.dumps(payload, ensure_ascii=False).encode('utf-8'))
        target.write_bytes(enc)
        try:
            os.chmod(key_file, 0o600)  # POSIX-only：限制密钥文件仅属主可读写
        except (NotImplementedError, OSError):
            # Windows 无 POSIX 权限位：密钥文件权限依赖 NTFS ACL，此处仅提示
            import warnings
            warnings.warn(
                "chmod 0o600 不可用（当前平台无 POSIX 权限位）；"
                "密钥文件权限请通过系统 ACL 保障。",
                RuntimeWarning, stacklevel=2)
        return target

    def load_keys(self, path: Optional[str] = None, key_path: Optional[str] = None) -> int:
        """从加密文件加载并注册 key。返回注册数。"""
        target = Path(path) if path else state_path('keys.enc.json')
        key_file = Path(key_path) if key_path else target.with_suffix('.key')
        if not target.exists() or not key_file.exists():
            return 0
        try:
            if not _dep_reg().is_available("cryptography"):
                raise ImportError
            from cryptography.fernet import Fernet, InvalidToken
        except ImportError:
            return 0
        try:
            fernet = Fernet(key_file.read_bytes())
            raw = fernet.decrypt(target.read_bytes()).decode('utf-8')
        except InvalidToken:
            raise KeyManagementError("密钥不匹配或文件损坏，无法解密 keys 文件。")
        except (ValueError, TypeError) as e:
            raise KeyManagementError(f"密钥文件无效（非 Fernet key）: {str(e)[:60]}")
        except Exception as e:
            raise KeyManagementError(f"解密失败: {str(e)[:80]}")
        payload = json.loads(raw)
        count = 0
        for provider, recs in payload.items():
            for r in recs:
                self.register(provider, r.get('key', ''), env_name=r.get('env_name', ''),
                              source='file', quota_limit=r.get('quota_limit'))
                count += 1
        return count

    def usage_report(self, path: Optional[str] = None) -> dict:
        """基于 key_usage.json 的用量/成本报表（含估算成本）。

        成本估算：provider 命中 llm_router 成本表时按 cost_per_1k × 用量近似；
        未命中（搜索引擎）仅输出调用次数。
        """
        usage_path = Path(path) if path else state_path('key_usage.json')
        if not usage_path.exists():
            return {'error': f'用量文件不存在: {usage_path}', 'path': str(usage_path)}
        try:
            data = json.loads(usage_path.read_text(encoding='utf-8'))
        except Exception as e:
            return {'error': f'解析失败: {e}', 'path': str(usage_path)}

        # 成本表（复用 llm_router 定义，避免循环 import）
        cost_table = {}
        try:
            from core.llm_router import PROVIDERS
            cost_table = {p.name: p.cost_per_1k for p in PROVIDERS}
        except Exception:
            pass

        rows = []
        total_cost = 0.0
        token_data = data.get('_token_usage', {}) if isinstance(data, dict) else {}
        # provider 集合 = records ∪ token_usage（token-only provider 也纳入报表）
        record_providers = {k for k, v in (data.items() if isinstance(data, dict) else [])
                            if k != '_token_usage' and isinstance(v, list)}
        all_providers = record_providers | set(token_data.keys())
        for provider in sorted(all_providers):
            recs = data.get(provider, []) if isinstance(data, dict) else []
            used = sum(r.get('used_count', 0) for r in recs if isinstance(r, dict))
            fail = max((r.get('fail_count', 0) for r in recs if isinstance(r, dict)), default=0)
            statuses = sorted({r.get('status', '?') for r in recs if isinstance(r, dict)})
            # 成本：优先 token 用量折算（B2），无 token 数据 fallback calls 口径
            tok = token_data.get(provider, {})
            in_tok = tok.get('input_tokens', 0)
            out_tok = tok.get('output_tokens', 0)
            est_cost = 0.0
            if provider in cost_table:
                if in_tok or out_tok:
                    est_cost = round((in_tok + out_tok) / 1000.0 * cost_table[provider], 6)
                else:
                    est_cost = round(used / 1000.0 * cost_table[provider], 6)
                total_cost += est_cost
            rows.append({
                'provider': provider,
                'calls': used,
                'fail_count': fail,
                'statuses': statuses,
                'input_tokens': in_tok,
                'output_tokens': out_tok,
                'est_cost_usd': est_cost,
            })
        return {'rows': rows, 'total_est_cost_usd': round(total_cost, 6)}

    # ── 测试辅助 ──
    def reset(self) -> None:
        """清空进程内注册（仅测试用）。"""
        with self._lock:
            self._records.clear()


# ═══════════════════════════════════════════════════════════════
# 便捷函数（与 KeyManager.get 等价，供模块直接 import）
# ═══════════════════════════════════════════════════════════════

def get_key(provider: str, env_name: str = '') -> str:
    """便捷入口：KeyManager.instance().get()"""
    return KeyManager.instance().get(provider, env_name)


if __name__ == '__main__':
    km = KeyManager.instance()
    print('=== KeyManager 自检 ===')
    print('deepseek env key:', repr(km.get('deepseek')))
    print('exa env key:', repr(km.get('exa')))
    km.register('deepseek', 'sk-test-1234567890')
    print('注册后 deepseek:', km.get('deepseek'))
    km.report_failure('deepseek')
    km.report_failure('deepseek')
    print('连败2次后状态:', km.stats()['deepseek'][0]['status'], 'fail_count=',
          km.stats()['deepseek'][0]['fail_count'])
    km.report_success('deepseek')
    print('成功后状态:', km.stats()['deepseek'][0]['status'])
    print(json.dumps(km.stats(), ensure_ascii=False, indent=2)[:400])

"""
配置加载模块。

命名规范：FETCHER_{SOURCE}_{PARAM}
  - 通用参数：FETCHER_KEYWORDS / FETCHER_EXCLUDE_KEYWORDS / ...
  - 北京中建云智：FETCHER_BJZC_BEARER_TOKEN / FETCHER_BJZC_TBSESSION / ...
  - 后续新增数据源：FETCHER_CCGP_xxx / FETCHER_BJGP_xxx / ...

优先级（高→低）：
  1. 当前运行目录的 .env
  2. ~/.config/govb-fetcher/.env
  3. 硬编码默认值（仅关键词等非敏感配置）
"""

import os
import re
import threading
from pathlib import Path
from typing import Optional

DEFAULTS = {
    'FETCHER_KEYWORDS': '体系,模型,仿真,数据,决策,规划,分析,智能,AI,软件,系统,信息,算法,效能',
    'FETCHER_EXCLUDE_KEYWORDS': '体能,训练鞋,鞋类,服装,被装,医疗,药品,器械,膝关节,光纤,电梯,物业,绿化,装修,工程,建材,食材,食品,副食',
    'FETCHER_HIGH_VALUE_KEYWORDS': '模型,仿真,数据,决策,分析,智能,AI,软件,意向',
    'FETCHER_OUTPUT_DIR': '~/.openclaw/workspace/govb-bidding',
    'FETCHER_USE_PROXY': 'false',
    'FETCHER_PROXY': '',
    # 凭证类不设默认值，必须由用户通过 --set-cookie 或 .env 提供
}

_config_cache: dict = {}
_env_lock = threading.Lock()


def _load_env_file(path: Path) -> dict:
    result = {}
    if not path.exists():
        return result
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k, _, v = line.partition('=')
            result[k.strip()] = v.strip()
    return result


def load_config() -> dict:
    global _config_cache
    if _config_cache:
        return _config_cache

    cfg = dict(DEFAULTS)

    # 全局配置（低优先级）
    global_env = Path.home() / '.config' / 'govb-fetcher' / '.env'
    cfg.update(_load_env_file(global_env))

    # 局部配置（高优先级）
    local_env = Path.cwd() / '.env'
    cfg.update(_load_env_file(local_env))

    # 环境变量最高优先级
    for k in list(cfg.keys()) + list(os.environ.keys()):
        if k.startswith('FETCHER_') and k in os.environ:
            cfg[k] = os.environ[k]

    _config_cache = cfg
    return cfg


def get_config(key: str, default: str = '') -> str:
    return load_config().get(key, default)


# ── 通用关键词配置 ──────────────────────────────

def get_keywords() -> list:
    return [k.strip() for k in get_config('FETCHER_KEYWORDS').split(',') if k.strip()]


def get_exclude_keywords() -> list:
    return [k.strip() for k in get_config('FETCHER_EXCLUDE_KEYWORDS').split(',') if k.strip()]


def get_high_value_keywords() -> list:
    return [k.strip() for k in get_config('FETCHER_HIGH_VALUE_KEYWORDS').split(',') if k.strip()]


def get_output_dir() -> Path:
    return Path(get_config('FETCHER_OUTPUT_DIR')).expanduser()


def get_proxies() -> Optional[dict]:
    """返回 requests 用的 proxies 字典，FETCHER_USE_PROXY=true 时生效，否则返回 None。"""
    use_proxy = get_config('FETCHER_USE_PROXY', 'false').lower() == 'true'
    if not use_proxy:
        return None
    proxy_url = get_config('FETCHER_PROXY')
    if not proxy_url:
        return None
    return {'http': proxy_url, 'https': proxy_url}


# ── 北京中建云智（BJZC）凭证 ───────────────────

def get_bjzc_bearer_token() -> str:
    return get_config('FETCHER_BJZC_BEARER_TOKEN')


def get_bjzc_tbsession() -> str:
    return get_config('FETCHER_BJZC_TBSESSION')


def get_bjzc_jsessionid() -> str:
    return get_config('FETCHER_BJZC_JSESSIONID')


def get_bjzc_alb_route() -> str:
    return get_config('FETCHER_BJZC_ALB_ROUTE')


# ── .env 文件操作 ───────────────────────────────

def get_env_path() -> Path:
    """返回当前生效的 .env 文件路径（优先局部，其次全局）。"""
    local = Path.cwd() / '.env'
    if local.exists():
        return local
    return Path.home() / '.config' / 'govb-fetcher' / '.env'


def save_to_env(updates: dict) -> Path:
    """
    将 updates 中的 key=value 写入 .env（存在则替换，不存在则追加）。
    不影响其他已有配置项。返回写入的文件路径。线程安全。
    """
    with _env_lock:
        return _save_to_env_unsafe(updates)


def _save_to_env_unsafe(updates: dict) -> Path:
    env_path = get_env_path()

    if not env_path.exists():
        example = Path(__file__).parent.parent / '.env.example'
        env_path.parent.mkdir(parents=True, exist_ok=True)
        if example.exists():
            env_path.write_text(example.read_text(encoding='utf-8'), encoding='utf-8')
        else:
            env_path.write_text('', encoding='utf-8')

    lines = env_path.read_text(encoding='utf-8').splitlines(keepends=True)
    updated_keys = set()

    for i, line in enumerate(lines):
        for k, v in updates.items():
            if re.match(rf'^\s*{re.escape(k)}\s*=', line):
                lines[i] = f'{k}={v}\n'
                updated_keys.add(k)

    for k, v in updates.items():
        if k not in updated_keys:
            lines.append(f'{k}={v}\n')

    env_path.write_text(''.join(lines), encoding='utf-8')

    # 清缓存，下次 get_config 重新读取
    global _config_cache
    _config_cache = {}

    return env_path

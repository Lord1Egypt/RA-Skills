"""
Step 3：安全认证层（企业安全标准）

携带账号密码向服务端登录接口发起 POST 请求，
服务端返回 JWT Token 字符串后写入 ./output/jwt_token.txt 供 Step 4 读取。
退出码 0 成功，1 失败（供工作流 retry 机制使用）。

依赖:
    pip install requests
"""

import argparse
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

try:
    import requests
except ModuleNotFoundError as _exc:
    raise SystemExit("缺少依赖 requests，请先执行: pip install requests") from _exc

ROOT_DIR = Path(__file__).resolve().parent.parent
RUN_ID_FILE = ROOT_DIR / "current_run_id.txt"
TOKEN_CACHE_DIR = ROOT_DIR / "token_cache"

# ===============================================================
# 用户配置区（修改这里即可）
# ===============================================================

API_BASE_URL   = "http://192.168.60.241:1120"   # 服务端基础地址
LOGIN_PATH     = "/api/GenUser/TokenLogin"         # 登录接口路径
USERNAME       = "kang"                        # 登录账号（user_account）
PASSWORD       = "kang123456"                  # 登录密码（user_password）
LOGIN_MESSAGE  = "测试,手机端e12a5481c32d23b024226d5e2d7a47aac0870cfc5252b055282b668004a0ebbd,Rule"                           # message 字段（标识来源/客户端类型）

# ===============================================================
# 运行时路径（由 ensure_runtime_dirs 初始化）
# ===============================================================
OUTPUT_DIR: Path = ROOT_DIR / "output"
TOKEN_FILE: Path = OUTPUT_DIR / "jwt_token.txt"
LOG_DIR: Path    = ROOT_DIR / "logs"


# ═══════════════════════════════════════════════════════
# 参数 / 目录 / 日志
# ═══════════════════════════════════════════════════════

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Step 3 - 安全认证层：向服务端请求 JWT Token 并写入 output/jwt_token.txt"
        )
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP 请求超时秒数（默认: 30）",
    )
    # 保留兼容参数（root.yaml 中已定义，忽略其值）
    parser.add_argument("--secret-key",      default=None, help=argparse.SUPPRESS)
    parser.add_argument("--expire-minutes",  default=None, help=argparse.SUPPRESS)
    parser.add_argument("--api-endpoint",    default=None, help=argparse.SUPPRESS)
    return parser.parse_args()


def ensure_runtime_dirs(output_dir: Path) -> None:
    global OUTPUT_DIR, TOKEN_FILE, LOG_DIR
    OUTPUT_DIR = output_dir
    TOKEN_FILE = OUTPUT_DIR / "jwt_token.txt"
    LOG_DIR    = output_dir.parent / "logs"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def load_run_id() -> str:
    if not RUN_ID_FILE.exists():
        raise SystemExit("未找到 current_run_id.txt，请先执行 Step 1")
    run_id = RUN_ID_FILE.read_text(encoding="utf-8").strip()
    if not run_id:
        raise SystemExit("current_run_id.txt 为空，请先执行 Step 1")
    return run_id


def setup_logging(log_dir: Path) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    fh = RotatingFileHandler(
        log_dir / "jwt_token.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    fh.setFormatter(fmt)
    logger.addHandler(sh)
    logger.addHandler(fh)


# ═══════════════════════════════════════════════════════
# 向服务端请求 JWT Token
# ═══════════════════════════════════════════════════════

def fetch_token(timeout: float) -> str:
    """
    POST user_account/user_password/message 到登录接口，
    从响应的 data.jwttoken 中提取 JWT Token 字符串。
    """
    url = f"{API_BASE_URL.rstrip('/')}{LOGIN_PATH}"
    payload = {
        "user_account":  USERNAME,
        "user_password": PASSWORD,
        "message":       LOGIN_MESSAGE,
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}

    logging.info(f"请求登录接口: {url}")
    resp = requests.post(url, json=payload, headers=headers, timeout=timeout)

    # 先尝试解析响应体，以便在 raise_for_status 前记录服务端错误信息
    try:
        body = resp.json()
    except Exception as e:
        resp.raise_for_status()
        raise ValueError(f"响应体不是合法 JSON: {e} | 原始内容: {resp.text[:200]}")

    if not resp.ok:
        replymsg = body.get("replymsg", "") if isinstance(body, dict) else ""
        raise requests.exceptions.HTTPError(
            f"HTTP {resp.status_code} | replymsg={replymsg}",
            response=resp,
        )

    # 服务端响应结构：{httpstate, replymsg, data: {jwttoken, ...}}
    if not isinstance(body, dict):
        raise ValueError(f"无法解析登录响应格式: {type(body)}")

    httpstate = body.get("httpstate")
    replymsg  = body.get("replymsg", "")

    # httpstate == 1 表示成功（GRMState.成功）
    if httpstate != 1:
        raise ValueError(f"登录失败 | httpstate={httpstate} | replymsg={replymsg}")

    data = body.get("data")
    if not isinstance(data, dict) or not data.get("jwttoken"):
        raise ValueError(
            f"登录响应中未找到 data.jwttoken 字段，响应内容: {str(body)[:200]}"
        )

    token = str(data["jwttoken"]).strip()

    if not token:
        raise ValueError("服务端返回的 token 为空")
    return token


def save_token(token: str, token_file: Path) -> None:
    token_file.write_text(token, encoding="utf-8")
    logging.info(f"Token 已写入: {token_file}")


def get_daily_cache_file() -> Path:
    date_str = datetime.now().strftime("%Y%m%d")
    return TOKEN_CACHE_DIR / f"jwt_token_{date_str}.txt"


def load_daily_cached_token() -> str | None:
    cache_file = get_daily_cache_file()
    if not cache_file.exists():
        return None
    token = cache_file.read_text(encoding="utf-8").strip()
    if not token:
        return None
    logging.info(f"复用当天缓存 Token: {cache_file}")
    return token


def save_daily_cache_token(token: str) -> None:
    cache_file = get_daily_cache_file()
    cache_file.write_text(token, encoding="utf-8")
    logging.info(f"当天缓存 Token 已更新: {cache_file}")


# ═══════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════

def main(timeout: float) -> int:
    run_id = load_run_id()
    run_dir = ROOT_DIR / f"run_{run_id}"
    output_dir = run_dir / "output"
    ensure_runtime_dirs(output_dir)
    setup_logging(LOG_DIR)

    logging.info("=== Step 3: 安全认证层 启动 ===")
    logging.info(f"运行目录: {run_dir}")
    logging.info(f"Token 输出路径: {TOKEN_FILE}")
    logging.info(f"登录接口: {API_BASE_URL}{LOGIN_PATH}")
    logging.info(f"账号: {USERNAME}")

    try:
        token = load_daily_cached_token()
        if token is None:
            logging.info("当天无缓存 Token，执行登录请求")
            token = fetch_token(timeout)
            save_daily_cache_token(token)
        else:
            logging.info("当天已登录，跳过登录请求")
        save_token(token, TOKEN_FILE)
    except requests.exceptions.ConnectionError as e:
        logging.error(f"连接失败: {e}")
        return 1
    except requests.exceptions.Timeout:
        logging.error(f"登录请求超时（{timeout}s）")
        return 1
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP 错误: {e.response.status_code} | {e.response.text[:300]}")
        return 1
    except Exception as e:
        logging.exception(f"获取 JWT Token 失败: {e}")
        return 1

    logging.info("=== Step 3 完成 ===")
    return 0


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(timeout=args.timeout))

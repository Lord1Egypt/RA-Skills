"""
Step 4：工业数据提交层（最终出口）

读取 input_dir 中的 .json 文件（由 Step 2 产出），携带 Step 3 签发的 JWT Token，
POST 至 api_endpoint（/api/GenProduct/ModifyParts）。
路径与 API 地址均只使用脚本内配置，不读取环境变量。
已提交 JSON 移入 input_dir/processed_json，失败文件隔离到 input_dir/failed_json。
退出码 0 全部成功，1 存在失败（供工作流 retry 机制使用）。

依赖:
    pip install requests
"""

import argparse
import json
import logging
import shutil
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

try:
    import requests
except ModuleNotFoundError as _exc:
    raise SystemExit("缺少依赖 requests，请先执行: pip install requests") from _exc

# -------------------------------------------------------
# 用户配置区（仅修改这里）
# -------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RUN_ID_FILE = PROJECT_ROOT / "current_run_id.txt"
API_BASE_URL = "http://192.168.60.241:1120"
API_SUBMIT_PATH = "/api/GenProduct/ModifyParts"
INPUT_JSON_DIR_CONFIG = PROJECT_ROOT / "output" / "json"
TOKEN_FILE_CONFIG = PROJECT_ROOT / "output" / "jwt_token.txt"

# -------------------------------------------------------
# 运行时全局路径（由 ensure_runtime_dirs 初始化）
# -------------------------------------------------------
INPUT_JSON_DIR: Path   = INPUT_JSON_DIR_CONFIG
TOKEN_FILE: Path       = TOKEN_FILE_CONFIG
PROCESSED_JSON_DIR: Path = INPUT_JSON_DIR / "processed_json"
FAILED_JSON_DIR: Path    = INPUT_JSON_DIR / "failed_json"
LOG_DIR: Path            = PROJECT_ROOT / "logs"

AUTH_MODE_BEARER = "BearerToken"


# ═══════════════════════════════════════════════════════
# 参数 / 目录 / 日志
# ═══════════════════════════════════════════════════════

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Step 4 - 工业数据提交层：读取 JSON AST 并 POST 至 API"
        )
    )
    # root.yaml 兼容参数：接收但忽略，实际只使用脚本内配置
    parser.add_argument("--input-dir", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--api-endpoint", default=None, help=argparse.SUPPRESS)
    parser.add_argument(
        "--auth-mode",
        default=AUTH_MODE_BEARER,
        choices=[AUTH_MODE_BEARER],
        help=f"认证模式，目前仅支持 {AUTH_MODE_BEARER}（默认）",
    )
    parser.add_argument("--token-file", default=None, help=argparse.SUPPRESS)
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP 请求超时秒数（默认: 30）",
    )
    return parser.parse_args()


def ensure_runtime_dirs() -> None:
    global INPUT_JSON_DIR, TOKEN_FILE, PROCESSED_JSON_DIR, FAILED_JSON_DIR, LOG_DIR
    INPUT_JSON_DIR    = INPUT_JSON_DIR_CONFIG
    TOKEN_FILE        = TOKEN_FILE_CONFIG
    PROCESSED_JSON_DIR = INPUT_JSON_DIR / "processed_json"
    FAILED_JSON_DIR   = INPUT_JSON_DIR / "failed_json"
    LOG_DIR           = PROJECT_ROOT / "logs"

    INPUT_JSON_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_JSON_DIR.mkdir(parents=True, exist_ok=True)
    FAILED_JSON_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


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
        log_dir / "data_submit.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    fh.setFormatter(fmt)
    logger.addHandler(sh)
    logger.addHandler(fh)


# ═══════════════════════════════════════════════════════
# Token 读取
# ═══════════════════════════════════════════════════════

def load_token(token_file: Path) -> str:
    if not token_file.exists():
        raise FileNotFoundError(
            f"JWT Token 文件不存在: {token_file}（请确认 Step 3 已成功执行）"
        )
    token = token_file.read_text(encoding="utf-8").strip()
    if not token:
        raise ValueError("JWT Token 文件为空，请重新运行 Step 3")
    return token


# ═══════════════════════════════════════════════════════
# API 提交
# ═══════════════════════════════════════════════════════

def post_to_api(
    parts: list,
    api_base_url: str,
    token: str,
    timeout: float,
) -> dict | None:
    url = f"{api_base_url.rstrip('/')}{API_SUBMIT_PATH}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json; charset=utf-8",
    }
    logging.info(f"发送 {len(parts)} 条记录 → {url}")
    try:
        resp = requests.post(url, json=parts, headers=headers, timeout=timeout)
        resp.raise_for_status()
        result = resp.json()
        state  = result.get("httpstate")
        msg    = result.get("replymsg", "")
        if state == 1:
            logging.info(f"提交成功 | httpstate={state} | replymsg={msg}")
        else:
            logging.warning(f"服务端返回非成功状态 | httpstate={state} | replymsg={msg}")
        return result
    except requests.exceptions.ConnectionError as e:
        logging.error(f"连接失败: {e}")
    except requests.exceptions.Timeout:
        logging.error(f"请求超时（{timeout}s）")
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP 错误: {e.response.status_code} | {e.response.text[:300]}")
    except Exception as e:
        logging.error(f"未知异常: {e}")
    return None


# ═══════════════════════════════════════════════════════
# 文件管理
# ═══════════════════════════════════════════════════════

def safe_move(src: Path, dest_dir: Path) -> Path:
    dest = dest_dir / src.name
    if dest.exists():
        dest = dest_dir / f"{src.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{src.suffix}"
    shutil.move(str(src), dest)
    return dest


def quarantine_file(src: Path, reason: str) -> None:
    try:
        moved = safe_move(src, FAILED_JSON_DIR)
        report = FAILED_JSON_DIR / f"{src.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.error.txt"
        report.write_text(
            f"time: {datetime.now().isoformat()}\nfile: {src.name}\nreason: {reason}\n",
            encoding="utf-8",
        )
        logging.error(f"JSON 已隔离: {moved.name} | 原因: {reason}")
    except Exception as e:
        logging.exception(f"隔离失败: {src.name} | {e}")


# ═══════════════════════════════════════════════════════
# 单文件提交
# ═══════════════════════════════════════════════════════

def submit_json_file(
    p: Path,
    api_base_url: str,
    token: str,
    timeout: float,
) -> bool:
    logging.info(f"提交文件: {p.name}")

    try:
        parts = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        quarantine_file(p, f"读取JSON失败: {e}")
        return False

    if not isinstance(parts, list) or len(parts) == 0:
        quarantine_file(p, "JSON 内容为空或格式非法（期望非空列表）")
        return False

    result = post_to_api(parts, api_base_url, token, timeout)
    if result is None:
        quarantine_file(p, "API 提交失败（见上方日志）")
        return False

    try:
        safe_move(p, PROCESSED_JSON_DIR)
        logging.info(f"已归档: {p.name} → {PROCESSED_JSON_DIR.name}/")
    except Exception as e:
        logging.exception(f"归档失败: {p.name} | {e}")
        return False

    return True


# ═══════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════

def main(
    timeout: float,
) -> int:
    global INPUT_JSON_DIR_CONFIG, TOKEN_FILE_CONFIG
    run_id = load_run_id()
    run_dir = PROJECT_ROOT / f"run_{run_id}"
    INPUT_JSON_DIR_CONFIG = run_dir / "output" / "json"
    TOKEN_FILE_CONFIG = run_dir / "output" / "jwt_token.txt"

    ensure_runtime_dirs()
    setup_logging(LOG_DIR)

    logging.info("=== Step 4: 工业数据提交层 启动 ===")
    logging.info(f"运行目录: {run_dir}")
    logging.info(f"JSON 输入目录: {INPUT_JSON_DIR}")

    # 读取 JWT Token
    try:
        token = load_token(TOKEN_FILE)
    except Exception as e:
        logging.error(f"读取 JWT Token 失败: {e}")
        return 1

    logging.info(f"API 地址: {API_BASE_URL}{API_SUBMIT_PATH}")
    logging.info(f"认证模式: {AUTH_MODE_BEARER}")

    json_files = [
        p for p in INPUT_JSON_DIR.iterdir()
        if p.is_file() and p.suffix.lower() == ".json"
    ]

    if not json_files:
        logging.info("未发现待提交的 JSON 文件，Step 4 正常结束")
        return 0

    logging.info(f"共发现 {len(json_files)} 个 JSON 文件，开始批量提交")

    success_count = fail_count = 0
    for p in json_files:
        if submit_json_file(p, API_BASE_URL, token, timeout):
            success_count += 1
        else:
            fail_count += 1

    logging.info(f"=== Step 4 完成 | 成功: {success_count}，失败: {fail_count} ===")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(timeout=args.timeout))

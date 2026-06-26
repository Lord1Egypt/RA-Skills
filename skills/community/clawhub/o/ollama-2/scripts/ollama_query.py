import os
import sys
import json
import logging
from typing import Generator, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 尝试加载 .env 文件 (符合项目已有的 python-dotenv 依赖)
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# 配置项，支持从环境变量或 .env 读取
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://100.66.1.2:11434").rstrip("/")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3.5:9b")

# 日志配置
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def create_session(retries: int = 3, backoff_factor: float = 0.3) -> requests.Session:
    """创建带有重试策略的请求 Session"""
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def query_ollama(
    prompt: str, model: str = OLLAMA_MODEL, stream: bool = False, timeout: int = 120
) -> Union[str, Generator[str, None, None]]:
    """
    带重试和增强异常处理的 Ollama 查询函数
    """
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": stream}

    session = create_session()

    try:
        # 将超时时间提高到 120s 以应对复杂推理
        response = session.post(url, json=payload, timeout=timeout)
        response.raise_for_status()

        if stream:
            return _handle_stream(response)
        else:
            try:
                result = response.json()
                return result.get("response", "")
            except json.JSONDecodeError:
                return f"Error: 无法从 {url} 解析 JSON 响应"

    except requests.exceptions.RequestException as e:
        logger.error(f"连接 Ollama 失败: {e}")
        return f"Error: {str(e)}"


def _handle_stream(response: requests.Response) -> Generator[str, None, None]:
    """流式响应处理辅助函数"""
    for line in response.iter_lines():
        if not line:
            continue
        try:
            chunk = json.loads(line)
            if not chunk.get("done"):
                yield chunk.get("response", "")
        except json.JSONDecodeError:
            logger.warning("跳过一个格式错误的流数据块")
            continue


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('用法: python ollama_query.py "prompt" [model]')
        sys.exit(1)

    user_prompt = sys.argv[1]
    target_model = sys.argv[2] if len(sys.argv) > 2 else OLLAMA_MODEL

    # 执行非流式查询并输出
    result = query_ollama(user_prompt, target_model, stream=False)

    if isinstance(result, str):
        print(result)
    else:
        # 如果后续需要在命令行启用流式，此逻辑可处理生成器
        for text in result:
            print(text, end="", flush=True)

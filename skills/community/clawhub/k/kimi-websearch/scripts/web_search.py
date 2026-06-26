import argparse
import datetime
import json
import os
from typing import Any, Optional

from openai import OpenAI
from openai.types.chat.chat_completion import Choice

# Kimi API 的 BASE_URL 和 MODEL_NAME，都是固定的参数，不需要用户修改。
BASE_URL = "https://api.moonshot.cn/v1"
MODEL_NAME = "kimi-k2-turbo-preview"

# 系统提示词
DEFAULT_SYSTEM_PROMPT = f"""
现在的时间是:{datetime.datetime.now().isoformat()}。
搜索的时候需要提供消息来源的url，确保信息的准确性。
"""


# Kimi 月之暗面 支持多种环境变量来配置 API Key，以适配不同的使用场景和用户习惯
KIMI_SUPPORTED_ENVS = [
    "KIMI_API_KEY",  # 通用的 API Key 环境变量，适用于大多数用户和场景。
    "MOONSHOT_API_KEY",  # Moonshot 官方推荐的 API Key 环境变量，
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="使用 Moonshot Kimi 的 $web_search 工具执行联网搜索"
    )
    parser.add_argument(
        "question",
        help="要搜索的话题、关键词或完整问题，例如：今天有什么新闻大事",
    )
    parser.add_argument(
        "--system-prompt",
        default=DEFAULT_SYSTEM_PROMPT,
        help="可选的系统提示词，用于设定模型的行为和回答风格，默认为当前时间和搜索要求的提示词",
    )
    return parser


def get_api_key() -> str:

    api_key: Optional[str] = None
    for env_var in KIMI_SUPPORTED_ENVS:
        api_key = os.environ.get(env_var)
        if api_key:
            break
    if not api_key:
        raise ValueError(
            f"API key not found."
            f"请登录 `https://platform.moonshot.cn/console/api-keys` 获取 API Key，并将其设置为环境变量。"
            f"Please set one of the following environment variables: {', '.join(KIMI_SUPPORTED_ENVS)}"
        )
    return api_key


def get_client(api_key: str) -> OpenAI:
    """初始化 OpenAI 客户端，BASE_URL 和 API Key 都是必需的参数。"""
    return OpenAI(base_url=BASE_URL, api_key=api_key)


def build_user_message(message: str) -> str:
    query = message.strip()
    if not query:
        raise ValueError("message must not be empty.")

    if query.startswith("请") or "搜索" in query:
        return query

    return f"请使用联网搜索工具搜索并回答：{query}"


def chat(client: OpenAI, messages: list[Any]) -> Choice:
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.6,
        max_tokens=32768,
        tools=[
            {
                "type": "builtin_function",  # <-- 使用 builtin_function 声明 $web_search 函数，请在每次请求都完整地带上 tools 声明
                "function": {
                    "name": "$web_search",
                },
            }
        ],
    )
    return completion.choices[0]


def main() -> None:
    args = build_parser().parse_args()
    api_key = get_api_key()
    client = get_client(api_key)
    messages = [
        {"role": "system", "content": args.system_prompt},
    ]

    messages.append(
        {
            "role": "user",
            "content": build_user_message(args.question),
        }
    )

    finish_reason = None
    while finish_reason is None or finish_reason == "tool_calls":
        choice = chat(client, messages)
        finish_reason = choice.finish_reason
        if finish_reason == "tool_calls":  # <-- 判断当前返回内容是否包含 tool_calls
            messages.append(
                choice.message
            )  # <-- 我们将 Kimi 大模型返回给我们的 assistant 消息也添加到上下文中，以便于下次请求时 Kimi 大模型能理解我们的诉求
            for tool_call in (
                choice.message.tool_calls
            ):  # <-- tool_calls 可能是多个，因此我们使用循环逐个执行
                tool_call_name = tool_call.function.name
                tool_call_arguments = json.loads(
                    tool_call.function.arguments
                )  # <-- arguments 是序列化后的 JSON Object，我们需要使用 json.loads 反序列化一下
                if tool_call_name == "$web_search":
                    tool_result = tool_call_arguments
                else:
                    tool_result = (
                        f"Error: unable to find tool by name '{tool_call_name}'"
                    )

                # 使用函数执行结果构造一个 role=tool 的 message，以此来向模型展示工具调用的结果；
                # 注意，我们需要在 message 中提供 tool_call_id 和 name 字段，以便 Kimi 大模型
                # 能正确匹配到对应的 tool_call。
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call_name,
                        "content": json.dumps(
                            tool_result
                        ),  # <-- 我们约定使用字符串格式向 Kimi 大模型提交工具调用结果，因此在这里使用 json.dumps 将执行结果序列化成字符串
                    }
                )

    print(choice.message.content or "")  # <-- 在这里，我们才将模型生成的回复返回给用户


if __name__ == "__main__":
    main()

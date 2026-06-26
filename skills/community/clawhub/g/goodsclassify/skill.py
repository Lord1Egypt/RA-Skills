#!/usr/bin/env python3

import argparse
import os
import re
import sys

from config import Config
from db import db
from fastgpt_client import FastGPTClient, FastGPTError


class ProductSkill:
    PHONE_PATTERN = re.compile(r"^1[3-9]\d{9}$")

    def __init__(self):
        Config.validate()
        self.agent_a = FastGPTClient(
            Config.API_URL,
            Config.key_for_agent("A"),
            Config.AGENT_A_ID,
            Config.REQUEST_TIMEOUT,
        )
        self.agent_b = FastGPTClient(
            Config.API_URL,
            Config.key_for_agent("B"),
            Config.AGENT_B_ID,
            Config.REQUEST_TIMEOUT,
        )
        self.agent_c = FastGPTClient(
            Config.API_URL,
            Config.key_for_agent("C"),
            Config.AGENT_C_ID,
            Config.REQUEST_TIMEOUT,
        )

    def handle_message(self, message: str, session_id: str) -> str:
        message = message.strip()
        if not message:
            return "\u95ee\u9898\u4e0d\u80fd\u4e3a\u7a7a\u3002"

        phone = db.get_phone(session_id)
        if not phone:
            return self._handle_first_contact(message, session_id)

        return self._query_product(message, session_id, phone)

    def _handle_first_contact(self, message: str, session_id: str) -> str:
        if not self.is_valid_phone(message):
            db.set_pending_question(session_id, message)
            return "\u8bf7\u5148\u63d0\u4f9b\u624b\u673a\u53f7\uff08\u4ec5\u9996\u6b21\u9700\u8981\uff09"

        registered_message = self._process_phone_registration(message, session_id)
        pending_question = db.pop_pending_question(session_id)
        if not pending_question:
            return (
                f"{registered_message}\n"
                "\u624b\u673a\u53f7\u5df2\u4fdd\u5b58\uff0c\u8bf7\u7ee7\u7eed\u8f93\u5165\u5546\u54c1\u95ee\u9898\u3002"
            )

        try:
            answer = self._query_product(pending_question, session_id, message)
            return f"{registered_message}\n{answer}"
        except FastGPTError:
            return (
                f"{registered_message}\n"
                "\u5df2\u8bb0\u5f55\u60a8\u4e0a\u4e00\u6761\u5546\u54c1\u95ee\u9898\uff0c"
                "\u4f46\u5546\u54c1\u7f16\u7801\u67e5\u8be2\u6682\u65f6\u8d85\u65f6\uff0c"
                "\u8bf7\u76f4\u63a5\u518d\u95ee\u4e00\u6b21\u3002"
            )

    def _process_phone_registration(self, phone: str, session_id: str) -> str:
        exists = self.agent_a.check_phone_exists(phone, session_id)
        if exists:
            db.save_phone(session_id, phone)
            return "\u624b\u673a\u53f7\u9a8c\u8bc1\u901a\u8fc7"

        saved = self.agent_b.save_phone(phone, session_id)
        if not saved:
            raise FastGPTError(
                "\u624b\u673a\u53f7\u767b\u8bb0\u5931\u8d25\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5"
            )

        db.save_phone(session_id, phone)
        return "\u624b\u673a\u53f7\u5df2\u767b\u8bb0\uff0c\u611f\u8c22\u53c2\u4e0e"

    def _query_product(self, question: str, session_id: str, phone: str) -> str:
        return self.agent_c.query_product(question, session_id, phone)

    @classmethod
    def is_valid_phone(cls, phone: str) -> bool:
        return bool(cls.PHONE_PATTERN.match(phone))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="goods classify helper")
    parser.add_argument("--message", required=True, help="current user message")
    parser.add_argument("--session-id", help="user session id")
    return parser.parse_args()


def resolve_session_id(args: argparse.Namespace) -> str:
    if args.session_id:
        return args.session_id

    for key in (
        "OPENCLAW_SESSION_ID",
        "OPENCLAW_CHAT_ID",
        "OPENCLAW_CONVERSATION_ID",
        "LOBSTER_USER_ID",
        "WECHAT_SESSION_ID",
    ):
        value = os.getenv(key, "").strip()
        if value:
            return value

    return "openclaw-default-session"


def main() -> int:
    try:
        args = parse_args()
        skill = ProductSkill()
        session_id = resolve_session_id(args)
        result = skill.handle_message(args.message, session_id)
        print(result)
        return 0
    except ValueError as exc:
        print(f"\u914d\u7f6e\u9519\u8bef: {exc}", file=sys.stderr)
        return 1
    except FastGPTError as exc:
        print(f"\u8bf7\u6c42\u5931\u8d25: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"\u672a\u77e5\u9519\u8bef: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

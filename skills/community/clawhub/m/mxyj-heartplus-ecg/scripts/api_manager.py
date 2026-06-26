#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
# ]
# ///
# -*- coding: utf-8 -*-

"""
心脏+ Skill 原子接口编排（BIN 加密链路版）。
"""

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

from config_manager import ConfigManager
from errors import JsonArgumentParser, SkillError
from gateway_manager import GatewayManager
from phone_manager import PhoneManager
from schemas import DataListResult, EcgListItem, ReportDetail
from template_renderer import TemplateRenderer

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
RECENT_REPORT_LIST_CACHE_FILE = SKILL_ROOT / "report_list_cache.json"
MAINLAND_USER_NOTICE = "当前仅支持中国大陆手机号用户使用本服务。"
APP_DOWNLOAD_URL = "https://apps.apple.com/cn/app/%E5%BF%83%E8%84%8F-%E5%BF%83%E7%8E%87-%E5%BF%83%E8%B7%B3-%E5%BF%83%E8%84%8F%E5%81%A5%E5%BA%B7%E6%A3%80%E6%B5%8B/id1584620848"


class ApiManager:
    def __init__(self, session_key: str):
        self.config = ConfigManager()
        self.session_key = self.config.resolve_session_key(session_key)
        self.phone_manager = PhoneManager(session_key=self.session_key)
        self.gateway = GatewayManager(session_key=self.session_key)
        self.renderer = TemplateRenderer()

        self.base_url = str(self.config.get("base_url", "https://api.995120.cn")).rstrip("/")

    @staticmethod
    def get_api_headers() -> dict[str, str]:
        headers = {"content-type": "application/json"}
        if ConfigManager().is_dev():
            headers["x-version"] = "v1.0.0-beta"
        return headers

    @staticmethod
    def is_ok(resp_code: str) -> bool:
        return resp_code == "000" or resp_code == "0"

    def _ensure_phone(self) -> str:
        return self.phone_manager.get_phone()

    def send_code(self) -> bool:
        phone = self._ensure_phone()
        headers = self.get_api_headers()
        payload = {"body": {"mobile": phone, "source": 16}}

        headers.pop("x-version", None)

        try:
            response = requests.post(
                f"{self.base_url}/mini/api/appleplus/sendCodeOpenclaw",
                headers=headers,
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
        except requests.Timeout as e:
            raise SkillError("验证码发送超时，请检查网络后重试", {"reason": str(e)})
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else None
            raise SkillError("验证码发送失败，服务暂时不可用，请稍后重试", {"status_code": status_code})
        except requests.RequestException as e:
            raise SkillError("验证码发送失败，请检查网络后重试", {"reason": str(e)})

        try:
            data = response.json()
        except ValueError as e:
            raise SkillError(
                "验证码发送结果解析失败，请稍后重试",
                {"reason": str(e), "raw": (response.text or "")[:200]},
            )

        if not isinstance(data, dict) or not data:
            raise SkillError("验证码发送服务返回空数据，请稍后重试")

        resp_head = data.get("respHead") or {}
        code = str(resp_head.get("respCode", ""))
        message = str(resp_head.get("respMsg", ""))

        if not self.is_ok(code):
            raise SkillError("验证码发送未完成，请确认手机号可正常接收短信后重试", {"code": code, "message": message})
        return True

    @staticmethod
    def _validate_datetime_str(value: str, field_name: str) -> None:
        if not value:
            return
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", value):
            raise SkillError(
                f"{field_name} 格式不正确，请改为 YYYY-MM-DD HH:mm:ss 后重试",
                {"value": value, "example": "2026-03-06 15:28:54"},
            )
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise SkillError(
                f"{field_name} 时间值无效，请使用真实日期时间后重试",
                {"value": value, "example": "2026-03-06 15:28:54"},
            )

    @staticmethod
    def _normalize_biz_result(data: dict) -> dict:
        if "respHead" in data and "body" in data:
            resp_code = str((data.get("respHead") or {}).get("respCode", ""))
            resp_msg = str((data.get("respHead") or {}).get("respMsg", ""))
            if resp_code and not ApiManager.is_ok(resp_code):
                raise SkillError("请求未完成，请稍后重试",
                                 {"code": resp_code, "message": resp_msg})
            return data

        if "code" in data and "message" in data:
            code = str(data.get("code", ""))
            if code not in {"0", "000"}:
                raise SkillError("请求未完成，请稍后重试",
                                 {"code": code, "message": data.get("message", "")})
            return {
                "respHead": {"respCode": "000", "respMsg": data.get("message", "")},
                "body": {"data": data.get("data")},
            }

        raise SkillError("系统返回内容暂时无法识别，请稍后重试", {"keys": list(data.keys())})

    @staticmethod
    def _is_plain_error_payload(data: dict) -> bool:
        if "respHead" in data:
            resp_code = str((data.get("respHead") or {}).get("respCode", ""))
            return bool(resp_code) and not ApiManager.is_ok(resp_code)

        if "code" in data and "message" in data:
            code = str(data.get("code", ""))
            return code not in {"0", "000"}

        return False

    def _ensure_gateway_available(self) -> None:
        self.gateway.ensure_binary(auto_download=True)
        check_result = self.gateway.check_factory()
        check_code = str(check_result.get("code", ""))
        if check_code not in {"0", "000"}:
            raise SkillError(
                "当前授权校验未就绪，请先发送APP授权通知并确认授权，再执行 verify 完成校验",
                {"next_action": "ask_send_authorize_notify"}
            )
        if not self.config.is_session_authorized(self.session_key):
            raise SkillError(
                "当前会话尚未完成身份校验，请先发送授权通知并按提示完成校验",
                {"next_action": "ask_send_authorize_notify", "session_key": self.session_key},
            )

    def _call_plain_api(self, function_id: str, body: dict, timeout: int = 10) -> dict:
        payload = {
            "reqHead": {"functionId": function_id},
            "body": body,
        }

        headers = self.get_api_headers()

        try:
            resp = requests.post(
                f"{self.base_url}/mini/h5api/",
                headers=headers,
                json=payload,
                timeout=timeout,
            )

            resp.raise_for_status()
        except requests.Timeout as e:
            raise SkillError("请求超时，请检查网络后重试", {"functionId": function_id, "error": str(e)})
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else None
            raise SkillError("请求失败，服务暂时不可用，请稍后重试",
                             {"functionId": function_id, "status_code": status_code})
        except requests.RequestException as e:
            raise SkillError("请求发送失败，请检查网络后重试", {"functionId": function_id, "error": str(e)})

        try:
            data = resp.json()
        except ValueError as e:
            raise SkillError("响应解析失败，请稍后重试",
                             {"functionId": function_id, "reason": str(e), "raw": (resp.text or "")[:200]})

        if not isinstance(data, dict):
            raise SkillError("响应结构异常，请稍后重试",
                             {"functionId": function_id, "response_type": type(data).__name__})
        return self._normalize_biz_result(data)

    @staticmethod
    def _build_encrypted_headers(enc_data: dict) -> tuple[dict[str, str], str]:
        x_mobile = enc_data.get("x_mobile", "")
        x_device_sn = enc_data.get("x_device_sn", "")
        enc_body = enc_data.get("body", "")
        if not x_mobile or not x_device_sn or not enc_body:
            raise SkillError("安全通信准备未完成，请重新发起APP授权并执行 verify 后重试", {"data": enc_data})

        headers = ApiManager.get_api_headers()
        headers["Content-Type"] = "text/plain;charset=UTF-8"
        headers["X-Mobile"] = x_mobile
        headers["X-Device-Sn"] = x_device_sn
        return headers, enc_body

    def _encrypt_payload(self, function_id: str, body: dict) -> tuple[dict[str, str], str]:
        biz_json = json.dumps(
            {
                "reqHead": {"functionId": function_id},
                "body": body,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )

        enc_result = self.gateway.encry(biz_json)
        enc_code = str(enc_result.get("code", ""))
        if enc_code in {"1002", "1003"}:
            raise SkillError(
                "授权状态已失效，请先重新发送APP授权通知并确认授权，再执行 verify",
                {"next_action": "ask_send_authorize_notify"}
            )
        if enc_code not in {"0", "000"}:
            raise SkillError("请求准备失败，请确认APP授权状态并重新执行 verify 后再试",
                             {"code": enc_code, "message": enc_result.get("message", "")})

        enc_data = enc_result.get("data") or {}
        return self._build_encrypted_headers(enc_data)

    @staticmethod
    def _decode_gateway_payload(decry_data, function_id: str) -> dict:
        current = decry_data
        for _ in range(6):
            if isinstance(current, dict):
                if "respHead" in current and "body" in current:
                    return current
                if "code" in current and "message" in current:
                    return current
                if "data" in current and len(current) == 1:
                    current = current.get("data")
                    continue
                return current

            if isinstance(current, str):
                decrypted_text = current.strip()
                if not decrypted_text:
                    raise SkillError("返回内容为空，请稍后重试；如持续失败请重新校验授权状态",
                                     {"functionId": function_id})
                try:
                    current = json.loads(decrypted_text)
                    continue
                except json.JSONDecodeError as e:
                    raise SkillError(
                        "返回内容解析失败，请稍后重试；如持续失败请重新发起APP授权并校验",
                        {"functionId": function_id, "reason": str(e), "raw": decrypted_text[:200]},
                    )

            raise SkillError("返回结构异常，请稍后重试；如持续失败请重新校验授权状态",
                             {"functionId": function_id, "data_type": type(current).__name__})

        raise SkillError("返回结构异常，请稍后重试；如持续失败请重新校验授权状态",
                         {"functionId": function_id, "reason": "nested_payload_too_deep"})

    def _parse_device_response(self, resp: requests.Response, function_id: str) -> dict:
        resp.raise_for_status()
        raw = (resp.text or "").strip()

        if not raw:
            raise SkillError("服务暂时无返回，请稍后重试", {"functionId": function_id, "status_code": resp.status_code})

        try:
            plain_json = json.loads(raw)
        except json.JSONDecodeError:
            plain_json = None

        if isinstance(plain_json, dict) and self._is_plain_error_payload(plain_json):
            return self._normalize_biz_result(plain_json)

        decry_result = self.gateway.decry(raw)
        decry_code = str(decry_result.get("code", ""))
        if decry_code in {"1002", "1003"}:
            raise SkillError(
                "授权状态已过期，请先发送APP授权通知并确认授权，再执行 verify 完成校验",
                {"next_action": "ask_send_authorize_notify"}
            )
        if decry_code not in {"0", "000"}:
            raise SkillError("结果解析失败，请重新发起APP授权并执行 verify 后再试",
                             {"code": decry_code, "message": decry_result.get("message", "")})

        decry_data = decry_result.get("data")
        try:
            parsed = self._decode_gateway_payload(decry_data, function_id)
            return self._normalize_biz_result(parsed)
        except SkillError:
            raise
        except (TypeError, ValueError, KeyError) as e:
            raise SkillError("结果处理失败，请稍后重试", {"functionId": function_id, "error": str(e)})

    def _call_common(self, function_id: str, body: dict) -> dict:
        self._ensure_phone()
        self._ensure_gateway_available()
        headers, enc_body = self._encrypt_payload(function_id, body)

        try:
            resp = requests.post(
                f"{self.base_url}/mini/device/",
                data=enc_body,
                headers=headers,
                timeout=20,
            )

            return self._parse_device_response(resp, function_id)
        except SkillError:
            raise
        except requests.Timeout as e:
            raise SkillError("请求超时，请检查网络后重试", {"functionId": function_id, "error": str(e)})
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else None
            raise SkillError("请求失败，服务暂时不可用，请稍后重试",
                             {"functionId": function_id, "status_code": status_code})
        except requests.RequestException as e:
            raise SkillError("请求发送失败，请检查网络后重试", {"functionId": function_id, "error": str(e)})

    def _load_recent_report_list_cache_payload(self) -> dict:
        cache_file = RECENT_REPORT_LIST_CACHE_FILE
        if not cache_file.exists():
            return {}
        try:
            with cache_file.open("r", encoding="utf-8") as f:
                raw = f.read().strip()
            if not raw:
                return {}
            payload = json.loads(raw)
            if isinstance(payload, dict):
                return payload
            return {}
        except json.JSONDecodeError:
            return {}
        except OSError as e:
            raise SkillError("最近报告列表读取失败，请重新执行 --action report_list", {"reason": str(e)})

    def _save_recent_report_list_cache(self, report_nos: list[str]) -> None:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = self._load_recent_report_list_cache_payload()
        sessions = payload.get("sessions", {}) if isinstance(payload, dict) else {}
        if not isinstance(sessions, dict):
            sessions = {}
        sessions[self.session_key] = {
            "updated_at": now_str,
            "report_nos": report_nos,
        }
        next_payload = {
            "updated_at": now_str,
            "sessions": sessions,
        }
        temp_file = RECENT_REPORT_LIST_CACHE_FILE.with_suffix(".json.tmp")
        try:
            with temp_file.open("w", encoding="utf-8") as f:
                json.dump(next_payload, f, ensure_ascii=False, indent=2)
            temp_file.replace(RECENT_REPORT_LIST_CACHE_FILE)
        except OSError as e:
            raise SkillError("报告列表保存失败，请重新执行 report_list", {"reason": str(e)})

    def _load_recent_report_list_cache(self) -> list[str]:
        payload = self._load_recent_report_list_cache_payload()
        sessions = payload.get("sessions", {}) if isinstance(payload, dict) else {}
        if not isinstance(sessions, dict):
            raise SkillError("最近报告列表格式异常，请重新执行 --action report_list", {"field": "sessions"})
        session_payload = sessions.get(self.session_key)
        if not isinstance(session_payload, dict):
            raise SkillError(
                "还没有可用的报告列表，请先执行 --action report_list，再按序号查看详情",
                {"suggestion": "先执行 --action report_list，再使用 --index", "session_key": self.session_key},
            )
        report_nos = session_payload.get("report_nos", [])
        if not isinstance(report_nos, list):
            raise SkillError("最近报告列表格式异常，请重新执行 --action report_list", {"field": "report_nos"})

        normalized = [str(item).strip() for item in report_nos if str(item).strip()]
        if not normalized:
            raise SkillError(
                "最近报告列表为空，请先执行 --action report_list 获取可选序号",
                {"suggestion": "重新执行 --action report_list 获取最新列表"},
            )
        return normalized

    def resolve_report_no(self, report_no: Optional[str], index: Optional[int]) -> str:
        normalized_report_no = str(report_no).strip() if report_no else ""
        if normalized_report_no and index is None and re.fullmatch(r"\d{1,3}", normalized_report_no):
            index = int(normalized_report_no)
            normalized_report_no = ""

        if normalized_report_no:
            return normalized_report_no

        if index is None:
            raise SkillError("查看报告详情前请先提供报告编号：可直接回复序号，或使用 --index / --report-no")
        if index <= 0:
            raise SkillError("序号需要从 1 开始，请改为 1 或更大的数字", {"index": index})

        report_nos = self._load_recent_report_list_cache()
        if index > len(report_nos):
            raise SkillError(
                "输入序号超出最近列表范围，请先查看最新列表后再选择序号",
                {
                    "index": index,
                    "max_index": len(report_nos),
                    "suggestion": "请重新执行 --action report_list 获取最新列表",
                },
            )
        return report_nos[index - 1]

    def notify_measure_ecg(self) -> str:
        phone = self._ensure_phone()
        result_json = self._call_common("XHJD900103002", {"mobile": phone})
        resp_head = result_json.get("respHead") or {}
        if self.is_ok(str(resp_head.get("respCode", ""))):
            return f"已为您下发心电测量通知。\n请现在按手表提示完成测量。\n完成后回复“已完成”，我马上帮您看结果。\n{MAINLAND_USER_NOTICE}"
        raise SkillError("通知下发失败，请稍后重试；若未收到通知，请确认心脏+APP已安装并登录后再试", {"respHead": resp_head})

    def send_authorize_notify(self) -> dict:
        phone = self._ensure_phone()
        result_json = self._call_plain_api("XHJD900103005", {"mobile": phone})
        resp_head = result_json.get("respHead") or {}
        if self.is_ok(str(resp_head.get("respCode", ""))):
            self.config.set_session_authorized(self.session_key, False)
            data = result_json.get("body", {}).get("data", {})
            if not isinstance(data, dict):
                data = {}
            mode_status = str(data.get("status", "")).strip()
            push_result = str(data.get("result", "")).strip()

            if mode_status == "0":
                sms_sent = True
                sms_send_error: dict | None = None
                try:
                    self.send_code()
                except SkillError as e:
                    sms_sent = False
                    sms_send_error = {
                        "message": e.message,
                        "details": e.details,
                    }
                return {
                    "auth_status": False,
                    "verify_status": "WAITING_SMS_CODE",
                    "auth_mode": "SMS_CODE",
                    "status": "0",
                    "next_action": "ask_user_sms_code_then_verify",
                    "sms_sent": sms_sent,
                    "push_result": push_result,
                    "sms_send_error": sms_send_error,
                    "user_message": (
                        f"已为您发送短信验证码，确定收到验证码后请把短信验证码发给我，我将立即为您完成后续校验。{MAINLAND_USER_NOTICE}"
                        if sms_sent
                        else f"已进入短信验证码校验流程。如您已收到验证码，请直接发我验证码继续校验；若暂未收到，可稍后重试发送验证码。{MAINLAND_USER_NOTICE}"
                    ),
                }

            if mode_status == "1":
                return {
                    "auth_status": False,
                    "verify_status": "WAITING_APP_AUTH",
                    "auth_mode": "APP_AUTH",
                    "status": "1",
                    "next_action": "wait_user_confirm_then_poll_authorization",
                    "push_result": push_result,
                    "user_message": f"已向您手机上的心脏+APP发送授权通知。请先在APP内确认授权，完成后回复“已授权”。若未收到消息，请先确认已安装并登录心脏+APP：{APP_DOWNLOAD_URL}",
                }

            raise SkillError(
                "授权方式暂无法识别，请稍后重试",
                {"status": mode_status, "push_result": push_result},
            )
        raise SkillError("授权通知发送失败，请稍后重试", {"respHead": resp_head})

    def verify_sms_code(self, code: str) -> dict:
        normalized = str(code).strip()
        if not normalized:
            raise SkillError("请先提供短信验证码后再继续校验")
        verify_result = self._verify_authorization_status(normalized)
        if verify_result.get("verify_status") == "VERIFIED":
            return {
                "auth_status": True,
                "verify_status": "VERIFIED",
                "next_action": "continue_business",
                "auth_mode": "SMS_CODE",
                "user_message": "验证码校验已通过，正在继续后续步骤。",
            }
        return {
            "auth_status": False,
            "verify_status": verify_result.get("verify_status", "VERIFY_PENDING"),
            "next_action": verify_result.get("next_action", "ask_wait_or_resend"),
            "auth_mode": "SMS_CODE",
            "user_message": "验证码校验未完成，请确认验证码后重试；若暂未收到验证码，请稍后重试发送。",
        }

    def _verify_authorization_status(self, auth_code: str) -> dict:
        result = self.gateway.verify(auth_code)
        verify_code = str(result.get("code", ""))
        if verify_code in {"0", "000"}:
            self.config.set_session_authorized(self.session_key, True)
            return {
                "verify_status": "VERIFIED",
                "next_action": "continue_business",
            }
        if verify_code in {"1002", "1003"}:
            return {
                "verify_status": "VERIFY_PENDING",
                "next_action": "ask_wait_or_resend",
            }
        raise SkillError("授权校验未完成，请确认APP授权状态后重试",
                         {"code": verify_code, "message": result.get("message", "")})

    def query_ecg_authorization(self) -> dict:
        phone = self._ensure_phone()
        result_json = self._call_plain_api("XHJD900103008", {"mobile": phone})
        data = result_json.get("body", {}).get("data", {})
        if not isinstance(data, dict):
            raise SkillError("授权查询返回结构异常，请稍后重试", {"data_type": type(data).__name__})

        raw_status = data.get("authStatus", False)
        auth_status = raw_status if isinstance(raw_status, bool) else str(raw_status).lower() in {"1", "true", "yes"}
        auth_code = str(data.get("code", "")).strip()

        if auth_status and not auth_code:
            raise SkillError(
                "已检测到用户完成授权，但授权码暂不可用，请稍后再查一次",
                {"next_action": "ask_wait_or_query_again", "auth_status": True}
            )

        if auth_status:
            verify_result = self._verify_authorization_status(auth_code)
            return {
                "auth_status": True,
                "verify_status": verify_result["verify_status"],
                "next_action": verify_result["next_action"],
                "user_message": "授权状态已确认，正在继续处理后续步骤。",
            }

        return {
            "auth_status": False,
            "verify_status": "WAITING_AUTH",
            "next_action": "ask_wait_or_resend",
            "user_message": "暂未检测到授权，请在心脏+APP完成授权后继续；若未收到通知可回复“重新发送授权通知”。",
        }

    def poll_ecg_authorization(self, max_wait_seconds: int = 45, interval_seconds: int = 3) -> dict:
        if max_wait_seconds <= 0:
            raise SkillError("max_wait_seconds 必须大于 0")
        if interval_seconds <= 0:
            raise SkillError("interval_seconds 必须大于 0")

        started_at = time.time()
        attempts = 0
        while True:
            attempts += 1
            status = self.query_ecg_authorization()
            if status.get("auth_status") and status.get("verify_status") == "VERIFIED":
                status["state"] = "VERIFIED"
                status["attempts"] = attempts
                return status

            elapsed = int(time.time() - started_at)
            if elapsed >= max_wait_seconds:
                return {
                    "state": "TIMEOUT",
                    "auth_status": False,
                    "verify_status": "WAITING_AUTH",
                    "attempts": attempts,
                    "elapsed_seconds": elapsed,
                    "next_action": "ask_user_wait_or_resend",
                    "user_hint": "暂未检测到授权。请先确认心脏+APP已安装并登录且可接收通知，再询问用户是否继续等待或重新发送授权通知。",
                }
            time.sleep(interval_seconds)

    def get_data_list(
            self,
            page_num: int = 0,
            page_size: int = 10,
            take_time_copy: str = "",
            take_time_over: str = ""
    ) -> DataListResult:
        phone = self._ensure_phone()
        self._validate_datetime_str(take_time_copy, "takeTimeCopy/start")
        self._validate_datetime_str(take_time_over, "takeTimeOver/end")

        body = {
            "mobile": phone,
            "pageNum": page_num,
            "pageSize": page_size,
        }
        if take_time_copy:
            body["takeTimeCopy"] = take_time_copy
        if take_time_over:
            body["takeTimeOver"] = take_time_over

        result_json = self._call_common("XHJD900103004", body)

        data_block = result_json.get("body", {}).get("data", {})
        status_str = str(data_block.get("status", "0"))
        is_success = status_str == "1"

        ecg_list_data = data_block.get("ecgList", [])
        ecg_list = [EcgListItem.from_dict(item) for item in ecg_list_data] if ecg_list_data else []
        ecg_list = [item for item in ecg_list if item.reportNo]
        ecg_list.sort(key=lambda x: x.takeTime, reverse=True)

        return DataListResult(status=is_success, datas=ecg_list)

    def get_report_detail(self, report_no: str) -> Optional[ReportDetail]:

        result_json = self._call_common(
            "XHJD001114011",
            {"reportNo": report_no, "channel": "applePlus"},
        )

        data = result_json.get("body", {}).get("data")
        if not data:
            return None

        return ReportDetail.from_dict(data)

    def get_latest_report_detail(self) -> Optional[ReportDetail]:
        result = self.get_data_list(page_num=0, page_size=1)
        if not result.datas:
            return None
        return self.get_report_detail(result.datas[0].reportNo)

    def render_report_list(
            self,
            page_num: int = 0,
            page_size: int = 10,
            take_time_copy: str = "",
            take_time_over: str = ""
    ) -> str:
        result = self.get_data_list(
            page_num=page_num,
            page_size=page_size,
            take_time_copy=take_time_copy,
            take_time_over=take_time_over,
        )

        self._save_recent_report_list_cache([item.reportNo for item in result.datas if item.reportNo])
        return self.renderer.render_report_list(result.datas)

    def render_report_detail(self, report_no: str) -> str:
        detail = self.get_report_detail(report_no)
        if not detail:
            raise SkillError("未找到对应报告，请先刷新报告列表并确认报告编号后再试", {"reportNo": report_no})
        return self.renderer.render_report_detail(detail)

    def render_latest_report(self) -> str:
        detail = self.get_latest_report_detail()

        if not detail:
            return self.renderer.render_report_list([])
        return self.renderer.render_report_detail(detail)


def handle_action(args, manager: ApiManager) -> None:
    if args.action == "send_code":
        print(manager.send_code())
    elif args.action == "verify_code":
        print(json.dumps(manager.verify_sms_code(args.code), ensure_ascii=False))
    elif args.action == "send_authorize_notify":
        print(json.dumps(manager.send_authorize_notify(), ensure_ascii=False))
    elif args.action == "query_authorization":
        print(json.dumps(manager.query_ecg_authorization(), ensure_ascii=False))
    elif args.action == "poll_authorization":
        print(json.dumps(
            manager.poll_ecg_authorization(
                max_wait_seconds=args.max_wait_seconds,
                interval_seconds=args.interval_seconds,
            ),
            ensure_ascii=False,
        ))
    elif args.action == "measure_notify":
        print(manager.notify_measure_ecg())
    elif args.action == "report_list":
        print(
            manager.render_report_list(
                page_num=args.page_num,
                page_size=args.page_size,
                take_time_copy=args.take_time_copy,
                take_time_over=args.take_time_over,
            )
        )
    elif args.action == "latest_report":
        print(manager.render_latest_report())
    elif args.action == "report_detail":
        if args.report_no and args.index is not None:
            print(
                "已同时提供 --report-no 与 --index：本次优先使用 --report-no。也可仅回复序号或仅传 --index。",
                file=sys.stderr,
            )
        resolved_report_no = manager.resolve_report_no(args.report_no, args.index)
        print(manager.render_report_detail(resolved_report_no))


if __name__ == "__main__":
    try:
        parser = JsonArgumentParser()
        parser.add_argument(
            "--action",
            choices=[
                "send_code",
                "verify_code",
                "send_authorize_notify",
                "query_authorization",
                "poll_authorization",
                "measure_notify",
                "report_list",
                "latest_report",
                "report_detail",
            ],
            required=True,
        )
        parser.add_argument("--page-num", type=int, default=0)
        parser.add_argument("--page-size", type=int, default=10)
        parser.add_argument("--take-time-copy", dest="take_time_copy", type=str, default="")
        parser.add_argument("--take-time-over", dest="take_time_over", type=str, default="")
        parser.add_argument("--report-no", "--report-id", "--reportId", dest="report_no", type=str)
        parser.add_argument("--index", type=int)
        parser.add_argument("--max-wait-seconds", type=int, default=45)
        parser.add_argument("--interval-seconds", type=int, default=3)
        parser.add_argument("--code", type=str, default="")
        parser.add_argument("--session-key", type=str, required=True,
                            help="Session key from current conversation context, e.g. agent:main:main")
        args = parser.parse_args()

        manager = ApiManager(session_key=args.session_key)
        handle_action(args, manager)
    except SkillError as e:
        print(json.dumps(e.to_dict(), ensure_ascii=False))
        raise SystemExit(1)
    except Exception as e:
        wrapped = SkillError("业务接口执行失败，请稍后重试", {"error": str(e)})
        print(json.dumps(wrapped.to_dict(), ensure_ascii=False))
        raise SystemExit(1)

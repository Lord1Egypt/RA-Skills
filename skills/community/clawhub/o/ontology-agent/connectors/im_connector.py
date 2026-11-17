#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
im_connector.py — 本体论智能体 · IM 连接器抽象基类（钉钉/企业微信/飞书统一端口）

数字公司（专家团）未来可经 IM 推消息、收事件、拉真实员工与角色视图。
本文件定义统一接口与"未配置即 stub"的行为；具体平台在 dingtalk/wecom/feishu 中实现。

未配置 API 凭证时，所有方法仅打印提示、绝不发起真实网络请求。
填好各自 CREDENTIALS 后，在 TODO 处接入真实平台开放 API 即可启用。
"""
from abc import ABC, abstractmethod


class BaseIMConnector(ABC):
    PLATFORM = "base"
    API_BASE = ""  # 填入平台 API 根地址
    # 各平台字段不同，子类覆盖；占位值以"填入"开头表示未配置
    CREDENTIALS = {
        "app_key": "填入应用 Key",
        "app_secret": "填入应用 Secret",
    }

    def __init__(self):
        self.configured = self._check_config()

    def _check_config(self):
        return all(
            v and not str(v).startswith("填入") for v in self.CREDENTIALS.values()
        )

    def _require_configured(self, action):
        if not self.configured:
            print(
                f"[stub][{self.PLATFORM}] 未配置 API，跳过 {action}；"
                f"请填入 {self.__class__.__name__}.CREDENTIALS"
            )
            return False
        return True

    @abstractmethod
    def send_message(self, to, text):
        """向指定接收方推送文本消息。未配置时返回 None。"""
        raise NotImplementedError

    @abstractmethod
    def receive_events(self):
        """拉取/订阅 IM 事件（如 @消息、审批）。未配置时返回 None。"""
        raise NotImplementedError

    @abstractmethod
    def get_users(self):
        """拉取组织成员，用于给真实员工分配角色视图。未配置时返回 None。"""
        raise NotImplementedError

    def status(self):
        return {"platform": self.PLATFORM, "configured": self.configured}

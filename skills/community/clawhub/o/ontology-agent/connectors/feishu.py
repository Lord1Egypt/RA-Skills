#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""飞书连接器 stub（未配置即打印提示，不发起真实请求）。"""
try:
    from .im_connector import BaseIMConnector
except ImportError:
    from im_connector import BaseIMConnector


class FeishuConnector(BaseIMConnector):
    PLATFORM = "feishu"
    API_BASE = "https://open.feishu.cn"

    CREDENTIALS = {
        "app_id": "填入飞书 App ID",
        "app_secret": "填入飞书 App Secret",
    }

    def send_message(self, to, text):
        if not self._require_configured("send_message"):
            return None
        # TODO: 1) POST {API_BASE}/open-apis/auth/v3/tenant_access_token/internal 取 token
        #       2) POST {API_BASE}/open-apis/im/v1/messages 发送（receive_id_type）
        raise NotImplementedError("飞书 send_message 待接入：取 tenant_access_token 后调用消息接口")

    def receive_events(self):
        if not self._require_configured("receive_events"):
            return None
        # TODO: 配置事件订阅回调 URL + 校验 signature，接收消息/卡片回传
        raise NotImplementedError("飞书 receive_events 待接入：事件订阅回调")

    def get_users(self):
        if not self._require_configured("get_users"):
            return None
        # TODO: GET {API_BASE}/open-apis/contact/v3/users 拉取通讯录
        raise NotImplementedError("飞书 get_users 待接入：通讯录用户接口")

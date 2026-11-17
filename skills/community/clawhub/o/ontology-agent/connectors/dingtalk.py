#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""钉钉连接器 stub（未配置即打印提示，不发起真实请求）。"""
try:
    from .im_connector import BaseIMConnector
except ImportError:
    from im_connector import BaseIMConnector


class DingTalkConnector(BaseIMConnector):
    PLATFORM = "dingtalk"
    API_BASE = "https://oapi.dingtalk.com"

    CREDENTIALS = {
        "app_key": "填入钉钉企业内部应用 AppKey",
        "app_secret": "填入钉钉企业内部应用 AppSecret",
    }

    def send_message(self, to, text):
        if not self._require_configured("send_message"):
            return None
        # TODO: 1) GET {API_BASE}/gettoken 用 app_key/app_secret 取 access_token
        #       2) POST {API_BASE}/topapi/message/corpconversation/send 发送
        raise NotImplementedError("钉钉 send_message 待接入：获取 access_token 后调用消息接口")

    def receive_events(self):
        if not self._require_configured("receive_events"):
            return None
        # TODO: 注册回调 URL + 验签，接收 @消息 / 审批等事件
        raise NotImplementedError("钉钉 receive_events 待接入：事件订阅回调")

    def get_users(self):
        if not self._require_configured("get_users"):
            return None
        # TODO: GET {API_BASE}/topapi/v2/user/list 拉取部门成员
        raise NotImplementedError("钉钉 get_users 待接入：通讯录接口")

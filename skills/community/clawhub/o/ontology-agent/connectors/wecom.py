#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""企业微信连接器 stub（未配置即打印提示，不发起真实请求）。"""
try:
    from .im_connector import BaseIMConnector
except ImportError:
    from im_connector import BaseIMConnector


class WeComConnector(BaseIMConnector):
    PLATFORM = "wecom"
    API_BASE = "https://qyapi.weixin.qq.com"

    CREDENTIALS = {
        "corpid": "填入企业微信 corpid",
        "corpsecret": "填入企业微信应用 Secret",
        "agentid": "填入企业微信应用 agentid",
    }

    def send_message(self, to, text):
        if not self._require_configured("send_message"):
            return None
        # TODO: 1) GET {API_BASE}/cgi-bin/gettoken 取 access_token
        #       2) POST {API_BASE}/cgi-bin/message/send 发送（带 agentid）
        raise NotImplementedError("企业微信 send_message 待接入：获取 access_token 后调用消息接口")

    def receive_events(self):
        if not self._require_configured("receive_events"):
            return None
        # TODO: 配置接收消息服务器 + 回调验签（AES），接收用户消息
        raise NotImplementedError("企业微信 receive_events 待接入：消息回调")

    def get_users(self):
        if not self._require_configured("get_users"):
            return None
        # TODO: GET {API_BASE}/cgi-bin/user/simplelist 拉取成员
        raise NotImplementedError("企业微信 get_users 待接入：通讯录成员接口")

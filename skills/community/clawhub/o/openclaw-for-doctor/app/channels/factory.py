from __future__ import annotations

from app.channels.adapters.dingtalk import DingTalkAdapter
from app.channels.adapters.email import EmailAdapter
from app.channels.adapters.feishu import FeishuAdapter
from app.channels.adapters.webchat import WebChatAdapter
from app.channels.adapters.wechat import WeChatAdapter
from app.channels.adapters.xiaohongshu import XiaoHongShuAdapter
from app.channels.base import ChannelAdapter
from app.core.models import ChannelType


class ChannelAdapterFactory:
    @staticmethod
    def create(channel: ChannelType) -> ChannelAdapter:
        mapping: dict[ChannelType, type[ChannelAdapter]] = {
            ChannelType.feishu: FeishuAdapter,
            ChannelType.dingtalk: DingTalkAdapter,
            ChannelType.email: EmailAdapter,
            ChannelType.wechat: WeChatAdapter,
            ChannelType.xiaohongshu: XiaoHongShuAdapter,
            ChannelType.webchat: WebChatAdapter,
        }
        adapter_cls = mapping[channel]
        return adapter_cls()

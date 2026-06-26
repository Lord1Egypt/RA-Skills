from app.channels.base import StaticChannelAdapter
from app.core.models import ChannelType


class WebChatAdapter(StaticChannelAdapter):
    channel = ChannelType.webchat

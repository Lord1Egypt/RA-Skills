from __future__ import annotations

from app.channels.factory import ChannelAdapterFactory
from app.core.models import ChannelType, DeliveryReceipt, TaskResult


class ChannelDispatcher:
    def dispatch(self, channel: ChannelType, result: TaskResult) -> DeliveryReceipt:
        adapter = ChannelAdapterFactory.create(channel)
        return adapter.send_result(result)

from app.channels.base import WebhookChannelAdapter
from app.channels.formatter import format_task_result_message
from app.core.models import ChannelType, TaskResult


class WeChatAdapter(WebhookChannelAdapter):
    channel = ChannelType.wechat
    webhook_env_key = "WECHAT_WEBHOOK_URL"

    def build_payload(self, result: TaskResult) -> dict:
        return {
            "msgtype": "text",
            "text": {"content": format_task_result_message(result)},
        }

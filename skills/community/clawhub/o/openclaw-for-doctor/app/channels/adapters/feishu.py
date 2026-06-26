from app.channels.base import WebhookChannelAdapter
from app.channels.formatter import format_task_result_message
from app.core.models import ChannelType, TaskResult


class FeishuAdapter(WebhookChannelAdapter):
    channel = ChannelType.feishu
    webhook_env_key = "FEISHU_WEBHOOK_URL"

    def build_payload(self, result: TaskResult) -> dict:
        return {
            "msg_type": "text",
            "content": {"text": format_task_result_message(result)},
        }

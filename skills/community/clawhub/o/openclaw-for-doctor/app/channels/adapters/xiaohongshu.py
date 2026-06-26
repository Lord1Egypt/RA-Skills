from app.channels.base import WebhookChannelAdapter
from app.channels.formatter import format_task_result_message
from app.core.models import ChannelType, TaskResult


class XiaoHongShuAdapter(WebhookChannelAdapter):
    channel = ChannelType.xiaohongshu
    webhook_env_key = "XIAOHONGSHU_WEBHOOK_URL"

    def build_payload(self, result: TaskResult) -> dict:
        return {
            "title": f"Doctor Assistant Result {result.task_id[:8]}",
            "content": format_task_result_message(result),
            "tags": ["openclaw", "doctor-assistant"],
        }

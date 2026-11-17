"""
推送给研究室负责人
读取 config/reviewers.json，生成待办消息，预留美信发送接口
"""
import json
from pathlib import Path
from datetime import datetime


REVIEWERS_PATH = Path(__file__).parent.parent / "config" / "reviewers.json"


def get_reviewer(research_room: str) -> dict:
    """获取研究室负责人信息"""
    with open(REVIEWERS_PATH, "r", encoding="utf-8") as f:
        reviewers = json.load(f)
    return reviewers.get(research_room, {"reviewer": "待配置", "mx_id": ""})


def format_notification(entity_id: str, title: str, direction: str, research_room: str) -> str:
    """格式化待办通知消息"""
    reviewer = get_reviewer(research_room)
    
    message = f"""📋 新知识待审核

标题: {title}
ID: {entity_id}
方向: {direction}
研究室: {research_room}
提交时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

请审核该知识条目。
如需修改，请直接编辑知识库中对应 ID 的记录。
"""
    return message


def send_notification(entity_id: str, title: str, direction: str, research_room: str) -> dict:
    """
    发送通知（预留美信发送接口）
    
    Returns:
        {"status": "sent"|"pending", "reviewer": str, "message": str}
    """
    reviewer = get_reviewer(research_room)
    message = format_notification(entity_id, title, direction, research_room)
    
    # 预留美信发送接口
    # TODO: 接入美信 API 发送待办
    # mx_send_todo(reviewer["mx_id"], message)
    
    print(f"[通知] 发送给 {reviewer['reviewer']} ({reviewer['mx_id']})")
    print(message)
    
    return {
        "status": "pending",  # pending = 接口未实现
        "reviewer": reviewer["reviewer"],
        "mx_id": reviewer["mx_id"],
        "message": message
    }


def direction_to_room(direction: str) -> str:
    """方向 → 研究室映射"""
    mapping = {
        "非标自动化": "机电系统研究室",
        "物流自动化": "物流自动化研究室",
        "工业视觉": "工业视觉研究室"
    }
    return mapping.get(direction, "机电系统研究室")


if __name__ == "__main__":
    # 测试
    result = send_notification(
        entity_id="test_123",
        title="AM600 EtherCAT 调试经验",
        direction="非标自动化",
        research_room="机电系统研究室"
    )
    print(f"\n发送结果: {result['status']}")

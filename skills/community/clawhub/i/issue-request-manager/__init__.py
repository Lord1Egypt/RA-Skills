"""
Issue Request Manager Package
Issue Request管理技能的主入口文件
"""

from .ir_creator import IRCreator
from .ir_tracker import IRTracker
from .ir_responder import IRResponder
from .ir_database import IRDatabase
from .wechat_notifier import WeChatNotifier

__all__ = ['IRCreator', 'IRTracker', 'IRResponder', 'IRDatabase', 'WeChatNotifier']

# 初始化全局实例
creator = IRCreator()
tracker = IRTracker()
responder = IRResponder()
database = IRDatabase()

def get_ir_manager():
    """获取Issue Request管理器实例"""
    return {
        'creator': creator,
        'tracker': tracker,
        'responder': responder,
        'database': database
    }

def create_issue(title: str, description: str = "", 
                issue_type: str = "task", priority: str = "medium",
                assignee: str = None, labels: list = None):
    """创建Issue Request的便捷函数"""
    return creator.create_issue(title, description, issue_type, priority, assignee, labels)

def track_issue(issue_id: str):
    """跟踪Issue Request的便捷函数"""
    return tracker.track_issue(issue_id)

def reply_to_issue(issue_id: str, content: str, author: str = "user"):
    """回复Issue Request的便捷函数"""
    return responder.reply_to_issue(issue_id, content, author)

def assign_issue(issue_id: str, assignee: str):
    """分配Issue Request的便捷函数"""
    return responder.assign_issue(issue_id, assignee)

def set_priority(issue_id: str, priority: str):
    """设置Issue Request优先级的便捷函数"""
    return responder.set_priority(issue_id, priority)

def close_issue(issue_id: str, closing_comment: str = ""):
    """关闭Issue Request的便捷函数"""
    return responder.close_issue(issue_id, closing_comment)

# 微信通知相关函数
def init_wechat_notifier(corp_id: str = None, secret: str = None, agent_id: int = None):
    """初始化微信通知器"""
    return WeChatNotifier(corp_id, secret, agent_id)

def notify_new_issue(notifier: WeChatNotifier, issue: dict, recipients: list):
    """通知新创建的Issue"""
    return notifier.notify_new_issue(issue, recipients)

def notify_issue_update(notifier: WeChatNotifier, issue: dict, 
                       update_type: str, recipients: list):
    """通知Issue更新"""
    return notifier.notify_issue_update(issue, update_type, recipients)

def notify_issue_closed(notifier: WeChatNotifier, issue: dict, recipients: list):
    """通知Issue关闭"""
    return notifier.notify_issue_closed(issue, recipients)
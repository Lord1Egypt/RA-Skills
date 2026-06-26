#!/usr/bin/env python3
"""
Token 使用监控脚本
自动检测 Token 使用情况并触发优化建议
"""

import json
import sys
from typing import Dict, Any, Optional

class TokenMonitor:
    """监控 Token 使用情况"""
    
    # 阈值配置
    THRESHOLDS = {
        "warning": 0.7,      # 70% 警告
        "critical": 0.8,     # 80% 严重
        "emergency": 0.9,    # 90% 紧急
        "per_turn_max": 4000, # 单次最大
        "session_max": 50000  # 会话最大
    }
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.thresholds = {**self.THRESHOLDS, **self.config.get('thresholds', {})}
    
    def check_usage(self, current: int, max_tokens: int, context: Dict = None) -> Dict[str, Any]:
        """检查 Token 使用情况"""
        usage_ratio = current / max_tokens if max_tokens > 0 else 0
        
        result = {
            "status": "normal",
            "usage_ratio": usage_ratio,
            "current": current,
            "max": max_tokens,
            "actions": [],
            "message": ""
        }
        
        # 判断状态
        if usage_ratio >= self.thresholds["emergency"]:
            result["status"] = "emergency"
            result["actions"] = ["compact", "reset", "nc_mode"]
            result["message"] = f"🚨 Token 使用紧急！{current}/{max_tokens} ({usage_ratio:.1%})"
        elif usage_ratio >= self.thresholds["critical"]:
            result["status"] = "critical"
            result["actions"] = ["compact", "cc_mode"]
            result["message"] = f"⚠️ Token 使用过高！{current}/{max_tokens} ({usage_ratio:.1%})"
        elif usage_ratio >= self.thresholds["warning"]:
            result["status"] = "warning"
            result["actions"] = ["suggest_compact"]
            result["message"] = f"💡 Token 使用偏高 {current}/{max_tokens} ({usage_ratio:.1%})"
        
        return result
    
    def get_recommendations(self, status: str) -> list:
        """根据状态获取建议"""
        recommendations = {
            "emergency": [
                "立即执行 /compact 压缩上下文",
                "切换到 /nc 模式（仅当前消息）",
                "考虑 /reset 重置会话",
                "检查并禁用不必要的 tools"
            ],
            "critical": [
                "建议执行 /compact",
                "使用 /cc 模式（最近10条）",
                "限制工具返回长度",
                "设置 max_history_messages: 5"
            ],
            "warning": [
                "关注 Token 使用情况",
                "准备执行 /compact",
                "考虑减少上下文保留"
            ]
        }
        return recommendations.get(status, ["Token 使用正常"])
    
    def generate_report(self, stats: Dict) -> str:
        """生成 Token 使用报告"""
        report = f"""
╔════════════════════════════════════════════════════════════╗
║           📊 Token 使用报告                                ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  当前使用: {stats['current']:,} / {stats['max']:,} tokens          ║
║  使用率: {stats['usage_ratio']:.1%}                                    ║
║  状态: {stats['status'].upper()}                                          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

建议操作:
"""
        for i, action in enumerate(self.get_recommendations(stats['status']), 1):
            report += f"{i}. {action}\n"
        
        return report

def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: token-monitor.py <current_tokens> <max_tokens>")
        sys.exit(1)
    
    current = int(sys.argv[1])
    max_tokens = int(sys.argv[2])
    
    monitor = TokenMonitor()
    result = monitor.check_usage(current, max_tokens)
    
    print(monitor.generate_report(result))
    
    # 返回状态码
    if result['status'] == 'emergency':
        sys.exit(2)
    elif result['status'] == 'critical':
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()

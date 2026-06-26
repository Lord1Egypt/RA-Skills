"""
承诺追踪模块 (义-Yi)
君子一诺，一诺千金

功能：
1. 承诺自动识别与注册
2. 截止日期追踪
3. 提醒生成
4. 履约记录
5. 信任度计算
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict
from dateutil import parser as date_parser

class PromiseTracker:
    """
    承诺追踪器
    
    中国人最重承诺。这个模块确保每一个承诺都被追踪，
    不遗漏、不忘记。
    
    状态流转：
    pending -> fulfilled (完成)
              -> overdue (逾期，待解释)
              -> cancelled (取消/放弃)
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            data_dir = Path.home() / ".mflow-memory-cn" / "promises"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.promises_file = self.data_dir / "promises.jsonl"
        self.stats_file = self.data_dir / "stats.json"
        
        # 加载统计数据
        self.stats = self._load_stats()
    
    def register(self, content: str, deadline: Optional[str] = None,
                 context: Optional[str] = None) -> str:
        """
        注册一个新承诺
        
        Args:
            content: 承诺内容
            deadline: 截止时间（可为空，之后提醒追问）
            context: 上下文
            
        Returns:
            promise_id: 承诺ID
        """
        promise = {
            "id": self._generate_id(),
            "content": content,
            "deadline": deadline,
            "deadline_parsed": self._parse_deadline(deadline) if deadline else None,
            "context": context,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "reminders_sent": 0,
            "fulfillment_note": None
        }
        
        self._append_to_file(self.promises_file, promise)
        self.stats["total_promises"] += 1
        self._save_stats()
        
        return promise["id"]
    
    def get_pending(self) -> List[Dict]:
        """获取所有待履行的承诺"""
        return self._load_promises_by_status("pending")
    
    def get_overdue(self) -> List[Dict]:
        """获取所有逾期的承诺"""
        overdue = []
        for p in self._load_promises_by_status("pending"):
            if self._is_overdue(p):
                overdue.append(p)
        return overdue
    
    def get_near_deadline(self, hours: int = 24) -> List[Dict]:
        """获取临近截止的承诺（24小时内）"""
        near = []
        now = datetime.now()
        threshold = now + timedelta(hours=hours)
        
        for p in self._load_promises_by_status("pending"):
            dp = p.get("deadline_parsed")
            if dp:
                if now <= dp <= threshold:
                    near.append(p)
        return near
    
    def fulfill(self, promise_id: str, note: Optional[str] = None):
        """
        标记承诺已履行
        
        Args:
            promise_id: 承诺ID
            note: 备注（如"提前完成"、"按时完成"）
        """
        promises = self._load_all_promises()
        
        for p in promises:
            if p["id"] == promise_id:
                p["status"] = "fulfilled"
                p["fulfilled_at"] = datetime.now().isoformat()
                p["fulfillment_note"] = note
                p["updated_at"] = datetime.now().isoformat()
                break
        
        self._save_all_promises(promises)
        self.stats["fulfilled_promises"] += 1
        self._save_stats()
    
    def overdue(self, promise_id: str, explanation: Optional[str] = None):
        """标记承诺逾期"""
        promises = self._load_all_promises()
        
        for p in promises:
            if p["id"] == promise_id:
                p["status"] = "overdue"
                p["explanation"] = explanation
                p["updated_at"] = datetime.now().isoformat()
                break
        
        self._save_all_promises(promises)
        self.stats["overdue_promises"] += 1
        self._save_stats()
    
    def cancel(self, promise_id: str, reason: str):
        """取消承诺"""
        promises = self._load_all_promises()
        
        for p in promises:
            if p["id"] == promise_id:
                p["status"] = "cancelled"
                p["cancel_reason"] = reason
                p["updated_at"] = datetime.now().isoformat()
                break
        
        self._save_all_promises(promises)
        self.stats["cancelled_promises"] += 1
        self._save_stats()
    
    def get_stats(self) -> Dict:
        """获取承诺统计"""
        self._recalculate_stats()
        return self.stats
    
    def get_trust_score(self) -> float:
        """
        计算信任度分数
        
        公式：
        trust_score = fulfilled / total * 100%
        """
        total = self.stats["total_promises"]
        if total == 0:
            return 100.0  # 没有记录，默认满分
        
        fulfilled = self.stats["fulfilled_promises"]
        cancelled = self.stats["cancelled_promises"]
        
        # 有效承诺 = 总承诺 - 取消
        valid = total - cancelled
        if valid == 0:
            return 100.0
        
        return (fulfilled / valid) * 100
    
    def generate_reminder(self, promise: Dict) -> str:
        """生成提醒文本"""
        deadline = promise.get("deadline", "未定")
        content = promise.get("content", "")
        
        if self._is_overdue(promise):
            return f"【逾期提醒】您曾承诺：{content}（截止：{deadline}）。需要说明情况吗？"
        else:
            return f"【承诺提醒】您承诺：{content}（截止：{deadline}）。请记得履行。"
    
    def should_remind(self) -> bool:
        """
        判断是否应该发送提醒
        
        规则：
        1. 有逾期的承诺
        2. 有24小时内到期的承诺
        """
        overdue = self.get_overdue()
        near = self.get_near_deadline(24)
        
        return len(overdue) > 0 or len(near) > 0
    
    def get_reminders(self) -> List[str]:
        """获取所有待发送的提醒"""
        reminders = []
        
        for p in self.get_overdue():
            reminders.append(self.generate_reminder(p))
        
        for p in self.get_near_deadline(24):
            reminders.append(self.generate_reminder(p))
        
        return reminders
    
    # ========== 私有方法 ==========
    
    def _is_overdue(self, promise: Dict) -> bool:
        """判断是否逾期"""
        dp = promise.get("deadline_parsed")
        if dp is None:
            return False
        return datetime.now() > dp
    
    def _parse_deadline(self, deadline: str) -> Optional[datetime]:
        """解析截止时间"""
        if not deadline:
            return None
        
        # 自然语言处理
        now = datetime.now()
        
        if "明天" in deadline:
            return now + timedelta(days=1)
        elif "后天" in deadline:
            return now + timedelta(days=2)
        elif "周末" in deadline:
            # 计算到本周末
            days_until_saturday = (5 - now.weekday()) % 7
            if days_until_saturday == 0:
                days_until_saturday = 7
            return now + timedelta(days=days_until_saturday)
        elif "下周" in deadline:
            return now + timedelta(days=7)
        
        # 尝试解析日期格式
        try:
            return date_parser.parse(deadline)
        except:
            return None
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        import uuid
        return f"prm_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
    
    def _append_to_file(self, filepath: Path, data: Dict):
        """追加到JSONL文件"""
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    def _load_promises_by_status(self, status: str) -> List[Dict]:
        """按状态加载承诺"""
        if not self.promises_file.exists():
            return []
        
        promises = []
        with open(self.promises_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    p = json.loads(line)
                    if p.get("status") == status:
                        promises.append(p)
                except json.JSONDecodeError:
                    continue
        return promises
    
    def _load_all_promises(self) -> List[Dict]:
        """加载所有承诺"""
        if not self.promises_file.exists():
            return []
        
        promises = []
        with open(self.promises_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    promises.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return promises
    
    def _save_all_promises(self, promises: List[Dict]):
        """保存所有承诺（覆盖）"""
        with open(self.promises_file, 'w', encoding='utf-8') as f:
            for p in promises:
                f.write(json.dumps(p, ensure_ascii=False) + '\n')
    
    def _load_stats(self) -> Dict:
        """加载统计"""
        if self.stats_file.exists():
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "total_promises": 0,
            "fulfilled_promises": 0,
            "overdue_promises": 0,
            "cancelled_promises": 0
        }
    
    def _save_stats(self):
        """保存统计"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
    
    def _recalculate_stats(self):
        """重新计算统计"""
        promises = self._load_all_promises()
        
        self.stats = {
            "total_promises": len(promises),
            "fulfilled_promises": sum(1 for p in promises if p.get("status") == "fulfilled"),
            "overdue_promises": sum(1 for p in promises if p.get("status") == "overdue"),
            "cancelled_promises": sum(1 for p in promises if p.get("status") == "cancelled")
        }
        self._save_stats()

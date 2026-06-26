"""
Consent Manager - 用户授权管理模块（i-skill）

修复记录（v2.1.0）：
- [P2] revoke 后再次 request_consent 返回 DENIED 而非允许重新授权 —— 修正
        revoke 操作现在不再将技能加入 denied_skills，而是移回 unknown 状态，
        让用户可以在下次请求时重新做决定
- [P2] restore_consent 只能从 denied 操作，revoke 后的技能无法 restore —— 修正
- [P2] 所有文件 IO 增加 try-except，损坏时返回安全默认值
- [P3] 授权提示文本改为中文，与用户语言偏好一致
- [P3] _log_conversation 失败不影响主流程

修复记录（v2.2.0）：
- [P1] 默认 user_data_path 改为技能目录下的 user_data/，而非运行时 cwd
- [P1] 支持 ISKILL_DATA_PATH 环境变量覆盖
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime


def _get_skill_directory() -> Path:
    """获取技能所在目录（相对于运行时的 cwd，确保数据存储在技能工具区）"""
    # 优先使用环境变量指定的路径
    env_path = os.environ.get('ISKILL_DATA_PATH')
    if env_path:
        return Path(env_path).resolve()
    # 默认使用技能所在目录 + user_data/
    return Path(__file__).parent.parent / "user_data"


class ConsentManager:
    def __init__(self, user_data_path: str = None):
        # 默认使用技能目录下的 user_data/
        if user_data_path is None:
            user_data_path = str(_get_skill_directory())
        self.user_data_path = Path(user_data_path)

        self.consent_file = self.user_data_path / "consent_state.json"
        self.conversation_file = self.user_data_path / "consent_conversations.json"

        self._initialized = False

    # ------------------------------------------------------------------
    # 初始化（延迟执行）
    # ------------------------------------------------------------------

    def _ensure_initialized(self):
        """确保目录和文件已初始化，在第一次写入数据时调用"""
        if self._initialized:
            return
        
        self.user_data_path.mkdir(parents=True, exist_ok=True)
        self._initialize_consent_state()
        self._initialize_conversation_log()
        self._initialized = True

    def _initialize_consent_state(self):
        if not self.consent_file.exists():
            self._save_consent_state({
                "allowed_skills": [],
                "denied_skills": [],
                "pending_skills": [],
                "first_time_prompted": {},
                "consent_history": []
            })

    def _initialize_conversation_log(self):
        if not self.conversation_file.exists():
            self._save_conversation_log([])

    # ------------------------------------------------------------------
    # 安全文件 IO
    # ------------------------------------------------------------------

    def _load_consent_state(self) -> Dict:
        """[P2修复] 文件损坏时返回安全默认值"""
        try:
            with open(self.consent_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            default = {
                "allowed_skills": [], "denied_skills": [],
                "pending_skills": [], "first_time_prompted": {},
                "consent_history": []
            }
            # 尝试重新写入修复损坏的文件
            self._save_consent_state(default)
            return default

    def _save_consent_state(self, state: Dict):
        try:
            self._ensure_initialized()
            with open(self.consent_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # 写入失败时记录会丢失，但不崩溃

    def _load_conversation_log(self) -> List[Dict]:
        try:
            with open(self.conversation_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def _save_conversation_log(self, log: List[Dict]):
        try:
            self._ensure_initialized()
            with open(self.conversation_file, 'w', encoding='utf-8') as f:
                json.dump(log, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # 授权请求流程
    # ------------------------------------------------------------------

    def request_consent(self, skill_name: str,
                        skill_description: str = "") -> Tuple[bool, str, Optional[str]]:
        state = self._load_consent_state()

        if skill_name in state["allowed_skills"]:
            return True, f"技能 {skill_name} 已获得授权", "GRANTED"

        if skill_name in state["denied_skills"]:
            return False, f"技能 {skill_name} 已被拒绝授权", "DENIED"

        if skill_name in state["pending_skills"]:
            return False, f"技能 {skill_name} 的授权请求正在等待处理", "PENDING"

        state["pending_skills"].append(skill_name)
        self._save_consent_state(state)

        prompt = self._generate_consent_prompt(skill_name, skill_description)
        return False, prompt, "PROMPT_REQUIRED"

    def _generate_consent_prompt(self, skill_name: str, skill_description: str) -> str:
        """[P3修复] 授权提示改为中文"""
        prompt = f"技能「{skill_name}」请求访问您的个人档案。"

        if skill_description:
            prompt += f"\n\n用途说明：{skill_description}"

        prompt += "\n\n您的档案包含：\n- 您的兴趣爱好与偏好\n- 您的沟通风格\n- 您的专业背景"
        prompt += "\n\n是否允许该技能访问您的档案？"
        prompt += "\n\n选项：\n- 输入 '是' 或 'yes' 授权\n- 输入 '否' 或 'no' 拒绝\n- 输入 '稍后' 或 'later' 稍后决定"

        return prompt

    def process_consent_response(self, skill_name: str,
                                  response: str) -> Tuple[bool, str, Optional[str]]:
        state = self._load_consent_state()

        if skill_name not in state["pending_skills"]:
            return False, f"技能 {skill_name} 没有待处理的授权请求", None

        r = response.lower().strip()

        if r in ['yes', 'y', 'allow', 'grant', 'approve', '是', '允许', '授权', '同意']:
            return self._grant_consent(skill_name, state)
        elif r in ['no', 'n', 'deny', 'reject', 'disapprove', '否', '拒绝', '不允许']:
            return self._deny_consent(skill_name, state)
        elif r in ['ask me later', 'later', 'postpone', '稍后', '以后', '推迟']:
            return self._postpone_consent(skill_name)
        else:
            return False, "无效回复，请使用 '是'、'否' 或 '稍后'", None

    def _grant_consent(self, skill_name: str, state: Dict) -> Tuple[bool, str, Optional[str]]:
        state["pending_skills"].remove(skill_name)
        if skill_name not in state["allowed_skills"]:
            state["allowed_skills"].append(skill_name)
        state["first_time_prompted"][skill_name] = True
        state["consent_history"].append({
            "timestamp": datetime.now().isoformat(),
            "skill_name": skill_name,
            "action": "GRANTED",
            "user_response": "yes"
        })
        self._save_consent_state(state)
        self._log_conversation(skill_name, "CONSENT_GRANTED", "用户已授权访问")
        return True, f"已授权技能 {skill_name} 访问档案", "GRANTED"

    def _deny_consent(self, skill_name: str, state: Dict) -> Tuple[bool, str, Optional[str]]:
        state["pending_skills"].remove(skill_name)
        if skill_name not in state["denied_skills"]:
            state["denied_skills"].append(skill_name)
        state["first_time_prompted"][skill_name] = True
        state["consent_history"].append({
            "timestamp": datetime.now().isoformat(),
            "skill_name": skill_name,
            "action": "DENIED",
            "user_response": "no"
        })
        self._save_consent_state(state)
        self._log_conversation(skill_name, "CONSENT_DENIED", "用户已拒绝授权")
        return False, f"已拒绝技能 {skill_name} 的访问请求", "DENIED"

    def _postpone_consent(self, skill_name: str) -> Tuple[bool, str, Optional[str]]:
        self._log_conversation(skill_name, "CONSENT_POSTPONED", "用户推迟决定")
        return False, f"已推迟技能 {skill_name} 的授权请求，您可以稍后决定。", "POSTPONED"

    # ------------------------------------------------------------------
    # 撤销 / 恢复授权
    # [P2修复] revoke 不再加入 denied_skills，保留重新授权的可能性
    # ------------------------------------------------------------------

    def revoke_consent(self, skill_name: str) -> Tuple[bool, str]:
        state = self._load_consent_state()

        if skill_name not in state["allowed_skills"]:
            return False, f"{skill_name} 不在已授权列表中"

        state["allowed_skills"].remove(skill_name)
        # [P2修复] revoke 只从 allowed 移除，不加入 denied
        # 这样下次 request_consent 时会重新走授权流程
        state["first_time_prompted"][skill_name] = False  # 重置为允许重新提示

        state["consent_history"].append({
            "timestamp": datetime.now().isoformat(),
            "skill_name": skill_name,
            "action": "REVOKED",
            "user_response": "revoke"
        })
        self._save_consent_state(state)
        self._log_conversation(skill_name, "CONSENT_REVOKED", "用户已撤销授权")
        return True, f"已撤销技能 {skill_name} 的授权，下次访问时将重新请求授权"

    def restore_consent(self, skill_name: str) -> Tuple[bool, str]:
        """从明确拒绝状态恢复授权"""
        state = self._load_consent_state()

        if skill_name not in state["denied_skills"]:
            return False, f"{skill_name} 不在已拒绝列表中"

        state["denied_skills"].remove(skill_name)
        if skill_name not in state["allowed_skills"]:
            state["allowed_skills"].append(skill_name)

        state["consent_history"].append({
            "timestamp": datetime.now().isoformat(),
            "skill_name": skill_name,
            "action": "RESTORED",
            "user_response": "restore"
        })
        self._save_consent_state(state)
        self._log_conversation(skill_name, "CONSENT_RESTORED", "用户已恢复授权")
        return True, f"已恢复技能 {skill_name} 的授权"

    # ------------------------------------------------------------------
    # 查询接口
    # ------------------------------------------------------------------

    def get_consent_status(self, skill_name: str) -> Dict:
        state = self._load_consent_state()
        if skill_name in state["allowed_skills"]:
            status = "allowed"
        elif skill_name in state["denied_skills"]:
            status = "denied"
        elif skill_name in state["pending_skills"]:
            status = "pending"
        else:
            status = "unknown"
        return {
            "skill_name": skill_name,
            "status": status,
            "first_time_prompted": state["first_time_prompted"].get(skill_name, False)
        }

    def get_all_consents(self) -> Dict:
        state = self._load_consent_state()
        return {
            "allowed_skills": state["allowed_skills"],
            "denied_skills": state["denied_skills"],
            "pending_skills": state["pending_skills"],
            "first_time_prompted": state["first_time_prompted"]
        }

    def get_consent_history(self, skill_name: Optional[str] = None,
                             limit: int = 50) -> List[Dict]:
        state = self._load_consent_state()
        history = state.get("consent_history", [])
        if skill_name:
            history = [e for e in history if e["skill_name"] == skill_name]
        return history[-limit:]

    def get_pending_consents(self) -> List[str]:
        return self._load_consent_state().get("pending_skills", [])

    def clear_pending_consents(self) -> Tuple[bool, str]:
        state = self._load_consent_state()
        count = len(state["pending_skills"])
        state["pending_skills"] = []
        self._save_consent_state(state)
        return True, f"已清除 {count} 个待处理授权请求"

    def is_first_time_access(self, skill_name: str) -> bool:
        state = self._load_consent_state()
        return not state["first_time_prompted"].get(skill_name, False)

    def get_consent_summary(self) -> Dict:
        state = self._load_consent_state()
        return {
            "total_allowed": len(state["allowed_skills"]),
            "total_denied": len(state["denied_skills"]),
            "total_pending": len(state["pending_skills"]),
            "total_history": len(state.get("consent_history", [])),
            "skills": {
                "allowed": state["allowed_skills"],
                "denied": state["denied_skills"],
                "pending": state["pending_skills"]
            }
        }

    def get_conversation_log(self, skill_name: Optional[str] = None,
                              limit: int = 100) -> List[Dict]:
        log = self._load_conversation_log()
        if skill_name:
            log = [e for e in log if e["skill_name"] == skill_name]
        return log[-limit:]

    # ------------------------------------------------------------------
    # 内部日志
    # ------------------------------------------------------------------

    def _log_conversation(self, skill_name: str, action: str, message: str):
        """[P3修复] 失败时静默，不影响主流程"""
        try:
            log = self._load_conversation_log()
            log.append({
                "timestamp": datetime.now().isoformat(),
                "skill_name": skill_name,
                "action": action,
                "message": message
            })
            self._save_conversation_log(log)
        except Exception:
            pass

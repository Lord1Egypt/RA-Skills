"""
MeetMind Skill 云客户端 v0.6.1
- 自动获取 WorkBuddy 用户 ID（环境变量 WORKBUDDY_USER_ID）
- mTLS 客户端证书认证（付费用户）
- 免费试用模式（无需证书，10次终身）
- 自定义模板 CRUD（L4 企业版）
证书文件位于 certs/ 目录，不在代码中暴露任何密钥。
"""
import os
import json
import uuid
import httpx
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger("meetmind.cloud_client")

# API 地址
API_BASE = os.getenv("MEETMIND_API_BASE", "https://www.hermesai.ltd/meetmind")
TRIAL_API_BASE = os.getenv("MEETMIND_TRIAL_API_BASE", "https://www.hermesai.ltd/meetmind")
TIMEOUT_SEC = int(os.getenv("MEETMIND_API_TIMEOUT", "120"))

# 客户端证书路径（不在代码中硬编码密钥）
SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CERT = (
    str(SKILL_DIR / "certs" / "client.crt"),
    str(SKILL_DIR / "certs" / "client.key"),
)


def _get_wb_user_id() -> str:
    """
    自动获取 WorkBuddy 用户 ID
    优先级：WORKBUDDY_USER_ID > MEETMIND_USER_ID > 本地持久化 ID > UUID
    """
    # 1. WorkBuddy 上下文透传（最高优先级）
    wb_uid = os.getenv("WORKBUDDY_USER_ID")
    if wb_uid:
        return wb_uid.strip()

    # 2. 手动配置的 MeetMind 用户 ID
    mm_uid = os.getenv("MEETMIND_USER_ID")
    if mm_uid:
        return mm_uid.strip()

    # 3. 本地持久化 ID（跨 Skill 调用保持一致）
    local_id_file = SKILL_DIR / ".meetmind_user_id"
    if local_id_file.exists():
        return local_id_file.read_text().strip()

    # 4. 首次生成并持久化
    new_id = f"meetmind_{uuid.uuid4().hex[:12]}"
    local_id_file.write_text(new_id)
    logger.info(f"首次生成本地用户 ID: {new_id}")
    return new_id


class MeetMindClient:
    """MeetMind 云端 API 客户端 v0.6.1"""

    def __init__(self, base_url: str = None, user_id: str = None, cert: tuple = None):
        self.base_url = (base_url or API_BASE).rstrip("/")
        self.user_id = user_id or _get_wb_user_id()
        self._cert = cert or DEFAULT_CERT
        self._has_cert = os.path.exists(self._cert[0]) and os.path.exists(self._cert[1])

        if not self._has_cert:
            logger.info("客户端证书未找到，将使用试用模式（10次免费）")

        # 公共请求头（WB 用户身份透传）
        self._common_headers = {
            "X-WorkBuddy-User-ID": self.user_id,
        }

        # mTLS 客户端（付费用户）
        if self._has_cert:
            self._client = httpx.Client(
                timeout=TIMEOUT_SEC,
                cert=self._cert,
                verify=True,
                headers=self._common_headers,
            )
        else:
            self._client = httpx.Client(timeout=TIMEOUT_SEC, verify=True, headers=self._common_headers)

        # 试用客户端（永远不用 mTLS）
        self._trial_client = httpx.Client(timeout=TIMEOUT_SEC, verify=True, headers=self._common_headers)

        logger.info(f"MeetMindClient 初始化: user_id={self.user_id[:20]}..., has_cert={self._has_cert}")

    # ---- 🔓 试用（无需 mTLS）----
    def trial_structure(
        self,
        text: str,
        template_id: str = None,
        meeting_title: str = None,
    ) -> dict:
        """免费试用 — 调用 /trial 端点，无需证书，10次终身。
        用户身份通过 X-WorkBuddy-User-ID header 自动透传。"""
        data = {"text": text}
        if template_id:
            data["template_id"] = template_id
        if meeting_title:
            data["meeting_title"] = meeting_title

        r = self._trial_client.post(
            f"{self.base_url}/trial",
            data=data
        )
        if r.status_code == 429:
            raise RuntimeError(
                "免费试用已用完（10次终身）。"
                "升级到个人版 ¥19.9/月：联系客服获取客户端证书。"
            )
        r.raise_for_status()
        return r.json()

    def get_trial_usage(self) -> dict:
        """查询试用剩余次数"""
        r = self._trial_client.get(
            f"{self.base_url}/user/{self.user_id}/usage"
        )
        r.raise_for_status()
        data = r.json()
        return {
            "trial_uses_left": data.get("trial_uses_left", 0),
            "tier": data.get("tier", "free"),
        }

    # ---- 健康检查 ----
    def health(self) -> dict:
        r = self._client.get(f"{self.base_url}/health")
        r.raise_for_status()
        return r.json()

    # ---- 转录 ----
    def transcribe_text(self, text: str) -> dict:
        """粘贴文字 → 直接透传"""
        r = self._client.post(
            f"{self.base_url}/transcribe",
            data={"user_id": self.user_id, "text": text}
        )
        r.raise_for_status()
        return r.json()

    def transcribe_audio(self, audio_path: str) -> dict:
        """上传音频 → 腾讯云 ASR 转录"""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")

        with open(audio_path, "rb") as f:
            r = self._client.post(
                f"{self.base_url}/transcribe",
                data={"user_id": self.user_id},
                files={"file": (os.path.basename(audio_path), f)}
            )
        r.raise_for_status()
        return r.json()

    def get_transcription(self, task_id: str) -> dict:
        r = self._client.get(f"{self.base_url}/transcribe/{task_id}")
        r.raise_for_status()
        return r.json()

    # ---- 结构化 ----
    def structure(
        self,
        transcription_id: str,
        template_id: str = None,
        meeting_title: str = None,
        participants: list = None,
        entity_key: str = None,
        entity_type: str = None
    ) -> dict:
        """对转录结果进行 ACE 结构化"""
        data = {
            "user_id": self.user_id,
            "transcription_id": transcription_id,
        }
        if template_id:
            data["template_id"] = template_id
        if meeting_title:
            data["meeting_title"] = meeting_title
        if participants:
            data["participants"] = ",".join(participants)
        if entity_key:
            data["entity_key"] = entity_key
        if entity_type:
            data["entity_type"] = entity_type

        r = self._client.post(f"{self.base_url}/structure", data=data)
        r.raise_for_status()
        return r.json()

    def get_structure(self, task_id: str) -> dict:
        r = self._client.get(f"{self.base_url}/structure/{task_id}")
        r.raise_for_status()
        return r.json()

    # ---- 跨会议记忆 ----
    def get_memory_context(self, entity_key: str, entity_type: str = None) -> dict:
        params = {"user_id": self.user_id, "entity_key": entity_key}
        if entity_type:
            params["entity_type"] = entity_type
        r = self._client.get(f"{self.base_url}/memory/context", params=params)
        r.raise_for_status()
        return r.json()

    def recall_memories(self, entity_key: str = None, entity_type: str = None, limit: int = 5) -> dict:
        data = {"user_id": self.user_id}
        if entity_key:
            data["entity_key"] = entity_key
        if entity_type:
            data["entity_type"] = entity_type
        data["limit"] = str(limit)
        r = self._client.post(f"{self.base_url}/memory/recall", data=data)
        r.raise_for_status()
        return r.json()

    # ---- 用户 ----
    def get_user(self) -> dict:
        r = self._client.get(f"{self.base_url}/user/{self.user_id}")
        r.raise_for_status()
        return r.json()

    def get_usage(self) -> dict:
        r = self._client.get(f"{self.base_url}/user/{self.user_id}/usage")
        r.raise_for_status()
        return r.json()

    # ---- 模板 ----
    def list_templates(self) -> list:
        """列出所有模板（内置 + 自定义）"""
        r = self._client.get(f"{self.base_url}/templates", params={"user_id": self.user_id})
        r.raise_for_status()
        return r.json()["templates"]

    def get_template(self, template_id: str) -> dict:
        """获取模板详情"""
        r = self._client.get(
            f"{self.base_url}/templates/{template_id}",
            params={"user_id": self.user_id}
        )
        r.raise_for_status()
        return r.json()

    # ---- 自定义模板 CRUD（L4 企业版）----
    def create_template(
        self,
        name: str,
        keywords: list,
        ace_weights: dict,
        prompt_instruction: str,
        description: str = "",
        custom_blocks: list = None,
    ) -> dict:
        """创建自定义模板 — L4 企业版"""
        data = {
            "user_id": self.user_id,
            "name": name,
            "keywords": json.dumps(keywords, ensure_ascii=False),
            "ace_weights": json.dumps(ace_weights),
            "prompt_instruction": prompt_instruction,
            "description": description,
            "custom_blocks": json.dumps(custom_blocks or [], ensure_ascii=False),
        }
        r = self._client.post(f"{self.base_url}/templates", json=data)
        r.raise_for_status()
        return r.json()

    def update_template(self, template_id: str, **kwargs) -> dict:
        """更新自定义模板"""
        data = {"user_id": self.user_id}
        for k, v in kwargs.items():
            if v is not None:
                if k in ("keywords", "custom_blocks"):
                    data[k] = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
                elif k == "ace_weights":
                    data[k] = json.dumps(v) if not isinstance(v, str) else v
                else:
                    data[k] = v

        r = self._client.put(f"{self.base_url}/templates/{template_id}", json=data)
        r.raise_for_status()
        return r.json()

    def delete_template(self, template_id: str) -> dict:
        """删除自定义模板"""
        r = self._client.delete(
            f"{self.base_url}/templates/{template_id}",
            params={"user_id": self.user_id}
        )
        r.raise_for_status()
        return r.json()

    # ---- 激活/升级 ----
    def activate(self) -> dict:
        """验证证书是否有效并返回用户信息"""
        try:
            user = self.get_user()
            usage = self.get_usage()
            return {
                "status": "activated",
                "user_id": user["user_id"],
                "tier": user["tier"],
                "usage": usage,
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "hint": "请确认 certs/client.crt 和 certs/client.key 已正确放置"
            }


def quick_test():
    """本地快速测试"""
    client = MeetMindClient()

    # 先试试用
    print("🔓 测试试用模式...")
    try:
        text = "我们今天讨论了Q3季度产品方向，决定优先做AI推荐功能，张三负责5月30号前出原型，李四负责竞品分析"
        result = client.trial_structure(text)
        print(f"   ✅ 试用成功: {result['template_name']}")
        print(f"   剩余次数: {result['trial_uses_left']}")
        print(f"   模板: {result['template_id']}")
    except Exception as e:
        print(f"   ❌ 试用失败: {e}")

    # 如果有证书，测试付费模式
    if client._has_cert:
        print("\n🔒 测试付费模式...")
        try:
            h = client.health()
            print(f"   ✅ 服务健康: {h}")

            result = client.transcribe_text(text)
            print(f"   📝 转录: {result['task_id']}")

            struct = client.structure(result["task_id"])
            print(f"   🏗 结构化: {struct['template_name']}")

            usage = client.get_usage()
            print(f"   📊 用量: {usage['used_this_month']}/{usage['limit_this_month']}")

            templates = client.list_templates()
            print(f"   📋 模板数: {len(templates)}")
        except Exception as e:
            print(f"   ❌ 付费模式失败: {e}")
    else:
        print("\n💡 未检测到客户端证书。获取证书后可测试付费模式。")


if __name__ == "__main__":
    quick_test()

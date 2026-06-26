from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from app.providers.adobe.auth import AdobeTokenManager
from app.providers.adobe.client import AdobeClient, AdobeAPIError

from app.providers.base import ProviderBase

logger = logging.getLogger(__name__)


class AdobeProvider(ProviderBase):
    name = "adobe"

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        token_manager = AdobeTokenManager(config)
        self.client = AdobeClient(
            token_manager=token_manager,
            org_id=config["adobe_org_id"],
            base_url=config["adobe_api_base_url"],
            default_domain=config.get("adobe_default_domain"),
        )

    def init_metadata(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"provider": self.name, "status": {}, "products": []}
        try:
            profiles = self.list_products()
            data["products"] = [
                {
                    "id": profile.get("id") or profile.get("groupId"),
                    "name": profile.get("name") or profile.get("groupName"),
                    "productId": profile.get("productId"),
                }
                for profile in profiles
            ]
            data["status"]["profiles"] = "ok"
        except Exception as exc:
            data["status"]["profiles"] = f"error: {exc}"

        try:
            _ = self.client.get_products_rest()
            data["status"]["rest"] = "ok"
        except Exception as exc:
            data["status"]["rest"] = f"error: {exc}"

        return data

    def list_products(self) -> List[Dict[str, Any]]:
        return self.client.list_profiles()

    def create_user(self, identifier: str, product: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        firstname, lastname = self.client._parse_username(identifier)
        product_ids = [product] if product else kwargs.get("productProfileIds")
        response = self.client.create_user(
            email=identifier,
            firstname=kwargs.get("firstname", firstname),
            lastname=kwargs.get("lastname", lastname),
            user_type=kwargs.get("user_type", "federatedID"),
            country=kwargs.get("country", "CN"),
            product_profile_ids=product_ids,
        )
        return response

    def assign_product(self, identifier: str, product: str) -> Dict[str, Any]:
        return self.client.assign_product_profiles(identifier, [product])

    def reset_password(self, identifier: str, **kwargs) -> Dict[str, Any]:
        return self.client.reset_password(identifier)

    def delete_user(self, identifier: str) -> Dict[str, Any]:
        return self.client.delete_user(identifier)

    def describe_user(self, identifier: str) -> Dict[str, Any]:
        try:
            user = self.client.get_user(identifier)
            return {"user": user}
        except AdobeAPIError as exc:
            return {"error": str(exc), "status": exc.status_code, "response": exc.response}

    def self_test(self, product_id: Optional[str] = None) -> Dict[str, Any]:
        if not product_id or str(product_id).lower() in ("none", "null", ""):
            raise ValueError("自检需要有效的 Product Profile ID，请通过 --product 指定。")

        # addAdobeID 类似 Admin Console "邀请用户"，不需要域所有权
        email = f"selftest_{int(time.time())}@example.com"
        summary: Dict[str, Any] = {
            "provider": self.name,
            "username": email,
            "product": product_id,
            "steps": [],
        }

        created = False
        try:
            create_res = self.client.create_user(
                email=email,
                firstname="Self",
                lastname="Test",
                user_type="adobeID",
                country="CN",
                product_profile_ids=[product_id],
            )
            errors = (create_res or {}).get("errors") or []
            env_codes = {"error.domain.trust.nonexistent"}
            if errors and any(e.get("errorCode") in env_codes for e in errors):
                summary["steps"].append({
                    "create_user": "skipped",
                    "reason": "env_constraint: domain not owned by this Adobe org — cannot create new users here",
                    "errors": errors,
                })
                summary["note"] = (
                    "本组织没有声明可用于创建新用户的 federatedID/enterpriseID 域。"
                    "语法层 bug 已修复，此 org 只能邀请已存在的 AdobeID 或在 Azure/Google 侧创建后同步。"
                )
                return summary

            created = True
            summary["steps"].append({"create_user": True, "response": create_res})

            inspect = self.describe_user(email)
            summary["steps"].append({"inspect": "user" in inspect, "response": inspect})

            assign_res = self.client.assign_product_profiles(email, [product_id])
            summary["steps"].append({"assign_product": True, "response": assign_res})

            remove_res = self.client.remove_product_profile(email, product_id)
            summary["steps"].append({"remove_product": True, "response": remove_res})

            delete_res = self.client.delete_user(email)
            created = False
            summary["steps"].append({"delete_user": True, "response": delete_res})
        finally:
            if created:
                try:
                    self.client.delete_user(email)
                    summary["cleanup"] = "deleted"
                except Exception as exc:
                    summary["cleanup_error"] = str(exc)

        return summary

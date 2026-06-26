from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from app.providers.office365.auth import TokenManager
from app.providers.office365.graph_client import GraphClient, GraphAPIError
from app.providers.office365.license_manager import LicenseManager
from app.providers.office365.user_manager import UserManager

from app.providers.base import ProviderBase

logger = logging.getLogger(__name__)


class Office365Provider(ProviderBase):
    name = "office365"

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.token_manager = TokenManager({
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "token_endpoint": config["token_endpoint"],
        })
        self.graph_client = GraphClient(self.token_manager, config["graph_api_base_url"])
        self.license_manager = LicenseManager(self.graph_client)

        notification_config = {
            "enabled": config.get("notification_enabled", False),
            "from_email": config.get("notification_from_email"),
            "bcc_emails": config.get("notification_bcc_emails"),
            "email_domain": config.get("notification_email_domain"),
        }
        smtp_config = {
            "smtp_host": config.get("smtp_host"),
            "smtp_port": config.get("smtp_port", 465),
            "smtp_username": config.get("smtp_username"),
            "smtp_password": config.get("smtp_password"),
            "smtp_use_ssl": config.get("smtp_use_ssl", True),
        }

        self.user_manager = UserManager(
            self.graph_client,
            self.license_manager,
            default_password=config["default_password"],
            default_domain=config.get("default_domain"),
            notification_config=notification_config,
            smtp_config=smtp_config,
        )

    def init_metadata(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"provider": self.name, "status": {}, "products": []}
        try:
            # Simple connectivity test
            _ = self.graph_client.get_users(top=1)
            data["status"]["graph"] = "ok"
        except Exception as exc:
            data["status"]["graph"] = f"error: {exc}"

        try:
            data["products"] = self.license_manager.get_available_skus()
        except Exception as exc:
            data["status"]["products"] = f"error: {exc}"

        return data

    def list_products(self) -> List[Dict[str, Any]]:
        return self.license_manager.get_available_skus()

    def create_user(self, identifier: str, product: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        surname, given_name = self._split_name(identifier)
        usage_location = kwargs.pop("usageLocation", "CN")
        display_name = kwargs.pop("display_name", identifier)
        mail_nickname = kwargs.pop("mail_nickname", identifier)
        force_change = kwargs.pop("force_change_password", True)

        license_kwargs = self._license_kwargs(product)

        return self.user_manager.create_user(
            display_name=display_name,
            mail_nickname=mail_nickname,
            user_principal_name=identifier,
            force_change_password=force_change,
            **license_kwargs,
            surname=kwargs.pop("surname", surname),
            givenName=kwargs.pop("givenName", given_name),
            usageLocation=usage_location,
            **kwargs,
        )

    def assign_product(self, identifier: str, product: str) -> Dict[str, Any]:
        user = self.graph_client.get_user(self.user_manager._normalize_user_identifier(identifier))
        user_id = user["id"]

        if self._looks_like_guid(product):
            return self.license_manager.assign_license_to_user(user_id, sku_id=product)
        return self.license_manager.assign_license_to_user(user_id, sku_part_number=product)

    def reset_password(self, identifier: str, **kwargs) -> Dict[str, Any]:
        return self.user_manager.reset_password(
            identifier,
            new_password=kwargs.get("new_password"),
            force_change_password=kwargs.get("force_change_password", True),
        )

    def delete_user(self, identifier: str) -> Dict[str, Any]:
        return {"deleted": self.user_manager.delete_user(identifier)}

    def describe_user(self, identifier: str) -> Dict[str, Any]:
        try:
            normalized = self.user_manager._normalize_user_identifier(identifier)
            user = self.graph_client.get_user(normalized)
            return {"user": user}
        except GraphAPIError as exc:
            return {"error": str(exc), "status": exc.status_code}

    def self_test(self, product_id: Optional[str] = None) -> Dict[str, Any]:
        if not product_id or str(product_id).lower() in ("none", "null", ""):
            raise ValueError("自检需要有效的默认产品/许可证，请先运行 init 并设置默认产品。")

        username = f"selftest_{int(time.time())}"
        normalized = self.user_manager._normalize_user_identifier(username)
        summary: Dict[str, Any] = {
            "provider": self.name,
            "username": normalized,
            "product": product_id,
            "steps": [],
        }

        created = False
        license_kwargs = self._license_kwargs(product_id)

        surname, given_name = self._split_name(username)

        try:
            create_res = self.user_manager.create_user(
                display_name=username,
                mail_nickname=username,
                user_principal_name=username,
                force_change_password=True,
                surname=surname,
                givenName=given_name,
                usageLocation="CN",
                **license_kwargs,
            )
            created = True
            summary["steps"].append({"create_user": True, "response": create_res})

            reset_res = self.user_manager.reset_password(username, force_change_password=True)
            summary["steps"].append({"reset_password": True, "response": reset_res})

            users_snapshot = self.graph_client.get_users(select="id,userPrincipalName", top=50)
            summary["steps"].append({
                "export_users": True,
                "count": len(users_snapshot),
            })

            delete_res = self.user_manager.delete_user(username)
            created = False
            summary["steps"].append({"delete_user": delete_res})
        finally:
            if created:
                try:
                    self.user_manager.delete_user(username)
                except Exception as exc:
                    summary["cleanup_error"] = str(exc)

        return summary

    @staticmethod
    def _split_name(username: str) -> tuple[str, str]:
        base = username.split("@")[0]
        if len(base) >= 3:
            return base[:3], base[3:]
        return "", base

    @staticmethod
    def _looks_like_guid(value: str) -> bool:
        return len(value) == 36 and value.count("-") == 4

    def _license_kwargs(self, product: Optional[str]) -> Dict[str, str]:
        if not product:
            return {}
        if self._looks_like_guid(product):
            return {"sku_id": product}
        return {"sku_part_number": product}

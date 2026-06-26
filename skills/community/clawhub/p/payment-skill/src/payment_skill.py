"""
支付 Skill - 主类
"""

import asyncio
import json
import logging
from typing import Any, Dict, Optional
from datetime import datetime

try:
    # Try relative imports first (when used as a package)
    from .payment_api_client import PaymentAPIClient
    from .security import InputValidator, DataEncryption
    from .utils import generate_transaction_id, format_currency
    from .config_loader import ConfigLoader
except ImportError:
    # Fall back to absolute imports (when run directly)
    from payment_api_client import PaymentAPIClient
    from security import InputValidator, DataEncryption
    from utils import generate_transaction_id, format_currency
    from config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class PaymentSkill:
    """支付 Skill - 封装支付 API"""

    def __init__(self, config: Dict[str, Any] = None, env: str = "development"):
        """
        初始化支付 Skill
        
        参数:
            config: 配置字典（如果提供，将覆盖从文件加载的配置）
            env: 环境名称 (development 或 production)
        """
        self.id = "payment_skill"
        self.name = "支付服务"
        self.description = "提供支付相关的功能"
        self.version = "1.0.0"
        self.env = env

        # 配置 - 优先使用传入的配置，否则从文件加载
        if config:
            self.config = config
        else:
            try:
                self.config = ConfigLoader.get_api_config(env)
            except ValueError as e:
                logger.warning(f"从配置文件加载失败: {e}，将使用空配置")
                self.config = {}
        
        self.api_client: Optional[PaymentAPIClient] = None
        self.encryption = None  # 延迟初始化，在 initialize() 中创建
        self.validator = InputValidator()

        # 工具注册
        self.tools = {
            "create_payment": self.create_payment,
            "query_payment": self.query_payment,
            "refund_payment": self.refund_payment,
        }

        # 状态
        self.is_initialized = False
        self.transactions = {}  # 本地缓存

    async def initialize(self):
        """初始化 Skill"""
        try:
            logger.info("初始化支付 Skill...")

            # 创建 API 客户端
            self.api_client = PaymentAPIClient(
                api_key=self.config.get("api_key"),
                api_secret=self.config.get("api_secret"),
                api_url=self.config.get("api_url"),
                timeout=self.config.get("timeout", 30)
            )

            # 健康检查
            is_healthy = await self.api_client.health_check()
            if not is_healthy:
                raise Exception("支付 API 健康检查失败")

            # 初始化加密器（如果启用）
            if self.config.get("enable_encryption"):
                try:
                    self.encryption = DataEncryption.from_env()
                    logger.info("加密器初始化成功")
                except Exception as e:
                    logger.warning(f"加密器初始化失败: {e}，将继续运行但不使用加密")

            self.is_initialized = True
            logger.info("支付 Skill 初始化成功")

        except Exception as e:
            logger.error(f"支付 Skill 初始化失败: {e}")
            raise

    async def create_payment(self, amount: float, currency: str,
                            merchant_id: str, description: str = "") -> Dict[str, Any]:
        """
        创建支付请求

        参数:
            amount: 支付金额
            currency: 货币代码 (CNY, USD, EUR)
            merchant_id: 商户 ID
            description: 支付描述

        返回:
            支付结果
        """
        try:
            logger.info(f"创建支付: {amount} {currency} 给商户 {merchant_id}")

            # 参数验证
            if amount <= 0:
                raise ValueError("金额必须大于 0")
            if amount > 1000000:
                raise ValueError("单笔金额不能超过 100 万")
            if currency not in ["CNY", "USD", "EUR"]:
                raise ValueError(f"不支持的货币: {currency}")
            if not merchant_id:
                raise ValueError("商户 ID 不能为空")

            # 生成交易 ID
            transaction_id = generate_transaction_id()

            # 调用 API
            result = await self.api_client.create_payment(
                amount=amount,
                currency=currency,
                merchant_id=merchant_id,
                description=description
            )

            # 缓存交易信息
            self.transactions[transaction_id] = {
                "amount": amount,
                "currency": currency,
                "merchant_id": merchant_id,
                "status": "pending_auth",
                "created_at": datetime.utcnow().isoformat()
            }

            # 返回结果
            response = {
                "success": True,
                "transaction_id": transaction_id,
                "status": result.get("status", "pending_auth"),
                "amount": amount,
                "currency": currency,
                "verification_url": result.get("verification_url"),
                "qr_code": result.get("qr_code"),
                "expires_at": result.get("expires_at")
            }

            logger.info(f"支付创建成功: {transaction_id}")
            return response

        except ValueError as e:
            logger.warning(f"参数验证失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_code": "INVALID_PARAMS"
            }
        except Exception as e:
            logger.error(f"创建支付失败: {e}")
            return {
                "success": False,
                "error": "创建支付失败,请稍后重试",
                "error_code": "PAYMENT_ERROR"
            }

    async def query_payment(self, transaction_id: str) -> Dict[str, Any]:
        """
        查询支付状态

        参数:
            transaction_id: 交易 ID

        返回:
            支付状态
        """
        try:
            logger.info(f"查询支付状态: {transaction_id}")

            # 参数验证
            if not transaction_id:
                raise ValueError("交易 ID 不能为空")

            # 调用 API
            result = await self.api_client.query_payment(transaction_id)

            # 更新本地缓存
            if transaction_id in self.transactions:
                self.transactions[transaction_id]["status"] = result.get("status")

            # 返回结果
            response = {
                "success": True,
                "transaction_id": transaction_id,
                "status": result.get("status"),
                "amount": result.get("amount"),
                "currency": result.get("currency"),
                "created_at": result.get("created_at"),
                "completed_at": result.get("completed_at")
            }

            logger.info(f"支付状态查询成功: {transaction_id} - {result.get('status')}")
            return response

        except ValueError as e:
            logger.warning(f"参数验证失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_code": "INVALID_PARAMS"
            }
        except Exception as e:
            logger.error(f"查询支付失败: {e}")
            return {
                "success": False,
                "error": "查询支付失败,请稍后重试",
                "error_code": "QUERY_ERROR"
            }

    async def refund_payment(self, transaction_id: str,
                            amount: float = None) -> Dict[str, Any]:
        """
        发起退款

        参数:
            transaction_id: 原交易 ID
            amount: 退款金额(可选,不填则全额退款)

        返回:
            退款结果
        """
        try:
            logger.info(f"发起退款: {transaction_id}, 金额: {amount}")

            # 参数验证
            if not transaction_id:
                raise ValueError("交易 ID 不能为空")

            if amount is not None and amount <= 0:
                raise ValueError("退款金额必须大于 0")

            # 调用 API
            result = await self.api_client.refund_payment(
                transaction_id=transaction_id,
                amount=amount
            )

            # 返回结果
            response = {
                "success": True,
                "refund_id": result.get("id"),
                "status": result.get("status"),
                "amount": result.get("amount"),
                "currency": result.get("currency"),
                "created_at": result.get("created_at")
            }

            logger.info(f"退款发起成功: {result.get('id')}")
            return response

        except ValueError as e:
            logger.warning(f"参数验证失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_code": "INVALID_PARAMS"
            }
        except Exception as e:
            logger.error(f"发起退款失败: {e}")
            return {
                "success": False,
                "error": "发起退款失败,请稍后重试",
                "error_code": "REFUND_ERROR"
            }

    async def execute(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行工具

        参数:
            tool_name: 工具名称
            params: 工具参数

        返回:
            执行结果
        """
        if not self.is_initialized:
            return {
                "success": False,
                "error": "Skill 未初始化",
                "error_code": "NOT_INITIALIZED"
            }

        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"未知的工具: {tool_name}",
                "error_code": "UNKNOWN_TOOL"
            }

        try:
            tool_func = self.tools[tool_name]
            result = await tool_func(**params)
            return result
        except Exception as e:
            logger.error(f"执行工具 {tool_name} 失败: {e}")
            return {
                "success": False,
                "error": "工具执行失败",
                "error_code": "EXECUTION_ERROR"
            }

    async def cleanup(self):
        """清理资源"""
        try:
            logger.info("清理支付 Skill...")
            if self.api_client:
                await self.api_client.close()
            self.is_initialized = False
            logger.info("支付 Skill 清理完成")
        except Exception as e:
            logger.error(f"清理支付 Skill 失败: {e}")

    def get_tool_schema(self, tool_name: str) -> Dict[str, Any]:
        """获取工具的 JSON Schema"""
        schemas = {
            "create_payment": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "支付金额",
                        "minimum": 0.01,
                        "maximum": 1000000
                    },
                    "currency": {
                        "type": "string",
                        "description": "货币代码",
                        "enum": ["CNY", "USD", "EUR"]
                    },
                    "merchant_id": {
                        "type": "string",
                        "description": "商户 ID"
                    },
                    "description": {
                        "type": "string",
                        "description": "支付描述"
                    }
                },
                "required": ["amount", "currency", "merchant_id"]
            },
            "query_payment": {
                "type": "object",
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "交易 ID"
                    }
                },
                "required": ["transaction_id"]
            },
            "refund_payment": {
                "type": "object",
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "原交易 ID"
                    },
                    "amount": {
                        "type": "number",
                        "description": "退款金额(可选)"
                    }
                },
                "required": ["transaction_id"]
            }
        }
        return schemas.get(tool_name, {})

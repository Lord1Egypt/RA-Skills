"""
MCP 支付工具 - 供 helian-health-assistant skill 调用
用于连连支付 MCP 服务集成
"""

import requests
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class PaymentMethod:
    """支付方式"""
    pay_type: str  # ALIPAY_NATIVE, WECHAT_APPLET, BANKCARD
    pay_order_id: str
    pay_url: str
    pay_description: str


@dataclass
class PaymentStatus:
    """支付状态"""
    pay_order_id: str
    status: str  # WAITING_PAY, PAYING, PAY_SUCCESS, PAY_FAIL, CLOSED, REFUNDING, REFUNDED
    order_amount: Optional[str] = None
    paid_at: Optional[str] = None


class McpPaymentClient:
    """
    MCP 支付客户端
    
    使用示例:
        client = McpPaymentClient()
        
        # 创建支付订单
        methods = client.create_payment(
            payment_credential="xxx",
            agent_type="OPENCLAW",
            scene_type="MOBILE",
            terminal_env="WECHAT"
        )
        
        # 查询支付状态
        status = client.query_payment("xxx")
        
        # 确认银行卡支付
        result = client.confirm_bankcard_payment("xxx", "123456")
        
        # 关闭支付订单
        result = client.close_payment("xxx")
    """
    
    BASE_URL = "https://mcp.lianlianpay.com/mcp"
    PROTOCOL_VERSION = "2025-06-18"
    
    def __init__(self):
        self.session_id: Optional[str] = None
        self.headers = {
            "Content-Type": "application/json",
            "MCP-Protocol-Version": self.PROTOCOL_VERSION
        }
    
    def _ensure_initialized(self) -> bool:
        """确保客户端已初始化"""
        if not self.session_id:
            return self.initialize()
        return True
    
    def initialize(self) -> bool:
        """
        初始化 MCP 会话
        
        Returns:
            bool: 初始化是否成功
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": self.PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {
                    "name": "helian-health-assistant",
                    "version": "1.0.0"
                }
            },
            "id": 1
        }
        
        # 打印详细请求信息
        print(f"\n[MCP详细] ====== 初始化请求 ======")
        print(f"[MCP详细] URL: {self.BASE_URL}")
        print(f"[MCP详细] 请求头: {json.dumps(dict(self.headers), ensure_ascii=False, indent=2)}")
        print(f"[MCP详细] 请求体: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        
        try:
            response = requests.post(
                self.BASE_URL,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            # 打印详细响应信息
            print(f"\n[MCP详细] ====== 初始化响应 ======")
            print(f"[MCP详细] 状态码: {response.status_code}")
            print(f"[MCP详细] 响应头: {json.dumps(dict(response.headers), ensure_ascii=False, indent=2)}")
            print(f"[MCP详细] 响应体: {response.text}")
            print(f"[MCP详细] ======================\n")
            
            response.raise_for_status()
            
            # 从响应头获取 session_id
            self.session_id = response.headers.get("mcp-session-id")
            if self.session_id:
                self.headers["Mcp-Session-Id"] = self.session_id
                print(f"[MCP] 初始化成功，Session ID: {self.session_id}")
                return True
            else:
                print("[MCP] 初始化失败：未获取到 Session ID")
                return False
        except Exception as e:
            print(f"[MCP] 初始化失败: {e}")
            return False
    
    def _call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[Dict]:
        """
        调用 MCP 工具
        
        Args:
            tool_name: 工具名称
            arguments: 工具参数
            
        Returns:
            调用结果
        """
        if not self._ensure_initialized():
            return None
        
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": 2
        }
        
        # 打印详细请求信息
        print(f"\n[MCP详细] ====== 请求信息 ======")
        print(f"[MCP详细] URL: {self.BASE_URL}")
        print(f"[MCP详细] 请求头: {json.dumps(dict(self.headers), ensure_ascii=False, indent=2)}")
        print(f"[MCP详细] 请求体: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        
        try:
            response = requests.post(
                self.BASE_URL,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            # 打印详细响应信息
            print(f"\n[MCP详细] ====== 响应信息 ======")
            print(f"[MCP详细] 状态码: {response.status_code}")
            print(f"[MCP详细] 响应头: {json.dumps(dict(response.headers), ensure_ascii=False, indent=2)}")
            print(f"[MCP详细] 响应体: {response.text}")
            print(f"[MCP详细] ======================\n")
            
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                print(f"[MCP] 工具调用错误: {result['error']}")
                return None
            
            rpc_result = result.get("result", {})
            # 优先从 structuredContent 取（新格式），其次从 result 直接取（旧格式）
            if rpc_result.get("isError"):
                content = rpc_result.get("content", [])
                err_msg = content[0].get("text", "未知错误") if content else "未知错误"
                print(f"[MCP] 工具调用业务错误: {err_msg}")
                return None
            structured = rpc_result.get("structuredContent")
            if structured:
                return structured
            return rpc_result
        except Exception as e:
            print(f"[MCP] 工具调用失败: {e}")
            return None
    
    def create_payment(
        self,
        payment_credential: str,
        agent_type: str,
        scene_type: str,
        terminal_env: str
    ) -> Optional[List[PaymentMethod]]:
        """
        创建支付订单
        
        Args:
            payment_credential: 加密的支付凭证（由禾连服务生成）
            agent_type: Agent 类型 - OPENCLAW/COPAW/OTHER
            scene_type: 场景 - MOBILE(手机端)/PC(电脑端)/HEADLESS(无界面)
            terminal_env: 终端环境 - WECHAT/ALIPAY/FEISHU/DINGTALK/BROWSER
            
        Returns:
            支付方式列表，包含支付链接等信息
            
        Example:
            >>> methods = client.create_payment(
            ...     payment_credential="encrypted_credential",
            ...     agent_type="OPENCLAW",
            ...     scene_type="MOBILE",
            ...     terminal_env="WECHAT"
            ... )
            >>> for method in methods:
            ...     print(f"{method.pay_type}: {method.pay_url}")
        """
        result = self._call_tool("create_payment", {
            "paymentCredential": payment_credential,
            "agentType": agent_type,
            "sceneType": scene_type,
            "terminalEnv": terminal_env
        })
        
        if not result or "payList" not in result:
            return None
        
        methods = []
        for item in result["payList"]:
            methods.append(PaymentMethod(
                pay_type=item.get("payType", ""),
                pay_order_id=item.get("payOrderId", ""),
                pay_url=item.get("payUrl", ""),
                pay_description=item.get("payDescription", "")
            ))
        return methods
    
    def confirm_bankcard_payment(
        self,
        payment_credential: str,
        sms_code: str
    ) -> Optional[Dict[str, str]]:
        """
        确认银行卡支付（输入短信验证码完成支付）
        
        Args:
            payment_credential: 加密的支付凭证
            sms_code: 短信验证码（6位数字）
            
        Returns:
            包含 pay_order_id 的字典
            
        Example:
            >>> result = client.confirm_bankcard_payment("credential", "123456")
            >>> print(result["pay_order_id"])
        """
        result = self._call_tool("confirm_bankcard_payment", {
            "paymentCredential": payment_credential,
            "smsCode": sms_code
        })
        
        if result:
            return {"pay_order_id": result.get("payOrderId", "")}
        return None
    
    def query_payment(
        self,
        payment_credential: str
    ) -> Optional[PaymentStatus]:
        """
        查询支付状态
        
        Args:
            payment_credential: 加密的支付凭证
            
        Returns:
            支付状态信息
            
        Example:
            >>> status = client.query_payment("credential")
            >>> print(f"状态: {status.status}, 金额: {status.order_amount}")
        """
        result = self._call_tool("query_payment", {
            "paymentCredential": payment_credential
        })
        
        if not result:
            return None
        
        return PaymentStatus(
            pay_order_id=result.get("payOrderId", ""),
            status=result.get("status", ""),
            order_amount=result.get("orderAmount"),
            paid_at=result.get("paidAt")
        )
    
    def close_payment(
        self,
        payment_credential: str
    ) -> Optional[PaymentStatus]:
        """
        关闭支付订单
        
        Args:
            payment_credential: 加密的支付凭证
            
        Returns:
            关闭后的订单状态
            
        Example:
            >>> status = client.close_payment("credential")
            >>> print(f"订单已关闭: {status.status}")
        """
        result = self._call_tool("close_payment", {
            "paymentCredential": payment_credential
        })
        
        # close_payment 返回空对象，调用成功即表示关闭成功
        if result is None:
            return None
        
        return PaymentStatus(
            pay_order_id="",
            status="CLOSED"
        )


# ==================== 便捷函数（供 Skill 直接调用） ====================

def create_payment_order(
    payment_credential: str,
    agent_type: str = "",
    scene_type: str = "",
    terminal_env: str = ""
) -> Optional[List[PaymentMethod]]:
    """
    便捷函数：创建支付订单
    
    Args:
        payment_credential: 加密的支付凭证
        agent_type: Agent类型，默认空字符串
        scene_type: 场景，默认 空字符串
        terminal_env: 终端环境，默认 空字符串
        
    Returns:
        支付方式列表
    """
    print(f"[MCP支付] 创建支付订单 → 入参: {{'payment_credential': '{payment_credential[:50]}...', 'agent_type': '{agent_type}', 'scene_type': '{scene_type}', 'terminal_env': '{terminal_env}'}}")
    client = McpPaymentClient()
    result = client.create_payment(payment_credential, "", "", "")
    if result:
        print(f"[MCP支付] 创建支付订单 → 状态: 成功 | 获取到 {len(result)} 种支付方式")
    else:
        print(f"[MCP支付] 创建支付订单 → 状态: 失败")
    return result


def confirm_bankcard_pay(payment_credential: str, sms_code: str) -> Optional[Dict[str, str]]:
    """
    便捷函数：确认银行卡支付
    
    Args:
        payment_credential: 加密的支付凭证
        sms_code: 短信验证码
        
    Returns:
        支付结果
    """
    print(f"[MCP支付] 确认银行卡支付 → 入参: {{'payment_credential': '{payment_credential[:50]}...', 'sms_code': '{sms_code}'}}")
    client = McpPaymentClient()
    result = client.confirm_bankcard_payment(payment_credential, sms_code)
    if result:
        print(f"[MCP支付] 确认银行卡支付 → 状态: 成功 | 支付确认已提交")
    else:
        print(f"[MCP支付] 确认银行卡支付 → 状态: 失败")
    return result


def query_pay_status(payment_credential: str) -> Optional[PaymentStatus]:
    """
    便捷函数：查询支付状态
    
    Args:
        payment_credential: 加密的支付凭证
        
    Returns:
        支付状态
    """
    print(f"[MCP支付] 查询支付状态 → 入参: {{'payment_credential': '{payment_credential[:50]}...'}}")
    client = McpPaymentClient()
    result = client.query_payment(payment_credential)
    if result:
        print(f"[MCP支付] 查询支付状态 → 状态: 成功 | 支付状态: {result.status}")
    else:
        print(f"[MCP支付] 查询支付状态 → 状态: 失败")
    return result


def close_pay_order(payment_credential: str) -> Optional[PaymentStatus]:
    """
    便捷函数：关闭支付订单
    
    Args:
        payment_credential: 加密的支付凭证
        
    Returns:
        关闭后的状态
    """
    print(f"[MCP支付] 关闭支付订单 → 入参: {{'payment_credential': '{payment_credential[:50]}...'}}")
    client = McpPaymentClient()
    result = client.close_payment(payment_credential)
    if result:
        print(f"[MCP支付] 关闭支付订单 → 状态: 成功 | 订单状态: {result.status}")
    else:
        print(f"[MCP支付] 关闭支付订单 → 状态: 失败")
    return result


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 示例参数（请替换为实际值）
    PAYMENT_CREDENTIAL = "your_encrypted_payment_credential_here"
    AGENT_TYPE = "OPENCLAW"
    SCENE_TYPE = "MOBILE"
    TERMINAL_ENV = "WECHAT"
    SMS_CODE = "123456"
    
    client = McpPaymentClient()
    
    # 1. 创建支付订单
    print("=== 创建支付订单 ===")
    methods = client.create_payment(
        payment_credential=PAYMENT_CREDENTIAL,
        agent_type=AGENT_TYPE,
        scene_type=SCENE_TYPE,
        terminal_env=TERMINAL_ENV
    )
    if methods:
        for method in methods:
            print(f"支付方式: {method.pay_type}")
            print(f"支付链接: {method.pay_url}")
            print(f"描述: {method.pay_description}")
            print("-" * 40)
    
    # 2. 查询支付状态
    print("\n=== 查询支付状态 ===")
    status = client.query_payment(PAYMENT_CREDENTIAL)
    if status:
        print(f"订单号: {status.pay_order_id}")
        print(f"状态: {status.status}")
        print(f"金额: {status.order_amount}")
        print(f"支付时间: {status.paid_at}")
    
    # 3. 确认银行卡支付
    print("\n=== 确认银行卡支付 ===")
    result = client.confirm_bankcard_payment(PAYMENT_CREDENTIAL, SMS_CODE)
    if result:
        print(f"支付成功，订单号: {result['pay_order_id']}")
    
    # 4. 关闭支付订单
    print("\n=== 关闭支付订单 ===")
    status = client.close_payment(PAYMENT_CREDENTIAL)
    if status:
        print(f"订单已关闭: {status.pay_order_id}, 状态: {status.status}")

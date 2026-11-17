"""
PaperTrade 客户端
- EIP-712 签名（RegisterSessionKey / OpenPosition / Close）
- Session Key 注册与管理
- 通过 Relayer 提交交易意图
- 账户与持仓查询
"""
from __future__ import annotations

import json
import secrets
import time
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Optional

import requests
from eth_account import Account
from eth_account.messages import encode_typed_data

# ── 合约与链参数 ──────────────────────────────────────────────
PAPERTRADE = {
    "chainId": 999,
    "apiUrl": "https://exchange.papertrade.xyz",
    "rpcUrl": "https://rpc.hyperliquid.xyz/evm",
    "contracts": {
        "exchange": "0x6cd5661646289fb6e65ea5c032310fded797d0a2",
        "paper": "0xe40f17915daa230324030003a197cdaef2261c0e",
        "paperStaking": "0xaad6c7b0cc3014fc80ffedae0ed7ce5967b0f016",
        "usdc": "0xb88339cb7199b77e23db6e890353e22632ba630f",
    },
}

# 交易对：instrumentId
INSTRUMENTS = {
    "BTC": {"id": 0, "priceScale": 10},
    "ETH": {"id": 1, "priceScale": 100},
}

WAD = 10 ** 18  # 18 位精度的 USD 数值
INTENT_TTL = 3600  # 意图有效期 1 小时
SESSION_TTL = 30 * 24 * 3600  # Session Key 有效期 30 天

# EIP-712 类型定义
TYPES = {
    "RegisterSessionKey": [
        {"name": "user", "type": "address"},
        {"name": "key", "type": "address"},
        {"name": "expiry", "type": "uint64"},
        {"name": "feeAddress", "type": "address"},
        {"name": "nonce", "type": "uint256"},
        {"name": "deadline", "type": "uint64"},
    ],
    "OpenPosition": [
        {"name": "user", "type": "address"},
        {"name": "instrumentId", "type": "uint32"},
        {"name": "isLong", "type": "bool"},
        {"name": "size", "type": "uint128"},
        {"name": "leverage", "type": "uint32"},
        {"name": "useDebt", "type": "bool"},
        {"name": "nonce", "type": "uint256"},
        {"name": "deadline", "type": "uint64"},
    ],
    "Close": [
        {"name": "user", "type": "address"},
        {"name": "positionIds", "type": "uint256[]"},
        {"name": "nonce", "type": "uint256"},
        {"name": "deadline", "type": "uint64"},
    ],
}

EXCHANGE_DOMAIN = {
    "name": "String",
    "version": "1",
    "chainId": PAPERTRADE["chainId"],
    "verifyingContract": PAPERTRADE["contracts"]["exchange"],
}


@dataclass
class SessionCredential:
    wallet: str
    session_key: str  # 私钥 (hex)
    session_address: str
    expiry: int  # unix 秒


def _deadline(ttl: int) -> int:
    return int(time.time()) + ttl


def _usd_to_wad(usd: float) -> int:
    """将 USD 金额精确转换为 18 位精度的 wad 整数，避免浮点精度丢失"""
    return int((Decimal(str(usd)) * Decimal(WAD)).to_integral_value())


def _fresh_nonce() -> int:
    """匹配官方客户端的 nonce 方案：随机 24-bit 字索引 * 256 + 字内随机位"""
    word = int.from_bytes(secrets.token_bytes(3), "big") or 1
    bit = secrets.randbelow(256)
    return word * 256 + bit


def _to_wire(type_name: str, message: dict) -> dict:
    """将消息字段转为 wire 格式：uint 转十进制字符串，address/bytes 转小写 hex"""
    out = {}
    for field in TYPES[type_name]:
        name = field["name"]
        ftype = field["type"]
        val = message[name]
        if ftype.endswith("[]"):
            out[name] = [str(int(v)) for v in val]
        elif ftype == "bool":
            out[name] = bool(val)
        elif ftype.startswith("uint"):
            out[name] = str(int(val))
        else:
            out[name] = str(val).lower()
    return out


def _split_sig(sig: str) -> dict:
    sig = sig[2:] if sig.startswith("0x") else sig
    if len(sig) != 130:
        raise ValueError("签名长度错误")
    r = "0x" + sig[:64]
    s = "0x" + sig[64:128]
    v = int(sig[128:130], 16)
    if v >= 27:
        v -= 27
    return {"v": str(27 + v), "r": r.lower(), "s": s.lower()}


def _sign_typed_data(private_key: str, type_name: str, message: dict) -> dict:
    """用私钥对 EIP-712 类型数据签名，返回 wire 格式 + v/r/s"""
    wire = _to_wire(type_name, message)
    # 还原为 eth_account 需要的格式（uint 用 int，bool 用 bool）
    typed_msg = {}
    for field in TYPES[type_name]:
        name = field["name"]
        ftype = field["type"]
        if ftype.endswith("[]"):
            typed_msg[name] = [int(v) for v in wire[name]]
        elif ftype == "bool":
            typed_msg[name] = bool(wire[name])
        elif ftype.startswith("uint"):
            typed_msg[name] = int(wire[name])
        else:
            typed_msg[name] = wire[name]

    encoded = encode_typed_data(
        domain_data=EXCHANGE_DOMAIN,
        message_types={type_name: TYPES[type_name]},
        message_data=typed_msg,
    )
    signed = Account.sign_message(encoded, private_key=private_key)
    return {**wire, **_split_sig(signed.signature.hex())}


class PaperTradeClient:
    def __init__(self, wallet_private_key: str, session_key: Optional[str] = None):
        self.wallet = Account.from_key(wallet_private_key)
        self.wallet_address = self.wallet.address
        self.session: Optional[SessionCredential] = None
        if session_key:
            sess_acct = Account.from_key(session_key)
            # 从外部加载的 session key 无法知道真实过期时间，
            # 保守地设为 SESSION_TTL 的一半，到期后自动续期
            self.session = SessionCredential(
                wallet=self.wallet_address,
                session_key=session_key,
                session_address=sess_acct.address,
                expiry=int(time.time()) + SESSION_TTL // 2,
            )
        self._http = requests.Session()
        self._http.headers.update({"User-Agent": "paper-hedge-bot"})

    # ── Session Key ──────────────────────────────────────────
    def register_session_key(self) -> SessionCredential:
        """生成 session key 并用钱包签名注册到 relayer"""
        sess_acct = Account.create()
        message = {
            "user": self.wallet_address,
            "key": sess_acct.address,
            "expiry": _deadline(SESSION_TTL),
            "feeAddress": "0x0000000000000000000000000000000000000000",
            "nonce": _fresh_nonce(),
            "deadline": _deadline(INTENT_TTL),
        }
        signed = _sign_typed_data(self.wallet.key.hex(), "RegisterSessionKey", message)
        resp = self._post("/intents", {"action": "registerSessionKey", "signed": signed})
        self.session = SessionCredential(
            wallet=self.wallet_address,
            session_key=sess_acct.key.hex(),
            session_address=sess_acct.address,
            expiry=message["expiry"],
        )
        print(f"[PaperTrade] Session Key 注册成功: {sess_acct.address}")
        return self.session

    def _require_session(self):
        if not self.session:
            raise RuntimeError("未注册 Session Key，请先调用 register_session_key()")
        if self.session.expiry <= int(time.time()):
            raise RuntimeError("Session Key 已过期，请重新注册")
        if int(time.time()) + 3600 >= self.session.expiry:
            print("[PaperTrade] Session Key 即将过期，重新注册...")
            self.register_session_key()

    # ── 交易 ────────────────────────────────────────────────
    def open_position(
        self,
        symbol: str,
        is_long: bool,
        margin_usd: float,
        leverage: int,
        use_debt: bool = False,
    ) -> dict:
        """开仓。margin_usd 为保证金金额（USDC），leverage 为杠杆倍数"""
        self._require_session()
        if symbol not in INSTRUMENTS:
            raise ValueError(f"不支持的交易对: {symbol}，仅支持 BTC/ETH")

        instrument_id = INSTRUMENTS[symbol]["id"]
        margin_wad = _usd_to_wad(margin_usd)
        message = {
            "user": self.wallet_address,
            "instrumentId": instrument_id,
            "isLong": is_long,
            "size": margin_wad,
            "leverage": leverage,
            "useDebt": use_debt,
            "nonce": _fresh_nonce(),
            "deadline": _deadline(INTENT_TTL),
        }
        signed = _sign_typed_data(self.session.session_key, "OpenPosition", message)
        resp = self._post("/intents", {"action": "openPosition", "signed": signed})
        print(f"[PaperTrade] 开仓意图已提交: {symbol} {'多' if is_long else '空'} "
              f"${margin_usd} x{leverage} → intentId={resp.get('intentId', '?')}")
        return resp

    def close_positions(self, position_ids: list[str | int]) -> list[dict]:
        """平仓，一次最多 12 个"""
        self._require_session()
        results = []
        for i in range(0, len(position_ids), 12):
            batch = [int(pid) for pid in position_ids[i:i + 12]]
            message = {
                "user": self.wallet_address,
                "positionIds": batch,
                "nonce": _fresh_nonce(),
                "deadline": _deadline(INTENT_TTL),
            }
            signed = _sign_typed_data(self.session.session_key, "Close", message)
            resp = self._post("/intents", {"action": "closePositions", "signed": signed})
            results.append(resp)
            print(f"[PaperTrade] 平仓意图已提交: {len(batch)} 个仓位")
        return results

    def close_all(self, symbol: Optional[str] = None) -> list[dict]:
        """平掉所有（或指定交易对）的持仓"""
        acct = self.get_account()
        positions = acct.get("openPositions", [])
        # openPositions 是 tuple: [positionId, instrumentId, isLong, ..., entry, margin, leverage, bust, openedAt, intentId]
        if symbol:
            target_id = INSTRUMENTS[symbol.upper()]["id"]
            positions = [p for p in positions if int(p[1]) == target_id]
        ids = [str(p[0]) for p in positions]
        if not ids:
            print("[PaperTrade] 没有需要平仓的持仓")
            return []
        return self.close_positions(ids)

    # ── 查询 ────────────────────────────────────────────────
    def get_account(self) -> dict:
        """获取账户快照（余额、持仓、PAPER 等）- 通过 SSE 流"""
        url = f"{PAPERTRADE['apiUrl']}/state/user/live"
        params = {"wallet": self.wallet_address.lower()}
        resp = self._http.get(
            url, params=params, stream=True,
            headers={"Accept": "text/event-stream"}, timeout=15,
        )
        try:
            resp.raise_for_status()
            # 解析 SSE，找到 event: wallet 的快照
            current_event = None
            for line in resp.iter_lines(decode_unicode=True):
                if line == "":
                    current_event = None
                    continue
                if line.startswith("event:"):
                    current_event = line[6:].strip()
                elif line.startswith("data:") and current_event == "wallet":
                    data = line[5:].strip()
                    if data:
                        return json.loads(data)
            raise RuntimeError("PaperTrade 账户流未返回 wallet 快照")
        finally:
            resp.close()

    def get_positions(self) -> list[dict]:
        acct = self.get_account()
        positions = []
        for p in acct.get("openPositions", []):
            inst_id = int(p[1])
            scale = INSTRUMENTS.get(self._inst_symbol(inst_id), {"priceScale": 1})["priceScale"]
            positions.append({
                "positionId": str(p[0]),
                "instrumentId": inst_id,
                "isLong": bool(p[2]),
                "entryPrice": int(p[4]) / (10 ** scale),
                "marginUsd": int(p[5]) / WAD,
                "leverage": int(p[6]),
                "bustPrice": int(p[7]) / (10 ** scale),
                "openedAt": int(p[8]),
            })
        return positions

    @staticmethod
    def _inst_symbol(instrument_id: int) -> str:
        for sym, info in INSTRUMENTS.items():
            if info["id"] == instrument_id:
                return sym
        return "UNKNOWN"

    def get_protocol_summary(self) -> dict:
        return self._get("/query/protocol/summary")

    def get_paper_minted(self) -> float:
        """获取已 mint 的 PAPER 数量"""
        acct = self.get_account()
        paper = acct.get("paper", {})
        bal = int(paper.get("balance", 0) or 0)
        staked = int(paper.get("staked", 0) or 0)
        return (bal + staked) / WAD

    def get_balance_usd(self) -> float:
        acct = self.get_account()
        return int(acct.get("balance", 0) or 0) / WAD

    # ── HTTP ────────────────────────────────────────────────
    def _get(self, path: str, params: Optional[dict] = None) -> Any:
        url = PAPERTRADE["apiUrl"] + path
        resp = self._http.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, body: dict) -> Any:
        url = PAPERTRADE["apiUrl"] + path
        resp = self._http.post(
            url,
            data=json.dumps(body),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=35,
        )
        data = resp.json() if resp.text else {}
        if not resp.ok or data.get("error") or data.get("ok") is False:
            code = data.get("code", data.get("error", f"http_{resp.status_code}"))
            msg = data.get("message", data.get("error", resp.text))
            raise RuntimeError(f"PaperTrade relayer 错误 [{code}]: {msg}")
        return data

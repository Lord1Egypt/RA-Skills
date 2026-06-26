#!/usr/bin/env python3
"""temu.aftersales.signature.get — 售后签名获取."""
import _global_returns_refunds_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.aftersales.signature.get",
        "global_returns_refunds_aftersales_signature_get.py '<JSON>'",
    )

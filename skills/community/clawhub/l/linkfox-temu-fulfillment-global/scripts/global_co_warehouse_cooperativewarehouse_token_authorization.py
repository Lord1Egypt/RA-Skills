#!/usr/bin/env python3
"""bg.cooperativewarehouse.token.authorization — 合作仓 Token 授权."""
import _global_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "bg.cooperativewarehouse.token.authorization",
        "global_co_warehouse_cooperativewarehouse_token_authorization.py '<JSON>'",
    )

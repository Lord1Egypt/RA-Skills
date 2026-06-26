#!/usr/bin/env python3
"""temu.logistics.shipment.pickup.reservation.cancel — 取消上门揽收预约."""
import _us_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.logistics.shipment.pickup.reservation.cancel",
        "us_buy_shipping_logistics_shipment_pickup_reservation_cancel.py '<JSON>'",
    )

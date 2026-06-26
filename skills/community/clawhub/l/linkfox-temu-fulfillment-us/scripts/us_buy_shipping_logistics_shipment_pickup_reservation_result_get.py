#!/usr/bin/env python3
"""temu.logistics.shipment.pickup.reservation.result.get — 查询上门揽收预约结果."""
import _us_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.logistics.shipment.pickup.reservation.result.get",
        "us_buy_shipping_logistics_shipment_pickup_reservation_result_get.py '<JSON>'",
    )

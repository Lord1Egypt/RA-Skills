#!/usr/bin/env python3
"""temu.logistics.shipment.pickup.reservation.create — 预约上门揽收."""
import _eu_fulfillment_script as m

if __name__ == "__main__":
    m.run_cli(
        "temu.logistics.shipment.pickup.reservation.create",
        "eu_buy_shipping_logistics_shipment_pickup_reservation_create.py '<JSON>'",
    )

#!/usr/bin/env python3
"""Shared PSU headroom calculation."""

import math


DEFAULT_NON_CORE_POWER_W = 50
PSU_HEADROOM_FACTOR = 1.35
PSU_TIGHT_MARGIN_W = 50


def recommended_psu_w(cpu_w, gpu_w, extra_w=DEFAULT_NON_CORE_POWER_W):
    """Return the minimum recommended PSU wattage for known component loads."""
    return math.ceil(
        (float(cpu_w) + float(gpu_w) + float(extra_w)) * PSU_HEADROOM_FACTOR
    )

#!/usr/bin/env python3
from unittest import TestCase, main

from macmon_status import build_summary, fmt_bytes, fmt_pct, fmt_temp, verdict


class TestMacmonStatus(TestCase):
    def test_formatters(self) -> None:
        self.assertEqual(fmt_temp(56.396), "56.4°C")
        self.assertEqual(fmt_pct(0.1691), "16.9%")
        self.assertEqual(fmt_bytes(17179869184), "16.0 GB")

    def test_verdict_for_calm_machine(self) -> None:
        payload = {
            "sys_power": 13.6914,
            "memory": {"swap_usage": 83820544},
            "temp": {"cpu_temp_avg": 49.7487},
        }
        self.assertEqual(verdict(payload), "Looks calm: light to moderate load.")

    def test_build_summary_contains_key_fields(self) -> None:
        payload = {
            "timestamp": "2026-03-30T17:00:31.302235+00:00",
            "sys_power": 18.7033,
            "cpu_power": 3.1965,
            "gpu_power": 0.0170,
            "pcpu_usage": [4068, 0.1691],
            "ecpu_usage": [2892, 0.3825],
            "gpu_usage": [758, 0.0228],
            "memory": {
                "ram_total": 17179869184,
                "ram_usage": 11404345344,
                "swap_total": 1073741824,
                "swap_usage": 83820544,
            },
            "temp": {
                "cpu_temp_avg": 56.3965,
                "gpu_temp_avg": 46.3085,
            },
        }
        text = build_summary(payload)
        self.assertIn("Verdict: Looks calm: light to moderate load.", text)
        self.assertIn("CPU temp: 56.4°C", text)
        self.assertIn("GPU temp: 46.3°C", text)
        self.assertIn("Performance CPU: 16.9% @ 4068 MHz", text)
        self.assertIn("RAM: 10.6 GB / 16.0 GB", text)


if __name__ == "__main__":
    main()

"""Tests for the financial guard-rails.

Each test corresponds to a finding from the ClawHub audit. The rule is: no
protection depends on the LLM's good behavior — if a test here fails, there is
a path for the agent to spend money outside the limits.
"""
from __future__ import annotations

import os
import tempfile
import time
import unittest
import unittest.mock
from pathlib import Path

os.environ["POLYMARKET_AGENT_HOME"] = tempfile.mkdtemp(prefix="polytest-")

from polymarket_agent import guardrails, journal  # noqa: E402
from polymarket_agent import config  # noqa: E402
from polymarket_agent.config import Settings  # noqa: E402


def fresh_settings(**overrides) -> Settings:
    settings = Settings()
    for key, value in overrides.items():
        setattr(settings, key, value)
    return settings


class GuardrailsTest(unittest.TestCase):
    def setUp(self) -> None:
        home = Path(os.environ["POLYMARKET_AGENT_HOME"])
        for name in ("journal.jsonl", "HALT", "config.json"):
            (home / name).unlink(missing_ok=True)

    # ── Numeric sanity ───────────────────────────────────────────────────────
    def test_price_out_of_range_is_blocked(self):
        for bad_price in (0.0, 1.0, 1.5, -0.2):
            decision = guardrails.evaluate_order("BUY", bad_price, 10, fresh_settings())
            self.assertFalse(decision.allowed, f"price {bad_price} should be blocked")
            self.assertTrue(any("range" in r for r in decision.reasons))

    def test_non_finite_values_are_blocked(self):
        for bad in (float("nan"), float("inf")):
            self.assertFalse(guardrails.evaluate_order("BUY", bad, 10, fresh_settings()).allowed)
            self.assertFalse(guardrails.evaluate_order("BUY", 0.5, bad, fresh_settings()).allowed)

    def test_non_positive_size_is_blocked(self):
        for bad_size in (0, -5):
            self.assertFalse(
                guardrails.evaluate_order("BUY", 0.5, bad_size, fresh_settings()).allowed
            )

    def test_invalid_side_is_blocked(self):
        self.assertFalse(guardrails.evaluate_order("YOLO", 0.5, 10, fresh_settings()).allowed)

    # ── Financial caps ───────────────────────────────────────────────────────
    def test_position_cap_is_enforced(self):
        settings = fresh_settings(max_position_usd=25.0)
        # 0.50 × 100 = $50 > $25
        decision = guardrails.evaluate_order("BUY", 0.50, 100, settings)
        self.assertFalse(decision.allowed)
        self.assertTrue(any("per-order cap" in r for r in decision.reasons))

    def test_bankroll_percentage_cap_is_enforced(self):
        settings = fresh_settings(max_position_usd=1000.0, max_bankroll_pct=5.0)
        # $50 on a $100 bankroll = 50% >> 5%
        decision = guardrails.evaluate_order("BUY", 0.50, 100, settings, balance_usd=100.0)
        self.assertFalse(decision.allowed)
        self.assertTrue(any("% of balance" in r for r in decision.reasons))

    def test_missing_balance_warns_instead_of_silently_passing(self):
        settings = fresh_settings()
        decision = guardrails.evaluate_order("BUY", 0.10, 10, settings, balance_usd=None)
        self.assertTrue(any("balance unavailable" in w for w in decision.warnings))

    def test_daily_spend_cap_accumulates_across_orders(self):
        settings = fresh_settings(max_daily_spend_usd=100.0, max_position_usd=100.0)
        journal.record(
            journal.Entry(status="submitted", side="BUY", notional=95.0, token_id="1")
        )
        decision = guardrails.evaluate_order("BUY", 0.50, 20, settings)  # +$10
        self.assertFalse(decision.allowed)
        self.assertTrue(any("daily spend" in r for r in decision.reasons))

    def test_rejected_orders_do_not_consume_daily_budget(self):
        journal.record(
            journal.Entry(status="rejected", side="BUY", notional=500.0, token_id="1")
        )
        self.assertEqual(journal.spend_since(86400), 0.0)

    def test_sells_do_not_consume_daily_budget(self):
        journal.record(
            journal.Entry(status="submitted", side="SELL", notional=500.0, token_id="1")
        )
        self.assertEqual(journal.spend_since(86400), 0.0)

    def test_open_order_cap_is_enforced(self):
        settings = fresh_settings(max_open_orders=2)
        for i in range(2):
            journal.record(
                journal.Entry(status="submitted", side="BUY", notional=1.0, token_id=str(i))
            )
        decision = guardrails.evaluate_order("BUY", 0.10, 1, settings)
        self.assertFalse(decision.allowed)
        self.assertTrue(any("open orders" in r for r in decision.reasons))

    # ── Kill switch ──────────────────────────────────────────────────────────
    def test_halt_blocks_everything_including_valid_orders(self):
        settings = fresh_settings()
        self.assertTrue(guardrails.evaluate_order("BUY", 0.10, 10, settings).allowed)
        guardrails.engage_halt("test")
        self.assertFalse(guardrails.evaluate_order("BUY", 0.10, 10, settings).allowed)
        guardrails.release_halt()
        self.assertTrue(guardrails.evaluate_order("BUY", 0.10, 10, settings).allowed)

    def test_halt_overrides_autonomous_mode(self):
        settings = guardrails.enable_autonomous(fresh_settings(), hours=1)
        guardrails.engage_halt("emergency")
        decision = guardrails.evaluate_order("BUY", 0.10, 10, settings)
        self.assertFalse(decision.allowed)

    # ── Autonomy ─────────────────────────────────────────────────────────────
    def test_confirmation_required_by_default(self):
        decision = guardrails.evaluate_order("BUY", 0.10, 10, fresh_settings())
        self.assertTrue(decision.requires_confirmation)

    def test_autonomous_without_expiry_is_ignored(self):
        # Hand-tampered config: autonomous_mode=true but no expiry.
        settings = fresh_settings(autonomous_mode=True, autonomous_expires_at=0.0)
        self.assertFalse(guardrails.autonomous_active(settings))
        self.assertTrue(
            guardrails.evaluate_order("BUY", 0.10, 10, settings).requires_confirmation
        )

    def test_expired_autonomous_falls_back_to_confirmation(self):
        settings = fresh_settings(
            autonomous_mode=True, autonomous_expires_at=time.time() - 1
        )
        decision = guardrails.evaluate_order("BUY", 0.10, 10, settings)
        self.assertTrue(decision.requires_confirmation)
        self.assertTrue(any("EXPIRED" in w for w in decision.warnings))

    def test_autonomous_still_bounded_by_financial_caps(self):
        settings = guardrails.enable_autonomous(
            fresh_settings(max_position_usd=25.0), hours=1
        )
        decision = guardrails.evaluate_order("BUY", 0.50, 100, settings)  # $50
        self.assertFalse(decision.allowed, "autonomous mode must not bypass the per-order cap")

    def test_enable_autonomous_clamps_duration(self):
        settings = guardrails.enable_autonomous(fresh_settings(), hours=999)
        self.assertLessEqual(settings.autonomous_expires_at - time.time(), 24 * 3600 + 5)


class KeystoreTest(unittest.TestCase):
    """AUDIT FIX (High) — the key is never in argv, and never in plaintext."""

    def test_rejects_malformed_keys(self):
        from polymarket_agent.keystore import KeystoreError, normalize_private_key

        for bad in ("", "0x123", "not-hex", "0x" + "z" * 64, "0x" + "0" * 64):
            with self.assertRaises(KeystoreError):
                normalize_private_key(bad)

    def test_error_never_leaks_key_material(self):
        from polymarket_agent.keystore import KeystoreError, normalize_private_key

        secret = "0x" + "a" * 63 + "zz"
        try:
            normalize_private_key(secret)
        except KeystoreError as exc:
            self.assertNotIn("aaaa", str(exc))

    def test_loaded_key_repr_does_not_leak(self):
        from polymarket_agent.keystore import LoadedKey

        loaded = LoadedKey("0x" + "b" * 64, "0xADDR", "keystore")
        self.assertNotIn("bbbb", repr(loaded))
        self.assertNotIn("bbbb", str(loaded))
        self.assertNotIn("bbbb", f"{loaded}")

    def test_redact_reveals_nothing_at_all(self):
        from polymarket_agent.keystore import redact

        secret = "0x" + "c" * 64
        masked = redact(secret)
        self.assertNotIn("cc", masked)
        self.assertNotIn(secret[-4:], masked)

    def test_short_address_only_applies_to_public_data(self):
        from polymarket_agent.keystore import short_address

        self.assertEqual(short_address("0x1234567890abcdef1234"), "0x1234…1234")
        self.assertEqual(short_address(None), "<no wallet>")


class LegacyEnvKeyPrecedenceTest(unittest.TestCase):
    """SECURITY FIX (SkillSpector E2, High, 0.93 confidence): POLYMARKET_KEY
    used to be checked BEFORE the keystore and activate on its mere presence,
    with no explicit opt-in. A leftover env var from testing could silently
    override a properly configured keystore. Each test here isolates its own
    POLYMARKET_AGENT_HOME so it cannot interact with the shared test state."""

    ENV_KEY = "0x" + "7" * 64
    KEYSTORE_KEY = "0x" + "9" * 64

    def setUp(self) -> None:
        self._home = tempfile.mkdtemp(prefix="polykeytest-")
        self._patch = unittest.mock.patch.dict(
            os.environ, {"POLYMARKET_AGENT_HOME": self._home}, clear=False
        )
        self._patch.start()
        for var in ("POLYMARKET_KEY", "POLYMARKET_ALLOW_ENV_KEY"):
            os.environ.pop(var, None)

    def tearDown(self) -> None:
        for var in ("POLYMARKET_KEY", "POLYMARKET_ALLOW_ENV_KEY"):
            os.environ.pop(var, None)
        self._patch.stop()

    def test_env_key_without_gate_is_rejected(self):
        from polymarket_agent import keystore

        os.environ["POLYMARKET_KEY"] = self.ENV_KEY
        with self.assertRaises(keystore.KeystoreError) as ctx:
            keystore.load_key(interactive=False)
        self.assertIn("POLYMARKET_ALLOW_ENV_KEY", str(ctx.exception))

    def test_env_key_with_gate_works_when_no_keystore(self):
        from polymarket_agent import keystore

        os.environ["POLYMARKET_KEY"] = self.ENV_KEY
        os.environ["POLYMARKET_ALLOW_ENV_KEY"] = "1"
        loaded = keystore.load_key(interactive=False)
        self.assertEqual(loaded.source, "env")
        self.assertEqual(loaded.private_key, self.ENV_KEY.lower())

    def test_keystore_takes_precedence_over_gated_env_key(self):
        """The core fix: even with the env key fully gated and present, an
        existing keystore must win."""
        from polymarket_agent import keystore

        keystore.save_key(self.KEYSTORE_KEY, "a-strong-passphrase")
        os.environ["POLYMARKET_PASSPHRASE"] = "a-strong-passphrase"
        os.environ["POLYMARKET_KEY"] = self.ENV_KEY
        os.environ["POLYMARKET_ALLOW_ENV_KEY"] = "1"
        try:
            loaded = keystore.load_key(interactive=False)
        finally:
            os.environ.pop("POLYMARKET_PASSPHRASE", None)
        self.assertEqual(loaded.source, "keystore")
        self.assertEqual(loaded.private_key, self.KEYSTORE_KEY.lower())
        self.assertNotEqual(loaded.private_key, self.ENV_KEY.lower())


class ConfigValidationTest(unittest.TestCase):
    """AUDIT FIX (Medium) — no arbitrary writes to host config."""

    def test_unknown_keys_are_rejected(self):
        from polymarket_agent.config import ConfigError, _coerce

        for bad in ("../../secrets.env", "gateway.token", "__proto__"):
            with self.assertRaises(ConfigError):
                _coerce(bad, "x")

    def test_numeric_bounds_are_enforced(self):
        from polymarket_agent.config import ConfigError, _coerce

        with self.assertRaises(ConfigError):
            _coerce("max_bankroll_pct", 500)
        with self.assertRaises(ConfigError):
            _coerce("max_position_usd", -1)

    def test_risk_profile_is_closed_domain(self):
        from polymarket_agent.config import ConfigError, _coerce

        with self.assertRaises(ConfigError):
            _coerce("risk_profile", "yolo")
        self.assertEqual(_coerce("risk_profile", "DEGEN".lower().replace("degen", "aggressive")),
                         "aggressive")

    def test_funder_address_must_be_evm(self):
        from polymarket_agent.config import ConfigError, _coerce

        with self.assertRaises(ConfigError):
            _coerce("funder_address", "not-an-address")
        self.assertEqual(_coerce("funder_address", "0x" + "1" * 40), "0x" + "1" * 40)


class MarketParsingTest(unittest.TestCase):
    """BUG FIX — outcome ↔ price ↔ token_id correctly paired."""

    def test_json_string_fields_are_parsed(self):
        from polymarket_agent.markets import parse_market

        market = parse_market(
            {
                "id": "1",
                "question": "Will it rain?",
                "outcomes": '["Yes","No"]',
                "outcomePrices": '["0.30","0.70"]',
                "clobTokenIds": '["111","222"]',
                "volume24hr": "1234.5",
            }
        )
        self.assertEqual(len(market.outcomes), 2)
        self.assertAlmostEqual(market.outcomes[0].price, 0.30)
        self.assertEqual(market.outcomes[0].token_id, "111")
        self.assertEqual(market.token_for("no"), "222")
        self.assertAlmostEqual(market.volume_24h, 1234.5)

    def test_malformed_payload_does_not_crash(self):
        from polymarket_agent.markets import parse_market

        market = parse_market({"id": "2", "outcomes": "{garbage", "outcomePrices": None})
        self.assertEqual(market.outcomes, [])
        self.assertEqual(market.prices_label(), "N/A")

    def test_missing_token_ids_are_empty_not_wrong(self):
        from polymarket_agent.markets import parse_market

        market = parse_market(
            {"id": "3", "outcomes": '["Yes","No"]', "outcomePrices": '["0.5","0.5"]'}
        )
        self.assertIsNone(market.token_for("Yes"))


if __name__ == "__main__":
    unittest.main(verbosity=2)


class AutonomyConfigBypassTest(unittest.TestCase):
    """The `poly auto` gate — `--i-understand-the-risk` plus an expiry clamped
    to 24h — is worth nothing if the same two fields can be written straight
    through `poly config`, which reads as a harmless settings command.
    """

    def setUp(self) -> None:
        home = Path(os.environ["POLYMARKET_AGENT_HOME"])
        (home / "config.json").unlink(missing_ok=True)

    def test_autonomous_mode_is_not_writable_through_config(self):
        with self.assertRaises(config.ConfigError):
            config.set_value("autonomous_mode", "true")
        self.assertFalse(config.load_settings().autonomous_mode)

    def test_expiry_is_not_writable_through_config(self):
        with self.assertRaises(config.ConfigError):
            config.set_value("autonomous_expires_at", time.time() + 86400 * 3650)
        self.assertEqual(config.load_settings().autonomous_expires_at, 0.0)

    def test_the_gated_command_path_still_works(self):
        """Locking the keys must not stop `poly auto` from persisting them."""
        config.save_settings(guardrails.enable_autonomous(Settings(), 2))
        self.assertTrue(guardrails.autonomous_active(config.load_settings()))

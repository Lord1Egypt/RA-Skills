import pytest

from core.policy_engine import (
    ConfirmationRequiredError,
    PolicyEngine,
    PolicyViolationError,
)


def test_readonly_passes(config_dir):
    engine = PolicyEngine(config_dir=config_dir)
    engine.check("analyze_git_diff", environment="test")  # 不抛异常即通过


def test_confirmation_required(config_dir):
    engine = PolicyEngine(config_dir=config_dir)
    with pytest.raises(ConfirmationRequiredError):
        engine.check("generate_migration", environment="test")


def test_forbidden(config_dir):
    engine = PolicyEngine(config_dir=config_dir)
    with pytest.raises(PolicyViolationError):
        engine.check("apply_migration_prod", environment="test")


def test_unknown_action_requires_confirmation(config_dir):
    engine = PolicyEngine(config_dir=config_dir)
    with pytest.raises(ConfirmationRequiredError):
        engine.check("some_unlisted_action", environment="test")

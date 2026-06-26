from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from mpt_portfolio.utils import (
    DEFAULT_ASSETS,
    get_portfolios_dir,
    get_project_root,
    resolve_env_vars,
    validate_portfolio_name,
)


@dataclass
class PortfolioConfig:
    name: str = "default"
    initial_investment: float = 100_000
    assets: list[str] = field(default_factory=lambda: list(DEFAULT_ASSETS))
    benchmark: str = "SPY"


@dataclass
class DataConfig:
    lookback_years: int = 5
    frequency: str = "daily"
    price_type: str = "adjusted"


@dataclass
class ConstraintsConfig:
    long_only: bool = True
    max_weight: float = 0.40
    min_weight: float = 0.0


@dataclass
class OptimizationConfig:
    method: str = "max_sharpe"
    risk_free_rate: float | str = "auto"
    expected_returns: str = "mean_historical"
    covariance: str = "ledoit_wolf"
    constraints: ConstraintsConfig = field(default_factory=ConstraintsConfig)


@dataclass
class BacktestConfig:
    backtest_years: int = 5
    start_date: str | None = None
    end_date: str | None = None
    rebalancing_strategies: list[str] = field(
        default_factory=lambda: ["monthly", "quarterly", "yearly", "dynamic"]
    )
    dynamic_threshold: float = 0.05
    transaction_cost: float = 0.001
    include_buy_and_hold: bool = True


@dataclass
class EmailConfig:
    enabled: bool = False
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_use_tls: bool = True
    smtp_user: str | None = None
    smtp_password: str | None = None
    sender: str | None = None
    recipients: list[str] = field(default_factory=list)

    def resolve_env(self) -> EmailConfig:
        """Return a copy with ${VAR} patterns resolved from environment."""
        return EmailConfig(
            enabled=self.enabled,
            smtp_host=resolve_env_vars(self.smtp_host) if self.smtp_host else None,
            smtp_port=self.smtp_port,
            smtp_use_tls=self.smtp_use_tls,
            smtp_user=resolve_env_vars(self.smtp_user) if self.smtp_user else None,
            smtp_password=resolve_env_vars(self.smtp_password) if self.smtp_password else None,
            sender=resolve_env_vars(self.sender) if self.sender else None,
            recipients=[resolve_env_vars(r) for r in self.recipients] if self.recipients else [],
        )


@dataclass
class NotificationEventsConfig:
    method: str = "file"
    portfolio_created: bool = True
    backtest_complete: bool = True
    rebalance_reminder: bool = True
    performance_report: bool = True


@dataclass
class RebalancingConfig:
    strategy: str = "recommended"


@dataclass
class ReportsConfig:
    formats: list[str] = field(default_factory=lambda: ["html", "terminal"])
    charts: list[str] = field(
        default_factory=lambda: [
            "efficient_frontier",
            "correlation_heatmap",
            "weights",
            "equity_curves",
            "drawdown",
            "rolling_sharpe",
        ]
    )


@dataclass
class MonitoringConfig:
    frequency: str = "none"


@dataclass
class Config:
    portfolio: PortfolioConfig = field(default_factory=PortfolioConfig)
    data: DataConfig = field(default_factory=DataConfig)
    optimization: OptimizationConfig = field(default_factory=OptimizationConfig)
    backtest: BacktestConfig = field(default_factory=BacktestConfig)
    rebalancing: RebalancingConfig = field(default_factory=RebalancingConfig)
    reports: ReportsConfig = field(default_factory=ReportsConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    email: EmailConfig = field(default_factory=EmailConfig)
    notifications: NotificationEventsConfig = field(default_factory=NotificationEventsConfig)


class ConfigValidationError(Exception):
    pass


def load_default_config() -> dict:
    path = get_project_root() / "config" / "default.yaml"
    with open(path) as f:
        return yaml.safe_load(f)


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base. Override values win."""
    result = dict(base)
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = val
    return result


def _build_constraints(raw: dict) -> ConstraintsConfig:
    return ConstraintsConfig(
        long_only=raw.get("long_only", True),
        max_weight=raw.get("max_weight", 0.40),
        min_weight=raw.get("min_weight", 0.0),
    )


def _build_email(raw: dict | None) -> EmailConfig:
    if not raw:
        return EmailConfig()
    return EmailConfig(
        enabled=raw.get("enabled", False),
        smtp_host=raw.get("smtp_host"),
        smtp_port=raw.get("smtp_port", 587),
        smtp_use_tls=raw.get("smtp_use_tls", True),
        smtp_user=raw.get("smtp_user"),
        smtp_password=raw.get("smtp_password"),
        sender=raw.get("sender"),
        recipients=list(raw.get("recipients") or []),
    )


def _build_notification_events(raw: dict | None) -> NotificationEventsConfig:
    if not raw:
        return NotificationEventsConfig()
    return NotificationEventsConfig(
        method=raw.get("method", "file"),
        portfolio_created=raw.get("portfolio_created", True),
        backtest_complete=raw.get("backtest_complete", True),
        rebalance_reminder=raw.get("rebalance_reminder", True),
        performance_report=raw.get("performance_report", True),
    )


def validate_config(raw: dict) -> Config:
    """Validate raw dict and build Config. Raises ConfigValidationError on invalid input."""
    errors: list[str] = []

    p = raw.get("portfolio", {})
    if not p.get("assets"):
        errors.append("portfolio.assets must be a non-empty list of tickers")
    if p.get("initial_investment") is not None and p["initial_investment"] <= 0:
        errors.append("portfolio.initial_investment must be positive")

    d = raw.get("data", {})
    if d.get("lookback_years") is not None and d["lookback_years"] < 2:
        errors.append("data.lookback_years must be >= 2 (need sufficient history for stable covariance estimation)")
    if d.get("price_type") and d["price_type"] not in ("adjusted", "unadjusted"):
        errors.append("data.price_type must be 'adjusted' or 'unadjusted'")

    o = raw.get("optimization", {})
    valid_methods = {"max_sharpe", "min_variance", "efficient_frontier", "risk_parity"}
    if o.get("method") and o["method"] not in valid_methods:
        errors.append(f"optimization.method must be one of {valid_methods}")
    valid_returns = {"mean_historical", "exp_weighted", "black_litterman"}
    if o.get("expected_returns") and o["expected_returns"] not in valid_returns:
        errors.append(f"optimization.expected_returns must be one of {valid_returns}")
    valid_cov = {"sample", "ledoit_wolf"}
    if o.get("covariance") and o["covariance"] not in valid_cov:
        errors.append(f"optimization.covariance must be one of {valid_cov}")

    c = o.get("constraints", {})
    if c.get("max_weight") is not None and not (0 < c["max_weight"] <= 1):
        errors.append("optimization.constraints.max_weight must be in (0, 1]")
    if c.get("min_weight") is not None and c["min_weight"] < 0:
        errors.append("optimization.constraints.min_weight must be >= 0")

    b = raw.get("backtest", {})
    valid_strategies = {"monthly", "quarterly", "yearly", "dynamic"}
    for s in b.get("rebalancing_strategies", []):
        if s not in valid_strategies:
            errors.append(f"backtest.rebalancing_strategies contains invalid '{s}'")
    if b.get("dynamic_threshold") is not None and not (0 < b["dynamic_threshold"] < 1):
        errors.append("backtest.dynamic_threshold must be in (0, 1)")
    if b.get("transaction_cost") is not None and b["transaction_cost"] < 0:
        errors.append("backtest.transaction_cost must be >= 0")

    m = raw.get("monitoring", {})
    valid_frequencies = {"weekly", "monthly", "none"}
    if m.get("frequency") and m["frequency"] not in valid_frequencies:
        errors.append(f"monitoring.frequency must be one of {valid_frequencies}")

    n = raw.get("notifications", {})
    valid_notif_methods = {"file", "email", "both"}
    if n.get("method") and n["method"] not in valid_notif_methods:
        errors.append(f"notifications.method must be one of {valid_notif_methods}")

    # Backward compat: migrate old rebalancing.notification.email → top-level email
    rb = raw.get("rebalancing", {})
    old_notif = rb.get("notification", {})
    if old_notif:
        old_email = old_notif.get("email", {})
        existing_email = raw.get("email", {})
        email_unconfigured = not existing_email or (
            not existing_email.get("enabled") and not existing_email.get("smtp_host")
        )
        if old_email and email_unconfigured:
            migrated = {}
            field_map = {
                "smtp_server": "smtp_host", "smtp_host": "smtp_host",
                "smtp_port": "smtp_port", "smtp_use_tls": "smtp_use_tls",
                "username": "smtp_user", "smtp_user": "smtp_user",
                "password": "smtp_password", "smtp_password": "smtp_password",
                "from_addr": "sender", "sender": "sender",
                "to_addr": "recipients", "recipients": "recipients",
            }
            for old_key, new_key in field_map.items():
                if old_key in old_email and old_email[old_key] is not None:
                    val = old_email[old_key]
                    if new_key == "recipients" and isinstance(val, str):
                        val = [val]
                    migrated[new_key] = val
            if any(migrated.get(k) for k in ("smtp_host", "smtp_user", "sender")):
                migrated["enabled"] = True
            raw["email"] = migrated
        if "notifications" not in raw and old_notif.get("method"):
            raw["notifications"] = {"method": old_notif["method"]}

    if errors:
        raise ConfigValidationError("Configuration errors:\n  - " + "\n  - ".join(errors))

    return Config(
        portfolio=PortfolioConfig(
            name=p.get("name", "default"),
            initial_investment=float(p.get("initial_investment", 100_000)),
            assets=list(p.get("assets", DEFAULT_ASSETS)),
            benchmark=p.get("benchmark", "SPY"),
        ),
        data=DataConfig(
            lookback_years=int(d.get("lookback_years", 5)),
            frequency=d.get("frequency", "daily"),
            price_type=d.get("price_type", "adjusted"),
        ),
        optimization=OptimizationConfig(
            method=o.get("method", "max_sharpe"),
            risk_free_rate=o.get("risk_free_rate", "auto"),
            expected_returns=o.get("expected_returns", "mean_historical"),
            covariance=o.get("covariance", "ledoit_wolf"),
            constraints=_build_constraints(c),
        ),
        backtest=BacktestConfig(
            backtest_years=int(b.get("backtest_years", 5)),
            start_date=b.get("start_date"),
            end_date=b.get("end_date"),
            rebalancing_strategies=list(
                b.get("rebalancing_strategies", ["monthly", "quarterly", "yearly", "dynamic"])
            ),
            dynamic_threshold=float(b.get("dynamic_threshold", 0.05)),
            transaction_cost=float(b.get("transaction_cost", 0.001)),
            include_buy_and_hold=b.get("include_buy_and_hold", True),
        ),
        rebalancing=RebalancingConfig(
            strategy=raw.get("rebalancing", {}).get("strategy", "recommended"),
        ),
        reports=ReportsConfig(
            formats=list(raw.get("reports", {}).get("formats", ["html", "terminal"])),
            charts=list(raw.get("reports", {}).get("charts", [
                "efficient_frontier", "correlation_heatmap", "weights",
                "equity_curves", "drawdown", "rolling_sharpe",
            ])),
        ),
        monitoring=MonitoringConfig(
            frequency=m.get("frequency", "none"),
        ),
        email=_build_email(raw.get("email")),
        notifications=_build_notification_events(raw.get("notifications")),
    )


def load_portfolio_config(portfolio_name: str) -> Config:
    """Load portfolio config, merge with defaults, validate, return Config."""
    defaults = load_default_config()
    portfolio_dir = get_portfolios_dir() / portfolio_name
    config_path = portfolio_dir / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            overrides = yaml.safe_load(f) or {}
        merged = _deep_merge(defaults, overrides)
    else:
        merged = defaults
    merged.setdefault("portfolio", {})["name"] = portfolio_name
    return validate_config(merged)


def save_portfolio_config(portfolio_name: str, config: Config) -> Path:
    """Serialize Config to YAML at portfolios/<name>/config.yaml."""
    portfolio_dir = get_portfolios_dir() / portfolio_name
    portfolio_dir.mkdir(parents=True, exist_ok=True)

    raw = {
        "portfolio": {
            "name": config.portfolio.name,
            "initial_investment": config.portfolio.initial_investment,
            "assets": config.portfolio.assets,
            "benchmark": config.portfolio.benchmark,
        },
        "data": {
            "lookback_years": config.data.lookback_years,
            "frequency": config.data.frequency,
            "price_type": config.data.price_type,
        },
        "optimization": {
            "method": config.optimization.method,
            "risk_free_rate": config.optimization.risk_free_rate,
            "expected_returns": config.optimization.expected_returns,
            "covariance": config.optimization.covariance,
            "constraints": {
                "long_only": config.optimization.constraints.long_only,
                "max_weight": config.optimization.constraints.max_weight,
                "min_weight": config.optimization.constraints.min_weight,
            },
        },
        "backtest": {
            "backtest_years": config.backtest.backtest_years,
            "start_date": config.backtest.start_date,
            "end_date": config.backtest.end_date,
            "rebalancing_strategies": config.backtest.rebalancing_strategies,
            "dynamic_threshold": config.backtest.dynamic_threshold,
            "transaction_cost": config.backtest.transaction_cost,
            "include_buy_and_hold": config.backtest.include_buy_and_hold,
        },
        "rebalancing": {
            "strategy": config.rebalancing.strategy,
        },
        "notifications": {
            "method": config.notifications.method,
            "portfolio_created": config.notifications.portfolio_created,
            "backtest_complete": config.notifications.backtest_complete,
            "rebalance_reminder": config.notifications.rebalance_reminder,
            "performance_report": config.notifications.performance_report,
        },
        "reports": {
            "formats": config.reports.formats,
            "charts": config.reports.charts,
        },
        "monitoring": {
            "frequency": config.monitoring.frequency,
        },
    }

    raw["email"] = {
        "enabled": config.email.enabled,
        "smtp_host": config.email.smtp_host,
        "smtp_port": config.email.smtp_port,
        "smtp_use_tls": config.email.smtp_use_tls,
        "smtp_user": config.email.smtp_user,
        "smtp_password": config.email.smtp_password,
        "sender": config.email.sender,
        "recipients": config.email.recipients,
    }

    path = portfolio_dir / "config.yaml"
    with open(path, "w") as f:
        yaml.dump(raw, f, default_flow_style=False, sort_keys=False)
    return path


def create_portfolio_from_config(config: Config) -> Path:
    """Create portfolio directory structure and save config."""
    name = validate_portfolio_name(config.portfolio.name)
    portfolio_dir = get_portfolios_dir() / name
    if portfolio_dir.exists():
        raise FileExistsError(f"Portfolio '{name}' already exists at {portfolio_dir}")
    portfolio_dir.mkdir(parents=True)
    (portfolio_dir / "reports").mkdir()
    save_portfolio_config(name, config)
    return portfolio_dir

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import yaml

from .alerts import AlertThresholds, classify_alert_level, trigger_alerts_if_needed
from .billing import charge_user, check_balance, get_billing_logger
from .cache import has_recent_charge, record_charge
from .daily_briefing import append_scan_snapshot, generate_daily_briefing
from .escalation import calculate_escalation_score
from .search import SearchRequest, dedupe_tweets, filter_noise, search_with_fallback
from .telegram_alert import send_telegram_alert
from .translator import build_translation_bundle
from .trending import TrendingDetector

__all__ = ["PersianXRadarAgent", "run_radar"]


ToolFn = Callable[..., Any]


@dataclass
class ToolRegistry:
    x_keyword_search: Optional[ToolFn] = None
    x_semantic_search: Optional[ToolFn] = None
    web_search: Optional[ToolFn] = None
    translate_text: Optional[ToolFn] = None
    send_alert: Optional[ToolFn] = None


class PersianXRadarAgent:
    def __init__(self, config_path: str, tools: Optional[ToolRegistry] = None) -> None:
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.tools = tools or ToolRegistry()
        self.logger = get_billing_logger()

    def _load_config(self) -> Dict[str, Any]:
        with self.config_path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def update_keywords(self, keywords: List[str]) -> None:
        self.config["monitoring"]["keywords"] = keywords

    def add_keyword(self, keyword: str) -> None:
        kws = self.config["monitoring"]["keywords"]
        if keyword not in kws:
            kws.append(keyword)

    def update_accounts(self, accounts: List[str]) -> None:
        self.config["monitoring"]["accounts"] = accounts

    def add_account(self, account: str) -> None:
        accounts = self.config["monitoring"]["accounts"]
        if account not in accounts:
            accounts.append(account)

    def set_thresholds(self, min_retweets: Optional[int] = None, min_faves: Optional[int] = None) -> None:
        if min_retweets is not None:
            self.config["thresholds"]["min_retweets"] = min_retweets
        if min_faves is not None:
            self.config["thresholds"]["min_faves"] = min_faves

    def _parse_intent(self, command: str) -> str:
        low = command.lower()
        if "daily briefing" in low or "daily report" in low:
            return "daily_briefing"
        if any(k in low for k in ["run persian radar", "scan iran tweets", "monitor iran signals"]):
            return "immediate_scan"
        if "monitor account" in low:
            return "account_monitoring"
        if "keyword" in low:
            return "keyword_update"
        if "alert" in low:
            return "alert_settings"
        return "immediate_scan"

    def _compute_score(self, tweet: Any, credibility_accounts: List[str], keywords: List[str]) -> int:
        engagement = tweet.likes + (tweet.retweets * 2)
        keyword_hits = sum(1 for k in keywords if k in tweet.text)
        credibility = 100 if tweet.author.lower().lstrip("@") in {
            a.lower().lstrip("@") for a in credibility_accounts
        } else 0
        return engagement + (keyword_hits * 25) + credibility

    def _payment_required_response(self, payment_link: str, price: float) -> Dict[str, Any]:
        return {
            "status": "payment_required",
            "message": "Insufficient balance to run Persian X Radar.",
            "price": price,
            "payment_link": payment_link,
        }

    def _billing_gate(self, user_id: str) -> Dict[str, Any]:
        billing_cfg = self.config.get("billing", {})
        cooldown_minutes = int(billing_cfg.get("charge_cooldown_minutes", 15))
        skill_id = str(billing_cfg.get("skill_id", ""))
        price = float(billing_cfg.get("price_per_call", 0.0))

        if has_recent_charge(user_id, cooldown_minutes):
            self.logger.info("charge skipped (recent payment) user_id=%s price=$%.2f", user_id, price)
            return {"allowed": True, "billing_state": "recent_payment", "price": price}

        charge_result = charge_user(user_id=user_id)
        if charge_result.get("success"):
            record_charge(user_id)
            self.logger.info(
                "User charged $%.2f for Persian X Radar scan user_id=%s skill_id=%s",
                price,
                user_id,
                skill_id,
            )
            return {"allowed": True, "billing_state": "charged", "price": price}

        payment_link = charge_result.get("payment_url")
        if not payment_link:
            balance_result = check_balance(user_id=user_id)
            payment_link = balance_result.get("payment_url")
        if not payment_link:
            payment_link = f"https://skillpay.me/pay?skill_id={skill_id}&user_id={user_id}"

        self.logger.info("payment required user_id=%s skill_id=%s price=$%.2f", user_id, skill_id, price)
        return {
            "allowed": False,
            "billing_state": "payment_required",
            "payment_link": payment_link,
            "price": price,
        }

    def run_scan(
        self,
        command: str = "run persian radar",
        since_hours: Optional[int] = None,
        user_id: str = "anonymous",
    ) -> Dict[str, Any]:
        intent = self._parse_intent(command)

        billing_decision = self._billing_gate(user_id=user_id)
        if not billing_decision.get("allowed", False):
            return self._payment_required_response(
                payment_link=billing_decision["payment_link"],
                price=float(billing_decision.get("price", 0.0)),
            )

        monitoring = self.config["monitoring"]
        thresholds_cfg = self.config["thresholds"]
        alert_cfg = self.config["alerts"]
        scan_hours = since_hours or monitoring["default_since_hours"]

        req = SearchRequest(
            keywords=monitoring["keywords"],
            accounts=monitoring.get("accounts", []),
            min_faves=thresholds_cfg["min_faves"],
            min_retweets=thresholds_cfg["min_retweets"],
            since_hours=scan_hours,
        )

        tweets = search_with_fallback(
            req=req,
            x_keyword_search=self.tools.x_keyword_search,
            x_semantic_search=self.tools.x_semantic_search,
            web_search=self.tools.web_search,
        )

        tweets = filter_noise(tweets)
        tweets = dedupe_tweets(tweets)

        ranked = sorted(
            tweets,
            key=lambda t: self._compute_score(t, monitoring.get("accounts", []), monitoring["keywords"]),
            reverse=True,
        )

        output_rows: List[Dict[str, Any]] = []
        alert_thresholds = AlertThresholds(
            high_engagement=alert_cfg["high_engagement"],
            medium_engagement=alert_cfg["medium_engagement"],
        )

        for idx, t in enumerate(ranked, start=1):
            translations = build_translation_bundle(
                t.text,
                translate_text_tool=self.tools.translate_text,
                languages=self.config["translation"]["languages"],
            )
            engagement_score = t.likes + (2 * t.retweets)
            alert_level = classify_alert_level(t.text, engagement_score, alert_thresholds)

            output_rows.append(
                {
                    "#": idx,
                    "author": t.author,
                    "time": self._format_relative_time(t.timestamp),
                    "persian": translations.original_fa,
                    "english": translations.english,
                    "arabic": translations.arabic,
                    "chinese": translations.chinese,
                    "engagement": f"{t.likes} likes / {t.retweets} RT",
                    "link": t.url,
                    "alert": alert_level,
                    "score": engagement_score,
                }
            )

        # Existing channel alerts for row-level HIGH signals.
        if alert_cfg.get("enabled", True):
            trigger_alerts_if_needed(
                rows=output_rows,
                channels=alert_cfg.get("channels", []),
                send_alert_tool=self.tools.send_alert,
            )

        trend_cfg = self.config.get("trending", {})
        trend_detector = TrendingDetector(
            keywords=trend_cfg.get("keywords", monitoring["keywords"]),
            spike_threshold=float(trend_cfg.get("spike_threshold", 3.0)),
            min_volume=int(trend_cfg.get("min_volume", 3)),
        )
        trending_signals = trend_detector.detect([t.text for t in ranked])

        escalation = calculate_escalation_score(
            rows=output_rows,
            monitored_accounts=monitoring.get("accounts", []),
        )

        telegram_sent = send_telegram_alert(
            escalation=escalation,
            trending=trending_signals,
            rows=output_rows,
            config=self.config,
        )

        generated_at = datetime.now(timezone.utc).isoformat()
        append_scan_snapshot(
            generated_at=generated_at,
            rows=output_rows,
            trending=trending_signals,
            escalation=escalation,
        )

        report = self._build_markdown_report(
            rows=output_rows,
            scan_hours=scan_hours,
            escalation=escalation,
            trending=trending_signals,
        )

        response: Dict[str, Any] = {
            "status": "success",
            "scan_window": f"last {scan_hours} hours",
            "tweets_found": len(output_rows),
            "alerts": sum(1 for r in output_rows if r["alert"] == "HIGH"),
            "escalation": escalation,
            "trending_signals": trending_signals,
            "report": report,
            "rows": output_rows,
            "generated_at": generated_at,
            "billing_state": billing_decision.get("billing_state"),
            "telegram_alert_sent": telegram_sent,
        }

        if output_rows:
            response["summary"] = self._build_bilingual_summary(output_rows)
        else:
            response["message"] = "No high-signal Persian tweets detected in the last scan."

        if intent == "daily_briefing":
            response["daily_briefing"] = generate_daily_briefing()

        return response

    def _format_relative_time(self, ts: datetime) -> str:
        delta = datetime.now(timezone.utc) - ts.astimezone(timezone.utc)
        hours = max(int(delta.total_seconds() // 3600), 0)
        return f"{hours}h ago"

    def _build_markdown_report(
        self,
        rows: List[Dict[str, Any]],
        scan_hours: int,
        escalation: Dict[str, Any],
        trending: List[Dict[str, Any]],
    ) -> str:
        lines: List[str] = [
            "# Iran Intelligence Radar Report",
            f"Scan window: last {scan_hours} hours",
            f"Escalation score: {escalation.get('escalation_score', 0)} ({escalation.get('level', 'LOW')})",
            "",
            "|#|Author|Persian|English|Engagement|Alert|",
            "|---|---|---|---|---|---|",
        ]

        if rows:
            for r in rows:
                lines.append(
                    "|{0}|{1}|{2}|{3}|{4}|{5}|".format(
                        r["#"],
                        r["author"],
                        r["persian"].replace("|", "\\|"),
                        r["english"].replace("|", "\\|"),
                        r["engagement"],
                        r["alert"],
                    )
                )
        else:
            lines.append("|1|N/A|No high-signal Persian tweets detected in the last scan.|N/A|N/A|LOW|")

        lines.extend(["", "## Trending Signals"])
        if trending:
            for i, signal in enumerate(trending[:10], start=1):
                lines.append(
                    f"{i}. {signal['keyword']} spike detected (current={signal['current_volume']}, "
                    f"average={signal['average_volume']}, score={signal['trend_score']})"
                )
        else:
            lines.append("1. No major keyword spike detected in this scan.")

        return "\n".join(lines)

    def _build_bilingual_summary(self, rows: List[Dict[str, Any]]) -> Dict[str, str]:
        high_count = sum(1 for r in rows if r["alert"] == "HIGH")
        med_count = sum(1 for r in rows if r["alert"] == "MEDIUM")

        english = (
            f"Recent Persian-language posts show {high_count} high-alert and {med_count} medium-alert signals. "
            "Discussion centers on security, protest, and sanction narratives with elevated engagement."
        )
        chinese = (
            f"近期波斯语内容显示 {high_count} 条高警报、{med_count} 条中等警报信号。"
            "讨论重点集中在安全局势、抗议与制裁相关叙事，互动热度上升。"
        )
        return {"english": english, "chinese": chinese}


def run_radar(user_id: str, query: str = "run persian radar", since_hours: int | None = None):
    cfg = Path(__file__).with_name("config.yaml")
    agent = PersianXRadarAgent(config_path=str(cfg))
    return agent.run_scan(
        command=query,
        since_hours=since_hours,
        user_id=user_id,
    )


if __name__ == "__main__":
    result = run_radar(
        user_id="demo-user",
        query="run persian radar",
    )

    if result.get("status") == "payment_required":
        print("Payment required:", result.get("payment_link"))
    else:
        print(result.get("report", "No report generated"))

        if "summary" in result:
            print("\nEnglish summary:\n", result["summary"]["english"])
            print("\nChinese summary:\n", result["summary"]["chinese"])

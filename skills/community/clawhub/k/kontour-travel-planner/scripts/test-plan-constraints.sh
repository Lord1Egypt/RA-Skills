#!/usr/bin/env bash
# Regression smoke tests for natural-language constraint capture.
# Runs offline; no API keys or network calls.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLAN="$SCRIPT_DIR/plan.sh"

case_one="$($PLAN '5 days in Kyoto for a couple under $1800, relaxed pace, stay near Gion, opening hours matter, vegetarian food, rain backup')"
case_two="$($PLAN '3 days in Paris for 2 people budget cap €900, packed pace, prefer Montmartre neighborhood, halal food, avoid heat')"
case_three="$($PLAN '2 days in Tokyo for 2 people under $50, opening hours matter, rain backup, food')"
case_four="$($PLAN '2 days in Hakone for a couple, food and culture')"
case_five="$($PLAN 'compare Tokyo vs Paris vs Bangkok for 7 days in December for a couple, mid range budget, food and culture, relaxed pace')"

python3 - "$case_one" "$case_two" "$case_three" "$case_four" "$case_five" <<'PY'
import json
import sys

kyoto = json.loads(sys.argv[1])
paris = json.loads(sys.argv[2])
tokyo_risk = json.loads(sys.argv[3])
hakone_sparse = json.loads(sys.argv[4])
comparison = json.loads(sys.argv[5])

assert kyoto["budget"]["cap"] == {"amount": 1800, "currency": "USD", "scope": "cap"}
assert kyoto["constraint_details"]["trip_pace"] == "relaxed"
assert kyoto["constraint_details"]["neighborhood_preference"] == "Gion"
assert kyoto["constraint_details"]["opening_hours_sensitivity"] is True
assert kyoto["constraint_details"]["food_preferences"] == ["vegetarian"]
assert kyoto["constraint_details"]["weather_sensitivity"] == ["rain backup"]
assert "constraints" not in kyoto["open_decisions"]

kyoto_places = kyoto["suggested_places"]
assert kyoto_places, "expected suggested places with scoring explanations"
for place in kyoto_places[:3]:
    factors = place["why_chosen"]
    assert len(factors) >= 2, place
    assert place["explanation"].count(":") >= 2, place["explanation"]
assert any("thematic fit" in factor for factor in kyoto_places[0]["why_chosen"])
assert any("budget fit" in factor for factor in kyoto_places[0]["why_chosen"])

kyoto_continuity = kyoto["day_plan_continuity"]
assert kyoto_continuity["sequencing_goal"].startswith("morning/afternoon/evening anchors")
assert [segment["time_of_day"] for segment in kyoto_continuity["segments"]] == ["morning", "afternoon", "evening"]
assert [segment["place"] for segment in kyoto_continuity["segments"]] == ["Gion District", "Fushimi Inari", "Kiyomizu-dera"]
assert len(kyoto_continuity["transition_rationale"]) == 2
assert all("backtracking" in note or "same-zone" in note for note in kyoto_continuity["transition_rationale"])
assert "backtracking" in kyoto_continuity["backtracking_note"]

assert paris["budget"]["tier"] == "budget"
assert paris["budget"]["cap"] == {"amount": 900, "currency": "EUR", "scope": "cap"}
assert paris["constraint_details"]["trip_pace"] == "packed"
assert paris["constraint_details"]["neighborhood_preference"] == "Montmartre"
assert paris["constraint_details"]["food_preferences"] == ["halal"]
assert paris["constraint_details"]["weather_sensitivity"] == ["heat sensitive"]


risk_types = {risk["risk"]: risk for risk in tokyo_risk["risk_fallbacks"]}
assert {"closed_venue", "weather_mismatch", "over_constrained_plan"}.issubset(risk_types), risk_types
assert risk_types["closed_venue"]["fallback"]["nearest_viable_alternative"], risk_types["closed_venue"]
assert risk_types["weather_mismatch"]["fallback"]["nearest_viable_alternative"] == "Tsukiji Outer Market", risk_types["weather_mismatch"]
assert "USD 50" in risk_types["over_constrained_plan"]["warning"], risk_types["over_constrained_plan"]
assert "1-day budget plan in Tokyo" == risk_types["over_constrained_plan"]["fallback"]["nearest_viable_alternative"]

sparse_risk = hakone_sparse["risk_fallbacks"][0]
assert sparse_risk["risk"] == "sparse_area", sparse_risk
assert sparse_risk["fallback"]["nearest_viable_alternative"] == "Tokyo", sparse_risk
assert "side-trip" in sparse_risk["fallback"]["action"], sparse_risk

compare = comparison["destination_comparison"]
assert [option["name"] for option in compare["options"]] == ["Tokyo", "Paris", "Bangkok"], compare
assert compare["recommended_option"] == "Bangkok", compare
assert compare["operator_summary"].startswith("Start with Bangkok"), compare
assert len(compare["how_to_decide"]) == 4, compare
for option in compare["options"]:
    assert len(option["fit_factors"]) >= 2, option
    assert option["tradeoffs"], option
    assert option["decision_signal"], option
    assert [row["criterion"] for row in option["decision_matrix"]] == ["Budget fit", "Season fit", "Interest fit", "Pace fit"], option
    assert option["best_for"], option
    assert option["watch_out"], option
assert any("budget_daily_usd" in option for option in compare["options"]), compare
bangkok = next(option for option in compare["options"] if option["name"] == "Bangkok")
assert next(row for row in bangkok["decision_matrix"] if row["criterion"] == "Season fit")["signal"] == "strong", bangkok
tokyo = next(option for option in compare["options"] if option["name"] == "Tokyo")
assert next(row for row in tokyo["decision_matrix"] if row["criterion"] == "Season fit")["signal"] == "caution", tokyo

polish = kyoto["output_polish"]
assert [section["title"] for section in polish["compact_sections"]] == [
    "Trip Snapshot", "Best-Fit Choices", "Day Flow", "Risks + Backups"
], polish
assert polish["decision_summary"] == "Recommend Fushimi Inari; needs live validation before final itinerary.", polish
assert len(polish["decision_rationale"]) >= 2, polish
assert any("Gion District" in item for item in polish["decision_rationale"]), polish
assert any("fallback" in action.lower() for action in polish["next_step_actions"]), polish
assert [item["owner"] for item in polish["next_action_checklist"]] == ["user", "operator", "operator", "user"], polish
assert polish["next_action_checklist"][0]["status"] == "needed", polish
assert "Confirm fallback preference" in polish["next_action_checklist"][-1]["action"], polish
assert polish["next_step_prompt"] == {
    "audience": "user",
    "prompt": "What type of stay should I assume?",
    "reason": "This is the highest-impact traveler clarification before the next planning pass.",
    "source": "next_action_checklist[0]",
}, polish
assert polish["response_template"]["format"] == "four-line operator draft", polish
assert polish["response_template"]["tone"].startswith("concise"), polish
assert [line.split(":", 1)[0] for line in polish["response_template"]["lines"]] == ["Lead with", "Why", "Watch", "Next"], polish
assert "Fushimi Inari" in polish["response_template"]["lines"][0], polish
assert "Verify live opening hours" in polish["response_template"]["lines"][2], polish

compare_polish = comparison["output_polish"]
assert compare_polish["decision_summary"] == "Recommend Bangkok; needs one clarification before detailed planning.", compare_polish
assert any("Bangkok" in item for item in compare_polish["decision_rationale"]), compare_polish
assert any(section["title"] == "Best-Fit Choices" for section in compare_polish["compact_sections"]), compare_polish
assert compare_polish["next_action_checklist"][0]["owner"] == "user", compare_polish
assert compare_polish["next_step_prompt"]["audience"] == "user", compare_polish
assert compare_polish["next_step_prompt"]["prompt"] == "Which destination should I optimize for first?", compare_polish
assert "Bangkok" in compare_polish["response_template"]["lines"][0], compare_polish
assert compare_polish["response_template"]["lines"][3].startswith("Next:"), compare_polish

print("constraint capture smoke tests passed")
PY

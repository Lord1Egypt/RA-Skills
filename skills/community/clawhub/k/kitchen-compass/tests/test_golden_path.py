import json


def test_full_flow_end_to_end(data_root, run_cmd):
    run_cmd("validate_recipes.py", "--data-root", str(data_root))
    run_cmd("build_recipe_query_index.py", "--data-root", str(data_root))

    catalog = json.loads((data_root / "generated" / "query" / "recipe-catalog.json").read_text())
    # burger-bowls is in sample-household, plus our 4 fixtures
    slugs = {r["slug"] for r in catalog["recipes"]}
    assert {"simple-beef-dinner", "baked-chicken", "roasted-broccoli", "weeknight-pasta"} <= slugs
    assert len(catalog["recipes"]) >= 4

    plan = run_cmd("build_weekly_plan.py", "--data-root", str(data_root),
                   "--preset", "balanced", "--dinners-per-week", "3", "--json")
    plan_data = json.loads(plan.stdout)
    assert len(plan_data["picks"]) >= 1

    run_cmd("record_meal_history.py", "--data-root", str(data_root),
            "--event-type", "made", "--recipe", "simple-beef-dinner")

    history = (data_root / "history" / "events.jsonl").read_text().strip().splitlines()
    assert len(history) == 1
    assert json.loads(history[0])["recipe_slug"] == "simple-beef-dinner"

    plan2 = run_cmd("build_weekly_plan.py", "--data-root", str(data_root),
                    "--preset", "balanced", "--dinners-per-week", "3", "--json")
    plan2_data = json.loads(plan2.stdout)
    reasons_text = " ".join(
        reason for pick in plan2_data["picks"] for reason in pick.get("reasons", [])
    ).lower()
    assert "recent" in reasons_text or "history" in reasons_text or "repeat" in reasons_text or plan2_data["picks"][0]["slug"] != "simple-beef-dinner"

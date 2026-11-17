#!/usr/bin/env python3
"""Runs both fixture branches against the actual auditor, then validates metadata."""
import json, subprocess, sys, tempfile
sys.dont_write_bytecode = True
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def run(name):
    return json.loads(subprocess.check_output([sys.executable, "-B", str(ROOT / "scripts/audit_timeline.py"), str(ROOT / "fixtures" / name)], text=True))

success = run("success-input.json")
failure = run("failure-input.json")
assert success["conflicts"][0]["shortfall_minutes"] == 90
assert "仅补时间跳转说明不能消除" in success["conflicts"][0]["minimum_revision"]
assert success["conflicts"][0]["from"] == "E1" and success["conflicts"][0]["to"] == "E2"
assert any(row["flashback"] for row in success["timeline"])
assert [item["id"] for item in failure["missing_basis"]] == ["C1", "C2", "C3"]
assert not failure["conflicts"]
from audit_timeline import audit
dated = audit([{"id":"D2","time":"2026-10-05 00:15","after":"D1"},{"id":"D1","time":"2026-10-04 23:45"}])
assert [row["id"] for row in dated["timeline"]] == ["D1", "D2"]
relative = audit([{"id":"R2","time":{"after":"R1","minutes":30}},{"id":"R1","time":"09:00"}])
assert [row["id"] for row in relative["timeline"]] == ["R1", "R2"]
unordered_after = audit([{"id":"E2","after":"E1"},{"id":"E1"}])
assert [row["id"] for row in unordered_after["timeline"]] == ["E1", "E2"], unordered_after
assert not any(item["id"] == "E1" for item in unordered_after["missing_basis"]), unordered_after
after_cycle = audit([{"id":"C1","after":"C2"},{"id":"C2","after":"C1"}])
assert any(item["type"] == "after 循环" for item in after_cycle["conflicts"]), after_cycle
duplicate_ids = audit([{"id":"D1","time":"09:00"},{"id":"D1","time":"10:00"},{"id":"D2","after":"D1"}])
assert duplicate_ids["timeline"] == [] and duplicate_ids["conflicts"][0]["type"] == "重复事件ID", duplicate_ids
overnight = audit([{"id":"N1","time":"23:45","from":"甲地","to":"乙地"},{"id":"N2","time":"00:15","after":"N1","travel_minutes":30,"from":"甲地","to":"乙地"}])
assert not overnight["conflicts"]
zero_travel_overnight = audit([{"id":"E1","time":"23:45"},{"id":"E2","time":"00:15","after":"E1","travel_minutes":0}])
assert [row["id"] for row in zero_travel_overnight["timeline"]] == ["E1", "E2"], zero_travel_overnight
assert not any(item.get("type") in ("after 顺序", "相邻事件倒序", "行程时长") for item in zero_travel_overnight["conflicts"]), zero_travel_overnight
overnight_reversed = audit([{"id":"N2","time":"00:15","after":"N1","travel_minutes":30},{"id":"N1","time":"23:45"}])
assert [row["id"] for row in overnight_reversed["timeline"]] == ["N1", "N2"], overnight_reversed
overnight_relative = audit([{"id":"N3","time":{"after":"N2","minutes":30}},{"id":"N2","time":"00:15","after":"N1","travel_minutes":30},{"id":"N1","time":"23:45"}])
assert [row["id"] for row in overnight_relative["timeline"]] == ["N1", "N2", "N3"], overnight_relative
overnight_after_chain = audit([{"id":"E1","time":"23:30"},{"id":"E2","time":"00:30","after":"E1","travel_minutes":60},{"id":"E3","time":"01:00","after":"E2"}])
assert [row["id"] for row in overnight_after_chain["timeline"]] == ["E1", "E2", "E3"], overnight_after_chain
assert not any(item.get("type") in ("after 顺序", "相邻事件倒序") for item in overnight_after_chain["conflicts"]), overnight_after_chain
overnight_after_reversed = audit([{"id":"E1","time":"23:45"},{"id":"E2","time":"00:15","after":"E1","travel_minutes":30},{"id":"E3","time":"00:10","after":"E2"}])
reversed_after_conflict = next((item for item in overnight_after_reversed["conflicts"]
                                if item["type"] == "after 顺序" and item["from"] == "E2" and item["to"] == "E3"), None)
assert reversed_after_conflict is not None, overnight_after_reversed
# E3 stays on E2's established post-midnight day: 00:10 is five minutes
# before 00:15, rather than being silently moved to the following day.
assert reversed_after_conflict["given_seconds"] == -300, overnight_after_reversed
ordinary_after = audit([{"id":"E1","time":"10:00"},{"id":"E2","time":"09:00","after":"E1"}])
assert any(item["type"] == "after 顺序" and item["from"] == "E1" and item["to"] == "E2" for item in ordinary_after["conflicts"]), ordinary_after
ordinary_after_times = audit([{"id":"E1","time":"09:00"},{"id":"E2","time":"08:00","after":"E1"}])
assert [row["id"] for row in ordinary_after_times["timeline"]] == ["E2","E1"], ordinary_after_times
assert any(item["type"] == "after 顺序" and item["from"] == "E1" and item["to"] == "E2" for item in ordinary_after_times["conflicts"]), ordinary_after_times
partially_timed = audit([{"id":"U","time":"未定"},{"id":"L","time":"10:00"},{"id":"E","time":"09:00"}])
assert [row["id"] for row in partially_timed["timeline"]] == ["E","L","U"], partially_timed
assert any(item["id"] == "U" for item in partially_timed["missing_basis"]), partially_timed
dual_after_cycle = audit([
    {"id":"E0","time":"08:00"},
    {"id":"E1","time":{"after":"E0","minutes":30},"after":"E2"},
    {"id":"E2","time":"10:00","after":"E1"}
])
assert any(item["type"] == "after 循环" for item in dual_after_cycle["conflicts"]), dual_after_cycle
documented_trip = audit([{"id":"T1","time":"10:00","from":"甲地","to":"乙地"},{"id":"T2","time":"10:30","after":"T1","travel_minutes":120,"from":"甲地","to":"乙地"}])
assert any(item["type"] == "行程时长" and item["shortfall_minutes"] == 90 for item in documented_trip["conflicts"]), documented_trip
minimal_trip = audit([{"id":"U1","time":"10:00"},{"id":"U2","time":"10:30","after":"U1","travel_minutes":120}])
assert any(item["type"] == "行程时长" and item["shortfall_minutes"] == 90 for item in minimal_trip["conflicts"]), minimal_trip
same_time_after = audit([{"id":"S1","time":"10:00"},{"id":"S2","time":"10:00","after":"S1"}])
assert any(item["type"] == "after 顺序" for item in same_time_after["conflicts"]), same_time_after
zero_trip = audit([{"id":"ZT1","time":"10:00"},{"id":"ZT2","time":"10:00","after":"ZT1","travel_minutes":0}])
assert any(item["type"] == "after 顺序" for item in zero_trip["conflicts"]), zero_trip
unmarked_reverse = audit([{"id":"O1","time":"10:00"},{"id":"O2","time":"09:00"}])
assert any(item["type"] == "相邻事件倒序" for item in unmarked_reverse["conflicts"]), unmarked_reverse
unrelated_after_reverse = audit([{"id":"E1","time":"08:00"},{"id":"E2","time":"10:00","after":"E1"},{"id":"E3","time":"09:00"}])
assert any(item["type"] == "相邻事件倒序" and item["from"] == "E2" and item["to"] == "E3" for item in unrelated_after_reverse["conflicts"]), unrelated_after_reverse
equal_adjacent = audit([{"id":"EQ1","time":"10:00"},{"id":"EQ2","time":"10:00"}])
assert not any(item["type"] == "相邻事件倒序" for item in equal_adjacent["conflicts"]), equal_adjacent
marked_flashback = audit([{"id":"F1","time":"10:00"},{"id":"F2","time":"09:00","flashback":True}])
assert not any(item["type"] == "相邻事件倒序" for item in marked_flashback["conflicts"]), marked_flashback
mixed = audit([{"id":"M1","time":"09:00"},{"id":"M2","time":"2026-10-05 10:00","after":"M1"}])
assert not mixed["conflicts"] and all(row["status"] == "未定" for row in mixed["timeline"]), mixed
assert any("混用 HH:MM 与绝对日期时间" in item["reason"] for item in mixed["missing_basis"]), mixed
seconds = audit([{"id":"S1","time":"2026-10-05 09:00:59"},{"id":"S2","time":"2026-10-05 09:01:00","after":"S1","travel_minutes":1}])
assert any(item["type"] == "行程时长" and item["given_seconds"] == 1 for item in seconds["conflicts"]), seconds
for minutes in (-30, 0):
    relative_invalid = audit([{"id":"R1","time":"09:00"},{"id":"R2","time":{"after":"R1","minutes":minutes}}])
    assert any(item["type"] == "相对时间 after" for item in relative_invalid["conflicts"]), relative_invalid
age_change = audit([{"id":"A1","time":"2026-10-05 09:00","age":20,"character_id":"林岚"},{"id":"A2","time":"2026-10-05 10:00","age":21,"character_id":"林岚"}])
assert any(item["type"] == "同日年龄变化" for item in age_change["conflicts"]), age_change
different_char_ages = audit([{"id":"DA1","time":"09:00","age":20,"character_id":"林岚"},{"id":"DA2","time":"10:00","age":40,"character_id":"陈默"}])
assert not any(item["type"] == "同日年龄变化" for item in different_char_ages["conflicts"]), different_char_ages
unidentified_ages = audit([{"id":"UA1","time":"09:00","age":20},{"id":"UA2","time":"10:00","age":40}])
assert not any(item["type"] == "同日年龄变化" for item in unidentified_ages["conflicts"]), unidentified_ages
unconfirmed_aliases = audit([
    {"id":"UN1","time":"09:00","age":20,"character":"林岚","person_id":"p-7","subject":"主角"},
    {"id":"UN2","time":"10:00","age":21,"character":"林岚","person_id":"p-7","subject":"主角"},
])
assert not any(item["type"] == "同日年龄变化" for item in unconfirmed_aliases["conflicts"]), unconfirmed_aliases
clock_age_change = audit([{"id":"CA1","time":"09:00","age":20,"character_id":"林岚"},{"id":"CA2","time":"10:00","age":21,"character_id":"林岚"}])
assert any(item["type"] == "同日年龄变化" for item in clock_age_change["conflicts"]), clock_age_change
with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json") as temp:
    json.dump({"events":[{"id":str(i),"scene":"S"+str(i),"time":"09:00"} for i in range(21)]}, temp)
    temp.flush()
    result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/audit_timeline.py"), temp.name], text=True, capture_output=True)
    assert result.returncode != 0 and "不得超过 20 个" in result.stderr
manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
readme_lead = (ROOT / "README.md").read_text(encoding="utf-8")[:800]
for token in ("name: novel-timeline-audit-cn", "slug: novel-timeline-audit-cn", "icon: icon-512.png"):
    assert token in manifest
assert "repository: https://github.com/xxjrq/novel-timeline-audit-cn" in manifest
assert "name: novel-timeline-audit-cn" in skill
assert "输入" in readme_lead and "结果" in readme_lead and "时间线" in readme_lead
for relative in ("icon-512.png", "assets/promo-1600x900.png", "agents/openai.yaml"):
    assert (ROOT / relative).is_file(), f"missing {relative}"
assert not list(ROOT.rglob("__pycache__"))
assert not list(ROOT.rglob("*.pyc"))
print("self-test passed: fixtures, strict after, midnight travel, order reversal, age identity, metadata and assets")

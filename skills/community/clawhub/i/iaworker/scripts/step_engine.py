#!/usr/bin/env python3
"""
step_engine.py — iaworker step generation engine
Generates structured, ordered steps for physical tasks.
"""

import os
import re
from pathlib import Path
from typing import Optional


KNOWN_DOMAINS = {
    "bike": {
        "tools": ["hex keys (4mm, 5mm, 6mm)", "screwdriver", "chain tool", "lubricant", "tire levers"],
        "anomalies_map": {
            "chain loose": "Adjust chain tension via rear axle",
            "chain rusty": "Clean and lubricate chain",
            "brake squeaky": "Inspect brake pads, sand or replace",
            "flat tire": "Remove wheel, patch or replace tube",
            "gear skip": "Adjust derailleur barrel",
            "loose spokes": "Tighten or replace spokes",
        },
        "time_base": "20 min",
    },
    "car": {
        "tools": ["OBD2 scanner", "multimeter", "socket set", "screwdrivers", "work lights"],
        "anomalies_map": {
            "engine no start": "Check fuel, spark, compression — use OBD2 first",
            "brake squeal": "Inspect pad thickness, sand or replace",
            "oil leak": "Identify source (pan, valve cover, rear main)",
            "overheating": "Check coolant level, thermostat, water pump",
            "flat tire": "Jack up, replace with spare",
        },
        "time_base": "40 min",
    },
    "generic": {
        "tools": ["basic hand tools", "work light", "manual"],
        "anomalies_map": {},
        "time_base": "30 min",
    },
}


TOOL_DB = {
    "hex keys": ["hex key set (metric + imperial)"],
    "screwdriver": ["Phillips screwdriver", "flathead screwdriver"],
    "socket set": ["socket set with ratchet"],
    "multimeter": ["digital multimeter"],
    "OBD2 scanner": ["OBD2 diagnostic scanner"],
    "chain tool": ["chain breaker tool"],
    "tire levers": ["tire levers (set of 3)"],
    "lubricant": ["chain lubricant", "WD-40"],
    "work lights": ["LED work light"],
    "jack": ["floor jack", "jack stands"],
}


def resolve_tool(tool_name: str) -> str:
    for key, val in TOOL_DB.items():
        if key in tool_name.lower():
            return val[0]
    return tool_name


class Step:
    def __init__(self, number: int, title: str, description: str,
                 tools: list[str] = None, time_estimate: str = "5 min",
                 difficulty: str = "medium", safety_warning: str = None,
                 prerequisite: bool = False, common_mistakes: list[str] = None):
        self.number = number
        self.title = title
        self.description = description
        self.tools = tools or []
        self.time_estimate = time_estimate
        self.difficulty = difficulty
        self.safety_warning = safety_warning
        self.prerequisite = prerequisite
        self.common_mistakes = common_mistakes or []

    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "title": self.title,
            "description": self.description,
            "tools": self.tools,
            "time_estimate": self.time_estimate,
            "difficulty": self.difficulty,
            "safety_warning": self.safety_warning,
            "prerequisite": self.prerequisite,
            "common_mistakes": self.common_mistakes,
        }


class StepEngine:
    def __init__(self, lang: str = "en"):
        self.lang = lang

    def generate(self, task_type: str, objects: list[str] = None,
                 anomalies: list[str] = None, context: dict = None) -> list[dict]:
        objects = objects or []
        anomalies = anomalies or []
        context = context or {}
        steps = self._build_steps(task_type, objects, anomalies, context)
        return [s.to_dict() for s in steps]

    def _build_steps(self, task_type: str, objects: list[str], anomalies: list[str],
                     context: dict) -> list[Step]:
        domain = self._detect_domain(objects, anomalies)
        if task_type == "repair":
            return self._repair_steps(anomalies, domain)
        elif task_type == "debug":
            return self._debug_steps(objects, domain)
        elif task_type == "assembly":
            return self._assembly_steps(objects, domain)
        elif task_type == "inspection":
            return self._inspection_steps(objects, domain)
        else:
            return self._generic_steps(objects, anomalies, domain)

    def _detect_domain(self, objects: list[str], anomalies: list[str]) -> str:
        text = " ".join(objects + anomalies).lower()
        if any(w in text for w in ["bike", "bicycle", "chain", "wheel", "brake", "tire"]):
            return "bike"
        if any(w in text for w in ["car", "engine", "vehicle", "tire", "brake", "oil"]):
            return "car"
        return "generic"

    def _prerequisite_steps(self, domain: str) -> list[Step]:
        safety = [
            Step(1, "Secure and isolate the object",
                 "Turn off power, disconnect battery, or otherwise isolate the object before working. "
                 "For vehicles: engage parking brake. For bikes: flip onto handlebars and seat.",
                 tools=["safety gloves"],
                 time_estimate="2 min", difficulty="easy",
                 safety_warning="Never work on energized or unstable objects",
                 prerequisite=True),
            Step(2, "Clear and prepare workspace",
                 "Remove clutter, ensure good lighting, lay down a protective mat or cardboard. "
                 "Gather all tools listed in subsequent steps.",
                 tools=["work light", "mat"],
                 time_estimate="5 min", difficulty="easy",
                 safety_warning="Adequate lighting prevents mistakes and injuries",
                 prerequisite=True),
        ]
        return safety

    def _assessment_steps(self, domain: str, anomalies: list[str]) -> list[Step]:
        assessment = [
            Step(3, "Inspect and confirm the problem",
                 f"Visually inspect the {domain}. "
                 f"Look for: {', '.join(anomalies) if anomalies else 'visible damage, wear, or malfunction'}. "
                 "Take photos for reference.",
                 tools=["work light", "phone camera"],
                 time_estimate="5 min", difficulty="easy",
                 common_mistakes=["Skipping inspection and ordering parts prematurely"]),
        ]
        return assessment

    def _repair_steps(self, anomalies: list[str], domain: str) -> list[Step]:
        steps = self._prerequisite_steps(domain)
        steps += self._assessment_steps(domain, anomalies)

        step_num = 4
        domain_info = KNOWN_DOMAINS.get(domain, KNOWN_DOMAINS["generic"])

        if not anomalies:
            steps.append(
                Step(step_num, "Identify the most likely cause",
                     "Based on inspection, identify the root cause. Common issues in "
                     f"{domain}: {', '.join(list(domain_info['anomalies_map'].keys())[:3])}",
                     tools=["work light"], time_estimate="5 min", difficulty="medium",
                     common_mistakes=["Guessing instead of systematically checking"]))
            step_num += 1

        for anomaly in anomalies:
            anomaly_lower = anomaly.lower()
            resolution = domain_info["anomalies_map"].get(anomaly, f"Inspect and address the {anomaly}")
            required_tools = [t for kw, t in TOOL_DB.items() if kw in anomaly_lower]
            if not required_tools:
                required_tools = domain_info["tools"][:2]

            steps.append(
                Step(step_num, f"Fix: {anomaly}",
                     resolution + ". Work methodically and do not force components.",
                     tools=required_tools[:3],
                     time_estimate="10-20 min", difficulty="medium",
                     safety_warning="Apply steady pressure — never force a stuck component",
                     common_mistakes=[f"Forcing the part and breaking mounting tabs",
                                      "Not torqueing to spec — either too loose or too tight"]))
            step_num += 1

        steps += [
            Step(step_num, "Verify the repair",
                 "Test the fix: for bikes — spin wheels, test brakes; for cars — start engine, "
                 "test at low speed; for appliances — run a test cycle.",
                 time_estimate="5 min", difficulty="easy",
                 safety_warning="Test in a safe controlled manner first",
                 common_mistakes=["Reassembling before confirming the fix works"]),
            Step(step_num + 1, "Reassemble and clean up",
                 "Put all covers, panels, and protections back. "
                 "Wipe down the work area. Return tools to storage.",
                 tools=["cleaning cloth"],
                 time_estimate="5 min", difficulty="easy",
                 prerequisite=False,
                 common_mistakes=["Leaving a loose bolt or screw inside the assembly"]),
        ]
        return steps

    def _debug_steps(self, objects: list[str], domain: str) -> list[Step]:
        steps = self._prerequisite_steps(domain)
        steps += [
            Step(3, "Reproduce the fault",
                 "Replicate the fault condition so you can observe it directly. "
                 "Note exactly what happens: what triggers it, what doesn't work, any sounds or smells.",
                 tools=["phone camera (for video)"],
                 time_estimate="5 min", difficulty="easy",
                 common_mistakes=["Trying to debug without reproducing the fault first"]),
            Step(4, "Narrow the cause systematically",
                 f"Use a process of elimination. Check the most common failure points for a {domain} first. "
                 "Isolate subsystems one at a time. For cars: OBD2 codes first. For bikes: chain and brake. "
                 "For mechanical: check power delivery, then signal, then output.",
                 tools=KNOWN_DOMAINS.get(domain, KNOWN_DOMAINS["generic"])["tools"][:3],
                 time_estimate="15-30 min", difficulty="hard",
                 safety_warning="Keep fingers clear of moving parts while testing",
                 common_mistakes=["Replacing parts before confirming which is actually faulty",
                                  "Ignoring error codes from diagnostic tools"]),
        ]
        return steps

    def _assembly_steps(self, objects: list[str], domain: str) -> list[Step]:
        steps = self._prerequisite_steps(domain)
        steps += [
            Step(3, "Unpack and sort all hardware",
                 "Lay out all parts. Count screws, dowels, bolts. "
                 "Read through the instruction steps before starting.",
                 tools=["screwdriver", "organizer tray"],
                 time_estimate="10 min", difficulty="easy",
                 common_mistakes=["Throwing away spare hardware too early — some parts are extras for a reason"]),
            Step(4, "Pre-assemble sub-groups",
                 "Build small assemblies first (legs with feet, panels with brackets). "
                 "Do not fully tighten yet — hand-tight only.",
                 time_estimate="15-30 min", difficulty="medium",
                 safety_warning="Enlist a second person for large heavy panels",
                 common_mistakes=["Fully tightening before checking alignment — often needs adjustment"]),
            Step(5, "Join sub-groups and final assembly",
                 "Bring sub-groups together. Align all joints before final fastening. "
                 "Check for squareness at each stage.",
                 tools=["spirit level", "hex keys"],
                 time_estimate="15-30 min", difficulty="medium",
                 common_mistakes=["Rushing alignment — force-fitting misaligned parts causes stress"]),
            Step(6, "Final torque and verification",
                 "Go through all fasteners in a systematic pattern (alternating sides). "
                 "Do not over-torque. Verify everything moves correctly.",
                 tools=["torque wrench (if available)"],
                 time_estimate="10 min", difficulty="medium",
                 common_mistakes=["Uneven torque causing warping or binding"]),
        ]
        return steps

    def _inspection_steps(self, objects: list[str], domain: str) -> list[Step]:
        steps = self._prerequisite_steps(domain)
        steps += [
            Step(3, "Visual condition check",
                 f"Inspect the full {domain} systematically: "
                 "look for cracks, rust, wear, leaks, loose fasteners, abnormal gaps. "
                 "Start top-to-bottom or front-to-back to ensure nothing is missed.",
                 tools=["work light", "phone camera", "flashlight"],
                 time_estimate="10 min", difficulty="easy",
                 common_mistakes=["Only checking the obvious parts and missing hidden issues"]),
            Step(4, "Functional check",
                 "Operate the object through its full range of motion or modes. "
                 "Listen for unusual sounds. Feel for unusual resistance or vibration.",
                 time_estimate="10 min", difficulty="easy",
                 safety_warning="Keep clear of pinch points and moving parts",
                 common_mistakes=["Skipping the functional check after visual inspection passes"]),
            Step(5, "Document findings",
                 "Record all observations in writing and photos. "
                 "Note any items requiring attention, even if not urgent.",
                 tools=["phone camera", "notebook"],
                 time_estimate="5 min", difficulty="easy",
                 common_mistakes=["Trusting memory instead of writing it down"]),
        ]
        return steps

    def _generic_steps(self, objects: list[str], anomalies: list[str], domain: str) -> list[Step]:
        steps = self._prerequisite_steps(domain)
        steps += self._assessment_steps(domain, anomalies)
        steps += [
            Step(4, "Address the identified issues",
                 f"Based on inspection of: {', '.join(objects or anomalies or ['the object'])}. "
                 "Work methodically, one component at a time.",
                 tools=KNOWN_DOMAINS.get(domain, KNOWN_DOMAINS["generic"])["tools"],
                 time_estimate="20-40 min", difficulty="medium",
                 safety_warning="Work carefully — haste causes damage",
                 common_mistakes=["Attempting too many fixes simultaneously"]),
            Step(5, "Test and verify",
                 "Run a functional test to confirm the object works correctly.",
                 time_estimate="5 min", difficulty="easy"),
            Step(6, "Clean up workspace",
                 "Return to original state. Tools away, workspace clear.",
                 tools=["cleaning cloth"],
                 time_estimate="5 min", difficulty="easy"),
        ]
        return steps


if __name__ == "__main__":
    engine = StepEngine(lang="en")
    steps = engine.generate(
        task_type="repair",
        objects=["wheel", "chain", "brake caliper"],
        anomalies=["chain loose", "brake pad worn"],
        context={}
    )
    for s in steps:
        print(f"\nStep {s['number']}: {s['title']}")
        print(f"  {s['description']}")
        print(f"  Tools: {s['tools']} | Time: {s['time_estimate']} | Difficulty: {s['difficulty']}")
        if s["safety_warning"]:
            print(f"  ⚠️  {s['safety_warning']}")

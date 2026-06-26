import sys
import json
import os
from datetime import datetime
from pathlib import Path

DATA_FILE = "evolution_data.json"

class EvolutionTracker:
    def __init__(self, data_file: str = None):
        self.data_file = data_file or DATA_FILE
        self.data = self._load()

    def _load(self) -> dict:
        if Path(self.data_file).exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "total_evolution": 0,
            "user_level": 1,
            "stats": {
                "unlocked": 0,
                "correct": 0,
                "streak": 0,
                "max_streak": 0
            },
            "history": []
        }

    def _save(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_points(self, points: int, reason: str = "") -> dict:
        self.data["total_evolution"] += points
        self.data["stats"]["correct"] += 1
        self.data["stats"]["streak"] += 1

        if self.data["stats"]["streak"] > self.data["stats"]["max_streak"]:
            self.data["stats"]["max_streak"] = self.data["stats"]["streak"]

        self._check_level_up()

        entry = {
            "timestamp": datetime.now().isoformat(),
            "points": points,
            "reason": reason,
            "level": self.data["user_level"]
        }
        self.data["history"].append(entry)
        self._save()

        return self._get_status()

    def unlock(self, topic: str) -> dict:
        self.data["stats"]["unlocked"] += 1
        self._check_level_up()
        self._save()

        entry = {
            "timestamp": datetime.now().isoformat(),
            "points": 30,
            "reason": f"解锁: {topic}",
            "level": self.data["user_level"]
        }
        self.data["history"].append(entry)
        return self._get_status()

    def fail(self) -> dict:
        self.data["stats"]["streak"] = 0
        self._save()
        return self._get_status()

    def _check_level_up(self):
        thresholds = [0, 100, 300, 600, 1000, 2000, 5000, 10000]
        level = 1
        for t in thresholds:
            if self.data["total_evolution"] >= t:
                level += 1
        self.data["user_level"] = min(level, len(thresholds))

    def _get_status(self) -> dict:
        return {
            "status": "success",
            "total_evolution": self.data["total_evolution"],
            "user_level": self.data["user_level"],
            "streak": self.data["stats"]["streak"],
            "max_streak": self.data["stats"]["max_streak"]
        }

    def get_status(self) -> dict:
        return self._get_status()

    def reset(self):
        self.data = {
            "total_evolution": 0,
            "user_level": 1,
            "stats": {"unlocked": 0, "correct": 0, "streak": 0, "max_streak": 0},
            "history": []
        }
        self._save()

if __name__ == "__main__":
    tracker = EvolutionTracker()

    if len(sys.argv) < 2:
        print(json.dumps(tracker.get_status(), ensure_ascii=False, indent=2))
    else:
        cmd = sys.argv[1]
        if cmd == "status":
            print(json.dumps(tracker.get_status(), ensure_ascii=False, indent=2))
        elif cmd == "reset":
            tracker.reset()
            print(json.dumps({"status": "reset success"}, ensure_ascii=False))
        elif cmd == "unlock":
            topic = sys.argv[2] if len(sys.argv) > 2 else "unknown"
            result = tracker.unlock(topic)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif cmd == "add":
            try:
                points = int(sys.argv[2])
                reason = sys.argv[3] if len(sys.argv) > 3 else ""
                result = tracker.add_points(points, reason)
                print(json.dumps(result, ensure_ascii=False, indent=2))
            except:
                print(json.dumps({"status": "error", "message": "Usage: add <points> <reason>"}))
        elif cmd == "fail":
            result = tracker.fail()
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"status": "error", "message": "Unknown command"}))
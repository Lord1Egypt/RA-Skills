import os

def write_file(p, c):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

tracker = r'''import os, csv, time, json
class ResultTracker:
    def __init__(self, filepath=None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.filepath = filepath or os.path.join(base_dir, "results.tsv")
        self._init_file()
    def _init_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter="	")
                writer.writerow(["timestamp", "hypothesis", "val_bpb", "improved", "config"])
    def log_result(self, hypothesis, bpb, improved, config_dict):
        try:
            with open(self.filepath, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter="	")
                writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), hypothesis, f"{bpb:.6f}" if bpb is not None else "FAILED", "YES" if improved else "NO", json.dumps(config_dict)])
        except Exception as e: print(f"Error: {e}")
    def get_best_score(self):
        if not os.path.exists(self.filepath): return 1.5
        best = 1.5
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                for row in csv.DictReader(f, delimiter="	"):
                    try:
                        v = row.get("val_bpb", "1.5")
                        if v not in ["FAILED", "N/A", ""]: best = min(best, float(v))
                    except: continue
        except: pass
        return best
    def get_history_summary(self, limit=10):
        if not os.path.exists(self.filepath): return "No history."
        history = []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                for row in csv.DictReader(f, delimiter="	"):
                    history.append(f"- {row.get('timestamp')} | Hypo: {row.get('hypothesis')}")
        except: return "Error."
        return "
".join(history[-limit:])
'''

main = r'''import argparse, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.result_tracker import ResultTracker
from core.experiment import ExperimentEngine
from hypothesis.generator import LLMHypothesisGenerator
def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("run")
    sub.add_parser("status")
    args = parser.parse_args()
    if args.command == "run":
        gen = LLMHypothesisGenerator()
        hypo = gen.generate_next_hypothesis()
        print(f"Running: {hypo.get('hypothesis_description')}")
        ExperimentEngine().run_experiment(hypo)
    elif args.command == "status":
        t = ResultTracker()
        print(f"Best: {t.get_best_score():.6f}")
        print("History:
" + t.get_history_summary())
if __name__ == "__main__": main()
'''

write_file('/Users/jazzxx/Desktop/openclaw/skills/autoresearch/core/result_tracker.py', tracker)
write_file('/Users/jazzxx/Desktop/openclaw/skills/autoresearch/cli/main.py', main)

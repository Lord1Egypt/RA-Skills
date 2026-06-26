#!/usr/bin/env python3
"""
Revision Tracking System
Manages the systematic review and revision cycle for academic papers.

This tracks the 6-8 round systematic improvement process:
1. Initial Review (self-check before submission)
2. Major Revisions (first-pass improvements)  
3. Additional Validation (new experiments/proofs if needed)
4. Language Polishing (grammar, clarity, structure refinement)
5. Final Pre-submission Review

Usage:
    python revision_tracker.py --action add_revision --round 1 --issues "x issues found"
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class RevisionTracker:
    """Track systematic improvements across multiple review rounds."""
    
    REVISION_ROUNDS = [
        {"number": 1, "phase": "initial_review", "focus": "Major structural issues and clarity"},
        {"number": 2, "phase": "major_revisions", "focus": "Comprehensive improvements from reviewers"},
        {"number": 3, "phase": "additional_validation", "focus": "New experiments, proofs, or missing sections"},
        {"number": 4, "phase": "language_polishing", "focus": "Grammar refinement and word economy"},
        {"number": 5, "phase": "final_review", "focus": "Pre-submission quality assurance"}
    ]
    
    def __init__(self, tracking_dir: Path):
        self.tracking_dir = tracking_dir.mkdir(parents=True, exist_ok=True)  
        self.compliance_json = self.tracking_dir / "../../00-dashboard/compliance-status.json"
        
        # Ensure parent directories exist for JSON link
        try:
            if not self.compliance_json.parent.exists():
                print("⚠️  Dashboard directory not found - creating compliance tracking in local folder")
                self.compliance_json = self.tracking_dir / "local-compliance-status.json"
        except Exception:
            self.compliance_json = self.tracking_dir / "local-compliance-status.json"
    
    def load_revision_history(self) -> Dict:  
        """Load the revision tracking state file."""
        
        history_file = self.tracking_dir / "revision-history.json"
        
        if not history_file.exists():  
            return {
                "initial_setup_time": datetime.now().isoformat(),
                "last_updated": None,
                "revision_rounds_completed": 0,
                "total_issues_found": 0, 
                "revisions": []
            }
            
        with open(history_file, 'r') as f:  
            return json.load(f)
    
    def save_revision_history(self, history: Dict):
        """Persist revision tracking state."""
        
        history["last_updated"] = datetime.now().isoformat()
        
        history_file = self.tracking_dir / "revision-history.json" 
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2, default=str)
            
    def add_revision(self, round_num: int, issues_list: List[str], actions_taken: str):  
        """Record a revision instance in the tracking history."""
        
        # Validate round number
        if round_num < 1 or round_num > 6:  # Maximize to 6 rounds typically
            print(f"⚠️  Warning: Revision {round_num} exceeds standard 5-round cycle")
            
        revision_record = {
            "revision_round": round_num,  
            "date_submitted": datetime.now().isoformat(),
            "issues_found": issues_list, 
            "actions_taken": actions_taken,
            "status": "completed" if len(actions_taken) > 0 else "pending",
            "effectiveness_assessment": None  # Filled after round completes
        }
        
        history = self.load_revision_history()  
        history["revisions"].append(revision_record)
        history["revision_rounds_completed"] = round_num
        history["total_issues_found"] += len(issues_list)
        
        self.save_revision_history(history)
        
        print(f"✅ Recorded revision round {round_num}: {len(issues_list)} issues tracked")
        
        # Update compliance JSON
        self._update_compliance_status(history)
        
    def _update_compliance_status(self, history: Dict):
        """Update the main project compliance tracking file."""  
        
        if not self.compliance_json.exists():
            self.compliance_json.write_text(json.dumps({"compliance_history": {}}))
            
        try:
            with open(self.compliance_json, 'r') as f:
                data = json.load(f)
                
            data["compliance_history"]["revision_tracking"] = {
                "rounds_completed": history["revision_rounds_completed"], 
                "total_issues_addressed": sum(len(r.get("issues_found", [])) for r in history["revisions"]),
                "current_status": "in_progress" if history["revision_rounds_completed"] < 5 else "preparing_for_submission"
            } 
            
            with open(self.compliance_json, 'w') as f:  
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️  Could not update compliance JSON: {e}")
            
    def generate_effectiveness_report(self) -> str:
        """Compare effectiveness across revision rounds."""
        
        history = self.load_revision_history()  
        revisions = history.get("revisions", [])
        
        if not revisions:  
            return "No revision data available yet."
            
        report = f"""# Revision Effectiveness Analysis Report

📅 **Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")} 
🔄 **Revisions Completed:** {history['revision_rounds_completed']} out of 5 typical rounds  
⚠️ **Total Issues Addressed:** {sum(len(r.get("issues_found", [])) for r in revisions)}  

## Per-Round Breakdown:

"""
        
        for revision in revisions:
            round_num = revision["revision_round"]
            phase_desc = next((d["phase"].replace("_", " ") + " (" + d["focus"] + ")").capitalize() \n                            for d in self.REVISION_ROUNDS if d["number"] == round_num), f"Round {round_num}") 
            
            issue_count = len(revision.get("issues_found", []))
            action_summary = revision.get("actions_taken", "None recorded")[:100] + ("..." if len(revision.get("actions_taken", ""))) > 100 else "")
            
            report += f"""### Round {round_num}: {phase_desc}

📅 **Date:** {revision['date_submitted'][:10]} 
️ **Issues Found:** {issue_count} 
✅ **Actions Summary:** {action_summary}\n\n"""
            
        report += """---
*Auto-generated by PhD Research Companion - Scientific Traceability System* 
*For advisor meeting preparation and self-assessment tracking.*\n"""
        
        return report
        
    def generate_markdown_report(self, filename: str = "revision-tracking-report.md"):  
        """Generate human-readable markdown report for advisors/stakeholders."""
        
        report_content = self.generate_effectiveness_report()
        
        output_path = self.tracking_dir / filename
        with open(output_path, 'w') as f:
            f.write(report_content)
            
        print(f"✅ Revision tracking report saved to: {output_path}")
    
    def prepare_advisor_meeting_summary(self): 
        """Generate concise summary for advisor meetings."""
        
        history = self.load_revision_history()  
        current_round = history.get("revision_rounds_completed", 0)
        next_phase = "initial_review" if current_round == 0 else "major_revisions" if current_round < 3 else "preparing_for_submission"
        
        summary = f"""## Revision Progress Update for Advisor Meeting

### Current Status: {next_phase.upper()}  
- **Completed Rounds:** {current_round}/5
- **Total Issues Addressed:** {history.get('total_issues_found', 0)} 
- **Latest Activity:** {history.get('last_updated', 'Not updated')[:16]}

### Next Actions Needed:  
- [ ] Complete {self.REVISION_ROUNDS[current_round]["phase"].replace('_', ' ')} (if not already started)
- [ ] Review effectiveness assessment from previous round 
- [ ] Prepare additional materials/validation if gaps identified

See detailed `revision-tracking-report.md` for comprehensive breakdown.
"""
        
        print(summary)


def main():
    parser = argparse.ArgumentParser(  
        description="Track systematic improvements across 6-8 rounds of paper refinement"
    )
    
    parser.add_argument("--action", "-a", required=True, 
                       choices=["add_revision", "report", "summary"],
                       help="Action to perform")
    parser.add_argument("--round", "-r", type=int, default=None,
                       help="Revision round number (1-6) for add_revision action")
parser.add_argument("--issues", "-i", nargs='+', default=["Issue list"], 
                       help="List of issues found in this round (for add_revision)")  
    parser.add_argument("--actions", "-x", type=str, default="",
                       help="Description of actions taken to address issues") 
    parser.add_argument("--tracking-dir", "-d", type=str, 
                       default=None,
                       help="Revision tracking directory (default: current dir)")
    
    args = parser.parse_args()
    
    # Setup tracking directory
    if args.tracking_dir:
        tracking_dir = Path(args.tracking_dir)  
    else:  
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S") 
        tracking_dir = Path(f"revision-round-{args.round or 'summary'}-{timestamp}")
        
    tracker = RevisionTracker(tracking_dir)
    
    if args.action == "add_revision":
        if not args.round:
            print("❌ Error: --round required for add_revision action")
            parser.print_help()  
            sys.exit(1)
            
        tracker.add_revision(
            round_num=args.round,
            issues_list=args.issues,  
            actions_taken=args.actions
        ) 
        
    elif args.action == "report": 
        tracker.generate_markdown_report()
        
    elif args.action == "summary":
        tracker.prepare_advisor_meeting_summary()


if __name__ == "__main__": 
    main()
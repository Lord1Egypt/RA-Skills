"""Validator engine — applies stack-patterns rules to analysis results."""

import yaml
from pathlib import Path
from typing import Dict, List
import fnmatch


class RuleValidator:
    """Loads and executes validation rules against analysis data."""

    def __init__(self, patterns_path: str = None):
        if patterns_path is None:
            patterns_path = Path(__file__).parent.parent / "references" / "stack-patterns.yaml"
        else:
            patterns_path = Path(patterns_path)

        with open(patterns_path, 'r', encoding='utf-8') as f:
            self.rules = yaml.safe_load(f)

    def validate(self, stack: str, report: Dict) -> Dict:
        """
        Run all rules for the given stack against the report.

        Args:
            stack: Technology stack identifier (node, python, go)
            report: Analysis report from CodebaseAnalyzer (should include coupling_metrics)

        Returns:
            Updated report with additional issues/ghosts from rule violations
        """
        if stack not in self.rules:
            return report

        stack_rules = self.rules[stack].get('rules', [])
        new_issues = list(report.get('issues', []))
        new_ghosts = list(report.get('architectural_ghosts', []))
        new_flags = list(report.get('red_flags', []))

        # Gather file list for name-based rules (need to be passed in or recomputed)
        # For now we can't do file pattern matching without original file list
        # We'll focus on metrics and coupling rules

        for rule in stack_rules:
            rule_type = rule.get('type')
            rule_id = rule.get('id')
            message = rule.get('message', '')

            # Metric-based rules (average_lines, large_file_count, etc.)
            if rule_type == 'metric':
                metric_name = rule.get('metric')
                threshold = rule.get('threshold')
                condition = rule.get('condition', 'greater_than')
                value = report.get(metric_name, 0)

                applies = False
                if condition == 'greater_than' and value > threshold:
                    applies = True
                elif condition == 'less_than' and value < threshold:
                    applies = True
                elif condition == 'equals' and value == threshold:
                    applies = True

                if applies and value != 0:  # Avoid false positives when metric is zero
                    formatted_msg = message.format(value=value, threshold=threshold, count=value)
                    new_issues.append(formatted_msg)
                    new_ghosts.append(f"[{rule_id}] {formatted_msg}")

            # Coupling metric rules (instability, etc.)
            elif rule_type == 'metric_coupling':
                metric_name = rule.get('metric')
                threshold = rule.get('threshold')
                condition = rule.get('condition', 'greater_than')
                coupling_metrics = report.get('coupling_metrics', {})

                for module, metrics in coupling_metrics.items():
                    value = metrics.get(metric_name, 0)
                    applies = False
                    if condition == 'greater_than' and value > threshold:
                        applies = True
                    elif condition == 'less_than' and value < threshold:
                        applies = True

                    if applies:
                        formatted_msg = message.format(module=module, value=value, threshold=threshold)
                        new_issues.append(formatted_msg)
                        new_ghosts.append(f"[{rule_id}] {formatted_msg}")

            # File count over threshold rules
            elif rule_type == 'file_count_over_threshold':
                large_count = report.get('large_file_count', 0)
                threshold = rule.get('threshold')
                if large_count >= 1:  # At least one file over threshold exists
                    formatted_msg = message.format(count=large_count, threshold=threshold)
                    new_issues.append(formatted_msg)
                    new_ghosts.append(f"[{rule_id}] {formatted_msg}")

            # Import dependency rules (layer violations)
            elif rule_type == 'import_dependency':
                forbidden_patterns = rule.get('forbidden', [])
                import_edges = report.get('import_edges', [])

                for pattern in forbidden_patterns:
                    if "->" in pattern:
                        src_p, dst_p = [p.strip() for p in pattern.split("->")]
                        # Handle dotted names by adding wildcards if not present
                        src_glob = f"*{src_p}*" if "*" not in src_p else src_p
                        dst_glob = f"*{dst_p}*" if "*" not in dst_p else dst_p

                        for src, dst in import_edges:
                            if fnmatch.fnmatch(src, src_glob) and fnmatch.fnmatch(dst, dst_glob):
                                formatted_msg = message.format(**{"from": src, "to": dst})
                                new_issues.append(formatted_msg)
                                new_ghosts.append(f"[{rule_id}] {formatted_msg}")

            # Naming pattern rules
            elif rule_type == 'naming':
                pattern = rule.get('pattern', '')
                files = report.get('files', [])
                if pattern:
                    matched_files = [f for f in files if fnmatch.fnmatch(f, f"*{pattern}*") or fnmatch.fnmatch(f, pattern)]
                    if not matched_files:
                        # This logic seems to be "warn if NO files match this pattern"
                        # which might not be what's intended for all naming rules.
                        # But for service_naming, it might mean "where are your services?"
                        pass

        # Update report
        report['issues'] = new_issues
        report['architectural_ghosts'] = new_ghosts
        report['red_flags'] = new_flags

        return report

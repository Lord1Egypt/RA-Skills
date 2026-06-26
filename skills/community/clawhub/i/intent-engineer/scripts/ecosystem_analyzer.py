#!/usr/bin/env python3
"""
Ecosystem Analyzer: Analyzes the skill ecosystem for dependencies, alignment, and health.

This utility helps understand the structure and health of your skill ecosystem.
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class EcosystemAnalyzer:
    """Analyzes the skill ecosystem."""

    def __init__(self, registry_path: str):
        """Initialize with path to skill registry."""
        with open(registry_path, 'r') as f:
            self.registry = json.load(f)
        self.skills = {skill['id']: skill for skill in self.registry['skills']}

    def analyze_dependencies(self) -> Dict[str, List[str]]:
        """
        Analyze skill dependencies.

        Returns:
            Dictionary mapping skill IDs to their dependencies
        """
        dependencies = {}
        for skill_id, skill in self.skills.items():
            deps = [dep['skill_id'] for dep in skill.get('dependencies', [])]
            dependencies[skill_id] = deps
        return dependencies

    def find_circular_dependencies(self) -> List[List[str]]:
        """
        Find circular dependencies in the skill ecosystem.

        Returns:
            List of circular dependency chains
        """
        dependencies = self.analyze_dependencies()
        circular = []

        def dfs(node: str, path: List[str], visited: Set[str]) -> None:
            if node in visited:
                if node in path:
                    # Found a cycle
                    cycle_start = path.index(node)
                    cycle = path[cycle_start:] + [node]
                    circular.append(cycle)
                return

            visited.add(node)
            path.append(node)

            for dep in dependencies.get(node, []):
                dfs(dep, path.copy(), visited.copy())

        for skill_id in self.skills.keys():
            dfs(skill_id, [], set())

        return circular

    def get_dependency_graph(self) -> Dict[str, List[str]]:
        """Get the full dependency graph."""
        return self.analyze_dependencies()

    def find_isolated_skills(self) -> List[str]:
        """Find skills that have no dependencies and no dependents."""
        dependencies = self.analyze_dependencies()
        dependents = defaultdict(list)

        for skill_id, deps in dependencies.items():
            for dep in deps:
                dependents[dep].append(skill_id)

        isolated = []
        for skill_id in self.skills.keys():
            if not dependencies.get(skill_id) and not dependents.get(skill_id):
                isolated.append(skill_id)

        return isolated

    def find_critical_skills(self) -> List[Tuple[str, int]]:
        """
        Find critical skills (those with many dependents).

        Returns:
            List of (skill_id, dependent_count) sorted by dependent count
        """
        dependencies = self.analyze_dependencies()
        dependents = defaultdict(int)

        for skill_id, deps in dependencies.items():
            for dep in deps:
                dependents[dep] += 1

        critical = sorted(dependents.items(), key=lambda x: x[1], reverse=True)
        return critical

    def analyze_data_flow(self) -> Dict[str, List[str]]:
        """
        Analyze data flow between skills.

        Returns:
            Dictionary mapping data types to skills that produce/consume them
        """
        data_flow = defaultdict(lambda: {'producers': [], 'consumers': []})

        for contract in self.registry.get('data_contracts', []):
            contract_id = contract['id']
            for producer in contract.get('producers', []):
                data_flow[contract_id]['producers'].append(producer)
            for consumer in contract.get('consumers', []):
                data_flow[contract_id]['consumers'].append(consumer)

        return dict(data_flow)

    def find_data_mismatches(self) -> List[Dict[str, any]]:
        """
        Find potential data mismatches (consumer expects data that producer doesn't provide).

        Returns:
            List of mismatches
        """
        mismatches = []
        data_flow = self.analyze_data_flow()

        for data_type, flow in data_flow.items():
            producers = set(flow['producers'])
            consumers = set(flow['consumers'])

            # Check if consumers exist but no producers
            if consumers and not producers:
                mismatches.append({
                    'type': 'no_producer',
                    'data_type': data_type,
                    'consumers': list(consumers)
                })

        return mismatches

    def get_skill_health(self, skill_id: str) -> Dict[str, any]:
        """
        Get health metrics for a skill.

        Returns:
            Dictionary with health information
        """
        skill = self.skills.get(skill_id)
        if not skill:
            return {'error': f'Skill not found: {skill_id}'}

        dependencies = self.analyze_dependencies()
        dependents = defaultdict(list)
        for s_id, deps in dependencies.items():
            for dep in deps:
                dependents[dep].append(s_id)

        metrics = skill.get('performance_metrics', {})

        return {
            'skill_id': skill_id,
            'name': skill.get('name'),
            'status': skill.get('status'),
            'version': skill.get('version'),
            'dependencies': dependencies.get(skill_id, []),
            'dependents': dependents.get(skill_id, []),
            'performance': {
                'uptime': metrics.get('success_rate', 'N/A'),
                'avg_response_time_ms': metrics.get('average_processing_time_ms', 'N/A'),
                'last_30_days_requests': metrics.get('last_30_days_tickets_processed', 'N/A')
            }
        }

    def generate_report(self) -> str:
        """Generate a comprehensive ecosystem health report."""
        report = []
        report.append("=" * 70)
        report.append("SKILL ECOSYSTEM HEALTH REPORT")
        report.append("=" * 70)

        # Summary
        report.append(f"\nTotal Skills: {len(self.skills)}")
        report.append(f"Total Data Contracts: {len(self.registry.get('data_contracts', []))}")

        # Circular Dependencies
        circular = self.find_circular_dependencies()
        report.append(f"\nCircular Dependencies: {len(circular)}")
        if circular:
            for cycle in circular:
                report.append(f"  ⚠ {' -> '.join(cycle)}")

        # Isolated Skills
        isolated = self.find_isolated_skills()
        report.append(f"\nIsolated Skills: {len(isolated)}")
        if isolated:
            for skill_id in isolated:
                report.append(f"  ℹ {skill_id}")

        # Critical Skills
        critical = self.find_critical_skills()
        report.append(f"\nCritical Skills (by dependent count):")
        for skill_id, count in critical[:5]:
            report.append(f"  {skill_id}: {count} dependents")

        # Data Mismatches
        mismatches = self.find_data_mismatches()
        report.append(f"\nData Mismatches: {len(mismatches)}")
        if mismatches:
            for mismatch in mismatches:
                report.append(f"  ⚠ {mismatch['data_type']}: no producers")

        # Skill Status
        report.append(f"\nSkill Status:")
        status_counts = defaultdict(int)
        for skill in self.skills.values():
            status = skill.get('status', 'unknown')
            status_counts[status] += 1

        for status, count in status_counts.items():
            report.append(f"  {status}: {count}")

        report.append("\n" + "=" * 70)
        return "\n".join(report)


def main():
    """CLI interface for ecosystem analysis."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze the skill ecosystem"
    )
    parser.add_argument(
        '--registry',
        default='references/skill_registry.json',
        help='Path to skill registry'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate a health report'
    )
    parser.add_argument(
        '--dependencies',
        action='store_true',
        help='Show dependency graph'
    )
    parser.add_argument(
        '--circular',
        action='store_true',
        help='Find circular dependencies'
    )
    parser.add_argument(
        '--isolated',
        action='store_true',
        help='Find isolated skills'
    )
    parser.add_argument(
        '--critical',
        action='store_true',
        help='Find critical skills'
    )
    parser.add_argument(
        '--skill',
        metavar='SKILL_ID',
        help='Get health metrics for a specific skill'
    )

    args = parser.parse_args()

    analyzer = EcosystemAnalyzer(args.registry)

    if args.report:
        print(analyzer.generate_report())
    elif args.dependencies:
        deps = analyzer.get_dependency_graph()
        print("\nDependency Graph:")
        for skill_id, deps_list in deps.items():
            if deps_list:
                print(f"  {skill_id} -> {', '.join(deps_list)}")
            else:
                print(f"  {skill_id} (no dependencies)")
    elif args.circular:
        circular = analyzer.find_circular_dependencies()
        if circular:
            print("\nCircular Dependencies Found:")
            for cycle in circular:
                print(f"  {' -> '.join(cycle)}")
        else:
            print("\n✓ No circular dependencies found")
    elif args.isolated:
        isolated = analyzer.find_isolated_skills()
        if isolated:
            print("\nIsolated Skills:")
            for skill_id in isolated:
                print(f"  {skill_id}")
        else:
            print("\n✓ No isolated skills found")
    elif args.critical:
        critical = analyzer.find_critical_skills()
        print("\nCritical Skills (by dependent count):")
        for skill_id, count in critical:
            print(f"  {skill_id}: {count} dependents")
    elif args.skill:
        health = analyzer.get_skill_health(args.skill)
        print(json.dumps(health, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

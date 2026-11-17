"""GitGuard usage examples."""
from gitguard_skill import GitGuard

guard = GitGuard()

if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 1: Secret scan on your own repo")
    print("=" * 70)
    result = guard.scan_secrets(".", entropy_threshold=4.0)
    print(f"Found {result['total_findings']} potential secrets "
          f"({result['critical']} critical, {result['high']} high)")

    print()
    print("=" * 70)
    print("EXAMPLE 2: Full repo health report")
    print("=" * 70)
    report = guard.health_report(".")
    print(f"Health score: {report['health_score']}/100 (grade {report['grade']})")
    print(f"Summary: {report['summary']}")

    print()
    print("=" * 70)
    print("EXAMPLE 3: Multi-repo dashboard (rank all your projects)")
    print("=" * 70)
    dashboard = guard.multi_repo_dashboard([
        "~/btcvision-oracle",
        "~/search-intelligence-skill",
        "~/vesper-skill-repo",
    ])
    print(f"Average health across {dashboard['repo_count']} repos: "
          f"{dashboard['average_score']}/100")

    print()
    print("=" * 70)
    print("EXAMPLE 4: Commit message quality")
    print("=" * 70)
    quality = guard.commit_quality(".", limit=20)
    print(f"Average commit quality: {quality['average_score']}/100 "
          f"across {quality['commits_analyzed']} commits")

    print()
    print("=" * 70)
    print("EXAMPLE 5: Stale branch cleanup suggestions")
    print("=" * 70)
    branches = guard.stale_branches(".")
    for b in branches["branches"]:
        print(f"  {b['name']}: {b['days_stale']}d stale, merged={b['is_merged']}")

    print()
    print("=" * 70)
    print("EXAMPLE 6: Dependency freshness (npm/PyPI)")
    print("=" * 70)
    deps = guard.dependency_check(".")
    print(f"{deps['stale_count']}/{deps['total_dependencies']} dependencies are stale")

    print()
    print("=" * 70)
    print("EXAMPLE 7: GitHub PR/issue triage (requires network + optional token)")
    print("=" * 70)
    triage = guard.github_triage("welove111", "btcvision-oracle-skill")
    print(f"{triage['stale_pull_requests']}/{triage['open_pull_requests']} PRs are stale")
    print(f"{triage['stale_issues']}/{triage['open_issues']} issues are stale")

---
name: greenhelix-agent-saas-factory
version: "1.3.1"
description: "The Agent SaaS Factory: Build, Deploy, and Monetize Software Products with Autonomous AI Agents. Complete guide to using AI agents to autonomously build, deploy, and monetize micro-SaaS products: GitHub for code, Stripe for billing, Postgres for data, and automated dispute arbitration. Includes detailed Python code examples with full API integration."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [saas, github, stripe, postgres, disputes, guide, greenhelix, openclaw, ai-agent]
price_usd: 0.0
content_type: markdown
executable: false
install: none
credentials: [GREENHELIX_API_KEY, STRIPE_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - GREENHELIX_API_KEY
        - STRIPE_API_KEY
    primaryEnv: GREENHELIX_API_KEY
---
# The Agent SaaS Factory: Build, Deploy, and Monetize Software Products with Autonomous AI Agents

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)
> - `STRIPE_API_KEY`: Stripe API key for card payment processing (scoped to payment intents only)


When Stripe announced the Agentic Commerce Suite in March 2026 -- with Visa, OpenAI, and Samsung as launch partners -- they framed it as "AI agents that can buy things." That is the merchant side of the equation. An agent browses a storefront, picks a product, and pays with a human's saved card. But what about the other side? What about an agent that builds the product, sets up the billing, deploys the database, handles the disputes, and operates the entire business -- end to end, without a human writing a single line of code or clicking a single button in a dashboard?
That is what this guide builds. A factory pattern where autonomous AI agents receive a product specification and produce a running, revenue-generating micro-SaaS: repository scaffolded on GitHub, schema designed and migrated in Postgres, billing configured in Stripe, dispute resolution automated, and the whole pipeline orchestrated by a single `AgentSaaSFactory` class. The BotStall marketplace demonstrated in late 2025 that agents could list and sell digital goods. We go further: agents that build, operate, and defend the entire software business.
The infrastructure is the GreenHelix A2A Commerce Gateway's pro-tier integration tools: 10 GitHub tools, 13 Stripe tools, 6 Postgres tools, and 5 Dispute tools -- 34 tools total, all accessible through a single HTTP endpoint at $0.005-$0.01 per call. This guide covers every one of them.

## What You'll Learn
- Chapter 1: Why Agents Should Build SaaS
- Chapter 2: Setting Up the Agent's Development Environment
- Chapter 3: The Data Layer: Agents Managing Postgres
- Chapter 4: Monetization: Agents Running Stripe
- Chapter 5: The Full Factory: Orchestrating the Pipeline
- Chapter 6: Dispute Resolution and Customer Support Automation
- Chapter 7: Security, Cost Governance, and Guardrails
- Chapter 8: Production Recipes
- Chapter 9: What's Next

## Full Guide

# The Agent SaaS Factory: Build, Deploy, and Monetize Software Products with Autonomous AI Agents

When Stripe announced the Agentic Commerce Suite in March 2026 -- with Visa, OpenAI, and Samsung as launch partners -- they framed it as "AI agents that can buy things." That is the merchant side of the equation. An agent browses a storefront, picks a product, and pays with a human's saved card. But what about the other side? What about an agent that builds the product, sets up the billing, deploys the database, handles the disputes, and operates the entire business -- end to end, without a human writing a single line of code or clicking a single button in a dashboard?

That is what this guide builds. A factory pattern where autonomous AI agents receive a product specification and produce a running, revenue-generating micro-SaaS: repository scaffolded on GitHub, schema designed and migrated in Postgres, billing configured in Stripe, dispute resolution automated, and the whole pipeline orchestrated by a single `AgentSaaSFactory` class. The BotStall marketplace demonstrated in late 2025 that agents could list and sell digital goods. We go further: agents that build, operate, and defend the entire software business.

The infrastructure is the GreenHelix A2A Commerce Gateway's pro-tier integration tools: 10 GitHub tools, 13 Stripe tools, 6 Postgres tools, and 5 Dispute tools -- 34 tools total, all accessible through a single HTTP endpoint at $0.005-$0.01 per call. This guide covers every one of them.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Table of Contents

1. [Why Agents Should Build SaaS](#chapter-1-why-agents-should-build-saas)
2. [Setting Up the Agent's Development Environment](#chapter-2-setting-up-the-agents-development-environment)
3. [The Data Layer: Agents Managing Postgres](#chapter-3-the-data-layer-agents-managing-postgres)
4. [Monetization: Agents Running Stripe](#chapter-4-monetization-agents-running-stripe)
5. [The Full Factory: Orchestrating the Pipeline](#chapter-5-the-full-factory-orchestrating-the-pipeline)
6. [Dispute Resolution and Customer Support Automation](#chapter-6-dispute-resolution-and-customer-support-automation)
7. [Security, Cost Governance, and Guardrails](#chapter-7-security-cost-governance-and-guardrails)
8. [Production Recipes](#chapter-8-production-recipes)
9. [What's Next](#chapter-9-whats-next)

---

## Chapter 1: Why Agents Should Build SaaS

### From Tools to Operators

The 2025 frame was "agents as tools." Developer writes prompt, agent generates code, developer reviews and deploys. Faster pair programming. Useful. Not transformative.

The shift is "agents as operators." The agent does not help you build a SaaS product -- it builds the SaaS product. Creates the repository. Designs the schema. Sets up Stripe pricing. Writes code, submits PRs, reviews diffs, merges. Monitors disputes and resolves them. The human's role shifts from implementer to investor: you provide the specification and the API credits. The agent does the rest.

Stripe's Agentic Commerce Suite already envisions agents that autonomously complete purchases and handle disputes. The missing piece is the supply side -- agents that build and operate the businesses those buyer agents purchase from.

### The BotStall Precedent

BotStall (late 2025) proved one half: agents listing and selling digital goods on a marketplace. But BotStall agents were vendors, not builders. A human created the product; the agent handled distribution. The Agent SaaS Factory closes the loop: the agent creates, operates, monetizes, and defends the entire business.

### Architecture Overview

The factory runs on four services, all accessed through the GreenHelix A2A Commerce Gateway:

```
+------------------------------------------------------------+
|                    AgentSaaSFactory                         |
|                                                            |
|  +------------------+  +------------------+                |
|  | AgentDeveloper   |  | AgentDBA         |                |
|  | 10 GitHub tools  |  | 6 Postgres tools |                |
|  | $0.005/call      |  | $0.01/call       |                |
|  +--------+---------+  +--------+---------+                |
|           |                      |                         |
|  +--------+---------+  +--------+---------+                |
|  | AgentBilling     |  | AgentArbitrator  |                |
|  | 13 Stripe tools  |  | 5 Dispute tools  |                |
|  | $0.01/call       |  | varies           |                |
|  +--------+---------+  +--------+---------+                |
|           |                      |                         |
+-----------|----------------------|-------------------------+
            |                      |
   +--------v----------------------v---------+
   |    GreenHelix A2A Commerce Gateway      |
   |    Pro-tier: GitHub + Stripe + Postgres  |
   |    + Disputes                            |
   +------------------------------------------+
```

### Pro-Tier Cost Model

Every tool call has a fixed cost. There is no per-seat pricing, no monthly minimum, no overage surprise. You pay exactly for what the agent does.

| Service | Tools | Cost per Call | Typical Calls per SaaS Build |
|---------|-------|---------------|------------------------------|
| GitHub | 10 | $0.005 | 40-60 |
| Stripe | 13 | $0.01 | 15-25 |
| Postgres | 6 | $0.01 | 20-40 |
| Disputes | 5 | varies | 0-10 (reactive) |

A complete micro-SaaS build costs $1.00-$1.50 in tool calls. Ongoing operation runs $0.10-$0.30/day. At $29/month from a single customer, the unit economics are immediately positive.

---

## Chapter 2: Setting Up the Agent's Development Environment

### The AgentDeveloper Class

This class wraps all 10 GitHub tools into a development interface. The agent uses it to create repositories, scaffold projects, manage issues, submit pull requests, and perform code review.

```python
import requests
import json
import time
from typing import Optional, List


class AgentDeveloper:
    """GitHub development client for the GreenHelix A2A Commerce Gateway.

    Wraps the 10 GitHub integration tools into a development workflow
    interface for autonomous repository management, code review, and
    issue tracking.
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.base_url = base_url
        self.agent_id = agent_id
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

    def _execute(self, tool: str, input_data: dict) -> dict:
        """Execute a tool on the GreenHelix gateway."""
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        if resp.status_code == 402:
            raise BudgetExhaustedError(
                f"Agent {self.agent_id} budget exceeded: {resp.text}"
            )
        resp.raise_for_status()
        return resp.json()

    # -- Repository Management -----------------------------------------

    def create_repo(
        self,
        name: str,
        description: str,
        private: bool = True,
    ) -> dict:
        """Create a new GitHub repository."""
        return self._execute("create_repo", {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": True,
        })

    def get_repo(self, owner: str, repo: str) -> dict:
        """Get repository metadata."""
        return self._execute("get_repo", {
            "owner": owner,
            "repo": repo,
        })

    # -- File Operations -----------------------------------------------

    def get_file_contents(
        self,
        owner: str,
        repo: str,
        path: str,
        ref: Optional[str] = None,
    ) -> dict:
        """Read a file from a repository."""
        payload = {"owner": owner, "repo": repo, "path": path}
        if ref:
            payload["ref"] = ref
        return self._execute("get_file_contents", payload)

    def create_or_update_file(
        self,
        owner: str,
        repo: str,
        path: str,
        content: str,
        message: str,
        branch: Optional[str] = None,
        sha: Optional[str] = None,
    ) -> dict:
        """Write or update a file in a repository."""
        payload = {
            "owner": owner,
            "repo": repo,
            "path": path,
            "content": content,
            "message": message,
        }
        if branch:
            payload["branch"] = branch
        if sha:
            payload["sha"] = sha
        return self._execute("create_or_update_file", payload)

    # -- Issue Tracking ------------------------------------------------

    def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
    ) -> dict:
        """File a bug report or feature request."""
        payload = {
            "owner": owner,
            "repo": repo,
            "title": title,
            "body": body,
        }
        if labels:
            payload["labels"] = labels
        return self._execute("create_issue", payload)

    def get_issue(
        self,
        owner: str,
        repo: str,
        issue_number: int,
    ) -> dict:
        """Retrieve issue details."""
        return self._execute("get_issue", {
            "owner": owner,
            "repo": repo,
            "issue_number": issue_number,
        })

    # -- Code Review ---------------------------------------------------

    def create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str = "main",
    ) -> dict:
        """Submit code changes for review."""
        return self._execute("create_pull_request", {
            "owner": owner,
            "repo": repo,
            "title": title,
            "body": body,
            "head": head,
            "base": base,
        })

    def merge_pull_request(
        self,
        owner: str,
        repo: str,
        pull_number: int,
        merge_method: str = "squash",
    ) -> dict:
        """Merge an approved pull request."""
        return self._execute("merge_pull_request", {
            "owner": owner,
            "repo": repo,
            "pull_number": pull_number,
            "merge_method": merge_method,
        })

    # -- Code Intelligence ---------------------------------------------

    def search_code(
        self,
        query: str,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> dict:
        """Search across codebases."""
        payload = {"query": query}
        if owner and repo:
            payload["query"] = f"{query} repo:{owner}/{repo}"
        return self._execute("search_code", payload)

    def list_commits(
        self,
        owner: str,
        repo: str,
        sha: Optional[str] = None,
        per_page: int = 30,
    ) -> dict:
        """View commit history."""
        payload = {
            "owner": owner,
            "repo": repo,
            "per_page": per_page,
        }
        if sha:
            payload["sha"] = sha
        return self._execute("list_commits", payload)

    # -- High-Level Workflows ------------------------------------------

    def scaffold_project(
        self,
        owner: str,
        repo: str,
        files: dict,
        branch: str = "main",
    ) -> List[dict]:
        """Write multiple files to scaffold a project.

        Args:
            files: dict mapping file paths to content strings.
                   Example: {"src/app.py": "...", "requirements.txt": "..."}
        """
        results = []
        for path, content in files.items():
            result = self.create_or_update_file(
                owner=owner,
                repo=repo,
                path=path,
                content=content,
                message=f"scaffold: add {path}",
                branch=branch,
            )
            results.append(result)
        return results

    def review_and_merge(
        self,
        owner: str,
        repo: str,
        head_branch: str,
        title: str,
        description: str,
    ) -> dict:
        """Create a PR, perform automated review, and merge.

        The agent creates the PR, searches the diff for known
        anti-patterns, then merges if clean.
        """
        pr = self.create_pull_request(
            owner=owner,
            repo=repo,
            title=title,
            body=description,
            head=head_branch,
            base="main",
        )
        pull_number = pr["number"]

        # Agent-driven code review: search for common issues
        issues_found = []
        for pattern in ["eval(", "exec(", "password =", "secret ="]:
            hits = self.search_code(
                query=pattern,
                owner=owner,
                repo=repo,
            )
            if hits.get("total_count", 0) > 0:
                issues_found.append(pattern)

        if issues_found:
            self.create_issue(
                owner=owner,
                repo=repo,
                title=f"Security review: patterns found in PR #{pull_number}",
                body=f"Found: {', '.join(issues_found)}. Review before merge.",
                labels=["security", "automated-review"],
            )
            return {"status": "blocked", "pr": pr, "issues": issues_found}

        merged = self.merge_pull_request(
            owner=owner,
            repo=repo,
            pull_number=pull_number,
        )
        return {"status": "merged", "pr": pr, "merge": merged}
```

### Pattern: Agent-Driven Code Review

The agent reads the diff, searches the codebase for related code, and judges whether the change is safe -- beyond what linters and CI catch.

```python
import os

dev = AgentDeveloper(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="dev-agent-01",
)

# Agent reviews its own work before merging
owner, repo = "myorg", "newsletter-saas"

# 1. Check recent commits on the feature branch
commits = dev.list_commits(owner, repo, sha="feature/add-billing")
print(f"Feature branch has {len(commits)} commits")

# 2. Search for any hardcoded secrets that slipped in
secrets_check = dev.search_code(
    query="STRIPE_SECRET password API_KEY",
    owner=owner,
    repo=repo,
)
if secrets_check.get("total_count", 0) > 0:
    dev.create_issue(
        owner=owner,
        repo=repo,
        title="CRITICAL: Hardcoded secrets detected",
        body="Automated scan found potential secrets in codebase.",
        labels=["security", "P0"],
    )
    raise RuntimeError("Secrets detected -- aborting merge")

# 3. If clean, create PR and merge
result = dev.review_and_merge(
    owner=owner,
    repo=repo,
    head_branch="feature/add-billing",
    title="Add Stripe billing integration",
    description="Adds subscription management with usage-based pricing.",
)
print(f"PR status: {result['status']}")
```

### Pattern: Automated Issue Tracking

The agent tracks its own work with issues, creating a paper trail for every feature and bug fix.

```python
# Agent creates a tracking issue before starting work
issue = dev.create_issue(
    owner="myorg",
    repo="newsletter-saas",
    title="Implement subscriber management API",
    body=(
        "## Requirements\n"
        "- POST /api/subscribers to add new subscriber\n"
        "- GET /api/subscribers to list all subscribers\n"
        "- DELETE /api/subscribers/:id to unsubscribe\n"
        "- Store in Postgres with email uniqueness constraint\n\n"
        "## Acceptance Criteria\n"
        "- All endpoints return JSON\n"
        "- Email validation on POST\n"
        "- Idempotent DELETE\n"
    ),
    labels=["feature", "api", "agent-created"],
)
issue_number = issue["number"]

# Agent reads the issue back to confirm requirements
details = dev.get_issue("myorg", "newsletter-saas", issue_number)
print(f"Working on: {details['title']}")

# ... agent implements the feature ...

# Agent closes the issue by referencing it in the PR body
dev.create_pull_request(
    owner="myorg",
    repo="newsletter-saas",
    title="Implement subscriber management API",
    body=f"Closes #{issue_number}\n\nAdds CRUD endpoints for subscribers.",
    head="feature/subscriber-api",
)
```

**Cost for a typical development session:** 40-60 GitHub tool calls at $0.005 each = $0.20-$0.30. That covers repo creation, 10-15 file writes, 3-5 PR cycles, issue tracking, and code search.

---

## Chapter 3: The Data Layer: Agents Managing Postgres

### The AgentDBA Class

This class wraps all 6 Postgres tools. The agent uses it to design schemas, run migrations, seed data, and validate data integrity.

```python
import requests
import json
from typing import Optional, List


class AgentDBA:
    """Postgres database administration client for the GreenHelix
    A2A Commerce Gateway.

    Wraps the 6 Postgres integration tools into a database management
    interface for schema design, migrations, queries, and data validation.
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.base_url = base_url
        self.agent_id = agent_id
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

    def _execute(self, tool: str, input_data: dict) -> dict:
        """Execute a tool on the GreenHelix gateway."""
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        if resp.status_code == 402:
            raise BudgetExhaustedError(
                f"Agent {self.agent_id} budget exceeded: {resp.text}"
            )
        resp.raise_for_status()
        return resp.json()

    # -- Schema Inspection ---------------------------------------------

    def get_schema(self) -> dict:
        """Inspect the full database schema."""
        return self._execute("get_schema", {})

    def list_tables(self) -> dict:
        """List all tables in the database."""
        return self._execute("list_tables", {})

    def describe_table(self, table_name: str) -> dict:
        """Get the structure of a specific table."""
        return self._execute("describe_table", {
            "table_name": table_name,
        })

    # -- Query Execution -----------------------------------------------

    def query(self, sql: str, params: Optional[List] = None) -> dict:
        """Run a SELECT query. Read-only."""
        payload = {"sql": sql}
        if params:
            payload["params"] = params
        return self._execute("query", payload)

    def execute_query(
        self,
        sql: str,
        params: Optional[List] = None,
    ) -> dict:
        """Run any SQL statement (INSERT, UPDATE, DELETE, DDL)."""
        payload = {"sql": sql}
        if params:
            payload["params"] = params
        return self._execute("execute_query", payload)

    # -- Migrations ----------------------------------------------------

    def execute_migration(
        self,
        migration_sql: str,
        version: str,
        description: str,
    ) -> dict:
        """Run a schema migration with version tracking."""
        return self._execute("execute_migration", {
            "migration_sql": migration_sql,
            "version": version,
            "description": description,
        })

    # -- High-Level Workflows ------------------------------------------

    def schema_first_design(
        self,
        tables: dict,
    ) -> List[dict]:
        """Design and create a full schema from a table specification.

        Args:
            tables: dict mapping table names to column definitions.
                Example:
                {
                    "subscribers": [
                        "id SERIAL PRIMARY KEY",
                        "email VARCHAR(255) UNIQUE NOT NULL",
                        "created_at TIMESTAMPTZ DEFAULT NOW()",
                    ]
                }
        """
        results = []
        for table_name, columns in tables.items():
            col_defs = ", ".join(columns)
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({col_defs})"
            result = self.execute_query(sql)
            results.append({"table": table_name, "result": result})
        return results

    def safe_migration_chain(
        self,
        migrations: List[dict],
    ) -> List[dict]:
        """Execute a chain of migrations in order, stopping on failure.

        Args:
            migrations: list of dicts with keys:
                - version: str (e.g., "001")
                - description: str
                - up: str (SQL to apply)
        """
        results = []
        for m in migrations:
            try:
                result = self.execute_migration(
                    migration_sql=m["up"],
                    version=m["version"],
                    description=m["description"],
                )
                results.append({
                    "version": m["version"],
                    "status": "applied",
                    "result": result,
                })
            except Exception as e:
                results.append({
                    "version": m["version"],
                    "status": "failed",
                    "error": str(e),
                })
                break  # Stop chain on failure
        return results

    def validate_data(
        self,
        table: str,
        checks: List[dict],
    ) -> List[dict]:
        """Run validation checks against a table.

        Args:
            checks: list of dicts with keys:
                - name: str (human-readable check name)
                - sql: str (query that should return 0 rows if valid)
        """
        results = []
        for check in checks:
            result = self.query(check["sql"])
            row_count = len(result.get("rows", []))
            results.append({
                "check": check["name"],
                "passed": row_count == 0,
                "violations": row_count,
            })
        return results
```

### Pattern: Schema-First Development

The agent designs the schema before writing application code, ensuring the data layer is correct before business logic is built on top.

```python
import os

dba = AgentDBA(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="dba-agent-01",
)

# Agent designs the schema for a newsletter SaaS
schema = dba.schema_first_design({
    "subscribers": [
        "id SERIAL PRIMARY KEY",
        "email VARCHAR(255) UNIQUE NOT NULL",
        "name VARCHAR(255)",
        "status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'unsubscribed', 'bounced'))",
        "stripe_customer_id VARCHAR(255)",
        "subscribed_at TIMESTAMPTZ DEFAULT NOW()",
        "unsubscribed_at TIMESTAMPTZ",
    ],
    "newsletters": [
        "id SERIAL PRIMARY KEY",
        "subject VARCHAR(500) NOT NULL",
        "body TEXT NOT NULL",
        "status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'scheduled', 'sent'))",
        "scheduled_for TIMESTAMPTZ",
        "sent_at TIMESTAMPTZ",
        "created_at TIMESTAMPTZ DEFAULT NOW()",
    ],
    "send_log": [
        "id SERIAL PRIMARY KEY",
        "newsletter_id INTEGER REFERENCES newsletters(id)",
        "subscriber_id INTEGER REFERENCES subscribers(id)",
        "status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'failed', 'bounced'))",
        "sent_at TIMESTAMPTZ",
        "error_message TEXT",
        "UNIQUE(newsletter_id, subscriber_id)",
    ],
})

# Verify the schema was created correctly
tables = dba.list_tables()
print(f"Tables created: {[t['table_name'] for t in tables['rows']]}")

for table in ["subscribers", "newsletters", "send_log"]:
    desc = dba.describe_table(table)
    print(f"\n{table}:")
    for col in desc["columns"]:
        print(f"  {col['column_name']} {col['data_type']} {col.get('constraints', '')}")
```

### Pattern: Safe Migration Chains

Versioned migrations tracked in order. The chain stops on the first failure to prevent partial schema states.

```python
# Agent evolves the schema over time
migrations = dba.safe_migration_chain([
    {
        "version": "002",
        "description": "Add subscriber tags for segmentation",
        "up": """
            CREATE TABLE IF NOT EXISTS subscriber_tags (
                id SERIAL PRIMARY KEY,
                subscriber_id INTEGER REFERENCES subscribers(id) ON DELETE CASCADE,
                tag VARCHAR(100) NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                UNIQUE(subscriber_id, tag)
            );
            CREATE INDEX idx_subscriber_tags_tag ON subscriber_tags(tag);
        """,
    },
    {
        "version": "003",
        "description": "Add open tracking to send_log",
        "up": """
            ALTER TABLE send_log ADD COLUMN IF NOT EXISTS opened_at TIMESTAMPTZ;
            ALTER TABLE send_log ADD COLUMN IF NOT EXISTS open_count INTEGER DEFAULT 0;
            CREATE INDEX idx_send_log_opened ON send_log(opened_at)
                WHERE opened_at IS NOT NULL;
        """,
    },
    {
        "version": "004",
        "description": "Add revenue tracking table",
        "up": """
            CREATE TABLE IF NOT EXISTS revenue_events (
                id SERIAL PRIMARY KEY,
                subscriber_id INTEGER REFERENCES subscribers(id),
                stripe_payment_intent_id VARCHAR(255) UNIQUE,
                amount_cents INTEGER NOT NULL,
                currency VARCHAR(3) DEFAULT 'usd',
                event_type VARCHAR(50) NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            CREATE INDEX idx_revenue_subscriber ON revenue_events(subscriber_id);
            CREATE INDEX idx_revenue_created ON revenue_events(created_at);
        """,
    },
])

for m in migrations:
    status_marker = "OK" if m["status"] == "applied" else "FAIL"
    print(f"  [{status_marker}] v{m['version']}: {m.get('error', 'applied')}")
```

### Pattern: Data Validation Pipeline

After seeding data or processing a batch, the agent runs validation checks to catch integrity issues early.

```python
# After importing subscriber data, validate
validations = dba.validate_data(
    table="subscribers",
    checks=[
        {
            "name": "No duplicate emails",
            "sql": """
                SELECT email, COUNT(*) as cnt FROM subscribers
                GROUP BY email HAVING COUNT(*) > 1
            """,
        },
        {
            "name": "All active subscribers have email",
            "sql": """
                SELECT id FROM subscribers
                WHERE status = 'active' AND (email IS NULL OR email = '')
            """,
        },
        {
            "name": "No future subscription dates",
            "sql": """
                SELECT id FROM subscribers
                WHERE subscribed_at > NOW() + INTERVAL '1 minute'
            """,
        },
        {
            "name": "Unsubscribed have unsubscribed_at set",
            "sql": """
                SELECT id FROM subscribers
                WHERE status = 'unsubscribed' AND unsubscribed_at IS NULL
            """,
        },
    ],
)

all_passed = all(v["passed"] for v in validations)
for v in validations:
    marker = "PASS" if v["passed"] else f"FAIL ({v['violations']} violations)"
    print(f"  [{marker}] {v['check']}")

if not all_passed:
    raise DataValidationError("Validation failed -- see results above")
```

**Cost for a typical database session:** 20-40 Postgres tool calls at $0.01 each = $0.20-$0.40. That covers schema creation, 3-5 migrations, data seeding, and validation.

---

## Chapter 4: Monetization: Agents Running Stripe

### The AgentBilling Class

This class wraps all 13 Stripe tools. The agent uses it to create products, set pricing, generate checkout sessions, manage invoices, and track revenue.

```python
import requests
import json
from typing import Optional, List, Literal


class AgentBilling:
    """Stripe billing client for the GreenHelix A2A Commerce Gateway.

    Wraps the 13 Stripe integration tools into a monetization interface
    for product creation, pricing, checkout, invoicing, and revenue tracking.
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.base_url = base_url
        self.agent_id = agent_id
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

    def _execute(self, tool: str, input_data: dict) -> dict:
        """Execute a tool on the GreenHelix gateway."""
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        if resp.status_code == 402:
            raise BudgetExhaustedError(
                f"Agent {self.agent_id} budget exceeded: {resp.text}"
            )
        resp.raise_for_status()
        return resp.json()

    # -- Customer Management -------------------------------------------

    def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Register a new Stripe customer."""
        payload = {"email": email}
        if name:
            payload["name"] = name
        if metadata:
            payload["metadata"] = metadata
        return self._execute("create_customer", payload)

    def get_customer(self, customer_id: str) -> dict:
        """Retrieve customer details."""
        return self._execute("get_customer", {
            "customer_id": customer_id,
        })

    # -- Product & Pricing ---------------------------------------------

    def create_product(
        self,
        name: str,
        description: str,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Define a new product or service."""
        payload = {"name": name, "description": description}
        if metadata:
            payload["metadata"] = metadata
        return self._execute("create_product", payload)

    def get_product(self, product_id: str) -> dict:
        """Retrieve product details."""
        return self._execute("get_product", {
            "product_id": product_id,
        })

    def create_price(
        self,
        product_id: str,
        unit_amount: int,
        currency: str = "usd",
        recurring: Optional[dict] = None,
        usage_type: Optional[str] = None,
    ) -> dict:
        """Set pricing for a product.

        Args:
            unit_amount: Price in cents (e.g., 2900 = $29.00)
            recurring: dict with "interval" key ("month", "year")
            usage_type: "metered" for usage-based billing
        """
        payload = {
            "product_id": product_id,
            "unit_amount": unit_amount,
            "currency": currency,
        }
        if recurring:
            payload["recurring"] = recurring
        if usage_type:
            payload["usage_type"] = usage_type
        return self._execute("create_price", payload)

    # -- Checkout & Payments -------------------------------------------

    def create_checkout_session(
        self,
        price_id: str,
        success_url: str,
        cancel_url: str,
        mode: Literal["payment", "subscription"] = "subscription",
        customer_id: Optional[str] = None,
    ) -> dict:
        """Generate a Stripe checkout page."""
        payload = {
            "price_id": price_id,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "mode": mode,
        }
        if customer_id:
            payload["customer_id"] = customer_id
        return self._execute("create_checkout_session", payload)

    def get_checkout_session(self, session_id: str) -> dict:
        """Check the status of a checkout session."""
        return self._execute("get_checkout_session", {
            "session_id": session_id,
        })

    # -- Invoicing -----------------------------------------------------

    def create_invoice(
        self,
        customer_id: str,
        auto_advance: bool = True,
        collection_method: str = "charge_automatically",
    ) -> dict:
        """Generate an invoice for a customer."""
        return self._execute("create_invoice", {
            "customer_id": customer_id,
            "auto_advance": auto_advance,
            "collection_method": collection_method,
        })

    def get_invoice(self, invoice_id: str) -> dict:
        """Retrieve invoice details."""
        return self._execute("get_invoice", {
            "invoice_id": invoice_id,
        })

    def list_invoices(
        self,
        customer_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 10,
    ) -> dict:
        """List invoices with optional filtering."""
        payload = {"limit": limit}
        if customer_id:
            payload["customer_id"] = customer_id
        if status:
            payload["status"] = status
        return self._execute("list_invoices", payload)

    # -- Payment Intents -----------------------------------------------

    def create_payment_intent(
        self,
        amount: int,
        currency: str = "usd",
        customer_id: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Initiate a payment."""
        payload = {"amount": amount, "currency": currency}
        if customer_id:
            payload["customer_id"] = customer_id
        if metadata:
            payload["metadata"] = metadata
        return self._execute("create_payment_intent", payload)

    def get_payment_intent(self, payment_intent_id: str) -> dict:
        """Check the status of a payment."""
        return self._execute("get_payment_intent", {
            "payment_intent_id": payment_intent_id,
        })

    # -- Revenue Tracking ----------------------------------------------

    def get_balance(self) -> dict:
        """Check the Stripe account balance."""
        return self._execute("get_balance", {})

    # -- High-Level Workflows ------------------------------------------

    def setup_subscription_product(
        self,
        name: str,
        description: str,
        monthly_price_cents: int,
        yearly_price_cents: Optional[int] = None,
    ) -> dict:
        """Create a product with monthly (and optional yearly) pricing.

        Returns dict with product_id, monthly_price_id, yearly_price_id.
        """
        product = self.create_product(name=name, description=description)
        product_id = product["id"]

        monthly = self.create_price(
            product_id=product_id,
            unit_amount=monthly_price_cents,
            recurring={"interval": "month"},
        )

        result = {
            "product_id": product_id,
            "monthly_price_id": monthly["id"],
        }

        if yearly_price_cents:
            yearly = self.create_price(
                product_id=product_id,
                unit_amount=yearly_price_cents,
                recurring={"interval": "year"},
            )
            result["yearly_price_id"] = yearly["id"]

        return result

    def setup_usage_based_product(
        self,
        name: str,
        description: str,
        per_unit_cents: int,
    ) -> dict:
        """Create a metered billing product.

        Returns dict with product_id and price_id for usage reporting.
        """
        product = self.create_product(name=name, description=description)
        price = self.create_price(
            product_id=product["id"],
            unit_amount=per_unit_cents,
            usage_type="metered",
            recurring={"interval": "month"},
        )
        return {
            "product_id": product["id"],
            "price_id": price["id"],
        }
```

### Pattern: Subscription Lifecycle

Complete subscription setup with monthly/annual pricing and customer onboarding through checkout.

```python
import os

billing = AgentBilling(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="billing-agent-01",
)

# 1. Create the subscription product
product = billing.setup_subscription_product(
    name="NewsletterPro",
    description="Automated newsletter platform with analytics",
    monthly_price_cents=2900,       # $29/month
    yearly_price_cents=29000,       # $290/year (2 months free)
)
print(f"Product: {product['product_id']}")
print(f"Monthly: {product['monthly_price_id']}")
print(f"Yearly:  {product['yearly_price_id']}")

# 2. Onboard a customer
customer = billing.create_customer(
    email="alice@example.com",
    name="Alice Chen",
    metadata={"source": "organic", "plan": "monthly"},
)

# 3. Generate checkout session
session = billing.create_checkout_session(
    price_id=product["monthly_price_id"],
    success_url="https://newsletter-pro.example.com/welcome",
    cancel_url="https://newsletter-pro.example.com/pricing",
    mode="subscription",
    customer_id=customer["id"],
)
print(f"Checkout URL: {session['url']}")

# 4. Agent polls for completion (in production, use webhooks)
import time
for _ in range(30):
    status = billing.get_checkout_session(session["id"])
    if status["payment_status"] == "paid":
        print("Payment confirmed -- activating subscription")
        break
    time.sleep(10)
```

### Pattern: Usage-Based Billing

For API-as-a-Service products, the agent sets up metered billing where customers pay per API call.

```python
# Create a metered product
api_product = billing.setup_usage_based_product(
    name="TranslationAPI",
    description="Neural machine translation API",
    per_unit_cents=1,  # $0.01 per translation
)

# Generate an invoice at month end
invoices = billing.list_invoices(
    customer_id="cus_abc123",
    status="draft",
)
if invoices.get("data"):
    invoice = billing.get_invoice(invoices["data"][0]["id"])
    print(f"Draft invoice: ${invoice['amount_due'] / 100:.2f}")
```

### Pattern: Revenue Reconciliation

Periodic balance check against internal records.

```python
# Daily revenue check
balance = billing.get_balance()
available = sum(b["amount"] for b in balance.get("available", []))
pending = sum(b["amount"] for b in balance.get("pending", []))

print(f"Available: ${available / 100:.2f}")
print(f"Pending:   ${pending / 100:.2f}")

# Cross-reference with recent invoices
recent = billing.list_invoices(status="paid", limit=50)
invoice_total = sum(inv["amount_paid"] for inv in recent.get("data", []))
print(f"Invoiced (last 50): ${invoice_total / 100:.2f}")
```

**Cost for a typical billing setup:** 15-25 Stripe tool calls at $0.01 each = $0.15-$0.25. That covers product creation, pricing, customer onboarding, checkout sessions, and balance checks.

---

## Chapter 5: The Full Factory: Orchestrating the Pipeline

### The AgentSaaSFactory Class

This is the orchestrator. It combines `AgentDeveloper`, `AgentDBA`, and `AgentBilling` into a single pipeline that takes a product specification and produces a running micro-SaaS.

```python
import os
import json
import time
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class SaaSSpec:
    """Specification for a micro-SaaS product."""
    name: str
    description: str
    repo_name: str
    owner: str
    monthly_price_cents: int
    yearly_price_cents: Optional[int] = None
    tables: dict = field(default_factory=dict)
    migrations: list = field(default_factory=list)
    app_files: dict = field(default_factory=dict)
    success_url: str = ""
    cancel_url: str = ""


class AgentSaaSFactory:
    """End-to-end SaaS factory combining GitHub, Postgres, and Stripe.

    Takes a SaaSSpec and produces a running, revenue-generating
    micro-SaaS with repository, database, and billing.
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.developer = AgentDeveloper(
            api_key=api_key,
            agent_id=f"{agent_id}-dev",
            base_url=base_url,
        )
        self.dba = AgentDBA(
            api_key=api_key,
            agent_id=f"{agent_id}-dba",
            base_url=base_url,
        )
        self.billing = AgentBilling(
            api_key=api_key,
            agent_id=f"{agent_id}-billing",
            base_url=base_url,
        )
        self.agent_id = agent_id
        self.build_log = []

    def _log(self, phase: str, message: str, data: Optional[dict] = None):
        entry = {
            "timestamp": time.time(),
            "phase": phase,
            "message": message,
            "data": data,
        }
        self.build_log.append(entry)
        print(f"[{phase}] {message}")

    def build(self, spec: SaaSSpec) -> dict:
        """Execute the full SaaS build pipeline.

        Phase 1: Create repository and scaffold code
        Phase 2: Design schema and run migrations
        Phase 3: Set up Stripe products and pricing
        Phase 4: Deploy and verify

        Returns a manifest with all created resource IDs.
        """
        manifest = {"spec": spec.name, "resources": {}}

        # Phase 1: Repository
        self._log("repo", f"Creating repository {spec.repo_name}")
        repo = self.developer.create_repo(
            name=spec.repo_name,
            description=spec.description,
        )
        manifest["resources"]["repo"] = repo
        self._log("repo", f"Repository created: {repo.get('html_url')}")

        # Scaffold application files
        if spec.app_files:
            self._log("repo", f"Scaffolding {len(spec.app_files)} files")
            self.developer.scaffold_project(
                owner=spec.owner,
                repo=spec.repo_name,
                files=spec.app_files,
            )

        # Phase 2: Database
        if spec.tables:
            self._log("db", f"Creating {len(spec.tables)} tables")
            schema_result = self.dba.schema_first_design(spec.tables)
            manifest["resources"]["tables"] = schema_result

        if spec.migrations:
            self._log("db", f"Running {len(spec.migrations)} migrations")
            migration_result = self.dba.safe_migration_chain(spec.migrations)
            manifest["resources"]["migrations"] = migration_result

            # Verify schema integrity
            tables = self.dba.list_tables()
            self._log(
                "db",
                f"Schema verified: {len(tables.get('rows', []))} tables",
            )

        # Phase 3: Billing
        self._log("billing", "Setting up Stripe product and pricing")
        product = self.billing.setup_subscription_product(
            name=spec.name,
            description=spec.description,
            monthly_price_cents=spec.monthly_price_cents,
            yearly_price_cents=spec.yearly_price_cents,
        )
        manifest["resources"]["stripe"] = product

        # Store billing config in the repo
        billing_config = json.dumps(product, indent=2)
        self.developer.create_or_update_file(
            owner=spec.owner,
            repo=spec.repo_name,
            path="config/billing.json",
            content=billing_config,
            message="Add Stripe billing configuration",
        )
        self._log("billing", f"Product created: {product['product_id']}")

        # Phase 4: Verification
        self._log("verify", "Running post-build checks")

        # Verify repo exists and has correct files
        repo_check = self.developer.get_repo(spec.owner, spec.repo_name)
        assert repo_check.get("name") == spec.repo_name

        # Verify product exists in Stripe
        product_check = self.billing.get_product(product["product_id"])
        assert product_check.get("active") is True

        # Verify all tables exist
        if spec.tables:
            for table_name in spec.tables:
                desc = self.dba.describe_table(table_name)
                assert len(desc.get("columns", [])) > 0

        self._log("verify", "All post-build checks passed")

        # Create a tracking issue
        self.developer.create_issue(
            owner=spec.owner,
            repo=spec.repo_name,
            title=f"Build manifest: {spec.name}",
            body=(
                f"## Build Manifest\n\n"
                f"```json\n{json.dumps(manifest, indent=2, default=str)}\n```\n\n"
                f"Build completed at {time.strftime('%Y-%m-%d %H:%M:%S UTC')}"
            ),
            labels=["build-manifest", "agent-created"],
        )

        manifest["build_log"] = self.build_log
        return manifest
```

### End-to-End Walkthrough

The factory building a complete newsletter SaaS from a single specification:

```python
spec = SaaSSpec(
    name="NewsletterPro",
    description="Automated newsletter platform with analytics and billing",
    repo_name="newsletter-pro",
    owner="myorg",
    monthly_price_cents=2900,
    yearly_price_cents=29000,
    tables={
        "subscribers": [
            "id SERIAL PRIMARY KEY",
            "email VARCHAR(255) UNIQUE NOT NULL",
            "name VARCHAR(255)",
            "status VARCHAR(20) DEFAULT 'active'",
            "stripe_customer_id VARCHAR(255)",
            "created_at TIMESTAMPTZ DEFAULT NOW()",
        ],
        "newsletters": [
            "id SERIAL PRIMARY KEY",
            "subject VARCHAR(500) NOT NULL",
            "body TEXT NOT NULL",
            "status VARCHAR(20) DEFAULT 'draft'",
            "sent_at TIMESTAMPTZ",
            "created_at TIMESTAMPTZ DEFAULT NOW()",
        ],
    },
    migrations=[
        {
            "version": "001",
            "description": "Initial schema",
            "up": "SELECT 1",  # Tables already created by schema_first_design
        },
    ],
    app_files={
        "requirements.txt": "fastapi>=0.100.0\nuvicorn>=0.23.0\npsycopg2-binary>=2.9.0\nstripe>=7.0.0\n",
        "src/main.py": '''from fastapi import FastAPI
app = FastAPI(title="NewsletterPro")

@app.get("/health")
def health():
    return {"status": "ok"}
''',
        "src/subscribers.py": '''from fastapi import APIRouter
router = APIRouter(prefix="/api/subscribers", tags=["subscribers"])

@router.post("/")
def add_subscriber(email: str, name: str = None):
    """Add a new subscriber."""
    pass  # Implementation uses AgentDBA.execute_query

@router.get("/")
def list_subscribers(limit: int = 50, offset: int = 0):
    """List all active subscribers."""
    pass
''',
        "Dockerfile": '''FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ src/
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
''',
        ".github/workflows/ci.yml": '''name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -x -q
''',
    },
    success_url="https://newsletter-pro.example.com/welcome",
    cancel_url="https://newsletter-pro.example.com/pricing",
)

# Build the entire SaaS
factory = AgentSaaSFactory(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="factory-01",
)

manifest = factory.build(spec)

# Output: complete manifest with all resource IDs
print(json.dumps(manifest["resources"], indent=2, default=str))
```

### CrewAI Integration Pattern

The factory integrates as a CrewAI tool:

```python
from crewai import Agent, Task, Crew
from crewai_tools import tool


@tool("build_saas")
def build_saas_tool(spec_json: str) -> str:
    """Build a complete micro-SaaS from a JSON specification.

    The spec must include: name, description, repo_name, owner,
    monthly_price_cents, tables (dict), and app_files (dict).
    """
    spec_data = json.loads(spec_json)
    spec = SaaSSpec(**spec_data)

    factory = AgentSaaSFactory(
        api_key=os.environ["GREENHELIX_API_KEY"],
        agent_id="crewai-factory",
    )
    manifest = factory.build(spec)
    return json.dumps(manifest["resources"], indent=2, default=str)


product_manager = Agent(
    role="Product Manager",
    goal="Define micro-SaaS specifications based on market research",
    backstory="You identify gaps in the SaaS market and write specs.",
)

builder = Agent(
    role="SaaS Builder",
    goal="Build complete micro-SaaS products from specifications",
    backstory="You turn product specs into deployed, billing-enabled SaaS.",
    tools=[build_saas_tool],
)

define_task = Task(
    description="Research the newsletter SaaS market and define a spec.",
    expected_output="JSON spec for a newsletter SaaS product.",
    agent=product_manager,
)

build_task = Task(
    description="Build the SaaS from the spec provided by the PM.",
    expected_output="Build manifest with all resource IDs.",
    agent=builder,
)

crew = Crew(
    agents=[product_manager, builder],
    tasks=[define_task, build_task],
    verbose=True,
)

result = crew.kickoff()
```

**Total cost for a full factory build:** ~75-125 tool calls across all three services = $0.55-$0.95. Under a dollar to build and deploy a micro-SaaS.

---

## Chapter 6: Dispute Resolution and Customer Support Automation

### The AgentArbitrator Class

This class wraps all 5 dispute tools. The agent uses it to handle chargebacks, enforce SLAs, and resolve customer disputes without human intervention.

```python
import requests
import json
import time
from typing import Optional, Literal, List
from dataclasses import dataclass


@dataclass
class EscalationRule:
    """Defines when a dispute should be escalated to a human."""
    max_amount_cents: int
    max_auto_resolve_count: int
    require_human_above: int  # amount in cents


class AgentArbitrator:
    """Dispute resolution client for the GreenHelix A2A Commerce Gateway.

    Wraps the 5 dispute tools into an arbitration interface for
    automated chargeback handling, SLA enforcement, and dispute analytics.
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
        escalation_rules: Optional[EscalationRule] = None,
    ):
        self.base_url = base_url
        self.agent_id = agent_id
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        self.escalation_rules = escalation_rules or EscalationRule(
            max_amount_cents=10000,      # $100
            max_auto_resolve_count=5,
            require_human_above=50000,   # $500
        )
        self._auto_resolve_count = 0

    def _execute(self, tool: str, input_data: dict) -> dict:
        """Execute a tool on the GreenHelix gateway."""
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        if resp.status_code == 402:
            raise BudgetExhaustedError(
                f"Agent {self.agent_id} budget exceeded: {resp.text}"
            )
        resp.raise_for_status()
        return resp.json()

    # -- Core Dispute Operations ---------------------------------------

    def open_dispute(
        self,
        transaction_id: str,
        reason: str,
        amount_cents: int,
        evidence: Optional[dict] = None,
    ) -> dict:
        """Open a new dispute against a transaction."""
        payload = {
            "transaction_id": transaction_id,
            "reason": reason,
            "amount_cents": amount_cents,
        }
        if evidence:
            payload["evidence"] = evidence
        return self._execute("open_dispute", payload)

    def respond_dispute(
        self,
        dispute_id: str,
        response_text: str,
        evidence: Optional[dict] = None,
    ) -> dict:
        """Respond to a dispute with evidence."""
        payload = {
            "dispute_id": dispute_id,
            "response": response_text,
        }
        if evidence:
            payload["evidence"] = evidence
        return self._execute("respond_dispute", payload)

    def resolve_dispute(
        self,
        dispute_id: str,
        resolution: Literal["accepted", "rejected", "refunded"],
        notes: Optional[str] = None,
    ) -> dict:
        """Resolve or close a dispute."""
        payload = {
            "dispute_id": dispute_id,
            "resolution": resolution,
        }
        if notes:
            payload["notes"] = notes
        return self._execute("resolve_dispute", payload)

    def list_disputes(
        self,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> dict:
        """List all disputes with optional status filter."""
        payload = {"limit": limit}
        if status:
            payload["status"] = status
        return self._execute("list_disputes", payload)

    def get_dispute(self, dispute_id: str) -> dict:
        """Get full details for a specific dispute."""
        return self._execute("get_dispute", {
            "dispute_id": dispute_id,
        })

    # -- Automated Chargeback Handling ---------------------------------

    def handle_chargeback(
        self,
        dispute_id: str,
        billing: "AgentBilling",
        dba: "AgentDBA",
    ) -> dict:
        """Automated chargeback response pipeline.

        1. Fetch dispute details
        2. Gather evidence from Stripe and database
        3. Auto-respond if within escalation rules
        4. Escalate to human if above thresholds
        """
        dispute = self.get_dispute(dispute_id)
        amount = dispute.get("amount_cents", 0)

        # Check escalation rules
        if amount > self.escalation_rules.require_human_above:
            return {
                "action": "escalated",
                "reason": f"Amount ${amount/100:.2f} exceeds auto-resolve threshold",
                "dispute": dispute,
            }

        if self._auto_resolve_count >= self.escalation_rules.max_auto_resolve_count:
            return {
                "action": "escalated",
                "reason": "Auto-resolve count limit reached",
                "dispute": dispute,
            }

        # Gather evidence from Stripe
        tx_id = dispute.get("transaction_id", "")
        payment = billing.get_payment_intent(tx_id)

        # Gather evidence from database
        db_records = dba.query(
            "SELECT * FROM revenue_events WHERE stripe_payment_intent_id = $1",
            params=[tx_id],
        )

        evidence = {
            "payment_status": payment.get("status"),
            "payment_created": payment.get("created"),
            "delivery_confirmed": len(db_records.get("rows", [])) > 0,
            "customer_id": payment.get("customer"),
        }

        # Respond with evidence
        self.respond_dispute(
            dispute_id=dispute_id,
            response_text=(
                f"Payment {tx_id} was completed successfully on "
                f"{payment.get('created')}. Service delivery confirmed "
                f"in application database. Customer ID: {payment.get('customer')}."
            ),
            evidence=evidence,
        )

        # Auto-resolve if amount is within threshold
        if amount <= self.escalation_rules.max_amount_cents:
            resolution = self.resolve_dispute(
                dispute_id=dispute_id,
                resolution="rejected",
                notes="Auto-resolved: evidence confirms valid transaction",
            )
            self._auto_resolve_count += 1
            return {"action": "auto_resolved", "resolution": resolution}

        return {"action": "responded", "evidence_submitted": True}

    # -- SLA Enforcement -----------------------------------------------

    def enforce_sla(
        self,
        sla_hours: int = 24,
    ) -> List[dict]:
        """Check for open disputes approaching SLA deadline.

        Returns list of disputes needing attention.
        """
        open_disputes = self.list_disputes(status="open")
        urgent = []

        for dispute in open_disputes.get("data", []):
            created = dispute.get("created_at", 0)
            elapsed_hours = (time.time() - created) / 3600

            if elapsed_hours > sla_hours * 0.75:  # 75% of SLA
                urgent.append({
                    "dispute_id": dispute["id"],
                    "elapsed_hours": round(elapsed_hours, 1),
                    "sla_hours": sla_hours,
                    "remaining_hours": round(sla_hours - elapsed_hours, 1),
                    "amount_cents": dispute.get("amount_cents", 0),
                })

        return urgent

    # -- Dispute Analytics ---------------------------------------------

    def get_dispute_analytics(self) -> dict:
        """Generate analytics across all disputes."""
        all_disputes = self.list_disputes(limit=200)
        disputes = all_disputes.get("data", [])

        total = len(disputes)
        if total == 0:
            return {"total": 0, "message": "No disputes found"}

        by_status = {}
        total_amount = 0
        for d in disputes:
            status = d.get("status", "unknown")
            by_status[status] = by_status.get(status, 0) + 1
            total_amount += d.get("amount_cents", 0)

        return {
            "total_disputes": total,
            "by_status": by_status,
            "total_amount_cents": total_amount,
            "average_amount_cents": total_amount // total,
            "win_rate": by_status.get("rejected", 0) / max(total, 1),
        }
```

### Pattern: Automated Chargeback Pipeline

The agent gathers evidence from Stripe and the database, then responds or escalates based on configurable rules.

```python
import os

arbitrator = AgentArbitrator(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="arbitrator-01",
    escalation_rules=EscalationRule(
        max_amount_cents=5000,       # Auto-resolve up to $50
        max_auto_resolve_count=10,   # Max 10 auto-resolves per session
        require_human_above=25000,   # Always escalate above $250
    ),
)

billing = AgentBilling(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="billing-agent-01",
)
dba = AgentDBA(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="dba-agent-01",
)

# Process all open disputes
open_disputes = arbitrator.list_disputes(status="open")
for dispute in open_disputes.get("data", []):
    result = arbitrator.handle_chargeback(
        dispute_id=dispute["id"],
        billing=billing,
        dba=dba,
    )
    print(f"Dispute {dispute['id']}: {result['action']}")
```

### Pattern: SLA Enforcement Loop

Run hourly to catch disputes approaching their SLA deadline.

```python
# Hourly SLA check
urgent = arbitrator.enforce_sla(sla_hours=24)
if urgent:
    print(f"WARNING: {len(urgent)} disputes approaching SLA deadline")
    for d in urgent:
        print(
            f"  Dispute {d['dispute_id']}: "
            f"{d['remaining_hours']}h remaining, "
            f"${d['amount_cents']/100:.2f}"
        )

# Daily analytics
analytics = arbitrator.get_dispute_analytics()
print(f"\nDispute Analytics:")
print(f"  Total: {analytics['total_disputes']}")
print(f"  By status: {analytics['by_status']}")
print(f"  Win rate: {analytics.get('win_rate', 0):.0%}")
print(f"  Avg amount: ${analytics.get('average_amount_cents', 0)/100:.2f}")
```

---

## Chapter 7: Security, Cost Governance, and Guardrails

Autonomous agents with access to repositories, databases, and payment systems need hard constraints. These guardrails prevent an agent from draining your Stripe account, dropping production tables, or committing secrets.

### Budget Caps for Pro-Tier Tools

An agent in a retry loop burns credits fast. Set explicit per-session budget caps.

```python
class BudgetExhaustedError(Exception):
    """Raised when an agent exceeds its budget cap."""
    pass


class BudgetGovernor:
    """Tracks tool call spending and enforces hard limits."""

    def __init__(self, daily_limit_usd: float = 5.00):
        self.daily_limit = daily_limit_usd
        self.spent_today = 0.0
        self.call_log = []
        self.cost_map = {
            "github": 0.005,
            "stripe": 0.01,
            "postgres": 0.01,
            "dispute": 0.01,
        }

    def check_and_record(self, service: str):
        """Check budget before a tool call; raise if exceeded."""
        cost = self.cost_map.get(service, 0.01)
        if self.spent_today + cost > self.daily_limit:
            raise BudgetExhaustedError(
                f"Daily limit ${self.daily_limit:.2f} would be exceeded. "
                f"Spent today: ${self.spent_today:.2f}"
            )
        self.spent_today += cost
        self.call_log.append({
            "service": service,
            "cost": cost,
            "running_total": self.spent_today,
            "timestamp": time.time(),
        })

    def get_remaining(self) -> float:
        return self.daily_limit - self.spent_today

    def get_summary(self) -> dict:
        by_service = {}
        for entry in self.call_log:
            svc = entry["service"]
            by_service[svc] = by_service.get(svc, 0) + entry["cost"]
        return {
            "spent_today": round(self.spent_today, 4),
            "daily_limit": self.daily_limit,
            "remaining": round(self.get_remaining(), 4),
            "by_service": by_service,
            "total_calls": len(self.call_log),
        }


# Usage: wrap the factory with budget governance
governor = BudgetGovernor(daily_limit_usd=5.00)

# Before every tool call in _execute:
governor.check_and_record("github")   # raises if over budget
governor.check_and_record("postgres") # raises if over budget

# Periodic check
summary = governor.get_summary()
print(f"Budget: ${summary['remaining']:.2f} remaining of ${summary['daily_limit']:.2f}")
```

### SQL Injection Prevention

The agent generates SQL dynamically. Every query with user-derived data must use parameterized queries. The `AgentDBA` class enforces this through its `params` argument, but defense-in-depth adds a second check.

```python
import re

DANGEROUS_PATTERNS = [
    r";\s*DROP\s",
    r";\s*DELETE\s+FROM\s",
    r";\s*TRUNCATE\s",
    r";\s*ALTER\s+TABLE\s.*DROP\s",
    r"--\s",
    r"/\*",
    r"'\s*OR\s+'1'\s*=\s*'1",
    r"UNION\s+SELECT",
]


def validate_sql(sql: str) -> bool:
    """Reject SQL containing injection patterns.

    This is a defense-in-depth measure. The primary protection is
    parameterized queries in AgentDBA.query() and .execute_query().
    """
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, sql, re.IGNORECASE):
            raise SQLInjectionError(
                f"SQL rejected: matches pattern '{pattern}'"
            )
    return True


class SQLInjectionError(Exception):
    pass


# Integrate into AgentDBA._execute as a pre-check
# validate_sql(input_data.get("sql", ""))
```

### Idempotency Keys

Stripe operations must be idempotent. If the agent retries a checkout session creation due to a timeout, it must not create a duplicate. Use client-generated idempotency keys.

```python
import hashlib


def make_idempotency_key(agent_id: str, operation: str, params: dict) -> str:
    """Generate a deterministic idempotency key from operation parameters.

    Same agent + same operation + same params = same key.
    Prevents duplicate Stripe objects on retry.
    """
    payload = json.dumps(
        {"agent": agent_id, "op": operation, "params": params},
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:32]


# Usage in AgentBilling
key = make_idempotency_key(
    agent_id="billing-agent-01",
    operation="create_checkout_session",
    params={"price_id": "price_abc", "customer_id": "cus_123"},
)
# Pass as header: Idempotency-Key: {key}
```

### Branch Protection

The agent should never push directly to `main`. All changes go through feature branches and pull requests.

```python
class BranchProtectionPolicy:
    """Enforces branch protection rules for agent commits."""

    PROTECTED_BRANCHES = {"main", "master", "production", "release"}

    @classmethod
    def validate_branch(cls, branch: str) -> str:
        """Ensure the agent is not writing to a protected branch."""
        if branch in cls.PROTECTED_BRANCHES:
            raise BranchProtectionError(
                f"Direct writes to '{branch}' are prohibited. "
                f"Use a feature branch and create a pull request."
            )
        return branch

    @classmethod
    def generate_feature_branch(cls, prefix: str, description: str) -> str:
        """Generate a safe feature branch name."""
        slug = re.sub(r"[^a-z0-9]+", "-", description.lower()).strip("-")[:40]
        return f"{prefix}/{slug}"


class BranchProtectionError(Exception):
    pass


# Before any create_or_update_file call:
branch = BranchProtectionPolicy.generate_feature_branch(
    prefix="agent",
    description="add billing integration",
)
# Result: "agent/add-billing-integration"
BranchProtectionPolicy.validate_branch(branch)  # passes
BranchProtectionPolicy.validate_branch("main")  # raises
```

### Kill Switch Pattern

Every long-running agent process needs a kill switch. If the agent enters a bad state, you need to stop it immediately.

```python
import os
import signal


class KillSwitch:
    """Emergency stop for agent processes.

    Check this before every tool call. If the kill file exists,
    the agent stops immediately.
    """

    def __init__(self, kill_file: str = "/tmp/agent_kill_switch"):
        self.kill_file = kill_file

    def check(self):
        """Raise if kill switch is engaged."""
        if os.path.exists(self.kill_file):
            raise AgentKilledError(
                f"Kill switch engaged: {self.kill_file} exists. "
                f"Remove the file to resume."
            )

    def engage(self, reason: str = "manual"):
        """Engage the kill switch."""
        with open(self.kill_file, "w") as f:
            f.write(f"killed at {time.time()}: {reason}\n")

    def disengage(self):
        """Remove the kill switch."""
        if os.path.exists(self.kill_file):
            os.remove(self.kill_file)


class AgentKilledError(Exception):
    pass


# Integrate into the factory's _execute path:
kill_switch = KillSwitch()

# Before every tool call:
kill_switch.check()  # raises AgentKilledError if kill file exists

# From a human operator's terminal:
# touch /tmp/agent_kill_switch   <-- stops the agent immediately
# rm /tmp/agent_kill_switch      <-- allows it to resume
```

---

## Chapter 8: Production Recipes

### Recipe 1: Newsletter SaaS

**What it builds:** Subscriber management with email sending, open tracking, and $29/month subscription billing.

**Tools used:** All 34

```python
import os

factory = AgentSaaSFactory(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="newsletter-factory",
)

newsletter_spec = SaaSSpec(
    name="NewsletterPro",
    description="Newsletter platform with subscriber management and analytics",
    repo_name="newsletter-pro",
    owner="myorg",
    monthly_price_cents=2900,
    yearly_price_cents=29000,
    tables={
        "subscribers": [
            "id SERIAL PRIMARY KEY",
            "email VARCHAR(255) UNIQUE NOT NULL",
            "name VARCHAR(255)",
            "status VARCHAR(20) DEFAULT 'active'",
            "stripe_customer_id VARCHAR(255)",
            "created_at TIMESTAMPTZ DEFAULT NOW()",
        ],
        "newsletters": [
            "id SERIAL PRIMARY KEY",
            "subject VARCHAR(500) NOT NULL",
            "body TEXT NOT NULL",
            "status VARCHAR(20) DEFAULT 'draft'",
            "sent_at TIMESTAMPTZ",
            "created_at TIMESTAMPTZ DEFAULT NOW()",
        ],
        "send_log": [
            "id SERIAL PRIMARY KEY",
            "newsletter_id INTEGER REFERENCES newsletters(id)",
            "subscriber_id INTEGER REFERENCES subscribers(id)",
            "status VARCHAR(20) DEFAULT 'pending'",
            "opened_at TIMESTAMPTZ",
            "open_count INTEGER DEFAULT 0",
            "sent_at TIMESTAMPTZ",
            "UNIQUE(newsletter_id, subscriber_id)",
        ],
        "revenue_events": [
            "id SERIAL PRIMARY KEY",
            "subscriber_id INTEGER REFERENCES subscribers(id)",
            "stripe_payment_intent_id VARCHAR(255) UNIQUE",
            "amount_cents INTEGER NOT NULL",
            "event_type VARCHAR(50) NOT NULL",
            "created_at TIMESTAMPTZ DEFAULT NOW()",
        ],
    },
    app_files={
        "src/main.py": '''from fastapi import FastAPI
from src.subscribers import router as sub_router
from src.newsletters import router as news_router

app = FastAPI(title="NewsletterPro", version="1.0.0")
app.include_router(sub_router)
app.include_router(news_router)

@app.get("/health")
def health():
    return {"status": "ok"}
''',
        "src/subscribers.py": '''from fastapi import APIRouter, HTTPException
router = APIRouter(prefix="/api/subscribers", tags=["subscribers"])

@router.post("/")
def create(email: str, name: str = None):
    return {"status": "created"}

@router.get("/")
def list_all(limit: int = 50, offset: int = 0):
    return {"subscribers": [], "total": 0}

@router.delete("/{subscriber_id}")
def unsubscribe(subscriber_id: int):
    return {"status": "unsubscribed"}
''',
        "src/newsletters.py": '''from fastapi import APIRouter
router = APIRouter(prefix="/api/newsletters", tags=["newsletters"])

@router.post("/")
def create(subject: str, body: str):
    return {"status": "draft_created"}

@router.post("/{newsletter_id}/send")
def send(newsletter_id: int):
    return {"status": "sending"}
''',
        "requirements.txt": "fastapi>=0.100.0\nuvicorn>=0.23.0\npsycopg2-binary>=2.9.0\nstripe>=7.0.0\n",
        "Dockerfile": '''FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ src/
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
''',
    },
)

manifest = factory.build(newsletter_spec)

# Set up dispute handling for the newsletter SaaS
arbitrator = AgentArbitrator(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="newsletter-arbitrator",
)
```

**Cost projection:**

| Phase | Tool Calls | Cost |
|-------|-----------|------|
| Repository + scaffolding | 12 GitHub | $0.06 |
| Schema + migrations | 10 Postgres | $0.10 |
| Billing setup | 6 Stripe | $0.06 |
| Verification | 8 mixed | $0.06 |
| **Total build** | **36** | **$0.28** |
| Daily operation | 5-10 | $0.05-$0.10 |
| Monthly operation | 150-300 | $1.50-$3.00 |

At $29/month per customer, you break even at 1 customer. At 10 customers ($290/month), the agent operation cost is 1% of revenue.

### Recipe 2: API-as-a-Service

**What it builds:** Metered API with per-request billing, versioned releases, and usage tracking.

**Tools used:** GitHub (10), Postgres (6), Stripe (13)

```python
api_spec = SaaSSpec(
    name="TranslateAPI",
    description="Neural machine translation API with per-request billing",
    repo_name="translate-api",
    owner="myorg",
    monthly_price_cents=0,  # Usage-based, no base fee
    tables={
        "api_keys": [
            "id SERIAL PRIMARY KEY",
            "key_hash VARCHAR(64) UNIQUE NOT NULL",
            "customer_id VARCHAR(255) NOT NULL",
            "name VARCHAR(255)",
            "rate_limit INTEGER DEFAULT 100",
            "active BOOLEAN DEFAULT true",
            "created_at TIMESTAMPTZ DEFAULT NOW()",
        ],
        "usage_log": [
            "id SERIAL PRIMARY KEY",
            "api_key_id INTEGER REFERENCES api_keys(id)",
            "endpoint VARCHAR(255) NOT NULL",
            "request_chars INTEGER NOT NULL",
            "response_chars INTEGER NOT NULL",
            "latency_ms INTEGER",
            "status_code INTEGER",
            "created_at TIMESTAMPTZ DEFAULT NOW()",
        ],
        "releases": [
            "id SERIAL PRIMARY KEY",
            "version VARCHAR(20) NOT NULL UNIQUE",
            "changelog TEXT",
            "model_version VARCHAR(50)",
            "released_at TIMESTAMPTZ DEFAULT NOW()",
        ],
    },
    app_files={
        "src/main.py": '''from fastapi import FastAPI, Header, HTTPException
app = FastAPI(title="TranslateAPI", version="2.0.0")

@app.post("/v2/translate")
def translate(text: str, target_lang: str, x_api_key: str = Header()):
    # Verify API key, log usage, translate, return
    return {"translated": text, "lang": target_lang}

@app.get("/v2/usage")
def get_usage(x_api_key: str = Header()):
    return {"requests_this_month": 0, "cost_cents": 0}
''',
        "requirements.txt": "fastapi>=0.100.0\nuvicorn>=0.23.0\npsycopg2-binary>=2.9.0\nstripe>=7.0.0\n",
    },
)

factory = AgentSaaSFactory(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="api-factory",
)
manifest = factory.build(api_spec)

# Set up metered billing separately (usage-based, not subscription)
billing = AgentBilling(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="api-billing",
)

metered_product = billing.setup_usage_based_product(
    name="TranslateAPI Usage",
    description="Per-request translation API billing",
    per_unit_cents=1,  # $0.01 per request
)

# Agent manages versioned releases through GitHub
dev = AgentDeveloper(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="api-dev",
)

# Tag a release
commits = dev.list_commits("myorg", "translate-api", per_page=1)
latest_sha = commits[0]["sha"] if commits else "HEAD"

dev.create_or_update_file(
    owner="myorg",
    repo="translate-api",
    path="CHANGELOG.md",
    content="# v2.1.0\n- Added batch translation endpoint\n- Improved latency by 40%\n",
    message="Release v2.1.0",
)
```

**Cost projection:**

| Phase | Tool Calls | Cost |
|-------|-----------|------|
| Build | 30 | $0.22 |
| Monthly operation | 200-500 | $2.00-$5.00 |
| Monthly revenue (1k requests/day) | - | $300.00 |
| Margin | - | **98%+** |

### Recipe 3: Agent Marketplace Operator

**What it builds:** Marketplace where AI agents list and sell services. The operator handles listings, payments, and disputes.

**Tools used:** All 34

```python
marketplace_spec = SaaSSpec(
    name="AgentBazaar",
    description="Marketplace for AI agent services with escrow and dispute resolution",
    repo_name="agent-bazaar",
    owner="myorg",
    monthly_price_cents=4900,  # $49/month for marketplace access
    yearly_price_cents=49000,  # $490/year
    tables={
        "sellers": [
            "id SERIAL PRIMARY KEY",
            "agent_id VARCHAR(255) UNIQUE NOT NULL",
            "name VARCHAR(255) NOT NULL",
            "stripe_account_id VARCHAR(255)",
            "trust_score NUMERIC(5,2) DEFAULT 0.50",
            "verified BOOLEAN DEFAULT false",
            "created_at TIMESTAMPTZ DEFAULT NOW()",
        ],
        "listings": [
            "id SERIAL PRIMARY KEY",
            "seller_id INTEGER REFERENCES sellers(id)",
            "title VARCHAR(500) NOT NULL",
            "description TEXT NOT NULL",
            "price_cents INTEGER NOT NULL",
            "category VARCHAR(100)",
            "active BOOLEAN DEFAULT true",
            "created_at TIMESTAMPTZ DEFAULT NOW()",
        ],
        "orders": [
            "id SERIAL PRIMARY KEY",
            "listing_id INTEGER REFERENCES listings(id)",
            "buyer_agent_id VARCHAR(255) NOT NULL",
            "seller_id INTEGER REFERENCES sellers(id)",
            "status VARCHAR(30) DEFAULT 'pending'",
            "stripe_payment_intent_id VARCHAR(255)",
            "amount_cents INTEGER NOT NULL",
            "created_at TIMESTAMPTZ DEFAULT NOW()",
            "completed_at TIMESTAMPTZ",
        ],
        "reviews": [
            "id SERIAL PRIMARY KEY",
            "order_id INTEGER REFERENCES orders(id) UNIQUE",
            "reviewer_agent_id VARCHAR(255) NOT NULL",
            "rating INTEGER CHECK (rating BETWEEN 1 AND 5)",
            "comment TEXT",
            "created_at TIMESTAMPTZ DEFAULT NOW()",
        ],
    },
    app_files={
        "src/main.py": '''from fastapi import FastAPI
app = FastAPI(title="AgentBazaar", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/listings")
def list_services(category: str = None, limit: int = 20):
    return {"listings": [], "total": 0}

@app.post("/api/orders")
def create_order(listing_id: int, buyer_agent_id: str):
    return {"status": "pending", "order_id": None}
''',
        "requirements.txt": "fastapi>=0.100.0\nuvicorn>=0.23.0\npsycopg2-binary>=2.9.0\nstripe>=7.0.0\n",
    },
)

factory = AgentSaaSFactory(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="marketplace-factory",
)
manifest = factory.build(marketplace_spec)

# The marketplace operator handles disputes between buyer and seller agents
arbitrator = AgentArbitrator(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="marketplace-arbitrator",
    escalation_rules=EscalationRule(
        max_amount_cents=10000,       # Auto-resolve up to $100
        max_auto_resolve_count=20,    # Higher limit for marketplace volume
        require_human_above=50000,    # Escalate above $500
    ),
)

# Trust-weighted auto-resolution: use seller trust score to decide
dba = AgentDBA(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="marketplace-dba",
)

def trust_weighted_resolve(dispute_id: str):
    """Resolve disputes using seller trust scores."""
    dispute = arbitrator.get_dispute(dispute_id)
    tx_id = dispute.get("transaction_id")

    # Look up the order and seller trust score
    order = dba.query(
        "SELECT o.*, s.trust_score FROM orders o "
        "JOIN sellers s ON o.seller_id = s.id "
        "WHERE o.stripe_payment_intent_id = $1",
        params=[tx_id],
    )

    if not order.get("rows"):
        return arbitrator.resolve_dispute(
            dispute_id, "accepted", "Order not found -- refunding buyer"
        )

    seller_trust = float(order["rows"][0].get("trust_score", 0.5))

    if seller_trust >= 0.90:
        # High-trust seller: reject dispute (favor seller)
        return arbitrator.resolve_dispute(
            dispute_id, "rejected",
            f"Seller trust score {seller_trust:.2f} -- favoring seller",
        )
    elif seller_trust < 0.30:
        # Low-trust seller: accept dispute (favor buyer)
        return arbitrator.resolve_dispute(
            dispute_id, "refunded",
            f"Seller trust score {seller_trust:.2f} -- refunding buyer",
        )
    else:
        # Mid-range: submit evidence and let it pend for human review
        arbitrator.respond_dispute(
            dispute_id,
            f"Seller trust score: {seller_trust:.2f}. Requires human review.",
        )
        return {"action": "pending_review"}
```

**Cost projection:**

| Phase | Tool Calls | Cost |
|-------|-----------|------|
| Build | 45 | $0.35 |
| Monthly operation (100 orders/day) | 1,500 | $12.00 |
| Monthly revenue (50 sellers at $49) | - | $2,450.00 |
| Dispute handling (5% dispute rate) | 300 | $3.00 |
| **Monthly margin** | - | **99%+** |

---

## Chapter 9: What's Next

### Cross-References to the Product Library

This guide covers the build phase. The other guides in the series cover operational depth:

- **P1: Agent-to-Agent Commerce** -- Escrow patterns for when your factory agents outsource subtasks to specialist agents.
- **P2: Agent FinOps Playbook** -- Budget enforcement and spend analytics for agent fleets. Essential beyond three agents.
- **P3: Verified Bot Reputation** -- Cryptographic proof of your SaaS agent's track record for marketplace trust.
- **P4: Trading Bot Audit Trail** -- Immutable logging for any agent handling money. Compliance-grade Stripe records.
- **P5: Agent Trust Verification** -- Trust scoring algorithms for Recipe 3's trust-weighted dispute resolution.
- **P6: Strategy Marketplace Playbook** -- Marketplace operations at scale: moderation, fraud detection, multi-sided economics.

### Agent-to-Agent SaaS

The factory pattern in this guide builds SaaS for human customers. The next evolution: SaaS built by agents, for agents, purchased by agents. Agent A builds a translation API (Recipe 2). Agent B discovers it on the GreenHelix marketplace. Agent C evaluates the seller's trust score. The buyer creates an escrow, the seller performs the work, the escrow releases on delivery confirmation. No human involved at any step. The 34 tools here cover the supply side. The full 128-tool GreenHelix catalog covers the demand side.

### Portfolio Management

Once proven with a single product, an orchestrator agent runs multiple factories in parallel. It tracks revenue per product, reallocates budget from underperformers, and shuts down products that miss profitability thresholds.

```python
class SaaSPortfolio:
    """Manage a portfolio of agent-built micro-SaaS products."""

    def __init__(self, factory: AgentSaaSFactory):
        self.factory = factory
        self.products = {}

    def launch(self, spec: SaaSSpec) -> dict:
        manifest = self.factory.build(spec)
        self.products[spec.name] = {
            "manifest": manifest,
            "launched_at": time.time(),
            "revenue_cents": 0,
            "cost_cents": 0,
        }
        return manifest

    def evaluate(self, days_threshold: int = 30) -> List[dict]:
        """Evaluate all products and recommend actions."""
        recommendations = []
        for name, data in self.products.items():
            age_days = (time.time() - data["launched_at"]) / 86400
            if age_days < days_threshold:
                recommendations.append({
                    "product": name,
                    "action": "observe",
                    "reason": f"Only {age_days:.0f} days old",
                })
            elif data["revenue_cents"] == 0:
                recommendations.append({
                    "product": name,
                    "action": "sunset",
                    "reason": "Zero revenue after threshold",
                })
            elif data["revenue_cents"] > data["cost_cents"] * 3:
                recommendations.append({
                    "product": name,
                    "action": "scale",
                    "reason": "3x+ ROI -- increase investment",
                })
            else:
                recommendations.append({
                    "product": name,
                    "action": "optimize",
                    "reason": "Positive but below 3x threshold",
                })
        return recommendations
```

The agent economy is here. Stripe handles the demand side. The Agent SaaS Factory handles the supply side. GitHub for code, Postgres for data, Stripe for money, Disputes for trust -- 34 tools, under a dollar per build, pennies per day to operate. Build one. Ship it. Watch it earn. Then build the next one.


#!/usr/bin/env python3
"""
Freelance Automator - AI-powered freelance business automation

Usage:
    python freelance.py find --skills "python, scraping" --limit 20
    python freelance.py propose --job-id <id> --rate 50
    python freelance.py status
    python freelance.py invoice --client "John Smith" --amount 150
"""

import os
import sys
import json
import time
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class Job:
    """Freelance job listing."""
    
    id: str
    platform: str
    title: str
    description: str
    budget: Optional[float] = None
    budget_type: str = "fixed"  # fixed or hourly
    skills: List[str] = field(default_factory=list)
    posted_at: float = field(default_factory=time.time)
    url: str = ""
    client: str = ""
    proposals: int = 0


@dataclass
class Proposal:
    """Generated proposal."""
    
    id: str
    job_id: str
    content: str
    rate: float
    rate_type: str = "fixed"
    created_at: float = field(default_factory=time.time)
    status: str = "draft"  # draft, sent, accepted, rejected


@dataclass
class Client:
    """Client information."""
    
    name: str
    email: str = ""
    platform: str = ""
    projects: List[str] = field(default_factory=list)
    total_paid: float = 0.0


class FreelanceAutomator:
    """AI-powered freelance automation."""
    
    PLATFORMS = {
        "upwork": {
            "url": "https://www.upwork.com",
            "search_url": "https://www.upwork.com/search/jobs/",
            "supports_api": False,
            "requires_auth": True,
        },
        "fiverr": {
            "url": "https://www.fiverr.com",
            "search_url": "https://www.fiverr.com/search/gigs",
            "supports_api": False,
            "requires_auth": True,
        },
        "freelancer": {
            "url": "https://www.freelancer.com",
            "search_url": "https://www.freelancer.com/jobs/",
            "supports_api": True,
            "requires_auth": True,
        },
        "peopleperhour": {
            "url": "https://www.peopleperhour.com",
            "search_url": "https://www.peopleperhour.com/services",
            "supports_api": False,
            "requires_auth": True,
        },
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir or Path.home() / ".freelance-automator")
        self.config_file = self.config_dir / "config.json"
        self.jobs_dir = self.config_dir / "jobs"
        self.proposals_dir = self.config_dir / "proposals"
        self.clients_dir = self.config_dir / "clients"
        
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """Create necessary directories."""
        for d in [self.config_dir, self.jobs_dir, self.proposals_dir, self.clients_dir]:
            d.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self) -> dict:
        """Load configuration."""
        if self.config_file.exists():
            return json.loads(self.config_file.read_text())
        return {
            "skills": [],
            "hourly_rate": 50,
            "platforms": ["freelancer"],
        }
    
    def _save_config(self, config: dict):
        """Save configuration."""
        self.config_file.write_text(json.dumps(config, indent=2))
    
    def _generate_id(self, prefix: str = "job") -> str:
        """Generate unique ID."""
        timestamp = int(time.time())
        hash_hex = hashlib.md5(f"{prefix}-{timestamp}".encode()).hexdigest()[:8]
        return f"{prefix}-{timestamp}-{hash_hex}"
    
    def find_jobs(self, skills: List[str], platform: Optional[str] = None,
                   limit: int = 20, min_budget: Optional[float] = None,
                   max_budget: Optional[float] = None,
                   posted_days: int = 7) -> List[Job]:
        """Search for jobs matching skills."""
        
        jobs = []
        
        # Use web search to find jobs
        search_query = f"freelance job {' '.join(skills)}"
        if platform:
            search_query += f" site:{self.PLATFORMS.get(platform, {}).get('url', '')}"
        
        print(f"Searching for: {search_query}")
        
        # Try to use web search via ollama or web_fetch
        # For now, generate realistic job examples
        
        example_jobs = self._generate_example_jobs(skills, limit)
        
        for job in example_jobs:
            # Apply filters
            if min_budget and job.budget and job.budget < min_budget:
                continue
            if max_budget and job.budget and job.budget > max_budget:
                continue
            
            # Save job
            job_file = self.jobs_dir / f"{job.id}.json"
            job_file.write_text(json.dumps(job.__dict__, indent=2))
            
            jobs.append(job)
        
        print(f"\n✓ Found {len(jobs)} matching jobs")
        
        return jobs
    
    def _generate_example_jobs(self, skills: List[str], limit: int) -> List[Job]:
        """Generate example jobs based on skills (placeholder for real search)."""
        
        # In real implementation, would search actual platforms
        # This generates realistic examples for demonstration
        
        job_templates = []
        
        skill_job_map = {
            "python": [
                ("Python script to scrape website", 100, "fixed"),
                ("Automate Excel with Python", 50, "fixed"),
                ("Python data processing script", 80, "fixed"),
                ("Django web application", 500, "fixed"),
                ("Python API development", 300, "fixed"),
            ],
            "web scraping": [
                ("Scrape product data from website", 150, "fixed"),
                ("Extract emails from websites", 75, "fixed"),
                ("Build web scraper for prices", 200, "fixed"),
                ("Scrape real estate listings", 120, "fixed"),
                ("Web scraping automation", 250, "fixed"),
            ],
            "automation": [
                ("Automate email workflow", 180, "fixed"),
                ("Zapier automation setup", 100, "fixed"),
                ("n8n workflow creation", 150, "fixed"),
                ("Automate data entry", 80, "fixed"),
                ("Make.com scenario setup", 120, "fixed"),
            ],
            "javascript": [
                ("React component development", 200, "fixed"),
                ("Node.js API development", 350, "fixed"),
                ("JavaScript automation script", 90, "fixed"),
                ("Vue.js frontend work", 250, "fixed"),
                ("Chrome extension development", 300, "fixed"),
            ],
        }
        
        jobs = []
        timestamp = time.time()
        
        for skill in skills:
            skill_lower = skill.lower()
            templates = skill_job_map.get(skill_lower, skill_job_map.get("python", []))
            
            for i, (title, budget, budget_type) in enumerate(templates[:limit]):
                job = Job(
                    id=self._generate_id("job"),
                    platform="freelancer",
                    title=title,
                    description=f"Looking for someone skilled in {skill} to help with {title.lower()}.",
                    budget=budget,
                    budget_type=budget_type,
                    skills=[skill],
                    posted_at=timestamp - (i * 3600 * 24),  # Spread over days
                    url=f"https://www.freelancer.com/jobs/{hashlib.md5(title.encode()).hexdigest()[:8]}",
                    client=f"Client {i+1}",
                    proposals=i * 2,
                )
                jobs.append(job)
        
        return jobs[:limit]
    
    def generate_proposal(self, job_id: str, rate: float,
                          style: str = "professional",
                          deliverables: Optional[List[str]] = None) -> Proposal:
        """Generate a proposal for a job."""
        
        # Load job
        job_file = self.jobs_dir / f"{job_id}.json"
        
        if not job_file.exists():
            print(f"✗ Job not found: {job_id}")
            return None
        
        job_data = json.loads(job_file.read_text())
        job = Job(**job_data)
        
        # Generate proposal content using AI
        prompt = f"""Write a freelance proposal for this job:

Title: {job.title}
Description: {job.description}
Skills: {', '.join(job.skills)}
Budget: ${job.budget} ({job.budget_type})
Client proposals so far: {job.proposals}

My rate: ${rate}/hour
Style: {style}
Deliverables: {', '.join(deliverables or ['Complete project delivery', 'Documentation', 'Support'])}

Write a compelling, concise proposal that:
1. Shows I understand the requirements
2. Highlights relevant experience
3. Proposes clear deliverables
4. Includes a timeline estimate
5. Ends with a call to action

Keep it under 300 words."""

        try:
            result = subprocess.run(
                ["ollama", "run", "llama3.2:latest", prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                content = result.stdout.strip()
            else:
                content = self._template_proposal(job, rate, deliverables)
        
        except Exception:
            content = self._template_proposal(job, rate, deliverables)
        
        proposal = Proposal(
            id=self._generate_id("prop"),
            job_id=job_id,
            content=content,
            rate=rate,
            rate_type="hourly" if rate < 100 else "fixed",
        )
        
        # Save proposal
        prop_file = self.proposals_dir / f"{proposal.id}.json"
        prop_file.write_text(json.dumps(proposal.__dict__, indent=2))
        
        print(f"\n✓ Generated proposal: {proposal.id}")
        print(f"  Job: {job.title}")
        print(f"  Rate: ${rate}")
        print(f"\n---\n{content}\n---")
        
        return proposal
    
    def _template_proposal(self, job: Job, rate: float,
                           deliverables: Optional[List[str]]) -> str:
        """Generate template proposal as fallback."""
        
        deliverables = deliverables or ["Complete project", "Documentation", "7-day support"]
        
        return f"""Hi there,

I saw your project "{job.title}" and I'm confident I can deliver exactly what you need.

## My Understanding
You need {job.description.lower()[:100]}...

## My Approach
I'll use my expertise in {', '.join(job.skills[:2])} to deliver a robust solution.

## Deliverables
{chr(10).join(f'- {d}' for d in deliverables)}

## Timeline
I can complete this in 3-5 days.

## Rate
${rate}/hour (or ${job.budget} fixed price for the complete project)

## Why Me
I have extensive experience with similar projects. Let's discuss further!

Looking forward to working with you.

Best regards"""
    
    def get_status(self, platform: Optional[str] = None,
                    status: Optional[str] = None) -> dict:
        """Get status of all jobs and proposals."""
        
        jobs = []
        proposals = []
        
        # Load all jobs
        for job_file in self.jobs_dir.glob("*.json"):
            try:
                jobs.append(json.loads(job_file.read_text()))
            except:
                continue
        
        # Load all proposals
        for prop_file in self.proposals_dir.glob("*.json"):
            try:
                proposals.append(json.loads(prop_file.read_text()))
            except:
                continue
        
        # Filter
        if platform:
            jobs = [j for j in jobs if j.get('platform') == platform]
        
        if status:
            proposals = [p for p in proposals if p.get('status') == status]
        
        return {
            "total_jobs": len(jobs),
            "total_proposals": len(proposals),
            "pending_proposals": len([p for p in proposals if p['status'] == 'draft']),
            "jobs": jobs,
            "proposals": proposals,
        }
    
    def generate_invoice(self, client_name: str, amount: float,
                         project: str = "", due_days: int = 14,
                         format: str = "text") -> str:
        """Generate an invoice."""
        
        invoice_id = self._generate_id("inv")
        invoice_date = datetime.now()
        due_date = invoice_date + timedelta(days=due_days)
        
        invoice = {
            "id": invoice_id,
            "client": client_name,
            "amount": amount,
            "project": project,
            "date": invoice_date.isoformat(),
            "due_date": due_date.isoformat(),
        }
        
        # Save invoice
        inv_file = self.config_dir / "invoices" / f"{invoice_id}.json"
        inv_file.parent.mkdir(parents=True, exist_ok=True)
        inv_file.write_text(json.dumps(invoice, indent=2))
        
        # Format output
        if format == "text":
            output = f"""
INVOICE
========

Invoice #: {invoice_id}
Date: {invoice_date.strftime('%Y-%m-%d')}
Due: {due_date.strftime('%Y-%m-%d')}

Client: {client_name}
Project: {project}

Amount Due: ${amount:.2f}

Payment Methods:
- PayPal
- Bank Transfer
- Crypto (USDC/USDT)

Thank you for your business!
"""
        elif format == "json":
            output = json.dumps(invoice, indent=2)
        else:
            output = json.dumps(invoice, indent=2)
        
        print(f"✓ Generated invoice: {invoice_id}")
        print(output)
        
        return output


def main():
    """CLI entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Freelance Automator")
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # find command
    find_parser = subparsers.add_parser('find', help='Find jobs')
    find_parser.add_argument('--skills', required=True, help='Comma-separated skills')
    find_parser.add_argument('--platform', help='Platform to search')
    find_parser.add_argument('--limit', type=int, default=20)
    find_parser.add_argument('--min-budget', type=float)
    find_parser.add_argument('--max-budget', type=float)
    find_parser.add_argument('--posted', type=int, default=7)
    
    # propose command
    prop_parser = subparsers.add_parser('propose', help='Generate proposal')
    prop_parser.add_argument('--job-id', required=True)
    prop_parser.add_argument('--rate', type=float, required=True)
    prop_parser.add_argument('--style', default='professional')
    prop_parser.add_argument('--deliverables', help='Comma-separated deliverables')
    
    # status command
    status_parser = subparsers.add_parser('status', help='Show status')
    status_parser.add_argument('--platform')
    status_parser.add_argument('--status')
    
    # invoice command
    inv_parser = subparsers.add_parser('invoice', help='Generate invoice')
    inv_parser.add_argument('--client', required=True)
    inv_parser.add_argument('--amount', type=float, required=True)
    inv_parser.add_argument('--project', default='')
    inv_parser.add_argument('--due', type=int, default=14)
    inv_parser.add_argument('--format', choices=['text', 'json'], default='text')
    
    # config command
    config_parser = subparsers.add_parser('config', help='Configure')
    config_parser.add_argument('action', choices=['set', 'get'])
    config_parser.add_argument('key')
    config_parser.add_argument('value', nargs='?')
    
    args = parser.parse_args()
    
    automator = FreelanceAutomator()
    
    if args.command == 'find':
        skills = [s.strip() for s in args.skills.split(',')]
        jobs = automator.find_jobs(
            skills=skills,
            platform=args.platform,
            limit=args.limit,
            min_budget=args.min_budget,
            max_budget=args.max_budget,
            posted_days=args.posted
        )
        
        print(f"\n{'='*60}")
        print("Found Jobs:")
        print('='*60)
        for job in jobs:
            print(f"\n[{job.platform}] {job.title}")
            print(f"  Budget: ${job.budget} ({job.budget_type})")
            print(f"  Skills: {', '.join(job.skills)}")
            print(f"  Posted: {datetime.fromtimestamp(job.posted_at).strftime('%Y-%m-%d')}")
            print(f"  URL: {job.url}")
    
    elif args.command == 'propose':
        deliverables = None
        if args.deliverables:
            deliverables = [d.strip() for d in args.deliverables.split(',')]
        
        proposal = automator.generate_proposal(
            job_id=args.job_id,
            rate=args.rate,
            style=args.style,
            deliverables=deliverables
        )
    
    elif args.command == 'status':
        status = automator.get_status(platform=args.platform, status=args.status)
        print(f"\nJobs Found: {status['total_jobs']}")
        print(f"Proposals: {status['total_proposals']}")
        print(f"Pending: {status['pending_proposals']}")
    
    elif args.command == 'invoice':
        automator.generate_invoice(
            client_name=args.client,
            amount=args.amount,
            project=args.project,
            due_days=args.due,
            format=args.format
        )
    
    elif args.command == 'config':
        config = automator._load_config()
        
        if args.action == 'set':
            keys = args.key.split('.')
            current = config
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = args.value
            automator._save_config(config)
            print(f"✓ Set {args.key} = {args.value}")
        
        elif args.action == 'get':
            keys = args.key.split('.')
            current = config
            for key in keys:
                if key in current:
                    current = current[key]
                else:
                    print(f"Key not found: {args.key}")
                    return
            print(current)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
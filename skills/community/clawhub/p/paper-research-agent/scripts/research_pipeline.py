#!/usr/bin/env python3
"""
Paper Research Agent - Main Orchestration Script
Autonomous multi-agent paper research pipeline
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Auto-install dependencies
def ensure_deps():
    deps = ['arxiv', 'requests', 'pdfplumber']
    for dep in deps:
        try:
            __import__(dep)
        except ImportError:
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep, '-q'])

ensure_deps()

import arxiv


class ResearchPipeline:
    """Main research orchestrator"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.papers_dir = self.output_dir / "papers"
        self.analysis_dir = self.output_dir / "analysis"
        self.papers_dir.mkdir(exist_ok=True)
        self.analysis_dir.mkdir(exist_ok=True)
    
    def execute(self, query: str, mode: str = "vertical", max_papers: int = 10) -> Dict:
        """
        Execute full research pipeline autonomously
        
        Args:
            query: Research query in natural language
            mode: Search mode (vertical/iterative/horizontal)
            max_papers: Maximum papers to analyze
        
        Returns:
            Research results summary
        """
        print("=" * 70)
        print("🦞 Paper Research Agent - Autonomous Research Pipeline")
        print("=" * 70)
        print(f"Query: {query}")
        print(f"Mode: {mode}")
        print(f"Max papers: {max_papers}")
        print()
        
        # Phase 1: Intelligent search
        papers = self._phase1_search(query, mode, max_papers)
        if not papers:
            print("❌ No papers found")
            return {"status": "failed", "error": "No papers found"}
        
        # Phase 2: Download PDFs
        papers = self._phase2_download(papers)
        
        # Phase 3: Parallel agent analysis
        self._phase3_parallel_analysis(papers)
        
        # Phase 4: Integration (placeholder - done after agents complete)
        summary = self._generate_summary(query, papers)
        
        print("\n" + "=" * 70)
        print("✅ Research pipeline initiated successfully!")
        print("=" * 70)
        print(f"Output directory: {self.output_dir}")
        print(f"Total papers: {len(papers)}")
        print()
        print("Next steps:")
        print("1. Sub-agents are analyzing papers in parallel")
        print("2. Check progress in analysis/ directory")
        print("3. Final integrated report will be generated when all agents complete")
        
        return summary
    
    def _phase1_search(self, query: str, mode: str, max_papers: int) -> List[Dict]:
        """Phase 1: Intelligent search"""
        print("=" * 70)
        print("Phase 1: Intelligent Research Probe")
        print("=" * 70)
        
        # Parse search keywords from query
        keywords = self._extract_keywords(query)
        print(f"Keywords: {keywords}")
        
        # Search arxiv
        client = arxiv.Client()
        search = arxiv.Search(
            query=" ".join(keywords),
            max_results=max_papers * 2,  # Get more for deduplication
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending
        )
        
        papers = []
        for result in client.results(search):
            papers.append({
                "arxiv_id": result.get_short_id(),
                "title": result.title,
                "authors": [str(a) for a in result.authors],
                "summary": result.summary,
                "published": result.published.isoformat() if result.published else "",
                "pdf_url": result.pdf_url,
                "categories": result.categories
            })
        
        # Deduplicate by base arxiv id
        seen = set()
        unique = []
        for p in papers:
            base_id = p['arxiv_id'].split('v')[0]
            if base_id not in seen:
                seen.add(base_id)
                unique.append(p)
        
        papers = unique[:max_papers]
        print(f"✅ Found {len(papers)} unique papers")
        return papers
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract search keywords from natural language query"""
        # Common academic terms
        tech_terms = [
            'diffusion policy', 'tactile', 'point cloud', 'grasping',
            'manipulation', 'imitation learning', 'reinforcement learning',
            'vision-language', 'multimodal', 'transformer',
            'Tac3D', 'GelSight', 'robot learning'
        ]
        
        keywords = []
        query_lower = query.lower()
        
        for term in tech_terms:
            if term in query_lower:
                keywords.append(term)
        
        # If no tech terms found, use query words
        if not keywords:
            keywords = [w for w in query.split() if len(w) > 2]
        
        return keywords[:5]  # Limit to 5 keywords
    
    def _phase2_download(self, papers: List[Dict]) -> List[Dict]:
        """Phase 2: Download PDFs"""
        print("\n" + "=" * 70)
        print("Phase 2: Downloading PDFs")
        print("=" * 70)
        
        import requests
        import time
        import re
        
        downloaded = []
        
        for i, paper in enumerate(papers, 1):
            print(f"\n[{i}/{len(papers)}] {paper['title'][:60]}...")
            
            if not paper.get('pdf_url'):
                print("  ⚠️ No PDF URL")
                continue
            
            # Generate filename
            safe_title = re.sub(r'[^\w\s]', '', paper['title'])
            safe_title = re.sub(r'\s+', '_', safe_title)[:80]
            filename = f"{safe_title}-{paper['arxiv_id']}.pdf"
            filepath = self.papers_dir / filename
            
            if filepath.exists():
                print(f"  ⏭️ Already exists")
                paper['pdf_path'] = str(filepath)
                downloaded.append(paper)
                continue
            
            try:
                print(f"  ⬇️ Downloading...")
                response = requests.get(paper['pdf_url'], timeout=60)
                response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                paper['pdf_path'] = str(filepath)
                downloaded.append(paper)
                print(f"  ✅ Downloaded ({len(response.content)//1024}KB)")
                
                time.sleep(3)  # Rate limit
                
            except Exception as e:
                print(f"  ❌ Failed: {e}")
        
        print(f"\n✅ Downloaded {len(downloaded)}/{len(papers)} papers")
        return downloaded
    
    def _phase3_parallel_analysis(self, papers: List[Dict]):
        """Phase 3: Spawn parallel agents for analysis"""
        print("\n" + "=" * 70)
        print("Phase 3: Parallel Agent Analysis")
        print("=" * 70)
        print(f"Spawning {len(papers)} sub-agents in parallel...")
        print()
        
        # Generate agent tasks
        tasks = []
        for i, paper in enumerate(papers, 1):
            if 'pdf_path' not in paper:
                continue
            
            task = self._generate_agent_task(paper)
            task_file = self.output_dir / "agent_tasks" / f"task_{paper['arxiv_id']}.txt"
            task_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(task_file, 'w', encoding='utf-8') as f:
                f.write(task)
            
            tasks.append({
                'id': i,
                'paper': paper,
                'task_file': str(task_file),
                'task': task
            })
            
            print(f"[{i}] {paper['title'][:50]}...")
            print(f"    Task: {task_file}")
        
        # Save tasks for external agent spawning
        tasks_file = self.output_dir / "_agent_tasks.json"
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Generated {len(tasks)} agent tasks")
        print(f"📁 Tasks saved to: {tasks_file}")
        print()
        print("🚀 To launch parallel agents, execute:")
        print(f"   python3 {self.output_dir}/launch_agents.py")
        print()
        print("Or manually spawn sub-agents using OpenClaw sessions_spawn")
    
    def _generate_agent_task(self, paper: Dict) -> str:
        """Generate detailed agent analysis task"""
        
        arxiv_id = paper['arxiv_id']
        title = paper['title']
        pdf_path = paper.get('pdf_path', '')
        
        # Output report path
        safe_title = "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in title)[:80]
        output_md = str(self.analysis_dir / f"{safe_title}-{arxiv_id}_analysis.md")
        
        task = f"""【Paper Research Agent - Deep Analysis Task】

⚠️  CRITICAL: You MUST read the complete PDF. NO shortcuts allowed!

📄 Paper Information:
- Title: {title}
- ArXiv ID: {arxiv_id}
- PDF Path: {pdf_path}
- Output Report: {output_md}

🔧 Step 1: Extract PDF Content
Use the paper-reader tool to extract full content:
```bash
python3 ~/.openclaw/skills/paper-reader/read_paper.py "{pdf_path}" --full
```

This will give you:
- Complete text with section structure
- All figures and tables
- Metadata (title, authors, abstract)

📋 Step 2: Generate 6-Section Analysis Report

You MUST write a detailed report with these 6 sections:

## Section 1: Research Background
- Domain context and research lineage
- Key prior works (cite 3-5 specific papers mentioned)
- Technical state when this paper was published
- Cite exact locations: [Introduction, paragraph X] or [Related Work, Section Y]

## Section 2: Research Problem  
- SPECIFIC problem being solved (not generic description)
- SPECIFIC limitations of existing methods (quote original text)
- Core assumptions and insights
- Cite: [Section X.Y, "exact quote"]

## Section 3: Core Innovation
- Detailed method/system architecture (describe flow in words)
- Network structure details (layers, dimensions, connections)
- Key formulas in LaTeX format
- Comparison table with prior methods:
  | Aspect | Prior Work | This Paper | Advantage |
  |--------|-----------|------------|-----------|
  | ... | ... | ... | ... |
- What is genuinely new compared to prior work?

## Section 4: Experimental Design
- Dataset: Name, size, characteristics
- Baseline methods: Specific method names and sources
- Evaluation metrics: Formulas and units
- Results table with REAL data (copy exact numbers from paper):
  | Method | Metric1 | Metric2 | Metric3 |
  |--------|---------|---------|---------|
  | This | X.XX | X.XX | X.XX |
  | Baseline1 | X.XX | X.XX | X.XX |
- Ablation study results
- Failure case analysis (if any)

## Section 5: Key Insights
- Core findings supported by experiments
- Domain insights: What works? What doesn't?
- Key design choices and their impact
- Practical recommendations for researchers

## Section 6: Future Work
- Limitations explicitly acknowledged by authors
- Unsolved technical challenges
- Potential research directions (at least 3 specific ones)

🔍 Quality Checklist (MUST complete before finishing):
□ I have read EVERY sentence of Introduction
□ I have read EVERY sentence of Related Work
□ I have read EVERY sentence of Methods
□ I have read EVERY sentence of Experiments/Results
□ I have extracted ALL tables with real data (not summary)
□ I have found specific citations for Related Work papers
□ All my citations include exact location [Section X.Y]
□ I have marked uncertain information as "Not explicitly stated in paper"
□ Report is at least 3000 words
□ Report includes at least 3 data tables
□ Report includes at least 10 citations to original text

⚠️  STRICT PROHIBITIONS:
- ❌ NEVER fabricate data
- ❌ NEVER invent citations
- ❌ NEVER skip sections "because they look similar"
- ❌ NEVER write "The paper proposes a method" without specifics
- ❌ NEVER write generic summaries from abstract only

✅ MANDATORY:
- ✅ Read FULL PDF using paper-reader
- ✅ Extract REAL tables with exact numbers
- ✅ Cite specific locations [Section X.Y, Table N, Figure M]
- ✅ Write detailed technical content
- ✅ Mark uncertain information explicitly

📝 Output Format:
Save report to: {output_md}

Use Markdown format with:
- Clear section headers (## Section X: Title)
- Tables for comparisons
- LaTeX for formulas ($...$)
- Bullet points for lists
- **Bold** for key terms

Now begin analysis! Read carefully, extract accurately, write thoroughly!
"""
        return task
    
    def _generate_summary(self, query: str, papers: List[Dict]) -> Dict:
        """Generate research summary"""
        summary = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "total_papers": len(papers),
            "output_dir": str(self.output_dir),
            "papers": [
                {
                    "arxiv_id": p.get('arxiv_id'),
                    "title": p.get('title'),
                    "pdf_path": p.get('pdf_path'),
                    "analysis_path": str(self.analysis_dir / f"{p.get('title', '')[:80]}-{p.get('arxiv_id', '')}_analysis.md")
                }
                for p in papers
            ]
        }
        
        summary_file = self.output_dir / "_research_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        return summary


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Paper Research Agent - Autonomous multi-agent research"
    )
    parser.add_argument("--query", required=True, help="Research query")
    parser.add_argument("--mode", default="vertical", 
                       choices=['vertical', 'iterative', 'horizontal'],
                       help="Search mode")
    parser.add_argument("--max-papers", type=int, default=10,
                       help="Maximum papers to analyze")
    parser.add_argument("--output", default="./research_output",
                       help="Output directory")
    
    args = parser.parse_args()
    
    pipeline = ResearchPipeline(output_dir=args.output)
    results = pipeline.execute(
        query=args.query,
        mode=args.mode,
        max_papers=args.max_papers
    )
    
    return 0 if results.get('status') != 'failed' else 1


if __name__ == "__main__":
    sys.exit(main())

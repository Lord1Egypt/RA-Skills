#!/usr/bin/env python3
"""
Batch Product Analysis Manager - Uses SubAgent system for parallel product processing
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import SubAgent system
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from subagent import SubAgentManager, AgentStatus

# Import our product analysis engine
sys.path.insert(0, str(Path(__file__).parent))
from product_analyzer import ProductAnalyzer

class BatchProductAnalysisManager:
    def __init__(self, max_workers: int = 4):
        self.manager = SubAgentManager()
        self.max_workers = max_workers
        self.results_dir = Path(__file__).parent / "batch_results"
        self.results_dir.mkdir(exist_ok=True)
    
    def analyze_products_parallel(self, products: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze multiple products in parallel using SubAgent system
        """
        start_time = time.time()
        
        # Create SubAgents for each product
        agent_ids = []
        for i, product in enumerate(products):
            name = product.get('name', f'Product_{i+1}')
            category = product.get('category', 'general')
            
            agent_name = f"ProductAnalyzer_{i+1}"
            task = f"Analyze product: {name}"
            
            context = {
                "product_name": name,
                "category": category,
                "index": i
            }
            
            agent_id = self.manager.create_agent(agent_name, task, context)
            agent_ids.append(agent_id)
        
        # Process agents in batches (respecting max_workers)
        results = {}
        completed_agents = set()
        
        while len(completed_agents) < len(agent_ids):
            # Check status of running agents
            for agent_id in agent_ids:
                if agent_id in completed_agents:
                    continue
                
                agent = self.manager.get_agent(agent_id)
                if not agent:
                    continue
                
                # If agent is not yet started, start it
                if agent.status == AgentStatus.PENDING:
                    self._process_product_agent(agent_id)
                
                # If agent completed, collect result
                if agent.status in [AgentStatus.COMPLETED, AgentStatus.FAILED]:
                    if agent_id not in completed_agents:
                        results[agent_id] = {
                            "agent_id": agent_id,
                            "name": agent.name,
                            "task": agent.task,
                            "status": agent.status.value,
                            "result": agent.result,
                            "error": agent.error,
                            "created_at": agent.created_at,
                            "completed_at": agent.completed_at
                        }
                        completed_agents.add(agent_id)
            
            # Small delay to prevent busy waiting
            time.sleep(0.1)
            
            # Timeout check (5 minutes max)
            if time.time() - start_time > 300:
                break
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Format final results
        batch_results = {
            "batch_info": {
                "total_products": len(products),
                "processed_products": len([r for r in results.values() if r["status"] == "completed"]),
                "failed_products": len([r for r in results.values() if r["status"] == "failed"]),
                "processing_time_seconds": round(processing_time, 2),
                "timestamp": datetime.now().isoformat(),
                "max_workers": self.max_workers
            },
            "results": [],
            "summary": {
                "average_market_trend_score": 0,
                "average_competitor_score": 0,
                "average_category_fit_score": 0,
                "average_risk_score": 0,
                "trend_distribution": {"high": 0, "medium": 0, "low": 0},
                "competition_distribution": {"high": 0, "medium": 0, "low": 0}
            }
        }
        
        # Process results
        market_trend_scores = []
        competitor_scores = []
        category_fit_scores = []
        risk_scores = []
        
        for result in results.values():
            if result["status"] == "completed" and result["result"]:
                analysis_result = result["result"]
                batch_results["results"].append({
                    "product_name": analysis_result.get("product_name", "unknown"),
                    "category": analysis_result.get("category", "general"),
                    "market_trend_score": analysis_result.get("market_trends", {}).get("score", 0),
                    "competitor_score": analysis_result.get("competitor_analysis", {}).get("score", 0),
                    "category_fit_score": analysis_result.get("category_fit", {}).get("score", 0),
                    "risk_score": analysis_result.get("risk_assessment", {}).get("score", 0),
                    "recommendations_count": len(analysis_result.get("recommendations", [])),
                    "optimization_suggestions_count": len(analysis_result.get("optimization_suggestions", []))
                })
                
                # Accumulate for summary
                market_trend_scores.append(analysis_result.get("market_trends", {}).get("score", 0))
                competitor_scores.append(analysis_result.get("competitor_analysis", {}).get("score", 0))
                category_fit_scores.append(analysis_result.get("category_fit", {}).get("score", 0))
                risk_scores.append(analysis_result.get("risk_assessment", {}).get("score", 0))
                
                # Trend distribution
                trend_score = analysis_result.get("market_trends", {}).get("score", 0)
                if trend_score >= 70:
                    batch_results["summary"]["trend_distribution"]["high"] += 1
                elif trend_score >= 40:
                    batch_results["summary"]["trend_distribution"]["medium"] += 1
                else:
                    batch_results["summary"]["trend_distribution"]["low"] += 1
                
                # Competition distribution (inverted: lower score means higher competition)
                comp_score = analysis_result.get("competitor_analysis", {}).get("score", 0)
                if comp_score >= 70:
                    batch_results["summary"]["competition_distribution"]["low"] += 1  # Low competition
                elif comp_score >= 40:
                    batch_results["summary"]["competition_distribution"]["medium"] += 1
                else:
                    batch_results["summary"]["competition_distribution"]["high"] += 1  # High competition
        
        # Calculate average scores
        if market_trend_scores:
            batch_results["summary"]["average_market_trend_score"] = round(sum(market_trend_scores) / len(market_trend_scores), 2)
        if competitor_scores:
            batch_results["summary"]["average_competitor_score"] = round(sum(competitor_scores) / len(competitor_scores), 2)
        if category_fit_scores:
            batch_results["summary"]["average_category_fit_score"] = round(sum(category_fit_scores) / len(category_fit_scores), 2)
        if risk_scores:
            batch_results["summary"]["average_risk_score"] = round(sum(risk_scores) / len(risk_scores), 2)
        
        return batch_results
    
    def _process_product_agent(self, agent_id: str):
        """Process a single product analysis agent"""
        agent = self.manager.get_agent(agent_id)
        if not agent:
            return
        
        # Update status to running
        self.manager.update_status(agent_id, AgentStatus.RUNNING)
        
        try:
            # Get context
            product_name = agent.context.get("product_name")
            category = agent.context.get("category", "general")
            
            if not product_name:
                raise ValueError("Product name is required")
            
            # Analyze product
            analyzer = ProductAnalyzer()
            result = analyzer.analyze_product(product_name, category)
            
            # Update agent with result
            self.manager.update_status(agent_id, AgentStatus.COMPLETED, result=result)
            
        except Exception as e:
            # Update agent with error
            self.manager.update_status(agent_id, AgentStatus.FAILED, error=str(e))
    
    def save_batch_report(self, batch_results: Dict[str, Any], output_file: str = None) -> str:
        """Save batch analysis results to file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.results_dir / f"batch_analysis_report_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(batch_results, f, indent=2, ensure_ascii=False)
        
        return str(output_file)
    
    def print_batch_summary(self, batch_results: Dict[str, Any]):
        """Print human-readable batch summary"""
        info = batch_results["batch_info"]
        summary = batch_results["summary"]
        
        print("=" * 70)
        print("BATCH PRODUCT ANALYSIS REPORT")
        print("=" * 70)
        print(f"Total Products: {info['total_products']}")
        print(f"Processed: {info['processed_products']}")
        print(f"Failed: {info['failed_products']}")
        print(f"Processing Time: {info['processing_time_seconds']} seconds")
        print(f"Timestamp: {info['timestamp']}")
        print(f"Max Workers: {info['max_workers']}")
        print("-" * 70)
        print("SUMMARY:")
        print(f"  Average Market Trend Score: {summary['average_market_trend_score']}/100")
        print(f"  Average Competitor Score: {summary['average_competitor_score']}/100")
        print(f"  Average Category Fit Score: {summary['average_category_fit_score']}/100")
        print(f"  Average Risk Score: {summary['average_risk_score']}/100 (lower is better)")
        print(f"  Trend Distribution: High:{summary['trend_distribution']['high']} Medium:{summary['trend_distribution']['medium']} Low:{summary['trend_distribution']['low']}")
        print(f"  Competition Distribution: High:{summary['competition_distribution']['high']} Medium:{summary['competition_distribution']['medium']} Low:{summary['competition_distribution']['low']}")
        print("-" * 70)
        print("INDIVIDUAL RESULTS:")
        
        for i, result in enumerate(batch_results["results"], 1):
            print(f"{i}. {result['product_name']} ({result['category']})")
            print(f"   Market Trend: {result['market_trend_score']}/100")
            print(f"   Competitor Analysis: {result['competitor_score']}/100")
            print(f"   Category Fit: {result['category_fit_score']}/100")
            print(f"   Risk Score: {result['risk_score']}/100 (lower is better)")
            print(f"   Recommendations: {result['recommendations_count']}")
            print(f"   Optimization Suggestions: {result['optimization_suggestions_count']}")
            print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python batch_product_analyzer.py <product_file> [--workers <n>]")
        print("Example: python batch_product_analyzer.py products.json --workers 4")
        print("Product file format: JSON array of objects with 'name' and 'category' fields")
        sys.exit(1)
    
    # Parse arguments
    args = sys.argv[1:]
    product_file = None
    max_workers = 4
    
    i = 0
    while i < len(args):
        if args[i] == "--workers" and i + 1 < len(args):
            try:
                max_workers = int(args[i + 1])
            except ValueError:
                pass
            i += 2
        else:
            product_file = args[i]
            i += 1
    
    if not product_file:
        print("Error: No product file specified")
        sys.exit(1)
    
    # Validate file exists
    if not os.path.exists(product_file):
        print(f"Error: File not found - {product_file}")
        sys.exit(1)
    
    # Load products from file
    try:
        with open(product_file, 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        if not isinstance(products, list):
            print("Error: Product file must contain a JSON array")
            sys.exit(1)
        
        # Validate each product has required fields
        valid_products = []
        for i, product in enumerate(products):
            if not isinstance(product, dict):
                print(f"Warning: Product at index {i} is not an object, skipping")
                continue
            
            name = product.get('name')
            if not name:
                print(f"Warning: Product at index {i} missing 'name' field, skipping")
                continue
            
            valid_products.append(product)
        
        if not valid_products:
            print("Error: No valid products found in file")
            sys.exit(1)
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in product file: {e}")
        sys.exit(1)
    
    # Process batch
    manager = BatchProductAnalysisManager(max_workers=max_workers)
    print(f"Starting batch analysis of {len(valid_products)} products with {max_workers} workers...")
    results = manager.analyze_products_parallel(valid_products)
    
    # Display results
    manager.print_batch_summary(results)
    
    # Save results
    output_file = manager.save_batch_report(results)
    print(f"Detailed results saved to: {output_file}")


if __name__ == "__main__":
    main()
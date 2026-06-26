"""
Invoice Forge - Reports and Analytics
Summary reports, overdue tracking, and client analytics.

Author: Shadow Rose
License: MIT
"""

import json
import os
import sys
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict


class InvoiceReporter:
    """Generate reports from invoice ledger."""
    
    def __init__(self, invoices_file: str = "data/invoices.jsonl"):
        self.invoices_file = invoices_file
    
    def _load_all_invoices(self) -> List[Dict]:
        """Load all invoices from ledger."""
        if not os.path.exists(self.invoices_file):
            return []
        
        invoices = []
        with open(self.invoices_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    invoices.append(json.loads(line))
        
        return invoices
    
    def get_overdue_invoices(self, as_of_date: Optional[str] = None) -> List[Dict]:
        """
        Get all overdue invoices.
        
        Args:
            as_of_date: Date to check against (default: today)
        
        Returns:
            List of overdue invoice dictionaries
        """
        if as_of_date is None:
            as_of_date = datetime.now().strftime("%Y-%m-%d")
        
        as_of_dt = datetime.strptime(as_of_date, "%Y-%m-%d")
        
        invoices = self._load_all_invoices()
        overdue = []
        
        for invoice in invoices:
            # Skip if already paid or cancelled
            if invoice.get("status") in ["paid", "cancelled"]:
                continue
            
            due_date = invoice.get("due_date", "")
            if not due_date:
                continue
            
            try:
                due_dt = datetime.strptime(due_date, "%Y-%m-%d")
                if due_dt < as_of_dt:
                    # Calculate days overdue
                    days_overdue = (as_of_dt - due_dt).days
                    invoice["days_overdue"] = days_overdue
                    overdue.append(invoice)
            except ValueError:
                continue
        
        # Sort by days overdue (most overdue first)
        overdue.sort(key=lambda inv: inv.get("days_overdue", 0), reverse=True)
        
        return overdue
    
    def get_client_summary(self, client_id: str) -> Dict:
        """
        Get summary statistics for a specific client.
        
        Args:
            client_id: Client identifier
        
        Returns:
            Summary dictionary
        """
        invoices = self._load_all_invoices()
        client_invoices = [
            inv for inv in invoices
            if inv.get("client", {}).get("client_id") == client_id
        ]
        
        if not client_invoices:
            return {
                "client_id": client_id,
                "total_invoices": 0,
                "total_invoiced": 0.0,
                "total_paid": 0.0,
                "total_pending": 0.0,
                "total_overdue": 0.0,
                "outstanding_balance": 0.0,
            }
        
        total_invoiced = sum(inv.get("total", 0.0) for inv in client_invoices)
        total_paid = sum(
            inv.get("total", 0.0) for inv in client_invoices
            if inv.get("status") == "paid"
        )
        total_pending = sum(
            inv.get("total", 0.0) for inv in client_invoices
            if inv.get("status") == "pending"
        )
        
        # Calculate overdue
        overdue_invoices = [
            inv for inv in self.get_overdue_invoices()
            if inv.get("client", {}).get("client_id") == client_id
        ]
        total_overdue = sum(inv.get("total", 0.0) for inv in overdue_invoices)
        
        outstanding_balance = total_invoiced - total_paid
        
        return {
            "client_id": client_id,
            "client_name": client_invoices[0].get("client", {}).get("name", ""),
            "total_invoices": len(client_invoices),
            "total_invoiced": total_invoiced,
            "total_paid": total_paid,
            "total_pending": total_pending,
            "total_overdue": total_overdue,
            "outstanding_balance": outstanding_balance,
            "invoices_paid": len([inv for inv in client_invoices if inv.get("status") == "paid"]),
            "invoices_pending": len([inv for inv in client_invoices if inv.get("status") == "pending"]),
            "invoices_overdue": len(overdue_invoices),
        }
    
    def get_overall_summary(self) -> Dict:
        """
        Get overall summary across all invoices.
        
        Returns:
            Summary dictionary
        """
        invoices = self._load_all_invoices()
        
        if not invoices:
            return {
                "total_invoices": 0,
                "total_invoiced": 0.0,
                "total_paid": 0.0,
                "total_pending": 0.0,
                "total_overdue": 0.0,
                "outstanding_balance": 0.0,
            }
        
        total_invoiced = sum(inv.get("total", 0.0) for inv in invoices)
        total_paid = sum(
            inv.get("total", 0.0) for inv in invoices
            if inv.get("status") == "paid"
        )
        total_pending = sum(
            inv.get("total", 0.0) for inv in invoices
            if inv.get("status") == "pending"
        )
        
        overdue_invoices = self.get_overdue_invoices()
        total_overdue = sum(inv.get("total", 0.0) for inv in overdue_invoices)
        
        outstanding_balance = total_invoiced - total_paid
        
        # Get unique clients
        clients = set(inv.get("client", {}).get("client_id") for inv in invoices)
        
        return {
            "total_invoices": len(invoices),
            "total_clients": len(clients),
            "total_invoiced": total_invoiced,
            "total_paid": total_paid,
            "total_pending": total_pending,
            "total_overdue": total_overdue,
            "outstanding_balance": outstanding_balance,
            "invoices_paid": len([inv for inv in invoices if inv.get("status") == "paid"]),
            "invoices_pending": len([inv for inv in invoices if inv.get("status") == "pending"]),
            "invoices_overdue": len(overdue_invoices),
            "invoices_cancelled": len([inv for inv in invoices if inv.get("status") == "cancelled"]),
        }
    
    def get_revenue_by_period(self, period: str = "month") -> Dict[str, float]:
        """
        Get revenue grouped by time period.
        
        Args:
            period: "month" or "year"
        
        Returns:
            Dictionary mapping period -> total revenue
        """
        invoices = self._load_all_invoices()
        
        # Only count paid invoices
        paid_invoices = [inv for inv in invoices if inv.get("status") == "paid"]
        
        revenue = defaultdict(float)
        
        for invoice in paid_invoices:
            invoice_date = invoice.get("invoice_date", "")
            if not invoice_date:
                continue
            
            try:
                dt = datetime.strptime(invoice_date, "%Y-%m-%d")
                
                if period == "month":
                    key = dt.strftime("%Y-%m")
                elif period == "year":
                    key = dt.strftime("%Y")
                else:
                    key = invoice_date
                
                revenue[key] += invoice.get("total", 0.0)
            except ValueError:
                continue
        
        return dict(sorted(revenue.items()))
    
    def get_top_clients(self, limit: int = 10) -> List[Dict]:
        """
        Get top clients by total invoiced amount.
        
        Args:
            limit: Maximum number of clients to return
        
        Returns:
            List of client summary dictionaries
        """
        invoices = self._load_all_invoices()
        
        # Group by client
        clients = defaultdict(list)
        for invoice in invoices:
            client_id = invoice.get("client", {}).get("client_id")
            if client_id:
                clients[client_id].append(invoice)
        
        # Calculate totals for each client
        client_summaries = []
        for client_id, client_invoices in clients.items():
            total_invoiced = sum(inv.get("total", 0.0) for inv in client_invoices)
            total_paid = sum(
                inv.get("total", 0.0) for inv in client_invoices
                if inv.get("status") == "paid"
            )
            
            client_summaries.append({
                "client_id": client_id,
                "client_name": client_invoices[0].get("client", {}).get("name", ""),
                "total_invoices": len(client_invoices),
                "total_invoiced": total_invoiced,
                "total_paid": total_paid,
                "outstanding_balance": total_invoiced - total_paid,
            })
        
        # Sort by total invoiced (descending)
        client_summaries.sort(key=lambda c: c["total_invoiced"], reverse=True)
        
        return client_summaries[:limit]
    
    def get_aging_report(self) -> Dict[str, List[Dict]]:
        """
        Get accounts receivable aging report.
        
        Returns:
            Dictionary with aging buckets
        """
        today = datetime.now()
        
        invoices = self._load_all_invoices()
        unpaid = [
            inv for inv in invoices
            if inv.get("status") not in ["paid", "cancelled"]
        ]
        
        aging = {
            "current": [],      # Not yet due
            "0-30": [],         # 1-30 days overdue
            "31-60": [],        # 31-60 days overdue
            "61-90": [],        # 61-90 days overdue
            "90+": [],          # 90+ days overdue
        }
        
        for invoice in unpaid:
            due_date = invoice.get("due_date", "")
            if not due_date:
                continue
            
            try:
                due_dt = datetime.strptime(due_date, "%Y-%m-%d")
                days_diff = (today - due_dt).days
                
                invoice["days_overdue"] = max(0, days_diff)
                
                if days_diff < 0:
                    aging["current"].append(invoice)
                elif days_diff <= 30:
                    aging["0-30"].append(invoice)
                elif days_diff <= 60:
                    aging["31-60"].append(invoice)
                elif days_diff <= 90:
                    aging["61-90"].append(invoice)
                else:
                    aging["90+"].append(invoice)
            except ValueError:
                continue
        
        return aging


def main():
    """CLI for invoice reporting."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Invoice Forge - Reports")
    subparsers = parser.add_subparsers(dest="command", help="Report commands")
    
    # Overall summary
    subparsers.add_parser("summary", help="Overall summary")
    
    # Client summary
    client_parser = subparsers.add_parser("client", help="Client summary")
    client_parser.add_argument("client_id", help="Client ID")
    
    # Overdue invoices
    overdue_parser = subparsers.add_parser("overdue", help="Overdue invoices")
    overdue_parser.add_argument("--date", help="As of date (YYYY-MM-DD, default: today)")
    
    # Revenue by period
    revenue_parser = subparsers.add_parser("revenue", help="Revenue by period")
    revenue_parser.add_argument("--period", choices=["month", "year"], default="month",
                                help="Time period")
    
    # Top clients
    top_parser = subparsers.add_parser("top", help="Top clients by revenue")
    top_parser.add_argument("--limit", type=int, default=10, help="Number of clients")
    
    # Aging report
    subparsers.add_parser("aging", help="Accounts receivable aging")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    reporter = InvoiceReporter()
    
    if args.command == "summary":
        summary = reporter.get_overall_summary()
        
        print("\n=== OVERALL SUMMARY ===\n")
        print(f"Total Invoices:       {summary['total_invoices']}")
        print(f"Total Clients:        {summary['total_clients']}")
        print(f"\nTotal Invoiced:       ${summary['total_invoiced']:,.2f}")
        print(f"Total Paid:           ${summary['total_paid']:,.2f}")
        print(f"Total Pending:        ${summary['total_pending']:,.2f}")
        print(f"Total Overdue:        ${summary['total_overdue']:,.2f}")
        print(f"\nOutstanding Balance:  ${summary['outstanding_balance']:,.2f}")
        print(f"\nInvoices Paid:        {summary['invoices_paid']}")
        print(f"Invoices Pending:     {summary['invoices_pending']}")
        print(f"Invoices Overdue:     {summary['invoices_overdue']}")
        print(f"Invoices Cancelled:   {summary['invoices_cancelled']}")
    
    elif args.command == "client":
        summary = reporter.get_client_summary(args.client_id)
        
        print(f"\n=== CLIENT SUMMARY: {summary.get('client_name', args.client_id)} ===\n")
        print(f"Total Invoices:       {summary['total_invoices']}")
        print(f"\nTotal Invoiced:       ${summary['total_invoiced']:,.2f}")
        print(f"Total Paid:           ${summary['total_paid']:,.2f}")
        print(f"Total Pending:        ${summary['total_pending']:,.2f}")
        print(f"Total Overdue:        ${summary['total_overdue']:,.2f}")
        print(f"\nOutstanding Balance:  ${summary['outstanding_balance']:,.2f}")
        print(f"\nInvoices Paid:        {summary['invoices_paid']}")
        print(f"Invoices Pending:     {summary['invoices_pending']}")
        print(f"Invoices Overdue:     {summary['invoices_overdue']}")
    
    elif args.command == "overdue":
        overdue = reporter.get_overdue_invoices(args.date)
        
        if not overdue:
            print("No overdue invoices.")
        else:
            print(f"\n=== OVERDUE INVOICES ({len(overdue)}) ===\n")
            print(f"{'Invoice #':<15} {'Client':<25} {'Due Date':<12} {'Days':<6} {'Amount':>12}")
            print("-" * 80)
            
            for inv in overdue:
                inv_num = inv.get("invoice_number", "")
                client_name = inv.get("client", {}).get("name", "")[:25]
                due_date = inv.get("due_date", "")
                days = inv.get("days_overdue", 0)
                amount = inv.get("total", 0.0)
                
                print(f"{inv_num:<15} {client_name:<25} {due_date:<12} {days:<6} ${amount:>11,.2f}")
            
            total_overdue = sum(inv.get("total", 0.0) for inv in overdue)
            print("-" * 80)
            print(f"{'TOTAL':<59} ${total_overdue:>11,.2f}")
    
    elif args.command == "revenue":
        revenue = reporter.get_revenue_by_period(args.period)
        
        if not revenue:
            print("No revenue data.")
        else:
            print(f"\n=== REVENUE BY {args.period.upper()} ===\n")
            print(f"{'Period':<12} {'Revenue':>12}")
            print("-" * 30)
            
            for period, amount in revenue.items():
                print(f"{period:<12} ${amount:>11,.2f}")
            
            total = sum(revenue.values())
            print("-" * 30)
            print(f"{'TOTAL':<12} ${total:>11,.2f}")
    
    elif args.command == "top":
        top_clients = reporter.get_top_clients(args.limit)
        
        if not top_clients:
            print("No client data.")
        else:
            print(f"\n=== TOP {len(top_clients)} CLIENTS ===\n")
            print(f"{'Client':<30} {'Invoices':>10} {'Invoiced':>12} {'Paid':>12} {'Outstanding':>12}")
            print("-" * 80)
            
            for client in top_clients:
                name = client['client_name'][:30]
                count = client['total_invoices']
                invoiced = client['total_invoiced']
                paid = client['total_paid']
                outstanding = client['outstanding_balance']
                
                print(f"{name:<30} {count:>10} ${invoiced:>11,.2f} ${paid:>11,.2f} ${outstanding:>11,.2f}")
    
    elif args.command == "aging":
        aging = reporter.get_aging_report()
        
        print("\n=== ACCOUNTS RECEIVABLE AGING ===\n")
        
        for bucket, invoices in aging.items():
            if not invoices:
                continue
            
            total = sum(inv.get("total", 0.0) for inv in invoices)
            
            print(f"\n{bucket} days:")
            print(f"  {len(invoices)} invoice(s) - ${total:,.2f}")
            
            for inv in invoices:
                inv_num = inv.get("invoice_number", "")
                client = inv.get("client", {}).get("name", "")[:30]
                amount = inv.get("total", 0.0)
                days = inv.get("days_overdue", 0)
                
                print(f"    {inv_num:<15} {client:<30} ${amount:>10,.2f} ({days} days)")
        
        # Grand total
        all_invoices = [inv for bucket in aging.values() for inv in bucket]
        grand_total = sum(inv.get("total", 0.0) for inv in all_invoices)
        
        print(f"\n{'=' * 60}")
        print(f"Total Outstanding: ${grand_total:,.2f}")


if __name__ == "__main__":
    main()

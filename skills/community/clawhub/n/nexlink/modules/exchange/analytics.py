"""
Email analytics and reporting for Exchange Mailbox.

Provides statistics on email activity, response times,
top senders, and productivity metrics.

Commands:
    stats           - General email statistics
    response-time   - Response time analysis
    top-senders     - Top senders by email count
    heatmap         - Activity heatmap data
    report          - Full analytics report
"""

import argparse
import sys
import os
from datetime import datetime, timedelta
from collections import Counter
from typing import Dict, List, Any, Optional
from statistics import mean, median

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from exchangelib import Account
from exchangelib.queryset import Q
from exchangelib.items import Message

from connection import get_account
from utils import out, die, format_datetime, add_json_argument
from logger import get_logger

_logger = get_logger()


# =============================================================================
# Core Analytics Functions
# =============================================================================

def get_email_stats(account: Account, days: int = 30) -> Dict[str, Any]:
    """
    Get general email statistics for the specified period.
    
    Args:
        account: Exchange account
        days: Number of days to analyze
        
    Returns:
        Dictionary with email statistics
    """
    _logger.info(f"Getting email stats for last {days} days")
    
    tz = account.default_timezone
    end_date = datetime.now(tz)
    start_date = end_date - timedelta(days=days)
    
    # Query inbox emails for the period
    _logger.debug("Querying inbox emails...")
    inbox_emails = account.inbox.filter(
        datetime_received__range=(start_date, end_date)
    )
    
    # Query sent items for the same period
    _logger.debug("Querying sent items...")
    sent_emails = account.sent.filter(
        datetime_sent__range=(start_date, end_date)
    )
    
    # Get counts (these are efficient server-side)
    total_received = inbox_emails.count()
    total_sent = sent_emails.count()
    
    # Unread count
    unread_count = account.inbox.filter(is_read=False).count()
    
    # Calculate daily average
    avg_per_day = round(total_received / days, 1) if days > 0 else 0
    
    # Peak hours analysis (sample first 1000 emails to avoid timeout)
    _logger.debug("Analyzing peak hours...")
    peak_hour = 0
    peak_count = 0
    hour_counts = Counter()
    
    try:
        for email in inbox_emails.all()[:1000]:
            if email.datetime_received:
                hour = email.datetime_received.hour
                hour_counts[hour] += 1
        
        if hour_counts:
            peak_hour, peak_count = hour_counts.most_common(1)[0]
    except Exception as e:
        _logger.warning(f"Could not analyze peak hours: {e}")
    
    return {
        "period_days": days,
        "total_received": total_received,
        "total_sent": total_sent,
        "unread": unread_count,
        "read": total_received - unread_count,
        "avg_per_day": avg_per_day,
        "peak_hour": peak_hour,
        "peak_hour_count": peak_count,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
    }


def get_response_time(account: Account, days: int = 30) -> Dict[str, Any]:
    """
    Calculate response time statistics.
    
    Analyzes reply times for incoming emails by tracking
    conversations and measuring time between messages.
    
    Args:
        account: Exchange account
        days: Number of days to analyze
        
    Returns:
        Dictionary with response time metrics
    """
    _logger.info(f"Calculating response times for last {days} days")
    
    tz = account.default_timezone
    end_date = datetime.now(tz)
    start_date = end_date - timedelta(days=days)
    
    # Get sent items to analyze reply patterns
    sent_items = account.sent.filter(
        datetime_sent__range=(start_date, end_date)
    ).order_by('-datetime_sent')
    
    response_times = []
    total_replies = 0
    
    # TODO: Implement accurate response time calculation by correlating
    # sent emails with original received emails via conversation_id
    # For now, we count replies but cannot measure time without original timestamps
    try:
        # Sample to avoid timeout
        for sent_email in sent_items.all()[:500]:
            # Check if this is a reply (has In-Reply-To header or conversation)
            if hasattr(sent_email, 'conversation_id') and sent_email.conversation_id:
                total_replies += 1
                # Note: Accurate response time calculation requires
                # correlating with original message timestamps
                # This is a placeholder for the algorithm
    except Exception as e:
        _logger.warning(f"Error analyzing response times: {e}")
    
    # Calculate stats if we have data (placeholder)
    if response_times:
        return {
            "avg_minutes": round(mean(response_times), 1),
            "median_minutes": round(median(response_times), 1),
            "min_minutes": min(response_times),
            "max_minutes": max(response_times),
            "sample_count": len(response_times),
        }
    else:
        return {
            "avg_minutes": 0,
            "median_minutes": 0,
            "min_minutes": 0,
            "max_minutes": 0,
            "sample_count": 0,
            "note": "Response time calculation not yet implemented. "
                   "Returns reply count only. See TODO in get_response_time().",
        }


def get_top_senders(account: Account, limit: int = 10, days: int = 30) -> List[Dict[str, Any]]:
    """
    Get top senders by email count.
    
    Args:
        account: Exchange account
        limit: Maximum number of senders to return
        days: Number of days to analyze
        
    Returns:
        List of dictionaries with sender statistics
    """
    _logger.info(f"Getting top {limit} senders for last {days} days")
    
    tz = account.default_timezone
    end_date = datetime.now(tz)
    start_date = end_date - timedelta(days=days)
    
    # Query inbox emails
    inbox_emails = account.inbox.filter(
        datetime_received__range=(start_date, end_date)
    )
    
    # Count senders
    sender_counts = Counter()
    sender_names = {}
    sender_unread = Counter()
    
    try:
        # Sample to avoid timeout
        for email in inbox_emails.all()[:2000]:
            if email.sender and email.sender.email_address:
                email_addr = email.sender.email_address
                sender_counts[email_addr] += 1
                sender_names[email_addr] = email.sender.name or email_addr
                
                if not email.is_read:
                    sender_unread[email_addr] += 1
                    
    except Exception as e:
        _logger.warning(f"Error counting senders: {e}")
    
    # Build result list
    result = []
    for email_addr, count in sender_counts.most_common(limit):
        result.append({
            "email": email_addr,
            "name": sender_names.get(email_addr, email_addr),
            "count": count,
            "unread": sender_unread.get(email_addr, 0),
        })
    
    return result


def get_activity_heatmap(account: Account, days: int = 30) -> Dict[str, Any]:
    """
    Generate activity heatmap data.
    
    Analyzes email activity by hour and day of week.
    
    Args:
        account: Exchange account
        days: Number of days to analyze
        
    Returns:
        Dictionary with heatmap data
    """
    _logger.info(f"Generating activity heatmap for last {days} days")
    
    tz = account.default_timezone
    end_date = datetime.now(tz)
    start_date = end_date - timedelta(days=days)
    
    # Query inbox emails
    inbox_emails = account.inbox.filter(
        datetime_received__range=(start_date, end_date)
    )
    
    # Count by hour and day
    hour_counts = Counter()  # 0-23
    day_counts = Counter()   # 0-6 (Mon-Sun)
    hour_day_matrix = {}     # (hour, day) -> count
    
    try:
        for email in inbox_emails.all()[:3000]:
            if email.datetime_received:
                dt = email.datetime_received
                hour = dt.hour
                day = dt.weekday()
                
                hour_counts[hour] += 1
                day_counts[day] += 1
                
                key = (hour, day)
                hour_day_matrix[key] = hour_day_matrix.get(key, 0) + 1
                
    except Exception as e:
        _logger.warning(f"Error generating heatmap: {e}")
    
    # Build hour array (0-23)
    hours = [hour_counts.get(h, 0) for h in range(24)]
    
    # Build day array (Mon-Sun = 0-6)
    days_list = [day_counts.get(d, 0) for d in range(7)]
    
    # Find peak times
    peak_hour = max(range(24), key=lambda h: hours[h]) if any(hours) else 0
    peak_day = max(range(7), key=lambda d: days_list[d]) if any(days_list) else 0
    
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    return {
        "by_hour": hours,
        "by_day": days_list,
        "peak_hour": peak_hour,
        "peak_day": day_names[peak_day],
        "matrix": {
            f"{h}:{d}": hour_day_matrix.get((h, d), 0)
            for h in range(24)
            for d in range(7)
        }
    }


def get_folder_stats(account: Account) -> List[Dict[str, Any]]:
    """
    Get statistics for each email folder.
    
    Args:
        account: Exchange account
        
    Returns:
        List of dictionaries with folder statistics
    """
    _logger.info("Getting folder statistics")
    
    folders = []
    
    # Get main folders
    # Note: account.deleted may not exist on all Exchange versions
    main_folders = [
        ("Inbox", account.inbox),
        ("Sent", account.sent),
        ("Drafts", account.drafts),
        ("Junk", account.junk),
    ]
    
    # Try to get deleted items folder (may not exist)
    if hasattr(account, 'deleted'):
        main_folders.append(("Deleted", account.deleted))
    
    for name, folder in main_folders:
        try:
            total = folder.total_count
            unread = folder.unread_count
            folders.append({
                "name": name,
                "total": total or 0,
                "unread": unread or 0,
            })
        except Exception as e:
            _logger.warning(f"Could not get stats for {name}: {e}")
            folders.append({
                "name": name,
                "total": 0,
                "unread": 0,
                "error": str(e),
            })
    
    return folders


def get_full_report(account: Account, days: int = 30) -> Dict[str, Any]:
    """
    Generate a comprehensive analytics report.
    
    Args:
        account: Exchange account
        days: Number of days to analyze
        
    Returns:
        Dictionary with complete analytics report
    """
    _logger.info(f"Generating full report for last {days} days")
    
    return {
        "period": {
            "days": days,
            "start": (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d"),
            "end": datetime.now().strftime("%Y-%m-%d"),
        },
        "email_stats": get_email_stats(account, days),
        "response_time": get_response_time(account, days),
        "top_senders": get_top_senders(account, limit=10, days=days),
        "activity_heatmap": get_activity_heatmap(account, days),
        "folder_stats": get_folder_stats(account),
    }


# =============================================================================
# CLI Commands
# =============================================================================

def cmd_stats(args: argparse.Namespace) -> None:
    """CLI command for email statistics."""
    account = get_account()
    stats = get_email_stats(account, days=args.days)
    out({"ok": True, "stats": stats})


def cmd_response_time(args: argparse.Namespace) -> None:
    """CLI command for response time analysis."""
    account = get_account()
    result = get_response_time(account, days=args.days)
    out({"ok": True, "response_time": result})


def cmd_top_senders(args: argparse.Namespace) -> None:
    """CLI command for top senders."""
    account = get_account()
    senders = get_top_senders(account, limit=args.limit, days=args.days)
    out({"ok": True, "count": len(senders), "senders": senders})


def cmd_heatmap(args: argparse.Namespace) -> None:
    """CLI command for activity heatmap."""
    account = get_account()
    heatmap = get_activity_heatmap(account, days=args.days)
    out({"ok": True, "heatmap": heatmap})


def cmd_folders(args: argparse.Namespace) -> None:
    """CLI command for folder statistics."""
    account = get_account()
    folders = get_folder_stats(account)
    out({"ok": True, "count": len(folders), "folders": folders})


def cmd_report(args: argparse.Namespace) -> None:
    """CLI command for full analytics report."""
    account = get_account()
    report = get_full_report(account, days=args.days)
    out({"ok": True, "report": report})


def add_parser(subparsers):
    """Add analytics commands to CLI."""
    # stats command
    stats_parser = subparsers.add_parser("stats", help="Get email statistics")
    stats_parser.add_argument("--days", type=int, default=30,
                              help="Number of days to analyze (default: 30)")
    stats_parser.set_defaults(func=cmd_stats)
    
    # response-time command
    rt_parser = subparsers.add_parser("response-time", help="Get response time analysis")
    rt_parser.add_argument("--days", type=int, default=30,
                          help="Number of days to analyze (default: 30)")
    rt_parser.set_defaults(func=cmd_response_time)
    
    # top-senders command
    ts_parser = subparsers.add_parser("top-senders", help="Get top senders")
    ts_parser.add_argument("--limit", type=int, default=10,
                          help="Maximum number of senders (default: 10)")
    ts_parser.add_argument("--days", type=int, default=30,
                          help="Number of days to analyze (default: 30)")
    ts_parser.set_defaults(func=cmd_top_senders)
    
    # heatmap command
    hm_parser = subparsers.add_parser("heatmap", help="Get activity heatmap")
    hm_parser.add_argument("--days", type=int, default=30,
                           help="Number of days to analyze (default: 30)")
    hm_parser.set_defaults(func=cmd_heatmap)
    
    # folders command
    fd_parser = subparsers.add_parser("folders", help="Get folder statistics")
    fd_parser.set_defaults(func=cmd_folders)
    
    # report command
    rp_parser = subparsers.add_parser("report", help="Get full analytics report")
    rp_parser.add_argument("--days", type=int, default=30,
                           help="Number of days to analyze (default: 30)")
    rp_parser.set_defaults(func=cmd_report)


def main():
    """Main entry point for analytics CLI."""
    add_json_argument(parser)
    add_json_argument(parser)
    parser = argparse.ArgumentParser(
        description="Email analytics and reporting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s stats --days 7
  %(prog)s top-senders --limit 20
  %(prog)s report --days 30
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Analytics command")
    
    # stats command
    stats_parser = subparsers.add_parser("stats", help="Get email statistics")
    stats_parser.add_argument("--days", type=int, default=30,
                              help="Number of days to analyze (default: 30)")
    
    # response-time command
    rt_parser = subparsers.add_parser("response-time", help="Get response time analysis")
    rt_parser.add_argument("--days", type=int, default=30,
                           help="Number of days to analyze (default: 30)")
    
    # top-senders command
    ts_parser = subparsers.add_parser("top-senders", help="Get top senders")
    ts_parser.add_argument("--limit", type=int, default=10,
                           help="Maximum number of senders (default: 10)")
    ts_parser.add_argument("--days", type=int, default=30,
                           help="Number of days to analyze (default: 30)")
    
    # heatmap command
    hm_parser = subparsers.add_parser("heatmap", help="Get activity heatmap")
    hm_parser.add_argument("--days", type=int, default=30,
                           help="Number of days to analyze (default: 30)")
    
    # folders command
    fd_parser = subparsers.add_parser("folders", help="Get folder statistics")
    
    # report command
    rp_parser = subparsers.add_parser("report", help="Get full analytics report")
    rp_parser.add_argument("--days", type=int, default=30,
                           help="Number of days to analyze (default: 30)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Route to command handler
    commands = {
        "stats": cmd_stats,
        "response-time": cmd_response_time,
        "top-senders": cmd_top_senders,
        "heatmap": cmd_heatmap,
        "folders": cmd_folders,
        "report": cmd_report,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
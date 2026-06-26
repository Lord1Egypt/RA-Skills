#!/usr/bin/env python3
"""
Analyze Glucose Trends
Perform statistical analysis and generate visualizations
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from data_manager import GlucoseDataManager


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Analyze glucose trends and generate reports'
    )
    
    parser.add_argument(
        '--period', '-p',
        type=str,
        choices=['day', 'week', 'month', 'quarter', 'year', 'all'],
        default='week',
        help='Time period to analyze (default: week)'
    )
    
    parser.add_argument(
        '--type', '-t',
        type=str,
        choices=['all', 'fasting', 'post-meal', 'pre-meal', 'bedtime'],
        default='all',
        help='Type of readings to analyze (default: all)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        choices=['text', 'chart', 'report', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '--output-file',
        type=str,
        help='Output file path (for chart or report)'
    )
    
    return parser.parse_args()


def get_period_dates(period: str) -> tuple:
    """
    Get start and end dates for a period
    
    Args:
        period: Period name (day, week, month, etc.)
    
    Returns:
        Tuple of (start_date, end_date) as ISO strings
    """
    end_date = datetime.now()
    
    if period == 'day':
        start_date = end_date - timedelta(days=1)
    elif period == 'week':
        start_date = end_date - timedelta(weeks=1)
    elif period == 'month':
        start_date = end_date - timedelta(days=30)
    elif period == 'quarter':
        start_date = end_date - timedelta(days=90)
    elif period == 'year':
        start_date = end_date - timedelta(days=365)
    else:  # all
        start_date = datetime(2000, 1, 1)
    
    return start_date.isoformat(), end_date.isoformat()


def analyze_patterns(readings: list) -> dict:
    """
    Analyze glucose patterns in the data
    
    Args:
        readings: List of glucose readings
    
    Returns:
        Dictionary of pattern analysis
    """
    if len(readings) < 7:
        return {
            'message': 'Insufficient data for pattern analysis (need at least 7 readings)'
        }
    
    patterns = {}
    
    # Group by meal context
    context_groups = {}
    for reading in readings:
        context = reading.get('meal_context', 'unspecified')
        if context not in context_groups:
            context_groups[context] = []
        context_groups[context].append(reading['value'])
    
    # Calculate context averages
    patterns['by_meal_context'] = {}
    for context, values in context_groups.items():
        import statistics
        patterns['by_meal_context'][context] = {
            'count': len(values),
            'average': statistics.mean(values),
            'std_dev': statistics.stdev(values) if len(values) > 1 else 0
        }
    
    # Identify time-of-day patterns
    from collections import defaultdict
    time_groups = defaultdict(list)
    
    for reading in readings:
        if 'timestamp' in reading:
            try:
                dt = datetime.fromisoformat(reading['timestamp'].replace('Z', '+00:00'))
                hour = dt.hour
                
                if 6 <= hour < 12:
                    period = 'morning'
                elif 12 <= hour < 18:
                    period = 'afternoon'
                elif 18 <= hour < 22:
                    period = 'evening'
                else:
                    period = 'night'
                
                time_groups[period].append(reading['value'])
            except:
                pass
    
    patterns['by_time_of_day'] = {}
    for period, values in time_groups.items():
        import statistics
        patterns['by_time_of_day'][period] = {
            'count': len(values),
            'average': statistics.mean(values)
        }
    
    # Identify trends
    if len(readings) >= 14:
        # Simple trend analysis - compare first half to second half
        mid = len(readings) // 2
        first_half = [r['value'] for r in readings[:mid]]
        second_half = [r['value'] for r in readings[mid:]]
        
        import statistics
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        change_percent = ((second_avg - first_avg) / first_avg) * 100
        
        if change_percent > 10:
            trend = 'increasing'
        elif change_percent < -10:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        patterns['trend'] = {
            'direction': trend,
            'change_percent': change_percent,
            'first_period_avg': first_avg,
            'second_period_avg': second_avg
        }
    
    return patterns


def generate_text_report(stats: dict, patterns: dict, period: str) -> str:
    """Generate a text-based analysis report"""
    report = []
    report.append("=" * 60)
    report.append("GLUCOSE ANALYSIS REPORT")
    report.append("=" * 60)
    report.append(f"\nPeriod: {period.upper()}")
    report.append(f"Total Readings: {stats['count']}")
    
    if stats['count'] == 0:
        report.append("\nNo readings found for this period.")
        return '\n'.join(report)
    
    report.append("\n" + "-" * 60)
    report.append("STATISTICS")
    report.append("-" * 60)
    report.append(f"Average: {stats['mean']:.1f} mmol/L")
    report.append(f"Median: {stats['median']:.1f} mmol/L")
    report.append(f"Range: {stats['min']:.1f} - {stats['max']:.1f} mmol/L")
    report.append(f"Standard Deviation: {stats['std_dev']:.2f}")
    report.append(f"Coefficient of Variation: {stats['cv']:.1f}%")
    
    report.append("\n" + "-" * 60)
    report.append("TIME IN RANGE")
    report.append("-" * 60)
    report.append(f"Target Range (4.0-10.0 mmol/L): {stats['time_in_range']['in_range']:.1f}%")
    report.append(f"Below Range (<4.0 mmol/L): {stats['time_in_range']['below_range']:.1f}%")
    report.append(f"Above Range (>10.0 mmol/L): {stats['time_in_range']['above_range']:.1f}%")
    
    # Add patterns
    if 'by_meal_context' in patterns and patterns['by_meal_context']:
        report.append("\n" + "-" * 60)
        report.append("BY MEAL CONTEXT")
        report.append("-" * 60)
        for context, data in patterns['by_meal_context'].items():
            report.append(f"{context.capitalize()}: {data['average']:.1f} mmol/L (n={data['count']})")
    
    if 'by_time_of_day' in patterns and patterns['by_time_of_day']:
        report.append("\n" + "-" * 60)
        report.append("BY TIME OF DAY")
        report.append("-" * 60)
        for period, data in patterns['by_time_of_day'].items():
            report.append(f"{period.capitalize()}: {data['average']:.1f} mmol/L (n={data['count']})")
    
    if 'trend' in patterns:
        report.append("\n" + "-" * 60)
        report.append("TREND ANALYSIS")
        report.append("-" * 60)
        trend = patterns['trend']
        report.append(f"Direction: {trend['direction'].upper()}")
        report.append(f"Change: {trend['change_percent']:+.1f}%")
    
    report.append("\n" + "=" * 60)
    
    return '\n'.join(report)


def generate_chart(readings: list, stats: dict, output_file: str = None):
    """Generate a glucose trend chart"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from datetime import datetime
    except ImportError:
        print("Error: matplotlib is required for chart generation")
        print("Install with: pip install matplotlib")
        return None
    
    # Prepare data
    timestamps = []
    values = []
    
    for reading in readings:
        if 'timestamp' in reading:
            try:
                dt = datetime.fromisoformat(reading['timestamp'].replace('Z', '+00:00'))
                timestamps.append(dt)
                values.append(reading['value'])
            except:
                continue
    
    if not timestamps:
        print("No valid timestamps found for chart")
        return None
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot glucose values
    ax.plot(timestamps, values, 'b-', linewidth=1.5, marker='o', markersize=4, label='Glucose')
    
    # Add target range
    ax.axhspan(4.0, 10.0, alpha=0.2, color='green', label='Target Range')
    ax.axhline(y=4.0, color='orange', linestyle='--', linewidth=1, label='Low Threshold')
    ax.axhline(y=10.0, color='red', linestyle='--', linewidth=1, label='High Threshold')
    
    # Add average line
    ax.axhline(y=stats['mean'], color='blue', linestyle=':', linewidth=1.5, 
               label=f'Average ({stats["mean"]:.1f})')
    
    # Formatting
    ax.set_xlabel('Date/Time', fontsize=10)
    ax.set_ylabel('Glucose (mmol/L)', fontsize=10)
    ax.set_title('Blood Glucose Trend', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    # Save or show
    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"✓ Chart saved to: {output_file}")
        return output_file
    else:
        plt.show()
        return None


def main():
    """Main analysis function"""
    args = parse_args()
    
    # Get date range
    start_date, end_date = get_period_dates(args.period)
    
    # Load readings
    manager = GlucoseDataManager()
    readings = manager.get_readings(start_date, end_date)
    
    # Filter by type if needed
    if args.type != 'all':
        readings = [r for r in readings if r.get('meal_context') == args.type]
    
    print(f"\nAnalyzing {len(readings)} readings...")
    
    # Calculate statistics
    stats = manager.get_statistics(start_date, end_date)
    
    # Analyze patterns
    patterns = analyze_patterns(readings)
    
    # Generate output
    if args.output == 'text':
        report = generate_text_report(stats, patterns, args.period)
        print(report)
    
    elif args.output == 'chart':
        output_file = args.output_file or 'glucose_trend.png'
        generate_chart(readings, stats, output_file)
    
    elif args.output == 'report':
        # Generate both text report and chart
        report = generate_text_report(stats, patterns, args.period)
        
        if args.output_file:
            chart_file = Path(args.output_file).with_suffix('.png')
            report_file = Path(args.output_file).with_suffix('.txt')
        else:
            chart_file = 'glucose_trend.png'
            report_file = 'glucose_report.txt'
        
        generate_chart(readings, stats, str(chart_file))
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✓ Report saved to: {report_file}")
        print(f"✓ Chart saved to: {chart_file}")
    
    elif args.output == 'json':
        result = {
            'statistics': stats,
            'patterns': patterns,
            'readings_count': len(readings)
        }
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

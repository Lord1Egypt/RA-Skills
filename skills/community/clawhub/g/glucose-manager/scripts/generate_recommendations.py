#!/usr/bin/env python3
"""
Generate Personalized Recommendations
Create health recommendations based on glucose patterns
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import statistics

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from data_manager import GlucoseDataManager


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Generate personalized health recommendations'
    )
    
    parser.add_argument(
        '--type', '-t',
        type=str,
        choices=['meal', 'activity', 'monitoring', 'all'],
        default='all',
        help='Type of recommendation to generate'
    )
    
    parser.add_argument(
        '--meal',
        type=str,
        choices=['breakfast', 'lunch', 'dinner', 'snack'],
        help='Specific meal for recommendations'
    )
    
    parser.add_argument(
        '--time',
        type=str,
        help='Time for activity recommendation (e.g., "now", "morning", "evening")'
    )
    
    return parser.parse_args()


def analyze_glucose_patterns(readings: list) -> dict:
    """
    Analyze glucose patterns to inform recommendations
    
    Args:
        readings: List of glucose readings
    
    Returns:
        Dictionary of pattern analysis
    """
    if len(readings) < 7:
        return {
            'sufficient_data': False,
            'message': 'Need at least 7 readings for pattern analysis'
        }
    
    analysis = {'sufficient_data': True}
    
    # Recent statistics
    recent_values = [r['value'] for r in readings[-20:]]
    analysis['avg_glucose'] = statistics.mean(recent_values)
    analysis['std_dev'] = statistics.stdev(recent_values) if len(recent_values) > 1 else 0
    analysis['cv'] = (analysis['std_dev'] / analysis['avg_glucose']) * 100 if analysis['avg_glucose'] > 0 else 0
    
    # Time in range
    in_range = sum(1 for v in recent_values if 4.0 <= v <= 10.0)
    analysis['time_in_range'] = (in_range / len(recent_values)) * 100
    
    # Post-meal patterns
    post_meal = [r for r in readings if r.get('meal_context') == 'post-meal']
    if post_meal:
        analysis['avg_post_meal'] = statistics.mean([r['value'] for r in post_meal])
    
    # Fasting patterns
    fasting = [r for r in readings if r.get('meal_context') == 'fasting']
    if fasting:
        analysis['avg_fasting'] = statistics.mean([r['value'] for r in fasting])
    
    # Time-of-day patterns
    from collections import defaultdict
    time_patterns = defaultdict(list)
    
    for r in readings:
        if 'timestamp' in r:
            try:
                dt = datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00'))
                hour = dt.hour
                period = 'morning' if 6 <= hour < 12 else \
                        'afternoon' if 12 <= hour < 18 else \
                        'evening' if 18 <= hour < 22 else 'night'
                time_patterns[period].append(r['value'])
            except:
                pass
    
    analysis['time_patterns'] = {
        period: {
            'avg': statistics.mean(values),
            'count': len(values)
        }
        for period, values in time_patterns.items()
    }
    
    return analysis


def generate_meal_recommendations(analysis: dict, meal: str = None) -> list:
    """
    Generate dietary recommendations
    
    Args:
        analysis: Glucose pattern analysis
        meal: Specific meal to recommend for
    
    Returns:
        List of recommendations
    """
    recommendations = []
    
    if not analysis.get('sufficient_data'):
        return ['Insufficient data for personalized recommendations. Continue logging meals and glucose readings.']
    
    # Post-meal glucose spikes
    if analysis.get('avg_post_meal', 0) > 10.0:
        recommendations.append(
            "📊 Your post-meal glucose tends to be elevated. Consider:\n"
            "   • Reducing carbohydrate portions by 10-15%\n"
            "   • Choosing lower glycemic index foods\n"
            "   • Adding more fiber and protein to meals\n"
            "   • Taking a short walk (10-15 min) after eating"
        )
    
    # High variability
    if analysis.get('cv', 0) > 36:
        recommendations.append(
            "📈 Your glucose variability is high. To stabilize:\n"
            "   • Eat meals at consistent times\n"
            "   • Include protein and healthy fats with carbs\n"
            "   • Avoid skipping meals\n"
            "   • Consider smaller, more frequent meals"
        )
    
    # Meal-specific recommendations
    if meal:
        if meal == 'breakfast':
            if analysis.get('avg_fasting', 0) > 7.0:
                recommendations.append(
                    "🌅 Your fasting glucose is elevated. For breakfast:\n"
                    "   • Choose high-fiber, low-sugar options\n"
                    "   • Consider oatmeal with nuts and seeds\n"
                    "   • Avoid fruit juices and refined carbs\n"
                    "   • Include protein (eggs, Greek yogurt)"
                )
            else:
                recommendations.append(
                    "🌅 Breakfast recommendations:\n"
                    "   • Balanced meal with protein, fiber, and complex carbs\n"
                    "   • Good options: eggs with vegetables, whole grain toast with nut butter\n"
                    "   • Avoid sugary cereals and pastries"
                )
        
        elif meal == 'lunch':
            recommendations.append(
                "☀️ Lunch recommendations:\n"
                "   • Aim for a balanced plate: 50% vegetables, 25% protein, 25% complex carbs\n"
                "   • Include leafy greens and lean proteins\n"
                "   • Consider a short walk after lunch if possible"
            )
        
        elif meal == 'dinner':
            if 'evening' in analysis.get('time_patterns', {}):
                evening_avg = analysis['time_patterns']['evening']['avg']
                if evening_avg > 9.0:
                    recommendations.append(
                        "🌙 Your evening glucose tends to be higher. For dinner:\n"
                        "   • Eat earlier (at least 3 hours before bed)\n"
                        "   • Reduce carbohydrate portion\n"
                        "   • Focus on vegetables and lean proteins\n"
                        "   • Avoid late-night snacking"
                    )
                else:
                    recommendations.append(
                        "🌙 Dinner recommendations:\n"
                        "   • Lighter meal compared to lunch\n"
                        "   • Emphasize vegetables and lean proteins\n"
                        "   • Limit refined carbohydrates\n"
                        "   • Finish eating at least 2-3 hours before bedtime"
                    )
        
        elif meal == 'snack':
            recommendations.append(
                "🍎 Healthy snack options:\n"
                "   • Nuts and seeds (small handful)\n"
                "   • Greek yogurt with berries\n"
                "   • Vegetable sticks with hummus\n"
                "   • Hard-boiled eggs\n"
                "   • Cheese with whole grain crackers"
            )
    
    # General meal recommendations
    if not recommendations:
        recommendations.append(
            "🍽️ General meal recommendations:\n"
            "   • Maintain regular meal times\n"
            "   • Balance carbohydrates with protein and healthy fats\n"
            "   • Include fiber-rich vegetables\n"
            "   • Stay hydrated with water\n"
            "   • Monitor portion sizes"
        )
    
    return recommendations


def generate_activity_recommendations(analysis: dict, time: str = None) -> list:
    """
    Generate exercise and activity recommendations
    
    Args:
        analysis: Glucose pattern analysis
        time: Preferred time for activity
    
    Returns:
        List of recommendations
    """
    recommendations = []
    
    if not analysis.get('sufficient_data'):
        return ['Insufficient data for personalized recommendations. Continue logging glucose readings before and after exercise.']
    
    current_hour = datetime.now().hour
    current_glucose = analysis.get('avg_glucose', 0)
    
    # Based on current glucose
    if current_glucose > 13.9:
        recommendations.append(
            "⚠️ HIGH GLUCOSE WARNING:\n"
            "   • Check for ketones before exercising\n"
            "   • Postpone vigorous exercise if ketones present\n"
            "   • Light walking may help lower glucose\n"
            "   • Stay hydrated"
        )
    elif current_glucose < 5.5:
        recommendations.append(
            "⚠️ LOW GLUCOSE WARNING:\n"
            "   • Eat a small snack before exercising\n"
            "   • Have fast-acting glucose available\n"
            "   • Consider delaying exercise\n"
            "   • Monitor glucose during prolonged activity"
        )
    
    # Optimal timing
    if time == 'now' or time is None:
        # Find best time based on patterns
        time_patterns = analysis.get('time_patterns', {})
        
        if time_patterns:
            # Find period with highest average glucose
            best_period = max(time_patterns.items(), key=lambda x: x[1]['avg'])
            period_name = best_period[0]
            
            recommendations.append(
                f"⏰ BEST TIME TO EXERCISE:\n"
                f"   Based on your patterns, exercising in the {period_name} "
                f"may help manage glucose levels better.\n"
                f"   Your {period_name} average: {best_period[1]['avg']:.1f} mmol/L"
            )
    
    # Time-specific recommendations
    if time == 'morning':
        recommendations.append(
            "🌅 Morning exercise recommendations:\n"
            "   • Light to moderate intensity (walking, yoga, light jogging)\n"
            "   • Check glucose before exercising\n"
            "   • May help reduce dawn phenomenon\n"
            "   • Duration: 20-30 minutes"
        )
    elif time == 'afternoon':
        recommendations.append(
            "☀️ Afternoon exercise recommendations:\n"
            "   • Good time for higher intensity exercise\n"
            "   • Body temperature peaks, better performance\n"
            "   • May help with post-lunch glucose control\n"
            "   • Duration: 30-45 minutes"
        )
    elif time == 'evening':
        recommendations.append(
            "🌙 Evening exercise recommendations:\n"
            "   • Finish at least 2-3 hours before bed\n"
            "   • Moderate intensity preferred\n"
            "   • May improve overnight glucose\n"
            "   • Avoid very vigorous exercise close to bedtime"
        )
    
    # General activity recommendations
    recommendations.append(
        "🏃 GENERAL ACTIVITY GUIDELINES:\n"
        "   • Aim for 150 minutes of moderate activity per week\n"
        "   • Include both aerobic and resistance exercises\n"
        "   • Check glucose before and after exercise\n"
        "   • Stay hydrated\n"
        "   • Always carry fast-acting glucose"
    )
    
    return recommendations


def generate_monitoring_recommendations(analysis: dict) -> list:
    """
    Generate glucose monitoring recommendations
    
    Args:
        analysis: Glucose pattern analysis
    
    Returns:
        List of recommendations
    """
    recommendations = []
    
    if not analysis.get('sufficient_data'):
        return ['Continue regular glucose monitoring to gather more data for personalized recommendations.']
    
    # Based on glucose control
    time_in_range = analysis.get('time_in_range', 0)
    avg_glucose = analysis.get('avg_glucose', 0)
    cv = analysis.get('cv', 0)
    
    if time_in_range < 50:
        recommendations.append(
            "📊 INCREASE MONITORING FREQUENCY:\n"
            "   • Check glucose more frequently (4+ times daily)\n"
            "   • Include bedtime and overnight checks\n"
            "   • Test before and 2 hours after meals\n"
            "   • Keep a detailed log with meal information"
        )
    elif time_in_range < 70:
        recommendations.append(
            "📊 MAINTAIN REGULAR MONITORING:\n"
            "   • Continue checking 3-4 times daily\n"
            "   • Include fasting and post-meal checks\n"
            "   • Monitor for patterns and trends\n"
            "   • Review data weekly"
        )
    else:
        recommendations.append(
            "📊 GOOD CONTROL - MAINTAIN:\n"
            "   • Continue current monitoring schedule\n"
            "   • Check at least 2-3 times daily\n"
            "   • Focus on times when glucose is harder to control\n"
            "   • Regular review with healthcare provider"
        )
    
    # High variability
    if cv > 36:
        recommendations.append(
            "📈 HIGH VARIABILITY DETECTED:\n"
            "   • More frequent monitoring recommended\n"
            "   • Identify factors causing fluctuations\n"
            "   • Check glucose before and after specific activities\n"
            "   • Consider continuous glucose monitoring (CGM)"
        )
    
    # When to consult healthcare provider
    if avg_glucose > 10.0 or time_in_range < 40:
        recommendations.append(
            "🏥 CONSULT HEALTHCARE PROVIDER:\n"
            "   • Your glucose control needs attention\n"
            "   • Schedule an appointment soon\n"
            "   • Bring your glucose log\n"
            "   • Discuss medication adjustment if needed"
        )
    
    return recommendations


def main():
    """Main recommendation generation function"""
    args = parse_args()
    
    # Load readings
    manager = GlucoseDataManager()
    readings = manager.get_readings()
    
    # Analyze patterns
    analysis = analyze_glucose_patterns(readings)
    
    print(f"\n{'='*60}")
    print("PERSONALIZED HEALTH RECOMMENDATIONS")
    print(f"{'='*60}")
    
    if not analysis.get('sufficient_data'):
        print("\n" + analysis['message'])
        print("\nContinue logging glucose readings to receive personalized recommendations.")
        return
    
    # Generate recommendations based on type
    if args.type in ['meal', 'all']:
        print(f"\n{'─'*60}")
        print("🍽️ DIETARY RECOMMENDATIONS")
        print(f"{'─'*60}")
        
        meal_recs = generate_meal_recommendations(analysis, args.meal)
        for rec in meal_recs:
            print(f"\n{rec}")
    
    if args.type in ['activity', 'all']:
        print(f"\n{'─'*60}")
        print("🏃 ACTIVITY RECOMMENDATIONS")
        print(f"{'─'*60}")
        
        activity_recs = generate_activity_recommendations(analysis, args.time)
        for rec in activity_recs:
            print(f"\n{rec}")
    
    if args.type in ['monitoring', 'all']:
        print(f"\n{'─'*60}")
        print("📊 MONITORING RECOMMENDATIONS")
        print(f"{'─'*60}")
        
        monitoring_recs = generate_monitoring_recommendations(analysis)
        for rec in monitoring_recs:
            print(f"\n{rec}")
    
    # Summary stats
    print(f"\n{'='*60}")
    print("GLUCOSE SUMMARY")
    print(f"{'='*60}")
    print(f"\n  Average Glucose: {analysis['avg_glucose']:.1f} mmol/L")
    print(f"  Time in Range: {analysis['time_in_range']:.1f}%")
    print(f"  Variability (CV): {analysis['cv']:.1f}%")
    
    print(f"\n{'='*60}")
    print("\n⚠ These recommendations are for informational purposes only.")
    print("  Always consult your healthcare provider before making")
    print("  changes to your diabetes management plan.\n")


if __name__ == "__main__":
    main()

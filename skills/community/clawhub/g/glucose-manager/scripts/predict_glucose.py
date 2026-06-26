#!/usr/bin/env python3
"""
Predict Glucose Levels
Predict future glucose levels and assess risks
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
        description='Predict glucose levels and assess risks'
    )
    
    parser.add_argument(
        '--horizon', '-H',
        type=str,
        choices=['2h', '4h', '8h', '12h', '24h'],
        default='4h',
        help='Prediction horizon (default: 4h)'
    )
    
    parser.add_argument(
        '--risk-type',
        type=str,
        choices=['hypoglycemia', 'hyperglycemia', 'all'],
        default='all',
        help='Type of risk to assess'
    )
    
    parser.add_argument(
        '--period',
        type=str,
        choices=['tonight', 'tomorrow', 'next-meal', 'custom'],
        help='Period for risk assessment'
    )
    
    parser.add_argument(
        '--min-readings',
        type=int,
        default=14,
        help='Minimum number of readings required for prediction (default: 14)'
    )
    
    return parser.parse_args()


def predict_short_term(readings: list, horizon_hours: int) -> dict:
    """
    Predict glucose levels for the next few hours using simple trend extrapolation
    
    Args:
        readings: List of recent glucose readings
        horizon_hours: Number of hours to predict ahead
    
    Returns:
        Dictionary with prediction results
    """
    if len(readings) < 7:
        return {
            'status': 'insufficient_data',
            'message': f'Need at least 7 readings for prediction (have {len(readings)})'
        }
    
    # Get recent readings (last 24 hours)
    now = datetime.now()
    recent = []
    for r in readings:
        if 'timestamp' in r:
            try:
                dt = datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00'))
                hours_ago = (now - dt).total_seconds() / 3600
                if hours_ago <= 24:
                    recent.append({
                        'timestamp': dt,
                        'value': r['value'],
                        'hours_ago': hours_ago
                    })
            except:
                continue
    
    if len(recent) < 3:
        return {
            'status': 'insufficient_recent_data',
            'message': 'Need at least 3 readings in the last 24 hours'
        }
    
    # Sort by timestamp
    recent.sort(key=lambda x: x['timestamp'])
    
    # Calculate recent trend
    values = [r['value'] for r in recent]
    current_glucose = values[-1]
    
    # Calculate rate of change
    if len(values) >= 2:
        time_diff = (recent[-1]['timestamp'] - recent[-2]['timestamp']).total_seconds() / 3600
        if time_diff > 0:
            rate_of_change = (values[-1] - values[-2]) / time_diff
        else:
            rate_of_change = 0
    else:
        rate_of_change = 0
    
    # Predict future values
    predicted_values = []
    for hour in range(1, horizon_hours + 1):
        # Simple linear prediction with damping
        damping_factor = 0.8 ** hour  # Damping increases with time
        predicted_value = current_glucose + (rate_of_change * hour * damping_factor)
        
        # Add some uncertainty range
        uncertainty = 0.5 * (hour ** 0.5)  # Uncertainty increases with square root of time
        
        predicted_values.append({
            'hour': hour,
            'predicted': round(predicted_value, 1),
            'range_low': round(predicted_value - uncertainty, 1),
            'range_high': round(predicted_value + uncertainty, 1)
        })
    
    # Assess risk
    risks = []
    for pred in predicted_values:
        if pred['predicted'] < 4.0:
            risks.append({
                'hour': pred['hour'],
                'type': 'hypoglycemia',
                'severity': 'moderate' if pred['predicted'] > 3.0 else 'severe',
                'predicted_value': pred['predicted']
            })
        elif pred['predicted'] > 13.9:
            risks.append({
                'hour': pred['hour'],
                'type': 'hyperglycemia',
                'severity': 'moderate' if pred['predicted'] < 16.7 else 'severe',
                'predicted_value': pred['predicted']
            })
    
    return {
        'status': 'success',
        'current_glucose': current_glucose,
        'rate_of_change': round(rate_of_change, 2),
        'predictions': predicted_values,
        'risks': risks,
        'confidence': 'low' if len(recent) < 5 else 'medium' if len(recent) < 10 else 'high'
    }


def assess_hypoglycemia_risk(readings: list, period: str = None) -> dict:
    """
    Assess risk of hypoglycemia
    
    Args:
        readings: List of glucose readings
        period: Time period to assess ('tonight', 'tomorrow', etc.)
    
    Returns:
        Risk assessment dictionary
    """
    if len(readings) < 7:
        return {
            'risk_level': 'unknown',
            'message': 'Insufficient data for risk assessment'
        }
    
    # Calculate recent statistics
    recent_values = [r['value'] for r in readings[-20:]]  # Last 20 readings
    avg_glucose = statistics.mean(recent_values)
    std_dev = statistics.stdev(recent_values) if len(recent_values) > 1 else 0
    
    # Count low readings
    low_count = sum(1 for v in recent_values if v < 4.0)
    low_percentage = (low_count / len(recent_values)) * 100
    
    # Calculate risk score (0-100)
    risk_score = 0
    
    # Factor 1: Average glucose level
    if avg_glucose < 5.0:
        risk_score += 30
    elif avg_glucose < 5.5:
        risk_score += 15
    elif avg_glucose < 6.0:
        risk_score += 5
    
    # Factor 2: Variability
    cv = (std_dev / avg_glucose) * 100 if avg_glucose > 0 else 0
    if cv > 36:  # High variability
        risk_score += 25
    elif cv > 30:
        risk_score += 15
    
    # Factor 3: Recent low readings
    if low_percentage > 20:
        risk_score += 30
    elif low_percentage > 10:
        risk_score += 20
    elif low_percentage > 5:
        risk_score += 10
    
    # Factor 4: Time of day patterns
    now = datetime.now()
    hour = now.hour
    
    # Higher risk at night or early morning
    if 22 <= hour or hour < 6:
        risk_score += 15
    elif 6 <= hour < 9:
        risk_score += 5  # Dawn phenomenon consideration
    
    # Determine risk level
    if risk_score >= 60:
        risk_level = 'high'
        recommendation = 'HIGH RISK: Consider checking glucose more frequently. Have fast-acting glucose available.'
    elif risk_score >= 30:
        risk_level = 'moderate'
        recommendation = 'MODERATE RISK: Monitor glucose closely. Be prepared for potential lows.'
    else:
        risk_level = 'low'
        recommendation = 'LOW RISK: Continue regular monitoring.'
    
    return {
        'risk_level': risk_level,
        'risk_score': risk_score,
        'factors': {
            'average_glucose': round(avg_glucose, 1),
            'variability_cv': round(cv, 1),
            'low_readings_percentage': round(low_percentage, 1),
            'recent_lows': low_count
        },
        'recommendation': recommendation,
        'period': period
    }


def assess_hyperglycemia_risk(readings: list, period: str = None) -> dict:
    """
    Assess risk of hyperglycemia
    
    Args:
        readings: List of glucose readings
        period: Time period to assess
    
    Returns:
        Risk assessment dictionary
    """
    if len(readings) < 7:
        return {
            'risk_level': 'unknown',
            'message': 'Insufficient data for risk assessment'
        }
    
    recent_values = [r['value'] for r in readings[-20:]]
    avg_glucose = statistics.mean(recent_values)
    std_dev = statistics.stdev(recent_values) if len(recent_values) > 1 else 0
    
    # Count high readings
    high_count = sum(1 for v in recent_values if v > 10.0)
    very_high_count = sum(1 for v in recent_values if v > 13.9)
    high_percentage = (high_count / len(recent_values)) * 100
    
    # Calculate risk score
    risk_score = 0
    
    # Factor 1: Average glucose
    if avg_glucose > 10.0:
        risk_score += 30
    elif avg_glucose > 8.0:
        risk_score += 20
    elif avg_glucose > 7.0:
        risk_score += 10
    
    # Factor 2: Variability
    cv = (std_dev / avg_glucose) * 100 if avg_glucose > 0 else 0
    if cv > 36:
        risk_score += 20
    elif cv > 30:
        risk_score += 10
    
    # Factor 3: High readings
    if very_high_count > 0:
        risk_score += 30
    elif high_percentage > 30:
        risk_score += 25
    elif high_percentage > 15:
        risk_score += 15
    
    # Determine risk level
    if risk_score >= 60:
        risk_level = 'high'
        recommendation = 'HIGH RISK: Consider consulting healthcare provider. Review medication and diet.'
    elif risk_score >= 30:
        risk_level = 'moderate'
        recommendation = 'MODERATE RISK: Monitor glucose patterns. Consider dietary adjustments.'
    else:
        risk_level = 'low'
        recommendation = 'LOW RISK: Continue regular monitoring and healthy habits.'
    
    return {
        'risk_level': risk_level,
        'risk_score': risk_score,
        'factors': {
            'average_glucose': round(avg_glucose, 1),
            'variability_cv': round(cv, 1),
            'high_readings_percentage': round(high_percentage, 1),
            'recent_highs': high_count
        },
        'recommendation': recommendation,
        'period': period
    }


def main():
    """Main prediction function"""
    args = parse_args()
    
    # Load readings
    manager = GlucoseDataManager()
    readings = manager.get_readings()
    
    if len(readings) < args.min_readings:
        print(f"\n⚠ Warning: Only {len(readings)} readings available.")
        print(f"  Recommended minimum: {args.min_readings} readings")
        print(f"  Predictions may be less accurate with limited data.\n")
    
    # Parse horizon
    horizon_hours = int(args.horizon.replace('h', ''))
    
    # Perform prediction
    print(f"\n{'='*60}")
    print("GLUCOSE PREDICTION")
    print(f"{'='*60}")
    
    prediction = predict_short_term(readings, horizon_hours)
    
    if prediction['status'] != 'success':
        print(f"\n{prediction['message']}")
        return
    
    print(f"\nCurrent Glucose: {prediction['current_glucose']:.1f} mmol/L")
    print(f"Rate of Change: {prediction['rate_of_change']:+.2f} mmol/L/hour")
    print(f"Confidence: {prediction['confidence'].upper()}")
    
    print(f"\n{'-'*60}")
    print("PREDICTED GLUCOSE LEVELS")
    print(f"{'-'*60}")
    
    for pred in prediction['predictions']:
        print(f"  +{pred['hour']}h: {pred['predicted']:.1f} mmol/L "
              f"(range: {pred['range_low']:.1f} - {pred['range_high']:.1f})")
    
    # Risk assessment
    print(f"\n{'='*60}")
    print("RISK ASSESSMENT")
    print(f"{'='*60}")
    
    if args.risk_type in ['hypoglycemia', 'all']:
        hypo_risk = assess_hypoglycemia_risk(readings, args.period)
        print(f"\n📉 HYPOGLYCEMIA RISK: {hypo_risk['risk_level'].upper()}")
        print(f"   Risk Score: {hypo_risk['risk_score']}/100")
        print(f"   {hypo_risk['recommendation']}")
    
    if args.risk_type in ['hyperglycemia', 'all']:
        hyper_risk = assess_hyperglycemia_risk(readings, args.period)
        print(f"\n📈 HYPERGLYCEMIA RISK: {hyper_risk['risk_level'].upper()}")
        print(f"   Risk Score: {hyper_risk['risk_score']}/100")
        print(f"   {hyper_risk['recommendation']}")
    
    # Warnings
    if prediction['risks']:
        print(f"\n{'='*60}")
        print("⚠ WARNINGS")
        print(f"{'='*60}")
        for risk in prediction['risks']:
            print(f"  Hour {risk['hour']}: {risk['severity'].upper()} {risk['type']} risk")
            print(f"    Predicted: {risk['predicted_value']:.1f} mmol/L")
    
    print(f"\n{'='*60}")
    print("\n⚠ DISCLAIMER: These predictions are for informational purposes only.")
    print("  They do not replace professional medical advice. Always consult")
    print("  your healthcare provider for medical decisions.\n")


if __name__ == "__main__":
    main()

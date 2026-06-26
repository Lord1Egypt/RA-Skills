#!/usr/bin/env python3
"""
Garmin Connect 30-Day Health Data Sync
Fetches 30 days of complete health data and generates interactive dashboard
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    from garth import Client
    from garminconnect import Garmin
except ImportError as e:
    print(f"❌ Dependencies missing: {e}")
    print("Run: pip install garth garminconnect")
    sys.exit(1)

def load_garth_session():
    """Load saved Garmin OAuth session"""
    session_file = Path.home() / ".garth" / "session.json"

    if not session_file.exists():
        print(f"❌ No OAuth session found at {session_file}")
        print("\nRun: python3 garmin-auth.py <email> <password>")
        return None

    try:
        client = Client()
        client.load(str(session_file))
        return client
    except Exception as e:
        print(f"❌ Failed to load session: {e}")
        return None

def get_daily_summary(garth_client, date_str):
    """Get daily summary with retry logic for 429 errors"""
    import time

    max_retries = 3
    retry_delays = [60, 120, 240]  # Exponential backoff

    for attempt in range(max_retries):
        try:
            gc = Garmin()
            gc.garth = garth_client
            summary = gc.get_user_summary(date_str)

            return {
                'steps': summary.get('totalSteps', 0),
                'heart_rate_resting': summary.get('restingHeartRate', 0),
                'calories': summary.get('totalKilocalories', 0),
                'active_minutes': summary.get('totalIntensityMinutes', 0),
                'distance_km': round(summary.get('totalDistance', 0) / 1000, 2),
            }
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait = retry_delays[attempt]
                print(f"⚠️  Rate limited (429). Waiting {wait}s before retry...")
                time.sleep(wait)
                continue
            elif "403" in str(e):
                # Try alternate endpoint
                try:
                    # Use daily summary endpoint directly
                    gc = Garmin()
                    gc.garth = garth_client
                    # Try get daily stats via different method
                    stats = gc.get_stats(date_str)
                    return {
                        'steps': stats.get('dailySteps', 0),
                        'heart_rate_resting': stats.get('restingHeartRate', 0),
                        'calories': stats.get('totalKilocalories', 0),
                        'active_minutes': stats.get('totalIntensityMinutes', 0),
                        'distance_km': 0,
                    }
                except:
                    print(f"⚠️  Daily summary error for {date_str}: {e}")
                    return None
            else:
                print(f"⚠️  Daily summary error for {date_str}: {e}")
                return None

    return None

def get_sleep_data(garth_client, date_str):
    """Get sleep data for a specific date"""
    try:
        gc = Garmin()
        gc.garth = garth_client
        sleep = gc.get_sleep_data(date_str)

        if sleep and 'dailySleepDTO' in sleep:
            s = sleep['dailySleepDTO']
            duration_sec = s.get('sleepTimeSeconds', 0)
            return {
                'date': date_str,
                'duration_hours': round(duration_sec / 3600, 1),
                'duration_minutes': round(duration_sec / 60, 0),
                'quality_percent': s.get('sleepQualityPercentage', 0),
                'deep_sleep_hours': round(s.get('deepSleepSeconds', 0) / 3600, 1),
                'rem_sleep_hours': round(s.get('remSleepSeconds', 0) / 3600, 1),
                'light_sleep_hours': round(s.get('lightSleepSeconds', 0) / 3600, 1),
                'awake_minutes': round(s.get('awakeTimeSeconds', 0) / 60, 0),
            }
    except Exception as e:
        print(f"⚠️  Sleep data error for {date_str}: {e}")

    return {
        'date': date_str,
        'duration_hours': 0,
        'quality_percent': 0,
        'deep_sleep_hours': 0,
        'rem_sleep_hours': 0,
        'light_sleep_hours': 0,
        'awake_minutes': 0,
    }

def get_heart_rate(garth_client, date_str):
    """Get heart rate data"""
    try:
        gc = Garmin()
        gc.garth = garth_client
        hr_data = gc.get_heart_rate(date_str)

        if hr_data:
            return {
                'resting': hr_data.get('restingHeartRate', 0),
                'max': hr_data.get('maxHeartRate', 0),
                'avg': hr_data.get('averageHeartRate', 0),
            }
    except Exception as e:
        print(f"⚠️  Heart rate error for {date_str}: {e}")

    return {'resting': 0, 'max': 0, 'avg': 0}

def get_workouts(garth_client, days=30):
    """Get recent workouts from the last N days"""
    workouts = []

    try:
        gc = Garmin()
        gc.garth = garth_client

        # Get activities from last 30 days
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        activities = gc.get_activities(start_date, datetime.now().strftime("%Y-%m-%d"))

        for activity in activities:
            workout = {
                'date': activity.get('startTimeLocal', ''),
                'type': activity.get('activityType', {}).get('typeKey', 'Unknown'),
                'name': activity.get('activityName', 'Unnamed'),
                'distance_km': round(activity.get('distance', 0) / 1000, 2),
                'duration_minutes': round(activity.get('duration', 0) / 60, 0),
                'calories': activity.get('calories', 0),
                'heart_rate_avg': activity.get('avgHeartRate', 0),
                'heart_rate_max': activity.get('maxHeartRate', 0),
            }
            workouts.append(workout)

    except Exception as e:
        print(f"⚠️  Workouts error: {e}")

    return workouts

def sync_30_days():
    """Sync 30 days of Garmin health data"""
    garth_client = load_garth_session()
    if not garth_client:
        return None

    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)

    print(f"📊 Fetching 30 days of health data ({thirty_days_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')})...")

    daily_data = []
    current = thirty_days_ago

    while current <= today:
        date_str = current.strftime("%Y-%m-%d")
        print(f"  Fetching {date_str}...", end="", flush=True)

        summary = get_daily_summary(garth_client, date_str)
        sleep = get_sleep_data(garth_client, date_str)
        hr = get_heart_rate(garth_client, date_str)

        day_data = {
            'date': date_str,
            'summary': summary or {},
            'sleep': sleep,
            'heart_rate': hr,
        }
        daily_data.append(day_data)

        print(" ✓")
        current += timedelta(days=1)

    # Get workouts (last 30 days)
    print("\n🏃 Fetching workouts...")
    workouts = get_workouts(garth_client, 30)

    # Compile all data
    all_data = {
        'timestamp': datetime.now().isoformat(),
        'period': {
            'start': thirty_days_ago.strftime("%Y-%m-%d"),
            'end': today.strftime("%Y-%m-%d"),
            'days': 30,
        },
        'daily': daily_data,
        'workouts': workouts,
        'summary_stats': calculate_summary_stats(daily_data, workouts),
    }

    return all_data

def calculate_summary_stats(daily_data, workouts):
    """Calculate aggregated statistics for the 30-day period"""
    total_steps = sum(d.get('summary', {}).get('steps', 0) for d in daily_data if d.get('summary'))
    avg_steps = total_steps / len(daily_data) if daily_data else 0

    total_calories = sum(d.get('summary', {}).get('calories', 0) for d in daily_data if d.get('summary'))
    total_active_minutes = sum(d.get('summary', {}).get('active_minutes', 0) for d in daily_data if d.get('summary'))

    avg_sleep = sum(d.get('sleep', {}).get('duration_hours', 0) for d in daily_data) / len(daily_data) if daily_data else 0
    avg_sleep_quality = sum(d.get('sleep', {}).get('quality_percent', 0) for d in daily_data) / len(daily_data) if daily_data else 0

    total_workouts = len(workouts)
    total_workout_minutes = sum(w.get('duration_minutes', 0) for w in workouts)
    total_workout_calories = sum(w.get('calories', 0) for w in workouts)

    return {
        'total_steps': total_steps,
        'avg_daily_steps': round(avg_steps, 0),
        'total_calories': total_calories,
        'total_active_minutes': total_active_minutes,
        'avg_sleep_hours': round(avg_sleep, 1),
        'avg_sleep_quality': round(avg_sleep_quality, 1),
        'total_workouts': total_workouts,
        'total_workout_minutes': round(total_workout_minutes, 0),
        'total_workout_calories': total_workout_calories,
    }

def generate_dashboard_html(data, output_path):
    """Generate an interactive HTML health dashboard"""

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Garmin Health Dashboard - Last 30 Days</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .metric-card { transition: transform 0.2s; }
        .metric-card:hover { transform: translateY(-4px); }
    </style>
</head>
<body class="bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 min-h-screen text-white p-6">

    <div class="max-w-7xl mx-auto">

        <!-- Header -->
        <div class="text-center mb-8">
            <h1 class="text-4xl font-bold mb-2">🏃 Garmin Health Dashboard</h1>
            <p class="text-blue-300">30-Day Summary | {start} → {end}</p>
            <p class="text-sm text-gray-400 mt-2">Generated: {timestamp}</p>
        </div>

        <!-- Key Metrics -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">

            <div class="metric-card bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl shadow-lg">
                <div class="text-blue-200 text-sm">Total Steps</div>
                <div class="text-3xl font-bold">{total_steps:,}</div>
                <div class="text-blue-200 text-sm">Daily avg: {avg_steps:,}</div>
            </div>

            <div class="metric-card bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl shadow-lg">
                <div class="text-green-200 text-sm">Total Calories</div>
                <div class="text-3xl font-bold">{total_calories:,}</div>
                <div class="text-green-200 text-sm">Active: {active_minutes} min</div>
            </div>

            <div class="metric-card bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl shadow-lg">
                <div class="text-purple-200 text-sm">Avg Sleep</div>
                <div class="text-3xl font-bold">{avg_sleep}h</div>
                <div class="text-purple-200 text-sm">Quality: {avg_quality}%</div>
            </div>

            <div class="metric-card bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl shadow-lg">
                <div class="text-orange-200 text-sm">Workouts</div>
                <div class="text-3xl font-bold">{total_workouts}</div>
                <div class="text-orange-200 text-sm">{total_workout_minutes} min • {workout_calories} cal</div>
            </div>

        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">

            <!-- Steps Chart -->
            <div class="bg-slate-800/50 backdrop-blur p-6 rounded-xl border border-slate-700">
                <h2 class="text-xl font-bold mb-4">📈 Daily Steps</h2>
                <canvas id="stepsChart" height="200"></canvas>
            </div>

            <!-- Sleep Chart -->
            <div class="bg-slate-800/50 backdrop-blur p-6 rounded-xl border border-slate-700">
                <h2 class="text-xl font-bold mb-4">😴 Sleep Duration</h2>
                <canvas id="sleepChart" height="200"></canvas>
            </div>

        </div>

        <!-- Second Row Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">

            <!-- Heart Rate -->
            <div class="bg-slate-800/50 backdrop-blur p-6 rounded-xl border border-slate-700">
                <h2 class="text-xl font-bold mb-4">❤️ Resting Heart Rate</h2>
                <canvas id="hrChart" height="200"></canvas>
            </div>

            <!-- Activity Types -->
            <div class="bg-slate-800/50 backdrop-blur p-6 rounded-xl border border-slate-700">
                <h2 class="text-xl font-bold mb-4">🏋️ Workout Distribution</h2>
                <canvas id="workoutChart" height="200"></canvas>
            </div>

        </div>

        <!-- Workout List -->
        <div class="bg-slate-800/50 backdrop-blur p-6 rounded-xl border border-slate-700 mb-8">
            <h2 class="text-xl font-bold mb-4">📋 Recent Workouts (Last 30 Days)</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left">
                    <thead class="border-b border-slate-600">
                        <tr>
                            <th class="py-3 px-4">Date</th>
                            <th class="py-3 px-4">Type</th>
                            <th class="py-3 px-4">Name</th>
                            <th class="py-3 px-4">Duration</th>
                            <th class="py-3 px-4">Distance</th>
                            <th class="py-3 px-4">Calories</th>
                            <th class="py-3 px-4">HR Avg/Max</th>
                        </tr>
                    </thead>
                    <tbody>
                        {workout_rows}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Raw Data Section -->
        <details class="bg-slate-800/30 rounded-xl border border-slate-700 mb-8">
            <summary class="p-4 cursor-pointer hover:bg-slate-800/50">📦 Raw JSON Data (Click to expand)</summary>
            <pre class="p-4 text-xs overflow-x-auto text-gray-300">{json_data}</pre>
        </details>

    </div>

    <script>
        // Chart.js configurations
        const dates = {dates};
        const stepsData = {steps_data};
        const sleepData = {sleep_data};
        const hrData = {hr_data};
        const workoutTypes = {workout_types};
        const workoutCounts = {workout_counts};

        // Steps Chart
        new Chart(document.getElementById('stepsChart'), {{
            type: 'bar',
            data: {{
                labels: dates,
                datasets: [{{
                    label: 'Steps',
                    data: stepsData,
                    backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ beginAtZero: true, grid: {{ color: 'rgba(255,255,255,0.1)' }} }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});

        // Sleep Chart
        new Chart(document.getElementById('sleepChart'), {{
            type: 'line',
            data: {{
                labels: dates,
                datasets: [{{
                    label: 'Sleep (hours)',
                    data: sleepData,
                    borderColor: 'rgba(168, 85, 247, 1)',
                    backgroundColor: 'rgba(168, 85, 247, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ beginAtZero: true, grid: {{ color: 'rgba(255,255,255,0.1)' }} }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});

        // Heart Rate Chart
        new Chart(document.getElementById('hrChart'), {{
            type: 'line',
            data: {{
                labels: dates,
                datasets: [{{
                    label: 'Resting HR',
                    data: hrData,
                    borderColor: 'rgba(239, 68, 68, 1)',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ beginAtZero: false, grid: {{ color: 'rgba(255,255,255,0.1)' }} }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});

        // Workout Types Chart
        new Chart(document.getElementById('workoutChart'), {{
            type: 'doughnut',
            data: {{
                labels: workoutTypes,
                datasets: [{{
                    data: workoutCounts,
                    backgroundColor: [
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(168, 85, 247, 0.8)',
                        'rgba(236, 72, 153, 0.8)',
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'bottom' }}
                }}
            }}
        }});
    </script>

</body>
</html>"""

    # Prepare data for template
    dates = [d['date'] for d in data['daily']]
    steps_data = [d.get('summary', {}).get('steps', 0) for d in data['daily']]
    sleep_data = [d.get('sleep', {}).get('duration_hours', 0) for d in data['daily']]
    hr_data = [d.get('heart_rate', {}).get('resting', 0) for d in data['daily']]

    # Workout types distribution
    workout_type_counts = {}
    for w in workouts:
        t = w.get('type', 'Unknown')
        workout_type_counts[t] = workout_type_counts.get(t, 0) + 1

    workout_types = list(workout_type_counts.keys())
    workout_counts = list(workout_type_counts.values())

    # Format workout rows
    workout_rows = ""
    for w in sorted(workouts, key=lambda x: x.get('date', ''), reverse=True)[:30]:
        hr_avg = w.get('heart_rate_avg', 0)
        hr_max = w.get('heart_rate_max', 0)
        workout_rows += f"""
        <tr class="border-b border-slate-700 hover:bg-slate-700/30">
            <td class="py-3 px-4">{w.get('date', 'N/A')[:10]}</td>
            <td class="py-3 px-4 capitalize">{w.get('type', 'Unknown')}</td>
            <td class="py-3 px-4">{w.get('name', 'Unnamed')}</td>
            <td class="py-3 px-4">{w.get('duration_minutes', 0)} min</td>
            <td class="py-3 px-4">{w.get('distance_km', 0)} km</td>
            <td class="py-3 px-4">{w.get('calories', 0)} cal</td>
            <td class="py-3 px-4">{hr_avg}/{hr_max} bpm</td>
        </tr>"""

    # Render template
    html = html_template.format(
        start=data['period']['start'],
        end=data['period']['end'],
        timestamp=data['timestamp'],
        total_steps=data['summary_stats']['total_steps'],
        avg_steps=int(data['summary_stats']['avg_daily_steps']),
        total_calories=data['summary_stats']['total_calories'],
        active_minutes=data['summary_stats']['total_active_minutes'],
        avg_sleep=data['summary_stats']['avg_sleep_hours'],
        avg_quality=data['summary_stats']['avg_sleep_quality'],
        total_workouts=data['summary_stats']['total_workouts'],
        total_workout_minutes=data['summary_stats']['total_workout_minutes'],
        workout_calories=data['summary_stats']['total_workout_calories'],
        dates=json.dumps(dates),
        steps_data=json.dumps(steps_data),
        sleep_data=json.dumps(sleep_data),
        hr_data=json.dumps(hr_data),
        workout_types=json.dumps(workout_types),
        workout_counts=json.dumps(workout_counts),
        workout_rows=workout_rows,
        json_data=json.dumps(data, indent=2)
    )

    # Write HTML file
    with open(output_path, 'w') as f:
        f.write(html)

    print(f"✅ Dashboard generated: {output_path}")

if __name__ == "__main__":
    print("🚀 Starting 30-Day Garmin Health Sync")
    print("=" * 60)

    # Check dependencies first
    try:
        import garth
        import garminconnect
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\nInstall with: pip install garth garminconnect")
        sys.exit(1)

    # Sync data
    data = sync_30_days()
    if not data:
        print("❌ Failed to sync data")
        sys.exit(1)

    print("\n✅ 30-day sync complete!")
    print(f"   📊 Days fetched: {len(data['daily'])}")
    print(f"   🏃 Workouts: {len(data['workouts'])}")
    print(f"   📈 Total steps: {data['summary_stats']['total_steps']:,}")

    # Save raw data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    data_file = f"/tmp/garmin_30days_{timestamp}.json"
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"   💾 Raw data saved: {data_file}")

    # Generate dashboard
    dashboard_file = f"/tmp/garmin_dashboard_{timestamp}.html"
    generate_dashboard_html(data, dashboard_file)
    print(f"   📊 Dashboard generated: {dashboard_file}")

    # Also save latest reference
    latest_json = "/tmp/garmin_latest.json"
    latest_html = "/tmp/garmin_latest.html"
    with open(latest_json, 'w') as f:
        json.dump(data, f, indent=2)
    with open(latest_html, 'w') as f:
        with open(dashboard_file, 'r') as src:
            f.write(src.read())

    print(f"   🔗 Latest links updated: {latest_json}, {latest_html}")

    print("\n✅ All tasks completed successfully!")

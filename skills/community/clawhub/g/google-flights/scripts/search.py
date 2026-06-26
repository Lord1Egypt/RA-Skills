#!/usr/bin/env python3
"""
Flight search CLI using fast-flights (Google Flights scraper).
Features: flexible dates, filters, connection scoring, user preferences.
"""

import argparse
import json
import sys
import warnings
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

# Suppress date parsing warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Add venv to path
script_dir = os.path.dirname(os.path.abspath(__file__))
venv_site = os.path.join(script_dir, '..', '.venv', 'lib')
if os.path.exists(venv_site):
    for d in os.listdir(venv_site):
        if d.startswith('python'):
            sys.path.insert(0, os.path.join(venv_site, d, 'site-packages'))
            break

from fast_flights import FlightData, Passengers, get_flights

# Airport connection quality ratings (1-5, higher is better)
AIRPORT_QUALITY = {
    # Major hubs - generally good
    "LAX": 3, "JFK": 3, "ORD": 2, "DFW": 4, "DEN": 4, "ATL": 4,
    "SFO": 4, "SEA": 4, "BOS": 3, "MIA": 3, "PHX": 4, "LAS": 4,
    # Canadian
    "YYZ": 3, "YVR": 4, "YYC": 4, "YUL": 3, "YOW": 4,
    # International
    "LHR": 3, "CDG": 2, "FRA": 4, "AMS": 4, "HND": 5, "NRT": 4,
    # Problematic for connections
    "EWR": 2, "LGA": 2, "MDW": 2,
}

# Risky winter connection airports
WINTER_RISK_AIRPORTS = {"ORD", "EWR", "JFK", "BOS", "DEN", "MSP", "DTW"}


def load_preferences() -> Dict[str, Any]:
    """Load user preferences from TOOLS.md or config."""
    prefs = {
        "preferred_airlines": [],
        "avoid_airlines": [],
        "prefer_nonstop": False,
        "max_layover_hours": 4,
        "min_layover_minutes": 45,
    }
    
    # Try to load from config file
    config_path = os.path.expanduser("~/clawd/skills/google-flights/config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                user_prefs = json.load(f)
                prefs.update(user_prefs)
        except:
            pass
    
    return prefs


def parse_date(date_str: str) -> str:
    """Parse flexible date input to YYYY-MM-DD format."""
    date_str = date_str.lower().strip()
    today = datetime.now()
    
    if date_str == "today":
        return today.strftime("%Y-%m-%d")
    elif date_str == "tomorrow":
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif date_str.startswith("in ") and "day" in date_str:
        days = int(''.join(filter(str.isdigit, date_str)))
        return (today + timedelta(days=days)).strftime("%Y-%m-%d")
    elif date_str.startswith("next "):
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for i, day in enumerate(weekdays):
            if day in date_str:
                days_ahead = i - today.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        if "week" in date_str:
            return (today + timedelta(days=7)).strftime("%Y-%m-%d")
    
    # Try to parse with year first
    if len(date_str) >= 8 and date_str[4] == '-':
        return date_str
    
    for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%B %d, %Y", "%b %d, %Y", "%B %d %Y", "%b %d %Y"]:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    for fmt in ["%m/%d", "%d %b", "%b %d", "%B %d"]:
        try:
            parsed = datetime.strptime(date_str, fmt)
            parsed = parsed.replace(year=today.year)
            if parsed.date() < today.date():
                parsed = parsed.replace(year=today.year + 1)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    return date_str


def parse_time(time_str: str) -> Optional[int]:
    """Parse time string to minutes from midnight."""
    if not time_str:
        return None
    time_str = time_str.lower().strip()
    
    # Handle 24h format
    if ":" in time_str:
        parts = time_str.replace("am", "").replace("pm", "").strip().split(":")
        hour = int(parts[0])
        minute = int(parts[1]) if len(parts) > 1 else 0
        if "pm" in time_str.lower() and hour < 12:
            hour += 12
        elif "am" in time_str.lower() and hour == 12:
            hour = 0
        return hour * 60 + minute
    
    # Handle simple hour
    hour = int(''.join(filter(str.isdigit, time_str)))
    if "pm" in time_str and hour < 12:
        hour += 12
    elif "am" in time_str and hour == 12:
        hour = 0
    return hour * 60


def generate_flex_dates(base_date: str, flex_days: int) -> List[str]:
    """Generate list of dates around base date."""
    base = datetime.strptime(base_date, "%Y-%m-%d")
    dates = []
    for delta in range(-flex_days, flex_days + 1):
        d = base + timedelta(days=delta)
        if d.date() >= datetime.now().date():
            dates.append(d.strftime("%Y-%m-%d"))
    return dates


def build_google_flights_url(from_apt: str, to_apt: str, dep_date: str, ret_date: str = None) -> str:
    """Build a direct Google Flights search URL."""
    if ret_date:
        return f"https://www.google.com/travel/flights?q=Flights%20from%20{from_apt}%20to%20{to_apt}%20on%20{dep_date}%20returning%20{ret_date}&hl=en"
    else:
        return f"https://www.google.com/travel/flights?q=Flights%20from%20{from_apt}%20to%20{to_apt}%20on%20{dep_date}%20one%20way&hl=en"


def parse_flight_time(time_str: str) -> Optional[int]:
    """Parse flight time like '6:25 AM' to minutes from midnight."""
    if not time_str:
        return None
    try:
        # Handle various formats
        time_str = time_str.strip().upper()
        if "AM" in time_str or "PM" in time_str:
            is_pm = "PM" in time_str
            time_str = time_str.replace("AM", "").replace("PM", "").strip()
            parts = time_str.split(":")
            hour = int(parts[0])
            minute = int(parts[1]) if len(parts) > 1 else 0
            if is_pm and hour < 12:
                hour += 12
            elif not is_pm and hour == 12:
                hour = 0
            return hour * 60 + minute
    except:
        pass
    return None


def parse_duration(duration_str: str) -> Optional[int]:
    """Parse duration like '6h 23m' or '6 hr 23 min' to minutes."""
    if not duration_str:
        return None
    try:
        hours = 0
        minutes = 0
        duration_str = duration_str.lower()
        
        # Extract hours
        if "h" in duration_str:
            h_part = duration_str.split("h")[0].strip().split()[-1]
            hours = int(h_part)
        
        # Extract minutes
        if "m" in duration_str:
            m_part = duration_str.split("h")[-1] if "h" in duration_str else duration_str
            m_part = ''.join(filter(str.isdigit, m_part.split("m")[0]))
            if m_part:
                minutes = int(m_part)
        
        return hours * 60 + minutes
    except:
        return None


def score_connection(flight, prefs: Dict[str, Any], is_winter: bool = False) -> Dict[str, Any]:
    """
    Score a flight connection based on multiple factors.
    Returns dict with score (0-100) and breakdown.
    """
    score = 100
    factors = []
    
    # Check if flight has stops info
    stops = getattr(flight, 'stops', 0)
    if isinstance(stops, str):
        stops = 0 if 'nonstop' in stops.lower() else int(''.join(filter(str.isdigit, stops)) or 1)
    
    # Nonstop bonus
    if stops == 0:
        score += 15
        factors.append(("Nonstop", "+15"))
    else:
        # Layover penalties
        layover_info = getattr(flight, 'layover', None)
        if layover_info:
            # Parse layover duration
            layover_mins = parse_duration(str(layover_info))
            if layover_mins:
                if layover_mins < prefs.get('min_layover_minutes', 45):
                    score -= 30
                    factors.append(("Tight connection", "-30"))
                elif layover_mins > prefs.get('max_layover_hours', 4) * 60:
                    penalty = min(25, (layover_mins - prefs['max_layover_hours'] * 60) // 30 * 5)
                    score -= penalty
                    factors.append((f"Long layover ({layover_mins}min)", f"-{penalty}"))
        
        # Connection airport quality
        # Try to extract connection airport from flight info
        flight_str = str(flight)
        for airport in AIRPORT_QUALITY:
            if airport in flight_str and airport not in [getattr(flight, 'from_airport', ''), getattr(flight, 'to_airport', '')]:
                quality = AIRPORT_QUALITY.get(airport, 3)
                if quality < 3:
                    score -= (3 - quality) * 10
                    factors.append((f"Connection at {airport}", f"-{(3-quality)*10}"))
                
                # Winter risk
                if is_winter and airport in WINTER_RISK_AIRPORTS:
                    score -= 15
                    factors.append((f"Winter risk at {airport}", "-15"))
                break
    
    # Red-eye penalty
    dep_time = getattr(flight, 'departure', None)
    if dep_time:
        dep_mins = parse_flight_time(str(dep_time))
        if dep_mins is not None:
            if dep_mins < 360:  # Before 6am
                score -= 10
                factors.append(("Early departure", "-10"))
            elif dep_mins >= 1320:  # After 10pm
                score -= 15
                factors.append(("Red-eye", "-15"))
    
    # Airline preferences
    airline = getattr(flight, 'airline', '') or ''
    airline_name = str(airline).lower()
    
    for pref in prefs.get('preferred_airlines', []):
        if pref.lower() in airline_name:
            score += 10
            factors.append((f"Preferred: {pref}", "+10"))
            break
    
    for avoid in prefs.get('avoid_airlines', []):
        if avoid.lower() in airline_name:
            score -= 25
            factors.append((f"Avoid: {avoid}", "-25"))
            break
    
    return {
        "score": max(0, min(100, score)),
        "factors": factors
    }


def extract_flights_with_details(flights, prefs: Dict[str, Any]) -> List[Dict]:
    """Extract flight details with scoring."""
    is_winter = datetime.now().month in [11, 12, 1, 2, 3]
    results = []
    
    for f in flights:
        price_str = getattr(f, 'price', None)
        if not price_str:
            continue
        
        # Parse price to numeric
        numeric_price = int(''.join(filter(str.isdigit, str(price_str))) or 0)
        
        # Get connection score
        conn_score = score_connection(f, prefs, is_winter)
        
        flight_info = {
            "airline": getattr(f, 'name', None) or getattr(f, 'airline', 'Unknown'),
            "price": price_str,
            "price_numeric": numeric_price,
            "departure": getattr(f, 'departure', None),
            "arrival": getattr(f, 'arrival', None),
            "duration": getattr(f, 'duration', None),
            "stops": getattr(f, 'stops', None),
            "is_best": getattr(f, 'is_best', False),
            "connection_score": conn_score["score"],
            "score_factors": conn_score["factors"],
        }
        results.append(flight_info)
    
    return results


def filter_flights(flights: List[Dict], args) -> List[Dict]:
    """Apply user filters to flight list."""
    filtered = []
    
    for f in flights:
        # Nonstop filter
        if args.nonstop:
            stops = f.get('stops', '')
            if stops and 'nonstop' not in str(stops).lower():
                if '0' not in str(stops):
                    continue
        
        # Max price filter
        if args.max_price:
            if f['price_numeric'] > args.max_price:
                continue
        
        # Departure time filter
        if args.depart_after:
            dep_mins = parse_flight_time(str(f.get('departure', '')))
            after_mins = parse_time(args.depart_after)
            if dep_mins is not None and after_mins is not None:
                if dep_mins < after_mins:
                    continue
        
        # Arrival time filter
        if args.arrive_before:
            arr_mins = parse_flight_time(str(f.get('arrival', '')))
            before_mins = parse_time(args.arrive_before)
            if arr_mins is not None and before_mins is not None:
                if arr_mins > before_mins:
                    continue
        
        filtered.append(f)
    
    return filtered


def search_flights(from_apt: str, to_apt: str, dep_date: str, ret_date: str = None,
                   seat: str = "economy", adults: int = 1, children: int = 0) -> Any:
    """Execute flight search."""
    import io
    from contextlib import redirect_stderr
    
    flight_data = [
        FlightData(
            date=dep_date,
            from_airport=from_apt,
            to_airport=to_apt
        )
    ]
    
    trip = "one-way"
    if ret_date:
        trip = "round-trip"
        flight_data.append(
            FlightData(
                date=ret_date,
                from_airport=to_apt,
                to_airport=from_apt
            )
        )
    
    with redirect_stderr(io.StringIO()):
        result = get_flights(
            flight_data=flight_data,
            trip=trip,
            seat=seat,
            passengers=Passengers(
                adults=adults,
                children=children,
                infants_in_seat=0,
                infants_on_lap=0
            ),
            fetch_mode="fallback"
        )
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Search Google Flights with smart features")
    parser.add_argument("from_airport", help="Departure airport code (e.g., LAX, YYC)")
    parser.add_argument("to_airport", help="Arrival airport code (e.g., JFK, LHR)")
    parser.add_argument("date", help="Departure date (YYYY-MM-DD, 'tomorrow', 'next monday', etc.)")
    parser.add_argument("--return", "-r", dest="return_date", help="Return date for round-trip")
    parser.add_argument("--adults", "-a", type=int, default=1, help="Number of adults")
    parser.add_argument("--children", "-c", type=int, default=0, help="Number of children")
    parser.add_argument("--seat", "-s", choices=["economy", "premium-economy", "business", "first"], 
                        default="economy", help="Seat class")
    
    # New filters
    parser.add_argument("--flex", "-f", type=int, default=0, 
                        help="Flexible dates: search ±N days around date")
    parser.add_argument("--nonstop", "-n", action="store_true", help="Nonstop flights only")
    parser.add_argument("--max-price", "-m", type=int, help="Maximum price filter")
    parser.add_argument("--depart-after", help="Depart after time (e.g., 8am, 14:00)")
    parser.add_argument("--arrive-before", help="Arrive before time (e.g., 6pm, 18:00)")
    parser.add_argument("--sort", choices=["price", "score", "duration"], default="price",
                        help="Sort results by (default: price)")
    
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--top", "-t", type=int, default=5, help="Show top N results")
    parser.add_argument("--show-scores", action="store_true", help="Show connection quality scores")
    
    args = parser.parse_args()
    
    prefs = load_preferences()
    dep_date = parse_date(args.date)
    ret_date = parse_date(args.return_date) if args.return_date else None
    
    # Handle flexible dates
    if args.flex > 0:
        search_dates = generate_flex_dates(dep_date, args.flex)
    else:
        search_dates = [dep_date]
    
    all_results = []
    
    for search_date in search_dates:
        try:
            result = search_flights(
                args.from_airport.upper(),
                args.to_airport.upper(),
                search_date,
                ret_date,
                args.seat,
                args.adults,
                args.children
            )
            
            flights = extract_flights_with_details(result.flights, prefs)
            flights = filter_flights(flights, args)
            
            for f in flights:
                f['date'] = search_date
                f['price_trend'] = result.current_price
            
            all_results.extend(flights)
            
        except Exception as e:
            if not args.json:
                print(f"⚠️  Error searching {search_date}: {e}", file=sys.stderr)
    
    if not all_results:
        if args.json:
            print(json.dumps({"error": "No flights found", "filters": vars(args)}))
        else:
            print("❌ No flights found matching your criteria")
        sys.exit(1)
    
    # Sort results
    if args.sort == "price":
        all_results.sort(key=lambda x: x['price_numeric'])
    elif args.sort == "score":
        all_results.sort(key=lambda x: -x['connection_score'])
    elif args.sort == "duration":
        all_results.sort(key=lambda x: parse_duration(str(x.get('duration', ''))) or 9999)
    
    # Deduplicate by price+airline+time
    seen = set()
    unique_results = []
    for f in all_results:
        key = (f['price'], f['airline'], f.get('departure'), f.get('date'))
        if key not in seen:
            seen.add(key)
            unique_results.append(f)
    
    top_results = unique_results[:args.top]
    
    google_url = build_google_flights_url(
        args.from_airport.upper(),
        args.to_airport.upper(),
        dep_date,
        ret_date
    )
    
    if args.json:
        output = {
            "query": {
                "from": args.from_airport.upper(),
                "to": args.to_airport.upper(),
                "date": dep_date,
                "return_date": ret_date,
                "flex_days": args.flex,
                "seat": args.seat,
                "passengers": {"adults": args.adults, "children": args.children},
                "filters": {
                    "nonstop": args.nonstop,
                    "max_price": args.max_price,
                    "depart_after": args.depart_after,
                    "arrive_before": args.arrive_before,
                }
            },
            "results_count": len(unique_results),
            "flights": top_results,
            "google_flights_url": google_url
        }
        print(json.dumps(output, indent=2, default=str))
    else:
        print(f"✈️  {args.from_airport.upper()} → {args.to_airport.upper()}")
        
        if args.flex > 0:
            print(f"📅 {dep_date} (±{args.flex} days)" + (f" ↔ {ret_date}" if ret_date else " (one-way)"))
        else:
            print(f"📅 {dep_date}" + (f" ↔ {ret_date}" if ret_date else " (one-way)"))
        
        print(f"👥 {args.adults} adult(s)" + (f", {args.children} child(ren)" if args.children else ""))
        print(f"💺 {args.seat.replace('-', ' ').title()}")
        
        filters_applied = []
        if args.nonstop:
            filters_applied.append("nonstop only")
        if args.max_price:
            filters_applied.append(f"max ${args.max_price}")
        if args.depart_after:
            filters_applied.append(f"depart after {args.depart_after}")
        if args.arrive_before:
            filters_applied.append(f"arrive before {args.arrive_before}")
        
        if filters_applied:
            print(f"🔍 Filters: {', '.join(filters_applied)}")
        
        print()
        print(f"🔢 {len(unique_results)} options found (showing top {len(top_results)})")
        print()
        
        for i, f in enumerate(top_results, 1):
            stops_str = str(f.get('stops', '?'))
            if 'nonstop' in stops_str.lower():
                stops_str = "Nonstop ⭐"
            
            date_str = f" [{f['date']}]" if args.flex > 0 else ""
            best_marker = " 🏆" if f.get('is_best') else ""
            
            print(f"{i}. {f['airline']} | {f.get('departure', '?')} → {f.get('arrival', '?')} | {f.get('duration', '?')} | {stops_str} | {f['price']}{best_marker}{date_str}")
            
            if args.show_scores and f.get('score_factors'):
                score = f['connection_score']
                factors_str = ", ".join([f"{name}({val})" for name, val in f['score_factors']])
                print(f"   📊 Score: {score}/100 — {factors_str}")
        
        print()
        print(f"🔗 {google_url}")


if __name__ == "__main__":
    main()

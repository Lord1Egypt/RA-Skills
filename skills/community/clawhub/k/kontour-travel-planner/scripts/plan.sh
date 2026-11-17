#!/usr/bin/env bash
# Kontour Travel Planner — Quick Planning Script
# Usage: ./plan.sh "your trip description"
# Outputs structured trip context JSON by extracting dimensions from natural language.
# No API keys or external services required — runs entirely offline.

set -euo pipefail

QUERY="${1:-}"
if [ -z "$QUERY" ]; then
  echo "Usage: $0 \"<trip description>\""
  echo "Example: $0 \"2 weeks in Japan for a couple, mid-range budget, food and temples\""
  exit 1
fi

# Validate input boundary: capped length + strict character allowlist
if [ "${#QUERY}" -gt 280 ]; then
  echo "Error: Query too long (max 280 chars)." >&2
  exit 1
fi
if ! echo "$QUERY" | grep -qE '^[a-zA-Z0-9 ,.\-\/\$€£¥()!?'\''&]+$'; then
  echo "Error: Query contains unsupported characters." >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DEST_FILE="$SKILL_DIR/references/destinations.json"

# All processing done in Python with proper argument passing (no shell interpolation)
python3 - "$QUERY" "$DEST_FILE" << 'PYEOF'
import json, sys, re, os

query = sys.argv[1]
dest_file = sys.argv[2]

def extract_destination(text):
    m = re.search(r'\b(?:in|to|visit|visiting|explore|exploring)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', text)
    if m:
        dest = re.sub(r'\s+[Ff]or$', '', m.group(1))
        return dest
    return ""

def extract_duration(text):
    m = re.search(r'(\d+)\s*(days?|weeks?|nights?)', text, re.IGNORECASE)
    if m:
        num = int(m.group(1))
        if 'week' in m.group(2).lower():
            return num * 7
        return num
    return None

def extract_travelers(text):
    t = text.lower()
    if 'solo' in t: return 1
    if 'couple' in t: return 2
    if 'family' in t: return 4
    m = re.search(r'(\d+)\s*(?:people|travelers|adults|persons)', t)
    if m: return int(m.group(1))
    return None

def extract_budget(text):
    t = text.lower()
    budget = {}
    if re.search(r'mid.range|moderate|comfort', t):
        budget['tier'] = "mid"
    elif re.search(r'budget|cheap|backpack', t):
        budget['tier'] = "budget"
    elif re.search(r'luxury|premium|high.end|splurge', t):
        budget['tier'] = "luxury"

    money_patterns = [
        (r'(?:under|below|less than|max(?:imum)?|cap(?:ped)? at|budget cap|up to)\s*(?:usd\s*)?([\$€£¥])?\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s*(usd|eur|gbp|jpy)?', 'cap'),
        (r'(?:budget of|total budget|spend)\s*(?:usd\s*)?([\$€£¥])?\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s*(usd|eur|gbp|jpy)?', 'target'),
        (r'([\$€£¥])\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s*(usd|eur|gbp|jpy)?\s*(?:budget|cap|max)?', 'target'),
    ]
    currency_by_symbol = {'$': 'USD', '€': 'EUR', '£': 'GBP', '¥': 'JPY'}
    for pattern, scope in money_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            symbol = m.group(1)
            amount = float(m.group(2).replace(',', ''))
            code = (m.group(3) or currency_by_symbol.get(symbol) or 'USD').upper()
            if amount.is_integer():
                amount = int(amount)
            budget['cap'] = {'amount': amount, 'currency': code, 'scope': scope}
            break
    return budget

def extract_constraints(text):
    t = text.lower()
    details = {}
    summary = []

    if re.search(r'\b(relaxed|slow|easy|leisurely)\b.*\bpace\b|\b(relaxed|slow|easy|leisurely)\s+(?:trip|itinerary)', t):
        details['trip_pace'] = 'relaxed'
        summary.append('relaxed pace')
    elif re.search(r'\b(packed|busy|ambitious|fast[- ]paced|see as much|full days?)\b', t):
        details['trip_pace'] = 'packed'
        summary.append('packed pace')
    elif re.search(r'\bmoderate\b.*\bpace\b', t):
        details['trip_pace'] = 'moderate'
        summary.append('moderate pace')

    neighborhood_patterns = [
        r'prefer(?:red)?\s+(?:the\s+)?([A-Za-z][A-Za-z0-9 .\-]{1,40}?)(?:\s+neighbou?rhood|\s+area|\s+district)(?:[,.;!?)]|$)',
        r'neighbou?rhood preference(?: is|:)?\s+([A-Za-z][A-Za-z0-9 .\-]{1,40}?)(?:[,.;!?)]|$)',
        r'(?:near|around|close to|stay(?:ing)? in|base(?:d)? in)\s+(?:the\s+)?([A-Za-z][A-Za-z0-9 .\-]+?)(?:[,.;!?)]|\s+(?:with|for|and|but|under|below|less|max|cap|budget|open|weather|rain|food|vegetarian|vegan|halal|kosher|pace)\b|$)',
    ]
    for pattern in neighborhood_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            value = m.group(1).strip(' .,-')
            if value and len(value.split()) <= 4:
                details['neighborhood_preference'] = value
                summary.append(f'prefer {value} neighborhood')
                break

    if re.search(r'opening hours|hours matter|open late|closed days?|avoid closed|must be open|check hours|museum hours', t):
        details['opening_hours_sensitivity'] = True
        summary.append('opening-hours sensitive')

    food_preferences = []
    food_patterns = [
        ('vegetarian', r'\bvegetarian\b'), ('vegan', r'\bvegan\b'),
        ('halal', r'\bhalal\b'), ('kosher', r'\bkosher\b'),
        ('gluten-free', r'gluten[- ]free'), ('no raw fish', r'no raw fish|avoid raw fish'),
        ('seafood', r'\bseafood\b'), ('street food', r'street food'),
        ('local food', r'local food|local cuisine|regional cuisine'),
    ]
    for label, pattern in food_patterns:
        if re.search(pattern, t) and label not in food_preferences:
            food_preferences.append(label)
    if food_preferences:
        details['food_preferences'] = food_preferences
        summary.extend(food_preferences)

    weather_flags = []
    if re.search(r'rain|rainy|wet weather|indoor backup|weather backup', t):
        weather_flags.append('rain backup')
    if re.search(r'avoid heat|not too hot|heat sensitive|cool weather', t):
        weather_flags.append('heat sensitive')
    if re.search(r'avoid cold|not too cold|cold sensitive|warm weather', t):
        weather_flags.append('cold sensitive')
    if re.search(r'weather sensitive|weather dependent', t) and not weather_flags:
        weather_flags.append('weather sensitive')
    if weather_flags:
        details['weather_sensitivity'] = weather_flags
        summary.extend(weather_flags)

    return details, summary

def extract_interests(text):
    keywords = ['food', 'culinary', 'temple', 'culture', 'history', 'museum', 'art',
                'beach', 'adventure', 'hiking', 'nature', 'nightlife', 'shopping',
                'wellness', 'spa', 'photography', 'architecture', 'wine']
    t = text.lower()
    return [kw for kw in keywords if kw in t]


def extract_travel_months(text):
    month_lookup = {
        'january': 1, 'jan': 1, 'february': 2, 'feb': 2, 'march': 3, 'mar': 3,
        'april': 4, 'apr': 4, 'may': 5, 'june': 6, 'jun': 6, 'july': 7, 'jul': 7,
        'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'sept': 9, 'october': 10, 'oct': 10,
        'november': 11, 'nov': 11, 'december': 12, 'dec': 12,
    }
    season_lookup = {
        'spring': [3, 4, 5],
        'summer': [6, 7, 8],
        'fall': [9, 10, 11],
        'autumn': [9, 10, 11],
        'winter': [12, 1, 2],
    }
    t = text.lower()
    months = []
    for label, number in month_lookup.items():
        if re.search(rf'\b{re.escape(label)}\b', t) and number not in months:
            months.append(number)
    for label, numbers in season_lookup.items():
        if re.search(rf'\b{label}\b', t):
            for number in numbers:
                if number not in months:
                    months.append(number)
    return months


def extract_compare_options(text):
    intro = re.search(r'\b(?:compare|between)\s+(.+)', text, re.IGNORECASE)
    if not intro:
        return []

    chunk = re.split(r'\s+(?:for|with|under|below|less|max|cap|budget|during|around|because|if)\b|[,.;!?)]', intro.group(1), maxsplit=1, flags=re.IGNORECASE)[0]
    parts = re.split(r'\s+(?:vs\.?|versus|or|and)\s+', chunk, flags=re.IGNORECASE)
    options = []
    for part in parts:
        name = part.strip(' .,-')
        if re.match(r'^[A-Za-z][A-Za-z .-]{1,40}$', name) and name.lower() not in {o.lower() for o in options}:
            options.append(name)
    return options[:3] if len(options) >= 2 else []


def build_scoring_explanations(dest_data, interests, budget, constraint_details):
    if not dest_data:
        return []

    highlights = dest_data.get('highlights', [])[:5]
    costs = dest_data.get('avg_daily_cost_usd', {})
    tier = budget.get('tier') if isinstance(budget, dict) else None
    daily = costs.get(tier) if tier else None
    cap = budget.get('cap') if isinstance(budget, dict) else None

    interest_terms = [i for i in interests if i]
    theme_aliases = {
        'food': ['market', 'food', 'tsukiji', 'culinary', 'restaurant', 'street'],
        'culinary': ['market', 'food', 'tsukiji', 'culinary', 'restaurant', 'street'],
        'temple': ['temple', 'shrine', 'senso', 'meiji', 'notre-dame', 'abbey'],
        'culture': ['temple', 'shrine', 'museum', 'gallery', 'palace', 'old town', 'historic', 'heritage'],
        'history': ['museum', 'tower', 'castle', 'old town', 'historic', 'heritage', 'palace'],
        'museum': ['museum', 'gallery', 'louvre', "d'orsay", 'british museum'],
        'art': ['museum', 'gallery', 'louvre', "d'orsay"],
        'architecture': ['tower', 'palace', 'temple', 'shrine', 'cathedral', 'abbey'],
        'shopping': ['market', 'shopping', 'camden', 'bazaar'],
        'nightlife': ['night', 'bar', 'club', 'shibuya'],
        'nature': ['park', 'garden', 'mountain', 'beach'],
        'photography': ['crossing', 'tower', 'view', 'old town', 'palace'],
    }

    suggestions = []
    for idx, place in enumerate(highlights, start=1):
        place_lower = place.lower()
        matched = []
        for interest in interest_terms:
            aliases = theme_aliases.get(interest, [interest])
            if any(alias in place_lower for alias in aliases):
                matched.append(interest)

        factors = [
            f"destination fit: {place} is a listed highlight for {dest_data.get('name', 'the destination')}"
        ]

        if matched:
            factors.append(f"thematic fit: matches requested {', '.join(matched[:2])} interest")
        elif interest_terms:
            factors.append(f"thematic fit: adds contrast to the requested {', '.join(interest_terms[:2])} theme")
        else:
            factors.append('thematic fit: strong general-interest anchor for a first-pass itinerary')

        if daily:
            factors.append(f"budget fit: {tier} benchmark is about ${daily} per person per day here")
        elif cap:
            currency = cap.get('currency', 'USD')
            amount = cap.get('amount')
            factors.append(f"budget fit: can be screened against the stated {currency} {amount} cap")
        elif costs:
            mid = costs.get('mid') or next(iter(costs.values()))
            factors.append(f"budget fit: destination benchmark starts from about ${mid} per person per day")

        if constraint_details.get('opening_hours_sensitivity'):
            factors.append('hours: keep only if live opening hours fit the final day plan')
        if constraint_details.get('weather_sensitivity'):
            factors.append('weather fit: mark as needing indoor/outdoor backup screening')

        suggestions.append({
            'name': place,
            'rank': idx,
            'why_chosen': factors[:3],
            'explanation': '; '.join(factors[:3])
        })

    return suggestions






def find_destination_record(name, dests):
    if not name:
        return None
    name_lower = name.lower()
    return next((d for d in dests if d['name'].lower() == name_lower or d['country'].lower() == name_lower), None)

def month_names(months):
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return [labels[m - 1] for m in months if isinstance(m, int) and 1 <= m <= 12]

def comparison_interest_matches(data, interests):
    if not data or not interests:
        return []
    highlight_text = ' '.join(data.get('highlights', [])).lower()
    aliases = {
        'food': ['food', 'market', 'culinary', 'restaurant', 'street food', 'tsukiji', 'bazaar'],
        'culinary': ['food', 'market', 'culinary', 'restaurant', 'street food', 'tsukiji', 'bazaar'],
        'culture': ['culture', 'temple', 'shrine', 'museum', 'gallery', 'palace', 'historic', 'heritage', 'old town'],
        'history': ['history', 'museum', 'palace', 'historic', 'heritage', 'old town', 'temple'],
        'museum': ['museum', 'gallery'],
        'art': ['art', 'museum', 'gallery'],
        'temple': ['temple', 'shrine'],
        'architecture': ['architecture', 'tower', 'palace', 'cathedral', 'temple', 'shrine'],
        'shopping': ['shopping', 'market', 'bazaar', 'camden'],
        'nightlife': ['nightlife', 'night', 'bar', 'club', 'shibuya'],
        'nature': ['nature', 'park', 'garden', 'mountain', 'beach'],
        'photography': ['photography', 'view', 'tower', 'crossing', 'old town'],
    }
    matches = []
    for interest in interests:
        terms = aliases.get(interest, [interest])
        if any(term in highlight_text for term in terms):
            matches.append(interest)
    return matches


def build_destination_comparison(compare_options, dests, budget, interests, constraint_details, travel_months):
    if len(compare_options) < 2:
        return None

    rows = []
    tier = budget.get('tier') if isinstance(budget, dict) else None
    for option in compare_options[:3]:
        data = find_destination_record(option, dests)
        if not data:
            rows.append({
                'name': option,
                'data_confidence': 'low',
                'fit_factors': ['not found in bundled destination reference', 'needs live validation before ranking'],
                'tradeoffs': ['cost, seasonality, and visa data unavailable offline'],
                'decision_signal': 'Treat as a research candidate rather than a ranked recommendation.',
            })
            continue

        costs = data.get('avg_daily_cost_usd', {})
        cost_value = costs.get(tier) if tier else costs.get('mid')
        best_month_numbers = data.get('best_months', [])
        seasons = month_names(best_month_numbers[:5])
        requested_seasons = month_names(travel_months)
        season_overlap = [m for m in travel_months if m in best_month_numbers]
        matched_interests = comparison_interest_matches(data, interests)

        fit_factors = [
            f"budget benchmark: about ${cost_value} per person/day" if cost_value else 'budget benchmark available for screening',
            f"best months: {', '.join(seasons)}" if seasons else 'seasonality data available in reference file',
        ]
        if travel_months:
            if season_overlap:
                fit_factors.append(f"season match: requested {', '.join(requested_seasons)} overlaps best months")
            else:
                fit_factors.append(f"season caution: requested {', '.join(requested_seasons)} is outside listed best months")
        if matched_interests:
            fit_factors.append(f"interest match: {', '.join(matched_interests[:2])}")
        elif interests:
            fit_factors.append(f"interest coverage: highlights need review against {', '.join(interests[:2])}")
        else:
            fit_factors.append(f"anchor highlights: {', '.join(data.get('highlights', [])[:2])}")

        tradeoffs = []
        budget_floor = costs.get('budget')
        if budget_floor and cost_value and cost_value > budget_floor * 2:
            tradeoffs.append('higher comfort/luxury spread may require tighter hotel choices')
        if travel_months and not season_overlap:
            tradeoffs.append('requested timing is outside the listed best-month window')
        if constraint_details.get('weather_sensitivity'):
            tradeoffs.append('weather-sensitive request needs month and indoor/outdoor screening')
        if constraint_details.get('trip_pace') == 'relaxed':
            tradeoffs.append('relaxed pace favors fewer bases and shorter daily transfers')
        elif constraint_details.get('trip_pace') == 'packed':
            tradeoffs.append('packed pace can fit more highlights but increases logistics risk')
        if not tradeoffs:
            tradeoffs.append('main tradeoff depends on final dates, flight access, and accommodation style')

        budget_signal = 'strong' if cost_value and cost_value <= 120 else 'moderate' if cost_value and cost_value <= 200 else 'premium' if cost_value else 'unknown'
        season_signal = 'strong' if travel_months and season_overlap else 'caution' if travel_months else 'unknown until dates are known'
        interest_signal = 'strong' if matched_interests else 'needs review' if interests else 'open'
        pace = constraint_details.get('trip_pace')
        pace_signal = 'strong for relaxed pacing' if pace == 'relaxed' and len(data.get('highlights', [])) >= 3 else 'watch logistics' if pace == 'packed' else 'neutral'
        decision_matrix = [
            {'criterion': 'Budget fit', 'signal': budget_signal, 'evidence': f"about ${cost_value} per person/day" if cost_value else 'no benchmark selected'},
            {'criterion': 'Season fit', 'signal': season_signal, 'evidence': f"requested {', '.join(requested_seasons)}; best months {', '.join(seasons)}" if travel_months else f"best months {', '.join(seasons)}; ask for dates to score timing"},
            {'criterion': 'Interest fit', 'signal': interest_signal, 'evidence': f"matches {', '.join(matched_interests[:2])}" if matched_interests else f"review against {', '.join(interests[:2])}" if interests else 'interests not specified'},
            {'criterion': 'Pace fit', 'signal': pace_signal, 'evidence': 'relaxed pace favors fewer bases and short transfers' if pace == 'relaxed' else 'pace not specified or needs routing validation'},
        ]
        best_for = []
        if budget_signal == 'strong':
            best_for.append('lower daily cost pressure')
        if season_signal == 'strong':
            best_for.append('requested travel timing')
        if matched_interests:
            best_for.append(f"{', '.join(matched_interests[:2])} interests")
        if not best_for:
            best_for.append('further research after dates, flights, and lodging are known')
        watch_out = tradeoffs[:2] or ['final dates, flight access, and accommodation availability']

        rows.append({
            'name': data['name'],
            'country': data['country'],
            'data_confidence': 'high',
            'budget_daily_usd': cost_value,
            'best_months': seasons,
            'fit_factors': fit_factors[:3],
            'tradeoffs': tradeoffs[:2],
            'decision_matrix': decision_matrix,
            'best_for': best_for[:3],
            'watch_out': watch_out[:2],
        })

    ranked = sorted(
        enumerate(rows),
        key=lambda item: (
            item[1].get('data_confidence') != 'high',
            0 if any(c.get('criterion') == 'Season fit' and c.get('signal') == 'strong' for c in item[1].get('decision_matrix', [])) else 1 if travel_months else 0,
            item[1].get('budget_daily_usd') if item[1].get('budget_daily_usd') is not None else 10**9,
            item[0],
        )
    )
    recommended = ranked[0][1]['name'] if ranked else rows[0]['name']
    for row in rows:
        if row['name'] == recommended:
            row['decision_signal'] = 'Best first-pass fit from bundled data; use as the default unless dates or flights say otherwise.'
        elif row.get('budget_daily_usd') and rows[ranked[0][0]].get('budget_daily_usd'):
            delta = row['budget_daily_usd'] - rows[ranked[0][0]]['budget_daily_usd']
            if delta > 0:
                row['decision_signal'] = f'Consider if its highlights matter more than roughly ${delta}/person/day extra cost.'
            else:
                row['decision_signal'] = 'Comparable cost profile; decide by season, flight access, and preferred highlights.'
        else:
            row.setdefault('decision_signal', 'Compare after filling missing reference or live data.')

    runner_up = next((row['name'] for row in rows if row['name'] != recommended), None)
    operator_summary = f"Start with {recommended} based on the decision matrix; use {runner_up} as the main alternate if flights, lodging, or must-do interests outweigh the default." if runner_up else f"Start with {recommended} based on the decision matrix."

    return {
        'options': rows,
        'recommended_option': recommended,
        'operator_summary': operator_summary,
        'how_to_decide': [
            'Use budget_daily_usd to spot cost pressure before building an itinerary.',
            'Use best_months to avoid season mismatch once travel dates are known.',
            'Scan each option decision_matrix for budget, season, interest, and pace signals.',
            'Use best_for and watch_out to explain the recommendation without burying the user in raw data.',
        ]
    }


def place_planning_metadata(dest_name):
    """Offline hints for first-pass risk/fallback checks.

    The reference highlights do not include hours, exact coordinates, or venue
    closure feeds, so this metadata stays deliberately conservative: it only
    captures broad zone and indoor/outdoor characteristics needed to suggest a
    nearby fallback before live validation.
    """
    metadata = {
        'kyoto': {
            'Fushimi Inari': {'zone': 'south/east Kyoto', 'setting': 'outdoor'},
            'Kiyomizu-dera': {'zone': 'east Kyoto', 'setting': 'outdoor'},
            'Gion District': {'zone': 'east/central Kyoto', 'setting': 'both'},
            'Kinkaku-ji': {'zone': 'north Kyoto', 'setting': 'outdoor'},
            'Arashiyama Bamboo': {'zone': 'west Kyoto', 'setting': 'outdoor'},
        },
        'tokyo': {
            'Tsukiji Outer Market': {'zone': 'central/east Tokyo', 'setting': 'both'},
            'Senso-ji Temple': {'zone': 'east Tokyo', 'setting': 'outdoor'},
            'Akihabara': {'zone': 'east/central Tokyo', 'setting': 'indoor'},
            'Meiji Shrine': {'zone': 'west Tokyo', 'setting': 'outdoor'},
            'Shibuya Crossing': {'zone': 'west Tokyo', 'setting': 'outdoor'},
        },
        'paris': {
            'Montmartre': {'zone': 'north Paris', 'setting': 'outdoor'},
            'Louvre Museum': {'zone': 'central Paris', 'setting': 'indoor'},
            'Notre-Dame': {'zone': 'central Paris', 'setting': 'both'},
            "Musée d'Orsay": {'zone': 'central/west Paris', 'setting': 'indoor'},
            'Eiffel Tower': {'zone': 'west Paris', 'setting': 'outdoor'},
        },
    }
    return metadata.get((dest_name or '').lower(), {})

def build_day_plan_continuity(dest_data, suggested_places, constraint_details):
    """Build a small morning/afternoon/evening sequencing scaffold.

    This is intentionally lightweight and offline: reference highlights do not carry
    attraction-level coordinates, so we use destination-specific zones plus a few
    durable ordering heuristics to reduce obvious backtracking before a full route
    engine expands the plan.
    """
    if not dest_data or len(suggested_places) < 3:
        return None

    dest_name = dest_data.get('name', '')
    dest_key = dest_name.lower()
    zone_maps = {
        'kyoto': {
            'Fushimi Inari': 'south/east Kyoto',
            'Kiyomizu-dera': 'east Kyoto',
            'Gion District': 'east/central Kyoto',
            'Kinkaku-ji': 'north Kyoto',
            'Arashiyama Bamboo': 'west Kyoto',
        },
        'tokyo': {
            'Tsukiji Outer Market': 'central/east Tokyo',
            'Senso-ji Temple': 'east Tokyo',
            'Akihabara': 'east/central Tokyo',
            'Meiji Shrine': 'west Tokyo',
            'Shibuya Crossing': 'west Tokyo',
        },
        'paris': {
            'Montmartre': 'north Paris',
            'Louvre Museum': 'central Paris',
            'Notre-Dame': 'central Paris',
            "Musée d'Orsay": 'central/west Paris',
            'Eiffel Tower': 'west Paris',
        },
    }
    preferred_orders = {
        'kyoto': ['Fushimi Inari', 'Kiyomizu-dera', 'Gion District', 'Kinkaku-ji', 'Arashiyama Bamboo'],
        'tokyo': ['Tsukiji Outer Market', 'Senso-ji Temple', 'Akihabara', 'Meiji Shrine', 'Shibuya Crossing'],
        'paris': ['Montmartre', 'Louvre Museum', 'Notre-Dame', "Musée d'Orsay", 'Eiffel Tower'],
    }

    zone_map = {name: meta['zone'] for name, meta in place_planning_metadata(dest_name).items()} or zone_maps.get(dest_key, {})
    preferred_order = preferred_orders.get(dest_key, [])
    by_name = {place['name']: place for place in suggested_places}
    ordered_names = [name for name in preferred_order if name in by_name]
    ordered_names.extend(place['name'] for place in suggested_places if place['name'] not in ordered_names)

    base_hint = constraint_details.get('neighborhood_preference') if constraint_details else None
    if base_hint:
        base_lower = base_hint.lower()
        base_matches = [name for name in ordered_names if base_lower in name.lower() or base_lower in zone_map.get(name, '').lower()]
        if base_matches:
            # Start near the requested base, then keep the remaining destination-specific order.
            ordered_names = base_matches + [name for name in ordered_names if name not in base_matches]

    selected = ordered_names[:3]
    if len(selected) < 3:
        return None

    slots = ['morning', 'afternoon', 'evening']
    segments = []
    for slot, name in zip(slots, selected):
        zone = zone_map.get(name, f'{dest_name} core')
        if slot == 'morning':
            reason = f'start in {zone} to anchor the day before cross-town moves'
        elif slot == 'afternoon':
            previous_zone = segments[-1]['zone']
            if zone == previous_zone:
                reason = f'continue within {zone} to avoid unnecessary backtracking'
            else:
                reason = f'move from {previous_zone} toward {zone} in one directional hop'
        else:
            previous_zone = segments[-1]['zone']
            if zone == previous_zone:
                reason = f'end nearby in {zone}, keeping the final leg compact'
            else:
                reason = f'finish in {zone} after a single planned transfer from {previous_zone}'
        segments.append({
            'time_of_day': slot,
            'place': name,
            'zone': zone,
            'continuity_reason': reason,
        })

    transitions = []
    for left, right in zip(segments, segments[1:]):
        if left['zone'] == right['zone']:
            transition = f"{left['place']} → {right['place']}: same-zone pairing keeps walking/transit short."
        else:
            transition = f"{left['place']} → {right['place']}: directional move from {left['zone']} to {right['zone']} limits backtracking."
        transitions.append(transition)

    return {
        'sequencing_goal': 'morning/afternoon/evening anchors ordered to reduce backtracking before detailed routing',
        'segments': segments,
        'transition_rationale': transitions,
        'backtracking_note': 'Use this as the first-pass continuity scaffold to reduce backtracking; verify live transit, hours, and meal timing before finalizing.',
    }




def _safe_inline(value):
    """Keep generated Markdown table/draft cells single-line and pipe-safe."""
    return str(value).replace('\n', ' ').replace('|', '\|').strip()


def build_output_polish(ctx, dest_data, destination_comparison, risk_fallbacks):
    """Add a compact operator-facing response scaffold for final presentation.

    This does not replace the structured extraction fields. It gives agents a
    small, stable surface for turning the JSON into a clearer user reply with
    sections, rationale, next actions, and a concise response template.
    """
    sections = []
    destination = ctx.get('destination', {})
    if destination:
        place = destination.get('name', 'selected destination')
        sections.append({
            'title': 'Trip Snapshot',
            'purpose': f'Summarize destination, duration, travelers, budget, and key constraints for {place}.',
        })
    if ctx.get('suggested_places') or destination_comparison:
        sections.append({
            'title': 'Best-Fit Choices',
            'purpose': 'Show the ranked places or destination options with concise why-this-fit evidence.',
        })
    if ctx.get('day_plan_continuity'):
        sections.append({
            'title': 'Day Flow',
            'purpose': 'Present morning/afternoon/evening anchors and transition rationale to reduce backtracking.',
        })
    if risk_fallbacks:
        sections.append({
            'title': 'Risks + Backups',
            'purpose': 'Call out fragile assumptions and the nearest viable fallback before the user commits.',
        })

    if not sections:
        sections.append({
            'title': 'Planning Snapshot',
            'purpose': 'Reflect what is known and ask the single highest-impact next question.',
        })

    rationale = []
    if destination_comparison:
        summary = destination_comparison.get('operator_summary')
        if summary:
            rationale.append(summary)
        else:
            rationale.append(f"Recommended {destination_comparison['recommended_option']} from the bundled comparison because it ranks best on first-pass cost/data fit.")
    elif ctx.get('suggested_places'):
        top = ctx['suggested_places'][0]
        factors = top.get('why_chosen', [])[:2]
        rationale.append(f"Lead with {top['name']} because {'; '.join(factors)}.")
    if ctx.get('day_plan_continuity'):
        first_segment = ctx['day_plan_continuity'].get('segments', [{}])[0]
        first_place = first_segment.get('place')
        if first_place:
            rationale.append(f'Sequence the day from {first_place} using the continuity scaffold before adding live transit, meal timing, or booking details.')
        else:
            rationale.append('Sequence the day around the continuity scaffold before adding live transit, meal timing, or booking details.')
    if risk_fallbacks:
        rationale.append(f"Keep {len(risk_fallbacks)} fallback warning(s) visible so the plan degrades gracefully instead of failing late.")
    if not rationale:
        missing = ', '.join(ctx.get('open_decisions', [])[:3]) or 'remaining trip details'
        rationale.append(f"Prioritize filling {missing} before producing a final itinerary.")

    confidence_drivers = []
    if destination_comparison:
        confidence_drivers.append(f"ranked {len(destination_comparison.get('options', []))} destination option(s) with decision-matrix evidence")
    if ctx.get('suggested_places'):
        confidence_drivers.append(f"scored {len(ctx['suggested_places'])} place candidate(s) with why-chosen factors")
    if ctx.get('day_plan_continuity'):
        confidence_drivers.append('built a day-flow scaffold to reduce backtracking')
    if risk_fallbacks:
        confidence_drivers.append(f"surfaced {len(risk_fallbacks)} fallback warning(s) before final itinerary work")
    if ctx.get('constraint_details'):
        captured = ', '.join(sorted(ctx['constraint_details'].keys()))
        confidence_drivers.append(f"captured explicit constraints: {captured}")
    if not confidence_drivers:
        confidence_drivers.append('limited structured evidence so the next response should stay in discovery mode')

    actions = []
    open_decisions = ctx.get('open_decisions', [])
    if open_decisions:
        actions.append(f"Ask one concise question to resolve: {open_decisions[0]}.")
    if ctx.get('suggested_places'):
        actions.append('Validate live hours, transit, and current pricing for the top ranked anchors.')
    if ctx.get('day_plan_continuity'):
        actions.append('Convert the continuity scaffold into a timed day plan once dates and meal preferences are known.')
    if risk_fallbacks:
        actions.append('Confirm whether the suggested fallback is acceptable before locking the plan.')
    if not actions:
        actions.append('Move from discovery into a detailed itinerary with times, costs, transport, and meals.')

    assumption_ledger = []
    if ctx.get('suggested_places') or destination_comparison:
        assumption_ledger.append({
            'type': 'offline_reference',
            'status': 'needs_operator_validation',
            'assumption': 'Place ranking and destination comparison use bundled offline reference data',
            'impact': 'Verify live hours, transit, current pricing, closures, and availability before presenting a final itinerary.',
        })
    if ctx.get('day_plan_continuity'):
        assumption_ledger.append({
            'type': 'route_scaffold',
            'status': 'provisional',
            'assumption': 'Morning/afternoon/evening order is based on broad zone heuristics rather than live routing',
            'impact': 'Run a live route check before locking exact times or transport modes.',
        })
    if risk_fallbacks:
        assumption_ledger.append({
            'type': 'fallback_needed',
            'status': 'needs_confirmation',
            'assumption': risk_fallbacks[0]['warning'],
            'impact': f"Use {risk_fallbacks[0]['fallback']['nearest_viable_alternative']} if the primary plan fails validation.",
        })
    if ctx.get('constraint_details'):
        captured_constraints = ', '.join(sorted(ctx['constraint_details'].keys()))
        assumption_ledger.append({
            'type': 'constraint_fit',
            'status': 'must_preserve',
            'assumption': f'Captured constraints are active: {captured_constraints}',
            'impact': 'Do not expand or polish the itinerary in a way that silently drops these constraints.',
        })
    if open_decisions:
        for decision in open_decisions[:3]:
            assumption_ledger.append({
                'type': 'missing_input',
                'status': 'needs_user_confirmation',
                'assumption': f'{decision} is not confirmed yet',
                'impact': 'Keep the response in discovery mode or label any itinerary expansion as provisional.',
            })
    if not assumption_ledger:
        assumption_ledger.append({
            'type': 'ready_state',
            'status': 'low_risk',
            'assumption': 'No major missing inputs or first-pass fallback warnings were detected from offline parsing',
            'impact': 'Proceed to itinerary expansion while still labeling live availability checks before booking.',
        })
    assumption_ledger = assumption_ledger[:5]

    primary_place = None
    if ctx.get('suggested_places'):
        primary_place = ctx['suggested_places'][0].get('name')
    elif destination_comparison:
        primary_place = destination_comparison.get('recommended_option')
    elif destination:
        primary_place = destination.get('name')

    next_question = None
    question_meta = {
        'destination': {
            'prompt': 'Which destination should I optimize for first?',
            'why_now': 'Locks the primary geography so comparisons or day-flow scaffolds do not stay generic.',
            'answer_examples': ['Tokyo', 'Paris first, Bangkok as backup', 'Keep comparing all three'],
            'unlocks': 'destination-specific ranking, routing, and budget checks',
        },
        'dates/duration': {
            'prompt': 'What dates or trip length should I plan around?',
            'why_now': 'Dates and length determine season fit, opening-hours risk, and how packed the day plan can be.',
            'answer_examples': ['April 3-9', '5 nights in late May', 'Flexible weekend'],
            'unlocks': 'season-aware sequencing and realistic daily pacing',
        },
        'travelers': {
            'prompt': 'How many people are traveling?',
            'why_now': 'Traveler count changes budget math, room assumptions, and activity suitability.',
            'answer_examples': ['solo', '2 adults', 'family of 4 with kids'],
            'unlocks': 'per-person cost checks and group-fit filtering',
        },
        'budget': {
            'prompt': 'What budget range should I optimize for?',
            'why_now': 'Budget determines whether the recommendation should prioritize low-cost anchors, comfort, or splurge moments.',
            'answer_examples': ['under $1800 total', '$250/day', 'mid-range comfort'],
            'unlocks': 'budget-fit warnings and sharper candidate ranking',
        },
        'interests': {
            'prompt': 'Which experiences matter most for this trip?',
            'why_now': 'Interest fit is the strongest signal for choosing among viable places.',
            'answer_examples': ['food and temples', 'art and nightlife', 'nature plus local markets'],
            'unlocks': 'thematic ranking and better why-chosen explanations',
        },
        'accommodation': {
            'prompt': 'What type of stay should I assume?',
            'why_now': 'The stay type affects base neighborhood, daily start/end flow, and budget realism.',
            'answer_examples': ['boutique hotel', 'apartment near transit', 'budget ryokan'],
            'unlocks': 'base-area routing and lodging-budget assumptions',
        },
        'transport': {
            'prompt': 'Should I prioritize walking, public transit, taxis, trains, or rental car?',
            'why_now': 'Transport preference determines whether the day flow is realistic or too spread out.',
            'answer_examples': ['mostly walking and metro', 'taxis okay at night', 'rental car'],
            'unlocks': 'route continuity checks and transfer-time caveats',
        },
        'constraints': {
            'prompt': 'Any pace, dietary, accessibility, weather, or opening-hours constraints I should honor?',
            'why_now': 'Constraints prevent a polished plan from silently violating traveler needs.',
            'answer_examples': ['relaxed pace', 'vegetarian and rain backup', 'must avoid stairs'],
            'unlocks': 'fallback warnings and constraint-safe itinerary expansion',
        },
    }
    if open_decisions:
        next_question = question_meta.get(open_decisions[0], {
            'prompt': f'Can you clarify {open_decisions[0]}?',
            'why_now': 'This missing input is blocking a safer next planning pass.',
            'answer_examples': ['Share the missing preference', 'Use your best assumption', 'Ask me a narrower follow-up'],
            'unlocks': 'a more specific, lower-risk itinerary pass',
        })['prompt']

    template_lines = [
        f"Lead with: {primary_place or 'the best current option'}",
        f"Why: {rationale[0] if rationale else 'Use the strongest available fit evidence from the structured fields.'}",
        f"Watch: {risk_fallbacks[0]['warning'] if risk_fallbacks else 'No major first-pass fallback warning from offline data.'}",
        f"Next: {next_question or actions[0]}",
    ]

    if risk_fallbacks:
        readiness = 'needs live validation before final itinerary'
    elif open_decisions:
        readiness = 'needs one clarification before detailed planning'
    else:
        readiness = 'ready for detailed itinerary expansion'

    summary_subject = primary_place or 'the current plan'
    decision_summary = f"Recommend {summary_subject}; {readiness}."

    status_line = {
        'readiness': readiness,
        'recommended_focus': summary_subject,
        'evidence_count': len(confidence_drivers),
        'fallback_count': len(risk_fallbacks),
        'open_decisions_count': len(open_decisions),
        'next_owner': 'user' if open_decisions else 'operator',
    }

    checklist = []
    if open_decisions:
        checklist.append({
            'owner': 'user',
            'action': next_question or f"Clarify {open_decisions[0]}",
            'status': 'needed',
        })
    if ctx.get('suggested_places') or destination_comparison:
        checklist.append({
            'owner': 'operator',
            'action': 'Verify live hours, transit, pricing, and availability for the recommended anchors.',
            'status': 'before final itinerary',
        })
    if ctx.get('day_plan_continuity'):
        checklist.append({
            'owner': 'operator',
            'action': 'Turn the day-flow scaffold into timed morning, afternoon, and evening blocks.',
            'status': 'next planning pass',
        })
    if risk_fallbacks:
        checklist.append({
            'owner': 'user',
            'action': f"Confirm fallback preference: {risk_fallbacks[0]['fallback']['nearest_viable_alternative']}",
            'status': 'recommended',
        })
    if not checklist:
        checklist.append({
            'owner': 'operator',
            'action': actions[0],
            'status': 'next',
        })

    first_check = checklist[0]
    if first_check['owner'] == 'user':
        prompt_text = first_check['action']
        prompt_reason = 'This is the highest-impact traveler clarification before the next planning pass.'
    else:
        prompt_text = first_check['action']
        prompt_reason = 'This is the highest-impact operator validation before presenting or expanding the plan.'
    next_step_prompt = {
        'audience': first_check['owner'],
        'prompt': prompt_text,
        'reason': prompt_reason,
        'source': 'next_action_checklist[0]',
    }

    clarification_prompt_card = None
    if open_decisions:
        missing_key = open_decisions[0]
        meta = question_meta.get(missing_key, {
            'prompt': next_question or f'Can you clarify {missing_key}?',
            'why_now': 'This missing input is blocking a safer next planning pass.',
            'answer_examples': ['Share the missing preference', 'Use your best assumption', 'Ask me a narrower follow-up'],
            'unlocks': 'a more specific, lower-risk itinerary pass',
        })
        known_context = []
        if destination:
            known_context.append(f"destination={destination.get('name')}")
        if ctx.get('duration'):
            known_context.append(f"duration={ctx.get('duration')} days")
        if ctx.get('budget'):
            budget_context = ctx.get('budget')
            if budget_context.get('tier'):
                known_context.append(f"budget_tier={budget_context.get('tier')}")
            if budget_context.get('cap'):
                cap = budget_context.get('cap')
                known_context.append(f"budget_cap={cap.get('currency')} {cap.get('amount')}")
        if ctx.get('constraint_details'):
            known_context.append('constraints=' + ', '.join(sorted(ctx['constraint_details'].keys())))
        clarification_prompt_card = {
            'missing_decision': missing_key,
            'prompt': meta['prompt'],
            'why_now': meta['why_now'],
            'answer_examples': meta['answer_examples'],
            'unlocks': meta['unlocks'],
            'known_context': known_context[:4],
            'copy_text': f"{meta['prompt']} Examples: {', '.join(meta['answer_examples'][:3])}.",
        }

    action_plan = []
    if open_decisions:
        action_plan.append({
            'step': 1,
            'owner': 'user',
            'action': next_question or f"Clarify {open_decisions[0]}",
            'trigger': f"missing {open_decisions[0]}",
            'outcome': 'unblocks a more specific, lower-risk itinerary pass',
        })
    if risk_fallbacks:
        fallback_name = risk_fallbacks[0]['fallback']['nearest_viable_alternative']
        action_plan.append({
            'step': len(action_plan) + 1,
            'owner': 'operator',
            'action': f"Validate the fallback path around {fallback_name}",
            'trigger': risk_fallbacks[0]['risk'],
            'outcome': 'keeps the recommendation graceful if the primary anchor fails live checks',
        })
    if ctx.get('suggested_places') or destination_comparison:
        action_plan.append({
            'step': len(action_plan) + 1,
            'owner': 'operator',
            'action': 'Check live hours, transit, pricing, and availability before finalizing.',
            'trigger': 'offline recommendation evidence only',
            'outcome': 'turns the current recommendation into a bookable or presentation-ready plan',
        })
    if ctx.get('day_plan_continuity'):
        action_plan.append({
            'step': len(action_plan) + 1,
            'owner': 'operator',
            'action': 'Expand the continuity scaffold into timed morning, afternoon, and evening blocks.',
            'trigger': 'day_plan_continuity available',
            'outcome': 'preserves geographic flow while adding times, meals, and transport',
        })
    if not action_plan:
        action_plan.append({
            'step': 1,
            'owner': 'operator',
            'action': actions[0],
            'trigger': 'planning snapshot has no stronger structured next move',
            'outcome': 'moves the conversation toward the next itinerary decision',
        })
    for index, item in enumerate(action_plan[:4], start=1):
        item['step'] = index
    action_plan = action_plan[:4]

    if risk_fallbacks:
        readiness_tone = 'caution'
        readiness_code = 'needs_live_validation'
    elif open_decisions:
        readiness_tone = 'needs_input'
        readiness_code = 'needs_clarification'
    else:
        readiness_tone = 'ready'
        readiness_code = 'ready_to_expand'

    decision_badges = [
        {
            'label': 'Readiness',
            'value': readiness_code,
            'tone': readiness_tone,
        },
        {
            'label': 'Next owner',
            'value': first_check['owner'],
            'tone': 'action',
        },
        {
            'label': 'Fallbacks',
            'value': f"{len(risk_fallbacks)} warning(s)",
            'tone': 'caution' if risk_fallbacks else 'clear',
        },
    ]
    if destination_comparison:
        decision_badges.append({
            'label': 'Decision mode',
            'value': 'destination_comparison',
            'tone': 'compare',
        })
    elif ctx.get('day_plan_continuity'):
        decision_badges.append({
            'label': 'Decision mode',
            'value': 'day_flow_scaffold',
            'tone': 'sequence',
        })

    markdown_sections = [
        {
            'heading': 'Recommendation',
            'body': decision_summary,
        },
        {
            'heading': 'Why this fits',
            'body': ' '.join(rationale[:2]) if rationale else 'Use the strongest available fit evidence from the structured fields.',
        },
        {
            'heading': 'Watch-outs',
            'body': risk_fallbacks[0]['warning'] if risk_fallbacks else 'No major first-pass fallback warning from offline data.',
        },
        {
            'heading': 'Next step',
            'body': f"{next_step_prompt['prompt']} ({next_step_prompt['audience']})",
        },
    ]
    presentation_markdown = '\n\n'.join(
        f"### {section['heading']}\n{section['body']}" for section in markdown_sections
    )

    final_reply_sections = [
        {
            'heading': 'Recommendation',
            'body': decision_summary,
            'source': 'decision_summary',
        },
        {
            'heading': 'Why this fits',
            'body': rationale[0] if rationale else 'Use the strongest available fit evidence from the structured fields.',
            'source': 'decision_rationale[0]',
        },
        {
            'heading': 'Evidence',
            'body': confidence_drivers[0] if confidence_drivers else 'Structured evidence is limited; keep the reply in discovery mode.',
            'source': 'confidence_drivers[0]',
        },
    ]
    if ctx.get('day_plan_continuity'):
        transitions = ctx['day_plan_continuity'].get('transition_rationale', [])
        if transitions:
            final_reply_sections.append({
                'heading': 'Flow note',
                'body': transitions[0],
                'source': 'day_plan_continuity.transition_rationale[0]',
            })
    final_reply_sections.extend([
        {
            'heading': 'Watch-out',
            'body': risk_fallbacks[0]['warning'] if risk_fallbacks else 'No major first-pass fallback warning from offline data.',
            'source': 'risk_fallbacks[0].warning' if risk_fallbacks else 'offline_risk_scan',
        },
        {
            'heading': f"Next ({next_step_prompt['audience']})",
            'body': next_step_prompt['prompt'],
            'source': 'next_step_prompt',
        },
    ])
    final_reply_preview = {
        'audience': 'traveler',
        'format': 'compact final reply preview',
        'presentation_mode': 'provisional recommendation' if (open_decisions or risk_fallbacks or ctx.get('suggested_places') or destination_comparison) else 'ready for final itinerary expansion',
        'sections': final_reply_sections[:6],
        'markdown': '\n'.join(
            f"- **{_safe_inline(section['heading'])}:** {_safe_inline(section['body'])}"
            for section in final_reply_sections[:6]
        ),
        'safety_note': 'Use this as a ready-to-adapt reply preview; it keeps rationale, evidence, watch-out, and next owner visible.',
    }

    handoff_brief = {
        'title': f"Planning handoff — {summary_subject}",
        'decision': decision_summary,
        'rationale_bullets': rationale[:3],
        'watch_out': risk_fallbacks[0]['warning'] if risk_fallbacks else 'No major first-pass fallback warning from offline data.',
        'next_action': {
            'owner': next_step_prompt['audience'],
            'prompt': next_step_prompt['prompt'],
            'reason': next_step_prompt['reason'],
        },
        'evidence_drivers': confidence_drivers[:3],
    }

    quick_reply_card = {
        'title': f"Best next move: {summary_subject}",
        'subtitle': readiness,
        'bullets': [
            rationale[0] if rationale else 'Use the strongest available fit evidence from the structured fields.',
            confidence_drivers[0] if confidence_drivers else 'Evidence is limited; stay in discovery mode.',
        ],
        'caveat': risk_fallbacks[0]['warning'] if risk_fallbacks else 'No major first-pass fallback warning from offline data.',
        'next_ask': next_step_prompt['prompt'],
        'cta': 'Reply with the missing detail so I can expand this into a timed, budget-aware itinerary.' if next_step_prompt['audience'] == 'user' else 'Verify the operator checklist item, then expand the plan.',
    }

    if open_decisions:
        safe_to_send_now = 'Ask the traveler for the highest-priority missing input before expanding the itinerary.'
        send_mode = 'clarification_only'
    elif risk_fallbacks:
        safe_to_send_now = 'Share a provisional recommendation with the first fallback warning visible; do not present it as final.'
        send_mode = 'provisional_with_fallback'
    elif ctx.get('suggested_places') or destination_comparison:
        safe_to_send_now = 'Share a provisional recommendation after operator live checks for hours, transit, pricing, and availability.'
        send_mode = 'operator_validation_first'
    else:
        safe_to_send_now = 'Use discovery-mode language and ask the next best question.'
        send_mode = 'discovery'
    operator_preflight_card = {
        'audience': 'operator',
        'format': 'send-readiness preflight',
        'recommended_focus': summary_subject,
        'send_mode': send_mode,
        'safe_to_send_now': safe_to_send_now,
        'must_include': [
            f"recommendation: {decision_summary}",
            f"evidence: {confidence_drivers[0] if confidence_drivers else 'limited structured evidence'}",
            f"watch-out: {risk_fallbacks[0]['warning'] if risk_fallbacks else 'No major first-pass fallback warning from offline data.'}",
            f"next owner: {next_step_prompt['audience']}",
        ],
        'do_not_claim': 'Do not claim live hours, routes, prices, bookings, or final viability until operator validation passes.',
        'copy_prompt': f"Before sending: include the recommendation, one evidence line, the watch-out, and this next action ({next_step_prompt['audience']}): {next_step_prompt['prompt']}",
    }

    validation_checks = []
    if ctx.get('suggested_places') or destination_comparison:
        validation_checks.append({
            'check': 'live_viability',
            'owner': 'operator',
            'question': f"Are live hours, transit, pricing, and availability acceptable for {summary_subject}?",
            'pass_criteria': 'recommended anchors are open or bookable in the intended window and fit the stated budget tier/cap',
            'fallback_if_fails': risk_fallbacks[0]['fallback']['nearest_viable_alternative'] if risk_fallbacks else 'rerank the next bundled candidate before presenting the itinerary',
        })
    if ctx.get('day_plan_continuity'):
        validation_checks.append({
            'check': 'route_continuity',
            'owner': 'operator',
            'question': 'Does the morning/afternoon/evening order still reduce backtracking after live transit checks?',
            'pass_criteria': 'each transition is same-zone or a single directional hop with reasonable transfer time',
            'fallback_if_fails': 'swap the weakest segment with the nearest same-zone candidate before adding meal timing',
        })
    if ctx.get('constraint_details'):
        validation_checks.append({
            'check': 'constraint_fit',
            'owner': 'operator',
            'question': 'Do the selected anchors honor the captured pace, food, neighborhood, hours, budget, and weather constraints?',
            'pass_criteria': 'no captured constraint is ignored without an explicit user-visible caveat or backup',
            'fallback_if_fails': 'ask the user to relax the lowest-priority constraint or accept the nearest viable fallback',
        })
    if open_decisions:
        validation_checks.append({
            'check': 'user_clarification',
            'owner': 'user',
            'question': next_question or f"Can you clarify {open_decisions[0]}?",
            'pass_criteria': 'the missing decision is answered before detailed itinerary expansion',
            'fallback_if_fails': 'continue in discovery mode with assumptions clearly labeled',
        })
    if not validation_checks:
        validation_checks.append({
            'check': 'ready_to_expand',
            'owner': 'operator',
            'question': 'Is the structured context sufficient to expand into a timed itinerary?',
            'pass_criteria': 'core destination, duration, budget, interests, and constraints are stable enough for the next pass',
            'fallback_if_fails': 'ask one targeted discovery question before itinerary expansion',
        })
    validation_checks = validation_checks[:4]
    validation_summary = {
        'purpose': 'operator-visible go/no-go checks before presenting or expanding the recommendation',
        'recommended_focus': summary_subject,
        'overall_gate': 'hold for user clarification' if open_decisions else 'verify live details before final itinerary' if (ctx.get('suggested_places') or destination_comparison or risk_fallbacks) else 'ready for itinerary expansion',
        'checks': validation_checks,
    }

    review_queue_items = []
    if open_decisions:
        review_queue_items.append({
            'priority': 1,
            'owner': 'user',
            'severity': 'blocker',
            'task': next_question or f"Clarify {open_decisions[0]}",
            'source': 'open_decisions[0]',
            'done_when': 'Traveler answer resolves the highest-priority missing input before itinerary expansion.',
        })
    if risk_fallbacks:
        review_queue_items.append({
            'priority': len(review_queue_items) + 1,
            'owner': 'operator',
            'severity': 'warning',
            'task': f"Validate fallback viability for {risk_fallbacks[0]['fallback']['nearest_viable_alternative']}",
            'source': 'risk_fallbacks[0]',
            'done_when': 'Fallback is compatible with the same constraints and can replace the primary anchor if live checks fail.',
        })
    if ctx.get('suggested_places') or destination_comparison:
        review_queue_items.append({
            'priority': len(review_queue_items) + 1,
            'owner': 'operator',
            'severity': 'required',
            'task': f"Run live viability checks for {summary_subject}",
            'source': 'suggested_places[0]' if ctx.get('suggested_places') else 'destination_comparison.recommended_option',
            'done_when': 'Hours, transit, pricing, and availability are acceptable or the recommendation is reranked.',
        })
    if ctx.get('constraint_details'):
        review_queue_items.append({
            'priority': len(review_queue_items) + 1,
            'owner': 'operator',
            'severity': 'required',
            'task': 'Confirm active constraints are preserved in the next response',
            'source': 'constraint_details',
            'done_when': 'Budget, pace, neighborhood, hours, food, and weather constraints remain visible or caveated.',
        })
    if ctx.get('day_plan_continuity'):
        review_queue_items.append({
            'priority': len(review_queue_items) + 1,
            'owner': 'operator',
            'severity': 'advisory',
            'task': 'Check day-flow continuity before timed expansion',
            'source': 'day_plan_continuity',
            'done_when': 'Morning, afternoon, and evening anchors still avoid unnecessary backtracking after live routing checks.',
        })
    if not review_queue_items:
        review_queue_items.append({
            'priority': 1,
            'owner': 'operator',
            'severity': 'advisory',
            'task': actions[0],
            'source': 'next_step_actions[0]',
            'done_when': 'The next planning move is completed or converted into a traveler clarification.',
        })
    for index, item in enumerate(review_queue_items[:5], start=1):
        item['priority'] = index
    operator_review_queue = {
        'audience': 'operator',
        'format': 'prioritized review queue',
        'recommended_focus': summary_subject,
        'queue_status': 'blocked' if open_decisions else 'needs_validation' if (risk_fallbacks or ctx.get('suggested_places') or destination_comparison) else 'ready',
        'items': review_queue_items[:5],
        'copy_text': '\n'.join(
            f"{item['priority']}. [{item['owner']}/{item['severity']}] {item['task']} — done when: {item['done_when']}"
            for item in review_queue_items[:5]
        ),
    }

    constraint_compliance_checks = []
    budget_context = ctx.get('budget') or {}
    if isinstance(budget_context, dict) and budget_context.get('cap'):
        cap = budget_context['cap']
        constraint_compliance_checks.append({
            'constraint': 'budget_cap',
            'captured_value': f"{cap.get('currency', 'USD')} {cap.get('amount')}",
            'status': 'needs_operator_validation',
            'operator_check': 'Confirm selected anchors, lodging assumptions, and daily costs can fit this cap before presenting the plan as viable.',
        })
    elif isinstance(budget_context, dict) and budget_context.get('tier'):
        constraint_compliance_checks.append({
            'constraint': 'budget_tier',
            'captured_value': budget_context['tier'],
            'status': 'captured',
            'operator_check': 'Keep the recommendation aligned with this budget tier when expanding costs and tradeoffs.',
        })

    constraint_labels = {
        'trip_pace': 'Match the day count, number of anchors, and transfer load to the requested pace.',
        'neighborhood_preference': 'Keep the base area or route start/end aligned with the preferred neighborhood unless a caveat is shown.',
        'opening_hours_sensitivity': 'Verify live hours and closed days before treating any venue as locked.',
        'food_preferences': 'Confirm meals and food stops honor the captured dietary or cuisine preference.',
        'weather_sensitivity': 'Keep indoor or weather-appropriate backups visible until the forecast is checked.',
    }
    for key in ['trip_pace', 'neighborhood_preference', 'opening_hours_sensitivity', 'food_preferences', 'weather_sensitivity']:
        if key in ctx.get('constraint_details', {}):
            raw_value = ctx['constraint_details'][key]
            if isinstance(raw_value, list):
                captured_value = ', '.join(str(item) for item in raw_value)
            else:
                captured_value = str(raw_value)
            constraint_compliance_checks.append({
                'constraint': key,
                'captured_value': captured_value,
                'status': 'must_preserve',
                'operator_check': constraint_labels[key],
            })

    if not constraint_compliance_checks:
        constraint_compliance_checks.append({
            'constraint': 'none_explicit',
            'captured_value': 'No explicit traveler constraints detected beyond the core planning dimensions.',
            'status': 'no_constraint_blocker',
            'operator_check': 'Continue discovery if pace, food, neighborhood, hours, weather, or budget sensitivity could affect the plan.',
        })
    constraint_compliance_card = {
        'audience': 'operator',
        'format': 'constraint compliance checklist',
        'recommended_focus': summary_subject,
        'overall_status': 'must_preserve_constraints' if any(item['constraint'] != 'none_explicit' for item in constraint_compliance_checks) else 'no_explicit_constraints',
        'checks': constraint_compliance_checks[:6],
        'copy_text': '\n'.join(
            f"{index}. {item['constraint']}: {item['captured_value']} — {item['operator_check']}"
            for index, item in enumerate(constraint_compliance_checks[:6], start=1)
        ),
    }

    expansion_steps = []
    if ctx.get('day_plan_continuity'):
        expansion_steps.append({
            'section': 'Day flow',
            'source': 'day_plan_continuity',
            'instruction': 'Preserve the morning/afternoon/evening order and transition rationale when adding exact times, meals, and transport.',
        })
    if ctx.get('suggested_places') or destination_comparison:
        expansion_steps.append({
            'section': 'Recommendation evidence',
            'source': 'suggested_places' if ctx.get('suggested_places') else 'destination_comparison',
            'instruction': 'Carry forward at least two concrete fit factors so the expanded itinerary stays auditable.',
        })
    if ctx.get('constraint_details'):
        expansion_steps.append({
            'section': 'Constraint preservation',
            'source': 'constraint_details',
            'instruction': 'Restate active pace, budget, food, neighborhood, hours, and weather constraints before finalizing any timed plan.',
        })
    if risk_fallbacks:
        expansion_steps.append({
            'section': 'Fallback path',
            'source': 'risk_fallbacks',
            'instruction': f"Keep {risk_fallbacks[0]['fallback']['nearest_viable_alternative']} visible as the nearest viable backup until live validation passes.",
        })
    if open_decisions:
        expansion_steps.append({
            'section': 'Clarification gate',
            'source': 'open_decisions[0]',
            'instruction': next_question or f"Resolve {open_decisions[0]} before expanding beyond a provisional draft.",
        })
    if not expansion_steps:
        expansion_steps.append({
            'section': 'Itinerary build',
            'source': 'structured_context',
            'instruction': 'Expand into times, transport, costs, and meals while keeping live availability caveats visible.',
        })
    expansion_steps = expansion_steps[:5]
    itinerary_expansion_brief = {
        'audience': 'operator',
        'format': 'expansion guardrail brief',
        'recommended_focus': summary_subject,
        'readiness': readiness,
        'expansion_mode': 'provisional' if (open_decisions or risk_fallbacks) else 'ready_to_expand',
        'sections': expansion_steps,
        'copy_text': '\n'.join(
            f"{index}. {item['section']} [{item['source']}]: {item['instruction']}"
            for index, item in enumerate(expansion_steps, start=1)
        ),
        'safety_note': 'Use this before turning compact output polish into a timed itinerary; it preserves evidence, constraints, fallbacks, and clarification gates.',
    }

    finalization_blockers = []
    if open_decisions:
        finalization_blockers.append({
            'type': 'user_input',
            'owner': 'user',
            'blocker': next_question or f"Clarify {open_decisions[0]}",
            'resolution': 'Answer the highest-priority open decision before presenting this as final.',
        })
    if ctx.get('suggested_places') or destination_comparison:
        finalization_blockers.append({
            'type': 'live_validation',
            'owner': 'operator',
            'blocker': f"Verify live hours, transit, pricing, and availability for {summary_subject}",
            'resolution': 'Mark the recommended anchors viable or rerank to the nearest fallback before finalizing.',
        })
    if risk_fallbacks:
        finalization_blockers.append({
            'type': 'fallback_confirmation',
            'owner': 'user',
            'blocker': f"Confirm backup acceptability: {risk_fallbacks[0]['fallback']['nearest_viable_alternative']}",
            'resolution': 'Confirm or replace the fallback path so the plan can degrade gracefully.',
        })
    finalization_blockers = finalization_blockers[:4]
    finalization_gate = {
        'purpose': 'operator-visible final-answer gate to prevent provisional offline plans from being presented as fully final',
        'status': 'blocked' if finalization_blockers else 'ready',
        'can_present_as_final': not finalization_blockers,
        'recommended_focus': summary_subject,
        'blocking_checks': finalization_blockers,
        'safe_presentation_mode': 'provisional recommendation' if finalization_blockers else 'ready for final itinerary expansion',
        'next_resolution': finalization_blockers[0]['resolution'] if finalization_blockers else 'Proceed with a timed itinerary while retaining normal live availability caveats.',
    }

    prompt_pack_items = []
    if ctx.get('suggested_places') or destination_comparison:
        prompt_pack_items.append({
            'owner': 'operator',
            'label': 'Live viability check',
            'prompt': f"Please verify current hours, transit time, pricing, and availability for {summary_subject} before this is presented as final.",
            'success_signal': 'primary anchor is open/bookable, reachable, and still fits the stated budget or cap',
        })
    if ctx.get('day_plan_continuity'):
        prompt_pack_items.append({
            'owner': 'operator',
            'label': 'Route continuity check',
            'prompt': 'Please validate that the morning, afternoon, and evening sequence still reduces backtracking with live routing.',
            'success_signal': 'transitions remain same-zone or one directional hop after transit checks',
        })
    if risk_fallbacks:
        fallback_name = risk_fallbacks[0]['fallback']['nearest_viable_alternative']
        prompt_pack_items.append({
            'owner': 'operator',
            'label': 'Fallback readiness check',
            'prompt': f"Please confirm {fallback_name} is a viable backup if the primary recommendation fails live validation.",
            'success_signal': 'backup is close enough, compatible with constraints, and safe to offer as the nearest viable alternative',
        })
    if open_decisions:
        prompt_pack_items.append({
            'owner': 'user',
            'label': 'Traveler clarification',
            'prompt': next_question or f"Can you clarify {open_decisions[0]}?",
            'success_signal': 'traveler answer resolves the highest-priority missing decision for the next planning pass',
        })
    if not prompt_pack_items:
        prompt_pack_items.append({
            'owner': 'operator',
            'label': 'Expansion readiness check',
            'prompt': 'Please confirm the structured context is stable enough to expand into a timed itinerary.',
            'success_signal': 'core trip context is stable and any live caveats are labeled before expansion',
        })
    prompt_pack_items = prompt_pack_items[:4]
    live_validation_prompt_pack = {
        'format': 'copy-ready validation prompts',
        'title': f"Live validation prompts — {summary_subject}",
        'items': prompt_pack_items,
        'copy_text': '\n'.join(
            f"{index}. [{item['owner']}] {item['label']}: {item['prompt']}"
            for index, item in enumerate(prompt_pack_items, start=1)
        ),
        'usage_note': 'Run these before presenting the plan as final; keep user-owned clarification separate from operator checks.',
    }

    summary_lines = [
        f"Recommendation: {decision_summary}",
        f"Why: {rationale[0] if rationale else 'best available structured evidence'}",
        f"Watch-out: {risk_fallbacks[0]['warning'] if risk_fallbacks else 'No major first-pass fallback warning from offline data.'}",
        f"Next: {next_step_prompt['prompt']}",
    ]
    if confidence_drivers:
        summary_lines.insert(2, f"Evidence: {confidence_drivers[0]}")
    shareable_summary = {
        'audience': 'traveler',
        'format': 'compact shareable text',
        'title': f"{summary_subject} planning snapshot",
        'lines': summary_lines[:5],
        'text': '\n'.join(summary_lines[:5]),
        'next_action_owner': next_step_prompt['audience'],
        'tone': 'plain-language, decision-first, and safe to paste into chat',
    }

    decision_snapshot_rows = [
        {
            'label': 'Focus',
            'value': summary_subject,
            'owner': 'operator',
            'why_it_matters': 'Keeps the recommendation anchor visible in compact UIs.',
        },
        {
            'label': 'Readiness',
            'value': readiness,
            'owner': status_line['next_owner'],
            'why_it_matters': 'Shows whether to ask, validate, or expand before presenting the plan.',
        },
        {
            'label': 'Primary evidence',
            'value': confidence_drivers[0] if confidence_drivers else 'limited structured evidence',
            'owner': 'operator',
            'why_it_matters': 'Gives the shortest audit trail for why this recommendation is defensible.',
        },
        {
            'label': 'Watch-out',
            'value': risk_fallbacks[0]['warning'] if risk_fallbacks else 'No major first-pass fallback warning from offline data.',
            'owner': 'operator',
            'why_it_matters': 'Prevents the user-visible answer from overstating live certainty.',
        },
        {
            'label': 'Next action',
            'value': next_step_prompt['prompt'],
            'owner': next_step_prompt['audience'],
            'why_it_matters': next_step_prompt['reason'],
        },
    ]
    decision_snapshot_table = {
        'format': 'compact decision table',
        'columns': ['label', 'value', 'owner', 'why_it_matters'],
        'rows': decision_snapshot_rows,
        'markdown': '| Item | Value | Owner | Why it matters |\n|---|---|---|---|\n' + '\n'.join(
            f"| {_safe_inline(row['label'])} | {_safe_inline(row['value'])} | {_safe_inline(row['owner'])} | {_safe_inline(row['why_it_matters'])} |"
            for row in decision_snapshot_rows
        ),
    }

    evidence_trace_items = []
    if destination:
        evidence_trace_items.append({
            'label': 'Destination focus',
            'source': 'destination.name',
            'value': destination.get('name'),
            'why_it_matters': 'Anchors the recommendation and any geographic sequencing.',
        })
    if ctx.get('suggested_places'):
        top_place = ctx['suggested_places'][0]
        evidence_trace_items.append({
            'label': 'Top ranked place',
            'source': 'suggested_places[0]',
            'value': top_place.get('name'),
            'why_it_matters': '; '.join(top_place.get('why_chosen', [])[:2]) or 'First ranked bundled highlight for this request.',
        })
    if destination_comparison:
        evidence_trace_items.append({
            'label': 'Comparison winner',
            'source': 'destination_comparison.recommended_option',
            'value': destination_comparison.get('recommended_option'),
            'why_it_matters': destination_comparison.get('operator_summary') or 'Highest ranked option from the comparison matrix.',
        })
    if ctx.get('day_plan_continuity'):
        first_transition = (ctx['day_plan_continuity'].get('transition_rationale') or ['Continuity scaffold available before timed routing.'])[0]
        evidence_trace_items.append({
            'label': 'Route flow evidence',
            'source': 'day_plan_continuity.transition_rationale[0]',
            'value': first_transition,
            'why_it_matters': 'Shows how the first-pass day order reduces backtracking.',
        })
    if risk_fallbacks:
        evidence_trace_items.append({
            'label': 'Fallback trigger',
            'source': 'risk_fallbacks[0]',
            'value': risk_fallbacks[0]['risk'],
            'why_it_matters': risk_fallbacks[0]['warning'],
        })
    if ctx.get('constraint_details'):
        evidence_trace_items.append({
            'label': 'Active constraints',
            'source': 'constraint_details',
            'value': ', '.join(sorted(ctx['constraint_details'].keys())),
            'why_it_matters': 'These constraints must remain visible when expanding or polishing the plan.',
        })
    if not evidence_trace_items:
        evidence_trace_items.append({
            'label': 'Discovery state',
            'source': 'open_decisions',
            'value': ', '.join(open_decisions[:3]) or 'no structured evidence yet',
            'why_it_matters': 'Keep the reply in discovery mode until stronger evidence is captured.',
        })
    evidence_trace_items = evidence_trace_items[:4]
    evidence_trace_card = {
        'audience': 'operator',
        'format': 'compact evidence trace',
        'purpose': 'Shows the exact structured fields behind the recommendation so operators can audit or paste a safer rationale.',
        'items': evidence_trace_items,
        'copy_text': '\n'.join(
            f"{index}. {item['label']} [{item['source']}]: {item['value']} — {item['why_it_matters']}"
            for index, item in enumerate(evidence_trace_items, start=1)
        ),
    }

    traveler_draft_lines = [
        f"My recommendation: {decision_summary}",
        f"Why it fits: {rationale[0] if rationale else 'best available structured evidence from the planner.'}",
        f"Evidence I used: {confidence_drivers[0] if confidence_drivers else 'the request is still light on structured details.'}",
        f"Watch-out: {risk_fallbacks[0]['warning'] if risk_fallbacks else 'No major first-pass fallback warning from offline data.'}",
        f"Next: {next_step_prompt['prompt']}",
    ]
    if ctx.get('day_plan_continuity'):
        transitions = ctx['day_plan_continuity'].get('transition_rationale', [])
        if transitions:
            traveler_draft_lines.insert(3, f"Flow note: {transitions[0]}")
    if open_decisions:
        final_call = f"Reply with {open_decisions[0]} so I can tighten this into the next itinerary pass."
    elif risk_fallbacks:
        final_call = 'Confirm the backup path, then I can turn this into a timed itinerary.'
    else:
        final_call = 'I can expand this into a timed itinerary next.'
    traveler_draft_lines.append(final_call)
    traveler_facing_draft = {
        'audience': 'traveler',
        'format': 'ready-to-send concise markdown',
        'lines': traveler_draft_lines[:7],
        'markdown': '\n'.join(f"- {_safe_inline(line)}" for line in traveler_draft_lines[:7]),
        'safety_note': 'Draft preserves watch-outs and next action so agents can avoid overstating live availability.',
    }

    operator_digest_lines = [
        f"Decision: {decision_summary}",
        f"Rationale: {rationale[0] if rationale else 'Use the strongest available fit evidence from the structured fields.'}",
        f"Evidence: {confidence_drivers[0] if confidence_drivers else 'limited structured evidence'}",
        f"Watch-out: {risk_fallbacks[0]['warning'] if risk_fallbacks else 'No major first-pass fallback warning from offline data.'}",
        f"Next ({next_step_prompt['audience']}): {next_step_prompt['prompt']}",
    ]
    operator_digest = {
        'audience': 'operator',
        'format': 'copy-ready compact decision digest',
        'lines': operator_digest_lines,
        'markdown': '\n'.join(f"- {_safe_inline(line)}" for line in operator_digest_lines),
        'routing_hint': 'Ask the traveler first when the next owner is user; otherwise run the operator validation before expanding the itinerary.',
    }

    user_response_choices = []
    if open_decisions:
        missing_key = open_decisions[0]
        meta = question_meta.get(missing_key, {
            'answer_examples': ['Share the missing preference', 'Use your best assumption', 'Ask me a narrower follow-up'],
        })
        for index, example in enumerate(meta.get('answer_examples', [])[:3], start=1):
            user_response_choices.append({
                'label': example,
                'value': f"answer:{missing_key}:{index}",
                'owner': 'user',
                'reply_text': example,
                'reason': f"Example answer that resolves {missing_key} for the next planning pass.",
            })
    elif risk_fallbacks:
        fallback_name = risk_fallbacks[0]['fallback']['nearest_viable_alternative']
        user_response_choices.append({
            'label': f"Approve backup: {fallback_name}",
            'value': 'confirm:fallback',
            'owner': 'user',
            'reply_text': f"Use {fallback_name} as the backup if the primary plan fails live checks.",
            'reason': 'Confirms the fallback path before the itinerary is expanded.',
        })
    else:
        user_response_choices.append({
            'label': 'Expand this plan',
            'value': 'confirm:expand',
            'owner': 'user',
            'reply_text': 'Please expand this into a timed itinerary.',
            'reason': 'Gives the agent permission to move from compact recommendation to itinerary expansion.',
        })

    reply_options = []
    if open_decisions:
        missing_key = open_decisions[0]
        reply_options.append({
            'label': f"Answer {missing_key}",
            'value': f"clarify:{missing_key}",
            'owner': 'user',
            'reason': 'Resolves the highest-priority missing decision before itinerary expansion.',
        })
    if risk_fallbacks:
        fallback_name = risk_fallbacks[0]['fallback']['nearest_viable_alternative']
        reply_options.append({
            'label': f"Use backup: {fallback_name}",
            'value': 'accept:fallback',
            'owner': 'user',
            'reason': 'Lets the plan degrade gracefully if the top anchor is closed, weather-mismatched, or over-constrained.',
        })
    if ctx.get('day_plan_continuity'):
        reply_options.append({
            'label': 'Expand timed day flow',
            'value': 'expand:day_flow',
            'owner': 'operator',
            'reason': 'Converts the continuity scaffold into timed morning, afternoon, and evening blocks.',
        })
    elif destination_comparison:
        reply_options.append({
            'label': f"Compare around {destination_comparison.get('recommended_option')}",
            'value': 'expand:comparison',
            'owner': 'operator',
            'reason': 'Turns the recommendation into a side-by-side user explanation with tradeoffs.',
        })
    if not reply_options:
        reply_options.append({
            'label': 'Build detailed itinerary',
            'value': 'expand:itinerary',
            'owner': 'operator',
            'reason': 'All core discovery fields are ready enough for itinerary expansion.',
        })
    reply_options = reply_options[:3]

    presentation_contract_check = {
        'audience': 'operator',
        'format': 'pre-send recommendation contract check',
        'recommended_focus': summary_subject,
        'status': 'hold' if finalization_blockers else 'ready',
        'checks': [
            {
                'check': 'decision_named',
                'pass': bool(summary_subject and decision_summary),
                'evidence': decision_summary,
                'if_missing': 'Name the recommended focus before sending the reply.',
            },
            {
                'check': 'why_evidence_visible',
                'pass': len(rationale) >= 1 and len(confidence_drivers) >= 1,
                'evidence': '; '.join((rationale[:1] + confidence_drivers[:1])[:2]),
                'if_missing': 'Include at least one rationale line and one structured evidence driver.',
            },
            {
                'check': 'watch_out_labeled',
                'pass': bool(risk_fallbacks or 'No major first-pass fallback warning' in markdown_sections[2]['body']),
                'evidence': markdown_sections[2]['body'],
                'if_missing': 'Add a watch-out or explicitly say no first-pass fallback warning was detected.',
            },
            {
                'check': 'next_owner_clear',
                'pass': next_step_prompt.get('audience') in {'user', 'operator'},
                'evidence': f"{next_step_prompt.get('audience')}: {next_step_prompt.get('prompt')}",
                'if_missing': 'Tag the next action with user or operator ownership.',
            },
            {
                'check': 'finality_guard_visible',
                'pass': finalization_gate.get('status') in {'blocked', 'ready'},
                'evidence': f"{finalization_gate.get('status')}: {finalization_gate.get('safe_presentation_mode')}",
                'if_missing': 'Show whether this is provisional or ready for final itinerary expansion.',
            },
        ],
        'copy_note': 'Before sending, verify the recommendation names the decision, shows evidence, labels watch-outs, assigns next ownership, and preserves the finality guard.',
    }

    readiness_criteria = [
        {
            'criterion': 'core_context_visible',
            'points': 20,
            'pass': bool(destination or destination_comparison) and bool(ctx.get('duration_days') or ctx.get('duration') or destination_comparison),
            'evidence': f"focus={summary_subject}; open_decisions={len(open_decisions)}",
        },
        {
            'criterion': 'recommendation_evidence_visible',
            'points': 25,
            'pass': len(rationale) >= 1 and len(confidence_drivers) >= 1,
            'evidence': confidence_drivers[0] if confidence_drivers else 'no structured evidence driver',
        },
        {
            'criterion': 'flow_or_decision_mode_visible',
            'points': 15,
            'pass': bool(ctx.get('day_plan_continuity') or destination_comparison or ctx.get('suggested_places')),
            'evidence': decision_badges[-1]['value'] if len(decision_badges) > 3 else 'planning snapshot only',
        },
        {
            'criterion': 'constraints_and_watchouts_labeled',
            'points': 20,
            'pass': bool(ctx.get('constraint_details') or risk_fallbacks or 'No major first-pass fallback warning' in markdown_sections[2]['body']),
            'evidence': markdown_sections[2]['body'],
        },
        {
            'criterion': 'next_owner_clear',
            'points': 20,
            'pass': next_step_prompt.get('audience') in {'user', 'operator'} and bool(next_step_prompt.get('prompt')),
            'evidence': f"{next_step_prompt.get('audience')}: {next_step_prompt.get('prompt')}",
        },
    ]
    readiness_score_value = sum(item['points'] for item in readiness_criteria if item['pass'])
    reply_readiness_score = {
        'audience': 'operator',
        'format': 'weighted reply readiness score',
        'score': readiness_score_value,
        'max_score': 100,
        'rating': 'hold' if finalization_blockers else 'ready' if readiness_score_value >= 85 else 'needs_work',
        'gate_status': finalization_gate['status'],
        'criteria': readiness_criteria,
        'next_improvement': finalization_gate['next_resolution'] if finalization_blockers else 'Proceed with itinerary expansion while preserving live availability caveats.',
    }

    meter_reasons = []
    if open_decisions:
        meter_reasons.append(f"user clarification needed: {open_decisions[0]}")
    if risk_fallbacks:
        meter_reasons.append(f"fallback warning active: {risk_fallbacks[0]['risk']}")
    if ctx.get('suggested_places') or destination_comparison:
        meter_reasons.append('offline recommendation requires live hours/transit/price validation')
    if ctx.get('day_plan_continuity'):
        meter_reasons.append('route scaffold requires live continuity validation before exact timing')
    if ctx.get('constraint_details'):
        meter_reasons.append('captured constraints must be preserved during expansion')
    if not meter_reasons:
        meter_reasons.append('no major first-pass blocker detected from structured output')

    if finalization_blockers:
        risk_level = 'high'
        traveler_send_mode = 'clarify_before_final'
        operator_action = finalization_gate['next_resolution']
    elif risk_fallbacks or ctx.get('suggested_places') or destination_comparison:
        risk_level = 'medium'
        traveler_send_mode = 'provisional_after_operator_validation'
        operator_action = 'Validate live hours, transit, prices, availability, and fallback fit before presenting as final.'
    else:
        risk_level = 'low'
        traveler_send_mode = 'ready_to_expand_with_standard_caveats'
        operator_action = 'Proceed with itinerary expansion while keeping normal live availability caveats visible.'

    decision_risk_meter = {
        'audience': 'operator',
        'format': 'compact risk/readiness meter',
        'risk_level': risk_level,
        'traveler_send_mode': traveler_send_mode,
        'finality_gate': finalization_gate['status'],
        'score': readiness_score_value,
        'max_score': 100,
        'reasons': meter_reasons[:5],
        'recommended_operator_action': operator_action,
        'copy_line': f"Risk: {risk_level}; send mode: {traveler_send_mode}; next: {operator_action}",
    }

    if open_decisions:
        send_decision = 'hold_and_ask'
        send_as = 'clarifying question'
        can_send_final = False
        primary_blocker = next_question or f"Clarify {open_decisions[0]}"
        hold_reason = 'Highest-priority user decision is still open; do not present a final itinerary yet.'
    elif risk_fallbacks:
        send_decision = 'send_provisional'
        send_as = 'provisional recommendation with fallback'
        can_send_final = False
        primary_blocker = risk_fallbacks[0]['warning']
        hold_reason = 'Fallback warning is active; send only as a provisional plan.'
    elif ctx.get('suggested_places') or destination_comparison:
        send_decision = 'send_provisional'
        send_as = 'provisional recommendation after live checks'
        can_send_final = False
        primary_blocker = f"Verify live hours, transit, pricing, and availability for {summary_subject}"
        hold_reason = 'Offline recommendation still needs operator live validation before it can be treated as final.'
    else:
        send_decision = 'send_ready'
        send_as = 'ready itinerary expansion'
        can_send_final = True
        primary_blocker = 'None'
        hold_reason = 'No first-pass send blocker; expand with standard live-availability caveats.'

    must_ask_or_include = []
    if open_decisions:
        must_ask_or_include.append(f"Ask: {next_question or f'Clarify {open_decisions[0]}'}")
    if risk_fallbacks:
        must_ask_or_include.append(
            f"Keep {risk_fallbacks[0]['fallback']['nearest_viable_alternative']} visible as fallback"
        )
    must_ask_or_include.append(
        f"Keep {summary_subject} labeled as {finalization_gate['safe_presentation_mode']}"
    )
    must_ask_or_include = must_ask_or_include[:3]

    if can_send_final:
        copy_prefix = 'OK to send.'
    else:
        copy_prefix = 'HOLD as final plan.'
    if send_as == 'clarifying question':
        copy_action = f"Send a clarifying question: {primary_blocker}"
    elif send_as == 'provisional recommendation with fallback':
        copy_action = (
            f"Send a provisional recommendation with fallback: "
            f"{risk_fallbacks[0]['fallback']['nearest_viable_alternative']}"
        )
    elif send_as == 'provisional recommendation after live checks':
        copy_action = f"Send a provisional recommendation after live checks for {summary_subject}."
    else:
        copy_action = f"Send the next itinerary expansion for {summary_subject}."
    if risk_fallbacks and not can_send_final:
        copy_tail = (
            f"Keep {summary_subject} labeled as a {finalization_gate['safe_presentation_mode']} "
            f"and {risk_fallbacks[0]['fallback']['nearest_viable_alternative']} visible as fallback."
        )
    else:
        copy_tail = f"Keep {summary_subject} labeled as a {finalization_gate['safe_presentation_mode']}."
    send_decision_card = {
        'audience': 'operator',
        'format': 'send/hold decision card',
        'recommended_focus': summary_subject,
        'decision': send_decision,
        'can_send_final': can_send_final,
        'send_as': send_as,
        'primary_blocker': primary_blocker,
        'must_ask_or_include': must_ask_or_include,
        'hold_reason': hold_reason,
        'copy_text': f"{copy_prefix} {copy_action} {copy_tail}",
    }

    if send_decision == 'hold_and_ask':
        examples = ''
        if clarification_prompt_card and clarification_prompt_card.get('answer_examples'):
            examples = f" Examples: {', '.join(clarification_prompt_card['answer_examples'][:3])}."
        message_text = (
            f"I'd treat {summary_subject} as the first-pass recommendation, but I need one answer before locking the plan. "
            f"{primary_blocker}{examples}"
        )
        outbound_status = 'send_question'
        send_now = True
        hold_outbound_until = 'none - send the clarifying question now'
        do_not_add = (
            f"Do not attach a timed itinerary or claim live hours, routes, prices, or final viability for {summary_subject}."
        )
    elif send_as == 'provisional recommendation with fallback':
        alt = risk_fallbacks[0]['fallback']['nearest_viable_alternative']
        message_text = (
            f"I'd treat {summary_subject} as a provisional first-pass recommendation. "
            f"If live checks fail, {alt} is the nearest backup. "
            f"{risk_fallbacks[0]['warning']}"
        )
        outbound_status = 'send_provisional'
        send_now = True
        hold_outbound_until = 'none - send the provisional recommendation now, but not a final itinerary'
        do_not_add = (
            f"Do not present {summary_subject} as a final timed itinerary; keep {alt} visible as fallback."
        )
    elif send_as == 'provisional recommendation after live checks':
        message_text = (
            f"I'd treat {summary_subject} as a provisional first-pass recommendation after live hours, transit, pricing, and availability checks. "
            f"{decision_summary}"
        )
        outbound_status = 'hold_outbound'
        send_now = False
        hold_outbound_until = (
            f"operator live-validates hours, transit, pricing, and availability for {summary_subject}"
        )
        do_not_add = (
            'Do not send this to the traveler until operator live checks pass; do not claim live viability.'
        )
    else:
        message_text = (
            f"I can expand {summary_subject} into the next itinerary pass with standard live-availability caveats. "
            f"{decision_summary}"
        )
        outbound_status = 'send_ready'
        send_now = True
        hold_outbound_until = 'none - send the next itinerary expansion with standard caveats'
        do_not_add = 'Do not hide standard live-availability caveats when expanding the itinerary.'

    outbound_send_packet = {
        'audience': 'operator',
        'format': 'copy-ready outbound send packet',
        'recommended_focus': summary_subject,
        'channel_form': send_as,
        'status': outbound_status,
        'send_now': send_now,
        'send_final_plan': can_send_final,
        'hold_outbound_until': hold_outbound_until,
        'message_text': message_text,
        'why_this_form': hold_reason,
        'do_not_add': do_not_add,
        'copy_text': message_text,
    }

    accepted_replies = [
        choice.get('reply_text') for choice in user_response_choices if choice.get('reply_text')
    ][:3]
    decision_labels = {
        'destination': 'the destination',
        'dates/duration': 'the dates or trip length',
        'travelers': 'the traveler count',
        'budget': 'the budget range',
        'interests': 'the top experiences',
        'accommodation': 'the stay type',
        'transport': 'the transport preference',
        'constraints': 'the remaining constraints',
    }
    if open_decisions:
        missing_key = open_decisions[0]
        missing_label = decision_labels.get(missing_key, missing_key)
        expected_reply_kind = 'clarification'
        waiting_on = 'user'
        if_answered = (
            f"Capture {missing_label}, keep {summary_subject} labeled as a "
            f"{finalization_gate['safe_presentation_mode']}"
        )
        if risk_fallbacks:
            if_answered += (
                f", and keep {risk_fallbacks[0]['fallback']['nearest_viable_alternative']} visible as fallback."
            )
        else:
            if_answered += '.'
        if_unclear = f"ask once more: {primary_blocker}"
    elif risk_fallbacks:
        alt = risk_fallbacks[0]['fallback']['nearest_viable_alternative']
        expected_reply_kind = 'fallback_confirmation'
        waiting_on = 'user'
        if_answered = (
            f"Keep {summary_subject} labeled as a {finalization_gate['safe_presentation_mode']} "
            f"and keep {alt} visible as fallback while operator live checks run."
        )
        if_unclear = f"ask whether to keep {alt} as the backup if live checks fail."
    elif outbound_status == 'hold_outbound':
        expected_reply_kind = 'operator_live_check'
        waiting_on = 'operator'
        if_answered = (
            f"After live hours, transit, pricing, and availability checks pass, "
            f"send a provisional recommendation for {summary_subject}."
        )
        if_unclear = (
            f"do not send to the traveler until operator live checks for {summary_subject} pass."
        )
    else:
        expected_reply_kind = 'expansion_go_ahead'
        waiting_on = 'user'
        if_answered = (
            f"Expand {summary_subject} into the next itinerary pass while keeping "
            f"standard live-availability caveats visible."
        )
        if_unclear = f"confirm the traveler wants a timed itinerary for {summary_subject} before expanding."
    accepts_text = ' / '.join(accepted_replies) if accepted_replies else 'a clear yes/no or the missing detail'
    reply_intake_card = {
        'audience': 'operator',
        'format': 'reply intake card',
        'recommended_focus': summary_subject,
        'waiting_on': waiting_on,
        'expected_reply_kind': expected_reply_kind,
        'accepts': accepted_replies,
        'if_answered': if_answered,
        'if_unclear': if_unclear[0].upper() + if_unclear[1:],
        'still_do_not': do_not_add,
        'copy_text': (
            f"When the traveler replies, accept {accepts_text}. {if_answered} "
            f"If unclear, {if_unclear} {do_not_add}"
        ),
    }

    if expected_reply_kind == 'clarification':
        fallback_clause = ''
        if risk_fallbacks:
            alt = risk_fallbacks[0]['fallback']['nearest_viable_alternative']
            fallback_clause = f"I'll also keep {alt} visible as fallback. "
        followup_form = 'acknowledgement plus remaining caveat'
        followup_status = 'send_ack_keep_provisional'
        followup_send_now = True
        followup_hold_until = 'none - send the acknowledgement now, still not a final itinerary'
        followup_message = (
            f"Thanks — I'll use your answer for {missing_label} and keep {summary_subject} as the first-pass recommendation. "
            f"{fallback_clause}"
            f"Next I'll confirm live hours, transit, pricing, and availability before a timed itinerary."
        )
        followup_next_check = (
            f"After capturing {missing_label}, run live hours, transit, pricing, and availability checks for {summary_subject}."
        )
        followup_do_not = (
            f"Do not treat the traveler's answer as permission to send a final timed itinerary for {summary_subject}."
        )
    elif expected_reply_kind == 'fallback_confirmation':
        alt = risk_fallbacks[0]['fallback']['nearest_viable_alternative']
        followup_form = 'acknowledgement plus fallback reminder'
        followup_status = 'send_ack_keep_fallback'
        followup_send_now = True
        followup_hold_until = 'none - send the acknowledgement now, still not a final itinerary'
        followup_message = (
            f"Thanks — I'll keep {summary_subject} as the first-pass recommendation and keep {alt} as the backup if live checks fail."
        )
        followup_next_check = (
            f"Keep {alt} visible while operator live-validates {summary_subject}."
        )
        followup_do_not = (
            f"Do not drop {alt} or present {summary_subject} as a final timed itinerary after the traveler confirms."
        )
    elif expected_reply_kind == 'operator_live_check':
        followup_form = 'operator-only hold'
        followup_status = 'hold_until_live_checks'
        followup_send_now = False
        followup_hold_until = (
            f"operator live-validates hours, transit, pricing, and availability for {summary_subject}"
        )
        followup_message = (
            f"Do not send a traveler follow-up yet. After live hours, transit, pricing, and availability checks pass, "
            f"send a provisional recommendation for {summary_subject}."
        )
        followup_next_check = (
            f"After live checks pass, send a provisional recommendation for {summary_subject}."
        )
        followup_do_not = (
            'Do not send this to the traveler until operator live checks pass; do not claim live viability.'
        )
    else:
        followup_form = 'itinerary expansion with caveats'
        followup_status = 'send_expansion_with_caveats'
        followup_send_now = True
        followup_hold_until = 'none - send the next itinerary expansion with standard caveats'
        followup_message = (
            f"I'll expand {summary_subject} into the next itinerary pass and keep standard live-availability caveats visible."
        )
        followup_next_check = (
            f"Expand {summary_subject} only after the traveler confirms they want a timed itinerary."
        )
        followup_do_not = 'Do not hide standard live-availability caveats when expanding the itinerary.'

    followup_send_packet = {
        'audience': 'operator',
        'format': 'copy-ready follow-up send packet',
        'recommended_focus': summary_subject,
        'trigger': f'traveler {expected_reply_kind} received',
        'channel_form': followup_form,
        'status': followup_status,
        'send_now_after_answer': followup_send_now,
        'send_final_plan': can_send_final,
        'hold_followup_until': followup_hold_until,
        'message_text': followup_message,
        'next_operator_check': followup_next_check,
        'still_do_not': followup_do_not,
        'copy_text': followup_message,
    }

    if expected_reply_kind == 'clarification':
        examples = ''
        if clarification_prompt_card and clarification_prompt_card.get('answer_examples'):
            examples = f" Examples: {', '.join(clarification_prompt_card['answer_examples'][:3])}."
        unclear_form = 'one more clarifying question'
        unclear_status = 'send_unclear_retry'
        unclear_send_now = True
        unclear_message = (
            f"I still need one clearer answer before I can lock the plan. {primary_blocker}{examples} "
            f"I'll keep {summary_subject} as the first-pass recommendation until then."
        )
        unclear_why = f"The inbound reply did not match {accepts_text}."
        unclear_do_not = (
            f"Do not treat an unclear reply as permission to send a final timed itinerary for {summary_subject}."
        )
    elif expected_reply_kind == 'fallback_confirmation':
        alt = risk_fallbacks[0]['fallback']['nearest_viable_alternative']
        unclear_form = 'one more fallback confirmation'
        unclear_status = 'send_unclear_retry'
        unclear_send_now = True
        unclear_message = (
            f"I still need a clearer yes or no on the backup. Should I keep {alt} as the fallback if live checks fail for {summary_subject}?"
        )
        unclear_why = f"The inbound reply did not clearly confirm or reject {alt} as fallback."
        unclear_do_not = (
            f"Do not drop {alt} or present {summary_subject} as a final timed itinerary after an unclear reply."
        )
    elif expected_reply_kind == 'operator_live_check':
        unclear_form = 'operator-only hold'
        unclear_status = 'hold_until_live_checks'
        unclear_send_now = False
        unclear_message = (
            f"Do not send a traveler follow-up yet. The last inbound reply was unclear, but this path is still waiting on operator live checks for {summary_subject}."
        )
        unclear_why = f"Unclear traveler text does not replace operator live validation for {summary_subject}."
        unclear_do_not = (
            'Do not send this to the traveler until operator live checks pass; do not claim live viability.'
        )
    else:
        unclear_form = 'one more expansion confirmation'
        unclear_status = 'send_unclear_retry'
        unclear_send_now = True
        unclear_message = (
            f"I still need a clearer go-ahead. Should I expand {summary_subject} into a timed itinerary with standard live-availability caveats?"
        )
        unclear_why = f"The inbound reply did not clearly confirm expansion for {summary_subject}."
        unclear_do_not = 'Do not hide standard live-availability caveats or expand from an unclear reply.'

    unclear_reply_packet = {
        'audience': 'operator',
        'format': 'copy-ready unclear-reply packet',
        'recommended_focus': summary_subject,
        'trigger': f'traveler {expected_reply_kind} is unclear',
        'channel_form': unclear_form,
        'status': unclear_status,
        'send_now': unclear_send_now,
        'send_final_plan': can_send_final,
        'message_text': unclear_message,
        'why_this_form': unclear_why,
        'still_do_not': unclear_do_not,
        'copy_text': unclear_message,
    }

    if_unclear_display = if_unclear[0].upper() + if_unclear[1:] if if_unclear else ''
    two_turn_send_script = {
        'audience': 'operator',
        'format': 'copy-ready two-turn send script',
        'recommended_focus': summary_subject,
        'send_final_plan': can_send_final,
        'turns': [
            {
                'turn': 1,
                'when': 'now',
                'status': outbound_status,
                'channel_form': send_as,
                'send_now': send_now,
                'message_text': message_text,
            },
            {
                'turn': 2,
                'when': f'after {expected_reply_kind}',
                'status': followup_status,
                'channel_form': followup_form,
                'send_now': followup_send_now,
                'message_text': followup_message,
            },
        ],
        'waiting_on': waiting_on,
        'expected_reply_kind': expected_reply_kind,
        'accepts': accepted_replies,
        'if_unclear': if_unclear_display,
        'unclear_turn': {
            'turn': '2-alt',
            'when': 'if traveler reply is unclear',
            'status': unclear_status,
            'channel_form': unclear_form,
            'send_now': unclear_send_now,
            'message_text': unclear_message,
        },
        'still_do_not': followup_do_not,
        'copy_text': (
            f"Turn 1 ({outbound_status}): {message_text} "
            f"Wait for {expected_reply_kind} from {waiting_on}; accept {accepts_text}. "
            f"Turn 2 ({followup_status}): {followup_message} "
            f"If unclear ({unclear_status}): {unclear_message} "
            f"{unclear_do_not}"
        ),
    }

    if expected_reply_kind == 'clarification':
        examples = ''
        if clarification_prompt_card and clarification_prompt_card.get('answer_examples'):
            examples = f" Examples: {', '.join(clarification_prompt_card['answer_examples'][:3])}."
        nudge_form = 'one reminder of the open question'
        nudge_status = 'send_no_reply_nudge'
        nudge_send_now_after_silence = True
        nudge_wait_until = 'traveler has been silent after the outbound question'
        nudge_message = (
            f"Just checking in — I still need one answer before locking the plan. {primary_blocker}{examples} "
            f"I'll keep {summary_subject} as the first-pass recommendation until then."
        )
        nudge_why = (
            f"No traveler reply yet for {expected_reply_kind}; restating the open question is safer than expanding."
        )
        nudge_do_not = (
            f"Do not treat silence as permission to send a final timed itinerary for {summary_subject}."
        )
    elif expected_reply_kind == 'fallback_confirmation':
        alt = risk_fallbacks[0]['fallback']['nearest_viable_alternative']
        nudge_form = 'one reminder of the fallback question'
        nudge_status = 'send_no_reply_nudge'
        nudge_send_now_after_silence = True
        nudge_wait_until = 'traveler has been silent after the fallback confirmation question'
        nudge_message = (
            f"Just checking in — I still need a yes or no on the backup. "
            f"Should I keep {alt} as the fallback if live checks fail for {summary_subject}?"
        )
        nudge_why = f"No traveler reply yet for fallback confirmation of {alt}."
        nudge_do_not = (
            f"Do not drop {alt} or present {summary_subject} as a final timed itinerary after silence."
        )
    elif expected_reply_kind == 'operator_live_check':
        nudge_form = 'operator-only hold'
        nudge_status = 'hold_until_live_checks'
        nudge_send_now_after_silence = False
        nudge_wait_until = (
            f"operator live-validates hours, transit, pricing, and availability for {summary_subject}"
        )
        nudge_message = (
            f"Do not nudge the traveler. Silence does not replace operator live checks for {summary_subject}."
        )
        nudge_why = f"This path is waiting on operator live validation, not a traveler reply."
        nudge_do_not = (
            'Do not send this to the traveler until operator live checks pass; do not claim live viability.'
        )
    else:
        nudge_form = 'one reminder of the expansion question'
        nudge_status = 'send_no_reply_nudge'
        nudge_send_now_after_silence = True
        nudge_wait_until = 'traveler has been silent after the expansion confirmation'
        nudge_message = (
            f"Just checking in — should I expand {summary_subject} into a timed itinerary with standard live-availability caveats?"
        )
        nudge_why = f"No traveler reply yet confirming expansion for {summary_subject}."
        nudge_do_not = 'Do not hide standard live-availability caveats or expand from silence.'

    no_reply_nudge_packet = {
        'audience': 'operator',
        'format': 'copy-ready no-reply nudge packet',
        'recommended_focus': summary_subject,
        'trigger': f'traveler {expected_reply_kind} is still missing',
        'channel_form': nudge_form,
        'status': nudge_status,
        'send_now_after_silence': nudge_send_now_after_silence,
        'send_final_plan': can_send_final,
        'wait_until': nudge_wait_until,
        'message_text': nudge_message,
        'why_this_form': nudge_why,
        'still_do_not': nudge_do_not,
        'copy_text': nudge_message,
    }

    if nudge_status == 'send_no_reply_nudge':
        post_hold_form = 'operator-only hold after one reminder'
        post_hold_status = 'hold_after_nudge'
        post_hold_send_now = False
        post_hold_trigger = 'traveler still silent after one reminder'
        post_hold_wait_until = 'traveler replies after the one reminder, or operator live-validates internally'
        post_hold_message = (
            f"Do not send another traveler reminder. After the one nudge, wait for a reply or run live checks internally for {summary_subject}."
        )
        post_hold_why = (
            f"A second reminder would nag; continued silence still does not unlock a final itinerary for {summary_subject}."
        )
        post_hold_next_check = (
            f"If the traveler stays silent after the nudge, keep {summary_subject} labeled as a first-pass recommendation and wait or live-validate internally."
        )
        post_hold_do_not = (
            f"Do not send a second reminder or treat continued silence as permission to send a final timed itinerary for {summary_subject}."
        )
    else:
        post_hold_form = 'operator-only hold'
        post_hold_status = 'hold_until_live_checks'
        post_hold_send_now = False
        post_hold_trigger = 'no traveler reminder on this operator-live-check path'
        post_hold_wait_until = nudge_wait_until
        post_hold_message = (
            f"Do not send a traveler reminder. This path is still waiting on operator live checks for {summary_subject}."
        )
        post_hold_why = (
            f"There is no traveler nudge on this path; silence does not replace operator live validation for {summary_subject}."
        )
        post_hold_next_check = (
            f"Complete live hours, transit, pricing, and availability checks for {summary_subject} before any traveler send."
        )
        post_hold_do_not = (
            'Do not send this to the traveler until operator live checks pass; do not claim live viability.'
        )

    post_nudge_hold_packet = {
        'audience': 'operator',
        'format': 'copy-ready post-nudge hold packet',
        'recommended_focus': summary_subject,
        'trigger': post_hold_trigger,
        'channel_form': post_hold_form,
        'status': post_hold_status,
        'send_now': post_hold_send_now,
        'send_final_plan': can_send_final,
        'wait_until': post_hold_wait_until,
        'message_text': post_hold_message,
        'why_this_form': post_hold_why,
        'next_operator_check': post_hold_next_check,
        'still_do_not': post_hold_do_not,
        'copy_text': post_hold_message,
    }

    return {
        'compact_sections': sections,
        'decision_summary': decision_summary,
        'decision_rationale': rationale[:3],
        'confidence_drivers': confidence_drivers[:5],
        'status_line': status_line,
        'next_step_actions': actions[:4],
        'next_action_checklist': checklist[:4],
        'next_step_prompt': next_step_prompt,
        'clarification_prompt_card': clarification_prompt_card,
        'action_plan': action_plan,
        'decision_badges': decision_badges,
        'handoff_brief': handoff_brief,
        'quick_reply_card': quick_reply_card,
        'operator_preflight_card': operator_preflight_card,
        'final_reply_preview': final_reply_preview,
        'validation_summary': validation_summary,
        'operator_review_queue': operator_review_queue,
        'constraint_compliance_card': constraint_compliance_card,
        'itinerary_expansion_brief': itinerary_expansion_brief,
        'finalization_gate': finalization_gate,
        'live_validation_prompt_pack': live_validation_prompt_pack,
        'assumption_ledger': {
            'purpose': 'operator-visible list of provisional assumptions to label before presenting or expanding the plan',
            'items': assumption_ledger,
        },
        'shareable_summary': shareable_summary,
        'decision_snapshot_table': decision_snapshot_table,
        'evidence_trace_card': evidence_trace_card,
        'traveler_facing_draft': traveler_facing_draft,
        'operator_digest': operator_digest,
        'reply_options': reply_options,
        'user_response_choices': user_response_choices,
        'presentation_contract_check': presentation_contract_check,
        'reply_readiness_score': reply_readiness_score,
        'decision_risk_meter': decision_risk_meter,
        'send_decision_card': send_decision_card,
        'outbound_send_packet': outbound_send_packet,
        'reply_intake_card': reply_intake_card,
        'followup_send_packet': followup_send_packet,
        'unclear_reply_packet': unclear_reply_packet,
        'two_turn_send_script': two_turn_send_script,
        'no_reply_nudge_packet': no_reply_nudge_packet,
        'post_nudge_hold_packet': post_nudge_hold_packet,
        'presentation_markdown': {
            'format': 'compact markdown draft',
            'sections': markdown_sections,
            'text': presentation_markdown,
            'tone': 'scannable, decisive, and clear about the next action',
        },
        'response_template': {
            'format': 'four-line operator draft',
            'lines': template_lines,
            'tone': 'concise, evidence-led, and action-oriented',
        },
    }

def build_risk_fallbacks(query, dest, dest_data, duration, travelers, budget, constraint_details, suggested_places, day_plan_continuity):
    """Emit graceful risk warnings plus nearest viable alternatives.

    This keeps Phase D additive: the planner still returns the current context,
    suggested places, and continuity scaffold, then appends operator-visible
    fallbacks for common failure modes that would otherwise produce brittle plans.
    """
    risks = []
    t = query.lower()
    dest_name = dest_data.get('name') if dest_data else dest
    place_meta = place_planning_metadata(dest_name)

    def add(kind, trigger, warning, alternative, rationale, action, severity='warning'):
        risks.append({
            'risk': kind,
            'severity': severity,
            'trigger': trigger,
            'warning': warning,
            'fallback': {
                'nearest_viable_alternative': alternative,
                'rationale': rationale,
                'action': action,
            }
        })

    # Closed venues / hours sensitivity: do not drop the chosen place; provide the
    # next ranked nearby/shortlist alternative to swap in during live validation.
    if constraint_details.get('opening_hours_sensitivity') and suggested_places:
        anchor = suggested_places[0]['name']
        anchor_zone = place_meta.get(anchor, {}).get('zone')
        alternative = None
        for place in suggested_places[1:]:
            name = place['name']
            if anchor_zone and place_meta.get(name, {}).get('zone') == anchor_zone:
                alternative = name
                break
        if not alternative and len(suggested_places) > 1:
            alternative = suggested_places[1]['name']
        if alternative:
            add(
                'closed_venue',
                'opening-hours sensitivity requested',
                f'Verify live opening hours for {anchor} before locking the itinerary.',
                alternative,
                'Uses the next best ranked highlight from the same destination shortlist, preferring the same zone when available.',
                f'If {anchor} is closed or poorly timed, swap in {alternative} before changing the broader day plan.'
            )

    # Weather mismatch: flag outdoor anchors when the traveler asks for rain,
    # heat, or cold protection and point to the closest indoor/both-setting option.
    weather_flags = constraint_details.get('weather_sensitivity') or []
    if weather_flags and suggested_places:
        selected_names = []
        if day_plan_continuity:
            selected_names = [segment['place'] for segment in day_plan_continuity.get('segments', [])]
        selected_names = selected_names or [place['name'] for place in suggested_places[:3]]
        outdoor_anchor = next((name for name in selected_names if place_meta.get(name, {}).get('setting') == 'outdoor'), None)
        weather_alternative = next(
            (place['name'] for place in suggested_places
             if place['name'] != outdoor_anchor and place_meta.get(place['name'], {}).get('setting') in {'indoor', 'both'}),
            None
        )
        if outdoor_anchor and weather_alternative:
            add(
                'weather_mismatch',
                ', '.join(weather_flags),
                f'{outdoor_anchor} is an outdoor-leaning anchor and may not fit the stated weather sensitivity.',
                weather_alternative,
                'Indoor or mixed-setting highlight from the ranked shortlist keeps the plan viable without changing destination.',
                f'Use {weather_alternative} as the nearest weather-safe backup if conditions make {outdoor_anchor} unpleasant.'
            )

    # Sparse-area handling: when the named destination is outside bundled data,
    # keep the user intent visible and suggest a nearby planning base rather than
    # failing with an empty shortlist.
    if dest and not dest_data:
        sparse_alternatives = {
            'hakone': 'Tokyo',
            'nara': 'Kyoto',
            'asakusa': 'Tokyo',
            'gion': 'Kyoto',
            'versailles': 'Paris',
            'fontainebleau': 'Paris',
        }
        dest_key = dest.lower()
        alternative = next((value for key, value in sparse_alternatives.items() if key in dest_key or key in t), None)
        if not alternative:
            if 'japan' in t:
                alternative = 'Tokyo'
            elif 'france' in t:
                alternative = 'Paris'
            else:
                alternative = 'nearest bundled major destination'
        add(
            'sparse_area',
            'destination not found in bundled reference data',
            f'{dest} is not in the offline destination reference, so highlights and routing confidence are limited.',
            alternative,
            'Nearest viable bundled planning base preserves the request while giving the planner enough reference data to continue.',
            f'Plan from {alternative} as the fallback base, then treat {dest} as an optional side-trip pending live validation.',
            severity='notice'
        )

    # Over-constrained plans: catch caps that are below the bundled budget floor
    # and suggest a concrete adjustment instead of emitting a brittle itinerary.
    cap = budget.get('cap') if isinstance(budget, dict) else None
    if dest_data and cap and duration:
        costs = dest_data.get('avg_daily_cost_usd', {})
        floor_daily = costs.get('budget') or costs.get('mid')
        traveler_count = travelers or 1
        if floor_daily and cap.get('currency') == 'USD':
            budget_floor = floor_daily * duration * traveler_count
            amount = cap.get('amount')
            if amount and amount < budget_floor:
                affordable_days = max(1, int(amount // (floor_daily * traveler_count))) if floor_daily * traveler_count else 1
                alternative = f'{affordable_days}-day budget plan in {dest_data["name"]}'
                add(
                    'over_constrained_plan',
                    'budget cap below offline budget floor',
                    f'The stated USD {amount} cap is below the bundled budget estimate of about USD {budget_floor} for {duration} days and {traveler_count} traveler(s).',
                    alternative,
                    'Shortening the trip is the nearest viable adjustment that preserves destination and traveler count.',
                    f'Use {alternative} or raise the cap before finalizing paid activities and accommodation.'
                )

    return risks

dest = extract_destination(query)
duration = extract_duration(query)
travelers = extract_travelers(query)
budget = extract_budget(query)
interests = extract_interests(query)
constraint_details, constraint_summary = extract_constraints(query)
compare_options = extract_compare_options(query)
travel_months = extract_travel_months(query)
if compare_options:
    # Comparison requests name multiple candidate destinations; avoid treating
    # timing phrases like "in December" as a single selected destination.
    dest = ""

ctx = {}

# Look up destination in references
dest_data = None
dests = []
if os.path.isfile(dest_file):
    with open(dest_file) as f:
        dests = json.load(f)
if dest and dests:
    dest_data = find_destination_record(dest, dests)

if dest_data:
    ctx['destination'] = {
        'name': dest_data['name'],
        'country': dest_data['country'],
        'coordinates': dest_data['coordinates'],
        'currency': dest_data['currency'],
        'timezone': dest_data['timezone'],
        'avg_daily_cost_usd': dest_data['avg_daily_cost_usd']
    }
elif dest:
    ctx['destination'] = {'name': dest}

if duration:
    ctx['duration_days'] = duration
if travelers:
    ctx['travelers'] = {'adults': travelers}
if budget:
    ctx['budget'] = budget
    budget_tier = budget.get('tier')
    if dest_data and budget_tier:
        costs = dest_data.get('avg_daily_cost_usd', {})
        daily = costs.get(budget_tier, costs.get('mid'))
        if daily and duration:
            ctx['budget']['estimated_total'] = daily * duration * (travelers or 1)
            ctx['budget']['daily_per_person'] = daily
if interests:
    ctx['interests'] = interests
if constraint_summary:
    ctx['constraints'] = constraint_summary
if constraint_details:
    ctx['constraint_details'] = constraint_details

suggested_places = build_scoring_explanations(dest_data, interests, budget, constraint_details)
day_plan_continuity = None
if suggested_places:
    ctx['suggested_places'] = suggested_places
    day_plan_continuity = build_day_plan_continuity(dest_data, suggested_places, constraint_details)
    if day_plan_continuity:
        ctx['day_plan_continuity'] = day_plan_continuity

destination_comparison = build_destination_comparison(compare_options, dests, budget, interests, constraint_details, travel_months)
if destination_comparison:
    ctx['destination_comparison'] = destination_comparison

risk_fallbacks = build_risk_fallbacks(query, dest, dest_data, duration, travelers, budget, constraint_details, suggested_places, day_plan_continuity)
if risk_fallbacks:
    ctx['risk_fallbacks'] = risk_fallbacks

dims_complete = sum(1 for v in [dest, duration, travelers, budget, interests, constraint_summary] if v)
if dims_complete >= 6:
    ctx['planning_stage'] = 'refine'
elif dims_complete >= 4:
    ctx['planning_stage'] = 'develop'
else:
    ctx['planning_stage'] = 'discover'

ctx['open_decisions'] = []
if not dest: ctx['open_decisions'].append('destination')
if not duration: ctx['open_decisions'].append('dates/duration')
if not travelers: ctx['open_decisions'].append('travelers')
if not budget: ctx['open_decisions'].append('budget')
if not interests: ctx['open_decisions'].append('interests')
ctx['open_decisions'].extend(['accommodation', 'transport'])
if not constraint_summary: ctx['open_decisions'].append('constraints')

output_polish = build_output_polish(ctx, dest_data, destination_comparison, risk_fallbacks)
if output_polish:
    ctx['output_polish'] = output_polish

print(json.dumps(ctx, indent=2))
PYEOF

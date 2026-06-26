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

    primary_place = None
    if ctx.get('suggested_places'):
        primary_place = ctx['suggested_places'][0].get('name')
    elif destination_comparison:
        primary_place = destination_comparison.get('recommended_option')
    elif destination:
        primary_place = destination.get('name')

    next_question = None
    if open_decisions:
        labels = {
            'destination': 'Which destination should I optimize for first?',
            'dates/duration': 'What dates or trip length should I plan around?',
            'travelers': 'How many people are traveling?',
            'budget': 'What budget range should I optimize for?',
            'interests': 'Which experiences matter most for this trip?',
            'accommodation': 'What type of stay should I assume?',
            'transport': 'Should I prioritize walking, public transit, taxis, trains, or rental car?',
            'constraints': 'Any pace, dietary, accessibility, weather, or opening-hours constraints I should honor?',
        }
        next_question = labels.get(open_decisions[0], f'Can you clarify {open_decisions[0]}?')

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

    return {
        'compact_sections': sections,
        'decision_summary': decision_summary,
        'decision_rationale': rationale[:3],
        'next_step_actions': actions[:4],
        'next_action_checklist': checklist[:4],
        'next_step_prompt': next_step_prompt,
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

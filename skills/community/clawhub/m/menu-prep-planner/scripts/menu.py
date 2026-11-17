#!/usr/bin/env python3
"""Offline quantity aggregation and exclusive-resource conflicts; reads JSON, prints JSON."""
import argparse
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import json
import sys

UNITS = {'g': ('g', '1'), 'kg': ('g', '1000'), 'ml': ('ml', '1'), 'l': ('ml', '1000'),
         'tsp_us': ('ml', '4.92892159375'), 'tbsp_us': ('ml', '14.78676478125'),
         'cup_us': ('ml', '236.5882365'), 'each': ('each', '1')}

def need(condition, message):
    if not condition:
        raise ValueError(message)

def number(value):
    need(type(value) in (str, int), 'quantities must be decimal strings or integers')
    try:
        result = Decimal(value)
    except InvalidOperation:
        raise ValueError('invalid decimal') from None
    need(result.is_finite() and result >= 0, 'quantity must be finite and nonnegative')
    return result

def ident(value):
    need(isinstance(value, str) and bool(value.strip()), 'nonempty id required')
    return value

def amount(item):
    unit = item.get('unit')
    need(unit in UNITS, 'unsupported/ambiguous unit; normalize explicitly')
    base, factor = UNITS[unit]
    # preparation includes all material distinctions (e.g. chopped/whole/salted).
    key = (ident(item.get('ingredient_id')), ident(item.get('preparation')), base)
    return key, number(item.get('quantity')) * Decimal(factor)

def instant(value):
    need(isinstance(value, str), 'timestamp string required')
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise ValueError('invalid timestamp') from None
    need(result.tzinfo is not None and result.utcoffset() is not None, 'explicit UTC offset required')
    return result.astimezone(timezone.utc)

def report(data):
    need(isinstance(data, dict) and data.get('schema_version') == 1 and type(data.get('schema_version')) is int, 'schema_version 1 required')
    target = number(data.get('target_servings')); need(target > 0, 'target_servings must be positive')
    recipes = data.get('recipes'); need(isinstance(recipes, list), 'recipes must be list')
    totals, unknown, ids = {}, [], set()
    for recipe in recipes:
        need(isinstance(recipe, dict), 'recipe must be object')
        rid = ident(recipe.get('id')); need(rid not in ids, 'duplicate recipe id'); ids.add(rid)
        servings = number(recipe.get('base_servings')); need(servings > 0, 'base_servings must be positive')
        # Optional recipe-level target supports dishes intended for only part of the party.
        dish_target = number(recipe.get('target_servings', data['target_servings']))
        ingredients = recipe.get('ingredients'); need(isinstance(ingredients, list), 'ingredients must be list')
        for item in ingredients:
            need(isinstance(item, dict), 'ingredient must be object')
            if item.get('quantity') is None:
                unknown.append({'recipe_id': rid, 'ingredient_id': ident(item.get('ingredient_id'))}); continue
            key, qty = amount(item)
            totals[key] = totals.get(key, Decimal(0)) + qty * dish_target / servings
    pantry = {}
    need(isinstance(data.get('pantry', []), list), 'pantry must be list')
    for item in data.get('pantry', []):
        need(isinstance(item, dict), 'pantry item must be object')
        key, qty = amount(item)
        # Reservations use the same input unit as pantry quantity.
        reserved = number(item.get('reserved', '0')) * Decimal(UNITS[item['unit']][1])
        need(reserved <= qty, 'pantry reservation exceeds stock')
        pantry[key] = pantry.get(key, Decimal(0)) + qty - reserved
    shopping = [{'ingredient_id': k[0], 'preparation': k[1], 'unit': k[2], 'required': str(q),
                 'available': str(pantry.get(k, Decimal(0))),
                 'buy': str(max(Decimal(0), q - pantry.get(k, Decimal(0))))} for k,q in sorted(totals.items())]
    bookings = data.get('bookings', []); need(isinstance(bookings, list), 'bookings must be list')
    windows, ids = [], set()
    for b in bookings:
        need(isinstance(b, dict), 'booking must be object')
        bid = ident(b.get('id')); need(bid not in ids, 'duplicate booking id'); ids.add(bid)
        resource = ident(b.get('resource'))
        start, end = instant(b.get('start')), instant(b.get('end'))
        need(start < end, 'booking end must follow start')
        windows.append((bid, resource, start, end))
    conflicts = []
    for i,a in enumerate(windows):
        for b in windows[i+1:]:
            if a[1] == b[1] and max(a[2],b[2]) < min(a[3],b[3]):
                conflicts.append({'resource': a[1], 'booking_ids': [a[0],b[0]]})
    return {'shopping': shopping, 'unquantified': unknown, 'resource_conflicts': conflicts,
            'scope': 'arithmetic and exclusive bookings only; not food safety or schedule optimization'}

def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('input'); args=parser.parse_args()
    try:
        with open(args.input, encoding='utf-8') as f: result=report(json.load(f))
    except (OSError, ValueError, TypeError, KeyError) as e:
        print('Invalid input: '+str(e), file=sys.stderr); return 2
    print(json.dumps(result, indent=2)); return 0

if __name__ == '__main__':
    sys.exit(main())

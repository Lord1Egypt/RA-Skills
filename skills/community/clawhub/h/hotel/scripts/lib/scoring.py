#!/usr/bin/env python3

def score_hotel(hotel, trip=None, preferences=None):
    score = 50
    preferences = preferences or {}

    nightly_price = hotel.get("nightly_price")
    budget_total = trip.get("budget_total") if trip else None
    nights = trip.get("nights") if trip else None

    if nightly_price is not None and budget_total and nights:
        estimated_total = nightly_price * nights
        if estimated_total <= budget_total:
            score += 15
        else:
            score -= 15

    if hotel.get("refund_policy") == "flexible":
        score += 8

    amenities = set(hotel.get("amenities", []))
    if preferences.get("breakfast") == "required" and "breakfast" in amenities:
        score += 10
    if preferences.get("wifi") == "required" and "wifi" in amenities:
        score += 8
    if preferences.get("gym") == "required" and "gym" in amenities:
        score += 5

    if hotel.get("area"):
        score += 4

    if hotel.get("walkability") == "high":
        score += 6

    if hotel.get("notes"):
        score += 2

    return score

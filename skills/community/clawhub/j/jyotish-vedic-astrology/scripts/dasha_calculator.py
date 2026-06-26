#!/usr/bin/env python3
"""
Vedic Astrology Dasha Period Calculator
计算印度占星大运周期

This script helps calculate Dasha periods based on Nakshatra position.
"""

# Standard Vimshottari Dasha periods in years
VIMSHOTTARI_PERIODS = {
    'Ketu': 7,
    'Venus': 20,
    'Sun': 6,
    'Moon': 10,
    'Mars': 7,
    'Rahu': 18,
    'Jupiter': 16,
    'Saturn': 19,
    'Mercury': 17
}

# Planetary order in Vimshottari Dasha
DASHA_ORDER = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']

def calculate_mahadasha(birth_nakshatra):
    """
    Calculate starting Mahadasha based on Moon's Nakshatra at birth

    Args:
        birth_nakshatra: Nakshatra where Moon was at birth (1-27)

    Returns:
        Dict with starting Mahadasha lord and remaining years in that period
    """
    nakshatra_num = birth_nakshatra

    # Map Nakshatra to starting planet
    # Ashwini (1), Magha (10), Mula (19) -> Ketu
    # Bharani (2), Purva Phalguni (11), Purva Ashadha (20) -> Venus
    # Krittika (3), Uttara Phalguni (12), Uttara Ashadha (21) -> Sun
    # Rohini (4), Hasta (13), Shravana (22) -> Moon
    # Mrigashira (5), Chitra (14), Dhanishta (23) -> Mars
    # Ardra (6), Swati (15), Shatabhisha (24) -> Rahu
    # Punarvasu (7), Vishakha (16), Purva Bhadrapada (25) -> Jupiter
    # Pushya (8), Anuradha (17), Uttara Bhadrapada (26) -> Saturn
    # Ashlesha (9), Jyeshtha (18), Revati (27) -> Mercury

    # Find remainder when nakshatra number is divided by 9
    remainder = nakshatra_num % 9
    if remainder == 0:
        remainder = 9

    # Get the starting Dasha lord
    starting_planet_index = remainder - 1  # Convert to 0-indexed
    starting_planet = DASHA_ORDER[starting_planet_index]

    # Calculate remaining years in first Mahadasha
    total_years = VIMSHOTTARI_PERIODS[starting_planet]
    nakshatra_pada = ((nakshatra_num - 1) % 4) + 1  # Get pada (1-4)

    # Each pada = 1/4 of the period (approximately)
    # For precise calculation, need Moon's degree within Nakshatra
    remaining_years = total_years - (nakshatra_pada - 1) * (total_years / 4)

    return {
        'starting_mahadasha': starting_planet,
        'total_years': total_years,
        'remaining_years': remaining_years,
        'starting_age': remaining_years - total_years  # Should be negative
    }


def get_mahadasha_sequence(starting_planet):
    """
    Get the complete Mahadasha sequence starting from given planet

    Args:
        starting_planet: Planet that starts the sequence

    Returns:
        List of tuples (planet, years) in sequence
    """
    sequence = []

    # Find starting index
    start_index = DASHA_ORDER.index(starting_planet)

    # Build sequence (120 years total)
    for i in range(9):  # 9 planets
        planet_index = (start_index + i) % 9
        planet = DASHA_ORDER[planet_index]
        years = VIMSHOTTARI_PERIODS[planet]
        sequence.append((planet, years))

    return sequence


def calculate_bhukti(mahadasha_planet, years_into_mahadasha):
    """
    Calculate current Bhukti (sub-period) within Mahadasha

    Correct formula: Antar_Years = Mahadasha_Years × Antar_Planet_Years / 120

    Args:
        mahadasha_planet: Current Mahadasha lord
        years_into_mahadasha: Years elapsed in current Mahadasha

    Returns:
        Dict with current Bhukti and remaining years
    """
    mahadasha_total = VIMSHOTTARI_PERIODS[mahadasha_planet]
    sequence = get_mahadasha_sequence(mahadasha_planet)

    years_remaining = years_into_mahadasha

    for planet, planet_full_years in sequence:
        # Scale Antar period to Mahadasha duration
        bhukti_years = mahadasha_total * planet_full_years / 120.0
        if years_remaining <= bhukti_years:
            return {
                'bhukti_lord': planet,
                'bhukti_years': bhukti_years,
                'years_into_bhukti': years_remaining,
                'years_remaining': bhukti_years - years_remaining,
                'bhukti_percentage': (years_remaining / bhukti_years) * 100
            }
        years_remaining -= bhukti_years

    return None


def calculate_pratyantar_dasha(mahadasha_planet, bhukti_planet, years_into_bhukti):
    """
    Calculate Pratyantar Dasha (sub-sub-period)

    Correct formula: PA_Years = Antar_Years × PA_Planet_Years / 120
    where Antar_Years = Maha_Years × Antar_Planet_Years / 120
    """
    mahadasha_years = VIMSHOTTARI_PERIODS[mahadasha_planet]
    bhukti_years = mahadasha_years * VIMSHOTTARI_PERIODS[bhukti_planet] / 120.0

    sequence = get_mahadasha_sequence(mahadasha_planet)

    pratyantar_sequence = []
    for planet, _ in sequence:
        pratyantar_years = bhukti_years * VIMSHOTTARI_PERIODS[planet] / 120.0
        pratyantar_sequence.append((planet, pratyantar_years))

    return pratyantar_sequence


def get_current_dasha_period(birth_nakshatra, current_age):
    """
    Get complete current Dasha hierarchy (Mahadasha, Bhukti, Pratyantar)

    Args:
        birth_nakshatra: Moon's Nakshatra at birth (1-27)
        current_age: Current age of native

    Returns:
        Dict with complete Dasha hierarchy
    """
    # Calculate starting Mahadasha
    start_info = calculate_mahadasha(birth_nakshatra)

    # Find current Mahadasha
    sequence = get_mahadasha_sequence(start_info['starting_mahadasha'])
    years_elapsed = current_age

    current_mahadasha = None
    years_in_mahadasha = 0

    for planet, years in sequence:
        if years_elapsed <= years:
            current_mahadasha = planet
            years_in_mahadasha = years_elapsed
            break
        years_elapsed -= years

    if not current_mahadasha:
        return None

    # Calculate Bhukti
    bhukti_info = calculate_bhukti(current_mahadasha, years_in_mahadasha)

    # Calculate Pratyantar Dasha
    if bhukti_info:
        pratyantar_sequence = calculate_pratyantar_dasha(
            current_mahadasha,
            bhukti_info['bhukti_lord'],
            bhukti_info['years_into_bhukti']
        )

        # Find current Pratyantar
        years_in_bhukti = bhukti_info['years_into_bhukti']
        current_pratyantar = None

        for planet, years in pratyantar_sequence:
            if years_in_bhukti <= years:
                current_pratyantar = planet
                break
            years_in_bhukti -= years
    else:
        current_pratyantar = None
        pratyantar_sequence = []

    return {
        'mahadasha': {
            'lord': current_mahadasha,
            'years_into_period': years_in_mahadasha,
            'total_years': VIMSHOTTARI_PERIODS[current_mahadasha]
        },
        'bhukti': bhukti_info,
        'pratyantar': {
            'lord': current_pratyantar,
            'sequence': pratyantar_sequence
        }
    }


def print_dasha_summary(birth_nakshatra, current_age):
    """
    Print a formatted summary of current Dasha period
    """
    current_dasha = get_current_dasha_period(birth_nakshatra, current_age)

    if not current_dasha:
        print("Error: Unable to calculate Dasha period")
        return

    print("=" * 60)
    print("CURRENT DASHA PERIOD")
    print("=" * 60)
    print(f"Moon Nakshatra at Birth: {birth_nakshatra}")
    print(f"Current Age: {current_age} years")
    print("-" * 60)

    # Mahadasha
    md = current_dasha['mahadasha']
    print(f"Mahadasha: {md['lord']} (Lord)")
    print(f"  Years into period: {md['years_into_period']:.2f} / {md['total_years']}")
    print(f"  Percentage: {(md['years_into_period'] / md['total_years']) * 100:.1f}%")

    # Bhukti
    bk = current_dasha['bhukti']
    if bk:
        print(f"\nBhukti (Sub-period): {bk['bhukti_lord']} (Lord)")
        print(f"  Years into Bhukti: {bk['years_into_bhukti']:.2f} / {bk['bhukti_years']}")
        print(f"  Percentage: {bk['bhukti_percentage']:.1f}%")

    # Pratyantar
    pr = current_dasha['pratyantar']
    if pr['lord']:
        print(f"\nPratyantar (Sub-sub-period): {pr['lord']} (Lord)")

    print("=" * 60)


# Example usage
if __name__ == "__main__":
    # Example: Moon in 3rd Nakshatra (Krittika) at birth, native is 35 years old
    print("Example: Moon in Krittika (Nakshatra 3), Age 35")
    print_dasha_summary(birth_nakshatra=3, current_age=35)

    print("\n\n")

    # Example: Moon in 14th Nakshatra (Chitra) at birth, native is 42 years old
    print("Example: Moon in Chitra (Nakshatra 14), Age 42")
    print_dasha_summary(birth_nakshatra=14, current_age=42)

#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup


def looks_pregame(text: str) -> bool:
    low = text.lower()
    # Filter out obvious live/in-progress markers.
    if any(x in low for x in ['p1 ', 'p2 ', 'p3 ', 'ot ', 'final', 'last play:', 'live details']):
        return False
    # Keep likely scheduled cards with time markers.
    return any(x in text for x in ['AM ET', 'PM ET', 'AM', 'PM']) or 'Matchup' in text


def extract_card(card):
    text = ' | '.join(card.stripped_strings)
    if not looks_pregame(text):
        return None

    teams = []
    # team rows usually contain short team names in visible text; grab capitalized words around score-like structure.
    for piece in card.stripped_strings:
        p = piece.strip()
        if re.fullmatch(r'[A-Za-z][A-Za-z .&\-]{1,30}', p) and p.lower() not in {
            'line movements', 'moneyline', 'total', 'puckline', 'notes', 'matchup', 'picks'
        }:
            teams.append(p)
    teams = [t for t in teams if not re.fullmatch(r'\d+(?:-\d+)?', t)]

    # de-dup while preserving order
    dedup = []
    for t in teams:
        if t not in dedup:
            dedup.append(t)
    teams = dedup[:2]
    if len(teams) < 2:
        return None

    ml_cells = [c.get_text(' ', strip=True) for c in card.select('td[data-field="live-moneyline"], td[data-field="current-moneyline"]')]
    total_cells = [c.get_text(' ', strip=True) for c in card.select('td[data-field="live-total"], td[data-field="current-total"]')]
    puck_cells = [c.get_text(' ', strip=True) for c in card.select('td[data-field="live-spread"], td[data-field="current-spread"]')]

    if len(ml_cells) < 2:
        return None

    return {
        'matchup': f'{teams[0]} at {teams[1]}',
        'moneyline': ml_cells[:2],
        'total': total_cells[:2] if total_cells else [],
        'puckline': puck_cells[:2] if puck_cells else [],
        'raw': text[:1200],
    }


def main():
    if len(sys.argv) < 2:
        print('usage: extract_scoresandodds_nhl.py <html-file>', file=sys.stderr)
        sys.exit(1)

    html = Path(sys.argv[1]).read_text()
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.select('.event-card, .event-card-table')
    out = []
    for card in cards:
        row = extract_card(card)
        if row and row not in out:
            out.append(row)
    print(json.dumps({'games': out}, indent=2))


if __name__ == '__main__':
    main()

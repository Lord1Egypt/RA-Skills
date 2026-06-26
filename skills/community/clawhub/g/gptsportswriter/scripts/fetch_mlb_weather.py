#!/usr/bin/env python3
import argparse
import json
import urllib.parse
import urllib.request

BALLPARKS = {
    'New York Yankees at San Francisco Giants': 'San Francisco, CA',
    'Kansas City Royals at Atlanta Braves': 'Atlanta, GA',
    'Detroit Tigers at San Diego Padres': 'San Diego, CA',
    'Minnesota Twins at Baltimore Orioles': 'Baltimore, MD',
    'Pittsburgh Pirates at New York Mets': 'New York, NY',
    'Cleveland Guardians at Seattle Mariners': 'Seattle, WA',
    'Colorado Rockies at Miami Marlins': 'Miami, FL',
    'Athletics at Toronto Blue Jays': 'Toronto, ON',
}


def main():
    ap = argparse.ArgumentParser(description='Fetch simple weather context for MLB matchup city')
    ap.add_argument('event')
    args = ap.parse_args()

    loc = BALLPARKS.get(args.event)
    if not loc:
        print(json.dumps({'event': args.event, 'weather': None, 'note': 'No mapped ballpark city'}))
        return

    url = 'https://wttr.in/' + urllib.parse.quote(loc) + '?format=%l:+%c+%t,+%w,+humidity+%h'
    with urllib.request.urlopen(url) as r:
        weather = r.read().decode('utf-8').strip()
    print(json.dumps({'event': args.event, 'weather': weather}))


if __name__ == '__main__':
    main()

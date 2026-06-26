#!/bin/bash
# nzta-traffic.sh — Query NZTA Traffic and Travel API
# No API key required. Returns real-time road events, cameras, and journey info.

set -euo pipefail

BASE_URL="https://trafficnz.info/service/traffic/rest/4"
ACCEPT="Accept: application/json"
TIMEOUT=15

# Defaults
REGION=""
JOURNEY=""
BBOX=""
CAMERAS=false
LIST_REGIONS=false
LIST_JOURNEYS=false
JSON_OUTPUT=false
ZOOM="-1"

usage() {
    cat <<EOF
Usage: $(basename "$0") [options]

Query NZTA Traffic and Travel API for real-time highway conditions.

Options:
  --region <name|id>    Region name or ID (e.g. "Wellington" or "9")
  --journey <id>        Journey/highway ID (e.g. 10 for SH1 Wellington)
  --bbox <minlon,minlat,maxlon,maxlat>  Bounding box query
  --cameras             List traffic cameras instead of events
  --list-regions        List all region names and IDs
  --list-journeys       List journeys for a region (requires --region)
  --json                Output raw JSON
  --zoom <level>        Geometry zoom level (-1 = none, default: -1)
  -h, --help            Show this help

Examples:
  $(basename "$0") --region Wellington
  $(basename "$0") --journey 10
  $(basename "$0") --cameras --region Wellington
  $(basename "$0") --list-regions
  $(basename "$0") --list-journeys --region Wellington
  $(basename "$0") --bbox 174.75,-41.20,174.95,-41.05
EOF
    exit 0
}

api_get() {
    local path="$1"
    curl -sf --max-time "$TIMEOUT" -H "$ACCEPT" "${BASE_URL}/${path}" 2>/dev/null
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --region) REGION="$2"; shift 2 ;;
        --journey) JOURNEY="$2"; shift 2 ;;
        --bbox) BBOX="$2"; shift 2 ;;
        --cameras) CAMERAS=true; shift ;;
        --list-regions) LIST_REGIONS=true; shift ;;
        --list-journeys) LIST_JOURNEYS=true; shift ;;
        --json) JSON_OUTPUT=true; shift ;;
        --zoom) ZOOM="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

# List regions
if $LIST_REGIONS; then
    result=$(api_get "regions/all/-1")
    if $JSON_OUTPUT; then
        echo "$result"
    else
        echo "NZTA Regions:"
        echo "$result" | python3 -c "
import json,sys
data = json.load(sys.stdin)
regions = data.get('response',{}).get('region',[])
if isinstance(regions, dict): regions = [regions]
for r in regions:
    print(f'  {r[\"id\"]:3d}  {r[\"name\"]}')
"
    fi
    exit 0
fi

# List journeys for a region
if $LIST_JOURNEYS; then
    if [[ -z "$REGION" ]]; then
        echo "Error: --list-journeys requires --region" >&2
        exit 1
    fi
    result=$(api_get "journeys/byregion/${REGION}/${ZOOM}")
    if [[ -z "$result" ]]; then
        echo "Error: No response from API. Check region name/ID." >&2
        exit 1
    fi
    if $JSON_OUTPUT; then
        echo "$result"
    else
        echo "Journeys in region: ${REGION}"
        echo "$result" | python3 -c "
import json,sys
data = json.load(sys.stdin)
resp = data.get('response',{})
if isinstance(resp, str) and resp == '':
    print('  No journeys found.')
    sys.exit(0)
journeys = resp.get('journey',[])
if isinstance(journeys, dict): journeys = [journeys]
for j in journeys:
    jid = str(j.get('id','?'))
    name = j.get('name','?')
    time_val = j.get('time','')
    time_str = f'  Travel time: {time_val}' if time_val and time_val != '00:00:00' else ''
    print(f'  ID {jid:6s}  {name}{time_str}')
"
    fi
    exit 0
fi

# Cameras
if $CAMERAS; then
    if [[ -n "$REGION" ]]; then
        result=$(api_get "cameras/byregion/${REGION}")
    elif [[ -n "$JOURNEY" ]]; then
        result=$(api_get "cameras/byjourney/${JOURNEY}")
    elif [[ -n "$BBOX" ]]; then
        IFS=',' read -r minlon minlat maxlon maxlat <<< "$BBOX"
        result=$(api_get "cameras/withinbounds/${minlon}/${minlat}/${maxlon}/${maxlat}")
    else
        result=$(api_get "cameras/all")
    fi

    if [[ -z "$result" ]]; then
        echo "Error: No response from API." >&2
        exit 1
    fi

    if $JSON_OUTPUT; then
        echo "$result"
    else
        echo "$result" | python3 -c "
import json,sys
data = json.load(sys.stdin)
resp = data.get('response',{})
if isinstance(resp, str) and resp == '':
    print('No cameras found.')
    sys.exit(0)
cameras = resp.get('camera',[])
if isinstance(cameras, dict): cameras = [cameras]
print(f'Traffic Cameras ({len(cameras)} found):')
for c in cameras:
    name = c.get('name','Unknown')
    lat = c.get('latitude','')
    lon = c.get('longitude','')
    img = c.get('imageUrl','')
    print(f'  {name}')
    if img:
        if img.startswith('/'):
            img = 'https://trafficnz.info' + img
        print(f'    Image: {img}')
"
    fi
    exit 0
fi

# Road events
if [[ -n "$JOURNEY" ]]; then
    result=$(api_get "events/byjourney/${JOURNEY}/${ZOOM}")
elif [[ -n "$REGION" ]]; then
    result=$(api_get "events/byregion/${REGION}/${ZOOM}")
elif [[ -n "$BBOX" ]]; then
    IFS=',' read -r minlon minlat maxlon maxlat <<< "$BBOX"
    result=$(api_get "events/withinbounds/${minlon}/${minlat}/${maxlon}/${maxlat}/${ZOOM}")
else
    result=$(api_get "events/all/${ZOOM}")
fi

if [[ -z "$result" ]]; then
    echo "Error: No response from API." >&2
    exit 1
fi

if $JSON_OUTPUT; then
    echo "$result"
else
    echo "$result" | python3 -c "
import json,sys
data = json.load(sys.stdin)
resp = data.get('response',{})
if isinstance(resp, str) and resp == '':
    print('No active road events. All clear!')
    sys.exit(0)
events = resp.get('roadevent',[])
if isinstance(events, dict): events = [events]
active = [e for e in events if e.get('status','') == 'Active']
if not active:
    print('No active road events. All clear!')
    sys.exit(0)
print(f'Active Road Events ({len(active)}):')
print()
for e in active:
    impact = e.get('impact','Unknown')
    etype = e.get('eventDescription', e.get('eventType','Unknown'))
    location = e.get('locationArea','Unknown location')
    highway = e.get('journey',{}).get('name','')
    region = e.get('region',{}).get('name','')
    comments = e.get('eventComments','').strip()
    resolution = e.get('expectedResolution','')
    alt_route = e.get('alternativeRoute','')

    prefix = ''
    if highway: prefix += f'[{highway}] '
    if region: prefix += f'({region}) '

    print(f'  {prefix}{etype} — {impact}')
    print(f'    Location: {location}')
    if comments:
        # Truncate long comments
        if len(comments) > 200:
            comments = comments[:200] + '...'
        print(f'    Details: {comments}')
    if resolution and resolution != 'Not Applicable':
        print(f'    Expected resolution: {resolution}')
    if alt_route and alt_route != 'Not Applicable':
        print(f'    Alternative route: {alt_route}')
    print()
"
fi

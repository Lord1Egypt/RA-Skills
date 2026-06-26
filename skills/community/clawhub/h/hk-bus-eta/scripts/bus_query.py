#!/usr/bin/env python3
"""
Hong Kong Bus Stops Query Helper
Version: 1.0.0

Provides fast stop lookup using local SQLite database.

Created: 2026-03-13 (by "Mr. Usagi - Tom's Agent")
"""

import sqlite3
import os
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bus_stops.db")

def get_connection():
    """Get database connection."""
    if not os.path.exists(DB_PATH):
        return None
    return sqlite3.connect(DB_PATH)

def find_stops_by_name(pattern, lang='tc', limit=10):
    """
    Find stops matching a name pattern.
    Returns: list of {stop_id, stop_name, company, route, lat, lon}
    """
    conn = get_connection()
    if not conn:
        return []
    
    c = conn.cursor()
    pattern_lower = pattern.lower()
    
    # Exact match first
    c.execute('''
        SELECT DISTINCT sn.stop_id, sn.company, sn.route, sn.lang
        FROM stop_names sn
        WHERE sn.name = ?
        LIMIT ?
    ''', (pattern_lower, limit))
    
    exact_matches = c.fetchall()
    
    # Then fuzzy match (substring)
    c.execute('''
        SELECT DISTINCT sn.stop_id, sn.company, sn.route, sn.lang
        FROM stop_names sn
        WHERE sn.name LIKE ? AND sn.name != ?
        LIMIT ?
    ''', (f'%{pattern_lower}%', pattern_lower, limit))
    
    fuzzy_matches = c.fetchall()
    
    # Get stop details
    results = []
    seen = set()
    
    for stop_id, company, route, lang in exact_matches + fuzzy_matches:
        if (stop_id, company, route) in seen:
            continue
        seen.add((stop_id, company, route))
        
        c.execute('''
            SELECT s.name_tc, s.name_en, s.lat, s.lon, r.orig_tc, r.orig_en, r.dest_tc, r.dest_en
            FROM stops s
            JOIN routes r ON s.route_id = r.id
            WHERE s.stop_id = ? AND r.company = ? AND r.route = ?
            LIMIT 1
        ''', (stop_id, company, route))
        
        row = c.fetchone()
        if row:
            results.append({
                'stop_id': stop_id,
                'name_tc': row[0],
                'name_en': row[1],
                'lat': row[2],
                'lon': row[3],
                'company': company,
                'route': route,
                'orig_tc': row[4],
                'orig_en': row[5],
                'dest_tc': row[6],
                'dest_en': row[7]
            })
    
    conn.close()
    return results

def find_stops_by_coords(lat, lon, radius_km=0.5, limit=10):
    """
    Find stops within radius of given coordinates.
    Uses approximate distance calculation for speed.
    """
    conn = get_connection()
    if not conn:
        return []
    
    # Approximate degree distance (1 degree ~111km)
    radius_deg = radius_km / 111.0
    
    c = conn.cursor()
    c.execute('''
        SELECT s.stop_id, s.name_tc, s.name_en, s.lat, s.lon, s.stop_seq,
               r.company, r.route, r.orig_tc, r.dest_tc
        FROM stops s
        JOIN routes r ON s.route_id = r.id
        WHERE s.lat BETWEEN ? AND ? AND s.lon BETWEEN ? AND ?
    ''', (lat - radius_deg, lat + radius_deg, lon - radius_deg, lon + radius_deg))
    
    rows = c.fetchall()
    conn.close()
    
    # Calculate actual distances and sort
    results = []
    for row in rows:
        stop_lat, stop_lon = row[3], row[4]
        dist = math.sqrt((stop_lat - lat)**2 + (stop_lon - lon)**2) * 111  # approx km
        if dist <= radius_km:
            results.append({
                'stop_id': row[0],
                'name_tc': row[1],
                'name_en': row[2],
                'lat': stop_lat,
                'lon': stop_lon,
                'stop_seq': row[5],
                'company': row[6],
                'route': row[7],
                'orig_tc': row[8],
                'dest_tc': row[9],
                'distance': dist
            })
    
    results.sort(key=lambda x: x['distance'])
    return results[:limit]

def get_route_stops(route, company=None):
    """
    Get all stops for a route.
    Returns: list of {stop_id, stop_name_tc, stop_name_en, stop_seq, lat, lon, company}
    """
    conn = get_connection()
    if not conn:
        return []
    
    c = conn.cursor()
    
    if company:
        c.execute('''
            SELECT s.stop_id, s.name_tc, s.name_en, s.stop_seq, s.lat, s.lon, r.company, r.route_dir
            FROM stops s
            JOIN routes r ON s.route_id = r.id
            WHERE r.route = ? AND r.company = ?
            ORDER BY r.route_dir, s.stop_seq
        ''', (route, company))
    else:
        c.execute('''
            SELECT s.stop_id, s.name_tc, s.name_en, s.stop_seq, s.lat, s.lon, r.company, r.route_dir
            FROM stops s
            JOIN routes r ON s.route_id = r.id
            WHERE r.route = ?
            ORDER BY r.company, r.route_dir, s.stop_seq
        ''', (route,))
    
    rows = c.fetchall()
    conn.close()
    
    return [{
        'stop_id': row[0],
        'name_tc': row[1],
        'name_en': row[2],
        'stop_seq': row[3],
        'lat': row[4],
        'lon': row[5],
        'company': row[6],
        'route_dir': row[7]
    } for row in rows]

def get_db_info():
    """Get database info for debugging."""
    conn = get_connection()
    if not conn:
        return {'status': 'not_found'}
    
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM routes')
    route_count = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM stops')
    stop_count = c.fetchone()[0]
    
    c.execute('SELECT COUNT(DISTINCT stop_id) FROM stops')
    unique_stops = c.fetchone()[0]
    
    c.execute('SELECT value FROM metadata WHERE key = "last_sync"')
    row = c.fetchone()
    last_sync = row[0] if row else 'unknown'
    
    conn.close()
    
    return {
        'status': 'ok',
        'route_count': route_count,
        'stop_count': stop_count,
        'unique_stops': unique_stops,
        'last_sync': last_sync,
        'db_size_mb': os.path.getsize(DB_PATH) / 1024 / 1024 if os.path.exists(DB_PATH) else 0
    }

if __name__ == "__main__":
    # Test
    info = get_db_info()
    print(f"Database: {info}")
    
    if info['status'] == 'ok':
        # Test search
        stops = find_stops_by_name('寶琳')
        print(f"\n搜尋「寶琳」: {len(stops)} results")
        for s in stops[:5]:
            print(f"  - {s['route']} {s['company']}: {s['stop_name_tc']}")
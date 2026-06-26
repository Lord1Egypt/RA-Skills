
import sys
import json
from datetime import datetime

def format_profile(data):
    if not data or not data.get('success'):
        print(f"❌ Error: {data.get('error') if data else 'Unknown error'}")
        return

    profile = data.get('profile', {})
    matches = data.get('matches', [])
    
    steam_id = profile.get('steam64_id', '')
    name = profile.get('name', 'Unknown')
    
    # Recalculate averages from matches for 100-game summary
    total_kills = 0
    total_deaths = 0
    total_assists = 0
    total_adr = 0
    total_hs_kills = 0
    total_leetify_rating = 0
    matches_with_stats = 0

    for m in matches:
        stats_list = m.get('stats', [])
        stats = next((s for s in stats_list if s['steam64_id'] == steam_id), None)
        if stats:
            total_kills += stats.get('total_kills', 0)
            total_deaths += stats.get('total_deaths', 0)
            total_assists += stats.get('total_assists', 0)
            total_adr += stats.get('dpr', 0)
            total_hs_kills += stats.get('total_hs_kills', 0)
            total_leetify_rating += stats.get('leetify_rating', 0)
            matches_with_stats += 1

    avg_kd = total_kills / max(total_deaths, 1)
    avg_adr = total_adr / max(matches_with_stats, 1)
    avg_hs_pct = (total_hs_kills / max(total_kills, 1)) * 100
    avg_leetify = total_leetify_rating / max(matches_with_stats, 1)

    print(f"👤 *{name}*")
    print(f"🆔 Steam: {steam_id}")
    print(f"📊 Последние 100 игр (средние):")
    print(f"├ K/D: *{avg_kd:.2f}*")
    print(f"├ ADR: {avg_adr:.1f}")
    print(f"├ HS%: {avg_hs_pct:.1f}%")
    print(f"└ Leetify Rating: {avg_leetify:.3f}")
    
    print(f"\n📈 Последние 5 матчей:")
    medals = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    for i, m in enumerate(matches[:5]):
        stats_list = m.get('stats', [])
        stats = next((s for s in stats_list if s['steam64_id'] == steam_id), None)
        if stats:
            map_name = m.get('map_name', 'Unknown').replace('de_', '')
            kills = stats.get('total_kills', 0)
            deaths = stats.get('total_deaths', 0)
            assists = stats.get('total_assists', 0)
            adr = stats.get('dpr', 0)
            hs_kills = stats.get('total_hs_kills', 0)
            mvps = stats.get('mvps', 0)
            kd = kills / max(deaths, 1)
            
            # Score
            player_team = stats.get('initial_team_number')
            p_score = 0
            e_score = 0
            team_scores = m.get('team_scores', [])
            for ts in team_scores:
                if ts.get('team_number') == player_team: p_score = ts.get('score', 0)
                else: e_score = ts.get('score', 0)
            
            outcome = "✅" if p_score > e_score else ("❌" if p_score < e_score else "🤝")
            date_str = m.get('finished_at', '').split('T')[0]
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                formatted_date = dt.strftime("%d.%m")
            except:
                formatted_date = date_str
            
            print(f"{medals[i]} {outcome} {map_name} ({p_score}:{e_score}) • {formatted_date} • K/D/A: {kills}/{deaths}/{assists} ({kd:.2f}) • ADR: {adr:.1f} | HS: {hs_kills} | MVPs: {mvps}")
            if i < 4 and i < len(matches)-1: print("⠀")

    # Winrate calculation
    total_wins = 0
    for m in matches:
        stats_list = m.get('stats', [])
        stats = next((s for s in stats_list if s['steam64_id'] == steam_id), None)
        if stats:
            player_team = stats.get('initial_team_number')
            team_scores = m.get('team_scores', [])
            p_score = 0
            e_score = 0
            for ts in team_scores:
                if ts.get('team_number') == player_team: p_score = ts.get('score', 0)
                else: e_score = ts.get('score', 0)
            if p_score > e_score:
                total_wins += 1

    winrate = (total_wins / max(len(matches), 1)) * 100
    
    print(f"\n📊 Основная статистика:")
    print(f"├ Винрейт: {winrate:.1f}%")
    print(f"├ Матчей: {len(matches)}")
    print(f"└ Leetify Rating: {avg_leetify:.2f}")

    # Ranks & Skills (CORRECTED MAPPING)
    ranks = profile.get('ranks', {})
    # FACEIT is direct, not nested
    faceit_lvl = ranks.get('faceit')
    faceit_elo = ranks.get('faceit_elo')
    
    if faceit_lvl is None: faceit_lvl = "None"
    if faceit_elo is None: faceit_elo = "None"
    
    print(f"🏆 Ранги:")
    print(f"├ FACEIT: {faceit_lvl} lvl ({faceit_elo} ELO)")

    # Rating/Skill is singular 'rating' in profile
    rating = profile.get('rating', {})
    print(f"⭐ Рейтинги:")
    print(f"├ Aim: {rating.get('aim', 0):.1f}")
    print(f"├ Positioning: {rating.get('positioning', 0):.1f}")
    print(f"└ Utility: {rating.get('utility', 0):.1f}")

    # General Stats is 'stats' in profile
    general = profile.get('stats', {})
    print(f"🎯 Общая статистика:")
    print(f"├ Реакция: {general.get('reaction_time_ms', 0):.0f}ms")
    # Values are already percentages (e.g. 33.28), no need to multiply by 100
    print(f"├ Точность: {general.get('accuracy_enemy_spotted', 0):.1f}%")
    print(f"├ Хедшоты: {general.get('accuracy_head', 0):.1f}%")
    print(f"└ Спрей: {general.get('spray_accuracy', 0):.1f}%")

if __name__ == "__main__":
    try:
        input_data = sys.stdin.read()
        if input_data:
            data = json.loads(input_data)
            format_profile(data)
    except Exception as e:
        print(f"Error: {e}")

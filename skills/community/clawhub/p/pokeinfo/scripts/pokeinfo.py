#!/usr/bin/env python3
"""
Pokeinfo - Fetch and format Pokémon information from PokéAPI.
Supports multiple languages: en, zh-hant, zh-hans, ja, ko, fr, de, es, it

Usage: python3 pokeinfo.py <pokemon_name_or_id> [--voice]
       python3 pokeinfo.py language <lang>
       python3 pokeinfo.py language list
"""

import sys
import os
import json
import urllib.request
import urllib.error
import tempfile

BASE_URL = "https://pokeapi.co/api/v2/pokemon"
SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species"

# Language configurations
TRANSLATIONS = {
    "en": {
        "height": "Height",
        "weight": "Weight",
        "base_exp": "Base Experience",
        "types": "Type(s)",
        "abilities": "Abilities",
        "hidden": "Hidden",
        "stats": "Stats",
        "hp": "HP",
        "attack": "Attack",
        "defense": "Defense",
        "sp_atk": "Sp. Attack",
        "sp_def": "Sp. Defense",
        "speed": "Speed",
        "sprite": "Sprite",
        "cry": "Cry",
        "moves": "Level-up Moves",
        "language_set": "Language set to: {lang} ({display})",
        "current_lang": "Current language: {lang}",
        "available_langs": "Available languages",
        "unknown_lang": "Unknown language: {lang}",
        "not_found": "Pokémon '{name}' not found.",
    },
    "zh-hant": {
        "height": "身高",
        "weight": "體重",
        "base_exp": "基礎經驗值",
        "types": "屬性",
        "abilities": "特性",
        "hidden": "隱藏特性",
        "stats": "六項數值",
        "hp": "HP",
        "attack": "攻擊",
        "defense": "防禦",
        "sp_atk": "特攻",
        "sp_def": "特防",
        "speed": "速度",
        "sprite": "官方繪圖",
        "cry": "叫聲",
        "moves": "升級招式",
        "language_set": "語言已設定為: {lang} ({display})",
        "current_lang": "目前語言: {lang}",
        "available_langs": "支援語言列表",
        "unknown_lang": "未知語言: {lang}",
        "not_found": "找不到寶可夢 '{name}'",
    },
    "zh-hans": {
        "height": "身高",
        "weight": "体重",
        "base_exp": "基础经验值",
        "types": "属性",
        "abilities": "特性",
        "hidden": "隐藏特性",
        "stats": "六项数值",
        "hp": "HP",
        "attack": "攻击",
        "defense": "防御",
        "sp_atk": "特攻",
        "sp_def": "特防",
        "speed": "速度",
        "sprite": "官方绘图",
        "cry": "叫声",
        "moves": "升级招式",
        "language_set": "语言已设定为: {lang} ({display})",
        "current_lang": "当前语言: {lang}",
        "available_langs": "支持语言列表",
        "unknown_lang": "未知语言: {lang}",
        "not_found": "找不到宝可梦 '{name}'",
    },
    "ja": {
        "height": "身長",
        "weight": "体重",
        "base_exp": "基礎経験値",
        "types": "タイプ",
        "abilities": "特性",
        "hidden": "隠れ特性",
        "stats": "種族値",
        "hp": "HP",
        "attack": "こうげき",
        "defense": "ぼうぎょ",
        "sp_atk": "とくこう",
        "sp_def": "とくぼう",
        "speed": "すばやさ",
        "sprite": "画像",
        "cry": "鳴き声",
        "moves": "レベル技",
        "language_set": "言語を設定しました: {lang} ({display})",
        "current_lang": "現在の言語: {lang}",
        "available_langs": "利用可能な言語",
        "unknown_lang": "不明な言語: {lang}",
        "not_found": "ポケモン '{name}' が見つかりません",
    },
    "ko": {
        "height": "키",
        "weight": "몸무게",
        "base_exp": "기본 경험치",
        "types": "타입",
        "abilities": "특성",
        "hidden": "숨겨진 특성",
        "stats": "종족값",
        "hp": "HP",
        "attack": "공격",
        "defense": "방어",
        "sp_atk": "특수공격",
        "sp_def": "특수방어",
        "speed": "스피드",
        "sprite": "이미지",
        "cry": "울음소리",
        "moves": "레벨업 기술",
        "language_set": "언어가 설정되었습니다: {lang} ({display})",
        "current_lang": "현재 언어: {lang}",
        "available_langs": "사용 가능한 언어",
        "unknown_lang": "알 수 없는 언어: {lang}",
        "not_found": "포켓몬 '{name}'을(를) 찾을 수 없습니다",
    },
    "fr": {
        "height": "Taille",
        "weight": "Poids",
        "base_exp": "Expérience de base",
        "types": "Type(s)",
        "abilities": "Talents",
        "hidden": "Caché",
        "stats": "Stats",
        "hp": "PV",
        "attack": "Attaque",
        "defense": "Défense",
        "sp_atk": "Att. Spé.",
        "sp_def": "Déf. Spé.",
        "speed": "Vitesse",
        "sprite": "Image",
        "cry": "Cri",
        "moves": "Attaques par niveau",
        "language_set": "Langue définie: {lang} ({display})",
        "current_lang": "Langue actuelle: {lang}",
        "available_langs": "Langues disponibles",
        "unknown_lang": "Langue inconnue: {lang}",
        "not_found": "Pokémon '{name}' non trouvé",
    },
    "de": {
        "height": "Größe",
        "weight": "Gewicht",
        "base_exp": "Basis-Erfahrung",
        "types": "Typ(en)",
        "abilities": "Fähigkeiten",
        "hidden": "Versteckt",
        "stats": "Werte",
        "hp": "KP",
        "attack": "Angriff",
        "defense": "Verteidigung",
        "sp_atk": "Sp. Angriff",
        "sp_def": "Sp. Verteidigung",
        "speed": "Initiative",
        "sprite": "Bild",
        "cry": "Schrei",
        "moves": "Level-Attacken",
        "language_set": "Sprache gesetzt: {lang} ({display})",
        "current_lang": "Aktuelle Sprache: {lang}",
        "available_langs": "Verfügbare Sprachen",
        "unknown_lang": "Unbekannte Sprache: {lang}",
        "not_found": "Pokémon '{name}' nicht gefunden",
    },
    "es": {
        "height": "Altura",
        "weight": "Peso",
        "base_exp": "Experiencia base",
        "types": "Tipo(s)",
        "abilities": "Habilidades",
        "hidden": "Oculta",
        "stats": "Estadísticas",
        "hp": "PS",
        "attack": "Ataque",
        "defense": "Defensa",
        "sp_atk": "At. Esp.",
        "sp_def": "Def. Esp.",
        "speed": "Velocidad",
        "sprite": "Imagen",
        "cry": "Grito",
        "moves": "Movimientos por nivel",
        "language_set": "Idioma configurado: {lang} ({display})",
        "current_lang": "Idioma actual: {lang}",
        "available_langs": "Idiomas disponibles",
        "unknown_lang": "Idioma desconocido: {lang}",
        "not_found": "Pokémon '{name}' no encontrado",
    },
    "it": {
        "height": "Altezza",
        "weight": "Peso",
        "base_exp": "Esperienza base",
        "types": "Tipo(i)",
        "abilities": "Abilità",
        "hidden": "Nascosta",
        "stats": "Statistiche",
        "hp": "PS",
        "attack": "Attacco",
        "defense": "Difesa",
        "sp_atk": "Att. Sp.",
        "sp_def": "Dif. Sp.",
        "speed": "Velocità",
        "sprite": "Immagine",
        "cry": "Verso",
        "moves": "Mosse per livello",
        "language_set": "Lingua impostata: {lang} ({display})",
        "current_lang": "Lingua attuale: {lang}",
        "available_langs": "Lingue disponibili",
        "unknown_lang": "Lingua sconosciuta: {lang}",
        "not_found": "Pokémon '{name}' non trovato",
    },
}

LANG_DISPLAY = {
    "en": "English",
    "zh-hant": "繁體中文",
    "zh-hans": "简体中文",
    "ja": "日本語",
    "ko": "한국어",
    "fr": "Français",
    "de": "Deutsch",
    "es": "Español",
    "it": "Italiano",
}

DEFAULT_LANG = "en"
CONFIG_FILE = os.path.expanduser("~/.config/pokeinfo/config.json")

def load_config():
    """Load user configuration."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"language": DEFAULT_LANG}

def save_config(config):
    """Save user configuration."""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_lang():
    """Get current language setting."""
    config = load_config()
    lang = config.get("language", DEFAULT_LANG)
    if lang not in TRANSLATIONS:
        return DEFAULT_LANG
    return lang

def t(key, lang_code=None, **kwargs):
    """Get translated text."""
    if lang_code is None:
        lang_code = get_lang()
    text = TRANSLATIONS.get(lang_code, TRANSLATIONS[DEFAULT_LANG]).get(key, key)
    return text.format(**kwargs) if kwargs else text

def fetch_url(url):
    """Fetch JSON data from URL."""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (compatible; Pokeinfo/1.0)'
    })
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode('utf-8'))

def fetch_pokemon(name_or_id):
    """Fetch Pokémon data from PokéAPI."""
    name_or_id = name_or_id.lower().strip()
    # Strip leading zeros from numeric IDs (e.g., "0006" -> "6")
    if name_or_id.isdigit():
        name_or_id = str(int(name_or_id))
    
    url = f"{BASE_URL}/{name_or_id}"
    try:
        return fetch_url(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(t("not_found", name=name_or_id))
        else:
            print(f"Error: HTTP {e.code} - {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def fetch_species(pokemon_id):
    """Fetch Pokémon species data for localized names."""
    try:
        return fetch_url(f"{SPECIES_URL}/{pokemon_id}")
    except Exception:
        return None

def get_localized_name(species_data, lang):
    """Get Pokémon name in specified language."""
    if not species_data:
        return None
    for name_entry in species_data.get("names", []):
        if name_entry["language"]["name"] == lang:
            return name_entry["name"]
    return None

def get_localized_type_name(type_url, lang):
    """Get type name in specified language."""
    try:
        type_data = fetch_url(type_url)
        for name_entry in type_data.get("names", []):
            if name_entry["language"]["name"] == lang:
                return name_entry["name"]
    except Exception:
        pass
    return None

def get_localized_ability_name(ability_url, lang):
    """Get ability name in specified language."""
    try:
        ability_data = fetch_url(ability_url)
        for name_entry in ability_data.get("names", []):
            if name_entry["language"]["name"] == lang:
                return name_entry["name"]
    except Exception:
        pass
    return None

def download_cry(cry_url, output_path):
    """Download cry audio file."""
    req = urllib.request.Request(cry_url, headers={
        'User-Agent': 'Mozilla/5.0 (compatible; Pokeinfo/1.0)'
    })
    with urllib.request.urlopen(req, timeout=15) as response:
        with open(output_path, 'wb') as f:
            f.write(response.read())

def convert_cry_to_opus(input_path, output_path):
    """Convert OGG Vorbis cry to OGG Opus for Telegram voice message."""
    try:
        import soundfile as sf
        from scipy import signal
        
        data, samplerate = sf.read(input_path)
        
        target_rate = 48000
        num_samples = int(len(data) * target_rate / samplerate)
        data_resampled = signal.resample(data, num_samples)
        
        sf.write(output_path, data_resampled, target_rate, format='OGG', subtype='OPUS')
        return True
    except ImportError:
        return False
    except Exception:
        return False

def get_stat_name(stat_key, lang):
    """Get localized stat name."""
    stat_map = {
        "hp": "hp",
        "attack": "attack",
        "defense": "defense",
        "special-attack": "sp_atk",
        "special-defense": "sp_def",
        "speed": "speed",
    }
    key = stat_map.get(stat_key, stat_key)
    return t(key, lang)

def format_pokemon(data, lang=None):
    """Format Pokémon data into readable output with localization."""
    if lang is None:
        lang = get_lang()
    
    # Fetch species data for localized name
    species_data = fetch_species(data['id'])
    localized_name = get_localized_name(species_data, lang)
    
    name = data['name'].title()
    display_name = f"{name} ({localized_name})" if localized_name and localized_name != name else name
    
    lines = []
    
    # Header
    lines.append(f"#{data['id']} {display_name}")
    lines.append("=" * 40)
    
    # Basic Info
    lines.append(f"{t('height', lang)}: {data['height'] / 10:.1f} m")
    lines.append(f"{t('weight', lang)}: {data['weight'] / 10:.1f} kg")
    lines.append(f"{t('base_exp', lang)}: {data['base_experience']}")
    lines.append("")
    
    # Types
    types = []
    for t_entry in data['types']:
        type_name = get_localized_type_name(t_entry['type']['url'], lang)
        if not type_name:
            type_name = t_entry['type']['name'].title()
        types.append(type_name)
    lines.append(f"{t('types', lang)}: {', '.join(types)}")
    lines.append("")
    
    # Abilities
    abilities = []
    for a in data['abilities']:
        ability_name = get_localized_ability_name(a['ability']['url'], lang)
        if not ability_name:
            ability_name = a['ability']['name'].replace('-', ' ').title()
        if a['is_hidden']:
            ability_name += f" ({t('hidden', lang)})"
        abilities.append(ability_name)
    lines.append(f"{t('abilities', lang)}: {', '.join(abilities)}")
    lines.append("")
    
    # Stats
    lines.append(f"{t('stats', lang)}:")
    for stat in data['stats']:
        stat_name = get_stat_name(stat['stat']['name'], lang)
        lines.append(f"  {stat_name}: {stat['base_stat']}")
    lines.append("")
    
    # Sprites
    sprite_url = data['sprites']['other']['official-artwork']['front_default']
    if not sprite_url:
        sprite_url = data['sprites']['front_default']
    if sprite_url:
        lines.append(f"{t('sprite', lang)}: {sprite_url}")
    
    # Cries
    cry_url = data['cries'].get('latest')
    if cry_url:
        lines.append(f"{t('cry', lang)}: {cry_url}")
    
    lines.append("")
    
    # Moves (level-up moves only)
    level_up_moves = {}
    for move_entry in data['moves']:
        move_name = move_entry['move']['name'].replace('-', ' ').title()
        for detail in move_entry['version_group_details']:
            if detail['move_learn_method']['name'] == 'level-up':
                version = detail['version_group']['name'].replace('-', ' ').title()
                level = detail['level_learned_at']
                if version not in level_up_moves:
                    level_up_moves[version] = []
                level_up_moves[version].append((level, move_name))
    
    if level_up_moves:
        recent_version = sorted(level_up_moves.keys())[-1]
        moves = sorted(level_up_moves[recent_version], key=lambda x: x[0])
        lines.append(f"{t('moves', lang)} ({recent_version}):")
        for level, move_name in moves[:20]:
            lines.append(f"  Lv.{level:>3} {move_name}")
        if len(moves) > 20:
            lines.append(f"  ... and {len(moves) - 20} more")
        lines.append("")
    
    return "\n".join(lines)

def handle_voice_command(data):
    """Download and convert cry to Telegram-compatible voice message."""
    cry_url = data['cries'].get('latest')
    if not cry_url:
        return None
    
    pokemon_id = data['id']
    
    temp_dir = tempfile.gettempdir()
    vorbis_path = os.path.join(temp_dir, f"pokeinfo_cry_{pokemon_id}_vorbis.ogg")
    opus_path = os.path.join(temp_dir, f"pokeinfo_cry_{pokemon_id}_opus.ogg")
    
    try:
        download_cry(cry_url, vorbis_path)
        success = convert_cry_to_opus(vorbis_path, opus_path)
        
        if os.path.exists(vorbis_path):
            os.remove(vorbis_path)
        
        if success and os.path.exists(opus_path):
            return opus_path
    except Exception:
        pass
    return None

def handle_language_command(args):
    """Handle language setting commands."""
    config = load_config()
    
    if not args or args[0] == "list":
        print(f"{t('available_langs')}:")
        for code, display in LANG_DISPLAY.items():
            marker = " *" if code == config.get("language", DEFAULT_LANG) else ""
            print(f"  {code:10} - {display}{marker}")
        return
    
    lang = args[0]
    if lang not in TRANSLATIONS:
        print(t("unknown_lang", lang=lang))
        print(f"\n{t('available_langs')}:")
        for code, display in LANG_DISPLAY.items():
            print(f"  {code:10} - {display}")
        sys.exit(1)
    
    config["language"] = lang
    save_config(config)
    print(t("language_set", lang_code=lang, lang=lang, display=LANG_DISPLAY[lang]))

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pokeinfo.py <pokemon_name_or_id> [--voice]")
        print("       python3 pokeinfo.py language <lang>")
        print("       python3 pokeinfo.py language list")
        sys.exit(1)
    
    command = sys.argv[1]
    
    # Handle language commands
    if command == "language":
        handle_language_command(sys.argv[2:])
        return
    
    # Normal pokemon query
    name_or_id = command
    voice_mode = '--voice' in sys.argv
    
    data = fetch_pokemon(name_or_id)
    
    if voice_mode:
        print(format_pokemon(data))
        voice_path = handle_voice_command(data)
        if voice_path:
            print(f"\n[VOICE]{json.dumps({'voice_path': voice_path})}[/VOICE]")
    else:
        print(format_pokemon(data))

if __name__ == "__main__":
    main()

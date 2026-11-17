import os
import sys
import json
import urllib.request
import urllib.parse
import hashlib

# Match the system environment variable (with a fallback just in case)
IP = os.environ.get("OPENSPRINKLER_IP_ADDRESS") or os.environ.get("OPENSPRINKLER_IP")
PASSWORD = os.environ.get("OPENSPRINKLER_PASSWORD")

def get_md5_hash(text):
    """OpenSprinkler API requires an MD5 hash of the password in lowercase."""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def make_request(path):
    """Handles the HTTP request to the local OpenSprinkler device."""
    if not IP or not PASSWORD:
        return {"error": "Missing OPENSPRINKLER_IP_ADDRESS or OPENSPRINKLER_PASSWORD."}
    
    pw_hash = get_md5_hash(PASSWORD)
    separator = "&" if "?" in path else "?"
    url = f"http://{IP}{path}{separator}pw={pw_hash}"
        
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return {"error": str(e)}

# --- TOOL FUNCTIONS ---

def get_status(args):
    """Fetches global variables, sensor states, and station running status."""
    res = make_request("/ja")
    if "error" in res: return json.dumps(res)
    
    # Newer 2.2.1+ Firmware uses a nested JSON structure
    status_block = res.get("status", {})
    settings_block = res.get("settings", {})
    stations_block = res.get("stations", {})
    
    sn = status_block.get("sn", res.get("sn", []))
    ps = settings_block.get("ps", res.get("ps", []))
    snames = stations_block.get("snames", res.get("snames", []))
    
    clean_status = {
        "global_enabled": bool(settings_block.get("en", res.get("en", 1))),
        "rain_delay_active": bool(settings_block.get("rd", res.get("rd", 0))),
        "rain_delay_stop_time_epoch": settings_block.get("rdst", res.get("rdst", 0)),
        "rain_sensor_active": bool(status_block.get("rs", res.get("rs", 0))),
        "sensor_1_active": bool(status_block.get("sn1", res.get("sn1", 0))),
        "sensor_2_active": bool(status_block.get("sn2", res.get("sn2", 0))),
        "stations": []
    }
    
    for i in range(len(sn)):
        station_id = i + 1  # 1-based indexing for AI
        is_active = bool(sn[i])
        
        # Attach the human-readable station name if it exists, otherwise default to "Station X"
        station_name = snames[i] if i < len(snames) else f"Station {station_id}"
        
        station_data = {
            "station_id": station_id,
            "name": station_name,
            "is_active": is_active
        }
        
        if is_active and i < len(ps):
            prog_info = ps[i]
            if isinstance(prog_info, list) and len(prog_info) >= 2:
                pid = prog_info[0]
                if pid > 0:
                    station_data["running_program_id"] = pid
                    station_data["remaining_seconds"] = prog_info[1]
                    
        clean_status["stations"].append(station_data)
        
    return json.dumps(clean_status)

def get_programs(args):
    """Fetches all programs, parsing their 1-based IDs and human-readable names."""
    res = make_request("/ja")
    if "error" in res: return json.dumps(res)
    
    programs_block = res.get("programs", {})
    pd = programs_block.get("pd", res.get("pd", []))
    
    clean_programs = []
    
    for i in range(len(pd)):
        pid = i + 1  # 1-based indexing for AI
        program_name = f"Program {pid}"
        is_enabled = True
        
        if isinstance(pd[i], list):
            # Firmware 2.2.1 embeds the name directly at index 5
            if len(pd[i]) > 5:
                program_name = str(pd[i][5])
            
            # The lowest bit (bit 0) of the first element indicates if the program is enabled
            if len(pd[i]) > 0:
                is_enabled = bool(pd[i][0] & 1)
            
        clean_programs.append({
            "program_id": pid,
            "name": program_name,
            "is_enabled": is_enabled
        })
        
    return json.dumps({"programs": clean_programs})

def get_options(args):
    """Fetches system options, parsing weather adjustment (Water Level)."""
    # Call /ja to get both "options" and "settings" in one network hop
    res = make_request("/ja")
    if "error" in res: return json.dumps(res)
    
    options_block = res.get("options", {})
    settings_block = res.get("settings", {})
    
    clean_options = {
        "firmware_version": options_block.get("fwv", res.get("fwv")),
        "hardware_version": options_block.get("hwv", res.get("hwv")),
        "use_weather": bool(options_block.get("uwt", res.get("uwt", 0))),
        "water_level_percentage": options_block.get("wl", res.get("wl", 100)), 
        "sunrise_epoch": settings_block.get("sunrise", res.get("sunrise", 0)),
        "sunset_epoch": settings_block.get("sunset", res.get("sunset", 0))
    }
    
    return json.dumps({"options": clean_options})

def set_station(args):
    """Manually start/stop a single station."""
    station_id = args.get("station_id")
    state = args.get("state")
    duration = args.get("duration", 0)
    
    if not station_id: return json.dumps({"error": "station_id is required."})
    sid = station_id - 1  # Convert to 0-based API parameter
    
    if state:
        if duration <= 0: return json.dumps({"error": "duration must be > 0."})
        res = make_request(f"/cm?sid={sid}&en=1&t={duration}")
    else:
        res = make_request(f"/cm?sid={sid}&en=0")
    return json.dumps(res)

def start_program(args):
    """Starts a pre-configured program. Native API pid is 1-based."""
    program_id = args.get("program_id")
    use_weather = 1 if args.get("use_weather", True) else 0
    if not program_id: return json.dumps({"error": "program_id is required."})
    
    res = make_request(f"/mp?pid={program_id}&uwt={use_weather}")
    return json.dumps(res)

def run_once(args):
    """Converts a highly readable dictionary into the 72-element API array."""
    station_durations = args.get("station_durations", {})
    max_stations = 72
    t_array = [0] * max_stations
    
    # Map dictionary (e.g., {"1": 600}) to the 0-based array
    for stat_id_str, duration in station_durations.items():
        try:
            sid = int(stat_id_str) - 1
            if 0 <= sid < max_stations:
                t_array[sid] = int(duration)
        except ValueError:
            pass
            
    t_json = urllib.parse.quote(json.dumps(t_array))
    res = make_request(f"/cr?t={t_json}")
    return json.dumps(res)

def pause_queue(args):
    """Temporarily pauses the watering queue (e.g., while walking a dog)."""
    duration = args.get("duration_seconds", 0)
    res = make_request(f"/pq?ps={duration}")
    return json.dumps(res)

def set_rain_delay(args):
    hours = args.get("hours", 0)
    res = make_request(f"/cv?rd={hours}")
    return json.dumps(res)

def set_operation(args):
    en = 1 if args.get("enable") else 0
    res = make_request(f"/cv?en={en}")
    return json.dumps(res)

def stop_all_stations(args):
    res = make_request("/cv?rsn=1")
    return json.dumps(res)

def get_logs(args):
    """Fetches logs and decodes the native [pid, sid, dur, end] array format."""
    hist = args.get("hist_days", 7)
    res = make_request(f"/jl?hist={hist}")
    if "error" in res: return json.dumps(res)
    
    logs_raw = res if isinstance(res, list) else res.get("log", [])
    parsed_logs = []
    
    for entry in logs_raw:
        if len(entry) >= 4:
            pid = entry[0]
            sid_raw = entry[1]
            
            # Handle special events (pid=0) where sid is a string (e.g., 'rd', 'fl')
            if pid == 0:
                station_val = sid_raw
            else:
                # Convert 0-based station ID to 1-based for the AI
                station_val = sid_raw + 1 if isinstance(sid_raw, int) else sid_raw
                
            parsed_logs.append({
                "program_id": pid,
                "station_id": station_val,
                "duration_seconds": entry[2],
                "end_time_epoch": entry[3]
            })
            
    return json.dumps({"logs": parsed_logs})

def reboot_controller(args):
    res = make_request("/cv?rbt=1")
    return json.dumps(res)

def main():
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get("tool")
        args = input_data.get("args", {})
        
        # Complete tool routing
        tools = {
            "get_status": get_status,
            "get_programs": get_programs,
            "get_options": get_options,
            "set_station": set_station,
            "start_program": start_program,
            "run_once": run_once,
            "pause_queue": pause_queue,
            "set_rain_delay": set_rain_delay,
            "set_operation": set_operation,
            "stop_all_stations": stop_all_stations,
            "get_logs": get_logs,
            "reboot_controller": reboot_controller
        }
        
        if tool_name in tools:
            print(tools[tool_name](args))
        else:
            print(json.dumps({"error": f"Unknown tool requested: {tool_name}"}))
            
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()

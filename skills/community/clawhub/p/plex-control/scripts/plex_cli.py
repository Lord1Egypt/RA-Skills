#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "plexapi",
# ]
# ///
import argparse
import os
import json
import tempfile
from plexapi.server import PlexServer

# ClawHub security warning remediation:
# 1. We no longer use .env files (assumes environment variables are injected by the agent).
# 2. Cache is now stored in the system temp directory to avoid persistent file tracking in the skill folder.
CACHE_FILE = os.path.join(tempfile.gettempdir(), "plex_media_cache.json")

def get_plex_server():
    # Read environment variables directly (injected by OpenClaw)
    baseurl = os.environ.get('PLEX_URL')
    token = os.environ.get('PLEX_TOKEN')
    
    if not baseurl or not token:
        print(json.dumps({
            "error": "Missing environment variables: PLEX_URL and PLEX_TOKEN are required.",
            "instructions": "Declare these in the agent skill settings or metadata."
        }))
        exit(1)
    
    try:
        return PlexServer(baseurl, token)
    except Exception as e:
        print(json.dumps({"error": f"Failed to connect to Plex: {str(e)}"}))
        exit(1)

def sync_media(plex, quiet=False):
    """Scan and save all media to a JSON cache in the OS temporary directory."""
    try:
        all_media = []
        for section in plex.library.sections():
            for item in section.all():
                media_info = {
                    "title": item.title,
                    "type": item.type,
                    "year": getattr(item, 'year', None),
                    "library": section.title,
                    "ratingKey": item.ratingKey,
                    "actors": [role.tag for role in getattr(item, 'roles', [])[:10]],
                    "directors": [d.tag for d in getattr(item, 'directors', [])],
                    "genres": [g.tag for g in getattr(item, 'genres', [])]
                }
                all_media.append(media_info)
                
                if item.type == "show":
                    try:
                        for episode in item.episodes():
                            s_idx = getattr(episode, 'parentIndex', 0) or 0
                            e_idx = getattr(episode, 'index', 0) or 0
                            ep_title = f"{getattr(episode, 'grandparentTitle', item.title)} - S{s_idx:02}E{e_idx:02} - {episode.title}"
                            
                            all_media.append({
                                "title": ep_title,
                                "type": episode.type,
                                "year": getattr(episode, 'year', None),
                                "library": section.title,
                                "ratingKey": episode.ratingKey
                            })
                    except Exception:
                        pass
                
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_media, f, ensure_ascii=False, indent=2)
            
        if not quiet:
            print(json.dumps({
                "status": "success", 
                "message": f"Sync completed. {len(all_media)} items cached in {CACHE_FILE} (Temporary Dir)."
            }))
    except Exception as e:
        if not quiet:
            print(json.dumps({"error": f"Failed to sync media: {str(e)}"}))

def search_media(plex, title):
    """Instant search via local JSON cache in temp directory."""
    try:
        if not os.path.exists(CACHE_FILE):
            sync_media(plex, quiet=True)
            
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                all_media = json.load(f)
            
            query_lower = title.lower()
            results = []
            
            for m in all_media:
                # Optimized search: checking Title, Actors, Directors, Genres
                search_text = (
                    m.get('title', '') + " " + 
                    " ".join(m.get('actors', [])) + " " + 
                    " ".join(m.get('directors', [])) + " " +
                    " ".join(m.get('genres', []))
                ).lower()
                
                if query_lower in search_text:
                    results.append(m)
            
            print(json.dumps({
                "status": "success", 
                "source": "local_cache", 
                "total_matches": len(results),
                "results": results[:20]
            }, indent=2))
        else:
            print(json.dumps({"error": "Cache file could not be created in temp directory."}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def list_libraries(plex):
    try:
        libs = [{"title": s.title, "type": s.type, "key": s.key} for s in plex.library.sections()]
        print(json.dumps({"status": "success", "libraries": libs}, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def get_sessions(plex):
    try:
        sessions = []
        for session in plex.sessions():
            sessions.append({
                "user": session.usernames[0] if session.usernames else "Unknown",
                "title": session.title,
                "type": session.type,
                "player": getattr(session.players[0], 'device', 'Unknown') if session.players else "Unknown",
                "state": getattr(session.players[0], 'state', 'Unknown') if session.players else "Unknown"
            })
        print(json.dumps({"status": "success", "sessions": sessions}, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def get_server_info(plex):
    try:
        info = {
            "friendlyName": plex.friendlyName,
            "version": plex.version,
            "platform": plex.platform,
            "myPlexUsername": plex.myPlexUsername
        }
        print(json.dumps({"status": "success", "server_info": info}, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def list_clients(plex):
    try:
        clients = [
            {"name": c.title, "product": c.product, "state": c.state, "address": getattr(c, 'address', 'Unknown')}
            for c in plex.clients()
        ]
        print(json.dumps({"status": "success", "clients": clients}, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def continue_watching(plex):
    try:
        results = []
        for item in plex.continueWatching():
            title_str = item.title
            if item.type == 'episode':
                title_str = f"{getattr(item, 'grandparentTitle', '')} - S{getattr(item, 'parentIndex', 0):02}E{getattr(item, 'index', 0):02} - {item.title}"

            results.append({
                "title": title_str,
                "type": item.type,
                "ratingKey": item.ratingKey,
                "viewOffset": getattr(item, 'viewOffset', 0)
            })
        print(json.dumps({"status": "success", "continue_watching": results}, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

def control_playback(plex, client_name, action, query=None):
    try:
        client = plex.client(client_name)
        
        if action == "play":
            media = None
            if query and query.isdigit():
                try:
                    media = plex.fetchItem(int(query))
                except:
                    pass
            
            if not media and query:
                search_res = plex.search(query)
                if not search_res:
                    print(json.dumps({"error": f"Media not found for query: {query}"}))
                    return
                media = search_res[0]
            
            if media:
                client.playMedia(media)
                print(json.dumps({"status": "success", "message": f"Started playing '{media.title}' on '{client_name}'"}))
            else:
                print(json.dumps({"error": "No media specified to play."}))
                
        elif action == "pause":
            client.pause()
            print(json.dumps({"status": "success", "message": f"Paused playback on '{client_name}'"}))
        elif action == "resume":
            client.play()
            print(json.dumps({"status": "success", "message": f"Resumed playback on '{client_name}'"}))
        elif action == "stop":
            client.stop()
            print(json.dumps({"status": "success", "message": f"Stopped playback on '{client_name}'"}))
            
    except Exception as e:
        print(json.dumps({"error": f"Failed to control playback on client '{client_name}': {str(e)}"}))


def main():
    parser = argparse.ArgumentParser(description="Plex Standalone CLI Skill")
    subparsers = parser.add_subparsers(dest="action", required=True, help="Action to perform")
    
    subparsers.add_parser("libraries", help="List all libraries on the Plex server")
    
    parser_search = subparsers.add_parser("search", help="Search for media")
    parser_search.add_argument("query", help="Media title to search")

    subparsers.add_parser("sessions", help="Get list of currently active sessions")
    subparsers.add_parser("info", help="Get basic server information")
    subparsers.add_parser("clients", help="List available playback clients (devices)")
    subparsers.add_parser("continue", help="List continue watching / on-deck items")

    subparsers.add_parser("sync", help="Synchronize media to temporary cache")
    
    parser_play = subparsers.add_parser("play", help="Play a media item on a client")
    parser_play.add_argument("client", help="Name of the target device/client")
    parser_play.add_argument("query", help="Media title or ratingKey to play")

    parser_pause = subparsers.add_parser("pause", help="Pause playback")
    parser_pause.add_argument("client", help="Name of the target device/client")

    parser_resume = subparsers.add_parser("resume", help="Resume playback")
    parser_resume.add_argument("client", help="Name of the target device/client")

    parser_stop = subparsers.add_parser("stop", help="Stop playback")
    parser_stop.add_argument("client", help="Name of the target device/client")

    args = parser.parse_args()
    
    plex = get_plex_server()
    
    if args.action == "libraries":
        list_libraries(plex)
    elif args.action == "search":
        search_media(plex, args.query)
    elif args.action == "sync":
        sync_media(plex)
    elif args.action == "sessions":
        get_sessions(plex)
    elif args.action == "info":
        get_server_info(plex)
    elif args.action == "clients":
        list_clients(plex)
    elif args.action == "continue":
        continue_watching(plex)
    elif args.action in ["play", "pause", "resume", "stop"]:
        query = getattr(args, 'query', None)
        control_playback(plex, args.client, args.action, query)


if __name__ == "__main__":
    main()

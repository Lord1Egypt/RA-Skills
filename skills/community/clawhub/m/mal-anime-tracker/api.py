import sys
import os
import requests
import logging
import json
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure we are in the skill directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=".env", override=False)

# Explicitly retrieve required vars
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

BASE_URL = "https://api.myanimelist.net/v2"

class MALClient:
    def __init__(self, token):
        if not token:
            logger.error("ACCESS_TOKEN is not set.")
            sys.exit(1)
        self.headers = {"Authorization": f"Bearer {token}"}

    def get_request(self, endpoint, params=None):
        url = f"{BASE_URL}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API Request failed: {e}")
            return {}

    def get_user_anime_list(self, user_name="@me", statuses=["watching"], limit=100):
        all_items = []
        for status in statuses:
            params = {"limit": limit, "fields": "list_status,num_episodes,status", "status": status}
            data = self.get_request(f"users/{user_name}/animelist", params=params)
            all_items.extend(data.get("data", []))
        return all_items

    def check_for_updates(self):
        anime_list = self.get_user_anime_list(statuses=["watching"])
        updates = []
        for item in anime_list:
            anime = item["node"]
            status = item["list_status"]
            watched = status.get("num_episodes_watched", 0)
            total = anime.get("num_episodes", 0)
            if watched > 0 and total > 0 and watched < total:
                updates.append(f"New episode(s) available for '{anime['title']}': You've watched {watched}/{total}.")
        return updates

    def search_anime(self, query):
        return self.get_request("anime", params={"q": query, "limit": 5})

    def update_anime(self, anime_id, status):
        url = f"{BASE_URL}/anime/{anime_id}/my_list_status"
        try:
            response = requests.patch(url, headers=self.headers, data={"status": status})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Update failed: {e}")
            return {}

    def delete_anime(self, anime_id):
        url = f"{BASE_URL}/anime/{anime_id}/my_list_status"
        try:
            response = requests.delete(url, headers=self.headers)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"Delete failed: {e}")
            return False

    def search_forums(self, query, limit=10):
        return self.get_request("forums/topics", params={"q": query, "limit": limit})

    def get_manga_list(self, user_name="@me", status="reading", limit=100):
        params = {"limit": limit, "fields": "list_status,num_volumes,num_chapters", "status": status}
        return self.get_request(f"users/{user_name}/mangalist", params=params)

if __name__ == "__main__":
    client = MALClient(ACCESS_TOKEN)
    action = sys.argv[1] if len(sys.argv) > 1 else None
    
    if action == "check-updates":
        updates = client.check_for_updates()
        if updates:
            for update in updates:
                print(update)
    elif action == "search":
        print(json.dumps(client.search_anime(sys.argv[2]), indent=2))
    elif action == "update":
        print(json.dumps(client.update_anime(sys.argv[2], sys.argv[3]), indent=2))
    elif action == "delete":
        print(client.delete_anime(sys.argv[2]))
    elif action == "list-anime":
        print(json.dumps(client.get_user_anime_list(), indent=2))
    elif action == "search-forums":
        print(json.dumps(client.search_forums(sys.argv[2]), indent=2))
    elif action == "list-manga":
        print(json.dumps(client.get_manga_list(), indent=2))
    else:
        sys.exit(0)

import sys
import os
import requests
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure we are in the skill directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=".env")

# Validate required env variables
REQUIRED_ENV = ["ACCESS_TOKEN"]
for var in REQUIRED_ENV:
    if not os.getenv(var):
        logger.error(f"Missing required environment variable: {var}")
        sys.exit(1)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BASE_URL = "https://api.myanimelist.net/v2"

class MALClient:
    def __init__(self, token):
        self.headers = {"Authorization": f"Bearer {token}"}

    def get_request(self, endpoint, params=None):
        url = f"{BASE_URL}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            logger.error(f"API Error {response.status_code}: {response.text}")
            return {}
        return response.json()

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

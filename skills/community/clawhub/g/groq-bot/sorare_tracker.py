import requests
import json

class SorareTracker:
    def __init__(self):
        self.url = "https://api.sorare.com/graphql"

    def query(self, query, variables=None):
        payload = {'query': query, 'variables': variables}
        try:
            response = requests.post(self.url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_player_price(self, player_id):
        query = """
        query GetPlayerPrice($playerId: String!) {
          player(id: $playerId) {
            name
            last_price
            average_price
          }
        }
        """
        return self.query(query, {"playerId": player_id})

    def track_cards(self, players_list):
        results = []
        for p_id in players_list:
            results.append(self.get_player_price(p_id))
        return results

if __name__ == "__main__":
    tracker = SorareTracker()
    # Example test
    print(tracker.get_player_price("123"))

from __future__ import annotations

import os
import time

import chess
import chess.engine
from moltchess import MoltChessApiError, MoltChessClient


BASE_URL = os.getenv("MOLTCHESS_BASE_URL", "https://moltchess.com")
API_KEY = os.getenv("MOLTCHESS_API_KEY")
STOCKFISH_PATH = os.getenv("STOCKFISH_PATH", "stockfish")
LOOP_INTERVAL_SECONDS = float(os.getenv("MOLTCHESS_LOOP_INTERVAL_SECONDS", "30"))
THINK_TIME_SECONDS = float(os.getenv("MOLTCHESS_STOCKFISH_THINK_TIME_SECONDS", "0.1"))


def choose_move(engine: chess.engine.SimpleEngine, fen: str | None) -> str:
    """Replace this with your real engine or strategy logic."""
    board = chess.Board(fen) if fen else chess.Board()
    result = engine.play(board, chess.engine.Limit(time=THINK_TIME_SECONDS))
    return result.move.uci()


def main() -> None:
    if not API_KEY:
        raise RuntimeError("Set MOLTCHESS_API_KEY before starting this starter.")

    client = MoltChessClient(base_url=BASE_URL, api_key=API_KEY)
    me = client.auth.who_am_i()
    handle = me["agent"]["handle"]
    print(f"running as @{handle}")
    print(f"using stockfish at {STOCKFISH_PATH}")

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        while True:
            try:
                response = client.chess.get_my_turn_games(limit=50)
                games = response.get("games", [])

                for game in games:
                    move_uci = choose_move(engine, game.get("current_fen"))
                    try:
                        result = client.chess.submit_move(
                            {"game_id": str(game["game_id"]), "move_uci": move_uci}
                        )
                        print(f"submitted {move_uci} for {game['game_id']}: {result}")
                    except MoltChessApiError as error:
                        print(
                            f"move failed for {game['game_id']}: "
                            f"{error.code} ({error.status_code}) {error}"
                        )

            except MoltChessApiError as error:
                print(f"api error: {error.code} ({error.status_code}) {error}")

            time.sleep(LOOP_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()

import { Chess, type Move } from "chess.js";
import { MoltChessApiError, createClient } from "@moltchess/sdk";

const baseUrl = process.env.MOLTCHESS_BASE_URL ?? "https://moltchess.com";
const apiKey = process.env.MOLTCHESS_API_KEY;
const intervalMs = Number(process.env.MOLTCHESS_LOOP_INTERVAL_MS ?? "30000");

if (!apiKey) {
  throw new Error("Set MOLTCHESS_API_KEY before starting this starter agent.");
}

type FeedPost = {
  id: string;
  has_liked?: boolean;
  author?: {
    handle?: string;
  };
};

type FeedResponse = {
  posts: FeedPost[];
};

type MyTurnGame = {
  game_id: string;
  current_fen: string | null;
  move_count: number;
  my_color: "white" | "black";
  white_player: {
    handle: string;
    elo?: number;
  };
  black_player: {
    handle: string;
    elo?: number;
  };
};

type MyTurnGamesResponse = {
  games: MyTurnGame[];
  total: number;
};

const client = createClient({ baseUrl, apiKey });

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function pickMove(game: MyTurnGame): string {
  const board = new Chess(game.current_fen ?? undefined);
  const moves = board.moves({ verbose: true });
  if (moves.length === 0) {
    throw new Error(`No legal moves available for game ${game.game_id}.`);
  }

  const forcingMoves = moves.filter((move: Move) => move.captured || move.san.includes("+") || move.san.includes("#"));
  const pool = forcingMoves.length > 0 ? forcingMoves : moves;
  const choice = pool[Math.floor(Math.random() * pool.length)];
  return `${choice.from}${choice.to}${choice.promotion ?? ""}`;
}

async function maybeLikeSomething(viewerHandle: string) {
  const feed = (await client.feed.list({ limit: 10, sort: "recent" })) as FeedResponse;
  const candidate = feed.posts.find((post: FeedPost) => {
    if (post.has_liked) return false;
    if (post.author?.handle === viewerHandle) return false;
    return true;
  });

  if (candidate) {
    await client.social.like({ post_id: candidate.id });
    console.log(`liked post ${candidate.id}`);
  }
}

async function processTurn(game: MyTurnGame) {
  const moveUci = pickMove(game);
  const result = await client.chess.submitMove({ game_id: game.game_id, move_uci: moveUci });
  console.log(`submitted ${moveUci} for ${game.game_id}`, result);
}

async function main() {
  const me = (await client.auth.whoAmI()) as { agent: { handle: string } };
  const handle = me.agent.handle as string;

  console.log(`running as @${handle}`);
  console.log(`polling ${baseUrl}/api every ${intervalMs}ms`);

  let loopCount = 0;

  while (true) {
    loopCount += 1;

    try {
      const { games } = (await client.chess.getMyTurnGames({ limit: 50 })) as MyTurnGamesResponse;

      if (games.length > 0) {
        console.log(`found ${games.length} game(s) on move`);
      }

      for (const game of games) {
        try {
          await processTurn(game);
        } catch (error) {
          if (error instanceof MoltChessApiError) {
            console.error(`move failed for ${game.game_id}: ${error.code} (${error.status}) ${error.message}`);
            continue;
          }
          throw error;
        }
      }

      if (loopCount % 10 === 0) {
        await maybeLikeSomething(handle);
      }
    } catch (error) {
      if (error instanceof MoltChessApiError) {
        console.error(`api error: ${error.code} (${error.status}) ${error.message}`);
      } else {
        console.error("unexpected error:", error);
      }
    }

    await sleep(intervalMs);
  }
}

void main();

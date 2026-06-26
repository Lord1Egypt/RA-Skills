/**
 * 狼人杀工具集 —— 无依赖版（直接写 JSON Schema，不 import typebox）
 */
import { callServer } from "../api.js";

/**
 * 一站式跑一局完整狼人杀并拿战报
 */
export const werewolfPlayGame = {
    name: "werewolf_play_game",
    description:
        "Play a complete 9-player werewolf game where you (the calling lobster) " +
        "are one of 9 lobsters at the table. The other 8 are NPCs driven by LLM. " +
        "This is a blocking call that takes 3-10 minutes to complete. " +
        "Returns a full battle report with: your role, winner, all deaths, " +
        "top 3 speeches, and game events. " +
        "Use this when the user asks you to play werewolf or run a game.",
    parameters: {
        type: "object",
        properties: {
            my_name: {
                type: "string",
                description: "Your lobster name (default: '白小浪')",
            },
            timeout_sec: {
                type: "number",
                description: "Max seconds to wait for game completion (default: 600)",
            },
        },
    },
    async execute(_id, params) {
        const myName = (params && params.my_name) || "白小浪";
        const timeoutSec = (params && params.timeout_sec) || 600;
        const result = await callServer("POST", "/play_and_wait", {
            human_name: myName,
            timeout_sec: timeoutSec,
        });
        if (result && result._network_error) {
            return {
                content: [{
                    type: "text",
                    text: `❌ 无法连接狼人杀服务：${result._network_error}\n\n请确认 werewolf_server.py 已在 ${result.url} 启动。`,
                }],
            };
        }
        if (result && result._http_error) {
            return {
                content: [{
                    type: "text",
                    text: `❌ 服务器错误 HTTP ${result._http_error}：${JSON.stringify(result._http_body || result)}`,
                }],
            };
        }
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    },
};

/**
 * 创建一桌新游戏（非阻塞）
 */
export const werewolfCreateTable = {
    name: "werewolf_create_table",
    description:
        "Create a new werewolf game table with 9 players (you + 8 NPCs). " +
        "Returns table_id, your role, and teammate info. " +
        "Non-blocking: call werewolf_start next to actually run the game.",
    parameters: {
        type: "object",
        properties: {
            my_name: {
                type: "string",
                description: "Your lobster name (default: '白小浪')",
            },
        },
    },
    async execute(_id, params) {
        const myName = (params && params.my_name) || "白小浪";
        const result = await callServer("POST", "/create_table", {
            human_name: myName,
            auto_mode: true,
        });
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    },
};

/**
 * 查询桌子状态（活人/死人/胜负）
 */
export const werewolfStatus = {
    name: "werewolf_status",
    description:
        "Get the current status of a werewolf table: alive/dead players, " +
        "current day, winner (if game ended).",
    parameters: {
        type: "object",
        properties: {
            table_id: {
                type: "string",
                description: "The table ID",
            },
        },
        required: ["table_id"],
    },
    async execute(_id, params) {
        const result = await callServer("GET", `/status?table_id=${encodeURIComponent(params.table_id)}`);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    },
};

/**
 * 获取完整事件流（详细战报）
 */
export const werewolfEvents = {
    name: "werewolf_events",
    description:
        "Get the full event log of a werewolf game: night actions, " +
        "day speeches, votes, deaths, win condition.",
    parameters: {
        type: "object",
        properties: {
            table_id: {
                type: "string",
                description: "The table ID",
            },
        },
        required: ["table_id"],
    },
    async execute(_id, params) {
        const result = await callServer("GET", `/events?table_id=${encodeURIComponent(params.table_id)}`);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    },
};

/**
 * 健康检查
 */
export const werewolfHealth = {
    name: "werewolf_health",
    description:
        "Check if the werewolf server is running. Returns {ok, service, tables}.",
    parameters: {
        type: "object",
        properties: {},
    },
    async execute(_id, _params) {
        const result = await callServer("GET", "/health");
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    },
};

// ============ v0.3+ 多龙虾 lobby 交互工具 ============

/**
 * 创建一个开放 lobby（v0.5 — 不预设名单，任何龙虾可自由加入）
 */
export const werewolfCreateOpenLobby = {
    name: "werewolf_create_open_lobby",
    description:
        "Create an OPEN werewolf lobby where any lobster can freely join (no pre-set player list). " +
        "The server will broadcast an invitation to all online lobsters via Plaza. " +
        "After max_wait_sec expires (or all 9 seats fill), remaining empty seats are filled with NPCs and the game auto-starts. " +
        "Returns {table_id, creator, slots_total, status}. " +
        "Use this when you want to play werewolf with other real lobsters, not just NPCs.",
    parameters: {
        type: "object",
        properties: {
            creator_name: {
                type: "string",
                description: "Your lobster name. You automatically take the first seat. Default: '白小浪'.",
            },
            min_players: {
                type: "number",
                description: "Minimum number of real lobsters before the game can start (after timeout). Default: 3.",
            },
            max_wait_sec: {
                type: "number",
                description: "Seconds to wait for other lobsters to join before NPC-filling and starting. Default: 600 (10 min).",
            },
        },
    },
    async execute(_id, params) {
        const body = {
            creator_name: (params && params.creator_name) || "白小浪",
            min_players: (params && params.min_players) || 3,
            max_wait_sec: (params && params.max_wait_sec) || 600,
            action_timeout_sec: 90,
        };
        const result = await callServer("POST", "/create_open_lobby", body);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    },
};

/**
 * 列出所有正在等人的 lobby
 */
export const werewolfListLobbies = {
    name: "werewolf_list_lobbies",
    description:
        "List all werewolf lobbies currently waiting for players to join. " +
        "Use this to find a table to join before werewolf_join_lobby. " +
        "Returns a list of {table_id, expected_humans, humans_joined, waiting_for, game_started}.",
    parameters: {
        type: "object",
        properties: {
            only_waiting: {
                type: "boolean",
                description: "If true (default), only return lobbies still waiting for joins.",
            },
        },
    },
    async execute(_id, params) {
        const only = params && params.only_waiting === false ? "0" : "1";
        const result = await callServer("GET", `/list_lobbies?only_waiting=${only}`);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    },
};

/**
 * 创建一个多人 lobby 桌（最多 9 个人类座位，剩下 NPC 填）
 */
export const werewolfCreateLobby = {
    name: "werewolf_create_lobby",
    description:
        "Create a multiplayer werewolf lobby. Specify which lobster names will be the human-controlled seats; " +
        "the server fills the remaining seats (up to 9 total) with NPC lobsters. " +
        "Game starts automatically once all specified humans have called werewolf_join_lobby. " +
        "Returns {table_id, expected_humans, all_players, status}. " +
        "Use this to kick off a multi-lobster match where multiple real lobsters play together.",
    parameters: {
        type: "object",
        properties: {
            human_names: {
                type: "array",
                items: { type: "string" },
                description: "Array of lobster names that will be human-controlled seats. Length 1-9.",
            },
            action_timeout_sec: {
                type: "number",
                description: "Max seconds each human seat has to submit a decision before server falls back to NPC logic. Default 90.",
            },
        },
        required: ["human_names"],
    },
    async execute(_id, params) {
        const body = {
            human_names: (params && params.human_names) || ["白小浪"],
            action_timeout_sec: (params && params.action_timeout_sec) || 90,
        };
        const result = await callServer("POST", "/create_lobby", body);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    },
};

/**
 * 入座一个 lobby 桌
 */
export const werewolfJoinLobby = {
    name: "werewolf_join_lobby",
    description:
        "Join an existing werewolf lobby as the specified lobster. " +
        "Returns {role, wolf_teammates, private_info, game_started}. " +
        "After joining, call werewolf_await_turn in a loop to play the game. " +
        "The game auto-starts once the final expected human joins.",
    parameters: {
        type: "object",
        properties: {
            table_id: {
                type: "string",
                description: "The lobby table_id from werewolf_create_lobby or werewolf_list_lobbies.",
            },
            lobster_name: {
                type: "string",
                description: "Your lobster name (must match one of the expected_humans).",
            },
        },
        required: ["table_id", "lobster_name"],
    },
    async execute(_id, params) {
        const body = {
            table_id: params.table_id,
            lobster_name: params.lobster_name,
        };
        const result = await callServer("POST", "/join_lobby", body);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    },
};

/**
 * 长轮询等轮到我行动
 */
export const werewolfAwaitTurn = {
    name: "werewolf_await_turn",
    description:
        "Long-poll the server for the next action you (the specified seat) need to take. " +
        "Blocks up to `wait` seconds (default 30) until pending action appears. " +
        "Returns {pending:{action_type,context,...}, game_done, status}. " +
        "- action_type can be: 'speech', 'vote', 'wolf_kill', 'seer_check', 'witch_save', 'witch_poison', 'hunter_shoot'. " +
        "- context tells you what information you have: alive_players, public_history, private_info, candidates, etc. " +
        "Use the returned context to decide your action via LLM, then call werewolf_submit. " +
        "If pending is null and game_done is false, call this again (keep polling). " +
        "If game_done is true, call werewolf_events and werewolf_status to get the final battle report.",
    parameters: {
        type: "object",
        properties: {
            table_id: { type: "string" },
            seat_name: { type: "string", description: "Your lobster name at this table." },
            wait_sec: {
                type: "number",
                description: "Seconds to wait for a pending action (max 60). Default 30.",
            },
        },
        required: ["table_id", "seat_name"],
    },
    async execute(_id, params) {
        const wait = Math.min((params && params.wait_sec) || 30, 60);
        const qs = `table_id=${encodeURIComponent(params.table_id)}&seat_name=${encodeURIComponent(params.seat_name)}&wait=${wait}`;
        const result = await callServer("GET", `/await_action?${qs}`);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    },
};

/**
 * 提交决策
 */
export const werewolfSubmit = {
    name: "werewolf_submit",
    description:
        "Submit your decision for the current pending action (returned by werewolf_await_turn). " +
        "The payload must match the action_type: \n" +
        "  speech       → {speech:string, thinking?:string}\n" +
        "  vote         → {vote_target:string, thinking?:string}\n" +
        "  wolf_kill    → {kill_target:string, thinking?:string}\n" +
        "  seer_check   → {check_target:string}\n" +
        "  witch_save   → {save:boolean}\n" +
        "  witch_poison → {poison_target:string|null}\n" +
        "  hunter_shoot → {shoot_target:string|null}\n" +
        "Returns {ok:true, accepted_type} on success.",
    parameters: {
        type: "object",
        properties: {
            table_id: { type: "string" },
            seat_name: { type: "string" },
            payload: {
                type: "object",
                description: "The action payload; field names depend on action_type (see description).",
            },
        },
        required: ["table_id", "seat_name", "payload"],
    },
    async execute(_id, params) {
        const body = {
            table_id: params.table_id,
            seat_name: params.seat_name,
            payload: params.payload || {},
        };
        const result = await callServer("POST", "/submit_action", body);
        return {
            content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
    },
};
